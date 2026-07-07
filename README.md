# Intro to Category Theory

*Objects, arrows, and the discipline of never peeking inside — with animated
diagrams and every claim checked in Python.*

A complete, self-contained seven-lesson course. Each lesson is a single
polished HTML page — motivation, boxed definitions, worked examples with
commutative diagrams that draw themselves, a "Going deeper" section, and a
large exercise set with hidden solutions — paired with a runnable Python
script and a JupyterLab notebook containing **every program in the lesson,
verified**: each output shown in the pages was actually produced by the code.

## The lessons

| # | Lesson | Highlights |
|---|--------|-----------|
| 01 | [What Is a Category?](lesson-01-what-is-a-category.html) | The two laws; a `FiniteCategory` axiom checker; monos & epis |
| 02 | [Functors](lesson-02-functors.html) | `map` fusion as a theorem; contravariance; the powerset functors |
| 03 | [Natural Transformations](lesson-03-natural-transformations.html) | Naturality squares; why `sorted` and `dedupe` fail; interchange |
| 04 | [Universal Properties](lesson-04-universal-properties.html) | Products = gcds; a category with *no* products, proved by search |
| 05 | [Limits & Colimits](lesson-05-limits-and-colimits.html) | One general limit finder; pullbacks are database joins; pasting |
| 06 | [Adjunctions](lesson-06-adjunctions.html) | foldMap; Galois connections; an adjoint *finder*; ∃ ⊣ f\* ⊣ ∀ |
| 07 | [Yoneda & Monads](lesson-07-yoneda-and-monads.html) | Yoneda *counted*; List/Maybe/Writer laws by enumeration; Kleisli |

Start at [`index.html`](index.html) and read in order — the lessons build
strictly on one another.

## Repository layout

```
index.html, lesson-0*.html    the course website (open index.html locally,
                              or serve via GitHub Pages)
notebooks/lesson-0*.ipynb     one JupyterLab notebook per lesson: all of the
                              lesson's verified code, sectioned and annotated
code/lesson-0*.py             the same code as plain scripts (python3 file.py
                              runs a lesson's entire verification suite)
```

## Running the code

No dependencies beyond the Python 3 standard library.

```bash
# any lesson's full verification suite, as a script:
python3 code/lesson-05-limits-and-colimits.py

# or interactively:
pip install jupyterlab
jupyter lab notebooks/
```

Run notebook cells top to bottom. The best exercise is breaking an assertion
on purpose and understanding exactly which law objected.

## Publishing with GitHub Pages

The site is plain static HTML at the repository root. In the repository
settings choose **Pages → Deploy from a branch → main / (root)** and the
course will be served at `https://<user>.github.io/<repo>/`.

## Reproducibility

Every output block in the HTML pages is the verbatim output of the
corresponding code, which lives in `code/` and `notebooks/`. If a page and a
program ever disagree, the program wins — please open an issue.

## Author & license

Course text, diagrams, and site © 2026 Rafael Espericueta
(Professor of Mathematics Emeritus, Bakersfield College), licensed
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
All code (scripts and notebooks) is released under the MIT License.
See [LICENSE](LICENSE) for both notices.
