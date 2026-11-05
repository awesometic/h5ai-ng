#!/usr/bin/env python3
"""Exercise a built image through Nginx/FPM using disposable Docker volumes."""
import base64
import http.cookiejar
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import time
import urllib.error
import urllib.request
import uuid
import zipfile


def docker(*args, timeout=60, merge_stderr=False):
    return subprocess.check_output(["docker", *args], text=True, timeout=timeout,
                                   stderr=subprocess.STDOUT if merge_stderr else None).strip()


def docker_logs(tail=200):
    return docker("logs", "--tail", str(tail), name, timeout=5, merge_stderr=True)


def best_effort_docker(*args, quiet=False):
    try:
        subprocess.run(["docker", *args], check=True, timeout=30,
                       stdout=subprocess.DEVNULL if quiet else None)
    except (OSError, subprocess.SubprocessError) as error:
        print(f"Docker diagnostics/cleanup failed: {error}", file=sys.stderr)


if not __debug__:
    raise SystemExit("Run without -O or PYTHONOPTIMIZE; this test requires assertions")
if len(sys.argv) != 3:
    raise SystemExit("Usage: python3 tests/smoke.py IMAGE PLATFORM")
image, platform = sys.argv[1:]
MIN_PHP_VERSION_ID = 80512  # Minimum patched runtime for the October 21, 2026 release.
name = "h5ai-smoke-" + uuid.uuid4().hex[:10]
volumes = [name + "-config", name + "-files", name + "-logs"]
opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({}),
    urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),
)


def request(path="/", data=None, auth=False, headers=None):
    headers = {"User-Agent": "h5ai-smoke", **(headers or {})}
    if auth:
        headers["Authorization"] = "Basic " + base64.b64encode(b"smoke:test-password").decode()
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url + path, json.dumps(data).encode() if data is not None else None, headers)
    try:
        with opener.open(req, timeout=20) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def api(data, auth=False):
    status, body = request("/_h5ai/public/index.php", data, auth)
    assert status == 200, (status, body[:300])
    result = json.loads(body)
    assert "err" not in result, result
    return result


def wait_for_logs(markers, timeout=30):
    paths = {
        "nginx_access": "/logs/nginx/access.log",
        "nginx_error": "/logs/nginx/error.log",
        "php_error": "/logs/php/error.log",
    }
    deadline = time.monotonic() + timeout
    while True:
        files = {}
        for stream, path in paths.items():
            try:
                files[stream] = docker("exec", name, "cat", path, timeout=5)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                files[stream] = ""
        container_logs = docker_logs()
        if (all(marker in files[stream] for stream, marker in markers.items())
                and all(marker in container_logs for marker in markers.values())):
            return files
        assert time.monotonic() < deadline, (
            "Service logs did not reach files and docker logs", markers, files, container_logs[-2000:])
        time.sleep(0.5)


def archive_paths(stream):
    directory, basename = {
        "nginx_access": ("/logs/nginx", "access.log"),
        "nginx_error": ("/logs/nginx", "error.log"),
        "php_error": ("/logs/php", "error.log"),
    }[stream]
    result = docker("exec", name, "find", directory, "-maxdepth", "1", "-type", "f",
                    "-name", basename + "-*", timeout=5)
    return result.splitlines() if result else []


def log_file_contents(path):
    reader = ["gzip", "-cd"] if path.endswith(".gz") else ["cat"]
    return docker("exec", name, *reader, path, timeout=5)


def wait_for_archived_logs(markers, timeout=30):
    deadline = time.monotonic() + timeout
    while True:
        archived = {}
        for stream, marker in markers.items():
            archived[stream] = any(
                marker in log_file_contents(path) for path in archive_paths(stream))
        if all(archived.values()):
            return
        assert time.monotonic() < deadline, ("Rotation did not preserve log records", markers, archived)
        time.sleep(0.5)


def set_last_rotation_days_ago(days):
    date = docker("exec", name, "php", "-r",
                  '$date = new DateTimeImmutable("now", new DateTimeZone(getenv("TZ")));'
                  'echo $date->modify("-' + str(days) + ' days")->format("Y-m-d");')
    docker("exec", name, "sh", "-c",
           "printf 'last=%s\\n' '" + date + "' > /logs/.state/last-rotation")


def create_archive_fixture(age_days, content):
    epoch = int(time.time()) - age_days * 86400
    date = docker("exec", name, "php", "-r",
                  f'$date = (new DateTimeImmutable("@{epoch}"))'
                  '->setTimezone(new DateTimeZone(getenv("TZ")));'
                  'echo $date->format("Ymd");')
    path = f"/logs/nginx/access.log-{date}-{epoch}"
    docker("exec", name, "sh", "-c",
           "printf '%s\\n' '" + content + "' > '" + path + "'")
    return path


def run_log_tick(success=True):
    # cron runs the same tick every minute; a tick that finds the lock taken exits 1 without output
    deadline = time.monotonic() + 30
    while True:
        result = subprocess.run(["docker", "exec", name, "/usr/local/bin/h5ai-logs", "tick"],
                                capture_output=True, text=True, timeout=15)
        busy = result.returncode == 1 and not result.stdout and not result.stderr
        if not busy or time.monotonic() >= deadline:
            break
        print("Log tick lock is busy; retrying")
        time.sleep(1)
    assert (result.returncode == 0) is success, (result.returncode, result.stdout, result.stderr)
    return result


def assert_invalid_log_interval_rejected():
    result = subprocess.run([
        "docker", "run", "--rm", "--platform", platform,
        "-e", "LOG_ROTATE_INTERVAL_DAYS=0",
        "--entrypoint", "/usr/local/bin/h5ai-logs", image, "prepare",
    ], capture_output=True, text=True, timeout=30)
    assert result.returncode != 0 and "LOG_ROTATE_INTERVAL_DAYS" in result.stderr, (
        "Invalid log rotation interval was accepted", result.returncode, result.stdout, result.stderr)


def assert_logs_read_only_as_service_user():
    docker("exec", name, "su", "-s", "/bin/sh", "-c", " && ".join([
        "test -r /logs && test -x /logs && ! test -w /logs",
        "test -r /logs/nginx && test -x /logs/nginx && ! test -w /logs/nginx",
        "test -r /logs/php && test -x /logs/php && ! test -w /logs/php",
        "! touch /logs/nginx/smoke-write-probe >/dev/null 2>&1",
        "! touch /logs/php/smoke-write-probe >/dev/null 2>&1",
        "test -r /logs/nginx/access.log && ! test -w /logs/nginx/access.log",
        "test -r /logs/nginx/error.log && ! test -w /logs/nginx/error.log",
        "test -r /logs/php/error.log && ! test -w /logs/php/error.log",
        "! sh -c 'printf x >> /logs/nginx/access.log' >/dev/null 2>&1",
        "! sh -c 'printf x >> /logs/nginx/error.log' >/dev/null 2>&1",
        "! sh -c 'printf x >> /logs/php/error.log' >/dev/null 2>&1",
        "! rm /logs/nginx/access.log >/dev/null 2>&1",
        "! rm /logs/nginx/error.log >/dev/null 2>&1",
        "! rm /logs/php/error.log >/dev/null 2>&1",
    ]), "abc")


def start(auth=False, timezone="Asia/Seoul", rotate_interval=None):
    command = ["run", "-d", "--platform", platform, "--name", name,
           "-p", "127.0.0.1::80", "-v", volumes[0] + ":/config",
           "-v", volumes[1] + ":/h5ai", "-v", volumes[2] + ":/logs",
           "-e", "PUID=1234", "-e", "PGID=2345",
           "-e", "TZ=" + timezone, "-e", "HTPASSWD=" + str(auth).lower(),
           "-e", "HTPASSWD_USER=smoke", "-e", "HTPASSWD_PW=test-password"]
    if rotate_interval is not None:
        command.extend(["-e", "LOG_ROTATE_INTERVAL_DAYS=" + str(rotate_interval)])
    docker(*command, image)
    wait_ready(auth)


def wait_ready(auth=False):
    global url
    url = "http://" + docker("port", name, "80/tcp")
    deadline = time.monotonic() + 45
    while True:
        try:
            status, body = request(auth=auth)
            if status == 200 and b"powered by h5ai" in body:
                return
        except (OSError, urllib.error.URLError):
            pass
        assert time.monotonic() < deadline, "Nginx/FPM did not become ready"
        time.sleep(0.5)


try:
    assert_invalid_log_interval_rejected()
    startup = subprocess.run(["docker", "run", "--rm", "--platform", platform,
                              "--entrypoint", "php", image, "-v"],
                             capture_output=True, text=True, timeout=60)
    assert startup.returncode == 0 and not startup.stderr, startup.stderr
    for volume in volumes:
        docker("volume", "create", volume)
    # Start from an Nginx configuration saved by docker-h5ai, which served /_h5ai/private/
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "h5ai.conf")) as conf:
        legacy_conf = conf.read().replace("location ^~ /_h5ai/ {", "location /_h5ai/ {")
    legacy_conf = re.sub(r"\n\n        # config and caches.*?\n        }\n", "\n", legacy_conf, flags=re.S)
    assert "_h5ai/private" not in legacy_conf and "location /_h5ai/ {" in legacy_conf, legacy_conf
    subprocess.run(["docker", "run", "--rm", "-i", "--platform", platform, "-v", volumes[0] + ":/config",
                    "--entrypoint", "sh", image, "-c", "mkdir -p /config/nginx /config/h5ai"
                    " && cat > /config/nginx/h5ai.conf"
                    # and from an h5ai 0.30.0 application copy, which an upgrade must replace
                    " && cp -a /usr/share/h5ai-default/_h5ai /config/h5ai/"
                    " && sed -i '1s/v[0-9][^ ]*/v0.30.0/' /config/h5ai/_h5ai/private/conf/options.json"
                    " /config/h5ai/_h5ai/public/js/scripts.js"
                    # whose options.json the upgrade keeps, old header included
                    " && printf '\\n// smoke: kept from 0.30.0\\n' >> /config/h5ai/_h5ai/private/conf/options.json"
                    " && touch /config/h5ai/_h5ai/stale-0.30.0"],
                   input=legacy_conf, text=True, check=True, timeout=60)
    start()
    docker("exec", name, "nginx", "-t")
    assert request("/_h5ai/private/conf/options.json")[0] == 403, "Private h5ai files are served"
    assert docker("exec", name, "sh", "-c", "ls /config/*_h5ai.conf.bak"), "Saved Nginx configuration was not backed up"
    docker("exec", name, "test", "!", "-e", "/config/h5ai/_h5ai/stale-0.30.0")
    assert docker("exec", name, "sh", "-c", "ls /config/*_options.json.bak"), "Saved options were not backed up"
    docker("exec", name, "grep", "-q", "smoke: kept from 0.30.0", "/config/h5ai/_h5ai/private/conf/options.json")
    docker("exec", name, "sh", "-c", "mkdir -p /h5ai/_h5ai/private && printf '<?php echo 42;' > /h5ai/_h5ai/private/probe.php")
    assert request("/_h5ai/private/probe.php")[0] == 403, "PHP under /_h5ai/private/ escapes the deny rule"
    docker("exec", name, "rm", "-r", "/h5ai/_h5ai")
    startup_logs = docker_logs()
    assert "HTPASSWD_PW=test-password" not in startup_logs, "Startup logs exposed the password environment variable"
    cli = docker("exec", name, "php", "-r", "echo PHP_VERSION;")

    probe = '''<?php
    echo json_encode([
        'version' => PHP_VERSION, 'version_id' => PHP_VERSION_ID, 'sapi' => PHP_SAPI,
        'timezone' => date_default_timezone_get(),
        'extensions' => array_map('extension_loaded', ['session', 'json', 'xml',
            'mbstring', 'exif', 'intl', 'gd', 'imagick', 'zip', 'Zend OPcache']),
        'opcache' => opcache_get_status(false),
    ]);
    '''
    subprocess.run(["docker", "exec", "-i", name, "sh", "-c", "cat > /h5ai/runtime.php"],
                   input=probe, text=True, check=True, timeout=60)
    docker("exec", name, "php", "-r",
           'file_put_contents("/h5ai/sample.txt", "h5ai smoke\\n");'
           '$im=imagecreatetruecolor(320,180); imagepng($im,"/h5ai/image.png");')
    docker("exec", name, "ffmpeg", "-v", "error", "-f", "lavfi", "-i",
           "color=c=blue:s=320x180:r=1:d=12", "-c:v", "mpeg4", "/h5ai/movie.mp4")
    # shorter than the 10 second capture point of a longer video
    docker("exec", name, "ffmpeg", "-v", "error", "-f", "lavfi", "-i",
           "color=c=blue:s=320x180:r=1:d=3", "-c:v", "mpeg4", "/h5ai/short.mp4")
    # written by hand so the fixture does not depend on the PDF support under test
    docker("exec", name, "sh", "-c", "printf '%s\\n' '%PDF-1.4' '1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj'"
           " '2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj'"
           " '3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 320 180]>>endobj'"
           " 'trailer<</Root 1 0 R>>' '%%EOF' > /h5ai/document.pdf")
    status, body = request("/runtime.php")
    assert status == 200, ("FPM runtime probe", status)
    runtime = json.loads(body)
    assert runtime["version"] == cli and runtime["sapi"] == "fpm-fcgi", runtime
    assert runtime["version_id"] >= MIN_PHP_VERSION_ID, ("PHP security baseline", runtime)
    assert runtime["timezone"] == "Asia/Seoul" and all(runtime["extensions"]), runtime
    assert runtime["opcache"]["opcache_enabled"], runtime
    if platform in ("linux/amd64", "linux/arm64"):
        assert runtime["opcache"]["jit"]["on"], runtime

    log_markers = {
        "nginx_access": "NGINX_ACCESS_" + uuid.uuid4().hex,
        "nginx_error": "NGINX_ERROR_" + uuid.uuid4().hex,
        "php_error": "PHP_ERROR_" + uuid.uuid4().hex,
    }
    assert request("/?smoke=" + log_markers["nginx_access"])[0] == 200
    assert request("/.ht/" + log_markers["nginx_error"])[0] == 403
    log_probe = "/h5ai/log-probe.php"
    docker("exec", name, "sh", "-c", "printf '%s\\n' "
           + "'<?php error_log(\"" + log_markers["php_error"] + "\"); echo \"ok\";' > " + log_probe)
    assert request("/log-probe.php") == (200, b"ok")
    wait_for_logs(log_markers)
    assert_logs_read_only_as_service_user()

    docker("exec", name, "sh", "-c",
           "printf keep > /tmp/log-state-target; "
           "ln -s /tmp/log-state-target /logs/.state/last-rotation.tmp")
    set_last_rotation_days_ago(2)
    run_log_tick()
    wait_for_archived_logs(log_markers)
    assert docker("exec", name, "cat", "/tmp/log-state-target") == "keep", "Rotation followed a state-file symlink"

    active_markers = {
        "nginx_access": "NGINX_ACCESS_AFTER_ROTATE_" + uuid.uuid4().hex,
        "nginx_error": "NGINX_ERROR_AFTER_ROTATE_" + uuid.uuid4().hex,
        "php_error": "PHP_ERROR_AFTER_ROTATE_" + uuid.uuid4().hex,
    }
    assert request("/?smoke=" + active_markers["nginx_access"])[0] == 200
    assert request("/.ht/" + active_markers["nginx_error"])[0] == 403
    docker("exec", name, "sh", "-c", "printf '%s\\n' "
           + "'<?php error_log(\"" + active_markers["php_error"] + "\"); echo \"ok\";' > " + log_probe)
    assert request("/log-probe.php") == (200, b"ok")
    wait_for_logs(active_markers)
    assert_logs_read_only_as_service_user()
    docker("exec", name, "rm", log_probe)

    assert request("/sample.txt") == (200, b"h5ai smoke\n")
    listing = api({"action": "get", "items": {"href": "/", "what": 1}})
    assert "/sample.txt" in {item["href"] for item in listing["items"]}, listing
    # a folder's items bring its own content and the folders above it without theirs
    docker("exec", name, "sh", "-c", "mkdir -p /h5ai/up/down && touch /h5ai/up/sibling.txt /h5ai/up/down/leaf.txt")
    nested = {item["href"]: item for item in api({"action": "get", "items": {"href": "/up/down/", "what": 1}})["items"]}
    assert "/up/down/leaf.txt" in nested, ("Content of the requested folder", sorted(nested))
    assert "/up/sibling.txt" not in nested and "/sample.txt" not in nested, ("Content of parent folders", sorted(nested))
    assert all(nested[href]["managed"] for href in ("/", "/up/", "/up/down/")), ("Parent folders for the breadcrumb", nested)
    assert not nested["/up/"]["fetched"] and nested["/up/down/"]["fetched"], nested
    deep = {item["href"] for item in api({"action": "get", "items": {"href": "/up/down/", "what": 2}})["items"]}
    assert {"/up/sibling.txt", "/sample.txt"} <= deep, ("Level 2 keeps the content of parent folders", sorted(deep))
    # folder redirects stay relative, so a mapped host port survives them
    status, body = request("/up")
    assert status == 200 and b"powered by h5ai" in body, ("Folder redirect", status)
    # a reverse proxy serving h5ai under /share/ names that path in X-Forwarded-Prefix
    share = {"X-Forwarded-Prefix": "/share"}
    status, body = request("/up/", headers=share)
    assert status == 200 and b"/share/_h5ai/public/css/styles.css" in body, ("Forwarded prefix in page", status)
    status, body = request("/_h5ai/public/index.php", {"action": "get", "items": {"href": "/share/up/", "what": 1}}, headers=share)
    shared = {item["href"] for item in json.loads(body)["items"]}
    assert status == 200 and "/share/up/down/" in shared, ("Forwarded prefix in items", status, sorted(shared))
    status, body = request(headers={"X-Forwarded-Prefix": '/x"><b>'})
    assert b'x"><b>' not in body and b"/_h5ai/public/css/styles.css" in body, "Unsafe forwarded prefix was used"
    requested_thumbs = [
        {"type": kind, "href": href, "width": 320, "height": 240}
        for kind, href in [("img", "/image.png"), ("mov", "/movie.mp4"), ("mov", "/short.mp4"),
                             ("doc", "/document.pdf")]
    ]
    thumbs = api({"action": "get", "thumbs": requested_thumbs})["thumbs"]
    assert isinstance(thumbs, list) and len(thumbs) == len(requested_thumbs), ("Missing thumbnails", thumbs)
    for thumb in thumbs:
        assert isinstance(thumb, str) and thumb.startswith("/_h5ai/"), thumbs
        status, body = request(thumb)
        assert status == 200 and body.startswith(b"\xff\xd8"), ("Thumbnail download", thumb, status)
        dimensions = subprocess.check_output(
            ["docker", "exec", "-i", name, "php", "-r",
             "$image = imagecreatefromstring(stream_get_contents(STDIN));"
             "if ($image === false) exit(1);"
             "echo json_encode([imagesx($image), imagesy($image)]);"],
            input=body, timeout=60,
        )
        assert json.loads(dimensions) == [320, 240], ("Thumbnail dimensions", thumb, dimensions)
    # sizes the interface never requests are refused, so the cache cannot grow without bound
    odd = api({"action": "get", "thumbs": [{"type": "img", "href": "/image.png", "width": 121, "height": 80}]})
    assert odd["thumbs"] == [None], ("Arbitrary thumbnail size", odd)
    for kind in ("php-tar", "shell-tar", "shell-zip"):
        print("Checking " + kind, flush=True)
        status, body = request("/_h5ai/public/index.php", {
            "action": "download", "type": kind, "as": "sample", "baseHref": "/",
            "hrefs": ["/sample.txt"],
        })
        assert status == 200, status
        archive = zipfile.ZipFile(io.BytesIO(body)) if kind == "shell-zip" else tarfile.open(fileobj=io.BytesIO(body))
        with archive:
            content = archive.read("sample.txt") if kind == "shell-zip" else archive.extractfile("sample.txt").read()
            assert content == b"h5ai smoke\n", kind

    options = "/config/h5ai/_h5ai/private/conf/options.json"
    docker("exec", name, "sh", "-c", "printf '\\n// smoke: preserve custom config\\n' >> " + options)
    before = docker("exec", name, "sha256sum", options)
    docker("rm", "-f", name)
    start(auth=True, timezone="UTC", rotate_interval=7)
    assert_logs_read_only_as_service_user()
    wait_for_logs(active_markers)
    for stream, marker in log_markers.items():
        assert any(marker in log_file_contents(path) for path in archive_paths(stream)), (
            "Rotated logs did not persist across container recreation", stream)
    set_last_rotation_days_ago(2)
    expired_marker = "EXPIRED_LOG_MARKER_" + uuid.uuid4().hex
    fresh_marker = "FRESH_LOG_MARKER_" + uuid.uuid4().hex
    expired_archive = create_archive_fixture(40, expired_marker)
    fresh_archive = create_archive_fixture(10, fresh_marker)
    unrelated = "/logs/nginx/unrelated.log"
    docker("exec", name, "sh", "-c", "printf '%s\\n' keep > " + unrelated)
    old_date, old_epoch = expired_archive.rsplit("-", 2)[-2:]
    symlink_archive = f"/logs/nginx/access.log-{old_date}-{int(old_epoch) - 1}"
    docker("exec", name, "ln", "-s", unrelated, symlink_archive)
    run_log_tick()
    docker("exec", name, "test", "!", "-e", expired_archive)
    assert fresh_marker in docker("exec", name, "cat", fresh_archive)
    assert docker("exec", name, "cat", unrelated) == "keep"
    docker("exec", name, "sh", "-c", "test -L '" + symlink_archive + "' && test -e '" + symlink_archive + "'")
    # The expiry fixture is not a valid archive for logrotate's compression pass.
    docker("exec", name, "rm", symlink_archive)
    for stream, marker in active_markers.items():
        active_path = {
            "nginx_access": "/logs/nginx/access.log",
            "nginx_error": "/logs/nginx/error.log",
            "php_error": "/logs/php/error.log",
        }[stream]
        assert marker in docker("exec", name, "cat", active_path), "Seven-day interval rotated early"

    crond_pid = docker("exec", name, "pidof", "crond")
    docker("exec", name, "kill", "-STOP", crond_pid)
    supervisor_pid = docker("exec", name, "cat", "/run/supervisord.pid")
    set_last_rotation_days_ago(8)
    # Signal the namespace init from Docker's host namespace so SIGSTOP takes effect.
    docker("kill", "--signal", "STOP", name)
    try:
        assert "State:\tT" in docker("exec", name, "cat", f"/proc/{supervisor_pid}/status"), "Supervisor was not stopped"
        failed_tick = run_log_tick(success=False)
        state = docker("exec", name, "cat", "/logs/.state/last-rotation")
        assert state.startswith("pending="), (
            "Failed reopen lost pending rotation state", state, failed_tick.stdout, failed_tick.stderr)
        wait_for_archived_logs(active_markers)
    finally:
        docker("kill", "--signal", "CONT", name)
    # Keep cron stopped until recreation so it cannot race the manual recovery tick.
    run_log_tick()

    for stream, marker in log_markers.items():
        compressed = [path for path in archive_paths(stream) if path.endswith(".gz")]
        assert compressed and any(marker in log_file_contents(path) for path in compressed), (
            "Delayed compression lost archived records", stream)

    recovered_markers = {
        "nginx_access": "NGINX_ACCESS_AFTER_RECOVERY_" + uuid.uuid4().hex,
        "nginx_error": "NGINX_ERROR_AFTER_RECOVERY_" + uuid.uuid4().hex,
        "php_error": "PHP_ERROR_AFTER_RECOVERY_" + uuid.uuid4().hex,
    }
    assert request("/?smoke=" + recovered_markers["nginx_access"], auth=True)[0] == 200
    assert request("/.ht/" + recovered_markers["nginx_error"], auth=True)[0] == 403
    docker("exec", name, "sh", "-c", "printf '%s\\n' "
           + "'<?php error_log(\"" + recovered_markers["php_error"] + "\"); echo \"ok\";' > " + log_probe)
    assert request("/log-probe.php", auth=True) == (200, b"ok")
    wait_for_logs(recovered_markers)

    assert request()[0] == 401 and request("/sample.txt")[0] == 401
    assert request("/sample.txt", auth=True) == (200, b"h5ai smoke\n")
    assert api({"action": "login", "pass": ""}, auth=True)["asAdmin"]
    setup = api({"action": "get", "setup": True, "refresh": True}, auth=True)["setup"]
    assert setup["AS_ADMIN"] and setup["PHP_VERSION"] == cli, ("Persisted login session", setup)
    assert docker("exec", name, "sha256sum", options) == before
    assert len(docker("exec", name, "sh", "-c", "ls /config/*_options.json.bak").split()) == 1, (
        "Recreating the container repeated the upgrade")
    assert docker("exec", name, "stat", "-c", "%u:%g", options) == "1234:2345"
    assert json.loads(request("/runtime.php", auth=True)[1])["timezone"] == "UTC"
    docker("rm", "-f", name)
    start()
    assert request("/sample.txt") == (200, b"h5ai smoke\n")

    conf_file, app_dir = "/config/nginx/h5ai.conf", "/config/h5ai/_h5ai"
    restored = f"test -f {conf_file} && test ! -L {conf_file} && test -d {app_dir} && test ! -L {app_dir}"
    # a saved file removed while the container exists comes back from the image's default on restart
    docker("exec", name, "rm", "-r", conf_file, app_dir)
    docker("restart", name, timeout=120)
    wait_ready()
    docker("exec", name, "sh", "-c", restored)
    assert request("/sample.txt") == (200, b"h5ai smoke\n")
    # a link to itself left in /config by an older image goes away when the new image starts
    docker("exec", name, "sh", "-c", f"rm -r {conf_file} {app_dir}"
           f" && ln -s {conf_file} {conf_file} && ln -s {app_dir} {app_dir}")
    docker("rm", "-f", name)
    start()
    docker("exec", name, "sh", "-c", restored)
    assert request("/_h5ai/private/conf/options.json")[0] == 403, "Private h5ai files are served"
    print(json.dumps({"image": image, "platform": platform, "php": cli,
                      "jit": runtime["opcache"].get("jit"), "result": "PASS"}))
except BaseException:
    best_effort_docker("logs", "--tail", "100", name)
    best_effort_docker("exec", name, "sh", "-c",
                       "cat /logs/nginx/error.log /logs/php/error.log 2>/dev/null; ps")
    raise
finally:
    best_effort_docker("rm", "-fv", name, quiet=True)
    for volume in volumes:
        best_effort_docker("volume", "rm", volume, quiet=True)
