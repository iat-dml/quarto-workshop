r"""Build the RStudio snippets ms2 to ms5 from index.qmd in this folder.

Run after changing index.qmd:  python make-snippets.py

RStudio runs any `r ...` in a snippet as R code when it inserts the snippet,
so each inline-code backtick is written as `r "\x60"` (which RStudio evaluates
to a single backtick). The editor reads $ as a placeholder, so $ is written \$.
The script checks that undoing both escapes gives back the text in index.qmd.
"""
import re
from pathlib import Path

here = Path(__file__).parent
qmd = (here / "index.qmd").read_text(encoding="utf-8")

setup_end = qmd.index("```\n", qmd.index("#| label: setup")) + 4
para_start = qmd.index("We monitored")
fig_start = qmd.index("```{r}\n#| label: fig-cover")
cite_start = qmd.index("Our monitoring follows")
parts = {
    "ms2": qmd[:setup_end],              # front matter and setup chunk
    "ms3": qmd[para_start:fig_start],    # paragraph with inline code
    "ms4": qmd[fig_start:cite_start],    # figure chunk and cross-reference
    "ms5": qmd[cite_start:],             # citation sentence (fallback)
}

BS = "\\"
TICK_R = '`r "' + BS + 'x60"`'


def body(text):
    text = text.strip("\n")
    text = text.replace(BS, BS + BS).replace("$", BS + "$")
    text = text.replace("`r ", TICK_R + "r ")
    return "\n".join("\t" + line for line in text.split("\n"))


out = "\n".join(f"snippet {name}\n{body(t)}\n" for name, t in parts.items())
(here / "markdown.snippets").write_text(out, encoding="utf-8", newline="\n")


def unescape(block):
    s = "\n".join(line[1:] for line in block.split("\n"))
    s = s.replace(TICK_R, "`")
    return re.sub(r"\\(.)", lambda m: m.group(1) if m.group(1) in "`$\\" else m.group(0), s)


blocks = re.findall(r"snippet (\w+)\n((?:\t.*\n?)+)", out)
rebuilt = {n: unescape(b.rstrip("\n")) for n, b in blocks}
ok = all(rebuilt[n] == parts[n].strip("\n") for n in parts)
print("Wrote markdown.snippets:", ", ".join(n for n, _ in blocks))
print("Round trip matches index.qmd:", ok)
