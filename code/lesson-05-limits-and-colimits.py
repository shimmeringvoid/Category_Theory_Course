from itertools import product as cartesian

# ---- carried over from Lessons 1-4 ------------------------------------------
class FiniteCategory:
    def __init__(self, objects, arrows, comp, ident):
        self.obj, self.ar, self.comp, self.id = set(objects), arrows, comp, ident
    def dom(self, a): return self.ar[a][0]
    def cod(self, a): return self.ar[a][1]

class Functor:
    def __init__(self, C, D, on_obj, on_arr):
        self.C, self.D, self.on_obj, self.on_arr = C, D, on_obj, on_arr

def arrows_between(C, X, Y):
    return [a for a, (d, c) in C.ar.items() if d == X and c == Y]

# ---- Part A: the general limit finder ----------------------------------------

def cones(C, D):
    "All cones over the diagram D : J -> C, as (apex, legs) pairs."
    J, out = D.C, []
    Jobjs = sorted(J.obj, key=str)
    for X in C.obj:
        legsets = [arrows_between(C, X, D.on_obj[j]) for j in Jobjs]
        for combo in cartesian(*legsets):
            legs = dict(zip(Jobjs, combo))
            # every triangle commutes:  D(a) . leg_i == leg_j   for a : i -> j
            if all(C.comp[(D.on_arr[a], legs[i])] == legs[j]
                   for a, (i, j) in J.ar.items()):
                out.append((X, legs))
    return out

def find_limits(C, D):
    "Limit = the cone through which every cone factors in exactly one way."
    cs = cones(C, D)
    hits = []
    for apex, legs in cs:
        if all(len([m for m in arrows_between(C, X, apex)
                    if all(C.comp[(legs[j], m)] == l[j] for j in legs)]) == 1
               for X, l in cs):
            hits.append((apex, legs))
    return hits

def cocones(C, D):
    J, out = D.C, []
    Jobjs = sorted(J.obj, key=str)
    for X in C.obj:
        legsets = [arrows_between(C, D.on_obj[j], X) for j in Jobjs]
        for combo in cartesian(*legsets):
            legs = dict(zip(Jobjs, combo))
            if all(C.comp[(legs[j], D.on_arr[a])] == legs[i]
                   for a, (i, j) in J.ar.items()):
                out.append((X, legs))
    return out

def find_colimits(C, D):
    cs = cocones(C, D)
    hits = []
    for apex, legs in cs:
        if all(len([m for m in arrows_between(C, apex, X)
                    if all(C.comp[(m, legs[j])] == l[j] for j in legs)]) == 1
               for X, l in cs):
            hits.append((apex, legs))
    return hits

# ---- the divisibility poset on {1,2,3,6}, as in Lesson 4 ---------------------
objs = {1, 2, 3, 6}
ar   = {f"{a}|{b}": (a, b) for a in objs for b in objs if b % a == 0}
comp = {}
for g, (gs, gt) in ar.items():
    for f, (fs, ft) in ar.items():
        if ft == gs:
            comp[(g, f)] = f"{fs}|{gt}"
ident = {n: f"{n}|{n}" for n in objs}
Div = FiniteCategory(objs, ar, comp, ident)

# ---- three index categories (shapes) ------------------------------------------
Empty = FiniteCategory(set(), {}, {}, {})

Disc2 = FiniteCategory({0, 1}, {'i0':(0,0), 'i1':(1,1)},
                       {('i0','i0'):'i0', ('i1','i1'):'i1'},
                       {0:'i0', 1:'i1'})

cos_ar = {'i0':(0,0),'i1':(1,1),'i2':(2,2),'u':(0,2),'v':(1,2)}
cos_comp = {('i0','i0'):'i0',('i1','i1'):'i1',('i2','i2'):'i2',
            ('u','i0'):'u',('i2','u'):'u',('v','i1'):'v',('i2','v'):'v'}
Cospan = FiniteCategory({0,1,2}, cos_ar, cos_comp, {0:'i0',1:'i1',2:'i2'})

# ---- diagrams of those shapes in Div ------------------------------------------
D_empty  = Functor(Empty,  Div, {}, {})
D_23     = Functor(Disc2,  Div, {0:2, 1:3}, {'i0':'2|2', 'i1':'3|3'})
D_cospan = Functor(Cospan, Div, {0:2, 1:3, 2:6},
                   {'i0':'2|2','i1':'3|3','i2':'6|6','u':'2|6','v':'3|6'})

print("limit of empty diagram :", find_limits(Div, D_empty))
print("limit of {2, 3}        :", find_limits(Div, D_23))
print("limit of 2 -> 6 <- 3   :", find_limits(Div, D_cospan))
print("colimit of {2, 3}      :", find_colimits(Div, D_23))

# ---- Part B: equalizers and pullbacks in Set -----------------------------------

# equalizer of f, g : X -> Y  =  the solution set of the equation f(x) = g(x)
X = range(-3, 4)
f = lambda x: x * x
g = lambda x: x + 2
E = [x for x in X if f(x) == g(x)]
print("equalizer of x\u00b2 and x+2 on [-3..3]:", E)

# pullback of  dept : Emp -> Key  and  key : Bldg -> Key   =  a database join
employees = [("Alice", "eng"), ("Bob", "sales"), ("Carol", "eng")]
buildings = [("eng", "Building 1"), ("sales", "Building 2")]
dept = lambda e: e[1]
key  = lambda b: b[0]

P  = [(e, b) for e in employees for b in buildings if dept(e) == key(b)]
p1 = lambda x: x[0]
p2 = lambda x: x[1]

for e, b in P:
    print(f"{e[0]} works in {b[1]}")
# the pullback square commutes:  dept . p1 == key . p2  on P
print("square commutes:", all(dept(p1(x)) == key(p2(x)) for x in P))

# ---- Exercise 9: the span shape, and a machine-checked pushout ----------------
sp_ar   = {'i0':(0,0),'i1':(1,1),'i2':(2,2),'u':(1,0),'v':(1,2)}
sp_comp = {('i0','i0'):'i0',('i1','i1'):'i1',('i2','i2'):'i2',
           ('u','i1'):'u',('i0','u'):'u',('v','i1'):'v',('i2','v'):'v'}
Span = FiniteCategory({0,1,2}, sp_ar, sp_comp, {0:'i0',1:'i1',2:'i2'})

D_span = Functor(Span, Div, {0:2, 1:1, 2:3},
                 {'i0':'2|2','i1':'1|1','i2':'3|3','u':'1|2','v':'1|3'})

print("limit of 2 <- 1 -> 3   :", find_limits(Div, D_span))
print("colimit (pushout!)     :", find_colimits(Div, D_span))

# ===== Exercise 11: the fork — a genuine (non-thin) equalizer, found ==========
fk_ar = {'iE':('E','E'),'iA':('A','A'),'iB':('B','B'),
         'e':('E','A'),'f':('A','B'),'g':('A','B'),'w':('E','B')}
fk_ident = {'E':'iE','A':'iA','B':'iB'}
fk_comp = {}
for x, (u, v) in fk_ar.items():
    fk_comp[(fk_ident[v], x)] = x
    fk_comp[(x, fk_ident[u])] = x
fk_comp[('f','e')] = 'w'
fk_comp[('g','e')] = 'w'              # both composites land on w
Fork = FiniteCategory({'E','A','B'}, fk_ar, fk_comp, fk_ident)

pp_ar = {'i0':(0,0),'i1':(1,1),'u':(0,1),'v':(0,1)}     # parallel-pair shape
pp_comp = {('i0','i0'):'i0',('i1','i1'):'i1',
           ('u','i0'):'u',('i1','u'):'u',('v','i0'):'v',('i1','v'):'v'}
Pair = FiniteCategory({0,1}, pp_ar, pp_comp, {0:'i0',1:'i1'})

D_fg = Functor(Pair, Fork, {0:'A',1:'B'}, {'i0':'iA','i1':'iB','u':'f','v':'g'})
print("equalizer in the fork  :", find_limits(Fork, D_fg))
