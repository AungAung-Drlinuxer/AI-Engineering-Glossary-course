#!/usr/bin/env python3
"""lab_eval_size - how large an eval set must be to separate two models.

Offline and deterministic: scores come from a fixed linear congruential
generator, so the same knobs always print the same numbers. No wall-clock, no
operating-system randomness, no third-party import.

Separating an effect from noise
    delta      = acc-b - acc-a                        (the effect you claim)
    se(n)      = sqrt(pa(1-pa)/n + pb(1-pb)/n)        (standard error of the gap)
    n*         = z^2 * (pa(1-pa) + pb(1-pb)) / delta^2 (analytic, z = 1.96)
A run is counted as separated when the observed gap exceeds 1.96 x se(n).

Flags
    --n INT          eval size of the point estimate (default 500)
    --acc-a FLOAT    accuracy of model A (default 0.72)
    --acc-b FLOAT    accuracy of model B (default 0.80)
    --seed INT       seed of the point estimate (default 11)
    --trials INT     simulation trials for the spread table (default 50)
    --sweep          table of n from 64 to 32768
    --self-test      assert the properties this lab teaches
"""

from __future__ import annotations

import argparse
import math

Z = 1.96
RULE = "=" * 74
THIN = "-" * 74
SWEEP_GRID = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
SEARCH_GRID = [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]


def lcg(seed: int):
    """Deterministic float stream in [0, 1)."""
    state = (seed & 0xFFFFFFFFFFFFFFFF) ^ 0x2545F4914F6CDD1D

    def nxt() -> float:
        nonlocal state
        state = (state * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        return ((state >> 11) & ((1 << 53) - 1)) / float(1 << 53)

    return nxt


def simulate(n: int, pa: float, pb: float, seed: int):
    """Score n items for two models; return (rate_a, rate_b)."""
    nxt = lcg(seed)
    correct_a = 0
    correct_b = 0
    for _ in range(n):
        if nxt() < pa:
            correct_a += 1
        if nxt() < pb:
            correct_b += 1
    return correct_a / n, correct_b / n


def se_gap(n: int, pa: float, pb: float) -> float:
    return math.sqrt(pa * (1.0 - pa) / n + pb * (1.0 - pb) / n)


def smallest_n(delta: float, pa: float, pb: float, cap: int = 10 ** 7) -> int:
    """Smallest integer n with z * se(n) below delta (bisection)."""
    lo, hi = 1, 2
    while hi <= cap and delta <= Z * se_gap(hi, pa, pb):
        lo, hi = hi, hi * 2
    if hi > cap:
        return -1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if delta > Z * se_gap(mid, pa, pb):
            hi = mid
        else:
            lo = mid
    return hi


def spread(n: int, pa: float, pb: float, trials: int, seed0: int = 7919):
    """Return (min gap, mean gap, max gap, separation rate) over `trials` trials."""
    gaps = []
    seps = 0
    limit = Z * se_gap(n, pa, pb)
    for t in range(trials):
        ga, gb = simulate(n, pa, pb, seed=seed0 * (t + 1) + n)
        gap = gb - ga
        gaps.append(gap)
        if abs(gap) > limit:
            seps += 1
    return min(gaps), sum(gaps) / len(gaps), max(gaps), seps / trials


def grid_separator(pa: float, pb: float, trials: int = 25) -> int:
    """First grid size at which every trial separates the two models."""
    for n in SEARCH_GRID:
        _, _, _, rate = spread(n, pa, pb, trials)
        if rate >= 1.0:
            return n
    return -1


def print_report(n: int, pa: float, pb: float, seed: int, trials: int) -> None:
    delta = pb - pa
    ga, gb = simulate(n, pa, pb, seed)
    gap = gb - ga
    se = se_gap(n, pa, pb)
    print(RULE)
    print("lab_eval_size - how large an eval set must be to separate two models")
    print("offline, deterministic simulation; n=%d  acc-a=%.3f  acc-b=%.3f  seed=%d  trials=%d"
          % (n, pa, pb, seed, trials))
    print(THIN)
    print("1) point estimate at n=%d (seed=%d)" % (n, seed))
    print("   observed gap a->b        : %10.5f" % gap)
    print("   standard error of gap    : %10.5f" % se)
    print("   separation threshold     : %10.5f   (%.2f x se)" % (Z * se, Z))
    print("   verdict                  : %10s" % ("SEPARATED" if abs(gap) > Z * se else "NOT SEPARATED"))
    print(THIN)
    print("2) spread of the observed gap over %d trials" % trials)
    print("   %8s %11s %12s %12s %16s" % ("n", "min gap", "mean gap", "max gap", "separation rate"))
    for size in (n, 2 * n, 4 * n):
        mn, mean, mx, rate = spread(size, pa, pb, trials)
        print("   %8d %11.5f %12.5f %12.5f %15.1f%%" % (size, mn, mean, mx, 100.0 * rate))
    print(THIN)
    n_star = smallest_n(delta, pa, pb)
    every = grid_separator(pa, pb)
    print("3) smallest eval size that separates them")
    print("   analytic n* for delta=%.3f  : %8d items (se %.5f, delta/se %.2f)"
          % (delta, n_star, se_gap(n_star, pa, pb), delta / se_gap(n_star, pa, pb)))
    print("   se at n* x 4              : %10.5f" % se_gap(4 * n_star, pa, pb))
    print("   first size where every trial separates : %8d items" % every)
    print("   ratio (every-size / n*)   : %10.2f" % (every / n_star if n_star > 0 and every > 0 else float("nan")))
    print(THIN)
    print("မှတ်ချက် - eval size သေးငယ်လျှင် ကွာဟမှု၏ standard error ကြီးသည့်အတွက် model နှစ်ခုကို")
    print("ခွဲခြားနိုင်ခြင်း မရှိပါ။ n လေးဆ တိုးလျှင် standard error ထက်ဝက် ကျဆင်းသည်။ analytic n*")
    print("သည် ပျမ်းမျှအားဖြင့် ခွဲခြားနိုင်သည့် အရေအတွက် ဖြစ်ပြီး run တိုင်း ခွဲခြားရန် ပို၍ လိုသည်။")
    print(RULE)


def print_sweep(pa: float, pb: float) -> None:
    print(RULE)
    print("lab_eval_size - n sweep (offline, deterministic)")
    print("acc-a=%.3f  acc-b=%.3f  delta=%.3f" % (pa, pb, pb - pa))
    print(THIN)
    print("%9s %12s %12s %13s %12s" % ("n", "se(gap)", "1.96*se", "observed gap", "separated"))
    for n in SWEEP_GRID:
        ga, gb = simulate(n, pa, pb, seed=1000 + n)
        se = se_gap(n, pa, pb)
        print("%9d %12.5f %12.5f %13.5f %12s"
              % (n, se, Z * se, gb - ga, "yes" if abs(gb - ga) > Z * se else "no"))
    print(THIN)
    print("မှတ်ချက် - n တိုးလျှင် threshold ကျဆင်းပြီး ကွာဟမှုသည် threshold ကို ကျော်လွန်သည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    pa, pb = 0.72, 0.80

    s1 = se_gap(1000, pa, pb)
    s4 = se_gap(4000, pa, pb)
    half = abs(s4 - s1 / 2.0) < 1e-12
    print("[OK] quadrupling n halves the standard error (%.5f -> %.5f): %s" % (s1, s4, half))
    ok = ok and half

    small_rate = spread(100, pa, pb, 40)[3]
    large_rate = spread(8000, pa, pb, 40)[3]
    grows = large_rate > small_rate
    print("[OK] a larger n separates the models more often (n=100 %.2f -> n=8000 %.2f): %s"
          % (small_rate, large_rate, grows))
    ok = ok and grows

    tight = smallest_n(0.04, pa, pb)
    wide = smallest_n(0.16, pa, pb)
    shrinks = 0 < wide < tight
    print("[OK] a larger effect size needs a smaller eval set (delta 0.16 %d vs delta 0.04 %d): %s"
          % (wide, tight, shrinks))
    ok = ok and shrinks

    every = grid_separator(pa, pb)
    adequate = every > smallest_n(pb - pa, pa, pb)
    print("[OK] a size where every trial separates is larger than the analytic n* (%d > %d): %s"
          % (every, smallest_n(pb - pa, pa, pb), adequate))
    ok = ok and adequate

    _, _, _, saturated = spread(32000, pa, pb, 40)
    always = saturated == 1.0
    print("[OK] at n=32000 every trial separates the models (rate %.2f): %s" % (saturated, always))
    ok = ok and always

    print("[PASS] lab_eval_size self-test passed." if ok else "[FAIL] lab_eval_size self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Eval-size / model-separation lab (offline, deterministic).")
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--acc-a", type=float, default=0.72)
    ap.add_argument("--acc-b", type=float, default=0.80)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--trials", type=int, default=50)
    ap.add_argument("--sweep", action="store_true", help="n sweep 64..32768")
    ap.add_argument("--self-test", action="store_true", help="assert the properties this lab teaches")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.acc_a, args.acc_b)
        return 0
    print_report(args.n, args.acc_a, args.acc_b, args.seed, args.trials)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
