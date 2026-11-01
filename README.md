# h5ai

[![license][license-img]][github] [![web][web-img]][web] [![github][github-img]][github]

A modern HTTP web server index for Apache httpd, lighttpd, and nginx.


## Important

* Do **not** install any files from the `src` folder, they need to be
  preprocessed to work correctly!
* Find a preprocessed package and detailed install instructions on the
  [project page][web].
* For bug reports and feature requests please use [issues][github-issues].


## Build

Requires [`node 24`][node]. The server needs PHP 8.3 or later. The interface
needs Chrome/Edge 91, Firefox 90 or Safari 15; older browsers get the plain
fallback list.
From within the root folder run the following commands to find the built
`_h5ai` folder in `build` (`npm run release` also creates a zipball there and
needs `zip`).

~~~sh
> npm ci
> npm run build
~~~


## Docker

The image serves `/h5ai` with Nginx and PHP 8.5 on Alpine Linux, and keeps
its configuration in `/config`.

~~~sh
> docker build -t h5ai-ng .
> docker run -d -p 80:80 -v /path/to/files:/h5ai -v /path/to/config:/config h5ai-ng
~~~

A `/config` volume from [docker-h5ai][docker-h5ai] can be reused. At startup a
saved `nginx/h5ai.conf` that still serves `/_h5ai/private/` is updated to deny
it, and an older h5ai copy in `h5ai/` is replaced. Dated backups of the Nginx
file and of the old `options.json` stay in `/config`. A saved configuration too
customized to update stops the container with instructions.

`python3 docker/smoke.py h5ai-ng linux/amd64` checks a built image end to end.


## License

The MIT License (MIT)

Copyright (c) 2020 Lars Jung (https://larsjung.de)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


## References

**h5ai** profits from other projects, all of them licensed under the MIT license
too. Exceptions are some [Material Design icons][material-design-icons] (CC BY 4.0).


[web]: https://larsjung.de/h5ai/
[github]: https://github.com/lrsjng/h5ai
[github-issues]: https://github.com/lrsjng/h5ai/issues
[release]: https://release.larsjung.de/h5ai/
[develop]: https://release.larsjung.de/h5ai/develop/
[node]: https://nodejs.org
[docker-h5ai]: https://github.com/awesometic/docker-h5ai
[material-design-icons]: https://github.com/google/material-design-icons

[license-img]: https://img.shields.io/badge/license-MIT-a0a060.svg?style=flat-square
[web-img]: https://img.shields.io/badge/web-larsjung.de/h5ai-a0a060.svg?style=flat-square
[github-img]: https://img.shields.io/badge/github-lrsjng/h5ai-a0a060.svg?style=flat-square
