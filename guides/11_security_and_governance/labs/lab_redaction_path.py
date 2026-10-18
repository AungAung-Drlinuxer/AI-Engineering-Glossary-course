#!/usr/bin/env python3
"""lab_redaction_path - request path တွင် redaction သို့မဟုတ် guardrail စစ်ဆေးမှု တစ်ခု ထည့်ခြင်း၏
latency၊ throughput ceiling နှင့် false redaction ကုန်ကျစရိတ်ကို စမ်းသပ်သည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ပုံသေနည်း
    total_check_ms    = check_ms + pattern_count * ms_per_pattern
    added_p50_ms      = total_check_ms
    added_p95_ms      = total_check_ms * p95_factor
    ceiling_req_s     = workers / ((base_ms + total_check_ms) / 1000)
    utilisation       = requests_per_s / ceiling_req_s
    false_per_day     = requests_per_s * 86400 * false_positive_rate
    false_cost_usd    = false_per_day * usd_per_false_redaction
"""

from __future__ import annotations

import argparse

RULE = "=" * 102
THIN = "-" * 102

MS_PER_PATTERN = 0.15
P95_FACTOR = 1.8
SECONDS_PER_DAY = 86400.0
SWEEP_CHECK_MS = [0.0, 5.0, 10.0, 20.0, 35.0, 70.0, 140.0]


def total_check_ms(check_ms: float, pattern_count: float) -> float:
    return check_ms + pattern_count * MS_PER_PATTERN


def added_p50_ms(check_ms: float, pattern_count: float) -> float:
    return total_check_ms(check_ms, pattern_count)


def added_p95_ms(check_ms: float, pattern_count: float) -> float:
    return total_check_ms(check_ms, pattern_count) * P95_FACTOR


def ceiling_req_s(check_ms: float, pattern_count: float, workers: int, base_ms: float) -> float:
    return workers / ((base_ms + total_check_ms(check_ms, pattern_count)) / 1000.0)


def false_per_day(requests_per_s: float, false_positive_rate: float) -> float:
    return requests_per_s * SECONDS_PER_DAY * false_positive_rate


def print_report(requests_per_s: float, check_ms: float, workers: int, pattern_count: int,
                 false_positive_rate: float, base_ms: float,
                 usd_per_false_redaction: float) -> None:
    tc = total_check_ms(check_ms, pattern_count)
    p50 = added_p50_ms(check_ms, pattern_count)
    p95 = added_p95_ms(check_ms, pattern_count)
    ceil = ceiling_req_s(check_ms, pattern_count, workers, base_ms)
    ceil_no = workers / (base_ms / 1000.0)
    fp = false_per_day(requests_per_s, false_positive_rate)
    print(RULE)
    print("lab_redaction_path - request path တွင် redaction စစ်ဆေးမှု၏ latency နှင့် throughput ကုန်ကျစရိတ်")
    print(f"requests_per_s={requests_per_s:g}  check_ms={check_ms:g}  workers={workers}  "
          f"pattern_count={pattern_count}  false_positive_rate={false_positive_rate:g}")
    print(f"(assumption) ms_per_pattern={MS_PER_PATTERN}  p95_factor={P95_FACTOR}  base_ms={base_ms:g}  "
          f"usd_per_false_redaction={usd_per_false_redaction:g}")
    print(THIN)
    print(f"total redaction check latency   : {tc:>14,.2f} ms per request")
    print(f"added p50 latency               : {p50:>14,.2f} ms")
    print(f"added p95 latency               : {p95:>14,.2f} ms")
    print(f"throughput ceiling with check   : {ceil:>14,.1f} req/s")
    print(f"throughput ceiling without check: {ceil_no:>14,.1f} req/s")
    print(f"ceiling lost to the check       : {(1.0 - ceil / ceil_no) * 100:>14,.1f} %")
    print(f"utilisation of the ceiling      : {requests_per_s / ceil:>14.3f}")
    print(f"requests falsely redacted / day : {fp:>14,.1f}")
    print(f"cost of false redactions / day  : {fp * usd_per_false_redaction:>14,.2f} USD")
    print(f"cost of false redactions / month: {fp * usd_per_false_redaction * 30:>14,.2f} USD")
    print(THIN)
    print("မှတ်ချက် - redaction စစ်ဆေးမှု တိုင်းသည် request တိုင်း၏ လမ်းကြောင်းတွင် latency ထည့်သည်၊ "
          "pattern တိုးလျှင် latency linear တိုးသည်၊ false positive သည် အသုံးပြုသူကို "
          "မှားယွင်းစွာ ပိတ်ဆို့သည်။")
    print(RULE)


def print_sweep(requests_per_s: float, workers: int, pattern_count: int, base_ms: float) -> None:
    print(RULE)
    print("lab_redaction_path - check_ms sweep (throughput ceiling နှင့် utilisation)")
    print(f"requests_per_s={requests_per_s:g}  workers={workers}  pattern_count={pattern_count}  "
          f"base_ms={base_ms:g}")
    print(THIN)
    print(f"{'check_ms':>10} {'total_ms':>10} {'added_p95':>11} {'ceiling_req_s':>15} {'utilisation':>13}")
    for c in SWEEP_CHECK_MS:
        tot = total_check_ms(c, pattern_count)
        ceil = ceiling_req_s(c, pattern_count, workers, base_ms)
        print(f"{c:>10.1f} {tot:>10.2f} {added_p95_ms(c, pattern_count):>11.2f} "
              f"{ceil:>15.1f} {requests_per_s / ceil:>13.3f}")
    print(THIN)
    print("မှတ်ချက် - စစ်ဆေးချိန် တိုးလျှင် ceiling ကျဆင်းသည်၊ utilisation တစ်ခုအထက် ရောက်လျှင် "
          "queueing ကြောင့် latency သည် သိသိသာသာ ကြီးထွားသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    args = dict(check_ms=35.0, pattern_count=12.0, workers=8, base_ms=90.0)

    p50 = added_p50_ms(args["check_ms"], args["pattern_count"])
    p95 = added_p95_ms(args["check_ms"], args["pattern_count"])
    ge = p95 >= p50
    print(f"[OK] p95 latency is never below p50 ({p50:.2f} <= {p95:.2f} ms): {ge}")
    ok = ok and ge

    d = total_check_ms(35.0, 24) - total_check_ms(35.0, 12)
    lin = abs(d - 12 * MS_PER_PATTERN) < 1e-9
    print(f"[OK] each extra pattern adds a fixed {MS_PER_PATTERN} ms, 12 more patterns add {d:.2f} ms: {lin}")
    ok = ok and lin

    c1 = ceiling_req_s(35.0, 12, 8, 90.0)
    c2 = ceiling_req_s(70.0, 12, 8, 90.0)
    falls = c2 < c1
    print(f"[OK] doubling the check time lowers the ceiling ({c1:.1f} -> {c2:.1f} req/s): {falls}")
    ok = ok and falls

    f1 = false_per_day(50.0, 0.0005)
    f2 = false_per_day(100.0, 0.0005)
    scales = abs(f2 - 2.0 * f1) < 1e-9
    print(f"[OK] false redactions scale linearly with the request rate ({f1:,.1f} -> {f2:,.1f} per day): {scales}")
    ok = ok and scales

    none = total_check_ms(0.0, 0) == 0.0
    print(f"[OK] with no check and no pattern the added latency is zero: {none}")
    ok = ok and none

    print("[PASS] lab_redaction_path self-test passed." if ok
          else "[FAIL] lab_redaction_path self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Redaction path latency, throughput ceiling and false-redaction cost (offline, deterministic).")
    ap.add_argument("--requests-per-s", type=float, default=50.0)
    ap.add_argument("--check-ms", type=float, default=35.0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--pattern-count", type=int, default=12)
    ap.add_argument("--false-positive-rate", type=float, default=0.0005)
    ap.add_argument("--base-ms", type=float, default=90.0)
    ap.add_argument("--usd-per-false-redaction", type=float, default=0.35)
    ap.add_argument("--sweep", action="store_true", help="check_ms 0..140 sweep")
    ap.add_argument("--self-test", action="store_true", help="assert the real properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.requests_per_s, args.workers, args.pattern_count, args.base_ms)
        return 0
    print_report(args.requests_per_s, args.check_ms, args.workers, args.pattern_count,
                 args.false_positive_rate, args.base_ms, args.usd_per_false_redaction)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
