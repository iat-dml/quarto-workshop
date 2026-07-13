# Talking points: opening and foundations

Approximate speaking time: 6–6½ minutes at a calm pace.

## Red thread

Keep returning to this one mental model:

> A Quarto source combines Markdown for the content, YAML for the configuration, and, when useful, code for computed results. Quarto renders that source into the output you need.

The deliberately modest version of the promise is **one reusable source, many possible outputs**. A paper, website, and talk still need different editing and emphasis; Quarto reduces duplication rather than making those differences disappear.

## Title slide — about 45 seconds

Good morning, and welcome. We are Ben Black from ZALF, and Isabel Nicholson-Thomas and Manuel Kurmann from ETH Zürich. Ben leads Data and Modelling Infrastructure for Living Labs, Isabel is a doctoral researcher, and I am a research assistant.

The title is deliberately a little dramatic: Quarto does not replace every tool. Think about your last project—your notes, the paper, and perhaps a talk or website. Much of the material overlapped, but you probably rebuilt and reformatted it in several places. Today is about a more modest and useful idea: keeping that material in one coherent source and reusing it across outputs.

**Bridge:** So what is the problem this is trying to solve?

## Why Quarto? — about 45 seconds

The individual tools are not necessarily the problem; the friction is at the boundaries between them. We copy text, figures, and references from one place to another, spend time reformatting them, and eventually one version changes while another does not.

Quarto separates the source from the way it is presented. In many cases, producing a webpage rather than a PDF becomes a configuration change instead of a rewrite. That does not mean every output is automatically perfect, and Quarto does not do the research or the editorial thinking for us. It reduces the duplicated packaging work around that research.

**Bridge:** The workshop moves from that basic idea to concrete examples.

## Workshop Roadmap — about 40 seconds

The morning has two halves. First, we establish the small set of concepts shared by every Quarto project. Then we apply the same concepts to different research outputs.

The use cases are a menu, not a checklist. You do not need research diaries, manuscripts, presentations, websites, and dashboards all at once; choose what is useful for your own work. The slides give you orientation, but the actual learning starts when you try an exercise this afternoon. The workshop website keeps the instructions and examples available afterwards.

**Bridge:** Let us first build the shared mental model.

## Foundations — about 20 seconds

These next four slides are essentially all the theory we need today. Keep one sentence in mind: Markdown carries the content, YAML configures the document, and optional code produces results. Quarto renders those ingredients into an output. Everything later is an application of that same model.

## What Is Quarto? — about 55 seconds

Quarto is an open-source publishing system created by Posit, the organisation behind RStudio. “Publishing system” simply means that it takes a source file and turns it into an output such as a document, presentation, or website. It is not a new programming language, and you can use the editor you already know.

If you have used R Markdown, Quarto is the newer and broader continuation of that approach, so much will feel familiar. If you have not, you have not missed a prerequisite: the same overall model works with R, Python, Julia, or with no code at all.

Most `.qmd` files bring together our three ingredients: Markdown for what we write, YAML for document settings, and optional code chunks for calculations, tables, and figures. We will see code become concrete in the use cases rather than in a separate foundation slide.

**Bridge:** Putting those ingredients in one source gives us several practical benefits.

## Key Strengths — about 65 seconds

First, a `.qmd` file is plain text. It remains readable without a particular word processor, and version-control tools can show changes line by line. A Word file can of course be revised and tracked, but it is not naturally stored as a human-readable line-by-line document.

Second, the source can be rendered to several formats. This is the source–presentation separation in practice: the target format is largely configuration, although a polished paper and a polished talk will still need some output-specific adjustment.

Third, code can sit beside the explanation it supports. When the document renders, that code can regenerate numbers, tables, and figures from the data. This does not guarantee reproducibility—the data and software environment still matter—but it removes a common source of stale copy-and-paste results.

And for LaTeX users: Quarto’s standard PDF route uses LaTeX underneath, so you keep its typesetting quality while writing most day-to-day structure in lighter syntax.

**Bridge:** Let us look at the two pieces everyone will use, starting with Markdown.

## Markdown in 30 Seconds — about 45 seconds

Markdown is a small set of plain-text conventions for describing structure. For example, `##` says “this line is a heading,” and two asterisks say “emphasise this text.” This slide is honestly most of what you need to begin; the less common syntax can be looked up when you need it.

The important mindset is that we describe what something *is*, not exactly how it should look. We mark a heading rather than choosing its font size and colour. The renderer decides how a heading looks in a webpage, PDF, or slide deck. That separation is what lets the same source adapt to different outputs. The workshop website has the full reference for the exercises.

**Bridge:** Markdown describes the content. YAML supplies the document-level settings.

## YAML: Configuring Your Document — about 55 seconds

YAML is best thought of as a settings panel written as text. In a Quarto file it normally appears at the top, between these two `---` lines. Each line is a `key: value` setting: here, the title and author are metadata, while `format: pdf` tells Quarto what to produce.

Changing `pdf` to `html` changes the target output without rewriting the body. In a real project we may still refine the result for that medium, but the switch itself is this small.

YAML uses indentation to show which options belong together, so spacing is meaningful. If rendering fails before it reaches the document content, this header is one of the first places to check for a misplaced space or colon.

**Handover:** We now have the complete authoring model: Markdown for content, YAML for configuration, and optional code for results. From here on, we are applying that model to actual research tasks.

## Minimal cue card

- **Title:** Dramatic title, modest promise: overlapping material, one coherent source, reuse across outputs.
- **Why:** The friction is between tools: copying, reformatting, and drifting versions. Reduce duplication, not thought.
- **Roadmap:** Shared foundations first; use cases are a menu; exercises are where learning happens.
- **Foundations:** Markdown = content; YAML = configuration; optional code = results; rendering = output.
- **What is Quarto?:** The publishing step, not a language or editor. Open source, multi-language, three ingredients.
- **Strengths:** Readable and trackable source; several outputs; regenerated results; LaTeX-quality PDF route.
- **Markdown:** Mark structure, not appearance. Learn the basics and look up the rest.
- **YAML:** A settings panel in text. `format` selects the target; indentation carries meaning.
- **Handover:** We have the model; now apply it to real research tasks.

## Honesty guardrails

- Prefer **reuse one source** over **write once**.
- Prefer **largely a configuration change** over **one line produces a perfect new format**.
- Prefer **helps keep computed results current** over **everything is automatically current**.
- Prefer **line-by-line comparison is natural with plain text** over **Word cannot track changes**.
- Prefer **Quarto's standard PDF route uses LaTeX** over **all Quarto PDFs use LaTeX**.
