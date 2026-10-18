#!/usr/bin/env python3
"""Worked example (b): retry amplification and the load a dependency sees.

ဤ script သည် retry များက dependency တစ်ခုပေါ် မည်မျှ ဝန် ထပ်တိုးစေသည်ကို တွက်သည်။
ချို့ယွင်းမှု တစ်ခုလုံး ဖြစ်ပေါ်စဉ် retry wave တစ်ခု၏ အမြင့်ဆုံး peak ကိုလည်း ဆန်းစစ်သည်။

Assumptions (ဤစာတမ်းတွင် ဖော်ပြထားသည်):
  original demand = 200 req/s
  dependency သည် 1.0 s ကြာ လုံးဝ ချို့ယွင်းသွားသည် (failure wave 1 ခု)
  ထို wave အတွင်း request တိုင်းသည် ကျရှုံးသည် (failure rate 1.00 on the wave)
  caller သည် အများဆုံး retry 3 ကြိမ် ပြုလုပ်သည် (attempt စုစုပေါင်း 4 ခု)
  backoff သည် 200 ms မှ စ၍ exponential ဖြစ်သည် (200, 400, 800 ms)
  retry budget သည် မူလ request ၏ 10% အထိသာ ခွင့်ပြုသည်
  circuit breaker သည် ပွင့်သည့်အခါ 1000 ms ပိတ်ထားသည် (closed fraction 0.500)
  jitter 1.0 သည် full jitter ဖြစ်သည် — delay ကို [0, delay] အတွင်း တူညီစွာ ဖြန့်သည်
  peak ကို 10 ms bucket ဖြင့် တိုင်းသည်

No third-party import, no wall-clock, deterministic (seeded jitter draw only).
"""

from __future__ import annotations

import argparse
import random

RULE = "=" * 74
THIN = "-" * 74
BUCKET_MS = 10.0


def amplification(failure_rate: float, retries: int) -> float:
    """attempt အရေအတွက် စုစုပေါင်း ÷ မူလ request အရေအတွက်။"""
    return sum(failure_rate ** k for k in range(retries + 1))


def retry_wave(rps: float, failure_rate: float, retries: int, backoff_ms: float, jitter: float,
               wave_s: float, seed: int) -> tuple[float, float, int]:
    """Failure wave တစ်ခု၏ retry များကို 10 ms bucket အလိုက် ခွဲ၍ peak ကို ရှာသည်။"""
    rnd = random.Random(seed)
    n = int(round(rps * wave_s))
    buckets: dict[int, int] = {}
    total = 0
    for k in range(1, retries + 1):
        delay_ms = backoff_ms * (2 ** (k - 1))
        count = int(round(n * (failure_rate ** (k - 1))))
        for _ in range(count):
            factor = 1.0 - jitter * rnd.random()
            at_ms = delay_ms * factor
            bucket = int(at_ms // BUCKET_MS)
            buckets[bucket] = buckets.get(bucket, 0) + 1
            total += 1
    peak = max(buckets.values()) if buckets else 0
    return peak * (1000.0 / BUCKET_MS), float(len(buckets)), total


def main() -> int:
    ap = argparse.ArgumentParser(description="Retry amplification and dependency load during partial failure.")
    ap.add_argument("--rps", type=float, default=200.0, help="original demand in req/s (assumed)")
    ap.add_argument("--failure-rate", type=float, default=0.50, help="per-attempt failure probability (assumed)")
    ap.add_argument("--retries", type=int, default=3, help="max retries after the first attempt")
    ap.add_argument("--backoff-ms", type=float, default=200.0, help="base backoff in ms (exponential, assumed)")
    ap.add_argument("--retry-budget", type=float, default=0.10, help="retry traffic allowed vs originals (assumed)")
    ap.add_argument("--breaker-open-ms", type=float, default=1000.0, help="breaker open time (assumed)")
    ap.add_argument("--breaker-after", type=int, default=5, help="consecutive failures before the breaker opens")
    ap.add_argument("--wave-seconds", type=float, default=1.0, help="how long the failure lasts (assumed)")
    ap.add_argument("--seed", type=int, default=20240)
    args = ap.parse_args()

    f = args.failure_rate
    print(RULE)
    print("retry_amplification - retry များ၏ ဝန် ထပ်တိုး အကျိုးသက်ရောက်မှု (offline, deterministic)")
    print(f"assumptions: original demand {args.rps:.0f} req/s, per-attempt failure rate {f:.2f}, "
          f"max retries {args.retries}, base backoff {args.backoff_ms:.0f} ms")
    print(THIN)
    print(f"{'layer':>6} {'requests/s':>11} {'cumulative/s':>13} {'backoff ms':>11} {'arrival window ms':>18}")
    layer_rps = args.rps
    cumulative = 0.0
    for k in range(args.retries + 1):
        backoff = args.backoff_ms * (2 ** (k - 1)) if k >= 1 else 0.0
        cumulative += layer_rps
        window = backoff if k >= 1 else 0.0
        print(f"{k:>6} {layer_rps:>11.2f} {cumulative:>13.2f} {backoff:>11.0f} {window:>18.0f}")
        layer_rps *= f
    amp = amplification(f, args.retries)
    load = args.rps * amp
    print(THIN)
    print(f"dependency load while the failure lasts : {load:.2f} req/s "
          f"(amplification {amp:.3f}x on {args.rps:.0f} req/s)")
    print(f"retry traffic alone                     : {load - args.rps:.2f} req/s")
    capped_amp = 1.0 + min(sum(f ** k for k in range(1, args.retries + 1)), args.retry_budget)
    print(f"with a retry budget of {args.retry_budget * 100:.0f}%              : {args.rps * capped_amp:.2f} req/s "
          f"(amplification {capped_amp:.3f}x)")
    open_s = args.breaker_open_ms / 1000.0
    closed_fraction = 1.0 / (1.0 + open_s)
    breaker_amp = 1.0 + (amp - 1.0) * closed_fraction
    print(f"with a breaker open {open_s:.0f} s after {args.breaker_after} failures : "
          f"{args.rps * breaker_amp:.2f} req/s (amplification {breaker_amp:.3f}x, "
          f"closed fraction {closed_fraction:.3f})")
    print(THIN)
    print(f"failure wave: dependency is down {args.wave_seconds:.1f} s, "
          f"{int(round(args.rps * args.wave_seconds))} requests fail and are retried")
    for jitter in (0.0, 1.0):
        peak, span, total = retry_wave(args.rps, f, args.retries, args.backoff_ms, jitter,
                                      args.wave_seconds, args.seed)
        print(f"  jitter {jitter:.1f}  retries {total:>4}  buckets used {int(span):>4}  "
              f"peak {peak:>10.2f} req/s over a {BUCKET_MS:.0f} ms bucket")
    print(THIN)
    print("မှတ်ချက် - retry သည် demand ကို ပြန်လည် ရယူသည့် နည်းလမ်း မဟုတ်ဘဲ ဝန် ကို ဆတိုး တိုးစေသည့် "
          "အရာ ဖြစ်သည်။ ချို့ယွင်းနေသည့် dependency သည် စွမ်းရည် အနည်းဆုံး ဖြစ်နေချိန်တွင် retry များက "
          "ဝန်ကို အမြင့်ဆုံး ရောက်စေသည်၊ jitter သည် retry တစ်ခုလုံးကို တစ်ချိန်တည်း မရောက်စေရန် ဖြန့်သည်။")
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
