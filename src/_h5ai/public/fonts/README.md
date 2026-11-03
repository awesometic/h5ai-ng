# Bundled fonts

Ubuntu (300, 400, 700) and Ubuntu Mono (400, 700) as woff2, unmodified.
Copyright 2011 Canonical Ltd. Licensed under the Ubuntu Font Licence 1.0 (`UFL.txt`).

## Source

| Family | npm package | Version | Files |
| --- | --- | --- | --- |
| Ubuntu | `@fontsource/ubuntu` | 5.3.0 | `files/ubuntu-<subset>-<weight>-normal.woff2` |
| Ubuntu Mono | `@fontsource/ubuntu-mono` | 5.3.0 | `files/ubuntu-mono-<subset>-<weight>-normal.woff2` |

Subsets: `latin`, `latin-ext`, `cyrillic`, `greek`.
The packages' `-ext` Cyrillic and Greek subsets (Old Cyrillic, polytonic Greek) are left out; no interface locale needs them.
`SHA256SUMS` lists the checksum of every file here, so `shasum -a 256 -c SHA256SUMS` checks a copy against the files that were committed.

To fetch the originals again: `npm pack @fontsource/ubuntu@5.3.0 @fontsource/ubuntu-mono@5.3.0`, unpack both, and copy the files named above.

## Use

`css/lib/fonts.less` declares one `@font-face` per file with `font-display: swap` and the `unicode-range` of its subset, copied from the packages' `300.css`, `400.css` and `700.css`.
A browser downloads only the subsets that the page's text needs.
Interface locales in Hebrew, Hindi, Japanese, Korean and Chinese are not covered by Ubuntu and use the next family of the stack.
