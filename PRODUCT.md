# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two audiences carry equal weight.

- Self-hosters who keep files on a NAS, home server, or Docker host and browse or download them in a browser, for themselves, family, or friends.
- Operators of public download sites (release files, mirrors, archives) whose visitors arrive for the first time, often from a direct link, and need to find and fetch one file.

In both cases the person using the interface is the visitor, not the operator: they did not install it and should not need to learn it.

## Product Purpose

h5ai-ng turns a plain web server directory into an index that is pleasant to browse: navigate folders, preview files, search and filter, and download single files or selections.
It is a maintained fork of h5ai (Lars Jung), which stopped releasing in 2021.
Success means a visitor finds and gets the file they came for without instructions, and an operator can drop it onto an existing server without changing how files are stored.

## Positioning

A read-only, database-free index that sits on top of an existing Apache httpd, lighttpd, or nginx server (or ships as a Docker image) and leaves the files exactly where they are.
It replaces the server's bare autoindex rather than becoming a file manager: no uploads, renames, or deletes.

## Operating Context

- Installed by copying the built `_h5ai` folder next to the served files and pointing the server's directory index at `/_h5ai/public/index.php`, or by running the Docker image with `/h5ai` (files) and `/config` volumes.
- Configured by the operator through `_h5ai/private/conf/options.json` (views, extensions, sorting, thumbnails, archives, tracking) and `types.json`.
- An admin info page, protected by a password hash in `options.json`, shows server capabilities.
- Visitors use desktop and mobile browsers; the layout switches at 700px.

## Capabilities and Constraints

- Views: details, grid, and icons, with adjustable sizes; breadcrumb and folder tree; sorting; filter and search; selection with archive download (tar, zip); file previews for images, audio, video, and text with Markdown and syntax highlighting; QR code for links; image, video, and PDF thumbnails when the server supports them; custom header and footer per folder; folder sizes; auto-refresh.
- 35 interface locales under `_h5ai/private/conf/l10n/`.
- Without JavaScript, or in browsers below the build target, the page falls back to a plain server-rendered list.
- Server: PHP 8.3 or later. Browsers: Chrome/Edge 91, Firefox 90, Safari 15.
- Read-only by design; any write capability is out of scope.
- Existing `options.json` files, URL structure, and icon themes (`default`, `comity`) must keep working across releases.
- The current interface has no ARIA attributes; no accessibility standard has been set yet.

## Brand Commitments

- The interface and its links name the product h5ai-ng.
- Credit to the original h5ai and its author stays visible and keeps the MIT license notices.
- Configuration compatibility with h5ai is part of the brand promise: an h5ai setup moves to h5ai-ng without edits.

## Evidence on Hand

- The running interface itself (build with `npm run build`, or the Docker image) and the bundled icon themes under `_h5ai/public/images/themes/`.
- Screenshots of the Docker image exist in the separate awesometic/docker-h5ai repository (`docs/*.png`).
- No user counts, testimonials, or benchmarks exist; do not invent them.

## Product Principles

1. The files are the content; the index stays out of their way.
2. A first-time visitor succeeds without instructions.
3. Read-only and stateless: nothing the visitor does changes the server.
4. It works where it is dropped: plain server, no database, graceful fallback without JavaScript.
5. An h5ai setup keeps working; compatibility is not traded for novelty.
