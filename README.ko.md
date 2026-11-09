# h5ai-ng

[English](README.md) · **한국어** · [Español](README.es.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md)

[![multiarch][arch-img]][docker-hub]
[![build][ci-img]][ci]

[![image size][size-img]][docker-hub]
[![docker pulls][pulls-img]][docker-hub]
[![docker stars][stars-img]][docker-hub]

h5ai-ng는 Apache httpd, lighttpd, nginx에서 쓰는 파일 목록 페이지입니다.
방문자는 폴더를 둘러보고, 이미지·동영상·오디오·텍스트를 미리 보고, 이름으로 걸러
내고, 고른 파일을 압축 파일 하나로 내려받습니다. 파일은 원래 자리에 그대로
있습니다.

이 프로젝트는 Lars Jung이 만든 [h5ai][h5ai]의 포크입니다. 원본은 2021년 이후 새
버전이 나오지 않아 이곳에서 이어서 관리합니다.

원본 사이트는 h5ai를 이렇게 소개합니다.

> h5ai is a modern file indexer for HTTP web servers with focus on your files. Directories are displayed in a appealing way and browsing them is enhanced by different views, a breadcrumb and a tree overview. Initially h5ai was an acronym for HTML5 Apache Index but now it supports other web servers too.

![h5ai-ng의 자세히 보기 화면](docs/screenshot.png)


## h5ai-ng를 쓰는 이유

* **읽기 전용이고 데이터베이스가 없습니다.** 서버의 기본 디렉터리 목록을 대신할
  뿐, 파일에는 아무것도 쓰지 않습니다.
* **최신 PHP에서 동작합니다.** PHP 8.3 이상을 지원하고 Docker 이미지에는
  PHP 8.5가 들어 있습니다.
* **외부 서버에 요청하지 않습니다.** 글꼴을 함께 배포하므로 페이지를 열어도 내
  서버 밖으로 나가는 요청이 없습니다.
* **쓰던 h5ai 설정을 그대로 씁니다.** `options.json`, URL, `default`와 `comity`
  아이콘 테마가 그대로 동작합니다.


## h5ai, docker-h5ai, h5ai-ng 비교

| | h5ai | docker-h5ai | h5ai-ng |
| --- | --- | --- | --- |
| 설명 | Lars Jung이 만든 원본 파일 목록 페이지 | h5ai 0.30.0을 담은 Docker 이미지 `awesometic/h5ai` | 이 포크와 Docker 이미지 `awesometic/h5ai-ng` |
| 상태 | 2021년 1월 0.30.0 이후 릴리스 없음 | 지원 중단. 2026년 11월 저장소 보관 처리(archive). 이미지는 계속 동작하지만 보안 수정을 포함해 업데이트 없음 | 관리 중. 2026년 11월 0.31.0부터 새 버전 배포 |
| PHP | 7.0 이상 | 이미지에 8.5 포함 | 8.3 이상, 이미지에 8.5 포함 |
| 설치 | 웹 서버용 zip | Docker | 웹 서버용 zip 또는 amd64·arm64·arm/v7·arm/v6용 Docker |

### h5ai는 아직 관리되나요?

원본 h5ai는 2021년 1월 0.30.0 이후 릴리스가 없습니다. h5ai-ng는 이를 이어
관리하는 포크로 2026년 11월 0.31.0부터 새 버전을 내고 있으며 PHP 8.3 이상이
필요합니다. `options.json`과 URL, `default`와 `comity` 아이콘 테마는 그대로
동작합니다. `types.json`, 테마, 번역 파일처럼 `_h5ai` 안에서 고친 다른 파일은
h5ai-ng로 옮길 때 다시 복사해 넣어야 합니다.

### h5ai용 Docker 이미지는 무엇을 쓰면 되나요?

`awesometic/h5ai-ng`를 쓰세요. linux/amd64, linux/arm64, linux/arm/v7,
linux/arm/v6용으로 배포되며 썸네일, 압축 다운로드, 폴더 크기 표시에 필요한
도구가 이미 들어 있습니다. 예전 `awesometic/h5ai` 이미지는 계속 동작하지만 보안
수정을 포함해 더는 업데이트되지 않습니다. 옮기려면 `/config`를 백업하고
`docker run` 명령이나 Compose 파일에서 이미지 이름을 바꾸세요. `docker run`을
쓴다면 먼저 기존 컨테이너를 지우세요. 자세한 내용은
[docker-h5ai에서 옮겨 오기](#docker-h5ai에서-옮겨-오기)를 보세요.

### Docker 없이 쓸 수 있나요?

네. [릴리스][releases]마다 zip 파일이 있습니다. PHP 8.3 이상이 동작하는 Apache
httpd, lighttpd, nginx의 웹 루트에 압축을 푸세요. 그다음 디렉터리 인덱스의
마지막 항목으로 `/_h5ai/public/index.php`를 추가하고 `options.json`과 비밀번호
해시가 들어 있는 `/_h5ai/private/` 접근을 막으세요.
[직접 운영하는 서버에 설치하기](#직접-운영하는-서버에-설치하기)를 보세요.


## Docker로 바로 시작하기

~~~sh
docker run -d --name h5ai -p 80:80 \
  -v /path/to/files:/h5ai \
  -v /path/to/config:/config \
  -e PUID=1000 -e PGID=1000 -e TZ=Asia/Seoul \
  --restart unless-stopped \
  awesometic/h5ai-ng
~~~

`http://localhost/`를 열면 됩니다. 이미지는 `linux/amd64`, `linux/arm64`,
`linux/arm/v7`, `linux/arm/v6`용으로 배포합니다.

이미지에는 부가 기능에 필요한 프로그램이 모두 들어 있어 이미지·동영상·PDF 썸네일,
tar와 zip 다운로드, 폴더 크기 표시가 바로 동작합니다. 정보 페이지
(`/_h5ai/public/index.php`)에 로그인하면 모든 점검 항목이 통과로 나옵니다.

![모든 점검 항목을 통과한 Docker 이미지의 정보 페이지](docs/info-page.png)

| 볼륨 | 내용 |
| --- | --- |
| `/h5ai` | 공유할 파일. 필요하면 읽기 전용(`:ro`)으로 마운트하세요. |
| `/config` | `h5ai/_h5ai`(애플리케이션과 `options.json`)와 `nginx/h5ai.conf`. 처음 시작할 때 만들어지며, 새 버전 이미지는 애플리케이션만 바꾸고 `options.json`은 그대로 둡니다. |
| `/logs` | 선택 사항. 컨테이너를 지워도 남는 Nginx와 PHP 로그. |

| 변수 | 기본값 | 설명 |
| --- | --- | --- |
| `PUID`, `PGID` | `911` | `/config`와 nginx·PHP 워커 프로세스의 소유자. |
| `TZ` | `Asia/Seoul` | 컨테이너의 시계, 로그, 로그 교체에 쓰는 시간대. 목록의 날짜는 방문자 브라우저의 시간대로 나옵니다. |
| `HTPASSWD` | `false` | `true`이면 모든 방문자에게 로그인을 요구합니다. |
| `HTPASSWD_USER`, `HTPASSWD_PW` | `guest`, 빈 값 | 로그인 계정. 비밀번호를 비워 두었다면 처음 한 번은 `-it`로 실행해 직접 입력하세요. |
| `LOG_ROTATE_INTERVAL_DAYS`, `LOG_RETENTION_DAYS` | `1`, `30` | `/logs` 아래 파일의 교체 주기와 보관 기간(일). |
| `LOG_READ_GID` | `PGID` 값 | `/logs` 아래 파일을 읽을 수 있는 호스트 그룹 ID(숫자). |

`docker logs h5ai`로 nginx 요청·오류와 PHP 오류를 볼 수 있습니다. `/logs`를
마운트하면 같은 기록이 그 안의 `nginx/access.log`, `nginx/error.log`,
`php/error.log`에도 남습니다. 로그 파일은 `TZ` 기준 자정이 지나면
`LOG_ROTATE_INTERVAL_DAYS`일마다 교체됩니다. 교체된 파일은 다음 교체 때 압축되고
교체 후 `LOG_RETENTION_DAYS`일이 지나면 삭제됩니다. 두 값은 1부터 36500까지이고
보관 기간은 교체 주기보다 짧을 수 없습니다. 파일 소유자는 root이며
`LOG_READ_GID` 그룹은 읽기만 할 수 있습니다. `/logs`는 쓰기 가능하게 마운트하고
컨테이너마다 폴더를 따로 쓰세요. 교체 일정은 `/logs/.state`에 저장되므로 이 폴더를 지우지
않으면 컨테이너를 다시 만들어도 일정이 이어집니다.

이미지는 암호화하지 않은 HTTP로 응답합니다. 앞단에 TLS를 적용한 리버스
프록시를 두세요. `HTPASSWD`를 쓴다면 더욱 그렇습니다.

다른 호스트 포트를 쓰려면 `-p`의 앞 숫자를 바꾸세요(예: `-p 8080:80`).
`/h5ai` 안을 가리키는 하드 링크와 심볼릭 링크는 그대로 동작합니다. `/h5ai`
바깥을 가리키는 심볼릭 링크는 대상 경로를 컨테이너의 같은 위치에 마운트해야
합니다(예: `-v /mnt/media:/mnt/media:ro`).

h5ai를 `/share/` 같은 경로 아래에서 서비스하려면 리버스 프록시가 그 경로를 떼고
`X-Forwarded-Prefix`로 알려 주게 하세요.

~~~nginx
location /share/ {
    proxy_pass http://127.0.0.1:8080/;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Prefix /share;
    proxy_redirect / /share/;
}
~~~

0.31.1 이전에 저장된 `/config/nginx/h5ai.conf`는 이 헤더를 읽지 않습니다. 현재
기본값으로 바꾸는 방법은 [docker-h5ai에서 옮겨 오기](#docker-h5ai에서-옮겨-오기)를 보세요.


## 직접 운영하는 서버에 설치하기

1. [Releases][releases]에서 `h5ai-<version>.zip`을 받거나 직접 빌드합니다(아래
   참고). `src`의 파일을 그대로 복사하면 **안 됩니다**. 먼저 빌드해야 합니다.
2. 웹 루트에 압축을 풀어 `_h5ai` 폴더가 공유할 파일들과 같은 위치에 오게 합니다.
3. 디렉터리 인덱스의 마지막 항목으로 `/_h5ai/public/index.php`를 추가합니다.
   * Apache httpd: `DirectoryIndex index.html index.php /_h5ai/public/index.php`
   * lighttpd: `index-file.names += ("/_h5ai/public/index.php")`
   * nginx: `index index.html index.php /_h5ai/public/index.php;`
4. `options.json`과 비밀번호 해시가 들어 있는 `/_h5ai/private/` 접근을 막으세요.
   `_h5ai` 안의 `.htaccess` 파일은 Apache httpd가 `AllowOverride All`일 때만
   동작하는데, Debian 패키지의 Apache처럼 `AllowOverride None`이 기본인 경우가
   있습니다. 웹 루트에 `AllowOverride All`을 쓰지 않는다면 서버에 맞는 규칙을
   추가하세요.

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

   lighttpd 규칙에는 `mod_access`가 필요합니다. 적용한 뒤
   `curl -I http://your-server/_h5ai/private/conf/options.json`이 403을 돌려주는지 확인하세요.
5. 웹 서버 사용자가 `_h5ai/public/cache`와 `_h5ai/private/cache`에 쓸 수 있게
   하세요. 쓸 수 있는지는 정보 페이지에서 확인할 수 있습니다.

서버에는 PHP 8.3 이상이 필요합니다. 방문자는 Chrome·Edge 91, Firefox 90,
Safari 15 이상을 써야 하고 그보다 오래된 브라우저에서는 단순한 목록이 나옵니다.


## 설정

설정 파일은 `_h5ai/private/conf/options.json`입니다(Docker에서는
`/config/h5ai/_h5ai/private/conf/options.json`). 옵션마다 파일 안에 설명이
있습니다.

`/_h5ai/public/index.php`를 열면 서버가 어떤 기능을 지원하는지 점검하는 정보
페이지가 나옵니다. 이 페이지의 기본 비밀번호는 비어 있으니 직접 정하세요.
비밀번호의 SHA-512 해시를 `passhash`에 넣으면 됩니다.

~~~sh
printf '%s' '비밀번호' | sha512sum    # macOS: shasum -a 512
~~~


## docker-h5ai에서 옮겨 오기

[docker-h5ai][docker-h5ai]를 쓰고 있다면 볼륨과 변수는 그대로 두고 이미지
이름만 바꾸면 됩니다.

1. 설정 폴더를 백업합니다.
   `cp -a /path/to/config /path/to/config.bak`
2. 기존 컨테이너를 지우고 같은 `-v`와 `-e` 옵션으로 `awesometic/h5ai-ng`를
   실행합니다. `docker rm -f h5ai`를 실행한 뒤 위의 `docker run` 명령을 씁니다.
   Compose를 쓴다면 `image:`를 바꾸고 `docker compose up -d`를 실행합니다.
3. `docker logs h5ai`로 로그를 확인합니다. 처음 시작할 때 컨테이너가 하는 일은
   다음과 같습니다.
   * `/config/h5ai/_h5ai`를 새 버전으로 바꾸되 `options.json`은 그대로 두고,
     그 사본을 `/config/<date>_options.json.bak`에 저장합니다.
   * `/config/nginx/h5ai.conf`에 `/_h5ai/private/` 차단 규칙을 넣고 기존 파일은
     `/config/<date>_h5ai.conf.bak`에 저장합니다. 이 파일을 많이 고쳐서 자동으로
     바꿀 수 없으면 컨테이너가 멈추고 고칠 곳을 알려 줍니다.

`options.json`은 비밀번호까지 예전 그대로입니다. 해당 항목을 바꾸지 않았다면
필터는 꺼져 있고 글꼴은 Google Fonts에서 불러옵니다. 새 기본값을 쓰고 싶다면
[새 기본 설정][options]과 비교해 필요한 부분만 옮기세요. `types.json`, 테마,
번역 파일처럼 `_h5ai` 안에서 고친 다른 파일은 새 버전으로 바뀌므로 1단계에서
만든 백업에서 다시 복사하세요.

이미 있는 `h5ai.conf`에는 처음 시작할 때 이 차단 규칙만 추가됩니다. 현재 기본값은
폴더 리다이렉트에서 매핑한 포트를 유지하고 `X-Forwarded-Prefix`를 읽습니다. 이
기본값을 쓰려면 컨테이너를 지운 다음 파일을 지우고 위의 `docker run` 명령을 다시
실행하세요.

~~~sh
docker rm -f h5ai
rm /path/to/config/nginx/h5ai.conf
~~~

이 파일을 직접 고쳤다면 새 파일에 같은 변경을 다시 적용하세요.

되돌리려면 컨테이너를 지우고 백업을 제자리에 놓은 뒤 `awesometic/h5ai`를 다시
실행합니다.

~~~sh
docker rm -f h5ai
mv /path/to/config /path/to/config.ng
cp -a /path/to/config.bak /path/to/config
~~~


## 빌드

[Node.js 24][node]가 필요합니다. 빌드한 `_h5ai` 폴더는 `build`에 생깁니다.

~~~sh
npm ci
npm run build     # build/_h5ai
npm run release   # build/h5ai-<version>.zip도 만듭니다(zip 필요)
docker build -t h5ai-ng .
~~~

버그 제보와 풀 리퀘스트는 [이 저장소][issues]로 보내 주세요. 원본 h5ai에 열려
있던 풀 리퀘스트도 이곳에서 하나씩 검토합니다.


## 메인테이너의 다른 프로젝트

[ToneDial][tonedial]은 코딩 에이전트에게 캐릭터를 입히는 로컬 CLI입니다. 캐릭터
7종 중 하나를 고르거나 톤 축 12개를 조절하면 Claude Code·Codex·Antigravity가 여러
프로젝트에서 그 말투로 답합니다. 아직 개발 중이며 Node 22 이상이 필요합니다.

~~~sh
npm install --global tonedial
~~~


## 라이선스

MIT 라이선스로 배포합니다. h5ai와 h5ai-ng의 저작권 고지를 담은 전문은
[LICENSE](LICENSE)에 있습니다.


## 사용한 프로젝트

**h5ai**는 다른 여러 프로젝트의 도움을 받았고, 그 프로젝트들도 모두 MIT 라이선스입니다. 예외는 일부
[Material Design 아이콘][material-design-icons](CC BY 4.0)과 Ubuntu, Ubuntu Mono
글꼴([`@fontsource/ubuntu`][fontsource-ubuntu], [`@fontsource/ubuntu-mono`][fontsource-ubuntu-mono]
5.3.0, Ubuntu Font Licence 1.0)입니다. 글꼴은 수정하지 않은 채 라이선스와 함께
`_h5ai/public/fonts/`에 들어 있습니다.


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
