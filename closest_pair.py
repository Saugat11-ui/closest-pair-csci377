"""Closest pair of points in the plane.

Two algorithms:
  * brute_force(points)         -> O(n^2)
  * closest_pair(points)        -> O(n log n), divide-and-conquer

Notation used everywhere in this project:
  n = number of points.
  d = the smaller of the two distances found in the left and right halves.
  strip = the points whose x-coordinate is within d of the dividing line.

Both functions return (squared_distance, point_a, point_b). Squared
distances are compared internally (no sqrt) and converted at the end.
"""
import math
import sys


def _sq(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def brute_force(points):
    """Check every pair. O(n^2). Requires at least 2 points."""
    n = len(points)
    if n < 2:
        raise ValueError("need at least 2 points")
    best = _sq(points[0], points[1])
    pair = (points[0], points[1])
    for i in range(n):
        pi = points[i]
        for j in range(i + 1, n):
            d2 = _sq(pi, points[j])
            if d2 < best:
                best = d2
                pair = (pi, points[j])
    return best, pair[0], pair[1]


def _merge_by_y(left, right):
    """Merge two lists already sorted by y into one list sorted by y. O(len)."""
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][1] <= right[j][1]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def _rec(px, lo, hi):
    """px is sorted by x (sorted ONCE by the caller). Works on px[lo:hi].

    Returns (best_sq, a, b, by_y) where by_y is px[lo:hi] sorted by y,
    built by MERGING the two halves' y-orders (never by re-sorting).
    """
    n = hi - lo
    if n <= 3:                                   # base case: brute force
        pts = px[lo:hi]
        if n == 1:
            return math.inf, None, None, pts
        best, a, b = brute_force(pts)
        return best, a, b, sorted(pts, key=lambda p: p[1])   # <= 3 points: O(1)

    mid = lo + n // 2
    mid_x = px[mid][0]                           # dividing line x = mid_x
    dl, la, lb, y_left = _rec(px, lo, mid)
    dr, ra, rb, y_right = _rec(px, mid, hi)

    if dl <= dr:                                 # d^2 = smaller of the two
        best, a, b = dl, la, lb
    else:
        best, a, b = dr, ra, rb

    by_y = _merge_by_y(y_left, y_right)          # O(n), no re-sort

    # strip = points with |x - mid_x| < d, already in y order
    strip = [p for p in by_y if (p[0] - mid_x) * (p[0] - mid_x) < best]
    for i in range(len(strip)):
        pi = strip[i]
        j = i + 1
        # Only points whose y is within d above pi can matter; at most ~7.
        while j < len(strip) and (strip[j][1] - pi[1]) * (strip[j][1] - pi[1]) < best:
            d2 = _sq(pi, strip[j])
            if d2 < best:
                best, a, b = d2, pi, strip[j]
            j += 1
    return best, a, b, by_y


def closest_pair(points):
    """Divide-and-conquer closest pair. O(n log n). Requires >= 2 points."""
    if len(points) < 2:
        raise ValueError("need at least 2 points")
    px = sorted(points)                          # the one up-front sort: O(n log n)
    best, a, b, _ = _rec(px, 0, len(px))
    return best, a, b


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print("Input points:", " ".join(map(str, pts)))
    for name, f in (("Divide-and-conquer", closest_pair), ("Brute force", brute_force)):
        d2, a, b = f(pts)
        print(f"{name:19s} closest pair: {a} and {b}   distance = {math.sqrt(d2):.4f}")
