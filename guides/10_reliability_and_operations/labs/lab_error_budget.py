#!/usr/bin/env python3
"""lab_error_budget - SLO မှ ဆင်းသက်လာသည့် error budget၊ burn rate၊ ကုန်ဆုံးချိန် နှင့်
alert threshold များကို စမ်းသပ်သည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

ပုံသေနည်း —
    allowed_failure_ratio = 1 - slo
    budget_requests = allowed_failure_ratio * requests_per_day * window_days
    request_rate    = requests_per_day / 86400
    budget_minutes  = budget_requests / request_rate / 60      (100% failure ဖြစ်ပါက)
    burn_rate       = observed_failure_rate / allowed_failure_ratio
    time_to_exhaust = window_days / burn_rate
    burn rate b သည် window ၏ b ပုံတစ်ပုံအတွင်း budget တစ်ခုလုံးကို ကုန်စေသည်။
"""

from __future__ import annotations

import argparse

RULE = "=" * 74
THIN = "-" * 74
SECONDS_PER_DAY = 86400.0
BUDGETS = ((14.4, 1.0 / 24.0), (6.0, 6.0 / 24.0), (1.0, 3.0))


def budget_requests(slo_percent: float, requests_per_day: float, window_days: float) -> float:
    return (1.0 - slo_percent / 100.0) * requests_per_day * window_days


def burn_rate(failure_rate: float, slo_percent: float) -> float:
    return failure_rate / (1.0 - slo_percent / 100.0)


def print_report(args: argparse.Namespace) -> None:
    allowed = 1.0 - args.slo_percent / 100.0
    total = args.requests_per_day * args.window_days
    budget = budget_requests(args.slo_percent, args.requests_per_day, args.window_days)
    rate = args.requests_per_day / SECONDS_PER_DAY
    budget_minutes = budget / rate / 60.0
    burn = burn_rate(args.failure_rate, args.slo_percent)
    observed = args.failure_rate * total
    print(RULE)
    print("lab_error_budget - error budget, burn rate နှင့် alert threshold (offline, deterministic)")
    print(f"slo={args.slo_percent:.3f}%  requests/day={args.requests_per_day:,.0f}  "
          f"window={args.window_days:.0f} days  failure-rate={args.failure_rate * 100:.4f}%")
    print(THIN)
    print(f"  total requests in window    : {total:>14,.0f}")
    print(f"  allowed failure ratio       : {allowed:>14.6f}")
    print(f"  error budget (requests)     : {budget:>14,.0f}")
    print(f"  request rate                : {rate:>14.2f} req/s")
    print(f"  error budget (minutes)      : {budget_minutes:>14.2f} min at 100% failure")
    print(THIN)
    print(f"  observed failures in window : {observed:>14,.0f}")
    print(f"  burn rate                   : {burn:>14.4f}x")
    print(f"  time to exhaust the budget  : {args.window_days / burn:>14.2f} days")
    print(THIN)
    print("alert thresholds (multiwindow, Google SRE style):")
    print(f"{'burn rate':>10} {'window':>9} {'budget share':>13} {'exhausts in':>13}")
    for b, window_days in BUDGETS:
        share = b * window_days / args.window_days
        print(f"{b:>10.1f} {window_days * 24:>7.0f} h {share * 100:>12.1f}% "
              f"{args.window_days / b:>10.2f} d")
    print(THIN)
    print("မှတ်ချက် - error budget သည် incident ဖြစ်ပေါ်စေရန် ခွဲတမ်း မဟုတ်ပါ။ ၎င်းသည် SLO မှ "
          "ဆင်းသက်လာသည့် ဆုံးဖြတ်ချက် နယ်နိမိတ် ဖြစ်သည်၊ ကျန်ရှိသည့် budget အတွင်း release "
          "လုပ်ဆောင်နိုင်ပြီး ကုန်ဆုံးလျှင် ပြောင်းလဲမှုကို ရပ်ရမည်။")
    print(RULE)


def print_sweep(args: argparse.Namespace) -> None:
    print(RULE)
    print("lab_error_budget - SLO sweep 99.0 .. 99.99% (requests/day %.0f, window %.0f days)"
          % (args.requests_per_day, args.window_days))
    print(f"{'slo %':>8} {'allowed %':>10} {'budget req':>13} {'budget min':>11} "
          f"{'burn rate':>10} {'exhaust days':>13}")
    rate = args.requests_per_day / SECONDS_PER_DAY
    for slo in (99.0, 99.5, 99.9, 99.95, 99.99):
        budget = budget_requests(slo, args.requests_per_day, args.window_days)
        burn = burn_rate(args.failure_rate, slo)
        print(f"{slo:>8.2f} {(1 - slo / 100) * 100:>9.3f}% {budget:>13,.0f} "
              f"{budget / rate / 60:>11.2f} {burn:>10.4f} {args.window_days / burn:>13.2f}")
    print(THIN)
    print("မှတ်ချက် - SLO တိုးလျှင် budget သည် အတိအကျ ကျဆင်းသည်၊ တူညီသည့် failure rate တွင် "
          "burn rate တိုးပြီး ကုန်ဆုံးချိန် တိုသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    slo, rpd, window, fr = 99.9, 1000000.0, 30.0, 0.0005
    total = rpd * window
    budget = budget_requests(slo, rpd, window)

    exact = abs(budget - 0.001 * total) < 1e-3
    print(f"[OK] the budget is exactly (1 - SLO) of the window's requests "
          f"({budget:,.0f} of {total:,.0f}): {exact}")
    ok = ok and exact

    tighter = budget_requests(99.99, rpd, window) < budget_requests(99.0, rpd, window)
    print(f"[OK] a tighter SLO shrinks the budget "
          f"({budget_requests(99.99, rpd, window):,.0f} < {budget_requests(99.0, rpd, window):,.0f}): {tighter}")
    ok = ok and tighter

    rate = rpd / SECONDS_PER_DAY
    minutes = budget / rate / 60.0
    minutes_ok = abs(minutes - 43.2) < 0.01
    print(f"[OK] the budget expressed in minutes of 100% failure "
          f"({minutes:.2f} min at {rate:.2f} req/s): {minutes_ok}")
    ok = ok and minutes_ok

    burn = burn_rate(fr, slo)
    burn_ok = abs(burn - 0.5) < 1e-12
    print(f"[OK] burn rate = observed failure rate / allowed failure rate ({burn:.4f}x): {burn_ok}")
    ok = ok and burn_ok

    exhaust = window / burn
    exhaust_ok = abs(exhaust - 60.0) < 1e-9
    print(f"[OK] time to exhaust = window / burn rate ({exhaust:.2f} days): {exhaust_ok}")
    ok = ok and exhaust_ok

    burn_high = burn_rate(0.005, slo)
    faster = burn_high > 1.0 and window / burn_high < window
    print(f"[OK] a failure rate above the allowance burns faster than the window "
          f"(burn {burn_high:.2f}x, exhausts in {window / burn_high:.2f} days): {faster}")
    ok = ok and faster

    share = 14.4 * (1.0 / 24.0) / window
    share_ok = abs(share - 0.02) < 1e-12
    print(f"[OK] the 14.4x / 1 h alert fires after {share * 100:.2f}% of the budget is burned: {share_ok}")
    ok = ok and share_ok

    print("[PASS] lab_error_budget self-test passed." if ok else "[FAIL] lab_error_budget self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Error budget lab (offline, deterministic).")
    ap.add_argument("--slo-percent", type=float, default=99.9)
    ap.add_argument("--requests-per-day", type=float, default=1000000.0)
    ap.add_argument("--window-days", type=float, default=30.0)
    ap.add_argument("--failure-rate", type=float, default=0.0005, help="observed failure ratio")
    ap.add_argument("--sweep", action="store_true", help="SLO 99.0 .. 99.99% sweep")
    ap.add_argument("--self-test", action="store_true", help="assert the real budget properties")
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
