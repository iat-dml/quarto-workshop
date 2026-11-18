# One Tool to Rule Them All: Quarto for Documentation, Presentations, Manuscripts and Outreach

**Website: [iat-dml.github.io/quarto-workshop](https://iat-dml.github.io/quarto-workshop/)**

This repository contains the source for a guided workshop website on [Quarto](https://quarto.org/), the open-source scientific and technical publishing system, and its use for typical academic outputs. The workshop can be followed from top to bottom as a live session, or used later as a reference for a specific output format.

The workshop was prepared by the service working group [Data and Modelling Infrastructure for Living Labs (DML)](https://iat-dml.github.io) in the Innovation Centre for Agricultural System Transformation (IAT) at the Leibniz Centre for Agricultural Landscape Research (ZALF). It was first given at the [13th International Congress on Environmental Modelling and Software (2026)](https://conference.iemss.org/) and runs again at the ZALF Science Conference 2026 on 19 November 2026.

## Who this workshop is for

This workshop is especially useful for:

- Early career researchers building their first durable workflow
- Experienced researchers who want fewer disconnected tools
- Teams that care about reproducibility, transparency, and reuse
- Anyone who wants websites, manuscripts, presentations, and notes to be part of the same system

Basic familiarity with at least one programming language such as R, Python, or Julia can help, but it is not required for most of the lessons.

## One system for the many outputs of research

Academic work usually produces many related outputs: rough notes and exploratory analysis that evolve into polished text, figures, and tables; manuscripts for publication; talks for conferences; reports for stakeholders or project partners; and public outreach material. These are often made with tools that are not integrated or compatible, which leads to a fragmented workflow and time lost to manual formatting.

Quarto brings these activities into a single system. You write notes, code, and text in plain text files, then render them into different formats (HTML, PDF, DOCX, slides, dashboards) without switching tools.

## What you will learn

The workshop has a foundations section, five academic use cases, and an advanced section for those who want to go deeper:

1. Foundations: Markdown, YAML, and installing Quarto
2. Research diary: documenting research reproducibly from the outset
3. Manuscripts: writing in plain text and rendering to PDF, HTML, or DOCX
4. Slides: building reveal.js talks from the same source as your research
5. Websites: project, lab, and personal websites for outreach
6. Dashboards: interactive dashboards for exploring and communicating research
7. Advanced topics: templates and extensions, brand.yml, multi-lingual outputs, personalised letters, and AI assistance

Each use case has a companion page with a guided exercise built around an academic scenario.

## Requirements

Quarto 1.8 or newer must be installed (it comes with RStudio 2026.01 and Positron), and `quarto check` should run cleanly in your terminal before starting. The [Installing Quarto](https://iat-dml.github.io/quarto-workshop/foundations/installing-quarto.html) page has the details, including a setup check script for ZALF laptops.

## Building the site locally

```bash
QUARTO_PROFILE=website quarto render
```

The site configuration lives in `_quarto-website.yml` and is only applied with the `website` profile. Some pages run R code, so R and the packages `knitr`, `rmarkdown`, `readr`, `dplyr`, `plotly` and `DT` must be installed. The rendered site in `_site/` is not tracked; a GitHub Actions workflow renders and publishes it from `main`.
