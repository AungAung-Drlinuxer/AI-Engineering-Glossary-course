#!/usr/bin/env python3
"""Worked example (b): roofline decode throughput and cost per million output tokens.

Assumptions (stated in the guide):
  bandwidth            = 3350 GB/s accelerator memory bandwidth (assumption)
  params               = 8.0B at fp16 (2 bytes per parameter)
  KV per token         = 524288 B = 512.0 KiB per sequence
                         (2 * 32 layers * 32 heads * head_dim 128 * fp16 = 524288 B)
  GPU-hour price       = USD 2.50 (assumption; varies by vendor and region)
  achieved bandwidth   = 75.0% of the stated bandwidth (assumption)

A decode step reads every weight once plus the KV cache of every sequence in the
batch, and produces one token per sequence:
    bytes_per_step = weight_bytes + batch * kv_bytes_per_token
    tokens/s       = batch * bandwidth_bytes_per_s / bytes_per_step
    cost_per_million = price_per_hour / (tokens_per_s * 3600) * 1e6

No library, no GPU: pure arithmetic, deterministic on every run.
"""

GB = 1_000_000_000.0
BYTES = {"fp16": 2.0, "bf16": 2.0, "int8": 1.0, "int4": 0.5}
BANDWIDTH_GBPS = 3350.0
PARAMS_B = 8.0
DTYPE = "fp16"
BATCHES = (1, 8, 32, 64, 128)
KV_PER_TOKEN_BYTES = 2 * 32 * 32 * 128 * 2
GPU_HOUR_COST = 2.50
MEMORY_EFFICIENCY = 0.75


def ceiling(batch: float, weight_bytes: float, bandwidth_bps: float) -> float:
    step = weight_bytes + batch * KV_PER_TOKEN_BYTES
    return batch * bandwidth_bps / step


def cost_per_million(tokens_per_s: float, price_per_hour: float) -> float:
    return price_per_hour / (tokens_per_s * 3600.0) * 1e6


def main() -> None:
    bpw = BYTES[DTYPE]
    weight_bytes = PARAMS_B * 1e9 * bpw
    bandwidth_bps = BANDWIDTH_GBPS * GB

    print("roofline estimate - memory bandwidth bound decode (not a benchmark)")
    print("assumption: bandwidth=%.1f GB/s  achieved=%.1f%%  GPU-hour price=USD %.2f  "
          "KV=%.0f B per token per sequence"
          % (BANDWIDTH_GBPS, MEMORY_EFFICIENCY * 100.0, GPU_HOUR_COST, KV_PER_TOKEN_BYTES))
    print("weights = %d B = %.3f GB (%s)" % (weight_bytes, weight_bytes / GB, DTYPE))
    print()
    print("%-6s %14s %16s %16s %16s"
          % ("batch", "bytes/step", "tok/s ceiling", "tok/s achieved", "USD/1e6 tokens"))
    first = last = 0.0
    for batch in BATCHES:
        step = weight_bytes + batch * KV_PER_TOKEN_BYTES
        top = ceiling(batch, weight_bytes, bandwidth_bps)
        achieved = top * MEMORY_EFFICIENCY
        cpm = cost_per_million(achieved, GPU_HOUR_COST)
        if batch == BATCHES[0]:
            first = cpm
        if batch == BATCHES[-1]:
            last = cpm
        print("%-6d %14.4e %16.1f %16.1f %16.4f" % (batch, step, top, achieved, cpm))
    print()
    print("cost ratio batch %d / batch %d = %.2fx"
          % (BATCHES[0], BATCHES[-1], first / last))
    print("the weight bytes are shared by every sequence in the batch, so batch size "
          "sets cost per million tokens until KV cache dominates the step")
    print("assumption: bandwidth, efficiency and price are stated inputs and vary by "
          "accelerator, vendor and region")


if __name__ == "__main__":
    main()
