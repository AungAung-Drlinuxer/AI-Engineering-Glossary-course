#!/usr/bin/env python3
"""lab_change_cost - retry များ ပါဝင်သည့် cost per merged change ကို တွက်သည်။

သတ်မှတ်ထားသည့် success rate အောက်တွင် လုပ်ငန်း တစ်ခုလျှင် လိုအပ်သည့် attempt အရေအတွက်၊
retry အရေအတွက်၊ merged change တစ်ခုလျှင် ကုန်ကျစရိတ် နှင့် စုစုပေါင်း ကုန်ကျစရိတ်ကို ပြသည်။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ဖော်မြူလာ (p = success-rate, A = attempts cap) —
    expected_attempts = sum_{k=1..A} (1 - p)^(k-1)
    success_prob      = 1 - (1 - p)^A
    merged_changes    = tasks * success_prob
    cost_per_attempt  = tokens_per_attempt/1e6 * price_per_mtok
                        + attempt_minutes/60 * repo_hour_cost
"""

from __future__ import annotations

import argparse

RULE = "=" * 74
THIN = "-" * 74
MTOK = 1_000_000.0

DEFAULT_TASKS = 100
DEFAULT_ATTEMPTS = 4
DEFAULT_SUCCESS_RATE = 0.62
DEFAULT_TOKENS_PER_ATTEMPT = 9000
DEFAULT_PRICE_PER_MTOK = 3.00
DEFAULT_REPO_HOUR_COST = 45.00

# ယူဆချက် (assumption) — attempt တစ်ခုစီသည် repo အချိန် သတ်မှတ်ချက် ကုန်သည်ဟု ယူသည်။
ATTEMPT_MINUTES = 6.0
SWEEP_SUCCESS_RATES = (0.30, 0.45, 0.62, 0.75, 0.90)


def expected_attempts(success_rate: float, attempts: int) -> float:
    return sum((1.0 - success_rate) ** (k - 1) for k in range(1, attempts + 1))


def success_probability(success_rate: float, attempts: int) -> float:
    return 1.0 - (1.0 - success_rate) ** attempts


def cost_per_attempt(tokens_per_attempt: float, price_per_mtok: float,
                     repo_hour_cost: float) -> tuple[float, float, float]:
    tokens = tokens_per_attempt / MTOK * price_per_mtok
    wall = ATTEMPT_MINUTES / 60.0 * repo_hour_cost
    return tokens, wall, tokens + wall


def report(tasks: int, attempts: int, success_rate: float,
           tokens_per_attempt: float, price_per_mtok: float,
           repo_hour_cost: float) -> None:
    exp = expected_attempts(success_rate, attempts)
    prob = success_probability(success_rate, attempts)
    merged = tasks * prob
    total_attempts = tasks * exp
    tok_cost, wall_cost, per_attempt = cost_per_attempt(
        tokens_per_attempt, price_per_mtok, repo_hour_cost)
    total = total_attempts * per_attempt
    print(RULE)
    print("lab_change_cost - cost per merged change with retries (offline, deterministic)")
    print(f"tasks={tasks:,}  attempts={attempts}  success-rate={success_rate:.3f}  "
          f"tokens-per-attempt={tokens_per_attempt:,.0f}  "
          f"price=USD {price_per_mtok:.2f}/Mtok  repo-hour=USD {repo_hour_cost:.2f}")
    print(f"assumption - each attempt consumes {ATTEMPT_MINUTES:.1f} minutes "
          f"of repo wall-clock time.")
    print(THIN)
    print(f"cost per attempt (tokens)        : USD {tok_cost:>8.4f}")
    print(f"cost per attempt (wall-clock)    : USD {wall_cost:>8.4f}")
    print(f"cost per attempt (total)         : USD {per_attempt:>8.4f}")
    print(f"expected attempts per task       : {exp:>12.4f}")
    print(f"success probability per task     : {prob:>12.4f}")
    print(f"retries beyond first attempt      : {total_attempts - tasks:>12.2f}")
    print(f"merged changes                   : {merged:>12.2f}")
    print(f"cost per merged change           : USD {total / merged:>8.4f}")
    print(f"total cost                       : USD {total:>8.2f}")
    print(THIN)
    print(f"a failed attempt costs USD {per_attempt:.4f} and yields nothing until it "
          f"succeeds; the multiplier is {total / merged / per_attempt:.3f}x")
    print("မှတ်ချက် - success rate နိမ့်လျှင် retry အရေအတွက် တိုးပြီး၊ merged change "
          "တစ်ခုလျှင် ကုန်ကျစရိတ် မြင့်သည်။")
    print(RULE)


def sweep(tasks: int, attempts: int, tokens_per_attempt: float,
          price_per_mtok: float, repo_hour_cost: float) -> None:
    print(RULE)
    print("lab_change_cost --sweep : success-rate အလိုက် retry နှင့် ကုန်ကျစရိတ်")
    print(f"tasks={tasks:,}  attempts cap={attempts}  "
          f"assumption - {ATTEMPT_MINUTES:.1f} minutes per attempt")
    print(THIN)
    print(f"{'success-rate':>13}{'expected attempts':>19}{'merged':>10}"
          f"{'USD / merged change':>22}")
    for p in SWEEP_SUCCESS_RATES:
        exp = expected_attempts(p, attempts)
        prob = success_probability(p, attempts)
        merged = tasks * prob
        _, _, per_attempt = cost_per_attempt(tokens_per_attempt, price_per_mtok, repo_hour_cost)
        cpm = tasks * exp * per_attempt / merged
        print(f"{p:>13.2f}{exp:>19.4f}{merged:>10,.1f}{cpm:>22.4f}")
    print("မှတ်ချက် - success-rate တိုးလျှင် cost per merged change ကျဆင်းသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    tok, wall, per = cost_per_attempt(DEFAULT_TOKENS_PER_ATTEMPT,
                                      DEFAULT_PRICE_PER_MTOK, DEFAULT_REPO_HOUR_COST)
    t1 = abs(tok - DEFAULT_TOKENS_PER_ATTEMPT / MTOK * DEFAULT_PRICE_PER_MTOK) < 1e-12
    t2 = abs(wall - ATTEMPT_MINUTES / 60.0 * DEFAULT_REPO_HOUR_COST) < 1e-12
    t3 = abs(per - (tok + wall)) < 1e-12
    print(f"[OK] cost per attempt = token cost + wall-clock cost "
          f"(USD {tok:.4f} + {wall:.4f} = {per:.4f}): {t1 and t2 and t3}")
    ok = ok and t1 and t2 and t3

    tok2, _, _ = cost_per_attempt(DEFAULT_TOKENS_PER_ATTEMPT * 3,
                                  DEFAULT_PRICE_PER_MTOK, DEFAULT_REPO_HOUR_COST)
    t4 = abs(tok2 - 3.0 * tok) < 1e-9
    print(f"[OK] the token part scales linearly with tokens-per-attempt: {t4}")
    ok = ok and t4

    lo = expected_attempts(0.80, DEFAULT_ATTEMPTS)
    hi = expected_attempts(0.40, DEFAULT_ATTEMPTS)
    t5 = hi > lo > 1.0
    print(f"[OK] a lower success rate needs more attempts ({lo:.4f} -> {hi:.4f}): {t5}")
    ok = ok and t5

    exp = expected_attempts(DEFAULT_SUCCESS_RATE, DEFAULT_ATTEMPTS)
    prob = success_probability(DEFAULT_SUCCESS_RATE, DEFAULT_ATTEMPTS)
    cpm = DEFAULT_TASKS * exp * per / (DEFAULT_TASKS * prob)
    t6 = cpm >= per
    print(f"[OK] cost per merged change is never below cost per attempt "
          f"({cpm:.4f} >= {per:.4f}): {t6}")
    ok = ok and t6

    t7 = success_probability(DEFAULT_SUCCESS_RATE, DEFAULT_ATTEMPTS + 2) > prob
    print(f"[OK] raising the attempt cap raises success probability "
          f"({prob:.4f} -> {success_probability(DEFAULT_SUCCESS_RATE, DEFAULT_ATTEMPTS + 2):.4f}): {t7}")
    ok = ok and t7

    t8 = DEFAULT_TASKS * exp - DEFAULT_TASKS > 0
    print(f"[OK] retries beyond the first attempt are positive "
          f"({DEFAULT_TASKS * exp - DEFAULT_TASKS:,.2f}): {t8}")
    ok = ok and t8

    print("[PASS] lab_change_cost self-test passed." if ok
          else "[FAIL] lab_change_cost self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Cost per merged change including retries (offline, deterministic).")
    ap.add_argument("--tasks", type=int, default=DEFAULT_TASKS)
    ap.add_argument("--attempts", type=int, default=DEFAULT_ATTEMPTS)
    ap.add_argument("--success-rate", type=float, default=DEFAULT_SUCCESS_RATE)
    ap.add_argument("--tokens-per-attempt", type=float, default=DEFAULT_TOKENS_PER_ATTEMPT)
    ap.add_argument("--price-per-mtok", type=float, default=DEFAULT_PRICE_PER_MTOK)
    ap.add_argument("--repo-hour-cost", type=float, default=DEFAULT_REPO_HOUR_COST)
    ap.add_argument("--sweep", action="store_true", help="vary success-rate across a range")
    ap.add_argument("--self-test", action="store_true", help="assert the cost properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        sweep(args.tasks, args.attempts, args.tokens_per_attempt,
              args.price_per_mtok, args.repo_hour_cost)
        return 0
    report(args.tasks, args.attempts, args.success_rate, args.tokens_per_attempt,
           args.price_per_mtok, args.repo_hour_cost)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
