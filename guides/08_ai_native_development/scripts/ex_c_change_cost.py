#!/usr/bin/env python3
"""ex_c_change_cost - သတ်မှတ်ထားသည့် success rate ဖြင့် retry များ ပါဝင်သည့်
cost per merged change ကို တွက်ချက်သည်။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ဖော်မြူလာ (p = success-rate, A = attempts cap) —
    expected_attempts = sum_{k=1..A} (1 - p)^(k-1)
    success_prob      = 1 - (1 - p)^A
    merged_changes    = tasks * success_prob
    total_attempts    = tasks * expected_attempts
    cost_per_attempt  = tokens_per_attempt/Mtok * price + attempt_minutes/60 * repo_hour_cost
    cost_per_merged   = total_attempts * cost_per_attempt / merged_changes

ဤဖိုင်ရှိ ကိန်းဂဏန်း အားလုံးသည် အောက်ပါ ယူဆချက် (assumption) များမှ တွက်ချက်ထားသည်။
"""

from __future__ import annotations

import argparse

RULE = "=" * 74
THIN = "-" * 74
MTOK = 1_000_000.0

TASKS = 100
ATTEMPTS = 4
SUCCESS_RATE = 0.62
TOKENS_PER_ATTEMPT = 9000
PRICE_PER_MTOK = 3.00
REPO_HOUR_COST = 45.00
ATTEMPT_MINUTES = 6.0


def expected_attempts(success_rate: float, attempts: int) -> float:
    return sum((1.0 - success_rate) ** (k - 1) for k in range(1, attempts + 1))


def success_probability(success_rate: float, attempts: int) -> float:
    return 1.0 - (1.0 - success_rate) ** attempts


def cost_per_attempt(tokens_per_attempt: int = TOKENS_PER_ATTEMPT,
                     price_per_mtok: float = PRICE_PER_MTOK,
                     repo_hour_cost: float = REPO_HOUR_COST,
                     attempt_minutes: float = ATTEMPT_MINUTES) -> tuple[float, float, float]:
    tokens = tokens_per_attempt / MTOK * price_per_mtok
    wall = attempt_minutes / 60.0 * repo_hour_cost
    return tokens, wall, tokens + wall


def report() -> None:
    exp = expected_attempts(SUCCESS_RATE, ATTEMPTS)
    prob = success_probability(SUCCESS_RATE, ATTEMPTS)
    merged = TASKS * prob
    total_attempts = TASKS * exp
    tok_cost, wall_cost, per_attempt = cost_per_attempt()
    total = total_attempts * per_attempt
    print(RULE)
    print("ex_c_change_cost - cost per merged change including retries")
    print(RULE)
    print(f"assumed work  : {TASKS} tasks, attempt cap {ATTEMPTS}, "
          f"success rate {SUCCESS_RATE:.3f} per attempt")
    print(f"assumed usage : {TOKENS_PER_ATTEMPT:,} tokens per attempt, "
          f"USD {PRICE_PER_MTOK:.2f} per 1M tokens")
    print(f"assumed infra : USD {REPO_HOUR_COST:.2f} per repo-hour, "
          f"{ATTEMPT_MINUTES:.1f} minutes per attempt")
    print(THIN)
    print(f"cost per attempt (tokens)       : USD {tok_cost:>8.4f}")
    print(f"cost per attempt (wall-clock)   : USD {wall_cost:>8.4f}")
    print(f"cost per attempt (total)        : USD {per_attempt:>8.4f}")
    print(f"expected attempts per task      : {exp:>12.4f}")
    print(f"success probability per task    : {prob:>12.4f}")
    print(f"retries beyond first attempt     : {total_attempts - TASKS:>12.2f}")
    print(f"merged changes                  : {merged:>12.2f}")
    print(f"total cost                      : USD {total:>8.2f}")
    print(f"cost per merged change          : USD {total / merged:>8.4f}")
    print(THIN)
    print(f"cost per merged change is {total / merged / per_attempt:.3f}x "
          f"the cost of a single attempt")
    print("မှတ်ချက် - success rate နိမ့်လျှင် retry အရေအတွက် တိုးပြီး၊ "
          "merged change တစ်ခုလျှင် ကုန်ကျစရိတ် မြင့်သည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    t1, w1, a1 = cost_per_attempt()
    t2, _, a2 = cost_per_attempt(tokens_per_attempt=TOKENS_PER_ATTEMPT * 2)
    t2b, _, _ = cost_per_attempt(price_per_mtok=PRICE_PER_MTOK * 2)
    lin = abs((t2 - t1) - t1) < 1e-9 and abs((t2b - t1) - t1) < 1e-9
    print(f"[OK] the token part of cost per attempt scales linearly with tokens and price: {lin}")
    ok = ok and lin

    lo = expected_attempts(0.80, ATTEMPTS)
    hi = expected_attempts(0.40, ATTEMPTS)
    t2ok = hi > lo > 1.0
    print(f"[OK] a lower success rate needs more attempts ({lo:.4f} -> {hi:.4f}): {t2ok}")
    ok = ok and t2ok

    _, _, per = cost_per_attempt()
    exp = expected_attempts(SUCCESS_RATE, ATTEMPTS)
    prob = success_probability(SUCCESS_RATE, ATTEMPTS)
    cpm = TASKS * exp * per / (TASKS * prob)
    t3 = cpm >= per
    print(f"[OK] cost per merged change is never below cost per attempt "
          f"({cpm:.4f} >= {per:.4f}): {t3}")
    ok = ok and t3

    higher = expected_attempts(SUCCESS_RATE, ATTEMPTS + 2)
    t4 = higher > exp and success_probability(SUCCESS_RATE, ATTEMPTS + 2) > prob
    print(f"[OK] raising the attempt cap raises both attempts and success probability "
          f"({exp:.4f} -> {higher:.4f}): {t4}")
    ok = ok and t4

    t5 = (TASKS * exp - TASKS) > 0
    print(f"[OK] retries beyond the first attempt are positive "
          f"({TASKS * exp - TASKS:,.2f}): {t5}")
    ok = ok and t5

    print("[PASS] ex_c_change_cost self-test passed." if ok
          else "[FAIL] ex_c_change_cost self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Cost per merged change including retries (offline, deterministic).")
    ap.add_argument("--self-test", action="store_true", help="assert the cost properties")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
