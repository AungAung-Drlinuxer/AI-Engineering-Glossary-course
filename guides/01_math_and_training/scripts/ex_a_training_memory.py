#!/usr/bin/env python3
"""Worked example (a): training memory for a stated model, batch and precision.

Assumptions (repeated in the guide, never measured on hardware):
  params     = 1.3e9 trainable parameters
  layers     = 24, d_model = 2048
  seq        = 2048 tokens per sequence, batch = 8 sequences
  weights    = params * bytes_per_parameter
  gradients  = params * bytes_per_parameter (kept in the weight dtype)
  optimizer  = Adam, two fp32 moments = params * 8 bytes
  activations = batch * seq * layers * d_model * act_factor * bytes_per_parameter
                act_factor = 10 without activation checkpointing, 2 with it
  usable budget = 64 GiB on one 80 GB accelerator (16 GiB reserved)

No library, no GPU: pure arithmetic, deterministic, offline.
"""

from __future__ import annotations

GIB = 1024 ** 3
PARAMS = 1.3e9
LAYERS = 24
D_MODEL = 2048
SEQ = 2048
BATCH = 8
ACT_FACTOR_OFF = 10
ACT_FACTOR_ON = 2
OPT_BYTES_PER_PARAM = 8.0
USABLE_GIB = 64.0
ACCELERATOR_GIB = 80.0
RESERVED_GIB = 16.0
DTYPES = (("fp32", 4.0), ("fp16", 2.0), ("bf16", 2.0))
RULE = "=" * 96
THIN = "-" * 96


def gib(value_bytes: float) -> float:
    return value_bytes / GIB


def activation_bytes(bpp: float, act_factor: float) -> float:
    return BATCH * SEQ * LAYERS * D_MODEL * act_factor * bpp


def largest_batch(bpp: float, act_factor: float) -> int:
    fixed = 2.0 * PARAMS * bpp + PARAMS * OPT_BYTES_PER_PARAM
    per_sequence = SEQ * LAYERS * D_MODEL * act_factor * bpp
    budget = USABLE_GIB * GIB
    if budget <= fixed:
        return 0
    return int((budget - fixed) // per_sequence)


def main() -> int:
    print(RULE)
    print("example (a) training memory - stated model, batch and precision")
    print("params=1.3B  layers=24  d_model=2048  seq=2048  batch=8")
    print("assumptions: gradients in the weight dtype, Adam keeps two fp32 moments,")
    print("             act_factor=10 per layer per token (2 with checkpointing)")
    print(THIN)
    print("%-6s %8s %10s %11s %11s %10s %9s %11s %10s"
          % ("dtype", "B/param", "weights", "gradients", "optimizer",
             "act(off)", "act(on)", "total(off)", "total(on)"))
    for name, bpp in DTYPES:
        weights = PARAMS * bpp
        gradients = PARAMS * bpp
        optimizer = PARAMS * OPT_BYTES_PER_PARAM
        act_off = activation_bytes(bpp, ACT_FACTOR_OFF)
        act_on = activation_bytes(bpp, ACT_FACTOR_ON)
        total_off = weights + gradients + optimizer + act_off
        total_on = weights + gradients + optimizer + act_on
        print("%-6s %8.1f %10.3f %11.3f %11.3f %10.3f %9.3f %11.3f %10.3f"
              % (name, bpp, gib(weights), gib(gradients), gib(optimizer),
                 gib(act_off), gib(act_on), gib(total_off), gib(total_on)))
    print(THIN)
    print("all values above are GiB, fixed components are identical across dtype")
    print("largest batch that fits one %.0f GB accelerator with %.0f GiB reserved (%.0f GiB usable):"
          % (ACCELERATOR_GIB, RESERVED_GIB, USABLE_GIB))
    print("%-6s %24s %24s" % ("dtype", "checkpointing=off", "checkpointing=on"))
    for name, bpp in DTYPES:
        print("%-6s %24d %24d"
              % (name, largest_batch(bpp, ACT_FACTOR_OFF), largest_batch(bpp, ACT_FACTOR_ON)))
    print(THIN)
    print("activation checkpointing divides activation memory by %.0fx and raises the largest batch"
          % (ACT_FACTOR_OFF / ACT_FACTOR_ON))
    print("that fits; it does not change weights, gradients or optimizer state.")
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
