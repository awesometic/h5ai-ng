{{changes}}

## Install

**Docker**

~~~sh
docker pull awesometic/h5ai-ng:{{version}}
~~~

Images for `linux/amd64`, `linux/arm64`, `linux/arm/v7` and `linux/arm/v6`.
Coming from docker-h5ai? Follow [Moving from docker-h5ai](https://github.com/awesometic/h5ai-ng#moving-from-docker-h5ai): back up `/config`, change the image name, then restore your `options.json`.

**Your own server**

Download `h5ai-{{version}}.zip` below, unpack it into your web root and add `/_h5ai/public/index.php` as the last directory index.
Requires PHP 8.3 or later.
See [Install on your own server](https://github.com/awesometic/h5ai-ng#install-on-your-own-server) for Apache httpd, lighttpd and nginx.

[Full changelog](https://github.com/awesometic/h5ai-ng/blob/v{{version}}/CHANGELOG.md)
