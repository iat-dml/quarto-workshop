# Presenter material for the ZALF manuscript demo

The demo in `slides/zalf-2026.qmd` (checkpoints 1 to 6) builds this manuscript live in RStudio while participants follow along. The folder name starts with `_`, so the website build ignores it.

| File | What it is |
|---|---|
| `index.qmd` | The finished demo manuscript, identical to the code in the manuscript exercise apart from the author block. Rendered with Quarto 1.8.25 (RStudio's version) on 18 November 2026 to PDF (Typst), HTML and Word. |
| `markdown.snippets` | RStudio snippets `ms2` to `ms5`, generated from `index.qmd`. |
| `make-snippets.py` | Regenerates `markdown.snippets` after you change `index.qmd`: `python make-snippets.py`. |

## Snippets

**Where:** your laptop.

The snippets were copied to `C:\Users\black\AppData\Roaming\RStudio\snippets\markdown.snippets` on 18 November. Restart RStudio once so it reads them.

To use one, type its name in a `.qmd` file in **Source** mode and press **Shift+Tab** (RStudio's key for Markdown snippets). They do not work in the Visual editor.

| Snippet | Inserts | Demo step |
|---|---|---|
| `ms2` | Front matter (your name, ORCID, ZALF) and the setup chunk | 2 |
| `ms3` | The paragraph with inline code | 3 |
| `ms4` | The figure chunk and the sentence that cross-references it | 4 |
| `ms5` | The citation sentence `[@gann2019]` | 5, fallback only |

Test once tonight: **File → New File → Quarto Document**, click **Create Empty Document**, switch to Source, type `ms3`, press Shift+Tab. You should see the paragraph with five `` `r ...` `` expressions. If the expressions come out blank, copy from `index.qmd` instead.

Why the file looks odd: RStudio runs any `` `r ...` `` inside a snippet as R code at the moment you insert it. Each inline expression therefore starts with `` `r "\x60"` ``, which RStudio evaluates to a single backtick, and every `$` is written `\$`. Edit `index.qmd` and regenerate rather than editing the snippets by hand.

To remove the snippets, delete the file above. RStudio's built-in Markdown snippets come back.

## Run sheet (30 minutes)

Before the session:

- In a browser tab, open the manuscript exercise: https://iat-dml.github.io/quarto-workshop/exercises/manuscripts-exercise.html
- Create the folder `C:\Users\black\quarto-workshop` (outside OneDrive). Delete any `my-manuscript` folder left over from rehearsal.
- RStudio: **Tools → Global Options → Appearance**, editor font size 18 or more.

| Step | Minutes | In RStudio |
|---|---|---|
| 1 | 5 | **File → New Project → New Directory → Quarto Manuscript**, name `my-manuscript`, parent folder `C:\Users\black\quarto-workshop`. Open `_quarto.yml`, select all, paste the block from exercise Step 3. |
| 2 | 6 | Files pane: **New Folder** `data`, and save `restoration-sites.csv` from the exercise page into it. Open `index.qmd`, Source mode, select all, delete, type `ms2`, Shift+Tab. **Render** (Ctrl+Shift+K): the PDF with title and byline appears in the Viewer. |
| 3 | 5 | Below the setup chunk: `ms3`, Shift+Tab, Render. Expected: 4 sites, 8 surveys, cover from 46% to 56%, an increase of 10 points. If there is time, change one cover value in the CSV, render, then change it back. |
| 4 | 4 | Below the paragraph: `ms4`, Shift+Tab, Render. The figure is numbered and the text says "Figure 1". |
| 5 | 5 | Switch to Visual (Ctrl+Shift+F4). At the end, type "Our monitoring follows recognised restoration standards ", then **Insert → Citation**, **From DOI**, paste `10.1111/rec.13035`, insert. Switch back to Source and render. Fallback without internet: paste the BibTeX entry from the tip in exercise Step 7 into `references.bib`, then `ms5`, Shift+Tab. |
| 6 | 5 | In `_quarto.yml` add the line `  docx: default` under `html: default`. **Build** tab, **Render Project**. Then Files pane: `_manuscript` folder, click `index.html`, **View in Web Browser**. Show the PDF and Word links under Other Formats. |

## Still untested

These depend on the RStudio interface and could not be checked from the command line:

- Whether the Build tab shows **Render Project** for a manuscript project. If it does not, run `quarto render` in the Terminal tab.
- Whether `quarto` is found in RStudio's Terminal tab on a ZALF kiosk laptop, where RStudio's copy of Quarto is not on the PATH.
- The **Insert → Citation** dialog and the DOI lookup over the conference wifi.
- Shift+Tab for the snippets (see the test above).
