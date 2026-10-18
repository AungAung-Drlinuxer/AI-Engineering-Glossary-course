#!/usr/bin/env python3
"""Worked example (c): attention versus feed-forward FLOPs at 2K, 8K, 32K context.

Reference model: L=32 layers, d_model=4096, d_ff=11008, H=32 heads, d_head=128.
Counting multiply-accumulate as 2 FLOPs, forward pass only, one sequence, batch 1.

  attention core per layer      = 4 * seq^2 * d_model      (QK^T and (attn)V)
  attention projections/layer   = 2 * seq * d_model * 4 * d_model  (Wq,Wk,Wv,Wo)
  feed-forward per layer        = 4 * seq * d_model * d_ff
  -> attention core overtakes feed-forward when seq = d_ff = 11008.
"""
L = 32
D = 4096
DFF = 11008
CONTEXTS = (2048, 8192, 32768)

print("reference: layers=%d d_model=%d d_ff=%d ; attention core = FFN when seq = d_ff = %d"
      % (L, D, DFF, DFF))
print()
print("%-7s %16s %16s %16s %10s" % ("seq", "attn core TFLOP", "attn proj TFLOP", "ffn TFLOP", "core/ffn"))
for s in CONTEXTS:
    core = 4 * s * s * D * L / 1e12
    proj = 8 * s * D * D * L / 1e12
    ffn = 4 * s * D * DFF * L / 1e12
    print("%-7d %16.2f %16.2f %16.2f %10.3f" % (s, core, proj, ffn, core / ffn))
print()
for s in CONTEXTS:
    core = 4 * s * s * D * L
    proj = 8 * s * D * D * L
    ffn = 4 * s * D * DFF * L
    print("seq %-6d attention total (core+proj) is %.1f%% of the layer FLOPs; core alone %.1f%%"
          % (s, 100 * (core + proj) / (core + proj + ffn), 100 * core / (core + proj + ffn)))
