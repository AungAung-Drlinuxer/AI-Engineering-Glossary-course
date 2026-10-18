#!/usr/bin/env python3
"""Worked example (d): cost per million output tokens from modelled throughput.

This is a roofline DERIVATION, not a benchmark. Throughput is modelled from
memory bandwidth, because single-stream decoding re-reads every weight for each
token and is therefore memory bound:

    tokens/s (batch B) = B * bandwidth / (weight_bytes + B * kv_bytes_per_token)

Assumptions (all of them are vendor-, GPU- and setup-dependent):
    model                = 7B parameters, fp16            -> 14.0 GB of weights
    accelerator bandwidth = 3350 GB/s  (stated assumption)
    kv_bytes_per_token    = 512 KiB (fp16, reference model of example (a))
    accelerator hour price = USD 2.50  (stated assumption)
    cost per 1e6 tokens  = price_per_hour / (tokens_per_second * 3600) * 1e6
Batch 32 additionally needs weights to be re-read only once per step, so per-step
compute (2 * N FLOPs per token) sets a second ceiling; that ceiling is checked too.
"""
BW = 3350e9            # bytes/s
WEIGHTS = 7e9 * 2      # bytes, fp16
KV_TOKEN = 2 * 32 * 32 * 128 * 2   # bytes per token per sequence
PRICE = 2.50           # USD per accelerator hour
FLOP_LIMIT = 990e12    # dense fp16 FLOPS, stated assumption
FLOPS_PER_TOKEN = 2 * 7e9

print("weights = %.2f GB fp16 ; KV per token per sequence = %.1f KiB ; price = USD %.2f/h"
      % (WEIGHTS / 1e9, KV_TOKEN / 1024, PRICE))
print()
print("%-7s %14s %14s %14s %16s" % ("batch", "bytes/step", "tok/s", "tok/s compute-cap", "USD / 1e6 tok"))
for batch in (1, 32):
    bytes_step = WEIGHTS + batch * KV_TOKEN
    tps_mem = batch * BW / bytes_step
    tps_comp = FLOP_LIMIT / FLOPS_PER_TOKEN * batch
    tps = min(tps_mem, tps_comp)
    cost = PRICE / (tps * 3600) * 1e6
    print("%-7d %14.3e %14.1f %14.1f %16.4f" % (batch, bytes_step, tps_mem, tps_comp, cost))
b1 = BW / (WEIGHTS + KV_TOKEN)
b32 = min(32 * BW / (WEIGHTS + 32 * KV_TOKEN), FLOP_LIMIT / FLOPS_PER_TOKEN * 32)
print()
print("cost ratio batch 1 / batch 32 = %.2fx" % ((PRICE / (b1 * 3600) * 1e6) / (PRICE / (b32 * 3600) * 1e6)))
