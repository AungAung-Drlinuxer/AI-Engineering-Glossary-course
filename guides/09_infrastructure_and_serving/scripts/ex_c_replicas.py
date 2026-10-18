#!/usr/bin/env python3
"""Worked example (c): replica count and cost for a stated arrival rate and utilisation.

Assumptions (stated in the guide):
  arrival rate           = 12 requests/s (assumption, stated workload)
  output length          = 220 output tokens per request (assumption)
  per-replica throughput = 900 output tokens/s (assumption, from ex_b_roofline geometry)
  target utilisation     = 0.75 (assumption, headroom policy)
  GPU-hour price         = USD 2.50 (assumption; varies by vendor and region)

    offered load        = arrival_rate * output_tokens                     [tokens/s]
    effective per copy  = replica_throughput * target_utilisation          [tokens/s]
    required replicas   = ceil(offered load / effective per copy)
    queue growth        = max(0, offered load - replicas * replica_throughput)
                          / output_tokens                                  [requests/s]

No library, no GPU: pure arithmetic, deterministic on every run.
"""

import math

RPS = 12.0
OUTPUT_TOKENS = 220
REPLICA_TPS = 900.0
TARGET_UTIL = 0.75
GPU_HOUR = 2.50
REPLICA_SWEEP = (2, 3, 4, 5, 6)


def main() -> None:
    load = RPS * OUTPUT_TOKENS
    effective = REPLICA_TPS * TARGET_UTIL
    required = math.ceil(load / effective)

    print("replica sizing - arrival rate %.1f req/s, %d output tokens, "
          "%.0f tokens/s per replica" % (RPS, OUTPUT_TOKENS, REPLICA_TPS))
    print("assumptions: target utilisation=%.2f  GPU-hour price=USD %.2f"
          % (TARGET_UTIL, GPU_HOUR))
    print("offered load = %.1f req/s * %d tokens = %.1f output tokens/s" % (RPS, OUTPUT_TOKENS, load))
    print("effective capacity per replica at the target = %.1f tokens/s" % effective)
    print("required replicas for the target utilisation = %d" % required)
    print()
    print("%-9s %12s %13s %15s %13s %18s"
          % ("replicas", "utilisation", "served tok/s", "queue req/s", "USD/hour",
             "USD/1e6 tokens"))
    for replicas in REPLICA_SWEEP:
        capacity = replicas * REPLICA_TPS
        served = min(load, capacity)
        utilisation = load / capacity
        queue = max(0.0, load - capacity) / OUTPUT_TOKENS
        usd_hour = replicas * GPU_HOUR
        cpm = usd_hour / (served * 3600.0) * 1e6
        print("%-9d %12.3f %13.1f %15.3f %13.2f %18.4f"
              % (replicas, utilisation, served, queue, usd_hour, cpm))
    print()
    below = max(1, required - 2)
    below_queue = max(0.0, load - below * REPLICA_TPS) / OUTPUT_TOKENS
    print("over-provisioning cost: each replica above %d is unused capacity = USD %.2f/hour idle"
          % (required, GPU_HOUR))
    print("under-provisioning cost: at %d replicas the queue grows %.3f requests/s "
          "= %.0f requests queued in 60 s"
          % (below, below_queue, below_queue * 60.0))
    print("requirement %d replicas at USD %.2f/hour = USD %.2f/hour, "
          "%.4f USD per million output tokens at this load"
          % (required, GPU_HOUR, required * GPU_HOUR,
             required * GPU_HOUR / (load * 3600.0) * 1e6))
    print("under-provisioning costs latency (the queue is unbounded), over-provisioning "
          "costs USD/hour; both are visible in this table")


if __name__ == "__main__":
    main()
