#!/usr/bin/env python3
"""lab_autoscale - replica count, queue growth, scale-up time and provision cost.

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

ပုံသေနည်းများ —
    offered_load    = rps * output_tokens                              [tokens/s]
    effective_copy  = replica_tps * target_utilisation                 [tokens/s]
    required        = ceil(offered_load / effective_copy)
    utilisation     = offered_load / (replicas * replica_tps)
    served          = min(offered_load, replicas * replica_tps)
    queue_growth    = max(0, offered_load - replicas * replica_tps) / output_tokens
    scale_up_time   = max(0, required - replicas) * cold_start_s
    usd_per_million = usd_per_hour / (served * 3600) * 1e6

rps၊ output length၊ per-replica throughput၊ target utilisation၊ cold-start time နှင့်
GPU-hour စျေးနှုန်းသည် stated assumption ဖြစ်သည်။
"""

from __future__ import annotations

import argparse
import math

RULE = "=" * 74
THIN = "-" * 74
REPLICA_SWEEP = (1, 2, 3, 4, 6, 8)


def required_replicas(rps: float, output_tokens: float, replica_tps: float,
                      target: float) -> int:
    load = rps * output_tokens
    return int(math.ceil(load / (replica_tps * target)))


def print_report(args: argparse.Namespace) -> None:
    load = args.rps * args.output_tokens
    effective = args.replica_tps * args.target_utilisation
    required = required_replicas(args.rps, args.output_tokens, args.replica_tps,
                                 args.target_utilisation)
    capacity = args.replicas * args.replica_tps
    served = min(load, capacity)
    utilisation = load / capacity
    queue = max(0.0, load - capacity) / args.output_tokens
    per_replica_load = load / args.replicas
    shortfall = max(0.0, load - capacity)
    scale_up = max(0, required - args.replicas)
    usd_hour = args.replicas * args.gpu_hour_cost
    cpm = usd_hour / (served * 3600.0) * 1e6
    over = max(0, args.replicas - required)
    print(RULE)
    print("lab_autoscale - replica count, queue growth, scale-up time and cost")
    print(f"rps={args.rps:.1f}  output-tokens={args.output_tokens}  "
          f"replica-tps={args.replica_tps:.0f}  replicas={args.replicas}  "
          f"target-utilisation={args.target_utilisation:.2f}  cold-start-s={args.cold_start_s}")
    print(f"GPU-hour price=USD {args.gpu_hour_cost:.2f} (assumption, varies by vendor)")
    print(THIN)
    print(f"offered load                : {load:>12.1f} output tokens/s")
    print(f"effective per replica       : {effective:>12.1f} tokens/s at the target")
    print(f"load per replica            : {per_replica_load:>12.1f} tokens/s  "
          f"(utilisation {utilisation:.3f})")
    print(f"queue growth                : {queue:>12.3f} requests/s  "
          f"(backlog {queue * 60.0:.0f} requests in 60 s)")
    print(f"required replicas (target)  : {required:>12}")
    print(f"scale-up needed             : {scale_up:>12} replica(s)")
    print(f"scale-up time               : {scale_up * args.cold_start_s:>12.1f} s")
    print(f"served throughput           : {served:>12.1f} tokens/s")
    print(f"cost at {args.replicas} replica(s)           : {usd_hour:>12.2f} USD/hour")
    print(f"cost per million tokens     : {cpm:>12.4f} USD")
    print(f"over-provisioning cost      : {over * args.gpu_hour_cost:>12.2f} USD/hour  "
          f"({over} idle replica(s))")
    print(f"under-provisioning shortfall: {shortfall:>12.1f} tokens/s unscheduled")
    print(THIN)
    print("replica sweep:")
    print(f"{'replicas':<10}{'utilisation':>12}{'served tok/s':>14}{'queue req/s':>13}"
          f"{'USD/hour':>11}{'USD/1e6 tokens':>16}")
    for replicas in REPLICA_SWEEP:
        cap = replicas * args.replica_tps
        srv = min(load, cap)
        util = load / cap
        q = max(0.0, load - cap) / args.output_tokens
        usd = replicas * args.gpu_hour_cost
        print(f"{replicas:<10}{util:>12.3f}{srv:>14.1f}{q:>13.3f}{usd:>11.2f}"
              f"{usd / (srv * 3600.0) * 1e6:>16.4f}")
    print(THIN)
    print("မှတ်ချက် - utilisation သည် 1.0 ကျော်လျှင် queue ကြီးထွားသည်၊ target utilisation "
          "အောက် ထားလျှင် latency headroom ရရှိသည်။")
    print(RULE)


def self_test() -> int:
    ok = True

    load = 12.0 * 220.0
    req = required_replicas(12.0, 220.0, 900.0, 0.75)
    covers = req * 900.0 * 0.75 >= load
    tight = (req - 1) * 900.0 * 0.75 < load
    print(f"[OK] required replicas cover the load at the target and are tight "
          f"({req} covers, {req - 1} does not): {covers and tight}")
    ok = ok and covers and tight

    cap_ok = min(load, 4 * 900.0) == load
    q_zero = max(0.0, load - 4 * 900.0) / 220.0 == 0.0
    print(f"[OK] no queue growth while capacity meets the load: {cap_ok and q_zero}")
    ok = ok and cap_ok and q_zero

    q2 = max(0.0, load - 2 * 900.0) / 220.0
    q3 = max(0.0, load - 3 * 900.0) / 220.0
    monotone = q2 > q3
    print(f"[OK] the queue grows faster with fewer replicas "
          f"({q2:.3f} at 2 vs {q3:.3f} at 3 req/s): {monotone}")
    ok = ok and monotone

    c2 = 2 * 2.50
    c4 = 4 * 2.50
    lin_ok = abs(c4 - 2.0 * c2) < 1e-9
    print(f"[OK] provision cost is linear in replicas ({c2:.2f} -> {c4:.2f} USD/hour): {lin_ok}")
    ok = ok and lin_ok

    short = max(0.0, load - 2 * 900.0)
    short_ok = abs(short - 840.0) < 1e-9
    print(f"[OK] under-provisioning reports the unscheduled tokens/s "
          f"({short:.1f}): {short_ok}")
    ok = ok and short_ok

    print("[PASS] lab_autoscale self-test passed." if ok
          else "[FAIL] lab_autoscale self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Replica sizing and queue-growth lab (offline, deterministic).")
    ap.add_argument("--rps", type=float, default=12.0)
    ap.add_argument("--output-tokens", type=int, default=220)
    ap.add_argument("--replica-tps", type=float, default=900.0)
    ap.add_argument("--replicas", type=int, default=2)
    ap.add_argument("--target-utilisation", type=float, default=0.75)
    ap.add_argument("--cold-start-s", type=float, default=45.0)
    ap.add_argument("--gpu-hour-cost", type=float, default=2.50)
    ap.add_argument("--sweep", action="store_true", help="sweep replicas 1 .. 8")
    ap.add_argument("--self-test", action="store_true", help="assert the autoscaling properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    print_report(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
