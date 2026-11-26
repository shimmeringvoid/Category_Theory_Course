#!/usr/bin/env python3
"""Check the whole course: pages, code, generated files and links.

Run from the repository root (standard library only):

    python3 tools/check_course.py

What is checked

  pages      each lesson page is well-formed, its exercises are numbered
             1, 2, 3, ... and each has a solution, its diagrams are defined,
             and every link and in-page anchor resolves
  exercises  the caption of each exercise group ("§5 · Exercises 9–11")
             names exactly the exercises under it, and every reference to
             an exercise ("Exercise 12", "Lesson 6, Exercise 8") names one
             that exists
  optional   every code box sits inside an optional Python lab or the
             optional Python part of an exercise, so that each lesson can be
             read without any code
  code       the code boxes of each page run, top to bottom, from the page
             alone, and print exactly the output shown on the page
  generated  code/*.py and notebooks/*.ipynb are what tools/sync_code.py
             would write, and each script prints the page's outputs
  index      index.html and README.md list every lesson

Exit status 0 means everything passed.
"""
import contextlib, io, os, re, subprocess, sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_code import ROOT, CODE_BOX, Lesson, lesson_pages, text   # noqa: E402

VOID = {"meta", "link", "br", "hr", "img", "input", "path", "circle", "rect",
        "line", "polyline", "polygon", "ellipse", "use", "stop"}


def unbalanced_tags(page):
    "a few messages about tags that do not nest properly ([] if all is well)"
    errors, stack = [], []

    class Parser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag not in VOID:
                stack.append((tag, self.getpos()[0]))

        def handle_endtag(self, tag):
            if tag in VOID:
                return
            if stack and stack[-1][0] == tag:
                stack.pop()
                return
            errors.append(f"line {self.getpos()[0]}: unexpected </{tag}>")
            if tag in [t for t, _ in stack]:
                while stack.pop()[0] != tag:
                    pass

    Parser(convert_charrefs=True).feed(page)
    return (errors + [f"<{t}> opened on line {n} is never closed" for t, n in stack])[:5]


def spans(page, opener, tag):
    "(start, end) of every element whose opening tag matches `opener`"
    token = re.compile(rf"<{tag}\b|</{tag}>")
    out = []
    for m in re.finditer(opener, page):
        depth = 0
        for t in token.finditer(page, m.start()):
            depth += -1 if t.group(0).startswith("</") else 1
            if depth == 0:
                out.append((m.start(), t.end()))
                break
    return out


def check_page(lesson, all_pages):
    page, problems = lesson.html, []
    name = os.path.basename(lesson.path)
    if not page.lstrip().lower().startswith("<!doctype html>"):
        problems.append("no <!DOCTYPE html>")
    problems += unbalanced_tags(page)

    # exercises
    numbers = [int(n) for n in re.findall(r'<span class="pn">Exercise (\d+)</span>', page)]
    if numbers != list(range(1, len(numbers) + 1)):
        problems.append(f"exercises are not numbered consecutively: {numbers}")
    probs = spans(page, r'<div class="prob">', "div")
    if len(probs) != len(numbers):
        problems.append(f"{len(numbers)} exercise headings but {len(probs)} exercise boxes")
    for k, (a, b) in enumerate(probs, 1):
        if "<summary>Show solution</summary>" not in page[a:b]:
            problems.append(f"Exercise {k} has no solution")

    # exercise groups: each caption names the exercises that follow it
    heads = [(m.start(), int(m.group(1)))
             for m in re.finditer(r'<span class="pn">Exercise (\d+)</span>', page)]
    captions = [(m.start(), text(m.group(1)))
                for m in re.finditer(r'<p class="exmeta">(.*?)</p>', page, re.S)]
    if captions and heads and heads[0][0] < captions[0][0]:
        problems.append("Exercise 1 comes before the first exercise group")
    for i, (start, caption) in enumerate(captions):
        end = captions[i + 1][0] if i + 1 < len(captions) else len(page)
        under = [n for at, n in heads if start < at < end]
        m = re.search(r"Exercises? (\d+)(?:–(\d+))?$", caption)
        named = list(range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1)) if m else []
        if named != under:
            problems.append(f"the group captioned {caption!r} contains exercises {under}")

    # diagrams
    used = set(re.findall(r'data-diagram="([^"]+)"', page))
    defined = set(re.findall(r"^  ([A-Za-z0-9_]+): \{", page, re.M))
    if used - defined:
        problems.append(f"diagrams used but not defined: {sorted(used - defined)}")

    # links and anchors
    ids = set(re.findall(r'\bid="([^"]+)"', page))
    for href in re.findall(r'<a\b[^>]*\bhref="([^"]+)"', page):
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        target, _, anchor = href.partition("#")
        if target and not os.path.exists(os.path.join(ROOT, target)):
            problems.append(f"broken link: {href}")
        if not target and anchor and anchor not in ids:
            problems.append(f"broken anchor: {href}")

    # previous / next
    i = all_pages.index(lesson.path)
    for neighbour in ([all_pages[i - 1]] if i else []) + all_pages[i + 1:i + 2]:
        if f'href="{os.path.basename(neighbour)}"' not in page:
            problems.append(f"no link to neighbouring lesson {os.path.basename(neighbour)}")
    if 'href="index.html"' not in page:
        problems.append("no link back to index.html")

    # Python must be optional: every code box inside a lab or an optional box
    optional = (spans(page, r'<details class="pylab"', "details")
                + spans(page, r'<div class="pytask"', "div"))
    for m in CODE_BOX.finditer(page):
        if not any(a <= m.start() and m.end() <= b for a, b in optional):
            problems.append(f"code box {m.group('name')!r} is not inside an optional Python box")
    if lesson.blocks and not spans(page, r'<details class="pylab"', "details"):
        problems.append("page has code but no optional Python lab")
    return [f"{name}: {p}" for p in problems]


REFERENCE = re.compile(
    r"(?:Lesson (\d+)(?:, |’s |&rsquo;s ))?Exercises? "
    r"(\d+(?:\([a-z]\))?(?:(?:, | and )\d+(?:\([a-z]\))?)*)")


def check_references(lessons):
    "every 'Exercise 12' or 'Lesson 6, Exercise 8' must name an exercise that exists"
    heading = r'<span class="pn">Exercise \d+</span>'
    count = {l.number: len(re.findall(heading, l.html)) for l in lessons}
    problems = []
    for lesson in lessons:
        for m in REFERENCE.finditer(re.sub(heading, "", lesson.html)):
            where = int(m.group(1)) if m.group(1) else lesson.number
            for n in re.findall(r"\d+", m.group(2)):
                if where not in count or not 1 <= int(n) <= count[where]:
                    problems.append(f"{os.path.basename(lesson.path)}: {m.group(0)!r} — "
                                    f"Lesson {where} has no Exercise {n}")
    return problems


def check_code(lesson):
    "run the page's code boxes in order; compare with the outputs shown"
    name, problems = os.path.basename(lesson.path), []
    namespace = {"__name__": "__main__"}
    for block in lesson.blocks:
        captured = io.StringIO()
        try:
            with contextlib.redirect_stdout(captured):
                exec(compile(block["code"], block["name"], "exec"), namespace)
        except BaseException as error:          # report it and carry on
            problems.append(f"{block['name']}: {type(error).__name__}: {error}")
        printed = captured.getvalue().rstrip("\n")
        shown = block["output"] or ""
        if printed != shown:
            problems.append(f"{block['name']}: the page shows\n{shown}\n  but the code prints\n{printed}")
    return [f"{name}: {p}" for p in problems]


def check_generated(lesson):
    name, problems = os.path.basename(lesson.path), []
    for target, content in lesson.targets().items():
        rel = os.path.relpath(target, ROOT)
        if not os.path.exists(target):
            problems.append(f"{rel} is missing — run tools/sync_code.py")
        elif open(target, encoding="utf-8").read() != content:
            problems.append(f"{rel} is out of date — run tools/sync_code.py")
    script = os.path.join(ROOT, "code", lesson.stem + ".py")
    if os.path.exists(script):
        run = subprocess.run([sys.executable, script], capture_output=True, text=True,
                             encoding="utf-8", cwd=ROOT, timeout=600)
        expected = "".join(b["output"] + "\n" for b in lesson.blocks if b["output"])
        if run.returncode != 0:
            problems.append(f"code/{lesson.stem}.py exits with status {run.returncode}: "
                            + run.stderr.strip().splitlines()[-1])
        elif run.stdout != expected:
            problems.append(f"code/{lesson.stem}.py does not print the outputs shown on the page")
    return [f"{name}: {p}" for p in problems]


def check_index(lessons):
    problems = []
    for filename in ("index.html", "README.md"):
        path = os.path.join(ROOT, filename)
        if not os.path.exists(path):
            problems.append(f"{filename} is missing")
            continue
        content = open(path, encoding="utf-8").read()
        for lesson in lessons:
            if lesson.stem + ".html" not in content:
                problems.append(f"{filename} does not mention {lesson.stem}.html")
        if filename == "index.html":
            for href in re.findall(r'<a\b[^>]*\bhref="([^"#]+)"', content):
                if not href.startswith(("http://", "https://", "mailto:")) \
                        and not os.path.exists(os.path.join(ROOT, href)):
                    problems.append(f"index.html: broken link: {href}")
    return problems


def main():
    pages = lesson_pages()
    lessons = [Lesson(p) for p in pages]
    numbers = [l.number for l in lessons]
    problems = []
    if numbers != list(range(1, len(numbers) + 1)):
        problems.append(f"lesson files are not numbered consecutively: {numbers}")
    for lesson in lessons:
        found = check_page(lesson, pages) + check_code(lesson) + check_generated(lesson)
        exercises = len(re.findall(r'<span class="pn">Exercise \d+</span>', lesson.html))
        status = "ok" if not found else f"{len(found)} PROBLEM(S)"
        print(f"lesson {lesson.number:02d}  {exercises:2d} exercises  "
              f"{len(lesson.blocks):2d} code boxes  {status}")
        problems += found
    problems += check_references(lessons)
    problems += check_index(lessons)
    for p in problems:
        print("  !!", p)
    total = sum(len(l.blocks) for l in lessons)
    print(f"\n{len(lessons)} lessons, {total} code boxes: "
          + ("all checks passed" if not problems else f"{len(problems)} problem(s)"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
