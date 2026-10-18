#!/usr/bin/env python3
"""lab_audit_volume - audit log ၏ record ပမာဏ၊ သိုလှောင်မှု နှင့် ကုန်ကျစရိတ်ကို
request rate နှင့် retention window အပေါ် အခြေခံ၍ စမ်းသပ်သည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ပုံသေနည်း
    records_per_day = requests_per_day * records_per_request
    bytes_per_day   = records_per_day * bytes_per_record
    storage_bytes   = bytes_per_day * retention_days * sampling_rate
    storage_gb      = storage_bytes / 1e9
    monthly_cost    = storage_gb * storage_cost_per_gb_month
"""

from __future__ import annotations

import argparse

RULE = "=" * 102
THIN = "-" * 102

GB = 1e9
SWEEP_RETENTION_DAYS = [30, 90, 180, 365, 730]


def records_per_day(requests_per_day: int, records_per_request: int) -> int:
    return requests_per_day * records_per_request


def bytes_per_day(requests_per_day: int, records_per_request: int, bytes_per_record: int) -> int:
    return records_per_day(requests_per_day, records_per_request) * bytes_per_record


def storage_gb(requests_per_day: int, records_per_request: int, bytes_per_record: int,
               retention_days: int, sampling_rate: float) -> float:
    return bytes_per_day(requests_per_day, records_per_request, bytes_per_record) \
        * retention_days * sampling_rate / GB


def monthly_cost_usd(storage_gb_value: float, storage_cost_per_gb_month: float) -> float:
    return storage_gb_value * storage_cost_per_gb_month


def print_report(requests_per_day: int, bytes_per_record: int, retention_days: int,
                 storage_cost_per_gb_month: float, records_per_request: int,
                 sampling_rate: float) -> None:
    rpd = records_per_day(requests_per_day, records_per_request)
    bpd = bytes_per_day(requests_per_day, records_per_request, bytes_per_record)
    full_gb = storage_gb(requests_per_day, records_per_request, bytes_per_record, retention_days, 1.0)
    stored_gb = storage_gb(requests_per_day, records_per_request, bytes_per_record, retention_days, sampling_rate)
    print(RULE)
    print("lab_audit_volume - audit log ပမာဏ၊ သိုလှောင်မှု နှင့် ကုန်ကျစရိတ်")
    print(f"requests_per_day={requests_per_day:,}  bytes_per_record={bytes_per_record}  "
          f"retention_days={retention_days}  storage_cost_per_gb_month={storage_cost_per_gb_month:g}")
    print(f"(assumption) records_per_request={records_per_request}  sampling_rate={sampling_rate:g}  "
          f"retention basis=steady state, 1 GB = 10^9 bytes")
    print(THIN)
    print(f"records per day               : {rpd:>14,}")
    print(f"volume per day                : {bpd / GB:>14,.2f} GB/day")
    print(f"storage at 100% retention     : {full_gb:>14,.2f} GB")
    print(f"storage at {sampling_rate:.0%} sampling      : {stored_gb:>14,.2f} GB")
    print(f"monthly cost at 100% retention: {monthly_cost_usd(full_gb, storage_cost_per_gb_month):>14,.2f} USD")
    print(f"monthly cost at {sampling_rate:.0%} sampling : "
          f"{monthly_cost_usd(stored_gb, storage_cost_per_gb_month):>14,.2f} USD")
    print(f"saving from sampling          : "
          f"{monthly_cost_usd(full_gb, storage_cost_per_gb_month) - monthly_cost_usd(stored_gb, storage_cost_per_gb_month):>14,.2f} USD/month")
    print(f"records dropped per day       : {rpd * (1.0 - sampling_rate):>14,.0f}")
    print(THIN)
    print("မှတ်ချက် - retention window နှင့် sampling rate သည် သိုလှောင်မှုကို ဆုံးဖြတ်သည်၊ "
          "sampling လုပ်လျှင် မှတ်တမ်း ပြည့်စုံမှု ဆုံးရှုံးသည်၊ ထို့ကြောင့် မည်သည့် event ကို "
          "sampling မလုပ်ရမည်ကို ရေးမှတ်ထားရမည်။")
    print(RULE)


def print_sweep(requests_per_day: int, records_per_request: int, bytes_per_record: int,
                storage_cost_per_gb_month: float, sampling_rate: float) -> None:
    print(RULE)
    print("lab_audit_volume - retention_days sweep (storage နှင့် monthly cost)")
    print(f"requests_per_day={requests_per_day:,}  records_per_request={records_per_request}  "
          f"bytes_per_record={bytes_per_record}  sampling_rate={sampling_rate:g}")
    print(THIN)
    print(f"{'retention_days':>14} {'storage_GB':>13} {'monthly_usd':>13} {'records_held':>16}")
    for days in SWEEP_RETENTION_DAYS:
        gb = storage_gb(requests_per_day, records_per_request, bytes_per_record, days, sampling_rate)
        print(f"{days:>14} {gb:>13,.2f} {monthly_cost_usd(gb, storage_cost_per_gb_month):>13,.2f} "
              f"{records_per_day(requests_per_day, records_per_request) * days * sampling_rate:>16,.0f}")
    print(THIN)
    print("မှတ်ချက် - retention နှစ်ဆ ဖြစ်လျှင် steady-state storage နှစ်ဆ ဖြစ်သည်၊ "
          "cost သည် storage အပေါ် linear မှီခိုသည်။")
    print(RULE)


def self_test() -> int:
    ok = True

    rpd = records_per_day(2_000_000, 3)
    rpd_ok = rpd == 6_000_000
    print(f"[OK] records per day is the request rate times records per request ({rpd:,}): {rpd_ok}")
    ok = ok and rpd_ok

    g100 = storage_gb(2_000_000, 3, 1200, 100, 1.0)
    g200 = storage_gb(2_000_000, 3, 1200, 200, 1.0)
    dbl = abs(g200 - 2.0 * g100) < 1e-6
    print(f"[OK] doubling the retention window doubles the storage ({g100:,.2f} -> {g200:,.2f} GB): {dbl}")
    ok = ok and dbl

    full = storage_gb(2_000_000, 3, 1200, 365, 1.0)
    tenth = storage_gb(2_000_000, 3, 1200, 365, 0.1)
    samp = abs(tenth - 0.1 * full) < 1e-6
    print(f"[OK] sampling at 10% keeps a tenth of the storage ({full:,.2f} -> {tenth:,.2f} GB): {samp}")
    ok = ok and samp

    cost = monthly_cost_usd(full, 0.023)
    lin = abs(cost - 0.023 * full) < 1e-9
    print(f"[OK] monthly cost is the storage times the unit price ({cost:,.2f} USD): {lin}")
    ok = ok and lin

    bpd = bytes_per_day(2_000_000, 3, 1200)
    vol = abs(bpd / GB - 7.2) < 1e-9
    print(f"[OK] volume per day follows the record volume ({bpd / GB:,.2f} GB/day): {vol}")
    ok = ok and vol

    print("[PASS] lab_audit_volume self-test passed." if ok
          else "[FAIL] lab_audit_volume self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Audit log volume, storage and cost (offline, deterministic).")
    ap.add_argument("--requests-per-day", type=int, default=2_000_000)
    ap.add_argument("--bytes-per-record", type=int, default=1200)
    ap.add_argument("--retention-days", type=int, default=365)
    ap.add_argument("--storage-cost-per-gb-month", type=float, default=0.023)
    ap.add_argument("--records-per-request", type=int, default=3)
    ap.add_argument("--sampling-rate", type=float, default=0.10)
    ap.add_argument("--sweep", action="store_true", help="retention 30..730 days sweep")
    ap.add_argument("--self-test", action="store_true", help="assert the real properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.requests_per_day, args.records_per_request, args.bytes_per_record,
                    args.storage_cost_per_gb_month, args.sampling_rate)
        return 0
    print_report(args.requests_per_day, args.bytes_per_record, args.retention_days,
                 args.storage_cost_per_gb_month, args.records_per_request, args.sampling_rate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
