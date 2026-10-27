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

# A visitor arriving from the site hasn't decided yet whether they're browsing or
# have files to hand, so each model asks first instead of opening straight onto
# the sample. The sample still loads underneath, so choosing it (or pressing
# Escape) just closes the dialog. Choosing upload clears the sample and points
# at the model's own drop boxes, which open the column-matching step in place.
START_CSS = """#start { border: 1px solid var(--rule); border-radius: 10px; padding: 24px; width: min(calc(100% - 32px), 520px); background: var(--panel); color: var(--ink); box-shadow: 0 20px 60px rgb(0 0 0 / .18) }
#start::backdrop { background: rgb(20 24 23 / .45) }
#start h2 { margin: 0 0 4px; font: 600 22px/1.2 var(--display) }
#start .choices { display: grid; gap: 10px; margin: 18px 0 12px }
#start .choice { display: grid; gap: 2px; text-align: left; padding: 14px 16px; border-radius: 8px; font: inherit }
#start .choice b { font: 600 15px var(--body) }
#start .choice span { font-size: 13px; line-height: 1.45; color: var(--ink-2) }
#start .choice.primary span { color: inherit; opacity: .85 }
.invite-note { margin: 0 0 10px; font-weight: 600; color: var(--accent) }
.loaders.invite .drop { border-style: solid; border-color: var(--accent); background: var(--accent-soft) }
"""

def start(s, sample, upload, invite):
    s = swap(s, "</style>\n\n<div class=\"wrap\">", START_CSS + "</style>\n\n<div class=\"wrap\">")
    s = swap(s, '<div class="loaders">', f'<p class="invite-note" id="inviteNote" hidden>{invite}</p>\n    <div class="loaders">')
    dialog = f"""<dialog id="start" aria-labelledby="startH">
  <h2 id="startH">How do you want to start?</h2>
  <p class="note">You can switch at any time from the Data panel.</p>
  <div class="choices">
    <button type="button" class="choice primary" data-start="sample"><b>Explore with sample data</b><span>{sample}</span></button>
    <button type="button" class="choice" data-start="upload"><b>Upload your own data</b><span>{upload}</span></button>
  </div>
  <p class="note">Your files are read in your browser and stay there.</p>
</dialog>
"""
    s = swap(s, '\n<div class="wrap">\n  <nav class="modules"', "\n" + dialog + '<div class="wrap">\n  <nav class="modules"')
    return swap(s, 'document.getElementById("sampleBtn").click();\n', """document.getElementById("sampleBtn").click();
(() => {
  const d = document.getElementById("start");
  if (!d.showModal) return;   // no <dialog>: the sample it already shows is the start
  const loaders = document.querySelector(".loaders"), note = document.getElementById("inviteNote");
  const settle = () => { loaders.classList.remove("invite"); note.hidden = true };
  d.querySelector('[data-start="sample"]').addEventListener("click", () => d.close());
  d.querySelector('[data-start="upload"]').addEventListener("click", () => {
    document.getElementById("clearBtn").click();
    d.close();
    note.hidden = false; loaders.classList.add("invite");
    note.scrollIntoView({ block: "start" });
    loaders.querySelector("input").focus({ preventScroll: true });
  });
  // Once a file is in, the highlight has done its job.
  loaders.addEventListener("change", settle); loaders.addEventListener("drop", settle);
  d.showModal();
})();
""")

perf = start(perf,
    "Three mock funds from a made-up GP, Lanternfish Ventures. Nothing to prepare.",
    "A GP's fund cash flows, plus its portfolio companies if you have them. CSV or Excel.",
    "Drop your files on the boxes below, or click one to choose a file. Fund cash flows is the one you need; the others add more views.")
exp = start(exp,
    "A mock LP portfolio: ten funds across eight managers. Nothing to prepare.",
    "Your fund commitments and each fund's schedule of investments. CSV or Excel.",
    "Drop your files on the two boxes below, or click one to choose a file. You need both.")

(here / "fund-performance.html").write_text(perf)
(here / "lp-exposure.html").write_text(exp)
