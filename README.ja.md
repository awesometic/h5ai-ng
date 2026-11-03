# h5ai-ng

[English](README.md) · [한국어](README.ko.md) · [Español](README.es.md) · **日本語** · [简体中文](README.zh-CN.md)

[![license][license-img]][license] [![ci][ci-img]][ci] [![docker][docker-img]][docker-hub]

Apache httpd、lighttpd、nginx 向けのファイル一覧ページです。訪問者はフォルダーを
たどり、画像・動画・音声・テキストをプレビューし、名前で絞り込み、選んだファイルを
まとめて 1 つのアーカイブとしてダウンロードできます。ファイルは今ある場所のままです。

h5ai-ng は、2021 年を最後にリリースが止まった Lars Jung 氏の [h5ai][h5ai] を
引き継いで保守するフォークです。

![詳細表示でフォルダーを一覧する h5ai-ng](docs/screenshot.png)


## h5ai-ng の特長

* **読み取り専用で、データベースは不要です。** サーバー標準のディレクトリ一覧を
  置き換えるだけで、ファイルには一切書き込みません。
* **最新の PHP で動きます。** PHP 8.3 以降に対応し、Docker イメージには PHP 8.5 が
  入っています。
* **外部サーバーへのリクエストはありません。** フォントを同梱しているので、
  ページの読み込みは自分のサーバー内で完結します。
* **h5ai の設定をそのまま使えます。** `options.json`、URL、`default` と `comity`
  のアイコンテーマはそのまま動きます。


## Docker ですぐに使う

~~~sh
docker run -d --name h5ai -p 80:80 \
  -v /path/to/files:/h5ai \
  -v /path/to/config:/config \
  -e PUID=1000 -e PGID=1000 -e TZ=Asia/Tokyo \
  --restart unless-stopped \
  awesometic/h5ai-ng
~~~

`http://localhost/` を開いてください。イメージは `linux/amd64`、`linux/arm64`、
`linux/arm/v7`、`linux/arm/v6` 向けに公開しています。

イメージには、画像・動画・PDF のサムネイル、tar と zip のダウンロード、フォルダーサイズの
表示に必要なものがすべて入っています。情報ページ（`/_h5ai/public/index.php`）に
ログインすると、すべてのチェックが合格になっています。

![すべてのチェックに合格した Docker イメージの情報ページ](docs/info-page.png)

| ボリューム | 内容 |
| --- | --- |
| `/h5ai` | 公開するファイル。必要なら読み取り専用（`:ro`）でマウントしてください。 |
| `/config` | `h5ai/_h5ai`（アプリケーションと `options.json`）と `nginx/h5ai.conf`。初回起動時に作られ、新しいイメージはアプリケーションだけを置き換えて `options.json` はそのまま残します。 |
| `/logs` | 任意。コンテナーを削除しても残る Nginx と PHP のログ。 |

| 変数 | 既定値 | 意味 |
| --- | --- | --- |
| `PUID`, `PGID` | `911` | `/config` と nginx・PHP のワーカープロセスの所有者。 |
| `TZ` | `Asia/Seoul` | コンテナーの時計、ログ、ログローテーションのタイムゾーン。一覧の日付は訪問者のブラウザーのタイムゾーンで表示されます。 |
| `HTPASSWD` | `false` | `true` にすると、すべての訪問者にログインを求めます。 |
| `HTPASSWD_USER`, `HTPASSWD_PW` | `guest`、空 | ログイン情報。パスワードが空なら、一度 `-it` 付きで起動して入力してください。 |
| `LOG_ROTATE_INTERVAL_DAYS`, `LOG_RETENTION_DAYS` | `1`、`30` | `/logs` 以下のファイルのローテーション間隔と保存期間（日）。 |

イメージは暗号化されていない HTTP で応答します。前段に TLS 対応のリバースプロキシを
置いてください。`HTPASSWD` を使う場合は特に必要です。


## 自分のサーバーにインストールする

1. [Releases][releases] から `h5ai-<version>.zip` をダウンロードするか、ビルドします
   （後述）。`src` のファイルをそのままコピーしては**いけません**。先にビルドが必要です。
2. Web ルートに展開し、`_h5ai` が公開するファイルと同じ階層に来るようにします。
3. ディレクトリインデックスの最後に `/_h5ai/public/index.php` を追加します。
   * Apache httpd: `DirectoryIndex index.html index.php /_h5ai/public/index.php`
   * lighttpd: `index-file.names += ("/_h5ai/public/index.php")`
   * nginx: `index index.html index.php /_h5ai/public/index.php;`
4. `options.json` とパスワードハッシュを含む `/_h5ai/private/` へのアクセスを
   禁止してください。`_h5ai` 内の `.htaccess` ファイルが効くのは
   `AllowOverride All` の Apache httpd だけで、Debian パッケージの Apache などは
   `AllowOverride None` が初期値です。Web ルートが `AllowOverride All` でなければ、
   サーバーに合わせたルールを追加します。

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

   lighttpd のルールには `mod_access` が必要です。設定後、
   `curl -I http://your-server/_h5ai/private/conf/options.json` が 403 を返すことを確認してください。
5. Web サーバーのユーザーが `_h5ai/public/cache` と `_h5ai/private/cache` に
   書き込めるようにします。書き込めるかどうかは情報ページで確認できます。

PHP 8.3 以降が必要です。訪問者のブラウザーは Chrome または Edge 91、Firefox 90、
Safari 15 以降が必要で、それより古いブラウザーには簡易な一覧が表示されます。


## 設定

設定は `_h5ai/private/conf/options.json` にあります（Docker では
`/config/h5ai/_h5ai/private/conf/options.json`）。各オプションの説明はファイル内に
書かれています。

`/_h5ai/public/index.php` を開くと、サーバーが何に対応しているかを確認できる
情報ページが表示されます。このページの初期パスワードは空なので、自分で設定して
ください。パスワードの SHA-512 ハッシュを `passhash` に入れます。

~~~sh
printf '%s' 'パスワード' | sha512sum    # macOS: shasum -a 512
~~~


## docker-h5ai からの移行

[docker-h5ai][docker-h5ai] を使っている場合、ボリュームと変数はそのままで、
イメージ名だけを変えます。

1. 設定フォルダーをバックアップします。
   `cp -a /path/to/config /path/to/config.bak`
2. 古いコンテナーを削除し、同じ `-v` と `-e` オプションで `awesometic/h5ai-ng` を
   起動します。`docker rm -f h5ai` を実行してから、上の `docker run` コマンドを使います。
3. `docker logs h5ai` を確認します。初回起動時、コンテナーは次のことを行います。
   * `/config/h5ai/_h5ai` を新しいバージョンに置き換えますが、`options.json` は
     そのまま残し、そのコピーを `/config/<date>_options.json.bak` として保存します。
   * `/config/nginx/h5ai.conf` で `/_h5ai/private/` をブロックし、以前のファイルを
     `/config/<date>_h5ai.conf.bak` として保存します。ファイルの変更が大きすぎて
     更新できない場合、コンテナーは停止し、直すべき箇所を表示します。

`options.json` はパスワードも含めて以前のままです。該当する項目を変えていなければ、
フィルターはオフのままで、フォントを Google Fonts から読み込みます。新しい既定値を
取り入れたい場合は、[新しい既定の設定][options]と比べてください。`types.json`、
テーマ、翻訳など `_h5ai` 内で変更したほかのファイルは新しいバージョンに置き換わる
ので、手順 1 のバックアップからコピーし直してください。

元に戻すには、コンテナーを止めて `/path/to/config.bak` を復元し、
`awesometic/h5ai` をもう一度起動します。


## ビルド

[Node.js 24][node] が必要です。ビルドした `_h5ai` フォルダーは `build` にできます。

~~~sh
npm ci
npm run build     # build/_h5ai
npm run release   # build/h5ai-<version>.zip も作成（zip が必要）
docker build -t h5ai-ng .
~~~

バグ報告とプルリクエストは[このリポジトリ][issues]へお願いします。元の h5ai で
開いたままのプルリクエストも、ここで 1 件ずつ検討しています。


## メンテナーのもう 1 つのプロジェクト

[ToneDial][tonedial] は、コーディングエージェントにキャラクターを与えるローカル CLI です。
7 種類のキャラクターから選ぶか 12 のトーン軸を調整すると、Claude Code、Codex、
Antigravity がどのプロジェクトでもその口調で応答します。現在開発中で、Node 22 以降が
必要です。

~~~sh
npm install --global tonedial
~~~


## ライセンス

MIT ライセンスです。英語の原文をそのまま載せています。

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


## 利用しているプロジェクト

**h5ai** はほかのプロジェクトの成果を利用しており、それらもすべて MIT ライセンスです。
例外は一部の [Material Design アイコン][material-design-icons]（CC BY 4.0）と、
Ubuntu および Ubuntu Mono フォント（[`@fontsource/ubuntu`][fontsource-ubuntu] と
[`@fontsource/ubuntu-mono`][fontsource-ubuntu-mono] 5.3.0、Ubuntu Font Licence 1.0）です。
フォントは改変せず、ライセンスとともに `_h5ai/public/fonts/` に同梱しています。


[h5ai]: https://larsjung.de/h5ai/
[tonedial]: https://github.com/awesometic/tonedial
[license]: #ライセンス
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

[license-img]: https://img.shields.io/badge/license-MIT-a0a060.svg?style=flat-square
[ci-img]: https://img.shields.io/github/actions/workflow/status/awesometic/h5ai-ng/ci.yml?branch=main&style=flat-square
[docker-img]: https://img.shields.io/docker/pulls/awesometic/h5ai-ng?style=flat-square
