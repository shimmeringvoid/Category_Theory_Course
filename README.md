# Intro to Category Theory

*Objects, arrows, and the discipline of never peeking inside — with animated
diagrams, full proofs, and optional Python labs in which every claim is checked.*

A complete, self-contained ten-lesson course. Each lesson is a single HTML
page: motivation, boxed definitions and theorems with their proofs, worked
examples with commutative diagrams that draw themselves, a section of
computations carried out by hand, a "Going deeper" section, and a large
exercise set with hidden solutions, grouped by topic and running from easier
to harder within each group.

**No programming is required.** Python is an optional track. Every lesson
reads from start to finish without code; the Python lives in clearly marked,
collapsible labs, and an exercise with a Python part always offers it as an
optional extra beside a pen-and-paper version. For readers who do want it,
each lesson's code is also collected in a script and a Jupyter notebook.

## The lessons

| # | Lesson | Highlights |
|---|--------|-----------|
| 01 | [What Is a Category?](lesson-01-what-is-a-category.html) | The two laws; sets, orders, monoids, relations, matrices; isomorphisms; monos & epis |
| 02 | [Functors](lesson-02-functors.html) | `map` fusion as a theorem; hom functors; full, faithful, essentially surjective |
| 03 | [Natural Transformations](lesson-03-natural-transformations.html) | Naturality squares; why `sorted` fails; the functor category; "natural in *X*" |
| 04 | [Equivalence of Categories](lesson-04-equivalence-of-categories.html) | Why isomorphism is too strict; the recognition theorem; skeletons; dualities |
| 05 | [New Categories from Old](lesson-05-new-categories-from-old.html) | Opposites and the duality principle; products; slices; comma categories |
| 06 | [Universal Properties](lesson-06-universal-properties.html) | Products = gcds; a category with *no* products; the uniqueness argument |
| 07 | [Limits & Colimits](lesson-07-limits-and-colimits.html) | Pullbacks are database joins; a formula for every limit of sets; hom functors preserve limits |
| 08 | [Adjunctions](lesson-08-adjunctions.html) | Free ⊣ forgetful; Galois connections; universal arrows; RAPL proved twice; ∃ ⊣ f\* ⊣ ∀ |
| 09 | [Representables & the Yoneda Lemma](lesson-09-representables-and-yoneda.html) | Graphs as presheaves; "track the identity"; Cayley; universal properties as representations |
| 10 | [Monads & Algebras](lesson-10-monads-and-algebras.html) | Monads from adjunctions; Kleisli = partial functions, relations; the algebras of List are the monoids |

Start at [`index.html`](index.html) and read in order — the lessons build
strictly on one another. Lessons 1–5 set up the language, 6–8 are about
universal constructions, and 9–10 are the two summits.

## Two ways through the course

**With pencil and paper.** Read the lesson, work through the "by hand"
section, and do the exercises. Nothing else is needed.

**With Python as well.** Open the optional labs inside each lesson (the
button at the top of a lesson page opens or closes all of them) and run the
code as you go:

```bash
# a lesson's labs, as a script:
python3 code/lesson-07-limits-and-colimits.py

# or interactively:
pip install jupyterlab
jupyter lab notebooks/
```

There are no dependencies beyond the Python 3 standard library. Run notebook
cells top to bottom. A good exercise is to break an assertion on purpose and
understand exactly which law objected.

## Repository layout

```
index.html                     the course's front page
lesson-NN-<topic>.html         the ten lessons; each page is self-contained
                               (styles, diagrams and scripts are inline)
code/lesson-NN-<topic>.py      a lesson's optional Python, as a plain script
notebooks/lesson-NN-….ipynb    the same code as a Jupyter notebook, with outputs
tools/sync_code.py             regenerates code/ and notebooks/ from the pages
tools/check_course.py          checks pages, links, code and generated files
tools/typeset.py               sets symbols upright in formulas, adds italic
                               corrections and sentence spacing
CHANGELOG.md                   what changed between editions
```

## Reproducibility

The lesson pages are the single source of truth for the code. Every code box
on a page runs from the page alone, top to bottom, and every output box is the
verbatim output of the code above it. The files in `code/` and `notebooks/`
are generated from the pages, never edited by hand.

```bash
python3 tools/check_course.py    # run every code box and compare its output with
                                 # the page; check links, anchors, exercise
                                 # numbering, references to exercises and the
                                 # generated files
python3 tools/sync_code.py       # after editing code on a page: regenerate
                                 # code/ and notebooks/
python3 tools/typeset.py         # after editing text on a page: set brackets and
                                 # symbols upright in formulas, space sentences
```

If a page and a program ever disagree, the checker fails — and if you find a
mathematical slip the checker cannot see, please open an issue.

## Publishing with GitHub Pages

The site is plain static HTML at the repository root. In the repository
settings choose **Pages → Deploy from a branch → main / (root)** and the
course will be served at `https://<user>.github.io/<repo>/`.

## Author & license

Course text, diagrams, and site © 2026 Rafael Espericueta
(Professor of Mathematics Emeritus, Bakersfield College), licensed
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
All code (scripts and notebooks) is released under the MIT License.
See [LICENSE](LICENSE) for both notices.
