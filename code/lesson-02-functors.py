from itertools import product

# ---- carried over from Lesson 1 --------------------------------------------
class FiniteCategory:
    def __init__(self, objects, arrows, comp, ident):
        self.obj, self.ar, self.comp, self.id = set(objects), arrows, comp, ident
    def dom(self, a): return self.ar[a][0]
    def cod(self, a): return self.ar[a][1]
    def composable(self, g, f): return self.dom(g) == self.cod(f)

# ---- Part A: the List functor on the category of types ---------------------

def fmap(f, xs):
    "lift an ordinary function to act on a list, elementwise"
    return [f(x) for x in xs]

idf = lambda x: x
inc = lambda x: x + 1
sq  = lambda x: x * x
data = [1, 2, 3, 4]

# Functor law 1:  fmap(id) == id
assert fmap(idf, data) == data

# Functor law 2:  fmap(g . f) == fmap(g) . fmap(f)
assert fmap(lambda x: sq(inc(x)), data) == fmap(sq, fmap(inc, data))

print(fmap(inc, data))            # [2, 3, 4, 5]
print("List functor laws hold")


# ---- Part B: a Functor between finite categories ---------------------------

class Functor:
    """F : C -> D, given by a map on objects and a map on arrows."""
    def __init__(self, C, D, on_obj, on_arr):
        self.C, self.D, self.on_obj, self.on_arr = C, D, on_obj, on_arr

    def check(self):
        C, D, Fo, Fa = self.C, self.D, self.on_obj, self.on_arr
        # 1. typing:  F(f) : F(dom f) -> F(cod f)
        for f in C.ar:
            X, Y = C.ar[f]
            assert D.ar[Fa[f]] == (Fo[X], Fo[Y]), f"F mistypes {f}"
        # 2. preserves identities:  F(id_X) = id_{F X}
        for X in C.obj:
            assert Fa[C.id[X]] == D.id[Fo[X]], f"F breaks id at {X}"
        # 3. preserves composition:  F(g . f) = F(g) . F(f)
        for g, f in product(C.ar, repeat=2):
            if C.composable(g, f):
                assert Fa[C.comp[(g, f)]] == D.comp[(Fa[g], Fa[f])], \
                    f"F breaks composition on {g},{f}"
        return True

# The monoid (Z/3, +) as a one-object category  (from Lesson 1)
ar   = {n: ('*', '*') for n in range(3)}
comp = {(a, b): (a + b) % 3 for a in range(3) for b in range(3)}
Z3 = FiniteCategory({'*'}, ar, comp, {'*': 0})

# "multiply by 2" is a monoid homomorphism Z/3 -> Z/3 ...
# ... and a monoid homomorphism is EXACTLY a functor of one-object categories
double = Functor(Z3, Z3, on_obj={'*': '*'}, on_arr={n: (2 * n) % 3 for n in range(3)})
print("multiply-by-2 is a functor:", double.check())

# A functor out of the category 2 = (0 -> 1) is exactly a choice of arrow.
two_ar = {'i0': (0, 0), 'i1': (1, 1), 'u': (0, 1)}
two_comp = {('i0','i0'):'i0', ('i1','i1'):'i1',
            ('u','i0'):'u', ('i1','u'):'u'}
Two = FiniteCategory({0, 1}, two_ar, two_comp, {0: 'i0', 1: 'i1'})
# pick the arrow '1' of Z3 as the image of u; identities are forced
pick = Functor(Two, Z3, on_obj={0: '*', 1: '*'},
               on_arr={'i0': 0, 'i1': 0, 'u': 1})
print("a functor 2 -> Z3 is a choice of arrow:", pick.check())

# ===== Exercise 9: all three functors 2 -> Z3, one per arrow of Z3 ============
for pick_arrow in (0, 1, 2):
    F = Functor(Two, Z3, on_obj={0: '*', 1: '*'},
                on_arr={'i0': 0, 'i1': 0, 'u': pick_arrow})
    print(pick_arrow, F.check())

# ===== Exercise 10: n |-> n+1 breaks BOTH functor laws ========================
shift = Functor(Z3, Z3, on_obj={'*': '*'},
                on_arr={n: (n + 1) % 3 for n in range(3)})
try:
    shift.check()
    print("checker FAILED to catch the broken functor")
except AssertionError:
    print("checker caught it: n |-> n+1 does not preserve the identity (0 |-> 1)")

# ===== Exercise 12: the covariant powerset functor, laws by brute force =======
from itertools import combinations

def pmap(f, S):                       # direct image on subsets
    return {f(x) for x in S}

def subsets(S):
    S = list(S)
    return [set(c) for r in range(len(S)+1) for c in combinations(S, r)]

h1 = lambda x: x % 2
h2 = lambda x: x + 1
for S in subsets({1, 2, 3}):
    assert pmap(lambda x: x, S) == S
    assert pmap(h1, pmap(h2, S)) == pmap(lambda x: h1(h2(x)), S)
print("powerset functor laws: 16 instances pass")
