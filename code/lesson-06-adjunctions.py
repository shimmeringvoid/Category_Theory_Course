import math
from itertools import product as cartesian

# ---- carried over from Lessons 1-5 -------------------------------------------
class FiniteCategory:
    def __init__(self, objects, arrows, comp, ident):
        self.obj, self.ar, self.comp, self.id = set(objects), arrows, comp, ident

def arrows_between(C, X, Y):
    return [a for a, (d, c) in C.ar.items() if d == X and c == Y]

def make_poset(objs, leq):
    ar = {f"{a}<={b}": (a, b) for a in objs for b in objs if leq(a, b)}
    comp = {}
    for g, (gs, gt) in ar.items():
        for f, (fs, ft) in ar.items():
            if ft == gs:
                comp[(g, f)] = f"{fs}<={gt}"
    return FiniteCategory(objs, ar, comp, {n: f"{n}<={n}" for n in objs})

Div   = make_poset({1, 2, 3, 6}, lambda a, b: b % a == 0)   # divisibility
Chain = make_poset({0, 1, 2},    lambda a, b: a <= b)        # ordinary order

# ---- Part A: a Galois connection everyone already knows -----------------------
reals = [i / 7 for i in range(-30, 31)]
ints  = range(-6, 7)
checks = 0
for r in reals:
    for n in ints:
        assert (math.ceil(r) <= n) == (r <= n)      # ceiling  -|  inclusion
        assert (n <= math.floor(r)) == (n <= r)     # inclusion -| floor
        checks += 2
print(f"ceiling -| inclusion -| floor: verified on {checks} instances")

# ---- Part B: the free monoid adjunction, executable ---------------------------
def fold_map(f, unit, op):
    "the unique monoid hom  List X -> M  extending  f : X -> M"
    def hat(xs):
        acc = unit
        for x in xs:
            acc = op(acc, f(x))
        return acc
    return hat

f   = {'a': 2, 'b': 3}.get
hat = fold_map(f, 0, lambda m, n: m + n)          # target monoid (Z, +, 0)

import itertools
samples = [list(t) for k in range(4) for t in itertools.product('ab', repeat=k)]
assert hat([]) == 0                                # unit goes to unit
assert all(hat(xs + ys) == hat(xs) + hat(ys)       # concat goes to +
           for xs in samples for ys in samples)
assert all(hat([x]) == f(x) for x in 'ab')         # hat . eta == f
print("fold_map is a monoid hom; hat.eta == f; hat(['a','b','a']) =", hat(['a','b','a']))

# ---- Part C: an adjoint finder for finite posets ------------------------------
def monotone_maps(C, D):
    "all monotone maps C -> D between finite posets"
    Cobjs = sorted(C.obj, key=str)
    for values in cartesian(sorted(D.obj, key=str), repeat=len(Cobjs)):
        g = dict(zip(Cobjs, values))
        if all(not arrows_between(C, x, y) or arrows_between(D, g[x], g[y])
               for x in C.obj for y in C.obj):
            yield g

def find_right_adjoints(f, C, D):
    "all monotone g : D -> C with   f(x) <= y   iff   x <= g(y)"
    return [g for g in monotone_maps(D, C)
            if all(bool(arrows_between(D, f[x], y)) == bool(arrows_between(C, x, g[y]))
                   for x in C.obj for y in D.obj)]

f = {0: 1, 1: 2, 2: 6}                    # Chain -> Div, monotone
print("right adjoints of f    :", find_right_adjoints(f, Chain, Div))

f_bad = {1: 1, 2: 1, 3: 1, 6: 1}          # Div -> Chain, constant at 1
print("right adjoints of f_bad:", find_right_adjoints(f_bad, Div, Chain))

# ---- Exercise 8: currying is a bijection, counted exhaustively ----------------
X, A, Y = range(2), range(2), range(3)
pairs = [(x, a) for x in X for a in A]
hs = [dict(zip(pairs, vs)) for vs in cartesian(Y, repeat=len(pairs))]
curry = lambda h: tuple(tuple(h[(x, a)] for a in A) for x in X)
images = {curry(h) for h in hs}
print("|Hom(XxA,Y)| =", len(hs), " distinct curried =", len(images),
      " (|Y|^|A|)^|X| =", (len(Y) ** len(A)) ** len(X))

# ---- Exercise 9: the dual finder recovers f from g ----------------------------
def find_left_adjoints(g, D, C):
    "all monotone f : C -> D with   f(x) <= y   iff   x <= g(y)"
    return [f for f in monotone_maps(C, D)
            if all(bool(arrows_between(D, f[x], y)) == bool(arrows_between(C, x, g[y]))
                   for x in C.obj for y in D.obj)]

g = {1: 0, 2: 1, 3: 0, 6: 2}
print("left adjoints of g     :", find_left_adjoints(g, Div, Chain))

# ===== Exercise 10: quantifiers are adjoints —  ∃f ⊣ f* ⊣ ∀f ==================
from itertools import combinations

A = {1, 2, 3}; B = {'a', 'b'}
fpt = {1: 'a', 2: 'a', 3: 'b'}
fq = lambda x: fpt[x]

def subsets(S):
    S = list(S)
    return [set(c) for r in range(len(S)+1) for c in combinations(S, r)]

Eim = lambda S: {fq(x) for x in S}                     # ∃f : direct image
pre = lambda T: {x for x in A if fq(x) in T}           # f* : preimage
All = lambda S: {b for b in B                          # ∀f
                 if all(x in S for x in A if fq(x) == b)}

n = 0
for S in subsets(A):
    for T in subsets(B):
        assert (Eim(S) <= T) == (S <= pre(T))     # ∃f  -|  f*
        assert (pre(T) <= S) == (T <= All(S))     # f*  -|  ∀f
        n += 2
print(f"quantifier sandwich verified on {n} biconditionals")
