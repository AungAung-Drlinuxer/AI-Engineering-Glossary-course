#!/usr/bin/env python3
"""ex_a_guardrail_cost - request path တွင် guardrail သို့မဟုတ် redaction အဆင့် တစ်ခု ထည့်ခြင်း၏
latency နှင့် throughput ကုန်ကျစရိတ်ကို တွက်ချက်သည်။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ပုံသေနည်း
    total_check_ms = base_check_ms + pattern_count * ms_per_pattern
    added_p50_ms   = total_check_ms
    added_p95_ms   = total_check_ms * p95_factor
    ceiling_req_s  = workers / ((base_service_ms + total_check_ms) / 1000)
    utilisation    = requests_per_s / ceiling_req_s
    false_redactions_per_day = requests_per_s * 86400 * false_positive_rate
    false_redaction_cost_per_day = false_redactions_per_day * cost_per_false_redaction

ယူဆချက် အားလုံးကို output တွင် (assumption) ဟု မှတ်သားထားသည်။
"""

from __future__ import annotations

RULE = "=" * 102
THIN = "-" * 102

MS_PER_PATTERN = 0.15
P95_FACTOR = 1.8
SECONDS_PER_DAY = 86400.0

REQUESTS_PER_S = 120.0
WORKERS = 32
BASE_SERVICE_MS = 90.0
PATTERN_COUNT = 12
FALSE_POSITIVE_RATE = 0.004
COST_PER_FALSE_REDACTION = 0.35

TIERS = [
    ("regex redaction only", 0.0),
    ("regex + small classifier", 12.0),
    ("regex + classifier + judge", 145.0),
]


def total_check_ms(base_check_ms: float, pattern_count: int) -> float:
    """guardrail အဆင့်တစ်ခု၏ စုစုပေါင်း စစ်ဆေးချိန် (ms)။"""
    return base_check_ms + pattern_count * MS_PER_PATTERN


def added_p50_ms(base_check_ms: float, pattern_count: int) -> float:
    return total_check_ms(base_check_ms, pattern_count)


def added_p95_ms(base_check_ms: float, pattern_count: int) -> float:
    return total_check_ms(base_check_ms, pattern_count) * P95_FACTOR


def ceiling_req_s(base_check_ms: float, pattern_count: int, workers: int,
                  base_service_ms: float) -> float:
    """request တစ်ခုလျှင် base service နှင့် guardrail စစ်ဆေးချိန် နှစ်ခုလုံး ပါဝင်သည့် ceiling။"""
    return workers / ((base_service_ms + total_check_ms(base_check_ms, pattern_count)) / 1000.0)


def false_redactions_per_day(requests_per_s: float, false_positive_rate: float) -> float:
    return requests_per_s * SECONDS_PER_DAY * false_positive_rate


def main() -> int:
    baseline = WORKERS / (BASE_SERVICE_MS / 1000.0)
    fpd = false_redactions_per_day(REQUESTS_PER_S, FALSE_POSITIVE_RATE)
    print(RULE)
    print("ex_a_guardrail_cost - guardrail / redaction အဆင့် တစ်ခု၏ latency နှင့် throughput ကုန်ကျစရိတ်")
    print(f"(assumption) requests_per_s={REQUESTS_PER_S:.0f}  workers={WORKERS}  "
          f"base_service_ms={BASE_SERVICE_MS:.1f}  pattern_count={PATTERN_COUNT}")
    print(f"(assumption) ms_per_pattern={MS_PER_PATTERN}  p95_factor={P95_FACTOR}  "
          f"false_positive_rate={FALSE_POSITIVE_RATE}  "
          f"usd_per_false_redaction={COST_PER_FALSE_REDACTION}")
    print(THIN)
    print(f"{'Guardrail tier':<26} {'check_ms':>9} {'added_p50':>10} {'added_p95':>10} "
          f"{'ceiling_req_s':>14} {'vs_base':>8} {'false/day':>10} {'usd/day':>8}")
    for name, base_check in TIERS:
        c = total_check_ms(base_check, PATTERN_COUNT)
        p50 = added_p50_ms(base_check, PATTERN_COUNT)
        p95 = added_p95_ms(base_check, PATTERN_COUNT)
        ceil = ceiling_req_s(base_check, PATTERN_COUNT, WORKERS, BASE_SERVICE_MS)
        print(f"{name:<26} {c:>9.2f} {p50:>10.2f} {p95:>10.2f} {ceil:>14.1f} "
              f"{ceil / baseline:>8.3f} {fpd:>10,.1f} {fpd * COST_PER_FALSE_REDACTION:>8.2f}")
    print(THIN)
    print(f"baseline ceiling with no guardrail at all = {baseline:.1f} req/s "
          f"(workers={WORKERS}, base_service_ms={BASE_SERVICE_MS:.1f})")
    print(f"false redactions per day = {REQUESTS_PER_S:.0f} req/s * 86400 s * {FALSE_POSITIVE_RATE} "
          f"= {fpd:,.1f} requests, cost {fpd * COST_PER_FALSE_REDACTION:,.2f} USD/day")
    print("မှတ်ချက် - guardrail အဆင့် တစ်ခုစီသည် request တိုင်း၏ လမ်းကြောင်းတွင် latency ထည့်သည်၊ "
          "ceiling သည် worker အရေအတွက်ကို request တစ်ခုလျှင် ကုန်သည့် အချိန်ဖြင့် စားသည့် တန်ဖိုး ဖြစ်သည်။ "
          "false redaction ၏ ကုန်ကျစရိတ်သည် လုပ်ငန်း အခြေအနေအလိုက် ကွာခြားသည်။")
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
