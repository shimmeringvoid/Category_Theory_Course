#!/usr/bin/env python3
"""Typeset the lesson pages: upright symbols in italics, italic corrections, sentence spacing.

Run from the repository root (standard library only) after editing a page:

    python3 tools/typeset.py            # rewrite the pages that need it
    python3 tools/typeset.py --check    # exit 1 if any page needs it

Running it again on a typeset page changes nothing.  What it does:

1. Upright symbols.  Inside formulas (.m, .hom, .var, composition tables) every
   character that is not a letter is set upright — brackets, operators,
   relations, arrows, digits, punctuation — and so are blackboard letters
   (ℕ, ℤ, …).  Inside italic prose (em, i, figure and table captions)
   brackets and mathematical symbols are set upright.  Each run is wrapped in
   <span class="up">.
2. Italic corrections.  An italic letter that overhangs its box (f above all)
   gets room before an upright character, a superscript, or the end of the
   italic element; one that overhangs to the left (f, j, p, y) gets room after
   an upright character.  The amounts are three quarters of each letter's
   overhang in Newsreader Italic at the body weight (460) and text size,
   measured from the font; they are applied as classes pl<N> and pr<N>
   (padding of N/100 em), which every page's stylesheet defines.
3. Sentence spacing.  The space after a sentence-ending . ? or ! in running
   text becomes an en space (U+2002), about two word spaces wide.  It still
   allows a line break, and it hangs at the end of a line.  Abbreviations
   (e.g., i.e.), list labels (ii.) and ellipses are left alone.

Code boxes, program output, scripts, styles and SVG are never touched, and
the visible text of a page never changes apart from those spaces.
"""
import glob, html, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# italic corrections in em, measured from Newsreader Italic (wght 460, opsz 20): 3/4 of the overhang
RIGHT = {"d": 0.05, "f": 0.18, "g": 0.05, "i": 0.04, "j": 0.05, "l": 0.04, "r": 0.03, "C": 0.04, "E": 0.04, "F": 0.07, "H": 0.07, "I": 0.07, "J": 0.08, "K": 0.08, "M": 0.05, "N": 0.08, "P": 0.04, "T": 0.08, "U": 0.08, "V": 0.11, "W": 0.1, "X": 0.08, "Y": 0.1, "Z": 0.07}
LEFT = {"f": 0.14, "g": 0.04, "j": 0.17, "p": 0.07, "y": 0.06, "A": 0.05, "J": 0.03, "M": 0.03, "X": 0.05}
SMALL = 0.72                                   # size of sub/sup relative to the text around them

TOKEN = re.compile(r"<!--.*?-->|</?[a-zA-Z][^>]*>|[^<]+|<", re.S)    # a "<" that starts no tag is text
VOID = {"br", "img", "hr", "input", "meta", "link", "wbr", "source", "col", "area", "base", "path", "circle", "rect", "line", "use"}
SKIP_TAGS = {"script", "style", "pre", "code", "svg", "textarea", "title", "button"}
SKIP_CLASSES = {"code", "out", "code-bar"}
BLOCK = {"p", "div", "li", "ul", "ol", "td", "th", "tr", "table", "thead", "tbody", "h1", "h2", "h3", "h4", "h5", "h6", "br",
         "section", "details", "summary", "figure", "figcaption", "nav", "header", "footer", "main", "pre", "blockquote",
         "caption", "dd", "dt", "dl", "hr", "ol", "aside"}
UPRIGHT_LETTERS = set("ℕℤℚℝℂℙ")
PROSE_UPRIGHT = set("()[]{}⟨⟩")               # plus every character of Unicode category Sm (+, =, ×, →, …)
ENTITY = re.compile(r"&(#\d+|#x[0-9a-fA-F]+|\w+);")


def units(text):
    """raw text -> [(raw, char)], one unit per character or entity"""
    out, i = [], 0
    for m in ENTITY.finditer(text):
        out += [(c, c) for c in text[i:m.start()]]
        out.append((m.group(0), html.unescape(m.group(0)))); i = m.end()
    out += [(c, c) for c in text[i:]]
    return out


def tag_info(tok):
    m = re.match(r"<\s*(/)?\s*([a-zA-Z][\w-]*)([^>]*?)(/)?\s*>$", tok, re.S)
    if not m: return None
    cls = re.search(r'\bclass="([^"]*)"', m.group(3))
    return dict(end=bool(m.group(1)), name=m.group(2).lower(), classes=set(cls.group(1).split()) if cls else set(),
                selfclose=bool(m.group(4)) or m.group(2).lower() in VOID)


def add_class(tok, cls):
    """add an italic-correction class, replacing one of the same side that is already there"""
    if re.search(r'class="[^"]*\b' + cls[:2] + r'\d+\b', tok):
        return re.sub(r'\b' + cls[:2] + r'\d+\b', cls, tok, count=1)
    if 'class="' in tok: return re.sub(r'class="([^"]*)"', lambda m: f'class="{m.group(1)} {cls}"', tok, count=1)
    return re.sub(r"^<(\w+)", lambda m: f'<{m.group(1)} class="{cls}"', tok, count=1)


def is_letter(ch): return unicodedata.category(ch).startswith("L") and ch not in UPRIGHT_LETTERS
def is_mark(ch): return unicodedata.category(ch).startswith("M")


def upright_char(ch, ctx):
    if ch.isspace() or is_mark(ch): return False
    if ctx == "math": return not is_letter(ch)
    return ch in PROSE_UPRIGHT or unicodedata.category(ch) == "Sm" or ch in UPRIGHT_LETTERS


def pad(kind, amount):
    n = int(round(amount * 100))
    return f"{kind}{n}" if n >= 2 else None


# ---------------------------------------------------------------------------------------------- 1 + 2
def upright_and_corrections(body):
    toks = [m.group(0) for m in TOKEN.finditer(body)]
    out = []                                   # output pieces (strings); tags may be patched later by index
    stack = []                                 # dicts: name, ctx, small, root(bool), out_index
    used = set()
    state = dict(last=None)                    # last visible italic letter: (char, small) — or None

    def ctx_now(): return stack[-1]["ctx"] if stack else "normal"
    def small_now(): return stack[-1]["small"] if stack else False
    def in_tbl(): return any(e["name"] == "table" and "tbl" in e["classes"] for e in stack)

    def next_visible(i):
        """first visible character after token i (skipping tags), or ''"""
        for t in toks[i + 1:]:
            if t.startswith("<"):
                info = tag_info(t)
                if info and info["name"] in BLOCK: return ""
                continue
            for _, ch in units(t):
                if not ch.isspace(): return ch
                return " "
        return ""

    for i, tok in enumerate(toks):
        if tok.startswith("<!--"): out.append(tok); continue
        if tok.startswith("<"):
            info = tag_info(tok)
            if not info: out.append(tok); continue
            if info["end"]:
                # close up to the matching element
                e = {}
                while stack:
                    e = stack.pop()
                    if e["name"] == info["name"]: break
                if e.get("root") and state["last"] and e["ctx"] in ("math", "pitalic"):
                    ch, sm = state["last"]
                    nxt = next_visible(i)
                    if nxt not in (".", ",") and ch in RIGHT:
                        c = pad("pr", RIGHT[ch] * (SMALL if sm else 1))
                        if c: out[e["out_index"]] = add_class(out[e["out_index"]], c); used.add(c)
                if e.get("root"): state["last"] = None
                if e["name"] in BLOCK: state["last"] = None
                out.append(tok); continue
            parent, name, cl = ctx_now(), info["name"], info["classes"]
            if parent == "skip" or name in SKIP_TAGS or cl & SKIP_CLASSES: ctx, root = "skip", False
            elif cl & {"cat", "op", "up"}: ctx, root = "upright", False
            elif cl & {"m", "hom", "var"}: ctx, root = "math", parent not in ("math",)
            elif name in ("em", "i"): ctx, root = ("math" if parent == "math" else "pitalic"), parent not in ("math", "pitalic")
            elif name == "figcaption" or (name == "caption" and in_tbl()): ctx, root = "pitalic", False
            elif name in ("td", "th") and in_tbl(): ctx, root = "math", False
            else: ctx, root = parent, False
            small = small_now() or name in ("sub", "sup")
            # superscript straight after an italic letter: room for the overhang
            if name == "sup" and ctx in ("math", "pitalic") and state["last"] and state["last"][0] in RIGHT:
                ch, sm = state["last"]
                c = pad("pl", RIGHT[ch] * (SMALL if sm else 1) / SMALL)
                if c: tok = add_class(tok, c); used.add(c)
            if name in BLOCK or ctx == "upright": state["last"] = None
            out.append(tok)
            if not info["selfclose"]:
                stack.append(dict(name=name, classes=cl, ctx=ctx, small=small, root=root, out_index=len(out) - 1))
            continue
        # ---- text
        ctx = ctx_now()
        if ctx not in ("math", "pitalic"):
            if tok.strip(): state["last"] = None
            out.append(tok); continue
        us = units(tok)
        # segment into runs: mode 'up' while upright characters (and the spaces among them) continue
        runs, mode, cur = [], "it", []
        for raw, ch in us:
            if upright_char(ch, ctx): new = "up"
            elif is_letter(ch): new = "it"
            else: new = mode                                       # spaces, marks, prose punctuation: stay
            if new != mode and cur: runs.append([mode, cur]); cur = []
            mode = new; cur.append((raw, ch))
        if cur: runs.append([mode, cur])
        sm = small_now()
        pieces = []
        for k, (mode, us_) in enumerate(runs):
            text = "".join(r for r, _ in us_)
            if mode == "it":
                pieces.append(text)
                for _, ch in us_:
                    if is_letter(ch): state["last"] = (ch, sm)
                    elif ch.isspace() or is_mark(ch): pass
                    else: state["last"] = None
                continue
            classes = ["up"]
            first = next((ch for _, ch in us_ if not ch.isspace()), "")
            if state["last"] and first not in (".", ",") and state["last"][0] in RIGHT:
                ch, lsm = state["last"]
                c = pad("pl", RIGHT[ch] * (SMALL if lsm and not sm else 1))
                if c: classes.append(c)
            # a following italic letter that overhangs to the left
            if k + 1 < len(runs) and not us_[-1][1].isspace():
                nxt = next((ch for _, ch in runs[k + 1][1] if is_letter(ch)), None)
                if nxt in LEFT:
                    c = pad("pr", LEFT[nxt]); classes.append(c) if c else None
            used.update(classes[1:])
            pieces.append(f'<span class="{" ".join(classes)}">{text}</span>')
            state["last"] = None
        out.append("".join(pieces))
    return "".join(out), used


# ---------------------------------------------------------------------------------------------- 3
ABBREV = {"e.g", "i.e", "cf", "vs", "q.e.d", "Mr", "Dr", "Prof", "Fig", "Eq", "Vol", "al"}
ROMAN = re.compile(r"^(i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)$")
CLOSERS = set("”’\")]")
OPENERS = set("“‘\"([§")
EN = " "


def sentence_spacing(body):
    toks = [m.group(0) for m in TOKEN.finditer(body)]
    # flatten to a stream of visible units with their token positions; tags are boundaries or transparent
    stream = []                                # (kind, payload): ("u", [tok_i, unit_j, char]) | ("tag", info) | ("block",)
    skip_depth, math_depth = [], []
    ctxs = []                                  # per open element: 'skip' | 'math' | None
    tok_units = {}
    for i, tok in enumerate(toks):
        if tok.startswith("<!--"): continue
        if tok.startswith("<"):
            info = tag_info(tok)
            if not info: continue
            if info["end"]:
                while ctxs:
                    nm, c = ctxs.pop()
                    if nm == info["name"]: break
                stream.append(("block",) if info["name"] in BLOCK else ("tag", info, i))
                continue
            parent = ctxs[-1][1] if ctxs else None
            if parent == "skip" or info["name"] in SKIP_TAGS or info["classes"] & SKIP_CLASSES: c = "skip"
            elif parent == "math" or info["classes"] & {"m", "hom", "var"}: c = "math"
            else: c = parent
            if not info["selfclose"]: ctxs.append((info["name"], c))
            stream.append(("block",) if info["name"] in BLOCK else ("tag", info, i, c))
            continue
        c = ctxs[-1][1] if ctxs else None
        us = units(tok); tok_units[i] = us
        for j, (raw, ch) in enumerate(us):
            stream.append(("u", i, j, ch, c))
    edits = {}                                 # (tok_i, unit_j) -> replacement raw ('' to delete)
    n = len(stream)
    k = 0
    while k < n:
        e = stream[k]
        if e[0] != "u" or not e[3] in " \n\t" or e[4] in ("skip", "math"):
            k += 1; continue
        # a whitespace run in prose
        a = k
        while k < n and stream[k][0] == "u" and stream[k][3] in " \n\t" and stream[k][4] not in ("skip", "math"): k += 1
        b = k                                   # run = stream[a:b]
        # look back across inline tags for the sentence end
        p = a - 1
        while p >= 0 and stream[p][0] == "tag": p -= 1
        while p >= 0 and ((stream[p][0] == "u" and stream[p][3] in CLOSERS) or stream[p][0] == "tag"): p -= 1
        if p < 0 or stream[p][0] != "u" or stream[p][3] not in ".?!" or stream[p][4] == "skip": continue
        # the word before the period
        q, word, word_in_math = p - 1, "", False
        while q >= 0 and ((stream[q][0] == "u" and not stream[q][3].isspace()) or stream[q][0] == "tag"):
            if stream[q][0] == "u":
                word = stream[q][3] + word; word_in_math |= stream[q][4] == "math"
            q -= 1
        if stream[p][3] == "." and not word_in_math and (word.endswith(".") or word.rstrip(".") in ABBREV or ROMAN.match(word.lstrip("(")) and (q < 0 or stream[q][0] == "block")):
            continue
        if stream[p][3] == "." and re.fullmatch(r"[A-Z]", word) and not word_in_math and (q >= 0 and stream[q][0] == "u"):
            continue                            # an initial, "S. Mac Lane"
        # look forward
        r = b
        ok = False
        while r < n and stream[r][0] == "tag":
            info = stream[r][1]
            if info["classes"] & {"m", "hom", "var"} and not info["end"]: ok = True; break
            r += 1
        if not ok and r < n and stream[r][0] == "u":
            ch = stream[r][3]
            ok = ch.isupper() or ch.isdigit() or ch in OPENERS
        if not ok: continue
        first = stream[a]
        edits[(first[1], first[2])] = EN
        for x in range(a + 1, b): edits[(stream[x][1], stream[x][2])] = ""
    out = []
    for i, tok in enumerate(toks):
        if i in tok_units and any((i, j) in edits for j in range(len(tok_units[i]))):
            out.append("".join(edits.get((i, j), raw) for j, (raw, _) in enumerate(tok_units[i])))
        else:
            out.append(tok)
    return "".join(out), len([v for v in edits.values() if v == EN])


def typeset(body):
    """typeset an HTML fragment or page; returns (html, italic-correction classes used, sentence spaces made)"""
    body, used = upright_and_corrections(body)
    body, n_sent = sentence_spacing(body)
    return body, used, n_sent


def pad_css():
    """the stylesheet rules for every italic-correction class: pl7 = padding-left .07em, pr18 = padding-right .18em"""
    rules = [f".p{s[0]}{n}{{padding-{s}:.{n:02d}em}}" for s in ("left", "right") for n in range(2, 31)]
    return "/* italic corrections, used by tools/typeset.py */\n" + "\n".join(
        " ".join(rules[i:i + 8]) for i in range(0, len(rules), 8)) + "\n"


def typeset_page(page):
    """typeset the <body> of a whole page; the head, styles and scripts are left alone"""
    a, b = page.index("<body"), page.index("</body>")
    out, _, _ = typeset(page[a:b])
    return page[:a] + out + page[b:]


def pages(root=ROOT):
    return [os.path.join(root, "index.html")] + sorted(glob.glob(os.path.join(root, "lesson-[0-9][0-9]-*.html")))


def main(argv):
    check, stale = "--check" in argv, []
    for path in pages():
        page = open(path, encoding="utf-8").read()
        new = typeset_page(page)
        if new != page:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
    if check:
        for s in stale:
            print("not typeset:", s)
        print("all pages are typeset" if not stale else f"{len(stale)} page(s) need tools/typeset.py")
        return 1 if stale else 0
    print(f"{len(pages())} pages checked" + (f"; typeset {len(stale)}" if stale else "; nothing to do"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
