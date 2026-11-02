---
name: h5ai-ng
description: A quiet, flat file index whose interface stays out of the way of the files it lists.
colors:
  link-sky: "#42a5f5"
  link-sky-deep: "#176fcb"
  highlighter-pink: "#ff4081"
  paper-white: "#ffffff"
  panel-mist: "#fafafa"
  charcoal: "#212121"
  slider-track: "#e0e0e0"
  slider-thumb: "#616161"
  ink: "rgba(0,0,0,0.87)"
  ink-secondary: "rgba(0,0,0,0.54)"
  ink-disabled: "rgba(0,0,0,0.26)"
  ink-inverse: "rgba(255,255,255,1)"
  hover-wash: "rgba(0,0,0,0.03)"
  hairline: "rgba(0,0,0,0.05)"
  row-rule: "rgba(0,0,0,0.07)"
  hairline-strong: "rgba(0,0,0,0.15)"
  scrim: "rgba(0,0,0,0.5)"
  viewer-bar: "rgb(27,27,27)"
  pass-green: "#4caf50"
  fail-red: "#f44336"
typography:
  body:
    fontFamily: '"Ubuntu", "Roboto", "Helvetica", "Arial", "sans-serif"'
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.4
  title:
    fontFamily: '"Ubuntu", "Roboto", "Helvetica", "Arial", "sans-serif"'
    fontSize: "16px"
    fontWeight: 400
    lineHeight: "48px"
  mono:
    fontFamily: '"Ubuntu Mono", "Monaco", "Lucida Sans Typewriter", "monospace"'
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.4
  hint:
    fontFamily: '"Ubuntu", "Roboto", "Helvetica", "Arial", "sans-serif"'
    fontSize: "16px"
    fontWeight: 700
    lineHeight: 1.4
  display:
    fontFamily: '"Ubuntu", "Roboto", "Helvetica", "Arial", "sans-serif"'
    fontSize: "52px"
    fontWeight: 300
    lineHeight: 1.4
rounded:
  sm: "2px"
  md: "4px"
  lg: "8px"
  pill: "20px"
spacing:
  s-4: "4px"
  s-8: "8px"
  s-12: "12px"
  s-16: "16px"
  s-24: "24px"
  s-32: "32px"
  bar: "48px"
components:
  topbar:
    backgroundColor: "{colors.panel-mist}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    height: "{spacing.bar}"
  tool-button:
    backgroundColor: "transparent"
    size: "{spacing.bar}"
    padding: "{spacing.s-12}"
  tool-button-hover:
    backgroundColor: "{colors.hover-wash}"
  crumb:
    textColor: "{colors.ink}"
    typography: "{typography.title}"
    height: "{spacing.bar}"
    padding: "0 8px"
  crumb-hover:
    textColor: "{colors.link-sky-deep}"
  row:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    height: "34px"
  row-hover:
    backgroundColor: "{colors.panel-mist}"
    textColor: "{colors.link-sky-deep}"
  row-selected:
    backgroundColor: "{colors.link-sky-deep}"
    textColor: "{colors.ink-inverse}"
  tile:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    height: "40px"
  sidebar:
    backgroundColor: "{colors.panel-mist}"
    textColor: "{colors.ink}"
    padding: "{spacing.s-16}"
  sidebar-button:
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    size: "{spacing.bar}"
  context-menu:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
  context-menu-entry:
    padding: "8px 16px"
  context-menu-entry-hover:
    backgroundColor: "{colors.hover-wash}"
    textColor: "{colors.link-sky-deep}"
  viewer-bar:
    backgroundColor: "{colors.viewer-bar}"
    textColor: "{colors.ink-inverse}"
    height: "{spacing.bar}"
  button-primary:
    backgroundColor: "{colors.link-sky-deep}"
    textColor: "{colors.ink-inverse}"
    rounded: "{rounded.sm}"
    padding: "0 12px"
    height: "28px"
  input:
    backgroundColor: "{colors.panel-mist}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "0 12px"
    height: "28px"
---

# Design System: h5ai-ng

This file records the interface as it ships today.
It is a refinement record, not a redesign: every value below was read from the Less sources in `src/_h5ai/public/css/`, the markup built in `src/_h5ai/public/js/lib/`, the icons in `src/_h5ai/public/images/`, and a rendered build of the Docker image.
Where the code has no decision, the item is listed under Open Items instead of being filled in.

## Overview

**Creative North Star: "The Quiet Ledger"**

The interface is a ruled ledger of files: white rows separated by hairlines, a pale panel for chrome, and one blue for everything that can be acted on.
The files are the content, so the index recedes.
It reads as the Material-2014 era it descends from: flat at rest, 13px type, 48px bars, 2px corners, and shadows only as a response to the pointer.

Density is compact by default and adjustable by the visitor.
Three views (details, grid, icons) share one palette and one hover grammar, and a size slider changes only the icon and row scale.
The interface has no light and dark pair; it is one light surface.

The visual anti-references are file-manager chrome that implies write actions (the product is read-only) and marketing-style heroes, gradients, or decorative color.

**Key Characteristics:**
- Flat at rest; shadow appears only on hover, in the preview, and in popups.
- One chromatic accent, Link Sky Deep, for links, hover text, selection, the selector badge, and the single button style; the lighter Link Sky stays defined and paints nothing.
- Hairline borders at 5% to 7% black instead of boxes or fills.
- Icon-only 48px tool targets that are keyboard buttons with a name and tooltip; section labels live in the sidebar and context menu.
- A 2px focus ring that appears for the keyboard only.
- A plain server-rendered list when JavaScript or the browser is missing.

## Colors

Source: `src/_h5ai/public/css/lib/colors.less`, with the literals named in Open Items.
The palette is Material greys plus one blue, a pink reserved for native text selection, and green and red used only on the admin info page.

### Primary
- **Link Sky** (#42a5f5): the accent's light shade (`@col-blue-400`), for fills that carry no text or glyph.
  Nothing paints it any more: the selector badge held it until batch 3, but a white check on it reaches only 2.65:1 at full opacity and 1.81:1 at the old 0.6 alpha, so the badge moved to Link Sky Deep.
  The token stays in `lib/colors.less`; removing it is a separate decision.
  Its 2.65:1 against white rules out text and white text on it.
- **Link Sky Deep** (#176fcb): the accent wherever it is text or sits under white text (`@col-blue-deep` in `lib/colors.less`).
  It is link and hover text, the selected-row fill, the selector badge (0.8 alpha while an unselected item is hovered, full on the badge itself and on a selected item), the default button fill, the custom header and footer links, and the 2px keyboard focus ring.
  The white check on the badge measures 3.57:1 at 0.8 alpha and 5.03:1 at full opacity.
  Measured in Chromium: 5.03:1 on Paper White and as the ground for white text, 4.82:1 on Panel Mist, 4.52:1 on Panel Mist under a Hover Wash (the backlink on hover).
  The first value chosen for this shade, #1976d2, reached 4.60:1 on white but only 4.41:1 on Panel Mist and 4.13:1 under a Hover Wash, so decision 1 was revised to #176fcb (`docs/decisions/2026-11-02-design-refinement-decisions.md`).

### Secondary
- **Highlighter Pink** (#ff4081): the native text selection background (`::selection`), with white text.
  Nowhere else.

### Neutral
- **Paper White** (#ffffff): the page, item rows, the context menu, and the text preview.
- **Panel Mist** (#fafafa): the top bar, sidebar, row hover, inputs, and the icons-view thumbnail well.
- **Ink** (rgba(0,0,0,0.87)): body text.
- **Ink Secondary** (rgba(0,0,0,0.54)): the "powered by" backlink, the empty-folder and no-match hints, tree summaries, the no-JavaScript list header cells, and hint links in the no-JavaScript bar; 4.59:1 on Paper White, 4.54:1 on Panel Mist.
- **Ink Disabled** (rgba(0,0,0,0.26)): a pending filter or search field (1.88:1; see Open Items).
- **Ink Inverse** (rgba(255,255,255,1)): text on Link Sky Deep (5.03:1), on the viewer bar, and on the scrim; also the focus ring on those surfaces and on selected rows.
- **Hover Wash** (rgba(0,0,0,0.03)): the hover fill for tool buttons, sidebar buttons, and context-menu entries.
- **Hairline** (rgba(0,0,0,0.05)): bar and panel borders, info-panel rules, code chips.
- **Row Rule** (rgba(0,0,0,0.07)): the rule under every details row and under the column header.
- **Hairline Strong** (rgba(0,0,0,0.15)): the dashed drag-selection rectangle.
- **Charcoal** (#212121): the hover color of links in custom headers and footers, and the fullscreen preview background.
- **Slider Track** (#e0e0e0) and **Slider Thumb** (#616161): the size range input in the sidebar.
- **Scrim** (rgba(0,0,0,0.5)): the preview overlay, and the color of the raised and popup shadows.
- **Viewer Bar** (rgb(27,27,27)): the preview bottom bar and the hovered previous and next controls (at 0.8 alpha).

### Status (admin info page only)
- **Pass Green** (#4caf50) and **Fail Red** (#f44336): test results, and the no-JavaScript and old-browser messages (red).

### Named Rules
**The One Voice Rule.** Link Sky Deep is the only chromatic accent in the browsing interface.
Hover is blue text or a 3% black wash, selection is a blue fill; nothing else carries color.
It carries every text, every fill that holds white text, and every glyph that must reach 3:1; the light shade (unused) never does.

**The Pink Selection Rule.** Highlighter Pink belongs to `::selection` and nothing else.

**The Visible Focus Rule.** Keyboard focus shows a 2px solid ring (`:focus-visible`), Link Sky Deep on light surfaces and white on the viewer bar and on selected rows.
Mouse clicks do not show it.
Nothing removes an outline without putting a visible focus style in its place.

## Typography

Source: `src/_h5ai/public/css/lib/fonts.less`, `lib/view/root.less`, `lib/misc.less`, and the per-component sizes in `lib/ext/` and `lib/main/info.less`.

**Body Font:** "Ubuntu", "Roboto", "Helvetica", "Arial", "sans-serif" (no font files are bundled; the visitor's installed fonts decide).
**Mono Font:** "Ubuntu Mono", "Monaco", "Lucida Sans Typewriter", "monospace", for code and preformatted text.
The operator can replace both stacks through `view.fonts` and `view.fontsMono` in `options.json`; the server injects them with `!important` (`src/_h5ai/private/php/core/class-context.php`).

**Character:** a humanist sans at a small, steady size.
Hierarchy comes from weight and opacity, not from size jumps; the only large type is the admin page title.

### Hierarchy
- **Body** (400, 13px, line-height 1.4): rows, tree, sidebar, menus, and the item list at every size.
- **Title** (400, 16px, line-height 48px): breadcrumb labels, with the active crumb in bold (700); also the filter and search fields and the info-panel name.
- **Mono** (400, 15px): code and preformatted text, including the text preview.
- **Hint** (700, 16px, Ink Secondary, 4.59:1): the empty-folder and no-match messages, centered with a 36px top margin.
  The size is the Title step and the bold weight carries it; it was 65px in the 5% black of a Hairline (1.12:1).
- **Display** (300, 52px): the admin info page title only.

Row labels, dates, and sizes use the body size; the row line-height is the icon size plus 14px.
The column header is body size at 0.65 opacity (5.04:1 on Paper White), rising to full opacity and Link Sky Deep on hover.

### Named Rules
**The Weight, Not Size Rule.** Emphasis is bold (active crumb, active tree folder, menu labels) or opacity, never a larger size inside the working list.

## Layout

Source: `src/_h5ai/public/css/lib/view/*.less`, `lib/ext/tree.less`, `lib/ext/info.less`, `lib/responsive.less`.

The root is a full-viewport flex column: a 48px top bar, then a main row that holds the folder tree, the content, and the info panel.
The top bar is a `header`, the content a `main`, the breadcrumb a `nav`, and the sidebar an `aside`; their ids are unchanged.
The top bar carries the sidebar toggle and tool buttons on the left, the breadcrumb filling the middle, and the backlink on the right (36px content plus 12px padding, so 48px).
The sidebar is a column of about 200px at the left of the main row that pushes the tree and the content aside, so nothing is cut off at its edge; under 700px it covers the full width under the top bar instead (see Responsive).
The folder tree is capped at 250px; the info panel is 240px of content with 48px and 32px side padding.

Rhythm is built from 4, 8, 12, 16, 24, 32, and 48px.
The code has no spacing variables, so these are the values that recur as literals; 6px and 28px also appear and are not part of the rhythm.
Page margins are 32px in details and 28px in grid and icons views; tiles sit on an 8px margin.

### Views
- **Details:** one rule-separated row per item, with a 16px-offset icon square, the label, a 130px date column at 116px from the right, and an 80px size column at 16px from the right.
  The row line-height is the icon size (clamped 20 to 80px) plus 14px, so the smallest step is 34px plus a 1px rule, and 44px plus the rule under 700px.
- **Grid:** floated 2px-radius tiles with a square icon (clamped 40 to 160px) beside a 180px label; dates and sizes are hidden.
- **Icons:** floated tiles with a landscape well (icon size clamped 80 to 1000px, tile width four-thirds of that) and a centered 24px-line-height label.

The size steps are the operator's `view.sizes` list in `options.json`.
The Less defaults (16px rows, 48px grid squares, 96px icon wells) apply only until JavaScript injects the per-step rules, so the smallest step (20px) gives 34px rows (44px under 700px) and 40px grid tiles.

### Responsive
The page switches at **700px** (`max-width: 700px`, `lib/responsive.less`):
- the breadcrumb shows only the active crumb, with its leading separator collapsed;
- the folder tree and the info panel are hidden;
- the sidebar covers the full width under the top bar, with no right edge, so the list or grid is never left half-visible beside it (above 700px it sits in the main row and the content is pushed right; the sidebar toggle republishes `resize` so the details view recomputes its width classes);
- the smallest details step grows to a 44px row (5px of padding above and below, date, size and icon shifted by the same amount), the Apple HIG minimum; larger steps are already above it, and WCAG 2.5.8 asks for 24px;
- the preview's previous and next hit areas are hidden (`lib/ext/preview.less`).

Input, not width, decides one rule: `@media (hover: none)` (`lib/ext/select.less`) shows the selector badge on every item as an empty 24px box set beside the item's content instead of on its corner (Selection).
A hybrid laptop whose primary pointer is a mouse keeps the hover behavior.

The details view also reacts to its own width in JavaScript (`src/_h5ai/public/js/lib/view/view.js`): under 480px the date column is hidden and the label margin shrinks, and under 320px the size column is hidden as well.

A print stylesheet clears all backgrounds and shadows, forces black text, and hides the toolbar, sidebar, tree, and info panel.

### No-JavaScript fallback
`html.no-js` and `html.no-browser` turn the root into a normal scrolling page and show a plain table list, at most 960px wide, with 20px PNG icons from `src/_h5ai/public/images/fallback/` and a hint bar above it (`lib/view/fallback.less`).
The table fills the page width and the name column takes what the date and size columns leave, ellipsized when it is too long; at 480px and below the date column is dropped, as in the details view, so the size stays visible at 390px without sideways scrolling.
Header cells use Ink Secondary.
`src/_h5ai/public/js/pre.js` decides which browsers get it and must stay in step with the build target.

## Elevation & Depth

The system is flat at rest and lifts in response to the pointer.
Rows, bars, and panels are separated by 1px hairlines, never by shadow.
Source: `src/_h5ai/public/css/lib/mixins.less` and the view and preview Less files.

### Shadow Vocabulary
- **Raised** (`box-shadow: 0 1px 10px 0 rgba(0,0,0,0.5)`): item hover in all three views (details also raises its z-index), the preview bottom bar, the preview media, the preview text sheet, the hovered previous and next controls, and the default button on hover.
- **Popup** (`box-shadow: 0 1px 20px 0 rgba(0,0,0,0.5)`): the context menu panel only.
- **Pressed** (`box-shadow: inset 0 0 4px 0 rgba(0,0,0,0.4)`): the active view-mode button in the sidebar, over a 3% black wash.
- **Thumb outline** (`box-shadow: 0 0 1px 0 rgba(0,0,0,0.2)`): thumbnails in the details view.

### Layers
Top bar, sidebar, and a hovered details row sit at z-index 1; the selection rectangle at 2; the preview bottom bar at 5; the notification and the preview overlay at 100; the context-menu overlay at 200.
While a drag selection is active, item hover shadows are suppressed.

### Named Rules
**The Flat-By-Default Rule.** Surfaces carry no shadow at rest.
A shadow appears because the pointer is on the thing, or because the thing floats above the page (preview, menu).

## Shapes

Corners are nearly square.
The 2px radius is the house shape: tiles, buttons, inputs, thumbnails, the context menu, the info-panel icon, and the sidebar buttons.
4px appears on the notification (bottom corners only), the admin page code chips, and the support box; 8px on the preview's previous and next controls (inner side only); 20px makes the slider track and thumb pills.
Circles are reserved for loading: the 240px preview placeholder and the spinner backdrop.

Borders are 1px hairlines.
The drag-selection rectangle is the one dashed border.
Transparent images sit on a 60px checkerboard (#f8f8f8 and #e8e8e8) in the preview.
The selector badge is a 22px square in the top-left corner of an item, rounded only at its bottom-right.
Where the device cannot hover it is a 24px box with the 2px house radius, placed beside the content (Selection).

## Components

Source for all of them: `src/_h5ai/public/css/lib/` (view, ext, main) and the markup in `src/_h5ai/public/js/lib/`.
Motion is a single curve: `transition: all 0.2s ease-in-out` on tool buttons, crumbs, sidebar buttons, header cells, and the default button, plus a 0.3s background fade on the preview overlay.
There is no keyframe animation in the styles; the spinner animates inside its own SVG.

### Tool buttons (top bar)
Icon-only, 48px square: a 24px icon with 12px padding on a transparent fill.
Hover is a Hover Wash.
The sidebar toggle, view-mode toggle, filter, search, and download tools use this one shape; filter and search expand an inline 160px, 16px-type, transparent input when active.
Filter ships on in the default `options.json` and search ships off, so a fresh install shows the filter tool; an existing install keeps whatever its own `options.json` says.
With the default `advanced` matching, typed characters match as a subsequence, and a `re:` prefix switches to a regular expression.
A `re:` text that is not a valid expression (for example `re:(`, or `re:(a` while it is being typed) is matched literally as typed, so the field never throws, never stays in `pending`, and a no-match result shows the usual hint.
The check lives in `parsePattern` (`js/lib/util/misc.js`), which both tools use.
Each tool is `role="button"` with `tabindex="0"`; Enter and Space click it (`dom.btn()` in `js/lib/util/dom.js`).
Its name and tooltip come from the l10n key in its `l10n_lb-<key>` class (`filter`, `search`, `download`, `view`, `sidebar`), so non-English locales use their own words and fall back to English.
The ring is inset 2px, because the bar clips overflow.
The expanding tools report `aria-expanded`.
While its input has focus, a 2px Link Sky Deep underline marks the field; text fields match `:focus-visible` for mouse and keyboard alike, so the underline stands in for the ring.

### Breadcrumb
16px type on a 48px line, with 8px label padding and a 24px chevron separator between crumbs; the active crumb is bold and links turn Link Sky Deep on hover.
A page-hint icon follows folders that carry their own index page.
Below 700px only the active crumb remains.

### Item rows (details view)
The signature component.
A white row with a Row Rule underneath, an icon square at 16px from the left, an ellipsized label, and right-aligned date and size.
A focused row shows the focus ring inset on its link, white on a selected row.
Hover turns the row Panel Mist, the text Link Sky Deep (4.82:1), and lifts it with the Raised shadow.
The header row shows Name, Last modified, and Size at 0.65 opacity; a sort chevron appears on the active column and rotates 180 degrees when descending.
The parent-folder row hides its date and size.

### Tiles (grid and icons views)
2px-radius floated tiles on an 8px margin, white on hover Panel Mist, lifted on hover.
The icons view sets the icon or thumbnail in a Panel Mist landscape well above a centered label.

### Selection
Hovering an item shows the selector badge: a Link Sky Deep square at 0.8 alpha with a white check (3.57:1), full opacity (5.03:1) when the pointer is on the badge.
Where the device cannot hover (`@media (hover: none)`) the badge is always there, as an empty 24px box with a 1px Ink Secondary outline (4.59:1) and a 2px radius on a Paper White fill and no check; tapping it fills it with Link Sky Deep and shows the check.
The box sits beside the content with at least 8px of clear space to the icon and to the label text, at every size step:
- **Details:** centred on the row, 4px from the left edge; the icon and the label start 12px further right than on a hover device.
- **Grid:** centred on the tile at its right edge, 8px in; the label's text area is 32px narrower, so the tile keeps its width.
- **Icons:** in the label line under the well, 4px from the left and bottom edges; the label line is 32px high and its text starts 34px in.
A tap on the label still opens the item.
A selected item fills with Link Sky Deep and white text (5.03:1) in every view, and its badge turns to the same fill at full opacity; the fill holds on hover.
Selection is still pointer and touch only (badge click or tap, drag rectangle); no keyboard way to select exists yet.
Dragging over the list draws the dashed selection rectangle (Hairline Strong border, 10% black fill) and switches the cursor to move.

### Sidebar settings
A Panel Mist column with a hairline on its right edge and 16px padding.
Blocks are 168px wide with a 24px bottom margin and a body-size bold heading.
View-mode buttons are 48px, 2px-radius icon buttons with a 4px margin; the active one shows the Pressed shadow and `aria-pressed="true"`.
The info and tree toggles follow the same shape and state; every sidebar control has a name from l10n, and the sidebar is an `aside`.
The size control is a range input with a 6px pill track (Slider Track) and a 16px pill thumb (Slider Thumb); selects are 48px tall with 8px side padding and the same hover wash.

### Folder tree
A 250px-max column with 32px padding (16px on the left) and body-size rows with 3px vertical padding, roughly 24px tall.
A 20px indicator rotates 90 degrees when open, fades to 0.3 while the folder's children are unknown, and disappears when there are none; its hit area is 24px wide (2px of padding offset by a negative margin, so the layout does not move) and 26px tall.
Labels too long for the column end with an ellipsis.
The active folder is bold; summaries ("more subfolders") use Ink Secondary.

### Context menu
A white 2px-radius panel with the Popup shadow, 200px minimum width, 8px and 16px entry padding, a bold label row, 20px icons, and a 1px separator at 8% black.
Entry hover is Link Sky Deep text on a Hover Wash (4.70:1 over Paper White, from the token values; the menu is off in the default configuration and was not rendered).

### Preview
A 50% black overlay (solid Charcoal in fullscreen) with the media centered and raised, a 48px Viewer Bar along the bottom with white 24px icons at 0.7 opacity (1.0 on hover), and previous and next arrows at half opacity that become dark rounded tabs on hover.
The overlay is a labelled modal dialog: opening it moves focus inside, the page behind is `inert` (where supported), and closing returns focus to the row.
The bar is a flex row in tab order previous, next, fullscreen, raw file, close; filename labels stay on the left and give way first (only the first label shows at 480px and below).
Its buttons are named from l10n, show a white ring on keyboard focus, and fullscreen reports `aria-pressed`.
The side arrows duplicate the bar buttons and are hidden from assistive technology.
Text previews sit on a white sheet, at most 960px wide, in mono type for source and 1.1em body type for Markdown, with links in their own blues.
Loading shows a half-opaque circular placeholder and a 100px spinner.

### Info panel
A 240px right column: a 180px icon or thumbnail, a block ruled top and bottom with hairlines holding the name (16px), time, size, and item counts at 20px lines, and a 200px QR code.
Hidden below 700px.

### Notification
A top-centered 200px toast: white text on 20% black, 4px bottom corners, 3px and 6px padding, above everything at z-index 100.

### Custom header and footer
Operator HTML in 16px-margin, 8px-padding blocks above and below the list; links are Link Sky Deep (5.03:1) and turn Charcoal on hover.

### Admin info page controls
The only place the shared form controls appear: a Link Sky Deep 2px-radius button (white text at 5.03:1, 28px line, 12px side padding, Raised shadow on hover) and a 2px-radius input on Panel Mist with a Hairline border.
Test results are 1.4em, with the status in bold Pass Green or Fail Red.

### Icons
Two kinds, both SVG.
UI icons (`src/_h5ai/public/images/ui/`, 22 files) are glyphs on a 24px grid: grey (#555) on light chrome, white for the preview bar and the selector check, and a branded PayPal button on the info page.
File-type icons come from the active theme (`src/_h5ai/public/images/themes/`):
- **default** (11 files: ar, aud, bin, file, folder, folder-page, folder-parent, img, txt, vid, x) is the monochrome #555 20px base set and the fallback for every type.
- **comity** (15 files: ar-apk, ar-deb, ar-rpm, txt-css, txt-go, txt-html, txt-js, txt-less, txt-md, txt-php, txt-py, txt-rb, txt-rust, txt-script, x-pdf) adds colored per-format glyphs over the default set; `options.json` ships with `"theme": "comity"`.
- A theme is a folder of `<type>.<ext>` files; a type with no match falls back to the default set (`src/_h5ai/public/js/lib/core/resource.js`).
- Theme folder names and the file layout are a compatibility surface.
  The favicon is a #555 SVG with PNG and ICO fallbacks (`src/_h5ai/public/images/favicon/`).

Comity icons carry their own palette (for example #fbc02d for JavaScript); those colors are not interface tokens.

## Do's and Don'ts

### Do:
- **Do** keep surfaces flat at rest and use the Raised shadow (`0 1px 10px 0 rgba(0,0,0,0.5)`) only in response to hover or for floating layers.
- **Do** reserve Link Sky Deep (#176fcb) for what can be acted on and carries text or a glyph: links, hover text, selection, the selector badge, the one button; the light Link Sky (#42a5f5) is unused and may only return as a fill with no text or glyph on it.
- **Do** give anything the phone layout shows a target of at least 24px on both sides (44px for rows), and never make a function depend on hover: show it under `@media (hover: none)`.
- **Do** build clickable tool targets as 48px squares (24px icon, 12px padding).
- **Do** separate rows and panels with 1px hairlines at 5% to 7% black.
- **Do** use the 2px radius for new surfaces; reach for 4px or 8px only where the code already does.
- **Do** keep hover to a 3% black wash or blue text with the shared `all 0.2s ease-in-out` transition.
- **Do** keep every layout change working at the 700px switch and in the no-JavaScript list.
- **Do** build a new clickable element as a native control, or with `dom.btn()` and a name from an `l10n_lb-<key>` class, so it works from the keyboard.
- **Do** keep the `<theme>/<type>.<ext>` icon layout and the `default` theme as the fallback.

### Don't:
- **Don't** add a second accent hue, a gradient, or decorative color to the browsing UI.
- **Don't** use Highlighter Pink anywhere except native text selection.
- **Don't** draw resting borders with shadows or add boxes around rows.
- **Don't** add write-action chrome (upload, rename, delete) to the interface; the product is read-only.
- **Don't** enlarge type inside the working list to create emphasis; use weight or opacity.
- **Don't** break icon-theme compatibility: existing theme folders must keep rendering.
- **Don't** write `outline: none` or `outline: 0` without a visible `:focus-visible` replacement, and don't use an image's `alt` for an internal id.

## Open Items

These are facts the code does not settle, listed so they are not mistaken for decisions.
None of them is changed by this document.

- **Dark theme:** none exists; whether one belongs here is undecided.
- **Keyboard coverage:** the tools, sidebar controls, preview bar, and rows are keyboard-reachable with a focus ring.
  Still open: the tree indicators (mouse-only), selecting rows and drag selection, the context menu, an ARIA name for the breadcrumb and tree, and `aria-sort` on the column headers.
  `PRODUCT.md` records that no accessibility standard has been set.
- **Contrast and size:** text and fill pairs of the list, bars, hints, selection and admin button were measured in Chromium against WCAG AA 4.5:1 and pass.
  Still below it: pending fields in Ink Disabled (1.88:1) and the `#pass` placeholder (4.4:1).
  Tree summaries and the no-JavaScript header cells now use Ink Secondary (4.59:1), and the white check on the hover selector badge measures 3.57:1 against the 3:1 asked of a graphic.
  Not measured: the viewer bar icons at 0.7 opacity, the text-preview link and code colors, and the admin test results.
  13px body text is not checked against a size target, and `PRODUCT.md` records that no accessibility standard has been set.
- **Touch targets:** measured in Chromium at 390px with touch emulation, every control the phone layout shows is at least 24px on both sides (tools and sidebar controls 48px, rows 44px, selector badge 24px, preview buttons 48px); the tree is hidden there.
  Above 700px the tree rows are about 27px tall and the indicator hit area 24px wide.
  No touch-target rule has been set, and the 22px hover badge on desktop is below 24px by design.
- **Regular-expression check:** `parsePattern` tests a `re:` expression with the browser's `RegExp`, while search hands the same text to PHP's PCRE, so an expression valid in JavaScript but not in PCRE (or the reverse) can still return no rows in search; the filter has no such gap.
  No server-side message exists for it.
- **Quoted generic family:** `"sans-serif"` is quoted in `lib/fonts.less` and in `view.fonts` in `src/_h5ai/private/conf/options.json`, so browsers read it as a family name rather than the generic fallback.
  `options.json` is an operator-facing compatibility surface, so any change there is a later decision.
- **Fonts are not bundled:** rendering is Ubuntu-first and host-dependent.
- **Product name in the UI:** the backlink ("powered by h5ai"), its link title, and the page titles still say h5ai, while `PRODUCT.md` commits the interface to name h5ai-ng and keep the credit to the original h5ai.
  Copy is unchanged here.
- **Literals outside the palette:** `#2080FF` and `#68A9FF` (text-preview links) and `#008200` (inline code) in `lib/ext/preview-txt.less`; `#f0f0f0` in `lib/view/fallback.less`; `#f8f8f8` and `#e8e8e8` (checkerboard); and several one-off black alphas (0.03, 0.08, 0.1, 0.2, 0.4).
- **Unused palette entries:** `lib/colors.less` defines `@col-grey-100`, `@col-border-stronger`, `@col-divider-black`, `@col-divider-white`, `@col-text-disabled-white`, and `@col-text-secondary-white`, which no style uses; they are left out of the tokens above.
- **Spacing has no named scale:** the `s-` keys label recurring literal values and are not variables in the code.
