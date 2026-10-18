#!/usr/bin/env python3
"""lab_retry_storm - retry များက dependency တစ်ခုပေါ် ဝန် မည်မျှ ထပ်တိုးစေသည်၊ jitter နှင့်
circuit breaker က ထို ဝန်ကို မည်သို့ ကန့်သတ်သည်ကို စမ်းသပ်သည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

model —
    layer 0 = မူလ request များ (--rps)
    layer k = layer k-1 မှ failure-rate ဖြင့် ကျရှုံးသည့် request များ (အများဆုံး --retries လွှာ)
    backoff သည် --backoff-ms မှ စ၍ exponential ဖြစ်သည် (200, 400, 800 ms ...)
    amplification = attempt အားလုံး စုစုပေါင်း ÷ မူလ request
    jitter သည် retry delay ကို [delay x (1 - jitter), delay] အတွင်း ဖြန့်သည်
    circuit breaker ပွင့်နေသည့် အချိုး = 1 - 1/(1 + open-seconds)  (assumed)
"""

from __future__ import annotations

import argparse
import random

RULE = "=" * 74
THIN = "-" * 74
BUCKET_MS = 10.0


def amplification(failure_rate: float, retries: int) -> float:
    return sum(failure_rate ** k for k in range(retries + 1))


def retry_wave(rps: float, failure_rate: float, retries: int, backoff_ms: float, jitter: float,
               wave_s: float, seed: int) -> dict:
    """Failure wave တစ်ခုအတွင်း retry များကို 10 ms bucket အလိုက် ခွဲသည်။"""
    rnd = random.Random(seed)
    n = int(round(rps * wave_s))
    buckets: dict[int, int] = {}
    total = 0
    for k in range(1, retries + 1):
        delay_ms = backoff_ms * (2 ** (k - 1))
        count = int(round(n * (failure_rate ** (k - 1))))
        for _ in range(count):
            at_ms = delay_ms * (1.0 - jitter * rnd.random())
            bucket = int(at_ms // BUCKET_MS)
            buckets[bucket] = buckets.get(bucket, 0) + 1
            total += 1
    peak = max(buckets.values()) if buckets else 0
    return {"retries": total, "buckets": len(buckets), "peak_rps": peak * (1000.0 / BUCKET_MS)}


def print_report(args: argparse.Namespace) -> None:
    f = args.failure_rate
    print(RULE)
    print("lab_retry_storm - retry amplification နှင့် dependency load (offline, deterministic)")
    print(f"rps={args.rps:.1f}  failure-rate={f:.2f}  retries={args.retries}  "
          f"backoff={args.backoff_ms:.0f} ms  jitter={args.jitter:.2f}  seed={args.seed}")
    print(THIN)
    print(f"{'layer':>6} {'requests/s':>11} {'cumulative/s':>13} {'backoff ms':>11}")
    layer = args.rps
    cumulative = 0.0
    for k in range(args.retries + 1):
        cumulative += layer
        backoff = args.backoff_ms * (2 ** (k - 1)) if k >= 1 else 0.0
        print(f"{k:>6} {layer:>11.2f} {cumulative:>13.2f} {backoff:>11.0f}")
        layer *= f
    amp = amplification(f, args.retries)
    print(THIN)
    print(f"amplification factor              : {amp:>8.3f}x")
    print(f"dependency load during failure    : {args.rps * amp:>8.2f} req/s "
          f"(baseline {args.rps:.2f}, extra {args.rps * (amp - 1.0):.2f})")
    capped = 1.0 + min(sum(f ** k for k in range(1, args.retries + 1)), args.retry_budget)
    print(f"retry budget {args.retry_budget * 100:.0f}%                     : {capped:>8.3f}x "
          f"-> {args.rps * capped:.2f} req/s")
    open_s = args.breaker_open_ms / 1000.0
    closed = 1.0 / (1.0 + open_s)
    breaker = 1.0 + (amp - 1.0) * closed
    print(f"circuit breaker (open {open_s:.0f} s)        : {breaker:>8.3f}x "
          f"-> {args.rps * breaker:.2f} req/s (closed fraction {closed:.3f})")
    print(THIN)
    print(f"jitter effect on one {args.wave_seconds:.1f} s failure wave ({BUCKET_MS:.0f} ms buckets):")
    print(f"{'jitter':>8} {'retries':>9} {'buckets':>9} {'peak req/s':>12}")
    rows = [0.0] if args.jitter == 0.0 else [0.0, args.jitter]
    for jitter in rows:
        w = retry_wave(args.rps, f, args.retries, args.backoff_ms, jitter, args.wave_seconds, args.seed)
        print(f"{jitter:>8.2f} {w['retries']:>9} {w['buckets']:>9} {w['peak_rps']:>12.2f}")
    print(THIN)
    print("မှတ်ချက် - retry သည် ဝန် ကို ဆတိုး တိုးစေသည်။ ချို့ယွင်းနေသည့် dependency သည် စွမ်းရည် "
          "အနည်းဆုံး ဖြစ်နေချိန်တွင် retry များ တစ်ချိန်တည်း ရောက်လျှင် ချို့ယွင်းမှု ပို၍ ကြာသည်။")
    print(RULE)


def print_sweep(args: argparse.Namespace) -> None:
    print(RULE)
    print("lab_retry_storm - retries sweep 0 .. 6 (failure-rate %.2f, rps %.1f)" % (args.failure_rate, args.rps))
    print(f"{'retries':>9} {'amplification':>14} {'dep load req/s':>15} {'peak no-jitter':>15} {'peak jitter':>12}")
    for retries in range(0, 7):
        amp = amplification(args.failure_rate, retries)
        no_jitter = retry_wave(args.rps, args.failure_rate, retries, args.backoff_ms, 0.0,
                               args.wave_seconds, args.seed)
        with_jitter = retry_wave(args.rps, args.failure_rate, retries, args.backoff_ms, 1.0,
                                 args.wave_seconds, args.seed)
        print(f"{retries:>9} {amp:>14.3f} {args.rps * amp:>15.2f} "
              f"{no_jitter['peak_rps']:>15.2f} {with_jitter['peak_rps']:>12.2f}")
    print(THIN)
    print("မှတ်ချက် - retry လွှာ တိုးလျှင် amplification သည် ကန့်သတ်တန်ဖိုး 1/(1-failure-rate) သို့ "
          "ရောက်သည်။ jitter သည် peak ကို လျှော့ချသည်၊ amplification ကို မလျှော့ချပါ။")
    print(RULE)


def self_test() -> int:
    ok = True
    f, retries = 0.50, 3

    amp = amplification(f, retries)
    exact = abs(amp - (1.0 + 0.5 + 0.25 + 0.125)) < 1e-12
    print(f"[OK] amplification is the closed-form sum of the attempt ratios (1.875 = 1.875): {exact}")
    ok = ok and exact

    more = amplification(f, retries + 2) > amplification(f, retries)
    print(f"[OK] more retries add load (1.875 -> {amplification(f, retries + 2):.6f}): {more}")
    ok = ok and more

    worse = amplification(0.75, retries) > amplification(0.25, retries)
    print(f"[OK] a higher failure rate raises amplification "
          f"({amplification(0.25, retries):.3f} -> {amplification(0.75, retries):.3f}): {worse}")
    ok = ok and worse

    no_j = retry_wave(200.0, f, retries, 200.0, 0.0, 1.0, 20240)
    full_j = retry_wave(200.0, f, retries, 200.0, 1.0, 1.0, 20240)
    spreads = full_j["peak_rps"] < no_j["peak_rps"] and full_j["buckets"] > no_j["buckets"]
    print(f"[OK] jitter spreads the same retries over more buckets and lowers the peak "
          f"({no_j['peak_rps']:.0f} -> {full_j['peak_rps']:.0f} req/s over a {BUCKET_MS:.0f} ms bucket): {spreads}")
    ok = ok and spreads

    same_total = full_j["retries"] == no_j["retries"]
    print(f"[OK] jitter does not remove retries, it only re-times them ({full_j['retries']} both): {same_total}")
    ok = ok and same_total

    budget = 0.10
    capped = 1.0 + min(sum(f ** k for k in range(1, retries + 1)), budget)
    bounded = abs(capped - 1.10) < 1e-12 and capped < amp
    print(f"[OK] a retry budget bounds amplification to 1 + budget ({capped:.3f} < {amp:.3f}): {bounded}")
    ok = ok and bounded

    open_s = 1.0
    closed = 1.0 / (1.0 + open_s)
    breaker = 1.0 + (amp - 1.0) * closed
    limits = breaker < amp and breaker > 1.0
    print(f"[OK] a circuit breaker cuts the retry share while it is open "
          f"({amp:.3f}x -> {breaker:.3f}x at closed fraction {closed:.3f}): {limits}")
    ok = ok and limits

    print("[PASS] lab_retry_storm self-test passed." if ok else "[FAIL] lab_retry_storm self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Retry storm lab (offline, deterministic).")
    ap.add_argument("--rps", type=float, default=200.0)
    ap.add_argument("--failure-rate", type=float, default=0.50)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--backoff-ms", type=float, default=200.0)
    ap.add_argument("--jitter", type=float, default=1.00, help="0.0 = none, 1.0 = full jitter")
    ap.add_argument("--retry-budget", type=float, default=0.10)
    ap.add_argument("--breaker-open-ms", type=float, default=1000.0)
    ap.add_argument("--wave-seconds", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=20240)
    ap.add_argument("--sweep", action="store_true", help="retries 0 .. 6 sweep")
    ap.add_argument("--self-test", action="store_true", help="assert the real retry properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args)
        return 0
    print_report(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
