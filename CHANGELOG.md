# Changelog

## Second edition

A full revision of the course: an accuracy review of every page and program,
a large expansion (seven lessons became ten), and a restructuring that makes
Python an optional track.

| | First edition | Second edition |
|---|---|---|
| Lessons | 7 | 10 |
| Words of course text | about 35,000 | about 105,000 |
| Boxed definitions and theorems | 20 | 63 |
| Diagrams | 32 | 52 |
| Exercises with solutions | 78 | 168 |
| Code boxes | 33, in the main text | 56, all inside optional labs and optional exercise parts |

### New numbering

Four pages have new file names, so links to the old ones need updating.

| First edition | Second edition |
|---|---|
| 01 What Is a Category? | 01 What Is a Category? |
| 02 Functors | 02 Functors |
| 03 Natural Transformations | 03 Natural Transformations |
| — | **04 Equivalence of Categories** (new) |
| — | **05 New Categories from Old** (new) |
| 04 Universal Properties (`lesson-04-universal-properties.html`) | 06 Universal Properties (`lesson-06-universal-properties.html`) |
| 05 Limits & Colimits (`lesson-05-limits-and-colimits.html`) | 07 Limits & Colimits (`lesson-07-limits-and-colimits.html`) |
| 06 Adjunctions (`lesson-06-adjunctions.html`) | 08 Adjunctions (`lesson-08-adjunctions.html`) |
| 07 Yoneda & Monads (`lesson-07-yoneda-and-monads.html`) | 09 Representables & the Yoneda Lemma, and 10 Monads & Algebras |

Within each lesson the original exercises keep their numbers (in Lesson 10
the old Exercises 5–11 became 1–7); new exercises were added after them.

### Python is now optional

- Every lesson reads from start to finish without code. The former
  "…in Python" sections are now collapsible **optional labs** inside a new
  **"by hand"** section, which carries out the same computations on paper.
- Every exercise that required code now leads with a pen-and-paper version;
  its Python part is a marked, optional box. (One exercise, Lesson 5's
  Exercise 14, is wholly optional: a machine check of two by-hand exercises.)
- Exercise statements that were written in Python notation (lambda
  expressions, dictionaries, `str.upper`) are now stated in words; the Python
  form is kept in the optional part.
- A button at the top of each lesson opens or closes all of its labs, and
  remembers the choice. The labs start closed.

### Added

- **Lesson 1.** More examples of categories (relations, matrices, discrete
  and empty categories, a table of the large ones); a section on
  isomorphisms; finite categories by hand; monos and epis in **Set**,
  sections and retractions; 7 new exercises.
- **Lesson 2.** Actions, `(−) × A` and the diagonal as functors; hom
  functors; full, faithful and essentially surjective functors, with what
  they preserve and reflect; functors by hand; 7 new exercises.
- **Lesson 3.** Naturality in mathematics (singletons and unions, the
  diagonal, the double dual, equivariant maps); examples of functor
  categories; natural isomorphisms and "natural in *X*"; whiskering on both
  sides; naturality by hand; 7 new exercises.
- **Lesson 4 (new).** Equivalence of categories: definition, the recognition
  theorem (full + faithful + essentially surjective) with a complete proof,
  five examples, what equivalences preserve, skeletons, dualities;
  14 exercises.
- **Lesson 5 (new).** Opposite categories and the duality principle,
  product categories and bifunctors, subcategories, arrow categories, slices
  and coslices, comma categories; 14 exercises.
- **Lesson 6.** Products as terminal spans and the calculus of pairing; a
  catalogue of products and coproducts across categories; universal
  properties by hand; 7 new exercises.
- **Lesson 7.** Monomorphisms as pullbacks; a coequalizer and a pushout
  computed; the limit of an arbitrary diagram of sets; "products and
  equalizers suffice", proved; limits in an order; the theorem that hom
  functors preserve limits; limits by hand; 7 new exercises.
- **Lesson 8.** Naturality of the hom-set bijection spelled out; more
  adjunctions; universal arrows and the pointwise construction of adjoints;
  uniqueness of adjoints, proved; two proofs that right adjoints preserve
  limits; right adjoints preserve monomorphisms; the adjoint functor theorem
  for orders; adjunctions by hand; 8 new exercises.
- **Lesson 9 (from the first half of the old Lesson 7).** Presheaves as data
  (graphs); representable functors; the Yoneda lemma read in an order, for a
  monoid, for graphs and in **Set**; the Yoneda embedding and proofs by
  Yoneda; universal elements, and universal properties as representations;
  Cayley's theorem; density; 11 new exercises.
- **Lesson 10 (from the second half of the old Lesson 7).** The definition
  in components; monads from adjunctions, including closure operators and
  the state monad; the power set monad; Kleisli categories of partial
  functions and of relations; bind; the Kleisli and Eilenberg–Moore
  adjunctions; algebras as a full section; monadicity; 8 new exercises.
- **Every page.** A document type and language, a link back to the index,
  linked breadcrumbs, a table of contents, previous/next links, and links to
  the lesson's script and notebook. (The first edition's lesson pages had no
  links at all.)
- **Narrow screens.** At phone width, six of the seven first-edition lessons
  scrolled sideways (long formulas, wide tables) and the title block touched
  the edge of the screen. Formulas now wrap, tables scroll inside their own
  box, and the title block is inset.

### Corrected

Mathematics and wording, by first-edition lesson number.

- **1 · What Is a Category?**
  - The commuting-square caption read `g ∘ f = q ∘ p`; for the square as
    drawn it is `q ∘ f = g ∘ p`.
  - Exercise 4(d) said the identities are "all present" among the functions
    with a fixed point. The identity of the empty set has none; the solution
    now says so.
  - Exercise 11: "precompose with the inverse" should be compose on the
    left; and a statement that held "vacuously" holds trivially.
  - "Going deeper" promised that Lesson 6 would use adjunctions to detect
    monos and epis, which it never did. The promise is now kept (Lessons 7
    and 8).
  - The first program's associativity "check" compared an expression with
    itself. It is replaced by a check that can fail.
- **2 · Functors.** A reference to "§3's aside" (it is in §2); "limits two
  lessons from now" (three); the opposite category described as still to
  come although Lesson 1 had defined it.
- **3 · Natural Transformations.** The determinant is natural with respect
  to homomorphisms of *commutative* rings; naturality of `flatten` is part
  of the definition of a monad rather than "one of the monad axioms".
- **4 · Universal Properties.** The discussion of global elements used a
  poset to show that arrows are not determined by them, which a thin
  category cannot show; the example is now **Grp**, where every object has
  exactly one global element. "Triangle identities" was used for two
  commuting triangles unrelated to adjunctions.
- **5 · Limits & Colimits.** Adjunctions were called "the concept the
  subject was built for", contradicting Lesson 3 and the history (natural
  transformations, 1945; adjunctions, 1958). "**Set** has all small limits"
  was attributed to binary products and equalizers; it needs products of
  arbitrary families, and the full statement is now proved. The pasting
  lemma's two directions were mislabelled (Exercise 10 proves the easier
  one; the other is now Exercise 16).
- **6 · Adjunctions.** The lede called adjunctions "the concept category
  theory was invented to state". §2 pointed to a "square formulation in
  Exercise 4" that did not exist; naturality is now spelled out in §2 and
  completed in Exercise 12. The forgetful functor attributed to Lesson 2 was
  not the one Lesson 2 used. The failing example was described as crushing
  "the bottom element" (it is a constant map); "a sandwich with Δ as the
  bread" (Δ is in the middle); a "six-element universe" with seven elements.
- **7 · Yoneda & Monads.**
  - Exercise 11's solution said that with a non-associative evaluator "the
    second assert fails". The first one fails already (`a([5]) = -5`); and
    the suggested swap to `"".join` could not run on the integer test data.
  - "The Eilenberg–Moore category, one of the two canonical adjunctions": a
    category is not an adjunction; and Exercise 5 deferred Kleisli and
    Eilenberg–Moore to "the next course" although the lesson introduced
    both. Both constructions are now treated in full.
  - Exercise 9(b)'s hand computation followed the other bracketing from the
    one asked for; "seven lessons later" was six; JavaScript promise
    chaining was given as an instance of bind with no caveat (promises
    flatten themselves, so the laws do not hold in every case); the Kleisli
    diagram's label put its subscript on the wrong symbol.

Code and claims.

- 7 of the 33 code boxes could not run from the page that showed them: they
  used names defined only in the downloadable script. Every page now carries
  a setup block, and all 56 boxes run from the page alone.
- The README said that every output block was the verbatim output of the
  code in `code/` and `notebooks/`. The scripts printed differently worded
  lines, and only about half of the pages' output lines appeared in them.
  The scripts and notebooks are now generated from the pages, so the claim
  is true by construction, and `tools/check_course.py` enforces it.
- Leftover revision markers ("· new" on 23 exercise labels, "Lesson 2's new
  Exercise 11") were removed, and two diagrams with overlapping labels were
  tidied.

### Tooling

- `tools/sync_code.py` regenerates `code/` and `notebooks/` from the lesson
  pages, which are now the single source of truth for the code.
- `tools/check_course.py` runs every code box and compares its output with
  the page, verifies the generated files, checks links, anchors, diagram
  definitions and exercise numbering, and confirms that every code box sits
  inside an optional lab or an optional exercise part.

## First edition

The original seven-lesson course.
