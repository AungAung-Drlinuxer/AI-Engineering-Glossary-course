#!/usr/bin/env python3
"""Worked example (c): the eval size needed to separate two models at a stated effect size.

DERIVATION plus a deterministic score simulation. No wall-clock and no
operating-system randomness: the scores come from a fixed linear congruential
generator, so every run prints the same numbers.

Assumptions (all labelled):
    model A accuracy            = 0.72
    model B accuracy            = 0.80  (stated effect size delta = 0.08)
    two-sided z for 95%         = 1.96
    power 80% z                 = 0.84
    discordant pair rate (McNemar) = 0.15  (stated assumption for the paired design)
    separation rule             = the observed gap must exceed 1.96 x its standard error
    simulation trials           = 200 at each reported eval size

Formulas (two independent binomial samples):
    se(n) = sqrt(pA(1-pA)/n + pB(1-pB)/n)
    n*    = z^2 * (pA(1-pA) + pB(1-pB)) / delta^2
Formula (paired design, McNemar on discordant pairs), d = discordant rate:
    n*_pair = (z*sqrt(d) + z_beta*sqrt(d - delta^2))^2 / delta^2
"""

import math

PA = 0.72
PB = 0.80
Z = 1.96
Z_BETA = 0.84
DISCORDANT = 0.15
TRIALS = 200
GRID = (100, 250, 500, 1000, 2000, 4000, 8000, 16000, 32000)
SPREAD_GRID = (100, 500, 2000, 8000)

RULE = "=" * 74
THIN = "-" * 74


def lcg(seed: int):
    """Deterministic float stream in [0, 1) from a 64-bit linear congruential generator."""
    state = (seed & 0xFFFFFFFFFFFFFFFF) ^ 0x2545F4914F6CDD1D

    def nxt() -> float:
        nonlocal state
        state = (state * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        return ((state >> 11) & ((1 << 53) - 1)) / float(1 << 53)

    return nxt


def simulate(n: int, pa: float, pb: float, seed: int):
    """Score n items for two models independently; return (rate_a, rate_b)."""
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
    """Smallest integer n whose standard error is below delta / z (bisection)."""
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


def main() -> None:
    delta = PB - PA
    print(RULE)
    print("ex_c_eval_size - eval size needed to separate two models (offline, deterministic)")
    print("assumptions: model A %.2f, model B %.2f, delta %.2f, z=%.2f, power z=%.2f, trials %d"
          % (PA, PB, delta, Z, Z_BETA, TRIALS))
    print("             separation rule: gap > %.2f x standard error of the gap" % Z)
    print(THIN)
    print("%8s %12s %14s %12s %12s" % ("n", "se(gap)", "1.96*se", "observed gap", "separated"))
    for n in GRID:
        ga, gb = simulate(n, PA, PB, seed=1000 + n)
        gap = gb - ga
        se = se_gap(n, PA, PB)
        print("%8d %12.5f %14.5f %12.5f %12s" % (n, se, Z * se, gap, "yes" if abs(gap) > Z * se else "no"))
    print(THIN)
    n_star = smallest_n(delta, PA, PB)
    n_star_exact = Z * Z * (PA * (1 - PA) + PB * (1 - PB)) / (delta * delta)
    n_pair = (Z * math.sqrt(DISCORDANT) + Z_BETA * math.sqrt(DISCORDANT - delta * delta)) ** 2 / (delta * delta)
    print("analytic unpaired n*              : %8.1f items (ceil %d)" % (n_star_exact, math.ceil(n_star_exact)))
    print("smallest integer n that separates  : %8d items (rule above)" % n_star)
    print("analytic paired  n* (McNemar)      : %8.1f items (ceil %d, discordant rate %.2f)"
          % (n_pair, math.ceil(n_pair), DISCORDANT))
    print("pairing discount                  : paired n is %.1f%% of the unpaired n at this delta"
          % (100.0 * n_pair / n_star_exact))
    print(THIN)
    print("spread of the observed gap over %d trials at the sizes below:" % TRIALS)
    print("%8s %10s %10s %10s %16s" % ("n", "min gap", "mean gap", "max gap", "separation rate"))
    for n in SPREAD_GRID:
        gaps = []
        seps = 0
        for t in range(TRIALS):
            ga, gb = simulate(n, PA, PB, seed=7919 * (t + 1) + n)
            gap = gb - ga
            gaps.append(gap)
            if abs(gap) > Z * se_gap(n, PA, PB):
                seps += 1
        print("%8d %10.5f %10.5f %10.5f %15.1f%%"
              % (n, min(gaps), sum(gaps) / len(gaps), max(gaps), 100.0 * seps / TRIALS))
    print(THIN)
    print("မှတ်ချက် - eval size သည် သေးငယ်လျှင် ကွာဟမှု၏ standard error ကြီးသည့်အတွက် model")
    print("နှစ်ခုကို ခွဲခြားနိုင်ခြင်း မရှိပါ။ n တိုးလျှင် standard error သည် sqrt(n) အလိုက် ကျဆင်းပြီး")
    print("သတ်မှတ်ထားသည့် effect size ကို စိတ်ချစွာ ဖော်ထုတ်နိုင်သည်။ ကိန်းဂဏန်းများသည်")
    print("သတ်မှတ်ထားသည့် accuracy နှင့် delta အပေါ် မှီခိုသည့်အတွက် 'တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်'။")
    print(RULE)


if __name__ == "__main__":
    main()
