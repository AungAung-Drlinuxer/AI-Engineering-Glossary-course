#!/usr/bin/env python3
"""Worked example (b): optimizer-state memory, Adam versus SGD, and the batch that still fits.

Assumptions (repeated in the guide, never measured on hardware):
  params     = 7.0e9 trainable parameters
  layers     = 32, d_model = 4096, seq = 2048
  weights    = params * 2 bytes (fp16 or bf16)
  gradients  = params * 2 bytes
  optimizer state per parameter:
      SGD without momentum  0 bytes
      SGD with momentum     4 bytes (one fp32 velocity)
      Adam / AdamW          8 bytes (two fp32 moments)
      Adam with 8-bit moments 2 bytes
  activations per sequence = seq * layers * d_model * act_factor * 2 bytes
      act_factor = 10 without activation checkpointing, 2 with it
  usable budget = 64 GiB on one 80 GB accelerator (16 GiB reserved)

No library, no GPU: pure arithmetic, deterministic, offline.
"""

from __future__ import annotations

GIB = 1024 ** 3
PARAMS = 7.0e9
LAYERS = 32
D_MODEL = 4096
SEQ = 2048
BPP = 2.0
ACT_FACTOR_OFF = 10
ACT_FACTOR_ON = 2
USABLE_GIB = 64.0
OPTIMIZERS = (
    ("SGD (no state)", 0.0),
    ("SGD + momentum", 4.0),
    ("Adam (fp32 moments)", 8.0),
    ("AdamW (fp32 moments)", 8.0),
    ("Adam (8-bit moments)", 2.0),
)
RULE = "=" * 96
THIN = "-" * 96


def gib(value_bytes: float) -> float:
    return value_bytes / GIB


def largest_batch(state_bytes_per_param: float, act_factor: float) -> int:
    fixed = 2.0 * PARAMS * BPP + PARAMS * state_bytes_per_param
    per_sequence = SEQ * LAYERS * D_MODEL * act_factor * BPP
    budget = USABLE_GIB * GIB
    if budget <= fixed:
        return 0
    return int((budget - fixed) // per_sequence)


def main() -> int:
    weights = PARAMS * BPP
    gradients = PARAMS * BPP
    act_off = SEQ * LAYERS * D_MODEL * ACT_FACTOR_OFF * BPP
    act_on = SEQ * LAYERS * D_MODEL * ACT_FACTOR_ON * BPP
    print(RULE)
    print("example (b) optimizer-state memory - Adam versus SGD")
    print("params=7.0B  layers=32  d_model=4096  seq=2048  weights+gradients=fp16 (2 B/param)")
    print("activations per sequence: %.3f GiB off, %.3f GiB on activation checkpointing"
          % (gib(act_off), gib(act_on)))
    print("usable budget %.0f GiB on one 80 GB accelerator (16 GiB reserved)" % USABLE_GIB)
    print(THIN)
    print("%-22s %8s %9s %11s %11s %11s"
          % ("optimizer", "B/param", "state GiB", "fixed GiB",
             "batch off", "batch on"))
    for name, state_bpp in OPTIMIZERS:
        state = PARAMS * state_bpp
        fixed = weights + gradients + state
        print("%-22s %8.1f %9.3f %11.3f %11d %11d"
              % (name, state_bpp, gib(state), gib(fixed),
                 largest_batch(state_bpp, ACT_FACTOR_OFF),
                 largest_batch(state_bpp, ACT_FACTOR_ON)))
    print(THIN)
    adam_state = gib(PARAMS * 8.0)
    sgd_state = gib(PARAMS * 0.0)
    print("Adam state is %.3f GiB per 7.0B model, SGD without momentum keeps none." % adam_state)
    print("that difference buys %.1f extra sequences of activation memory at seq=2048."
          % (adam_state / gib(act_off)))
    print("an 8-bit moment copy halves the state to %.3f GiB and raises the batch that fits."
          % gib(PARAMS * 2.0))
    print("weights %.3f GiB and gradients %.3f GiB are unchanged by the optimizer choice."
          % (gib(weights), gib(gradients)))
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
