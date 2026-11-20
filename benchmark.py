"""First timing results: divide-and-conquer vs brute force."""
import math, random, sys, time
from closest_pair import closest_pair, brute_force

sys.setrecursionlimit(10000)
random.seed(377)


def make(n):
    return [(random.uniform(0, 10**6), random.uniform(0, 10**6)) for _ in range(n)]


def best_of(f, pts, reps):
    best = float("inf")
    for _ in range(reps):
        t = time.perf_counter(); r = f(pts); best = min(best, time.perf_counter() - t)
    return best, r


print(f"{'n':>8} {'D&C (s)':>10} {'brute (s)':>10} {'same d?':>8} {'D&C/(n log2 n) x1e6':>20}")
for n, reps_dc, reps_bf in ((100, 20, 20), (1000, 5, 3), (10000, 3, 1)):
    pts = make(n)
    t_dc, r_dc = best_of(closest_pair, pts, reps_dc)
    t_bf, r_bf = best_of(brute_force, pts, reps_bf)
    print(f"{n:>8} {t_dc:>10.4f} {t_bf:>10.4f} {str(r_dc[0]==r_bf[0]):>8} {t_dc/(n*math.log2(n))*1e6:>20.3f}")

# scaling check, D&C only (brute force skipped: ~5 billion pair checks at n = 100,000)
print("\nD&C only:")
for n in (1000, 10000, 100000, 200000):
    pts = make(n)
    t, _ = best_of(closest_pair, pts, 3)
    print(f"{n:>8} {t:>10.4f} s   t/(n log2 n) = {t/(n*math.log2(n))*1e6:.3f} microseconds")
