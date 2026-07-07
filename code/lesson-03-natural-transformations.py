from itertools import product

# ---- carried over from Lessons 1 & 2 ---------------------------------------
class FiniteCategory:
    def __init__(self, objects, arrows, comp, ident):
        self.obj, self.ar, self.comp, self.id = set(objects), arrows, comp, ident
    def dom(self, a): return self.ar[a][0]
    def cod(self, a): return self.ar[a][1]
    def composable(self, g, f): return self.dom(g) == self.cod(f)

class Functor:
    def __init__(self, C, D, on_obj, on_arr):
        self.C, self.D, self.on_obj, self.on_arr = C, D, on_obj, on_arr

# ---- Part A: polymorphic functions are natural transformations -------------

def fmap(f, xs):                 # the List functor on arrows
    return [f(x) for x in xs]

def reverse(xs):                 # component of  reverse : List => List
    return xs[::-1]

inc = lambda x: x + 1
data = [1, 2, 3, 4]

# Naturality of `reverse`:  map f . reverse  ==  reverse . map f
assert fmap(inc, reverse(data)) == reverse(fmap(inc, data))
print(fmap(inc, reverse(data)))                  # [5, 4, 3, 2]

# `safe_head` : List => Maybe   (Maybe modelled as a 1-or-0 element list)
def safe_head(xs):
    return [xs[0]] if xs else []
def fmap_maybe(f, m):
    return [f(x) for x in m]

# Naturality of `safe_head`:  fmap_maybe f . safe_head == safe_head . map f
for xs in ([], [10, 20, 30]):
    assert fmap_maybe(inc, safe_head(xs)) == safe_head(fmap(inc, xs))
print("reverse and safe_head are natural")


# ---- Part B: a naturality checker for finite functors ----------------------

class Nat:
    """alpha : F => G, with F, G : C -> D sharing source and target.
       `comp` maps each object X of C to a component arrow alpha_X of D."""
    def __init__(self, F, G, comp):
        self.F, self.G, self.comp = F, G, comp

    def check(self):
        F, G, C, D = self.F, self.G, self.F.C, self.F.D
        # 1. each component is typed  alpha_X : F X -> G X
        for X in C.obj:
            assert D.ar[self.comp[X]] == (F.on_obj[X], G.on_obj[X])
        # 2. naturality square:  for every f: X -> Y,  G f . alpha_X == alpha_Y . F f
        for f in C.ar:
            X, Y = C.ar[f]
            assert D.comp[(G.on_arr[f], self.comp[X])] == \
                   D.comp[(self.comp[Y], F.on_arr[f])], f"naturality fails at {f}"
        return True

# Target D: the commuting-square category  A --f--> B,  A --p--> C,
#                                          B --q--> D,  C --g--> D,  d = q.f = g.p
arr = {'iA':('A','A'),'iB':('B','B'),'iC':('C','C'),'iD':('D','D'),
       'f':('A','B'),'p':('A','C'),'q':('B','D'),'g':('C','D'),'d':('A','D')}
ident = {'A':'iA','B':'iB','C':'iC','D':'iD'}
comp = {}
for x,(u,v) in arr.items():
    comp[(ident[v], x)] = x          # id . x = x
    comp[(x, ident[u])] = x          # x . id = x
comp[('q','f')] = 'd'                # q . f = d
comp[('g','p')] = 'd'                # g . p = d
Square = FiniteCategory(set('ABCD'), arr, comp, ident)

# Source 2 = ( 0 --u--> 1 )
two_ar   = {'i0':(0,0),'i1':(1,1),'u':(0,1)}
two_comp = {('i0','i0'):'i0',('i1','i1'):'i1',('u','i0'):'u',('i1','u'):'u'}
Two = FiniteCategory({0,1}, two_ar, two_comp, {0:'i0',1:'i1'})

# Two functors 2 -> Square: F picks the edge f (A->B), G picks the edge g (C->D)
F = Functor(Two, Square, {0:'A',1:'B'}, {'i0':'iA','i1':'iB','u':'f'})
G = Functor(Two, Square, {0:'C',1:'D'}, {'i0':'iC','i1':'iD','u':'g'})

# A natural transformation F => G is exactly a commuting square: components p, q
alpha = Nat(F, G, comp={0:'p', 1:'q'})
print("alpha : F => G is natural:", alpha.check())

# ===== Exercise 6: a mistyped component is rejected before naturality =========
bad = Nat(F, G, comp={0: 'p', 1: 'f'})     # 'f' is typed A->B, not B->D
try:
    bad.check()
    print("checker FAILED to catch the mistyped component")
except AssertionError:
    print("rejected: component at 1 is mistyped")

# ===== Exercise 7: flatten is natural  List.List => List ======================
flatten = lambda xss: [x for xs in xss for x in xs]
xss = [[1, 2], [3]]
tenfold = lambda x: x * 10
assert fmap(tenfold, flatten(xss)) == flatten(fmap(lambda xs: fmap(tenfold, xs), xss))
print("flatten is natural: map f . flatten == flatten . map (map f)")

# ===== Exercise 9: duplicate is natural; sorted is NOT ========================
dup = lambda xs: [x for x in xs for _ in (0, 1)]
neg = lambda x: -x
assert fmap(neg, dup([1, 2])) == dup(fmap(neg, [1, 2]))     # natural

lhs = fmap(neg, sorted([1, 2]))     # [-1, -2]
rhs = sorted(fmap(neg, [1, 2]))     # [-2, -1]
print(lhs, rhs, lhs == rhs)         # sorted inspects elements -> not natural

# ===== Exercise 11: take2 is natural; dedupe is NOT ===========================
take2  = lambda xs: xs[:2]
dedupe = lambda xs: list(dict.fromkeys(xs))
const0 = lambda x: 0

for f_ in (str, lambda x: -x):
    for xs in ([], [1], [3, 1, 2], [5, 5, 1]):
        assert fmap(f_, take2(xs)) == take2(fmap(f_, xs))   # natural
print("take2 is natural")

lhs = fmap(const0, dedupe([1, 2]))    # dedupe sees 1 != 2 ...
rhs = dedupe(fmap(const0, [1, 2]))    # ... but const0 merges them first
print(lhs, rhs, lhs == rhs)           # equality-testing breaks naturality
