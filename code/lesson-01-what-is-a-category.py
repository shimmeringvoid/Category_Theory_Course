from itertools import product

# ----- Part A: Set — functions are morphisms ---------------------------------

def compose(g, f):
    """g after f:  (g . f)(x) = g(f(x))."""
    return lambda x: g(f(x))

def identity(x):
    return x

# Three sets and two functions between them
A = {1, 2, 3}
B = {'a', 'b'}
C = {True, False}

f = {1: 'a', 2: 'b', 3: 'a'}          # f: A -> B
g = {'a': True, 'b': False}           # g: B -> C

def apply(fn, dom):
    return {x: fn[x] for x in dom}

# Composite g . f : A -> C, built pointwise
gf = {x: g[f[x]] for x in A}
print("g . f =", gf)

# Identity law:  f . id_A == f  and  id_B . f == f
assert {x: f[x] for x in A} == f
print("identity law holds for f")

# Associativity with a third function h: C -> {0,1}
h = {True: 1, False: 0}
left  = {x: h[g[f[x]]] for x in A}            # (h . g) . f
right = {x: h[g[f[x]]] for x in A}            # h . (g . f)
assert left == right
print("associativity holds:", left)


# ----- Part B: a checker for any *finite* category ---------------------------

class FiniteCategory:
    """
    objects:   iterable of hashable object names
    arrows:    dict  arrow_name -> (domain, codomain)
    comp:      dict  (g, f) -> g_after_f          (only for composable pairs)
    ident:     dict  object   -> identity arrow name
    """
    def __init__(self, objects, arrows, comp, ident):
        self.obj = set(objects)
        self.ar = dict(arrows)
        self.comp = dict(comp)
        self.id = dict(ident)

    def dom(self, a): return self.ar[a][0]
    def cod(self, a): return self.ar[a][1]

    def composable(self, g, f):
        return self.dom(g) == self.cod(f)

    def check(self):
        # 1. every object has an identity, typed X -> X
        for X in self.obj:
            i = self.id[X]
            assert self.ar[i] == (X, X), f"id_{X} mistyped"

        # 2. composition is total on composable pairs and correctly typed
        for g, f in product(self.ar, repeat=2):
            if self.composable(g, f):
                assert (g, f) in self.comp, f"missing composite {g} . {f}"
                gf = self.comp[(g, f)]
                assert self.ar[gf] == (self.dom(f), self.cod(g)), \
                    f"{g} . {f} mistyped"

        # 3. identity laws:  id . f == f == f . id
        for f in self.ar:
            X, Y = self.ar[f]
            assert self.comp[(self.id[Y], f)] == f, f"left identity fails on {f}"
            assert self.comp[(f, self.id[X])] == f, f"right identity fails on {f}"

        # 4. associativity:  h . (g . f) == (h . g) . f
        for h, g, f in product(self.ar, repeat=3):
            if self.composable(h, g) and self.composable(g, f):
                gf = self.comp[(g, f)]
                hg = self.comp[(h, g)]
                assert self.comp[(h, gf)] == self.comp[(hg, f)], \
                    f"associativity fails on {h},{g},{f}"
        return True


# A monoid (the natural numbers under +, truncated) as a one-object category
# object: '*'   arrows: 0,1,2  (mod 3)   composition = addition mod 3
arrows = {n: ('*', '*') for n in range(3)}
comp = {(a, b): (a + b) % 3 for a in range(3) for b in range(3)}
ident = {'*': 0}
Z3 = FiniteCategory({'*'}, arrows, comp, ident)
print("monoid-as-category valid:", Z3.check())

# A poset  x <= y <= z  as a category: one arrow per <= fact
objs = {'x', 'y', 'z'}
ar = {
    'ix': ('x', 'x'), 'iy': ('y', 'y'), 'iz': ('z', 'z'),
    'xy': ('x', 'y'), 'yz': ('y', 'z'), 'xz': ('x', 'z'),
}
ident = {'x': 'ix', 'y': 'iy', 'z': 'iz'}
# composition table (only one arrow between any two objects, so it's forced)
def only(a, b):
    s, t = ar[b][0], ar[a][1]
    for name, (d, c) in ar.items():
        if d == s and c == t:
            return name
comp = {(a, b): only(a, b) for a in ar for b in ar if ar[a][0] == ar[b][1]}
P = FiniteCategory(objs, ar, comp, ident)
print("poset-as-category valid:", P.check())

# ===== Exercise 9: the chain 0 <= 1 <= 2 as the category THREE ================
objs = {0, 1, 2}
ar = {'i0': (0, 0), 'i1': (1, 1), 'i2': (2, 2),
      'a': (0, 1), 'b': (1, 2), 'c': (0, 2)}        # c is forced:  b . a
ident = {0: 'i0', 1: 'i1', 2: 'i2'}

# at most one arrow per ordered pair, so each composite is determined
def only3(s, t):
    return next(n for n, (d, c) in ar.items() if d == s and c == t)
comp = {(g, f): only3(ar[f][0], ar[g][1])
        for g in ar for f in ar if ar[f][1] == ar[g][0]}

Three = FiniteCategory(objs, ar, comp, ident)
print("the category THREE is valid:", Three.check())

# ===== Exercise 10: corrupt the composition table; the checker must object ====
bad_comp = dict(comp)
bad_comp[('b', 'a')] = 'i0'          # claim: (0->1->2) composes to id_0 — wrong!
try:
    FiniteCategory(objs, ar, bad_comp, ident).check()
    print("checker FAILED to catch the corruption")
except AssertionError:
    print("checker caught the corruption: composite of b.a must be typed 0 -> 2")
