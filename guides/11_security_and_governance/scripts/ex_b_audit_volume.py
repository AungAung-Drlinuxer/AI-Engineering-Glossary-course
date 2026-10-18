#!/usr/bin/env python3
"""ex_b_audit_volume - audit log ၏ ပမာဏ၊ သိုလှောင်မှု နှင့် ကုန်ကျစရိတ်ကို
request rate နှင့် retention window အပေါ် အခြေခံ၍ တွက်ချက်သည်။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ပုံသေနည်း
    records_per_day = requests_per_day * records_per_request
    bytes_per_day   = records_per_day * bytes_per_record
    storage_bytes   = bytes_per_day * retention_days
    storage_gb      = storage_bytes / 1e9
    monthly_cost    = storage_gb * storage_cost_per_gb_month
    sampled_storage = storage_bytes * sampling_rate
    sampled_cost    = sampled_storage / 1e9 * storage_cost_per_gb_month

ယူဆချက် အားလုံးကို output တွင် (assumption) ဟု မှတ်သားထားသည်။
"""

from __future__ import annotations

RULE = "=" * 102
THIN = "-" * 102

GB = 1e9

REQUESTS_PER_DAY = 2_000_000
RECORDS_PER_REQUEST = 3
BYTES_PER_RECORD = 1200
STORAGE_COST_PER_GB_MONTH = 0.023
SAMPLING_RATE = 0.10
RETENTION_DAYS = 365

RETENTION_SWEEP = [30, 90, 180, 365, 730]


def records_per_day(requests_per_day: int, records_per_request: int) -> int:
    return requests_per_day * records_per_request


def bytes_per_day(requests_per_day: int, records_per_request: int, bytes_per_record: int) -> int:
    return records_per_day(requests_per_day, records_per_request) * bytes_per_record


def retention_storage_gb(requests_per_day: int, records_per_request: int, bytes_per_record: int,
                         retention_days: int) -> float:
    return bytes_per_day(requests_per_day, records_per_request, bytes_per_record) * retention_days / GB


def monthly_cost_usd(storage_gb: float, storage_cost_per_gb_month: float) -> float:
    return storage_gb * storage_cost_per_gb_month


def main() -> int:
    rpd = records_per_day(REQUESTS_PER_DAY, RECORDS_PER_REQUEST)
    bpd = bytes_per_day(REQUESTS_PER_DAY, RECORDS_PER_REQUEST, BYTES_PER_RECORD)
    print(RULE)
    print("ex_b_audit_volume - audit log ပမာဏ၊ သိုလှောင်မှု နှင့် ကုန်ကျစရိတ်")
    print(f"(assumption) requests_per_day={REQUESTS_PER_DAY:,}  "
          f"records_per_request={RECORDS_PER_REQUEST}  bytes_per_record={BYTES_PER_RECORD}")
    print(f"(assumption) storage_usd_per_gb_month={STORAGE_COST_PER_GB_MONTH}  "
          f"sampling_rate={SAMPLING_RATE}  (1 GB = 10^9 bytes)")
    print(THIN)
    print(f"records per day              : {rpd:>14,}")
    print(f"volume per day               : {bpd / GB:>14.2f} GB/day   ({bpd:,} bytes)")
    print(f"full-fidelity retention {RETENTION_DAYS} days : "
          f"{retention_storage_gb(REQUESTS_PER_DAY, RECORDS_PER_REQUEST, BYTES_PER_RECORD, RETENTION_DAYS):>8,.2f} GB"
          f"   {monthly_cost_usd(retention_storage_gb(REQUESTS_PER_DAY, RECORDS_PER_REQUEST, BYTES_PER_RECORD, RETENTION_DAYS), STORAGE_COST_PER_GB_MONTH):>8,.2f} USD/month")
    print(THIN)
    print(f"{'retention_days':>14} {'records_held':>16} {'storage_GB':>12} "
          f"{'monthly_usd':>12} {'sampled_GB':>11} {'sampled_usd':>12}")
    for days in RETENTION_SWEEP:
        storage = retention_storage_gb(REQUESTS_PER_DAY, RECORDS_PER_REQUEST, BYTES_PER_RECORD, days)
        cost = monthly_cost_usd(storage, STORAGE_COST_PER_GB_MONTH)
        sstorage = storage * SAMPLING_RATE
        scost = monthly_cost_usd(sstorage, STORAGE_COST_PER_GB_MONTH)
        print(f"{days:>14} {rpd * days:>16,} {storage:>12,.2f} {cost:>12,.2f} "
              f"{sstorage:>11,.2f} {scost:>12,.2f}")
    print(THIN)
    print(f"sampling {SAMPLING_RATE:.0%} of records keeps {SAMPLING_RATE:.0%} of the volume and "
          f"{SAMPLING_RATE:.0%} of the monthly cost; the discarded records cannot answer "
          f"an investigation that needs them.")
    print("မှတ်ချက် - retention_days တိုးလျှင် သိုလှောင်မှု တိုးသည်၊ sampling သည် ကုန်ကျစရိတ်ကို "
          "လျှော့သည်၊ သို့သော် မှတ်တမ်း ပြည့်စုံမှုကို လျှော့သည်။ storage စျေးနှုန်းသည် "
          "provider နှင့် tier အလိုက် ကွာခြားသည်။")
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
