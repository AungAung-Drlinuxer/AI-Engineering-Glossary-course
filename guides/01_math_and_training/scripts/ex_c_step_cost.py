#!/usr/bin/env python3
"""Worked example (c): step time and run cost for a stated token budget and GPU-hour price.

Assumptions (repeated in the guide, never measured on hardware):
  token budget = 100.0e9 training tokens
  batch = 8 sequences, seq = 2048 tokens -> 16384 tokens per optimizer step
  training FLOPs per step = 6 * params * tokens (forward 2 N, backward 4 N)
  params = 7.0e9, peak fp16 throughput = 1000 TFLOP/s per accelerator
  achieved throughput = utilisation * peak
  activation checkpointing recomputes one forward pass -> 8 / 6 step FLOPs
  price = USD 2.50 per accelerator-hour, one accelerator

No library, no GPU: pure arithmetic, deterministic, offline.
"""

from __future__ import annotations

BUDGET_TOKENS = 100.0e9
PARAMS = 7.0e9
BATCH = 8
SEQ = 2048
PEAK_TFLOPS = 1000.0
PRICE_PER_HOUR = 2.50
UTILISATIONS = ((0.20, "20%"), (0.40, "40%"), (0.60, "60%"))
CKPT_MULTIPLIER = 8.0 / 6.0
RULE = "=" * 96
THIN = "-" * 96


def row(utilisation: float, label: str, step_flops: float, steps: float) -> tuple:
    achieved = utilisation * PEAK_TFLOPS
    step_seconds = step_flops / (achieved * 1e12)
    wall_hours = step_seconds * steps / 3600.0
    cost = wall_hours * PRICE_PER_HOUR
    print("%-12s %16.1f %14.3f %14.1f %12.1f %14.2f"
          % (label, achieved, step_seconds, wall_hours, wall_hours, cost))
    return step_seconds, wall_hours, cost


def main() -> int:
    tokens_per_step = BATCH * SEQ
    steps = BUDGET_TOKENS / tokens_per_step
    step_flops = 6.0 * PARAMS * tokens_per_step
    print(RULE)
    print("example (c) step time and cost - stated token budget and GPU-hour price")
    print("budget=%.1fB tokens  batch=%d  seq=%d  tokens/step=%d"
          % (BUDGET_TOKENS / 1e9, BATCH, SEQ, tokens_per_step))
    print("step FLOPs = 6 * params * tokens per step = %.4e FLOPs" % step_flops)
    print("optimizer steps = %.1fB / %d = %d" % (BUDGET_TOKENS / 1e9, tokens_per_step, steps))
    print("peak %.0f TFLOP/s fp16 per accelerator, price USD %.2f per accelerator-hour"
          % (PEAK_TFLOPS, PRICE_PER_HOUR))
    print(THIN)
    print("%-12s %16s %14s %14s %12s %14s"
          % ("utilisation", "achieved TFLOP/s", "step seconds", "wall-clock h", "GPU-hours", "cost USD"))
    base_cost = 0.0
    base_hours = 0.0
    for utilisation, label in UTILISATIONS:
        _step, hours, cost = row(utilisation, label, step_flops, steps)
        if label == "40%":
            base_cost = cost
            base_hours = hours
    print(THIN)
    print("activation checkpointing recomputes one forward pass: step FLOPs x %.3f (= 8/6)."
          % CKPT_MULTIPLIER)
    print("%-12s %16s %14s %14s %12s %14s"
          % ("utilisation", "achieved TFLOP/s", "step seconds", "wall-clock h", "GPU-hours", "cost USD"))
    for utilisation, label in UTILISATIONS:
        row(utilisation, label, step_flops * CKPT_MULTIPLIER, steps)
    print(THIN)
    print("at 40%% utilisation the budget costs USD %.2f and %.1f accelerator-hours without checkpointing."
          % (base_cost, base_hours))
    print("the same budget costs USD %.2f with checkpointing: %.1f%% more accelerator time."
          % (base_cost * CKPT_MULTIPLIER, (CKPT_MULTIPLIER - 1.0) * 100.0))
    print("doubling utilisation halves wall-clock and cost; the FLOPs are unchanged.")
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
