from itertools import product as cartesian

# ================= Part A: Yoneda in a poset — an element IS its down-set ======
# In the divisibility poset, the presheaf Hom(-, a) is the down-set of a:
# the set of everything with an arrow into a, i.e. the divisors of a.
objs = {1, 2, 3, 6}
downset = {a: {x for x in objs if a % x == 0} for a in objs}

pairs = 0
for a in objs:
    for b in objs:
        assert (b % a == 0) == (downset[a] <= downset[b])   # a|b iff ds(a) ⊆ ds(b)
        pairs += 1
print(f"Yoneda in Div: a|b <=> downset(a) subset-of downset(b) — {pairs} pairs checked")
for a in sorted(objs):
    print(f"  downset({a}) = {sorted(downset[a])}")

# ================= Part B: Yoneda counted — Nat(y*, y*) in Z3 ==================
# One object *, Hom(*,*) = {0,1,2}, composition = addition mod 3.
# A natural family y* => y* is one function alpha : Hom -> Hom with
#     alpha(f . g) = alpha(f) . g      for all f, g       (naturality)
H = [0, 1, 2]
comp = lambda a, b: (a + b) % 3          # a . b

nats = []
for vals in cartesian(H, repeat=3):
    alpha = dict(zip(H, vals))
    if all(alpha[comp(f, g)] == comp(alpha[f], g) for f in H for g in H):
        nats.append(alpha)

print(f"natural transformations y* => y* : {len(nats)}   |Hom(*,*)| = {len(H)}")
for a in nats:
    assert all(a[f] == comp(a[0], f) for f in H)   # each is postcomposition
    print(f"  {a}  =  postcompose by {a[0]}")

# ================= Part C: the List monad, laws checked wholesale ==============
eta  = lambda x: [x]
mu   = lambda xss: [x for xs in xss for x in xs]        # Lesson 3's flatten
fmap = lambda f, xs: [f(x) for x in xs]

def lists_over(base, maxlen=2):
    out = [[]]
    for k in range(1, maxlen + 1):
        out += [list(t) for t in cartesian(base, repeat=k)]
    return out

T1 = lists_over([0, 1])          # lists
T2 = lists_over(T1)              # lists of lists
T3 = lists_over(T2)              # lists of lists of lists

assert all(mu(mu(x3)) == mu(fmap(mu, x3)) for x3 in T3)          # associativity
assert all(mu(eta(xs)) == xs == mu(fmap(eta, xs)) for xs in T1)  # unit laws
print(f"List monad: associativity on {len(T3)} T^3 values, units on {len(T1)} — all pass")

# ================= Part D: the Maybe monad, laws checked exhaustively ==========
J     = lambda x: ('Just', x)                       # eta
fmapM = lambda f, m: None if m is None else J(f(m[1]))
muM   = lambda mm: None if mm is None else mm[1]    # collapse one layer

M1 = [None] + [J(x) for x in (0, 1)]
M2 = [None] + [J(m) for m in M1]
M3 = [None] + [J(m) for m in M2]

assert all(muM(muM(m3)) == muM(fmapM(muM, m3)) for m3 in M3)
assert all(muM(J(m)) == m == muM(fmapM(J, m)) for m in M1)
print(f"Maybe monad: associativity on {len(M3)} T^3 values, units on {len(M1)} — all pass")

# ================= Exercise 8: the Writer monad (needs a monoid!) ==============
etaW  = lambda x: (x, "")
fmapW = lambda f, p: (f(p[0]), p[1])
def muW(pp):
    (x, inner), outer = pp
    return (x, outer + inner)

logs = ["", "a", "bc"]
W1 = [(x, w) for x in (0, 1) for w in logs]
W2 = [(p, w) for p in W1 for w in logs]
W3 = [(q, w) for q in W2 for w in logs]

assert all(muW(muW(q3)) == muW(fmapW(muW, q3)) for q3 in W3)
assert all(muW(etaW(p)) == p == muW(fmapW(etaW, p)) for p in W1)
print(f"Writer monad: associativity on {len(W3)} values, units on {len(W1)} — all pass")

# ================= Exercise 9: Kleisli composition for List ====================
kleisli = lambda g, f: (lambda x: mu(fmap(g, f(x))))
f = lambda x: [x, x + 1]
g = lambda x: [x * 2]
h = lambda x: [x, -x]

assert all(kleisli(kleisli(h, g), f)(x) == kleisli(h, kleisli(g, f))(x)
           for x in range(-5, 6))
assert all(kleisli(f, eta)(x) == f(x) == kleisli(eta, f)(x) for x in range(-5, 6))
print("Kleisli for List: associativity and identity laws — all pass")
print("  (h .K g) .K f  at 2 :", kleisli(kleisli(h, g), f)(2))

# ===== Exercise 11: sum is a List-algebra — the monoid laws, enforced =========
alg = sum                        # a : List Z -> Z,  with a([]) == 0

assert all(alg(eta(x)) == x for x in (0, 1, 5, -3))          # a . eta = id
T2i = lists_over(lists_over([0, 1]))
assert all(alg(mu(xss)) == alg(fmap(alg, xss)) for xss in T2i)  # a . mu = a . Ta
print(f"sum is a List-algebra: laws pass on {len(T2i)} T\u00b2 values")
