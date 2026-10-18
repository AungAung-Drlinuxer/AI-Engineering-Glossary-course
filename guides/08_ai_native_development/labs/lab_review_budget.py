#!/usr/bin/env python3
"""lab_review_budget - ထုတ်လုပ်လိုက်သည့် စာကြောင်းများအတွက် review budget ကို တွက်သည်။

review minutes၊ reviewer capacity နှင့် နှိုင်းယှဉ်သည့် queue၊ သတ်မှတ်ထားသည့် defect rate
အရ လွတ်ထွက်သည့် defect အရေအတွက် နှင့် ကုန်ကျစရိတ်ကို ပြသည်။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ဖော်မြူလာ —
    review_minutes    = generated_lines / 100 * review_min_per_100
    reviewable_lines  = min(generated_lines, capacity_min / review_min_per_100 * 100)
    queue_minutes     = max(0, review_minutes - capacity_min)
    defects_escaping  = generated_lines * defect_rate
                        - reviewable_lines * defect_rate * catch_rate
"""

from __future__ import annotations

import argparse

RULE = "=" * 74
THIN = "-" * 74

DEFAULT_GENERATED_LINES = 1200
DEFAULT_REVIEW_MIN_PER_100 = 25.0
DEFAULT_DEFECT_RATE = 0.08
DEFAULT_REVIEWER_CAPACITY_MIN = 480.0

# ယူဆချက် (assumption) များ — ဤတန်ဖိုးများသည် အခြေအနေအလိုက် ကွာခြားသည်။
CATCH_RATE = 0.70
REVIEWER_USD_PER_HOUR = 60.0
SWEEP_LINES = (300, 600, 1200, 2400, 4800, 9600)


def review_minutes(generated_lines: int, review_min_per_100: float) -> float:
    return generated_lines / 100.0 * review_min_per_100


def reviewable_lines(generated_lines: int, capacity_min: float,
                     review_min_per_100: float) -> float:
    return min(float(generated_lines),
               capacity_min / review_min_per_100 * 100.0)


def report(generated_lines: int, review_min_per_100: float, defect_rate: float,
           capacity_min: float) -> None:
    minutes = review_minutes(generated_lines, review_min_per_100)
    reviewed = reviewable_lines(generated_lines, capacity_min, review_min_per_100)
    queue = max(0.0, minutes - capacity_min)
    total_defects = generated_lines * defect_rate
    caught = reviewed * defect_rate * CATCH_RATE
    escaping = total_defects - caught
    hours = minutes / 60.0
    print(RULE)
    print("lab_review_budget - review minutes, queue, escaping defects, cost")
    print(f"generated-lines={generated_lines:,}  "
          f"review-min-per-100={review_min_per_100:.1f}  "
          f"defect-rate={defect_rate:.3f}  capacity={capacity_min:,.0f} min")
    print(f"assumption - reviewer catches {CATCH_RATE * 100:.0f}% of defects in reviewed "
          f"lines; reviewer cost USD {REVIEWER_USD_PER_HOUR:.2f}/hour (assumed).")
    print(THIN)
    print(f"review minutes                   : {minutes:>10,.1f}")
    print(f"reviewer capacity (min)          : {capacity_min:>10,.1f}")
    print(f"lines reviewable this period     : {reviewed:>10,.1f}")
    print(f"queue beyond capacity (min)      : {queue:>10,.1f}")
    print(f"defects in generated lines       : {total_defects:>10,.1f}")
    print(f"defects caught in review         : {caught:>10,.1f}")
    print(f"defects escaping                 : {escaping:>10,.1f}")
    print(f"review cost (reviewer-hours)     : {hours:>10,.2f}")
    print(f"review cost (USD, assumed)       : {hours * REVIEWER_USD_PER_HOUR:>10,.2f}")
    print(THIN)
    print(f"review cost per 100 lines = USD "
          f"{review_min_per_100 / 60.0 * REVIEWER_USD_PER_HOUR:.2f} "
          f"(assumed rate {REVIEWER_USD_PER_HOUR:.2f}/hour)")
    print("မှတ်ချက် - review minutes သည် capacity ကို ကျော်လွန်လျှင် queue ဖြစ်ပေါ်ပြီး၊ "
          "စစ်ဆေးမရသည့် စာကြောင်းများမှ defect များ လွတ်ထွက်သည်။")
    print(RULE)


def sweep(review_min_per_100: float, defect_rate: float, capacity_min: float) -> None:
    print(RULE)
    print("lab_review_budget --sweep : generated-lines အလိုက် queue နှင့် လွတ်ထွက်မှု")
    print(f"review-min-per-100={review_min_per_100:.1f}  defect-rate={defect_rate:.3f}  "
          f"capacity={capacity_min:,.0f} min")
    print(f"assumption - catch rate {CATCH_RATE * 100:.0f}% in reviewed lines")
    print(THIN)
    print(f"{'generated-lines':>15}{'review min':>12}{'queue min':>11}"
          f"{'reviewable':>12}{'escaping':>11}")
    for lines in SWEEP_LINES:
        minutes = review_minutes(lines, review_min_per_100)
        reviewed = reviewable_lines(lines, capacity_min, review_min_per_100)
        escaping = lines * defect_rate - reviewed * defect_rate * CATCH_RATE
        print(f"{lines:>15,}{minutes:>12,.1f}{max(0.0, minutes - capacity_min):>11,.1f}"
              f"{reviewed:>12,.1f}{escaping:>11,.1f}")
    print("မှတ်ချက် - generated-lines တိုးလျှင် queue နှင့် လွတ်ထွက်သည့် defect တိုးသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    m1 = review_minutes(DEFAULT_GENERATED_LINES, DEFAULT_REVIEW_MIN_PER_100)
    m2 = review_minutes(DEFAULT_GENERATED_LINES * 2, DEFAULT_REVIEW_MIN_PER_100)
    t1 = abs(m2 - 2.0 * m1) < 1e-9
    print(f"[OK] review minutes scale linearly with generated lines "
          f"({m1:,.1f} -> {m2:,.1f}): {t1}")
    ok = ok and t1

    reviewed = reviewable_lines(DEFAULT_GENERATED_LINES, DEFAULT_REVIEWER_CAPACITY_MIN,
                                DEFAULT_REVIEW_MIN_PER_100)
    t2 = reviewed == DEFAULT_GENERATED_LINES and m1 <= DEFAULT_REVIEWER_CAPACITY_MIN
    print(f"[OK] a budget inside capacity is fully reviewable with no queue: {t2}")
    ok = ok and t2

    big = 6000
    big_min = review_minutes(big, DEFAULT_REVIEW_MIN_PER_100)
    big_reviewed = reviewable_lines(big, DEFAULT_REVIEWER_CAPACITY_MIN,
                                    DEFAULT_REVIEW_MIN_PER_100)
    t3 = big_min > DEFAULT_REVIEWER_CAPACITY_MIN and big_reviewed < big
    print(f"[OK] a budget beyond capacity drops lines "
          f"({big - big_reviewed:,.0f} unreviewed, queue "
          f"{big_min - DEFAULT_REVIEWER_CAPACITY_MIN:,.1f} min): {t3}")
    ok = ok and t3

    esc_small = (DEFAULT_GENERATED_LINES * DEFAULT_DEFECT_RATE
                 - reviewed * DEFAULT_DEFECT_RATE * CATCH_RATE)
    esc_big = big * DEFAULT_DEFECT_RATE - big_reviewed * DEFAULT_DEFECT_RATE * CATCH_RATE
    t4 = esc_big > esc_small > 0
    print(f"[OK] more generated lines mean more escaping defects "
          f"({esc_small:,.1f} -> {esc_big:,.1f}): {t4}")
    ok = ok and t4

    esc_hi = (DEFAULT_GENERATED_LINES * 0.16
              - reviewed * 0.16 * CATCH_RATE)
    t5 = esc_hi > esc_small
    print(f"[OK] a higher defect rate means more escaping defects "
          f"({esc_small:,.1f} -> {esc_hi:,.1f}): {t5}")
    ok = ok and t5

    t6 = abs(review_minutes(200, 25.0) / 60.0 * REVIEWER_USD_PER_HOUR - 50.0) < 1e-9
    print(f"[OK] review cost follows the review minutes at the assumed rate: {t6}")
    ok = ok and t6

    print("[PASS] lab_review_budget self-test passed." if ok
          else "[FAIL] lab_review_budget self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Review budget, queue and escaping defects (offline, deterministic).")
    ap.add_argument("--generated-lines", type=int, default=DEFAULT_GENERATED_LINES)
    ap.add_argument("--review-min-per-100", type=float, default=DEFAULT_REVIEW_MIN_PER_100)
    ap.add_argument("--defect-rate", type=float, default=DEFAULT_DEFECT_RATE)
    ap.add_argument("--reviewer-capacity-min", type=float,
                    default=DEFAULT_REVIEWER_CAPACITY_MIN)
    ap.add_argument("--sweep", action="store_true", help="vary generated lines across a range")
    ap.add_argument("--self-test", action="store_true", help="assert the review properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        sweep(args.review_min_per_100, args.defect_rate, args.reviewer_capacity_min)
        return 0
    report(args.generated_lines, args.review_min_per_100,
           args.defect_rate, args.reviewer_capacity_min)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
