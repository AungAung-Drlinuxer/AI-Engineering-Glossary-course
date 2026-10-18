#!/usr/bin/env python3
"""lab_attention_cost - Attention ၏ FLOPs၊ score-matrix memory နှင့် FFN နှင့် နှိုင်းယှဉ်မှုကို တွက်သည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

Assumption များ (block တစ်ခုစီတွင် ပြန်လည် ဖော်ပြသည်)
    d_model = heads * head_dim
    attention FLOPs (per head, per layer) = 2 * n^2 * d   (QK^T နှင့် PV matmul နှစ်ခု)
    d_ff    = 4 * d_model               (feed-forward intermediate size)
    FFN FLOPs (per layer) = 4 * n * d_model * d_ff        (up projection + down projection)
    attention = FFN ဖြစ်သည့် break-even context  n* = 2 * d_ff
"""

from __future__ import annotations

import argparse

DTYPE_BYTES = {"fp16": 2.0, "bf16": 2.0, "int8": 1.0, "int4": 0.5}
DTYPE_ORDER = ["fp16", "bf16", "int8", "int4"]
FFN_MULTIPLIER = 4
MIB = 1024.0 * 1024.0
RULE = "=" * 74
THIN = "-" * 74


def d_model_of(heads: int, head_dim: int) -> int:
    return heads * head_dim


def attention_flops(n: int, layers: int, heads: int, head_dim: int) -> float:
    """layers * heads * 2 * n^2 * head_dim"""
    return layers * heads * 2.0 * n * n * head_dim


def ffn_flops(n: int, layers: int, heads: int, head_dim: int, d_ff: int) -> float:
    """layers * 4 * n * d_model * d_ff"""
    return layers * 4.0 * n * d_model_of(heads, head_dim) * d_ff


def attn_decode_flops(n: int, layers: int, heads: int, head_dim: int) -> float:
    """decode step တစ်ခု (query 1 လုံး၊ key n လုံး): layers * heads * 2 * n * head_dim"""
    return layers * heads * 2.0 * n * head_dim


def gb(value_bytes: float) -> float:
    return value_bytes / MIB / 1024.0


def print_report(context: int, layers: int, heads: int, head_dim: int, dtype: str) -> None:
    d_model = d_model_of(heads, head_dim)
    d_ff = FFN_MULTIPLIER * d_model
    bpe = DTYPE_BYTES[dtype]
    attn = attention_flops(context, layers, heads, head_dim)
    ffn = ffn_flops(context, layers, heads, head_dim, d_ff)
    score_per_head = context * context * bpe
    score_total = score_per_head * layers * heads
    break_even = 2 * d_ff
    dominant = "attention" if attn > ffn else "FFN"

    print(RULE)
    print("lab_attention_cost - attention FLOPs, score memory, FFN comparison")
    print(f"context={context}  layers={layers}  heads={heads}  head_dim={head_dim}  dtype={dtype}")
    print(f"d_model = {d_model}   d_ff = {FFN_MULTIPLIER} * d_model = {d_ff}")
    print(THIN)
    print("Assumption: attention = layers * heads * 2 * n^2 * head_dim  (per head per layer 2*n^2*d)")
    print(f"Attention FLOPs          : {attn:>22,.0f}  ({attn / 1e12:.2f} TFLOPs)")
    print("Assumption: FFN = layers * 4 * n * d_model * d_ff")
    print(f"FFN FLOPs                : {ffn:>22,.0f}  ({ffn / 1e12:.2f} TFLOPs)")
    print(f"Attention / FFN ratio    : {attn / ffn:>22.4f}")
    print(f"Dominant term at n={context}: {dominant}")
    print(f"Break-even context n*    : {break_even:>22,}  (n* = 2 * d_ff)")
    print(THIN)
    print(f"Score-matrix memory per head : {score_per_head / MIB:>12,.3f} MB  (n*n*{bpe} bytes)")
    print(f"Score-matrix memory total    : {score_total / MIB:>12,.3f} MB  ({gb(score_total):.3f} GB, "
          f"layers*heads*n*n*{bpe})")
    print(THIN)
    print(f"Decode step with KV cache ({context} keys, 1 query):")
    dec = attn_decode_flops(context, layers, heads, head_dim)
    print(f"  attention FLOPs        : {dec:>22,.0f}  ({dec / 1e9:.3f} GFLOPs)")
    print(f"  score row per head     : {context * bpe / MIB:>22,.6f} MB  (n*{bpe} bytes)")
    print(f"  score rows total       : {layers * heads * context * bpe / MIB:>22,.3f} MB")
    print(f"  full-sequence attention: {attn:>21,.0f}  -> {attn / dec:,.1f}x အလုပ် သက်သာသည်")
    print(RULE)


def self_test() -> int:
    ok = True
    cfg = dict(layers=32, heads=32, head_dim=128)
    n = 8192
    d_model = d_model_of(cfg["heads"], cfg["head_dim"])
    d_ff = FFN_MULTIPLIER * d_model

    a1 = attention_flops(n, **cfg)
    a2 = attention_flops(2 * n, **cfg)
    quad = abs(a2 - 4.0 * a1) < 1e-6
    print(f"[OK] attention FLOPs grow quadratically with context ({a1 / 1e12:.2f} -> {a2 / 1e12:.2f} TFLOPs): {quad}")
    ok = ok and quad

    c1 = attn_decode_flops(n, **cfg)
    c2 = attn_decode_flops(2 * n, **cfg)
    lin = abs(c2 - 2.0 * c1) < 1e-6
    print(f"[OK] cached decode attention grows linearly ({c1 / 1e9:.3f} -> {c2 / 1e9:.3f} GFLOPs): {lin}")
    ok = ok and lin

    be = 2 * d_ff
    lhs = attention_flops(be, **cfg)
    rhs = ffn_flops(be, **cfg, d_ff=d_ff)
    cross = abs(lhs - rhs) / rhs < 1e-12
    below = ffn_flops(be - 1, **cfg, d_ff=d_ff) > attention_flops(be - 1, **cfg)
    above = attention_flops(be + 1, **cfg) > ffn_flops(be + 1, **cfg, d_ff=d_ff)
    print(f"[OK] break-even context is 2*d_ff = {be:,} where attention meets the FFN: {cross and below and above}")
    ok = ok and cross and below and above

    saved = attn_decode_flops(n, **cfg) < attention_flops(n, **cfg)
    print(f"[OK] a cached decode step costs far less than full-sequence attention at n={n:,}: {saved}")
    ok = ok and saved

    mem1 = n * n * DTYPE_BYTES["fp16"]
    mem2 = (2 * n) * (2 * n) * DTYPE_BYTES["fp16"]
    mem4 = abs(mem2 - 4.0 * mem1) < 1e-6
    print(f"[OK] the n*n score matrix grows quadratically ({gb(mem1):.4f} -> {gb(mem2):.4f} GB): {mem4}")
    ok = ok and mem4

    print("[PASS] lab_attention_cost self-test passed." if ok else "[FAIL] lab_attention_cost self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Attention cost, score memory and FFN comparison (offline, deterministic).")
    ap.add_argument("--context", type=int, default=8192)
    ap.add_argument("--layers", type=int, default=32)
    ap.add_argument("--heads", type=int, default=32)
    ap.add_argument("--head-dim", type=int, default=128)
    ap.add_argument("--dtype", choices=DTYPE_ORDER, default="fp16")
    ap.add_argument("--self-test", action="store_true", help="assert the real quadratic/linear properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    print_report(args.context, args.layers, args.heads, args.head_dim, args.dtype)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
