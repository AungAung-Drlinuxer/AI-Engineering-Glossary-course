#!/usr/bin/env python3
"""Worked example (b): the KV-cache memory a longer prompt costs, and what
prefix caching saves when many calls share a prefix.

Formulas (shown, all arithmetic below comes from them):

    kv_bytes(tokens)  = 2 (K and V) * layers * tokens * heads * head_dim
                        * bytes_per_element
    prefill_without_cache = calls * (prefix_tokens + suffix_tokens)
    prefill_with_cache    = prefix_tokens + calls * suffix_tokens
    saved_fraction        = (calls - 1) * prefix_tokens
                            / (calls * (prefix_tokens + suffix_tokens))

Assumptions (stated; every one of them is vendor-, model- and GPU-dependent):

    reference model  : layers 32, heads 32, head_dim 128 (d_model 4096), fp16
                       -> 2 * 32 * 32 * 128 * 2 = 524288 B = 0.500 MiB per token
    accelerator      : 80 GB, 16 GiB reserved for weights and buffers
                       -> 64 GiB usable for KV cache
    prefill rate     : 8000 tokens/s (for the latency columns)
    input price      : USD 3.00 per 1e6 tokens
    prefix / calls   : 3000 shared prefix tokens, 100 calls, 200 suffix tokens

Standard library only; deterministic.
"""

from __future__ import annotations

MIB = 1024.0 * 1024.0
LAYERS = 32
HEADS = 32
HEAD_DIM = 128
BYTES_PER_ELEMENT = 2.0          # fp16
KV_PER_TOKEN = 2 * LAYERS * HEADS * HEAD_DIM * BYTES_PER_ELEMENT   # bytes
USABLE_GIB = 64.0
PREFILL_RATE = 8000.0            # tokens/s (assumption)
IN_PRICE = 3.00                  # USD per 1e6 tokens (assumption)
PREFIX_TOKENS = 3000
CALLS = 100
SUFFIX_TOKENS = 200


def kv_mib(tokens: int, batch: int = 1) -> float:
    return batch * tokens * KV_PER_TOKEN / MIB


def main() -> int:
    print("estimator of KV memory: kv_bytes = 2 * layers * tokens * heads * head_dim * bytes")
    print("reference model: layers=%d heads=%d head_dim=%d fp16 -> %.3f MiB per token"
          % (LAYERS, HEADS, HEAD_DIM, KV_PER_TOKEN / MIB))
    print("usable KV on one 80 GB accelerator with 16 GiB reserved = %.0f GiB" % USABLE_GIB)
    print()
    print("part 1 - what a longer prompt costs in KV cache")
    print("%-12s %14s %14s %14s %14s"
          % ("prompt tok", "batch 1 MiB", "batch 1 GiB", "batch 32 GiB", "batch 32 fits"))
    for tokens in (1000, 3000, 8000, 32000):
        b1 = kv_mib(tokens, 1)
        b32_gi = kv_mib(tokens, 32) / 1024.0
        fits = int(b32_gi <= USABLE_GIB)
        print("%-12d %14.2f %14.4f %14.4f %14d" % (tokens, b1, b1 / 1024.0, b32_gi, fits))
    print()
    print("part 2 - prefix caching: %d shared prefix tokens, %d calls, %d suffix tokens each"
          % (PREFIX_TOKENS, CALLS, SUFFIX_TOKENS))
    without = CALLS * (PREFIX_TOKENS + SUFFIX_TOKENS)
    with_cache = PREFIX_TOKENS + CALLS * SUFFIX_TOKENS
    saved = without - with_cache
    percent = saved / without * 100.0
    print("%-34s %10d" % ("prefill tokens without cache", without))
    print("%-34s %10d" % ("prefill tokens with prefix cache", with_cache))
    print("%-34s %10d" % ("prefill tokens saved", saved))
    print("%-34s %9.2f%%" % ("saved, percent of the uncached prefill", percent))
    print("%-34s %10d" % ("token saving per added call (calls>1)",
                          (CALLS - 1) * PREFIX_TOKENS // CALLS))
    print()
    print("latency at %.0f tokens/s prefill" % PREFILL_RATE)
    print("%-34s %10.1f ms" % ("without cache", without / PREFILL_RATE * 1000.0))
    print("%-34s %10.1f ms" % ("with prefix cache", with_cache / PREFILL_RATE * 1000.0))
    print("%-34s %10.1f ms" % ("saved", saved / PREFILL_RATE * 1000.0))
    print()
    print("cost at USD %.2f per 1e6 prefill tokens" % IN_PRICE)
    print("%-34s %10.6f USD" % ("without cache", without * IN_PRICE / 1e6))
    print("%-34s %10.6f USD" % ("with prefix cache", with_cache * IN_PRICE / 1e6))
    print()
    print("memory side: the shared prefix KV is stored once = %.2f MiB (%.4f GiB); "
          "without sharing, %d copies would take %.2f GiB"
          % (kv_mib(PREFIX_TOKENS), kv_mib(PREFIX_TOKENS) / 1024.0, CALLS,
             kv_mib(PREFIX_TOKENS, CALLS) / 1024.0))
    print("the cache contract (eligibility, lifetime, minimum block) is provider-specific, "
          "so misses are normal.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
