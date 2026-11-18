# Presenter material for the ZALF manuscript demo

The demo in `slides/zalf-2026.qmd` (checkpoints 1 to 6) builds this manuscript live in RStudio while participants follow along. The folder name starts with `_`, so the website build ignores it.

| File | What it is |
|---|---|
| `index.qmd` | The finished demo manuscript, identical to the code in the manuscript exercise apart from the author block. Rendered with Quarto 1.8.25 (RStudio's version) on 18 November 2026 to PDF (Typst), HTML and Word, including the Methods heading and its cross-reference. |
| `markdown.snippets` | RStudio snippets `ms2` to `ms5`, generated from `index.qmd`. |
| `make-snippets.py` | Regenerates `markdown.snippets` after you change `index.qmd`: `python make-snippets.py`. |

## Snippets

**Where:** your laptop.

The snippets were copied to `C:\Users\black\AppData\Roaming\RStudio\snippets\markdown.snippets` on 18 November, and copied again the same evening after the Methods heading and section cross-reference were added. Restart RStudio once so it reads them.

To use one, type its name in a `.qmd` file in **Source** mode and press **Shift+Tab** (RStudio's key for Markdown snippets). They do not work in the Visual editor.

| Snippet | Inserts | Demo step |
|---|---|---|
| `ms2` | Front matter (your name, ORCID, ZALF, `number-sections: true`) and the setup chunk | 2 |
| `ms3` | The heading `## Methods {#sec-methods}` and the paragraph with inline code | 3 |
| `ms4` | The figure chunk and the sentence that cross-references it | 4 |
| `ms5` | The sentence with the section cross-reference `@sec-methods` and the citation `[@gann2019]` | 5, fallback only |

Test once tonight: **File → New File → Quarto Document**, click **Create Empty Document**, switch to Source, type `ms3`, press Shift+Tab. You should see the Methods heading and the paragraph with five `` `r ...` `` expressions. If the expressions come out blank, copy from `index.qmd` instead.

Why the file looks odd: RStudio runs any `` `r ...` `` inside a snippet as R code at the moment you insert it. Each inline expression therefore starts with `` `r "\x60"` ``, which RStudio evaluates to a single backtick, and every `$` is written `\$`. Edit `index.qmd` and regenerate rather than editing the snippets by hand.

To remove the snippets, delete the file above. RStudio's built-in Markdown snippets come back.

## Run sheet (34 minutes)

| Step | Minutes | What happens |
|---|---|---|
| 1 | 5 | Create the manuscript project and replace `_quarto.yml` |
| 1b | 2 | Click between the Source and Visual editors |
| 2 | 6 | Data folder, front matter and setup chunk, first render |
| 3 | 6 | A Methods heading and the outline, then inline code puts numbers from the data into the text |
| 4 | 4 | A labelled figure and its cross-reference |
| 5 | 6 | A cross-reference to the Methods section and a citation from a DOI, both in the Visual editor |
| 6 | 5 | Add Word and render the whole project |

Step 1b is new and adds two minutes, and the outline in Step 3 and the section cross-reference in Step 5 each add about a minute. If the session runs late, drop the CSV change in Step 3 to win time back.

The Render button (Ctrl+Shift+K) in a manuscript project previews only the HTML article, so Steps 2 to 5 show the web page in the Viewer. The PDF and Word file appear only when Step 6 renders the whole project.

### Before the session

**Where:** your laptop, the evening before and again 10 minutes before the start.

- In a browser tab, open the manuscript exercise: https://iat-dml.github.io/quarto-workshop/exercises/manuscripts-exercise.html
- Create the folder `C:\Users\black\quarto-workshop` (outside OneDrive). Delete any `my-manuscript` folder left over from rehearsal, so the New Project dialog does not complain that the folder exists.
- RStudio: **Tools → Global Options → Appearance**, editor font size 18 or more. Check the size from the back of the room on the projector.
- RStudio: **Tools → Global Options → R Markdown → Basics**, set **Show output preview in** to **Viewer Pane**, click **OK**. The default is **Window**, which opens every render in a separate browser window. The same setting sits under the gear icon next to the Render button (**Preview in Viewer Pane**).
- Check that `readr`, `dplyr` and `ggplot2` are installed: run `library(ggplot2)` in the Console. An error means the package is missing.
- Close every open project and file, so the audience sees a clean RStudio.

### Projector: show RStudio, keep this run sheet on your laptop

**Where:** your laptop, connected to the projector, before participants arrive.

The idea: the projector becomes a second screen next to your laptop screen. The audience sees only what you put on the projector (the slides, then RStudio), and this README stays on the laptop screen where only you can see it.

1. Connect the projector cable, then press **Windows key + P** and choose **Extend**. Do not choose **Duplicate**: that mirrors your laptop screen, run sheet included.
2. **Settings → System → Display**. Click **Identify** to see which number is which screen. If the projector sits to the left of the laptop in the room, drag the boxes into the same order, so the mouse leaves the laptop screen on the side where the projector is.
3. In the same page, click the laptop screen (usually 1), tick **Make this my main display**. New windows and Windows notifications then open on the laptop, not in front of the audience.
4. Turn notifications off for the session: **Settings → System → Notifications → Do not disturb** on. Quit Outlook and Teams, or set Teams to Do not disturb.
5. Open this README on the laptop screen in VS Code and press **Ctrl+Shift+V** to see it formatted. Do not open it in RStudio, which is the window on the projector.
6. Put RStudio on the projector: click RStudio, press **Windows key + Shift + Right arrow** (or Left, depending on where the projector is) to move it across, then **Windows key + Up arrow** to maximise it there.
7. Put the slides on the projector too: open the deck in Edge, move the window across the same way and press **F11** for full screen. Press **S** in the deck to open the speaker notes in a separate window, and keep that window on the laptop.
8. Check from the back of the room that the RStudio text is readable. If it is too small, raise the editor font size, or click the projector screen in **Settings → System → Display** and set **Scale** to 125% or 150%.

During the demo:

- Switch between the slides and RStudio by clicking on the projector, or with **Alt+Tab**. Rehearse Alt+Tab once, because it also lists the README and speaker notes windows.
- To check the run sheet, look down at the laptop screen. Scroll it with the mouse over the README; the projector does not change.
- The mouse pointer is visible to the audience when it is on the projector. Move it back to the laptop before you scroll the README so the audience does not see the pointer wander off.
- Step 6 opens `index.html` in the web browser. If it opens on the laptop screen, move it across with **Windows key + Shift + arrow**.
- If the room uses Teams or Zoom for remote participants as well, share the RStudio and Edge windows one at a time (**Share → Window**), not the whole screen. Remote participants then never see the README either.

### Step 1: create the project (5 minutes)

**Where:** RStudio.

1. **File → New Project → New Directory → Quarto Manuscript**.
2. Directory name `my-manuscript`, **Create project as subdirectory of** `C:\Users\black\quarto-workshop`. If the dialog has a **Use visual markdown editor** box, leave it unticked: ticked, it writes `editor: visual` into the front matter and the file always opens in Visual, where the snippets do not work.
3. Click **Create Project**. RStudio restarts in the new project; this takes a few seconds. Say what is happening while it does.
4. In the Files pane, point at the three files that matter: `index.qmd` (the article), `_quarto.yml` (project settings) and `references.bib` (the bibliography). Ignore anything else the template created.
5. Open `_quarto.yml`, Ctrl+A, then paste the block from exercise Step 3 (copy button on the exercise page). Save with Ctrl+S.
6. Say why: the starter file has `freeze: true`, which would stop the numbers in Step 3 from updating, and on Quarto 1.8 the PDF must come before `html` in the list.

Expect: `_quarto.yml` holds exactly the six lines from the exercise. Wait until most hands show they have the project open before moving on.

### Step 1b: Source and Visual editors (2 minutes)

**Where:** RStudio, `index.qmd` as the template created it.

1. Open `index.qmd`. It opens in **Source**: the plain text file, with `#` for headings, `**` for bold and the YAML front matter between the `---` lines.
2. Click **Visual** at the top left of the editor toolbar (or Ctrl+Shift+F4). The first time, RStudio may show a dialog saying that Visual mode can reformat the Markdown. Tick **Don't show this message again** and continue, and tell the room they will see the same dialog.
3. Point at what changed: headings are set as headings, the front matter is folded at the top, and a toolbar has appeared with bold, italic, lists and an **Insert** menu. Code chunks look the same in both modes and still run.
4. Make one small edit to show the round trip: select a word, press Ctrl+B to make it bold, then click **Source**. The word now reads `**word**`. Visual mode is a view on the same plain text file, not a different file format.
5. Undo the edit with Ctrl+Z and stay in **Source** for Steps 2 to 4.
6. Say when each is useful: Source to see and paste exact code, Visual for writing prose, tables and citations. Step 5 comes back to Visual for the citation dialog.

Expect: everyone ends this step in Source mode. Anyone left in Visual will find the snippets and pasted code behave differently.

### Step 2: front matter, setup chunk and first render (6 minutes)

**Where:** RStudio, `index.qmd` in Source mode.

1. Files pane: **New Folder**, name it `data`.
2. In the browser, click **Download restoration-sites.csv** on the exercise page and save it into `C:\Users\black\quarto-workshop\my-manuscript\data`. In the Files pane, open `data` and show that the CSV is there.
3. In `index.qmd`, Ctrl+A, Delete. Type `ms2`, press Shift+Tab. The front matter and setup chunk appear.
4. Walk through the front matter top to bottom: title, author with ORCID and affiliation, `date: today`, `number-sections: true` (headings get numbers, which Step 5 needs for the section cross-reference), `bibliography: references.bib`. Then the setup chunk: `include: false` runs the code but keeps it out of the article.
5. Click **Render** (Ctrl+Shift+K). The first render takes longer than later ones because R starts and loads the packages.
6. The HTML article appears in the Viewer pane. Point at the title and the byline with the ORCID icon and affiliation. If the Viewer is small, drag the divider or use **View → Panes → Zoom Viewer**.
7. Say that the Render button shows only the web page while writing, because it is fastest; the PDF comes in Step 6.

Expect: a web page with title and byline and no body text yet. If a render fails with "file name conversion problem", that participant has not set `R_USER` (see the R setup slide). If someone's render opens in a browser window, they can switch to the Viewer with the setting in "Before the session"; the browser window works just as well for the demo.

### Step 3: a Methods heading and numbers from the data (6 minutes)

**Where:** RStudio, `index.qmd` in Source mode.

1. Put the cursor on an empty line below the closing ```` ``` ```` of the setup chunk.
2. Type `ms3`, press Shift+Tab. The snippet inserts the heading `## Methods {#sec-methods}` and the paragraph below it.
3. Point at the heading: `##` makes a level 2 heading, and `{#sec-methods}` gives it a label. The `sec-` prefix is what lets the text refer to it later, as `fig-` does for figures in Step 4.
4. Click **Outline** at the top right of the editor toolbar (or Ctrl+Shift+O). The outline lists the headings in the document; click **Methods** in it to jump there. Say that in a full paper with Introduction, Methods, Results and Discussion this is the quickest way to move around. Code chunks appear in the outline only if **Tools → Global Options → R Markdown → Show in document outline** is set to include chunks; the default shows sections only.
5. Point at the five `` `r ...` `` expressions in the paragraph: each one is a small R calculation that Quarto replaces with its result.
6. Render. In the Viewer, show the heading "1 Methods" with its number, then read the sentence aloud: 4 sites, 8 surveys, cover from 46% to 56%, an increase of 10 points.
7. If there is time: open `data/restoration-sites.csv` in RStudio (click it, **View File**), change one `vegetation_cover_pct` value in the last survey, save, render, and show that the sentence changes. Change the value back and save before Step 4.

Expect: a numbered heading "1 Methods" and no backticks or R code in the text, only numbers. Code showing in the output means the backtick before the `r` is missing. A heading without a number means `number-sections: true` is missing from the front matter.

### Step 4: a figure with a cross-reference (4 minutes)

**Where:** RStudio, `index.qmd` in Source mode.

1. Put the cursor on an empty line below the paragraph.
2. Type `ms4`, press Shift+Tab. Point at the label `fig-cover` and the caption line, then at `@fig-cover` in the sentence below the chunk.
3. Render. In the Viewer, show the caption "Figure 1: Vegetation cover ..." and that the sentence reads "Figure 1". Hover over it to show the preview of the figure, then click it: the link jumps to the figure.
4. Say that adding a second figure above this one would renumber both automatically.

Expect: a line chart with four coloured sites and a numbered caption.

### Step 5: a section cross-reference and a citation (6 minutes)

**Where:** RStudio, `index.qmd`, switching to Visual.

The sentence you build is: "The survey design in @sec-methods follows recognised restoration standards [@gann2019]."

1. Click **Visual** (Ctrl+Shift+F4). Click at the end of the last sentence and press Enter for a new paragraph.
2. Type "The survey design in " (with the trailing space).
3. **Insert → Cross Reference**. The dialog lists every label in the document: `sec-methods` and `fig-cover`. Pick `sec-methods` and insert. Say that this is the same mechanism as the figure reference in Step 4, now pointing at a section.
4. Type " follows recognised restoration standards " (spaces at both ends).
5. **Insert → Citation**. Choose **From DOI**, paste `10.1111/rec.13035` and wait for the reference to appear, then click **Insert**. Type the full stop.
6. Click **Source**. Show `@sec-methods` and the new `[@gann2019]` (the key may differ slightly), and say that the paragraph may have been rewrapped; the text is unchanged.
7. In the Files pane, open `references.bib` and show the new entry that the dialog wrote.
8. Back in `index.qmd`, render. Show that the sentence reads "Section 1" and links to the Methods heading, then the citation in the text and the **References** list at the end of the article.

If **Insert → Cross Reference** is missing, type `@sec-methods` directly in Visual mode; RStudio offers it as you type.

Fallback without internet: paste the BibTeX entry from the tip in exercise Step 7 into `references.bib`, save, then in `index.qmd` (Source mode) type `ms5`, Shift+Tab, and render. `ms5` inserts the whole sentence, cross-reference included.

Expect: "The survey design in Section 1 follows ... (Gann et al. 2019)." The PDF fails in Step 6 with "cannot reference heading without numbering" if `number-sections: true` is missing from the front matter; the Viewer does not show this, because the Render button builds only the web page.

### Step 6: Word and the whole project (5 minutes)

**Where:** RStudio.

1. Open `_quarto.yml`. Below `  html: default`, add the line `  docx: default` with the same two spaces of indentation. Save. Wrong indentation is the most likely error here.
2. **Build** tab, **Render Project**. Explain why: the Render button only renders the first format in the list, while Render Project builds all three.
3. Files pane: open the new `_manuscript` folder and show `index.pdf`, `index.html` and `index.docx`.
4. Click `index.html`, **View in Web Browser**. Show the byline, the numbers, the figure and the references, then the PDF and Word links under **Other Formats** in the margin. Open the Word file to show it opens with everything in place.

Expect: three files in `_manuscript/`. If the Build tab has no **Render Project**, run `quarto render` in the Terminal tab.

## Still untested

These depend on the RStudio interface and could not be checked from the command line:

- Whether the Build tab shows **Render Project** for a manuscript project. If it does not, run `quarto render` in the Terminal tab.
- Whether `quarto` is found in RStudio's Terminal tab on a ZALF kiosk laptop, where RStudio's copy of Quarto is not on the PATH.
- The **Insert → Citation** dialog and the DOI lookup over the conference wifi.
- Shift+Tab for the snippets (see the test above).
- Whether the Quarto Manuscript dialog has the **Use visual markdown editor** box, and whether the first switch to Visual shows the reformatting dialog in RStudio 2026.01.
- Whether **Show output preview in: Viewer Pane** also keeps the Build tab's **Render Project** out of the browser.
- The name and place of **Insert → Cross Reference** in RStudio 2026.01's Visual editor, and the **Outline** button and shortcut.
- The projector set-up in the room: whether **Extend** works with the room's projector and cable, and whether ZALF's managed Windows lets you change the main display and Do not disturb.
