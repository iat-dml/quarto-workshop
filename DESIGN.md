---
name: One Tool to Rule Them All — Quarto Workshop
description: The workshop site and decks in the look of the ZALF Science Conference 2026, with the DML brand fonts.
colors:
  mint: "#EFF8E5"
  mint-deep: "#DDEFCB"
  mint-pale: "#F5F8F2"
  leaf: "#4A9E48"
  green: "#2F7F43"
  forest: "#153D31"
  forest-2: "#1F5646"
  ink: "#16322B"
  muted: "#53675E"
  sage-light: "#CFE3C8"
  leaf-light: "#A9DB8F"
  teal-ink: "#2B6A66"
  amber: "#8A5A00"
  red: "#B3261E"
  white: "#FFFFFF"
typography:
  display:
    fontFamily: "DM Serif Display, Georgia, serif"
    fontSize: "clamp(3rem, 6.2vw, 5.1rem)"
    fontWeight: 400
    lineHeight: 1.0
    letterSpacing: "-0.015em"
  headline:
    fontFamily: "DM Serif Display, Georgia, serif"
    fontSize: "2.1rem"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.01em"
  title:
    fontFamily: "DM Serif Display, Georgia, serif"
    fontSize: "1.5rem"
    fontWeight: 400
    lineHeight: 1.2
  body:
    fontFamily: "DM Sans, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "DM Sans, system-ui, sans-serif"
    fontSize: "0.84rem"
    fontWeight: 600
    lineHeight: 1.3
  mono:
    fontFamily: "IBM Plex Mono, ui-monospace, Consolas, monospace"
    fontSize: "0.9em"
    fontWeight: 400
    lineHeight: 1.55
rounded:
  sm: "0.375rem"
  md: "0.75rem"
  lg: "1.125rem"
  pill: "999px"
components:
  button-primary:
    backgroundColor: "{colors.green}"
    textColor: "{colors.white}"
    rounded: "{rounded.pill}"
  button-primary-hover:
    backgroundColor: "{colors.forest}"
    textColor: "{colors.white}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.forest}"
    border: "2px solid {colors.forest}"
    rounded: "{rounded.pill}"
  card:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.lg}"
  callout:
    backgroundColor: "{colors.mint}"
    rounded: "{rounded.md}"
  inline-code:
    backgroundColor: "{colors.mint-deep}"
    textColor: "{colors.forest-2}"
    rounded: "{rounded.sm}"
  code-block:
    backgroundColor: "{colors.mint-pale}"
    rounded: "{rounded.md}"
---

# Design System: One Tool to Rule Them All — Quarto Workshop

## 1. Overview

The site and the ZALF deck share the look of the ZALF Science Conference 2026 website (science-conference.zalf.de): a mint ground, forest-green headings and dark bands, slanted section edges and rounded white surfaces. The type is the DML brand pair (iat-dml/dml-brand-yml): DM Serif Display for headings, DM Sans for text. The DML mark sits in the navbar and the slide corner, the full DML lockup in the footer.

The site is itself a showcase of Quarto output, so it must look like something a careful researcher would publish. On the homepage the design carries the message; on interior reference pages findability comes first and the colour is held back.

Chosen in November 2026 from three mock-ups (institutional ZALF frame, conference look, editorial ZALF gradient). The institutional design system in iat-zalf-slides was judged too plain for a workshop site; this system keeps its greens and its restraint but takes the conference's typography and shapes.

**Key characteristics**

- White pages, with mint for homepage bands, slide grounds, callouts and the closed exercise steps.
- Forest (`#153D31`) for headings and dark bands; green (`#2F7F43`) for links and buttons; leaf (`#4A9E48`) only for bullets, underlines and large shapes.
- Two typefaces and a mono: serif to display, sans to read, mono for code.
- Slanted edges on full-width bands, never on cards.
- One light theme. There is no dark mode.

## 2. Colours

All colours live in `_brand.yml`. `styles.scss` and `revealjs.scss` expose each one as a CSS variable named after its brand token (`--ds-mint`, `--ds-forest`, …); use those, never hex values, in rules and markup.

| Token | Hex | Use |
|---|---|---|
| mint | `#EFF8E5` | Homepage bands, slide ground, callouts, closed exercise steps, the active sidebar item |
| mint-deep | `#DDEFCB` | Open exercise step header and its border, inline code |
| mint-pale | `#F5F8F2` | Code blocks, sidebar hover |
| leaf | `#4A9E48` | Bullet markers, active TOC rule, large shapes. Not for text: 3.4:1 on white |
| green | `#2F7F43` | Links, primary buttons, italic emphasis in titles, labels on cards (4.9:1 on white) |
| forest | `#153D31` | Headings, outline buttons, dark bands (with forest-2 as a 135° gradient), footer |
| ink | `#16322B` | Body text |
| muted | `#53675E` | Secondary text, captions (6.1:1 on white, 5.5:1 on mint) |
| sage-light, leaf-light | `#CFE3C8`, `#A9DB8F` | Secondary text and links on forest |
| teal-ink, amber, red | | Strings in code, warning text, important and caution text |

**The tint marks what you can open or what stands apart.** Long reading happens on white. Mint fills callouts and the closed exercise steps; on the homepage it alternates with white and forest bands. A mint surface never sits on a mint band: on mint, surfaces are white.

## 3. Typography

- **DM Serif Display** (one weight, 400, with italic): page titles, h1 to h4, card titles, team names, exercise step titles, slide titles. Its weight is fixed, so hierarchy comes from size alone.
- **DM Sans** (400 to 700): body text, navigation, buttons, h5 and h6, callout headers, sidebar and TOC labels.
- **IBM Plex Mono**: code.

Italic in a title (`*Rule Them All*`) renders in green. Labels are sentence case in DM Sans 600; nothing is set in capitals, and there are no eyebrow labels above headings.

## 4. Shapes and depth

- **Slanted edges** (`--ds-cut`, up to 72px): full-width homepage bands, the footer, the title slide's band and the dividers' mint wedge. Each band overlaps the previous one by one cut.
- **Radii**: 18px for cards and the video frame, 12px for callouts and code, 14px for exercise steps, pills for buttons.
- **Shadow**: one soft forest shadow (`--ds-shadow`) under white surfaces on mint, and a deeper one on hover for clickable cards, which also rise by 3px. Shadows are mixed from forest, never black.
- **Borders**: hairlines only, mixed from forest. No coloured side stripes.

## 5. Components

### Navbar and footer
White navbar with a hairline shadow, the DML mark (`assets/dml-mark.svg`) and "Quarto workshop" in the serif. No active underline: with one sidebar for the whole site, Quarto marks the first item active on every page. The footer is a forest band with a slanted top, the DML lockup for dark grounds (`assets/dml-lockup-dark.png`, rendered from `dml-strata-lockup-deep-dark.svg` with its fonts baked in) and two links.

### Homepage
Built from full-width divs in `index.qmd`: `.home-band` with `--white`, `--mint` or `--forest`, the hero `.home-hero`, and `.home-band--last` before the footer. Inside, `.home-wrap` holds the 70rem content width. The hero has the title, subtitle, three buttons and `.home-video`, a 16:9 frame with a white border that holds a placeholder until the shortened pitch video replaces it (instructions in the comment above it). The event box is white because the conference logo has a white ground.

### Subject cards
White cards on the mint band: serif title as a stretched link, description in muted, a green line ("Guide and exercise") at the foot. No icons.

### Exercise steps
`{.step}` headings become `<details>` panels (`assets/step-accordion.html`). Closed steps are mint bars with the step title in the serif; the open step has a mint-deep header over a white body with a mint-deep border. The "Open all steps" button is a forest outline pill.

### Callouts
Mint fill, no frame, header in DM Sans 600 coloured by type: forest (note), green (tip), amber (warning), red (important, caution). On slides they are white.

### Code
Inline: mint-deep fill, forest-2 text. Blocks: mint-pale with a hairline on the site, white panels with a shadow on slides. Syntax colours come from the palette (keywords forest, functions green, strings teal-ink, comments muted italic, numbers amber).

### Slides (`revealjs.scss`, `title-slide.html`)
Mint ground; content panels, code, callouts and the `.rendered` output are white. Slide titles in the serif, forest. The DML mark sits bottom right via `logo:` in the deck's YAML; Quarto then moves the slide number to the top right. Footer and mark are hidden on the title slide and on dividers.

- **Title slide** (`title-style: editorial`): event logo top left (`event: logo:`), the title with its italic part on its own line in green, the subtitle in DM Sans, and a forest band across the foot with the presenter and `event.tagline`. The band is drawn inside the slide and runs past its edges, so the text stays on it at any aspect ratio.
- **Dividers** (`# Title {.divider}`): forest gradient with a mint wedge rising to the right. The deck's `background-color` attributes are overridden from the stylesheet, so they need no editing.
- **Checkpoints**: the current step has a green numbered disc, earlier steps a mint-deep tick.
- **Agenda** (`.agenda` > `.agenda-row`): time in green, the part in the serif over a muted line, a green bar on a white timeline track and the length. Each row sets `--start` and `--len` in minutes.
- **Question** (`.question`): a question to the room, large and vertically centred, with prompts underneath.
- **Tabsets**: tabs as DM Sans 600 text with a green rule under the open tab; the content on a white panel.
- **Screen recordings** (`img.screencast`): GIFs in `assets/screencasts/`, made by `_screencasts/record-screencasts.py` from the rendered site. Re-record them when the home page or the deck changes visibly.
- **Lists** in the ZALF deck have 0.6em between items (`slides/zalf-2026.scss`), except the checkpoint steps and the mock output in `.rendered`.

## 6. Do's and don'ts

**Do**
- Take every colour and font from `_brand.yml` through the `--ds-*` variables.
- Keep interior pages white; use mint for callouts, steps and homepage bands.
- Put white surfaces on mint and mint surfaces on white.
- Check text against WCAG 2.1 AA: leaf and mint-deep are never text colours on white.
- Give every transition a `prefers-reduced-motion` fallback and keep visible focus rings.

**Don't**
- Bring back the old Quartile Press system (warm paper, Newsreader, IBM Plex Sans, indigo/coral/moss/amber).
- Add a third typeface, set headings in capitals or put eyebrow labels above headings.
- Use coloured side stripes, gradient text, glassmorphism or decorative icons.
- Slant cards or panels; slants belong to full-width bands only.
- Add a dark theme without drawing and contrast-checking a full dark palette first.
