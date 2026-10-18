#!/usr/bin/env python3
"""lab_drift_monitor - window rates, a drift statistic, the alert decision and its cost.

Offline and deterministic: the per-window successes come from a fixed linear
congruential generator, and the false-alarm rate is the analytic normal tail of
the threshold. No wall-clock, no operating-system randomness.

Statistic
    se            = sqrt(p0 * (1 - p0) / window)          p0 = baseline accuracy
    z(w)          = (rate(w) - p0) / se                   per monitoring window
    z_pooled      = (mean_rate - p0) / (se / sqrt(windows))
    alert         = the first window with |z| >= threshold
    alpha         = 2 * (1 - Phi(threshold))              false-alarm rate per window
    false alerts  = alpha * windows_per_day
    cost per day  = false alerts * cost per investigation

Flags
    --window INT        items per monitoring window (default 200)
    --baseline FLOAT    reference accuracy on the eval set (default 0.92)
    --observed FLOAT    true accuracy after the shift (default 0.85)
    --threshold FLOAT   |z| that raises the alert (default 3.0)
    --seed INT          seed of the per-window draws (default 7)
    --windows INT       number of windows printed (default 6)
    --sweep             observed rate from baseline down to baseline - 0.12
    --self-test         assert the properties this lab teaches
"""

from __future__ import annotations

import argparse
import math

RULE = "=" * 74
THIN = "-" * 74
WINDOWS_PER_DAY = 144          # stated assumption: one window every 10 minutes
INVESTIGATION_USD = 25.00      # stated assumption: cost of one investigation
SWEEP_SHIFTS = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.12]


def lcg(seed: int):
    """Deterministic float stream in [0, 1)."""
    state = (seed & 0xFFFFFFFFFFFFFFFF) ^ 0x2545F4914F6CDD1D

    def nxt() -> float:
        nonlocal state
        state = (state * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        return ((state >> 11) & ((1 << 53) - 1)) / float(1 << 53)

    return nxt


def window_rate(window: int, rate: float, seed: int) -> float:
    """Draw one monitoring window of `window` items with true success rate `rate`."""
    nxt = lcg(seed)
    hits = 0
    for _ in range(window):
        if nxt() < rate:
            hits += 1
    return hits / window


def normal_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def false_alarm_rate(threshold: float) -> float:
    """Two-sided normal false-alarm rate for a |z| >= threshold decision rule."""
    return 2.0 * (1.0 - normal_cdf(threshold))


def se_of_rate(window: int, p0: float) -> float:
    return math.sqrt(p0 * (1.0 - p0) / window)


def pooled_z(mean_rate: float, windows: int, window: int, p0: float) -> float:
    se = se_of_rate(window, p0) / math.sqrt(windows)
    return (mean_rate - p0) / se


def windows_to_detect(observed: float, window: int, p0: float, threshold: float) -> float:
    """Windows of pooled evidence needed for |z_pooled| to reach the threshold."""
    se1 = se_of_rate(window, p0)
    step = abs(observed - p0) / se1
    if step == 0.0:
        return float("inf")
    return (threshold / step) ** 2


def report(window: int, baseline: float, observed: float, threshold: float,
           seed: int, windows: int) -> None:
    se = se_of_rate(window, baseline)
    rates = [window_rate(window, observed, seed + 1000 * (i + 1)) for i in range(windows)]
    zs = [(r - baseline) / se for r in rates]
    alert_at = 0
    for i, z in enumerate(zs):
        if abs(z) >= threshold:
            alert_at = i + 1
            break
    mean_rate = sum(rates) / len(rates)
    z_pool = pooled_z(mean_rate, windows, window, baseline)
    alpha = false_alarm_rate(threshold)
    alerts_day = alpha * WINDOWS_PER_DAY
    cost_day = alerts_day * INVESTIGATION_USD
    needed = windows_to_detect(observed, window, baseline, threshold)

    print(RULE)
    print("lab_drift_monitor - window rates, drift statistic, alert and false-positive cost")
    print("offline, deterministic; window=%d  baseline=%.3f  observed=%.3f  threshold=%.2f  seed=%d"
          % (window, baseline, observed, threshold, seed))
    print("assumption: se = sqrt(p0(1-p0)/window) = %.5f; alert when |z| >= %.2f" % (se, threshold))
    print(THIN)
    print("1) per-window accuracy and drift statistic (shift = %.3f)" % (observed - baseline))
    print("  window  successes   rate          z     decision")
    for i, (r, z) in enumerate(zip(rates, zs)):
        print("  %6d  %9d  %6.4f  %9.3f     %s"
              % (i + 1, round(r * window), r, z, "ALERT" if abs(z) >= threshold else "ok"))
    print(THIN)
    print("2) decision: %s" % ("ALERT at window %d" % alert_at if alert_at else "no alert"))
    print("   pooled rate %.4f over %d windows -> pooled z %+.3f" % (mean_rate, windows, z_pool))
    print("   analytic windows for the pooled z to reach %.2f : %.2f" % (threshold, needed))
    print(THIN)
    print("3) cost of the false alarms this threshold buys")
    print("   false-alarm rate per window     : %.6f" % alpha)
    print("   windows per day %d -> false alerts per day : %.4f" % (WINDOWS_PER_DAY, alerts_day))
    print("   investigation USD %.2f per alert -> USD %.2f/day, USD %.2f per 30 days"
          % (INVESTIGATION_USD, cost_day, cost_day * 30))
    print(THIN)
    print("မှတ်ချက် - window သေးလျှင် standard error ကြီးသည့်အတွက် ပြောင်းလဲမှုကို ဖော်ထုတ်ရန်")
    print("window အရေအတွက် ပိုလိုသည်။ threshold ကို နိမ့်လျှင် ဖမ်းယူနိုင်မှု တိုးသော်လည်း false alert")
    print("အရေအတွက် တိုးသည့်အတွက် စုံစမ်းစစ်ဆေးမှု ကုန်ကျစရိတ် တိုးသည်။ ကိန်းဂဏန်းများသည်")
    print("baseline၊ window အရွယ်အစားနှင့် ကုန်ကျစရိတ် ယူဆချက်အပေါ် မှီခိုသည်။")
    print(RULE)


def sweep(baseline: float, window: int, threshold: float) -> None:
    print(RULE)
    print("lab_drift_monitor - detected-shift sweep (offline, deterministic)")
    print("baseline=%.3f  window=%d  threshold=%.2f  se=%.5f"
          % (baseline, window, threshold, se_of_rate(window, baseline)))
    print(THIN)
    print("%10s %10s %12s %16s %14s" % ("shift", "observed", "z per window", "windows to alert", "verdict"))
    needed_prev = None
    for shift in SWEEP_SHIFTS:
        observed = baseline - shift
        z1 = (observed - baseline) / se_of_rate(window, baseline)
        needed = windows_to_detect(observed, window, baseline, threshold)
        verdict = "alert" if abs(z1) >= threshold else ("alert later" if needed <= 24 else "too small")
        if shift == 0.0:
            verdict = "no shift"
        print("%10.2f %10.3f %12.3f %16s %14s"
              % (shift, observed, z1, "-" if math.isinf(needed) else "%.2f" % needed, verdict))
        needed_prev = needed
    print(THIN)
    print("မှတ်ချက် - ပြောင်းလဲမှု ကြီးလျှင် window တစ်ခုတည်းဖြင့် ဖမ်းနိုင်သည်၊ သေးလျှင် window")
    print("အရေအတွက် များစွာ စုစည်းပြီးမှ pooled z သည် threshold ကို ကျော်သည်။ လွတ်သည့် ပြောင်းလဲမှုကို")
    print("မဖမ်းမိဘဲ ကျန်ခြင်းသည် ထုတ်လုပ်မှုတွင် တိတ်ဆိတ်စွာ ကျဆင်းမှု ဖြစ်စေသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    window, baseline, threshold = 200, 0.92, 3.0

    small_shift = 0.915
    z_small = (small_shift - baseline) / se_of_rate(window, baseline)
    stays = abs(z_small) < threshold
    print("[OK] a small drift stays under the threshold (z %+.3f at shift %.3f): %s"
          % (z_small, baseline - small_shift, stays))
    ok = ok and stays

    big_shift = 0.84
    z_big = (big_shift - baseline) / se_of_rate(window, baseline)
    crosses = abs(z_big) >= threshold
    print("[OK] the stated shift crosses the threshold (z %+.3f at shift %.3f): %s"
          % (z_big, baseline - big_shift, crosses))
    ok = ok and crosses

    r_small = window_rate(window, small_shift, 7)
    r_big = window_rate(window, big_shift, 7)
    decides = abs((r_small - baseline) / se_of_rate(window, baseline)) < threshold <= \
        abs((r_big - baseline) / se_of_rate(window, baseline))
    print("[OK] the simulated windows give the same decisions (%.4f under, %.4f over): %s"
          % (r_small, r_big, decides))
    ok = ok and decides

    se1 = se_of_rate(200, baseline)
    se4 = se_of_rate(800, baseline)
    halves = abs(se4 - se1 / 2.0) < 1e-12
    print("[OK] a window four times larger halves the standard error (%.5f -> %.5f): %s" % (se1, se4, halves))
    ok = ok and halves

    cheap = false_alarm_rate(2.0)
    strict = false_alarm_rate(3.0)
    fewer = cheap > strict
    print("[OK] a lower threshold buys more false alarms (alpha %.4f at 2.0 vs %.6f at 3.0): %s"
          % (cheap, strict, fewer))
    ok = ok and fewer

    print("[PASS] lab_drift_monitor self-test passed." if ok else "[FAIL] lab_drift_monitor self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Drift monitoring window / alert cost lab (offline, deterministic).")
    ap.add_argument("--window", type=int, default=200, help="items per monitoring window")
    ap.add_argument("--baseline", type=float, default=0.92, help="reference accuracy on the eval set")
    ap.add_argument("--observed", type=float, default=0.85, help="true accuracy after the shift")
    ap.add_argument("--threshold", type=float, default=3.0, help="|z| that raises the alert")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--windows", type=int, default=6)
    ap.add_argument("--sweep", action="store_true", help="shift sweep from 0.00 to 0.12")
    ap.add_argument("--self-test", action="store_true", help="assert the properties this lab teaches")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        sweep(args.baseline, args.window, args.threshold)
        return 0
    report(args.window, args.baseline, args.observed, args.threshold, args.seed, args.windows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
