from itertools import product as cartesian

# ---- carried over from Lessons 1-3 ------------------------------------------
class FiniteCategory:
    def __init__(self, objects, arrows, comp, ident):
        self.obj, self.ar, self.comp, self.id = set(objects), arrows, comp, ident
    def dom(self, a): return self.ar[a][0]
    def cod(self, a): return self.ar[a][1]
    def composable(self, g, f): return self.dom(g) == self.cod(f)

def arrows_between(C, X, Y):
    return [a for a, (d, c) in C.ar.items() if d == X and c == Y]

# ---- Part A: universal-object finders ---------------------------------------

def terminal_objects(C):
    "T is terminal iff every object has EXACTLY ONE arrow into T."
    return [T for T in C.obj
            if all(len(arrows_between(C, X, T)) == 1 for X in C.obj)]

def initial_objects(C):
    "I is initial iff every object has EXACTLY ONE arrow out of I into it."
    return [I for I in C.obj
            if all(len(arrows_between(C, I, X)) == 1 for X in C.obj)]

def is_product(C, P, pA, pB):
    "Check the universal property of (P, pA: P->A, pB: P->B)."
    A, B = C.cod(pA), C.cod(pB)
    if C.dom(pA) != P or C.dom(pB) != P:
        return False
    for X in C.obj:
        for f in arrows_between(C, X, A):
            for g in arrows_between(C, X, B):
                mediators = [m for m in arrows_between(C, X, P)
                             if C.comp[(pA, m)] == f and C.comp[(pB, m)] == g]
                if len(mediators) != 1:          # exists AND is unique
                    return False
    return True

def find_products(C, A, B):
    hits = []
    for P in C.obj:
        for pA in arrows_between(C, P, A):
            for pB in arrows_between(C, P, B):
                if is_product(C, P, pA, pB):
                    hits.append((P, pA, pB))
    return hits

# ---- The divisibility poset on {1, 2, 3, 6} as a category -------------------
objs = {1, 2, 3, 6}
ar   = {f"{a}|{b}": (a, b) for a in objs for b in objs if b % a == 0}
comp = {}
for g, (gs, gt) in ar.items():
    for f, (fs, ft) in ar.items():
        if ft == gs:
            comp[(g, f)] = f"{fs}|{gt}"          # thin category: forced
ident = {n: f"{n}|{n}" for n in objs}
Div = FiniteCategory(objs, ar, comp, ident)

print("initial:", initial_objects(Div))          # [1]
print("terminal:", terminal_objects(Div))        # [6]
print("product of 2 and 3:", find_products(Div, 2, 3))   # gcd = 1
print("product of 2 and 6:", find_products(Div, 2, 6))   # gcd = 2
# coproducts are products in the OPPOSITE category = lcm here; check directly:
def find_coproducts(C, A, B):
    hits = []
    for P in C.obj:
        for iA in arrows_between(C, A, P):
            for iB in arrows_between(C, B, P):
                ok = True
                for X in C.obj:
                    for f in arrows_between(C, A, X):
                        for g in arrows_between(C, B, X):
                            med = [m for m in arrows_between(C, P, X)
                                   if C.comp[(m, iA)] == f and C.comp[(m, iB)] == g]
                            if len(med) != 1: ok = False
                if ok: hits.append((P, iA, iB))
    return hits
print("coproduct of 2 and 3:", find_coproducts(Div, 2, 3))  # lcm = 6

# ---- A category with NO products: the monoid (Z/3, +) -----------------------
zar  = {n: ('*', '*') for n in range(3)}
zcmp = {(a, b): (a + b) % 3 for a in range(3) for b in range(3)}
Z3   = FiniteCategory({'*'}, zar, zcmp, {'*': 0})
print("products in Z3:", find_products(Z3, '*', '*'))       # []

# ---- Part B: the product in Set, with its pairing map -----------------------
def pairing(f, g):
    "the unique mediating map <f, g> : X -> A x B"
    return lambda x: (f(x), g(x))

fst = lambda p: p[0]
snd = lambda p: p[1]

X = [0, 1, 2]
f = lambda x: x + 10          # f : X -> A
g = lambda x: x * x           # g : X -> B
m = pairing(f, g)

# the two triangles commute:  fst . <f,g> == f   and   snd . <f,g> == g
assert all(fst(m(x)) == f(x) for x in X)
assert all(snd(m(x)) == g(x) for x in X)
print("pairing triangles commute:", [m(x) for x in X])
