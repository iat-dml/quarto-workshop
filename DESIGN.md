---
name: One Tool to Rule Them All — Quarto Workshop
description: A scholarly-editorial publishing site that is itself exemplary Quarto output.
colors:
  # Quartile accents (light theme, canonical)
  indigo: "#3D2F8C"
  coral: "#D9543F"
  moss: "#2F7D6A"
  amber: "#C98A2B"
  # Tinted accent surfaces
  indigo-soft: "#EDE9FA"
  coral-soft: "#FBE7E1"
  moss-soft: "#E0EFE9"
  amber-soft: "#F5EAD3"
  # Neutrals — warm paper to deep ink
  paper: "#FBF7F0"
  paper-2: "#F4EFE4"
  paper-3: "#E8E1D2"
  ink: "#1A1B2E"
  ink-2: "#3A3B52"
  muted: "#6B6275"
typography:
  display:
    fontFamily: "Newsreader, Iowan Old Style, Georgia, serif"
    fontSize: "clamp(2.2rem, 4.2vw, 3.4rem)"
    fontWeight: 600
    lineHeight: 1.04
    letterSpacing: "-0.012em"
  headline:
    fontFamily: "Newsreader, Iowan Old Style, Georgia, serif"
    fontSize: "1.9rem"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.012em"
  title:
    fontFamily: "Newsreader, Iowan Old Style, Georgia, serif"
    fontSize: "1.45rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.012em"
  body:
    fontFamily: "IBM Plex Sans, system-ui, -apple-system, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: "normal"
  label:
    fontFamily: "IBM Plex Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "0.74em"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "0.04em"
  mono:
    fontFamily: "IBM Plex Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "0.92em"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
rounded:
  sm: "0.35rem"
  md: "0.5rem"
  lg: "0.75rem"
  pill: "999px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
    padding: "0.55rem 1.1rem"
  button-primary-hover:
    backgroundColor: "{colors.indigo}"
    textColor: "{colors.paper}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0.55rem 1.1rem"
  button-outline-hover:
    backgroundColor: "{colors.paper-2}"
    textColor: "{colors.ink}"
  card:
    backgroundColor: "{colors.paper-2}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "1.1rem 1.2rem"
  chip:
    backgroundColor: "{colors.indigo-soft}"
    textColor: "{colors.indigo}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0.25em 0.7em"
  inline-code:
    backgroundColor: "{colors.moss-soft}"
    textColor: "{colors.moss}"
    rounded: "{rounded.sm}"
    padding: "0.12em 0.38em"
  code-block:
    backgroundColor: "{colors.paper-2}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "1rem 1.1rem"
  blockquote:
    backgroundColor: "{colors.indigo-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0.85rem 1.1rem"
---

# Design System: One Tool to Rule Them All — Quarto Workshop

## 1. Overview

**Creative North Star: "The Quartile Press"**

This is an editorial press rendered in HTML. The page is warm paper stock; the type is set, not typed; and the system carries four signature accent colors — indigo, coral, moss, amber — as its four "quarters," one per family of Quarto output. The whole site is its own proof of concept: a Quarto site that teaches Quarto, so every surface has to read as something a careful researcher would be proud to publish. Restraint is the house style. Warmth comes from the paper, the Newsreader serif, and the quartile accents, never from effects.

The system rejects four things by name. It is **not** the out-of-the-box Bootstrap/Quarto default theme — undifferentiated, obviously templated. It is **not** a corporate SaaS landing page — no gradient hero, no hero-metric stat blocks, no identical feature-card grids, no buzzword copy. It is **not** overdesigned — no decorative animation, no glassmorphism, nothing that competes with reading. And it is done with **AI-slop card scaffolding**: numbered section markers (`01 ·` / `02 ·`) and colored left-stripe borders are recognised tells, slated for removal, never to be extended.

The reader is either mid-workshop or returning in a hurry; both must find the right page fast. On interior reference pages, structure and findability outrank decoration. On the landing page, the design is allowed to carry the message.

**Key Characteristics:**
- Warm paper ground (`#FBF7F0`), deep indigo-black ink (`#1A1B2E`) — never pure white, never pure black.
- Four-accent "quartile" system, used sparingly and meaningfully, one accent per use-case family.
- Serif display (Newsreader) over sans body (IBM Plex Sans) over mono (IBM Plex Mono) — a three-axis contrast, not three competing voices.
- Soft ambient depth at rest, a gentle 2px lift on hover. Nothing floats.
- First-party light and dark `brand.yml` themes, both contrast-checked to WCAG 2.1 AA.

## 2. Colors

A warm-neutral ground carrying four deliberately spaced accents — one cool-deep, one warm, one green, one gold — so each Quarto use-case can own a hue without the palette fragmenting.

### Primary
- **Deep Indigo** (`#3D2F8C`): The brand spine. Links, the active sidebar item, primary emphasis, the Foundations quarter. Conveys depth and trust. In dark theme it lifts to `#A899FF` for contrast.

### Secondary
- **Warm Coral** (`#D9543F`): Energy and warning. Callout accents (important/caution), the italic emphasis inside the page title, the Notebooks quarter, text selection. The single warmest note in the system; deploy it where you want the eye to land.

### Tertiary
- **Forest Moss** (`#2F7D6A`): Code and success. Inline code text on a moss-soft fill, success callouts, the Manuscripts quarter. The "this works" color.
- **Golden Amber** (`#C98A2B`): Signal and highlight. Warning callouts, the Outreach/Advanced quarters. A measured gold, never neon.

### Neutral
- **Paper** (`#FBF7F0`): The page ground. Warm off-white, the default body background.
- **Paper 2** (`#F4EFE4`): Subtle raised surfaces — cards, code blocks, callout bodies.
- **Paper 3** (`#E8E1D2`): Borders and dividers at full strength.
- **Ink** (`#1A1B2E`): Primary text and the primary button fill. A deep indigo-black, not neutral black.
- **Ink 2** (`#3A3B52`): Secondary text, lead paragraphs, nav links at rest.
- **Muted** (`#6B6275`): Tertiary text, captions, section numbers, label/eyebrow text. **Audit:** muted on paper is the system's tightest contrast pairing — verify ≥4.5:1 before using it for anything a reader must actually read; reserve it for genuinely secondary text.

### Tinted Surfaces
- **Indigo / Coral / Moss / Amber Soft** (`#EDE9FA` / `#FBE7E1` / `#E0EFE9` / `#F5EAD3`): Fills for callout bodies, inline code, blockquotes, and chips. Each is a near-white wash of its parent accent.

### Named Rules
**The Quartile Rule.** Each of the four accents maps to a use-case family and keeps that meaning everywhere: indigo = Foundations/links, coral = energy/notebooks, moss = code/success, amber = signal/advanced. Never pick an accent for decoration alone; pick it because it carries that meaning here.

**The Warm-Ground Rule.** Pure `#FFFFFF` and pure `#000000` are forbidden. The page is paper and ink. Every neutral carries a trace of the brand's warmth.

## 3. Typography

**Display Font:** Newsreader (with Iowan Old Style, Georgia, serif)
**Body Font:** IBM Plex Sans (with system-ui, -apple-system, sans-serif)
**Label/Mono Font:** IBM Plex Mono (with ui-monospace, Menlo, monospace)

**Character:** A literary serif paired with a clear, slightly technical humanist sans and an honest mono. The pairing works on a true contrast axis (serif display + sans body + mono labels), so it reads as edited, not indecisive. Newsreader supplies the editorial warmth; Plex Sans keeps long instructional prose comfortable; Plex Mono signals "this is code or a literal token."

### Hierarchy
- **Display** (Newsreader 600, `clamp(2.2rem, 4.2vw, 3.4rem)`, line-height 1.04, tracking -0.012em): Page titles only. Italic `<em>` inside a title renders in Warm Coral.
- **Headline** (Newsreader 600, `1.9rem`, line-height 1.15): `h2` section headings.
- **Title** (Newsreader 600, `1.45rem`, line-height 1.2): `h3` subsection headings.
- **Body** (IBM Plex Sans 400, `1.0625rem`, line-height 1.65): All prose. Cap measure at 65–75ch.
- **Subtitle** (Newsreader 400 italic, `clamp(1.1rem, 1.6vw, 1.35rem)`, Ink 2): The line under a page title.
- **Label** (IBM Plex Mono 500, `0.74em`, tracking 0.04em, UPPERCASE): Chips, tags, table headers, the employer line on team cards, sidebar/TOC section labels. ≤4 words only.
- **Mono** (IBM Plex Mono 400, `0.92em`, line-height 1.55): Code blocks and inline code.

### Named Rules
**The Three-Voice Rule.** Three families, no more: serif to display, sans to read, mono to signal code. Adding a fourth typeface is forbidden; hierarchy comes from weight and scale within these three.

**The Caps-Label-Only Rule.** Uppercase is permitted only for labels of four words or fewer (chips, table headers, the mono section labels). Sentences and headings are never set in all caps.

## 4. Elevation

The system is mostly flat, lifted by a single soft ambient shadow that warms rather than darkens (it is mixed from the ink color, not black). Surfaces sit quietly on the paper at rest and rise a gentle 2px on hover. Depth is a response to interaction, not a permanent decoration.

### Shadow Vocabulary
- **Ambient rest** (`box-shadow: 0 1px 2px color-mix(in oklab, #1A1B2E 4%, transparent), 0 6px 24px -10px color-mix(in oklab, #1A1B2E 10%, transparent)`): The resting shadow under cards, callouts, and code blocks. Barely there; it separates the surface from the paper without announcing itself.
- **Lifted hover** (`box-shadow: 0 4px 20px rgba(26,27,46,0.12), 0 2px 6px rgba(26,27,46,0.07)` paired with `transform: translateY(-2px)`): The interactive state for clickable cards.

### Named Rules
**The Warm-Shadow Rule.** Shadows are mixed from Ink (`#1A1B2E`), never pure black. A neutral-black shadow on warm paper reads as cheap and cold.

**The Lift-On-Intent Rule.** The 2px rise is reserved for surfaces the reader can actually click. Don't lift static containers; the motion is a signal, not a flourish.

## 5. Components

### Buttons
- **Shape:** Fully pill (999px radius), weight 500, padding `0.55rem 1.1rem`.
- **Primary:** Ink fill (`#1A1B2E`), Paper text. On hover the fill shifts to Deep Indigo — the button "warms into" the brand color rather than just darkening.
- **Outline:** Transparent fill, Ink text, hairline rule border. On hover, a Paper 2 fill and an Ink 2 border.
- **Hover / Focus:** Color transitions ~120ms ease. Keep a visible `:focus-visible` ring for keyboard users.

### Chips / Tags
- **Style:** Mono Label type (uppercase, tracked), pill shape, a soft-accent fill with its parent accent as text (e.g. indigo-soft bg / indigo text).
- **Use:** Exercise labels, metadata badges. Never as decorative sprinkles.

### Cards / Containers
- **Corner Style:** `0.75rem` (lg) radius.
- **Background:** Paper 2 on the Paper ground.
- **Shadow Strategy:** Ambient rest → Lifted hover (see Elevation). Clickable cards get `cursor: pointer` and the 2px lift.
- **Border:** A single hairline rule on **all four sides** — `1px solid` of the 12%-ink rule color. **No colored left-stripe.** (The current homepage subject cards and team cards still carry a 3px colored `border-left`; that is the flagged slop and is being removed, not the pattern to copy.)
- **Internal Padding:** ~`1.1rem` to `1.2rem`.

### Inputs / Fields
- **Style:** Hairline rule border, Paper or Paper 2 fill, `md` (0.5rem) radius, body type.
- **Focus:** Border shifts to Deep Indigo with a soft indigo focus ring. No glow, no glassmorphism.
- **Placeholder:** Must clear 4.5:1 — use Ink 2, not Muted.

### Navigation
- **Navbar:** Paper background with a hairline bottom rule and a faint `saturate(1.1) blur(6px)` backdrop. Brand in Newsreader; nav links in Plex Sans 500, Ink 2 at rest → Ink on hover/active.
- **Sidebar:** Mono uppercase section labels (Muted); item text in Ink 2 → Deep Indigo on hover/active. The active item carries a 2px indigo left-accent — the one sanctioned left-accent in the system, because it marks position in a list rather than decorating a card.
- **TOC (right rail):** Small (`0.88rem`), mono uppercase title, active entry in Deep Indigo.

### Callouts
- **Style:** Paper 2 body, `lg` radius, hairline rule, ambient-rest shadow, header in Plex Sans 600. The colored accent rides the **left edge (4px)** and the header text matches: indigo (note), moss (tip), amber (warning), coral (important/caution). This left-accent is Quarto's native callout idiom and is the **one** place a thick colored left-edge is allowed — it is not licence to put stripes on cards.

### Code
- **Inline:** Moss text on Moss Soft fill, `sm` radius, a hairline moss-tinted border, `0.9em`.
- **Block:** Paper 2 fill, hairline rule, `md` radius, `0.92em` Plex Mono at line-height 1.55. Copy button in Muted → Deep Indigo on hover.

### Blockquote
- Indigo Soft fill, 3px indigo left border, Newsreader italic at `1.08em`. The editorial pull-quote voice of the system.

### Signature Component — The Quartile Rule (`<hr>`)
Horizontal rules render not as a line but as a 10px four-square mark: indigo / coral / moss / amber in a 2×2, the system's logo in miniature. Use it as a section break with meaning; it is the press's colophon.

## 6. Do's and Don'ts

### Do:
- **Do** keep the warm paper-and-ink ground. Background is Paper (`#FBF7F0`), text is Ink (`#1A1B2E`).
- **Do** honor the Quartile Rule — each accent carries its use-case meaning everywhere it appears.
- **Do** border cards on all four sides with a single hairline rule; let the ambient shadow and the 2px hover lift carry separation and interactivity.
- **Do** keep prose at 65–75ch and body type at line-height 1.65.
- **Do** restrict uppercase to mono labels of ≤4 words.
- **Do** mix shadows from Ink, never black, and reserve the 2px lift for clickable surfaces.
- **Do** provide a `prefers-reduced-motion` alternative for every transition, and a visible `:focus-visible` ring everywhere.
- **Do** verify Muted-on-Paper hits ≥4.5:1 before using it for readable text; bump to Ink 2 if it's close.

### Don't:
- **Don't** ship the generic default docs theme look — the out-of-the-box Bootstrap/Quarto template is an explicit anti-reference.
- **Don't** build a corporate SaaS landing — no gradient hero, no hero-metric stat blocks, no identical feature-card grids, no buzzword copy ("streamline", "empower", "seamless", "world-class").
- **Don't** overdesign — no decorative animation, no glassmorphism, no effect that competes with reading.
- **Don't** use colored left-stripe borders greater than 1px on cards, list items, or grid items (the homepage subject/team cards currently do; they are being reworked). The callout left-accent and the active-sidebar accent are the only sanctioned exceptions.
- **Don't** scaffold sections with numbered markers (`01 ·` / `02 ·`) by reflex — numbers earn their place only in a genuine ordered sequence.
- **Don't** use gradient text (`background-clip: text`) or pure-white/pure-black anywhere.
- **Don't** add a fourth typeface, and don't set sentences or headings in all caps.
- **Don't** use Muted gray for body text or placeholders — it fails contrast on warm paper.
