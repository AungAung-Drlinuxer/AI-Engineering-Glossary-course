#!/usr/bin/env python3
"""Worked example (a): KV cache memory for the reference model.

Assumptions (stated in the guide):
  L      = 32 layers
  H      = 32 attention heads
  d_head = 128  -> d_model = H * d_head = 4096
  KV cache holds one key tensor and one value tensor per layer.
  Formula: bytes = 2 (K and V) * L * H * d_head * seq_len * bytes_per_element * batch
  fp16 = 2 bytes/element, int8 = 1 byte/element.
No library, no GPU: pure arithmetic.
"""
GIB = 1024 ** 3
L, H, DH = 32, 32, 128
BATCHES = (1, 32)
PRECISIONS = (("fp16", 2), ("int8", 1))
CONTEXTS = (8192, 32768, 131072)

print("reference model: layers=%d heads=%d head_dim=%d d_model=%d" % (L, H, DH, H * DH))
per_token = 2 * L * H * DH * 2
print("KV bytes per token (fp16, batch 1) = 2*%d*%d*%d*2 = %d B = %.3f MiB"
      % (L, H, DH, per_token, per_token / 1024 / 1024))
print()
print("%-9s %-6s %-6s %14s %14s" % ("context", "prec", "batch", "KV caches (GiB)", "bytes"))
for ctx in CONTEXTS:
    for prec, width in PRECISIONS:
        for batch in BATCHES:
            total = 2 * L * H * DH * ctx * width * batch
            print("%-9d %-6s %-6d %14.3f %14d" % (ctx, prec, batch, total / GIB, total))
print()
print("headroom check against one 80 GB accelerator with 16 GiB reserved (64 GiB usable):")
for ctx in CONTEXTS:
    for prec, width in PRECISIONS:
        per_seq = 2 * L * H * DH * ctx * width / GIB
        max_batch = int(64 // per_seq)
        print("  context %-7d %-5s per sequence %7.2f GiB -> largest batch that fits = %d"
              % (ctx, prec, per_seq, max_batch))
