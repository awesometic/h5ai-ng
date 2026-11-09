# h5ai-ng

**English** · [한국어](README.ko.md) · [Español](README.es.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md)

[![multiarch][arch-img]][docker-hub]
[![build][ci-img]][ci]

[![image size][size-img]][docker-hub]
[![docker pulls][pulls-img]][docker-hub]
[![docker stars][stars-img]][docker-hub]

A file index for Apache httpd, lighttpd and nginx. Visitors browse folders,
preview images, video, audio and text, filter by name and download a whole
selection as one archive. Your files stay where they are.

h5ai-ng is a maintained fork of [h5ai][h5ai] by Lars Jung, which stopped
releasing in 2021.

The [original site][h5ai] describes h5ai like this:

> h5ai is a modern file indexer for HTTP web servers with focus on your files. Directories are displayed in a appealing way and browsing them is enhanced by different views, a breadcrumb and a tree overview. Initially h5ai was an acronym for HTML5 Apache Index but now it supports other web servers too.

![h5ai-ng listing a folder in the details view](docs/screenshot.png)


## Why h5ai-ng

* **Read-only, no database.** It replaces the server's plain directory listing
  and never writes to your files.
* **Current PHP.** Runs on PHP 8.3 and later; the Docker image ships PHP 8.5.
* **No third-party requests.** The fonts ship with the interface, so a page
  load stays on your server.
* **Your h5ai setup carries over.** `options.json`, URLs and the `default` and
  `comity` icon themes keep working.


## Quick start with Docker

~~~sh
docker run -d --name h5ai -p 80:80 \
  -v /path/to/files:/h5ai \
  -v /path/to/config:/config \
  -e PUID=1000 -e PGID=1000 -e TZ=Europe/Berlin \
  --restart unless-stopped \
  awesometic/h5ai-ng
~~~

Open `http://localhost/`. Images are published for `linux/amd64`,
`linux/arm64`, `linux/arm/v7` and `linux/arm/v6`.

The image ships what the optional features need: image, video and PDF
thumbnails, tar and zip downloads and folder sizes. Log in to its info page
(`/_h5ai/public/index.php`) and every check passes:

![The info page of the Docker image with every check passed](docs/info-page.png)

| Volume | Contents |
| --- | --- |
| `/h5ai` | The files to serve. Mount it read-only (`:ro`) if you like. |
| `/config` | `h5ai/_h5ai` (the application and its `options.json`) and `nginx/h5ai.conf`. Created on first start; a newer image replaces the application and keeps `options.json`. |
| `/logs` | Optional. Nginx and PHP logs that survive the container. |

| Variable | Default | Meaning |
| --- | --- | --- |
| `PUID`, `PGID` | `911` | Owner of `/config` and the nginx and PHP workers. |
| `TZ` | `Asia/Seoul` | Time zone of the container's clock, the logs and their rotation. The listing shows dates in the visitor's browser time zone. |
| `HTPASSWD` | `false` | `true` asks every visitor for a login. |
| `HTPASSWD_USER`, `HTPASSWD_PW` | `guest`, empty | The login. Without a password, start once with `-it` to type it. |
| `LOG_ROTATE_INTERVAL_DAYS`, `LOG_RETENTION_DAYS` | `1`, `30` | Rotation of the files under `/logs`. |
| `LOG_READ_GID` | `PGID` | Numeric host group that can read the files under `/logs`. |

`docker logs h5ai` shows nginx requests and errors and PHP errors. With `/logs`
mounted, they are also written to `nginx/access.log`, `nginx/error.log` and
`php/error.log` there. The files rotate every `LOG_ROTATE_INTERVAL_DAYS` days
after midnight in `TZ`, are compressed one rotation later and are deleted
`LOG_RETENTION_DAYS` days after rotation. Both values range from 1 to 36500,
and retention must be at least the interval. Root owns the files and the
`LOG_READ_GID` group can only read them. Mount `/logs` read-write, give each
container its own folder and keep `/logs/.state`, which holds the rotation
schedule across recreations.

The image serves plain HTTP. Put a reverse proxy with TLS in front of it,
especially with `HTPASSWD`.

To use another host port, change the first number of `-p`, for example
`-p 8080:80`. Hard links and symlinks within `/h5ai` work as they are; a
symlink that points outside `/h5ai` needs its target mounted at the same path,
for example `-v /mnt/media:/mnt/media:ro`.

To serve h5ai under a path such as `/share/`, let the reverse proxy strip the
path and name it in `X-Forwarded-Prefix`:

~~~nginx
location /share/ {
    proxy_pass http://127.0.0.1:8080/;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Prefix /share;
    proxy_redirect / /share/;
}
~~~

A `/config/nginx/h5ai.conf` saved before 0.31.1 ignores that header; see
[Moving from docker-h5ai](#moving-from-docker-h5ai) for how to get the current
default.


## Install on your own server

1. Download `h5ai-<version>.zip` from [Releases][releases], or build it (see
   below). Do **not** copy files from `src`; they must be built first.
2. Unpack it into your web root, so that `_h5ai` sits next to your files.
3. Add `/_h5ai/public/index.php` as the last directory index:
   * Apache httpd: `DirectoryIndex index.html index.php /_h5ai/public/index.php`
   * lighttpd: `index-file.names += ("/_h5ai/public/index.php")`
   * nginx: `index index.html index.php /_h5ai/public/index.php;`
4. Block `/_h5ai/private/`, which holds `options.json` and its password hash.
   The `.htaccess` files in `_h5ai` do this only on Apache httpd with
   `AllowOverride All`; Debian's packaged Apache, for one, ships
   `AllowOverride None`. Unless your web root has `AllowOverride All`, add the
   rule for your server:

   ~~~apache
   <Location "/_h5ai/private/">
       Require all denied
   </Location>
   ~~~

   ~~~lighttpd
   $HTTP["url"] =~ "^/_h5ai/private/" { url.access-deny = ("") }
   ~~~

   ~~~nginx
   location ^~ /_h5ai/private/ { deny all; }
   ~~~

   The lighttpd rule needs `mod_access`. Then check that
   `curl -I http://your-server/_h5ai/private/conf/options.json` answers 403.
5. Let the web server user write to `_h5ai/public/cache` and
   `_h5ai/private/cache`. The info page shows whether it can.

PHP 8.3 or later is required. Visitors need Chrome or Edge 91, Firefox 90 or
Safari 15; older browsers get a plain list.


## Configuration

Settings live in `_h5ai/private/conf/options.json` (in Docker:
`/config/h5ai/_h5ai/private/conf/options.json`). Each option is described in
the file.

`/_h5ai/public/index.php` opens the info page, which checks what your server
supports. Its preset password is empty, so set your own: put the SHA-512 hash
of it in `passhash`.

~~~sh
printf '%s' 'your password' | sha512sum    # macOS: shasum -a 512
~~~


## Moving from docker-h5ai

[docker-h5ai][docker-h5ai] users keep their volumes and variables and change
only the image name.

1. Back up the config folder:
   `cp -a /path/to/config /path/to/config.bak`
2. Remove the old container and start `awesometic/h5ai-ng` with the same
   `-v` and `-e` options:
   `docker rm -f h5ai`, then the `docker run` command above. With Compose,
   change `image:` and run `docker compose up -d`.
3. Read `docker logs h5ai`. On the first start the container:
   * replaces `/config/h5ai/_h5ai` with the new version but keeps your
     `options.json`, and saves a copy of it as
     `/config/<date>_options.json.bak`;
   * blocks `/_h5ai/private/` in `/config/nginx/h5ai.conf` and saves the old
     file as `/config/<date>_h5ai.conf.bak`. If that file was changed too much
     to update, the container stops and prints what to change.

Your `options.json` stays as it was, password included. Unless you changed
those entries, it keeps the filter off and loads fonts from Google Fonts;
compare it with the [new defaults][options] if you want those changes. Other
files you changed in `_h5ai`, such as `types.json`, a theme or a translation,
are replaced by the new version; copy them back from the backup of step 1.

The first start adds only that block to a saved `h5ai.conf`. To also get the
current default, which keeps a mapped port in folder redirects and reads
`X-Forwarded-Prefix`, remove the container, then the file, and run the
`docker run` command above again:

~~~sh
docker rm -f h5ai
rm /path/to/config/nginx/h5ai.conf
~~~

If you changed that file, make your changes again in the new one.

To go back, remove the container, put the backup in place and start
`awesometic/h5ai` again:

~~~sh
docker rm -f h5ai
mv /path/to/config /path/to/config.ng
cp -a /path/to/config.bak /path/to/config
~~~


## Build

Requires [Node.js 24][node]. The built `_h5ai` folder lands in `build`.

~~~sh
npm ci
npm run build     # build/_h5ai
npm run release   # also build/h5ai-<version>.zip (needs zip)
docker build -t h5ai-ng .
~~~

Bugs and pull requests go to [this repository][issues]. Open pull requests
from the original h5ai are reviewed here one at a time.


## Also from the maintainer

[ToneDial][tonedial] gives your coding agent a character. Pick one of 7
characters or set 12 tone axes, and the local CLI applies that voice to
Claude Code, Codex or Antigravity across your projects. It is still in
development and needs Node 22 or later.

~~~sh
npm install --global tonedial
~~~


## License

Released under the MIT License. The full text, with the copyright notices of
h5ai and h5ai-ng, is in [LICENSE](LICENSE).


## References

**h5ai** profits from other projects, all of them licensed under the MIT license
too. Exceptions are some [Material Design icons][material-design-icons] (CC BY 4.0)
and the Ubuntu and Ubuntu Mono fonts ([`@fontsource/ubuntu`][fontsource-ubuntu] and
[`@fontsource/ubuntu-mono`][fontsource-ubuntu-mono] 5.3.0, Ubuntu Font Licence 1.0),
which are bundled unmodified in `_h5ai/public/fonts/` together with the licence.


[h5ai]: https://larsjung.de/h5ai/
[tonedial]: https://github.com/awesometic/tonedial
[ci]: https://github.com/awesometic/h5ai-ng/actions/workflows/ci.yml
[docker-hub]: https://hub.docker.com/r/awesometic/h5ai-ng
[releases]: https://github.com/awesometic/h5ai-ng/releases
[issues]: https://github.com/awesometic/h5ai-ng/issues
[docker-h5ai]: https://github.com/awesometic/docker-h5ai
[options]: https://github.com/awesometic/h5ai-ng/blob/main/src/_h5ai/private/conf/options.json
[node]: https://nodejs.org
[material-design-icons]: https://github.com/google/material-design-icons
[fontsource-ubuntu]: https://www.npmjs.com/package/@fontsource/ubuntu
[fontsource-ubuntu-mono]: https://www.npmjs.com/package/@fontsource/ubuntu-mono

[arch-img]: https://img.shields.io/badge/multiarch-amd64(x86__64)%2C%20arm64%2C%20armv7%2C%20armv6-lightgrey?style=flat-square
[ci-img]: https://img.shields.io/github/actions/workflow/status/awesometic/h5ai-ng/ci.yml?branch=main&style=flat-square
[size-img]: https://img.shields.io/docker/image-size/awesometic/h5ai-ng/latest?style=flat-square
[pulls-img]: https://img.shields.io/docker/pulls/awesometic/h5ai-ng?style=flat-square
[stars-img]: https://img.shields.io/docker/stars/awesometic/h5ai-ng?style=flat-square
