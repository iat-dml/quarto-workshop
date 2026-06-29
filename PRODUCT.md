# Product

## Register

brand

_Split surface: the landing page and overall identity are **brand** (the design is part of the message), while the interior reference pages lean **product** (design serves fast lookup). PRODUCT.md carries `brand` as the default; override to product when working purely on interior docs utility._

## Users

Researchers, across two arrival paths:

- **In a live workshop session**, following the site top-to-bottom while learning.
- **Returning later**, jumping straight to one page when stuck on a specific output format.

Spanning early-career researchers building their first durable workflow, experienced researchers tired of juggling disconnected tools, and teams that care about reproducibility, transparency, and reuse. Mixed technical background: comfortable with at least one of R / Python / Julia is helpful but not assumed.

**The job to be done:** learn to author once in plain text and render to many professional outputs (HTML, PDF, DOCX, slides, dashboards, websites) without switching tools, then keep the site as a reference.

## Product Purpose

A guided workshop and standing reference for Quarto, the open-source scientific and technical publishing system. It moves researchers from scattered authoring workflows to a single integrated system, organised as Foundations → Academic Use Cases → Advanced Topics, each section paired with a hands-on exercise grounded in a real academic scenario.

Success: a researcher leaves able to produce a genuine output (research diary, manuscript, talk, or website) in Quarto, and comes back to the site when they need it again. The site is also a working demonstration: built in Quarto itself, it is evidence of what the tool can produce.

## Brand Personality

Scholarly and editorial. Warm, literate, quietly confident, the feel of a well-made academic publication rather than a software landing page. The voice is clear, specific, and generous; it explains the *why*, not only the *how*.

- Three words: **literate, credible, unhurried.**
- Emotional goal: a researcher should feel that adopting Quarto is a calm, sensible upgrade in capable hands, with no hype.

## Anti-references

- **Generic default docs theme** — the out-of-the-box Bootstrap/Quarto look: undifferentiated and clearly templated.
- **Corporate SaaS landing** — gradient hero, hero-metric stat blocks, identical feature-card grids, buzzword copy.
- **Overdesigned / flashy** — heavy animation, glassmorphism, decorative effects that compete with learning.
- **AI-slop card scaffolding** — the current homepage subject cards and after-body nav cards lean on numbered section markers (`01 ·` / `02 ·`) and colored left-stripe borders, both recognised tells. Treat these as the first thing to rework, not a pattern to extend.

## Design Principles

1. **Practice what you preach.** The site is itself exemplary Quarto output; every page is proof the tool can make beautiful, credible work. This is why the landing is brand even though interior reference pages serve their content like a product.
2. **Teach by showing.** Real rendered output and runnable code over abstract description.
3. **Reference-first navigation.** A learner mid-session and a returner-in-a-hurry both find the right page fast; structure and findability beat decoration on interior pages.
4. **Earn every flourish.** Warmth comes from typography, warm paper, and the quartile accents, not from effects. If a decorative element does not aid comprehension, cut it.
5. **Credible, not corporate.** Scholarly restraint throughout; no marketing cadence, no hype.

## Accessibility & Inclusion

Target **WCAG 2.1 AA**.

- Body text ≥ 4.5:1 against its background (watch muted text on warm paper); large text ≥ 3:1.
- Visible keyboard focus and full keyboard navigability.
- Full `prefers-reduced-motion` alternatives for any motion.
- Both the light and dark `brand.yml` themes must pass contrast.
- Content must stay usable when rendered to other Quarto formats (PDF / DOCX) and at small viewports on shared screens during a live session.
