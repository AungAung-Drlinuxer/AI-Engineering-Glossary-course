#!/usr/bin/env python3
"""Worked example (a): served-model memory budget - weights, KV cache, activations.

Assumptions (stated in the guide, offline arithmetic only):
  params        = 8.0B at fp16 (2 bytes per parameter)
  geometry      = 32 layers, 32 heads, head_dim 128 -> d_model 4096
  context       = 8192 tokens
  KV cache      = 2 (K and V) * layers * heads * head_dim * context * bytes_per_element
  activations   = batch * context * d_model * ACTIVATION_FACTOR * bytes_per_element
                  with ACTIVATION_FACTOR = 4.0 (residual stream plus two FFN
                  intermediates plus the attention output projection)
  memory budget = 72.000 GiB usable for weights + KV cache + activations together
The batch sweep shows how batch size trades KV cache and activation memory
against a fixed weights footprint.

No library, no GPU: pure arithmetic, deterministic on every run.
"""

GIB = 1024 ** 3
BYTES = {"fp16": 2.0, "bf16": 2.0, "int8": 1.0, "int4": 0.5}
PARAMS_B = 8.0
LAYERS, HEADS, HEAD_DIM = 32, 32, 128
CONTEXT = 8192
DTYPE = "fp16"
ACTIVATION_FACTOR = 4.0
BUDGET_GIB = 72.0
BATCHES = (1, 8, 32, 64, 128)


def main() -> None:
    bpw = BYTES[DTYPE]
    d_model = HEADS * HEAD_DIM
    weights = PARAMS_B * 1e9 * bpw
    kv_per_seq = 2 * LAYERS * HEADS * HEAD_DIM * CONTEXT * bpw
    act_per_seq = CONTEXT * d_model * bpw * ACTIVATION_FACTOR
    per_seq = kv_per_seq + act_per_seq
    budget_bytes = BUDGET_GIB * GIB
    max_batch = int((budget_bytes - weights) // per_seq)

    print("reference serving geometry: params=%.1fB layers=%d heads=%d head_dim=%d "
          "d_model=%d context=%d dtype=%s"
          % (PARAMS_B, LAYERS, HEADS, HEAD_DIM, d_model, CONTEXT, DTYPE))
    print("assumption: %s = %.3f bytes per parameter and per KV element; "
          "activation workspace = batch * context * d_model * %.2f * bytes"
          % (DTYPE, bpw, ACTIVATION_FACTOR))
    print("weights on the accelerator        = %14d B = %8.3f GiB" % (weights, weights / GIB))
    print("KV cache per sequence             = %14d B = %8.3f GiB" % (kv_per_seq, kv_per_seq / GIB))
    print("activation workspace per sequence = %14d B = %8.3f GiB"
          % (act_per_seq, act_per_seq / GIB))
    print("memory budget (stated)            = %14d B = %8.3f GiB" % (budget_bytes, BUDGET_GIB))
    print()
    print("%-6s %14s %10s %12s %6s %14s"
          % ("batch", "KV total GiB", "act GiB", "total GiB", "fits", "headroom GiB"))
    for batch in BATCHES:
        kv_total = kv_per_seq * batch
        act_total = act_per_seq * batch
        total = weights + kv_total + act_total
        fits = "yes" if total <= budget_bytes else "no"
        print("%-6d %14.3f %10.3f %12.3f %6s %14.3f"
              % (batch, kv_total / GIB, act_total / GIB, total / GIB, fits,
                 (budget_bytes - total) / GIB))
    print()
    print("largest batch that fits %.3f GiB with these weights = %d" % (BUDGET_GIB, max_batch))
    print("memory per sequence beyond the weights = %.3f GiB (KV %.3f + activations %.3f)"
          % (per_seq / GIB, kv_per_seq / GIB, act_per_seq / GIB))
    print("doubling the batch doubles KV cache and activation memory but not the weights; "
          "KV cache grows with context, weights do not")


if __name__ == "__main__":
    main()
