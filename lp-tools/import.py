"""Copies the two LP models in from acldxyz/rorschach and fits them to this site.

python3 lp-tools/import.py PATH/TO/rorschach/lp-analytics/index.html PATH/TO/exposure.html

The pages are built in rorschach (its build.py); change them there, rebuild,
and run this again rather than editing the copies here. Each step below asserts
that its anchor is still in the page, so a change upstream fails loudly here
instead of quietly dropping the way back to the site.
"""
import pathlib, sys

here = pathlib.Path(__file__).parent
perf_src, exp_src = (pathlib.Path(p).read_text() for p in sys.argv[1:3])

BACK = '<a class="back" href="../venture-lp-tools.html">&larr; Venture LP Tools</a>'

def nav(current):
    links = [("fund-performance.html", "Fund performance"), ("lp-exposure.html", "LP exposure")]
    return ('<nav class="modules" aria-label="Modules">' + BACK + "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in links) + "</nav>")

# The way out sits apart from the two module pills: it leaves the tool rather
# than switching inside it, so it gets no pill of its own. With it the row no
# longer fits a phone, so it wraps between links rather than inside them.
BACK_CSS = (".modules { flex-wrap: wrap } .modules a { white-space: nowrap }\n"
            ".modules .back { border-color: transparent; padding-left: 0; margin-right: 10px }\n"
            ".modules .back:hover { border-color: transparent }\n"
            "@media (max-width: 520px) { .modules .back { flex-basis: 100%; margin: 0 0 4px } }\n")

def swap(s, old, new):
    assert s.count(old) == 1, f"anchor not found exactly once: {old[:60]!r}"
    return s.replace(old, new)

# LP exposure already carries the module nav; its links name rorschach's files.
exp = swap(exp_src, '<nav class="modules" aria-label="Modules"><a href="index.html">Fund performance</a>'
                    '<a href="exposure.html" aria-current="page">LP exposure</a></nav>', nav("lp-exposure.html"))
exp = swap(exp, "</style>\n\n<div class=\"wrap\">", BACK_CSS + "</style>\n\n<div class=\"wrap\">")

# Fund performance on rorschach's main predates the module nav, so it gets the
# nav and the styles LP exposure uses for it.
MODULES_CSS = exp_src[exp_src.index(".modules {"):exp_src.index("\n", exp_src.index('.modules a[aria-current="page"]')) + 1]
perf = swap(perf_src, "</style>\n\n<div class=\"wrap\">\n  <header>",
            MODULES_CSS + BACK_CSS + "</style>\n\n<div class=\"wrap\">\n  " + nav("fund-performance.html") + "\n  <header>")

(here / "fund-performance.html").write_text(perf)
(here / "lp-exposure.html").write_text(exp)
