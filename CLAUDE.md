# Adam Dawson — personal site

Static hand-written HTML. No build step, no framework, no dependencies. Each page
is a single self-contained file with its CSS in a `<style>` block and its JS in a
`<script>` block at the end of `<body>`.

## Two styles live here — know which one you're in

The site is mid-redesign, so there are two visual languages side by side. Check
which one the file you're editing belongs to before matching anything.

**Old (most existing pages)** — `index.html`, `about.html`, `reading.html`,
`links.html`, `fatherhood.html`. Dark sidebar nav, `'Crimson Pro', Georgia, serif`,
shared `styles.css`.

**New (`home-draft.html`)** — warm paper background, wooden alphabet blocks, quiet
uppercase controls. Self-contained, does not use `styles.css`. **This file is the
reference for the new direction, and the tokens below are taken from it.**

When redesigning a page, target the new language unless told otherwise.

## Files

| File | What it is |
|---|---|
| `index.html` | **Live home page, and the style reference for the new language.** Self-contained apart from the favicon and the analytics tag. |
| `home-draft.html` | The draft `index.html` was promoted from. Now **stale**: it still carries the animated root system under Writing, and a third child. Kept because the root animation lives nowhere else. |
| `thoughts.html` | Writing → Thoughts. Entries drift in and out of focus; the field in the foreground catches the ones that match. New language. Entries are placeholder. **Draft — deliberately not deployed**, so its link is held out of the live menu; re-add when it ships. Also the only page carrying no analytics tag. |
| `favicon-block.svg` | Tab icon: the red "A" block, flattened from its live pose. |
| `pine-tree.html` | Illustration library — six versions of a pine tree icon, none in use. Shelved, not dead. |
| `reading-v2.html` | An earlier reading-list redesign attempt that didn't land. Decide whether to build on it or replace it before starting. |
| `styles.css` | Old design language only. |

---

## Design tokens

### Surface

```css
background: radial-gradient(ellipse 90% 70% at 50% 44%,
            #faf8f3 0%, #f2eee5 55%, #e8e3d8 100%);
```

Warm off-white paper, never flat white. Content sits centred in the viewport.

### Type

Two registers, and only two.

**Display** — the name, and nothing else so far:
`"Arial Black", "Helvetica Neue", Helvetica, Impact, system-ui, sans-serif`, weight 900.

**Interface** — every control and label:
```css
font-family: system-ui, "Segoe UI", Helvetica, sans-serif;
font-size: clamp(10px, 1.05vw, 12px);   /* 11px fixed for fixed-position controls */
font-weight: 600;
letter-spacing: .16em;
text-transform: uppercase;
```

The `.16em` tracking is the signature. Anything interactive gets it.

### Ink

| Use | Value |
|---|---|
| Interface text, resting | `#6f665d` |
| Interface text, hover / active | `#2f2a24` |
| Interface text, de-emphasised | `#8a8076` |
| Focus ring | `#3d7ba8` |

### Block palette

Classic four-colour alphabet-block set, cycled in order. Within a block,
everything is one hue — the letter and border are the same colour stepped down.

```js
red    [201,  74,  63]
green  [ 92, 159,  82]
yellow [225, 182,  64]
blue   [ 74, 135, 185]

DARKEN = 0.80   // letter + border: a gentle step down from the face
CORE   = 0.62   // inner cube glimpsed at the corners
```

`DARKEN` is deliberately subtle — it was tuned down from 0.48 on request. Letter
contrast against the panel is ~1.37:1. Fine at 67px; it disappears at icon sizes,
which is why the favicon overrides it to 0.32.

### Lighting

Faces are shaded live from their orientation against a fixed light:

```js
L = (-0.40, -0.55, 0.73)   // upper-left, in front
AMBIENT = 0.52             // faces turned away keep this much colour
shade opacity = (1 - brightness) * 0.85
```

---

## Component patterns

### The pill control

Every button and nav item. Borderless until hovered, so a row of them reads as
text rather than as chrome.

```css
color: #6f665d;
padding: .78em 1.2em;
border-radius: 999px;
border: 1px solid transparent;
transition: color .2s ease, background-color .2s ease, border-color .2s ease;

:hover  { color: #2f2a24; background: rgba(0,0,0,.05); border-color: rgba(0,0,0,.14); }
:focus-visible { outline: 2px solid #3d7ba8; outline-offset: 2px; }
```

### Progressive disclosure

Controls that only apply sometimes stay invisible until they do — see `.reset`,
which fades in only once a block has been disturbed. Pair `opacity` with
`pointer-events: none` and the `disabled` attribute so hidden controls leave the
tab order.

### Motion

`.2s` for colour, `.3s` for position, `.45–.62s` for reveals. Everything is
`ease` or `ease-out`. Nothing bounces, overshoots, or uses a custom bezier.

Always provide `@media (prefers-reduced-motion: reduce)` — collapse durations to
`.01s` and zero the delays rather than removing transitions wholesale.

The block spin was tuned down deliberately, 900 → 520 → 260 deg/sec per px/ms,
with `MAX_SPIN` 2400 → 700 alongside it. A pass now turns a block well under two
revolutions a second, so the faces stay legible going past instead of blurring.
These read low; they are not an oversight. `MAX_SPIN` is the one that governs a
fast swipe — `SPIN_PER_SPEED` only bites on gentler passes.

Note that spin speed is currently coupled to frame rate: the loop advances by
`Math.min(64, now - last)`, so time beyond 64ms in a slow frame is discarded and
the simulation runs behind the wall clock. A fixed-timestep accumulator would
decouple them. Not done yet.

---

## Conventions

- **Self-contained pages.** One file, no shared CSS, no external requests. The
  favicon is the only separate asset.
- **Comments say *why*, not *what*.** The codebase explains non-obvious choices —
  why a dash gap is `2` and not `1`, why the core cube is inset the way it is.
  Match that; skip comments that restate the code.
- **Derive dimensions from one variable.** `--s` is the block edge and everything
  else is `calc()`'d from it, so the whole composition scales from one number.
- **Accessibility is not optional.** Real `<button>` for actions and `<a>` for
  navigation; `aria-expanded` on disclosure toggles; `inert` on collapsed
  regions; visible focus rings.
- **Verify in the browser, not by reasoning.** Preview tools over assumption —
  several bugs this project has hit were invisible in the source and obvious on
  screen.

### Preview pane quirk

The in-app preview frequently refuses to reload and serves stale frames, and
sometimes stops compositing entirely (screenshots time out or return black).
When results look wrong, confirm state by querying the DOM before concluding the
code is broken. Editing the file usually forces a genuine reload.

---

## Current state

`index.html` is live at acld.xyz in the new language: ten tumbling blocks
spelling ADAM / DAWSON, and a horizontal menu beneath them.

Menu targets: About → `about.html`, Bookshelf → `reading.html`,
CWR → `links.html`, Contact → `mailto:adam@acld.xyz`.
**Writing is a `<button>`, not a link** — it toggles a submenu rather than
navigating, and has no page of its own. Still open.

Writing's children are Fatherhood → `fatherhood.html` and Research →
`research.html`, revealed as a plain row that fades up under the button. An
earlier version grew an animated root system down to three children; that was
removed from the live page and survives only in `home-draft.html`. Thoughts is
the third child and is commented out of the menu until `thoughts.html` ships.

**Only the home page has moved to the new language.** About, Bookshelf and CWR
are still the old one, so the menu drops visitors into a different-looking site
— a known transitional state, to be made uniform in a later pass. Naming
diverges too: the home menu says CWR where `links.html` still calls itself
Links, in its title, heading and sidebar. Bookshelf has already been made
consistent everywhere; CWR has not.

Deploying is `git push` to `main` — the live site tracks that branch. There is
no CNAME, workflow or `gh-pages` branch in the repo, so the host is configured
outside it. Drafts and experiments live untracked in the working tree on
purpose; keep them out of deploy commits.
