# AGENTS Guide

Operating guide for AI agents in h5ai-ng.
It is a condensed, project-specific version of the agent-engineering harness 1.15.3.
It is not byte-shared with that harness and is not managed by its sync tool;
edit it here when this project's rules change.

## Project

h5ai-ng is a maintained fork of [lrsjng/h5ai](https://github.com/lrsjng/h5ai), a web server index for Apache httpd, lighttpd, and nginx.
The upstream project stopped releasing in 2021; this fork modernizes the toolchain, raises the PHP baseline, ships a Docker image, and reviews open upstream pull requests.

| Path | Contents |
| --- | --- |
| `src/_h5ai/private/php/` | PHP backend (`core/`, `ext/`, Pug page templates in `pages/`) |
| `src/_h5ai/private/conf/` | `options.json`, `types.json`, `l10n/*.json` (JSON with comments) |
| `src/_h5ai/public/` | `index.php` entry, JS (`js/`), Less (`css/`), images |
| `build.js` | Build: esbuild (JS/CSS), Less, Pug → `build/_h5ai` |
| `test/` | JS unit tests (`scar` + `jsdom`) |
| `docker/` | Image config (nginx, php-fpm, supervisord, init, logs) and `smoke.py` |

## Commands

```bash
npm ci                 # install
npm run lint           # eslint
npm test               # JS unit tests
npm run build          # build/_h5ai
node test/bundle.js    # boots the built bundle in jsdom (after build)
npm run release        # build + build/h5ai-<version>.zip (needs `zip`)
docker buildx build --load -t h5ai-ng:test .
python3 docker/smoke.py h5ai-ng:test linux/arm64   # or linux/amd64
```

Never install files from `src/` directly; they must be built.

## Constraints

- **PHP**: `MIN_PHP_VERSION` is 8.3 (`src/_h5ai/public/index.php`).
  Source must run on 8.3 through 8.5; do not use syntax or functions newer than 8.3.
  The Docker image ships PHP 8.5.
- **Browsers**: the JS/CSS target lives in `build.js` → `TARGET` (Chrome/Edge 91, Firefox 90, Safari 15).
  `src/_h5ai/public/js/pre.js` sends older browsers to the fallback list; keep its checks in step with the target.
- **Node**: the build runs on Node 24 (the Docker build stage uses `node:24-alpine`).
- `build/` and `node_modules/` are never committed.
- Server-side configuration (`H5AI_ROOT_PATH`, php-fpm, nginx) belongs to the operator.
  Never trust request data for paths; keep the existing path checks in `core/`.

## Workflow

1. Read the code a change touches and trace the real flow before editing.
2. Make the smallest change that fixes the root cause.
   Prefer the platform, the standard library, or an installed dependency over new code;
   add a dependency only when a few lines cannot do the job.
3. Verify with evidence: `npm run lint`, `npm test`, `npm run build`, `node test/bundle.js`.
   For changes under `docker/`, `Dockerfile`, PHP runtime behavior, or bundled h5ai code, also build the image and run `docker/smoke.py`.
   A successful build alone is not evidence that the service works.
4. Report outcomes faithfully: failed or skipped checks are stated as such.

Tell the user which skills and sub-agents you plan to use and which you actually used.

## Required Skills

| Skill | Source | Use it for |
| --- | --- | --- |
| Ponytail (plugin) | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Every implementation and review |
| Impeccable (skill) | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Any interface change: Less, Pug, interface JS, the preview, the admin page; it reads `PRODUCT.md`, `DESIGN.md` and `.impeccable/` |

At the start of each session, check whether both are available.
If one is missing, warn the user before the first task: name it, link its source, and say which work it covers.
Then continue under the rules of this guide; for interface work without Impeccable, follow `DESIGN.md` directly and say so in the report.
Do not install or enable either one yourself.

## Testing

- A test must fail when the behavior it covers breaks.
  Before trusting a new assertion, show that a broken result is rejected.
- When a change touches behavior an existing test covers, update that test in the same change.
- Do not weaken an assertion only to make a run pass.

## Upstream Pull Requests

Upstream PRs are reviewed one at a time against this fork.
Keep the original author's authorship (cherry-pick or `Co-authored-by`) and note the upstream PR number in the commit body.
Reject or adapt a PR that conflicts with the constraints above, and say why.

## Git

- Work on a branch, not `main`. Commit or push only when the user asks.
- Commit subject: `<scope>: <Imperative summary>` (for example `build: Replace ghu with esbuild`).
- Never commit credentials, tokens, or private user data.

## Documents

- `README.md` is the user-facing document; keep its commands in sync with `package.json`.
- Korean text should read naturally; avoid literal translationese.
- Agent working records stay local and are ignored by git:
  - `docs/loop/` — loop logs and `current.md` (current state, next step, known risks).
    Read `current.md` at the start of a task and update it at the end.
  - `docs/decisions/` — durable decision records (context, decision, consequences).
  - `docs/plan/` — the user's own planning documents.
    Create, edit, or delete files there only on the user's explicit instruction.
