#!/usr/bin/env python3
"""ex_b_review_budget - ထုတ်လုပ်လိုက်သည့် စာကြောင်း အရေအတွက်အတွက် review budget ကို
သတ်မှတ်ထားသည့် reviewer rate နှင့် defect rate ဖြင့် တွက်ချက်သည် — review minutes၊
queue ၊ လွတ်ထွက်သည့် defect အရေအတွက် နှင့် ကုန်ကျစရိတ် ဖြစ်သည်။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ဖော်မြူလာ —
    review_minutes   = generated_lines / 100 * review_min_per_100
    reviewable_lines = min(generated_lines, capacity / review_min_per_100 * 100)
    queue_minutes    = max(0, review_minutes - capacity)
    defects_generated = generated_lines * defect_rate
    defects_caught    = reviewable_lines * defect_rate * catch_rate
    defects_escaping  = defects_generated - defects_caught

ဤဖိုင်ရှိ ကိန်းဂဏန်း အားလုံးသည် အောက်ပါ ယူဆချက် (assumption) များမှ တွက်ချက်ထားသည်။
"""

from __future__ import annotations

import argparse

RULE = "=" * 74
THIN = "-" * 74

GENERATED_LINES = 1200
REVIEW_MIN_PER_100 = 25.0
DEFECT_RATE = 0.08
REVIEWER_CAPACITY_MIN = 480.0
CATCH_RATE = 0.70
REVIEWER_USD_PER_HOUR = 60.0


def review_minutes(generated_lines: int,
                   review_min_per_100: float = REVIEW_MIN_PER_100) -> float:
    return generated_lines / 100.0 * review_min_per_100


def reviewable_lines(generated_lines: int, capacity_min: float,
                     review_min_per_100: float = REVIEW_MIN_PER_100) -> float:
    by_capacity = capacity_min / review_min_per_100 * 100.0
    return min(float(generated_lines), by_capacity)


def defects(generated_lines: int, reviewed: float,
            defect_rate: float = DEFECT_RATE,
            catch_rate: float = CATCH_RATE) -> tuple[float, float, float]:
    total = generated_lines * defect_rate
    caught = reviewed * defect_rate * catch_rate
    return total, caught, total - caught


def report() -> None:
    minutes = review_minutes(GENERATED_LINES)
    reviewed = reviewable_lines(GENERATED_LINES, REVIEWER_CAPACITY_MIN)
    queue = max(0.0, minutes - REVIEWER_CAPACITY_MIN)
    total, caught, escaping = defects(GENERATED_LINES, reviewed)
    hours = minutes / 60.0
    print(RULE)
    print("ex_b_review_budget - review minutes, queue, escaping defects, cost")
    print(RULE)
    print(f"assumed input : {GENERATED_LINES:,} generated lines, "
          f"review rate {REVIEW_MIN_PER_100:.1f} min per 100 lines")
    print(f"assumed rates : {DEFECT_RATE:.3f} defects per line, "
          f"catch rate {CATCH_RATE:.2f} in reviewed lines")
    print(f"assumed cost  : USD {REVIEWER_USD_PER_HOUR:.2f} per reviewer-hour, "
          f"capacity {REVIEWER_CAPACITY_MIN:,.0f} min")
    print(THIN)
    print(f"review minutes                  : {minutes:>10,.1f}")
    print(f"reviewer capacity (min)         : {REVIEWER_CAPACITY_MIN:>10,.1f}")
    print(f"lines reviewable this period    : {reviewed:>10,.1f}")
    print(f"queue beyond capacity (min)     : {queue:>10,.1f}")
    print(f"defects in generated lines      : {total:>10,.1f}")
    print(f"defects caught in review        : {caught:>10,.1f}")
    print(f"defects escaping                : {escaping:>10,.1f}")
    print(f"review cost (reviewer-hours)    : {hours:>10,.2f}")
    print(f"review cost (USD)               : {hours * REVIEWER_USD_PER_HOUR:>10,.2f}")
    print(THIN)
    print(f"each 100 lines costs {REVIEW_MIN_PER_100:.1f} reviewer-minutes "
          f"= USD {REVIEW_MIN_PER_100 / 60.0 * REVIEWER_USD_PER_HOUR:.2f}")
    print("မှတ်ချက် - review minutes သည် capacity ကို ကျော်လွန်လျှင် queue ဖြစ်ပေါ်ပြီး၊ "
          "စစ်ဆေးမရသည့် စာကြောင်းများမှ defect များ လွတ်ထွက်သည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    m1 = review_minutes(GENERATED_LINES)
    m2 = review_minutes(GENERATED_LINES * 2)
    t1 = abs(m2 - 2.0 * m1) < 1e-9
    print(f"[OK] review minutes scale linearly with generated lines "
          f"({m1:,.1f} -> {m2:,.1f}): {t1}")
    ok = ok and t1

    fits = reviewable_lines(GENERATED_LINES, REVIEWER_CAPACITY_MIN) == GENERATED_LINES
    t2 = fits and max(0.0, m1 - REVIEWER_CAPACITY_MIN) == 0.0
    print(f"[OK] a budget inside capacity leaves an empty queue: {t2}")
    ok = ok and t2

    big = review_minutes(6000)
    over = big > REVIEWER_CAPACITY_MIN
    reviewed_big = reviewable_lines(6000, REVIEWER_CAPACITY_MIN)
    t3 = over and reviewed_big < 6000 and big - REVIEWER_CAPACITY_MIN > 0
    print(f"[OK] a budget beyond capacity builds a queue and drops lines "
          f"({6000 - reviewed_big:,.0f} lines unreviewed): {t3}")
    ok = ok and t3

    _, _, esc_in = defects(GENERATED_LINES,
                           reviewable_lines(GENERATED_LINES, REVIEWER_CAPACITY_MIN))
    _, _, esc_out = defects(6000, reviewable_lines(6000, REVIEWER_CAPACITY_MIN))
    t4 = esc_out > esc_in
    print(f"[OK] more generated lines mean more escaping defects "
          f"({esc_in:,.1f} -> {esc_out:,.1f}): {t4}")
    ok = ok and t4

    _, _, esc_hi = defects(GENERATED_LINES, GENERATED_LINES, defect_rate=0.16)
    _, _, esc_lo = defects(GENERATED_LINES, GENERATED_LINES, defect_rate=0.08)
    t5 = esc_hi > esc_lo
    print(f"[OK] a higher defect rate means more escaping defects "
          f"({esc_lo:,.1f} -> {esc_hi:,.1f}): {t5}")
    ok = ok and t5

    print("[PASS] ex_b_review_budget self-test passed." if ok
          else "[FAIL] ex_b_review_budget self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Review budget for generated lines (offline, deterministic).")
    ap.add_argument("--self-test", action="store_true", help="assert the budget properties")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
