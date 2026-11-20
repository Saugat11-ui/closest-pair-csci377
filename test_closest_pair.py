"""Correctness check: divide-and-conquer vs brute force."""
import math
import random
from closest_pair import closest_pair, brute_force

random.seed(377)
fails = 0
total = 0


def check(points, label):
    global fails, total
    total += 1
    d_dc, a, b = closest_pair(points)
    d_bf, _, _ = brute_force(points)
    # the returned pair must be two input points (distinct entries) at distance d_dc
    # distances must agree AND the returned pair must be real input points at that distance
    dx, dy = a[0] - b[0], a[1] - b[1]
    sq = dx * dx + dy * dy
    ok = (d_dc == d_bf) and sq == d_dc and a in points and b in points
    if not ok:
        fails += 1
        print("MISMATCH", label, d_dc, d_bf, points[:10])
    return ok


# --- named edge cases -------------------------------------------------
edge = {
    "n=2": [(0, 0), (3, 4)],
    "n=3": [(0, 0), (10, 10), (1, 1)],
    "n=4": [(0, 0), (10, 10), (1, 1), (50, 50)],
    "duplicate points (distance 0)": [(5, 5), (1, 1), (5, 5), (9, 2), (7, 7)],
    "all on one vertical line (same x)": [(4, y) for y in (10, 3, 7, 25, 18, 1, 40)],
    "all on one horizontal line (same y)": [(x, 6) for x in (10, 3, 7, 25, 18, 1, 40)],
    "all points identical": [(2, 2)] * 8,
    "closest pair straddles the dividing line": [(0, 0), (4, 9), (9, 0), (10, 0), (15, 9), (20, 0), (30, 5), (40, 1)],
    "points sharing the dividing x": [(5, 0), (5, 2), (5, 4), (5, 6), (1, 1), (9, 9), (5, 5)],
}
for name, pts in edge.items():
    ok = check(pts, name)
    d, a, b = closest_pair(pts)
    print(f"{'PASS' if ok else 'FAIL'}  {name:45s} d = {math.sqrt(d):.4f}  pair = {a} , {b}")

# --- random tests -----------------------------------------------------
# tiny coordinate range => many duplicates / same-x / same-y ties
configs = [(2, 6, 3), (3, 12, 5), (5, 40, 10), (10, 100, 30), (50, 300, 1000), (100, 1000, 10**6)]
count = 0
for n_lo, n_hi, rng in configs:
    for _ in range(300):
        n = random.randint(n_lo, n_hi)
        pts = [(random.randint(0, rng), random.randint(0, rng)) for _ in range(n)]
        check(pts, f"random n={n} range={rng}")
        count += 1
# float coordinates
for _ in range(200):
    n = random.randint(2, 200)
    pts = [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(n)]
    check(pts, "float")
    count += 1

print(f"\n{len(edge)} named edge cases + {count} random cases run; mismatches = {fails}")
