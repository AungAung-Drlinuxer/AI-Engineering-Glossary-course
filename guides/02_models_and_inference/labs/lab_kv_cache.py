#!/usr/bin/env python3
"""lab_kv_cache - KV Cache ၏ memory နှင့် ထပ်တလဲလဲ တွက်ချက်မှု သက်သာမှုကို တိုင်းတာသည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

ပုံသေနည်း
    kv_mb  = batch * layers * 2 * n * heads * head_dim * bytes_per_element / MiB
             (2 သည် key နှင့် value နှစ်မျိုးအတွက် ဖြစ်သည်)
    weight_mb = params_b * 1e9 * bytes_per_element / MiB

Attention အလုပ်ပမာဏ (decode) — score pair အရေအတွက်
    cached decode   : n          (query 1 လုံး x key n လုံး)
    uncached decode : n * n      (position n လုံး x key n လုံး၊ prefix ကို ပြန်လည် တွက်သည်)
ထို့ကြောင့် generated token တစ်လုံးစီအတွက် အလုပ်ပမာဏသည် O(n^2) မှ O(n) သို့ ကျဆင်းသည်။
"""

from __future__ import annotations

import argparse

DTYPE_BYTES = {"fp16": 2.0, "bf16": 2.0, "int8": 1.0, "int4": 0.5}
DTYPE_ORDER = ["fp16", "bf16", "int8", "int4"]
MIB = 1024.0 * 1024.0
RULE = "=" * 74
THIN = "-" * 74
SWEEP_CONTEXTS = [1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]


def kv_mb(context: int, layers: int, heads: int, head_dim: int, batch: int, dtype: str) -> float:
    """KV cache ၏ memory (MB)။ lab_context_budget.py သည် ဤပုံသေနည်းကို ပြန်လည် အသုံးပြုသည်။"""
    return batch * layers * 2 * context * heads * head_dim * DTYPE_BYTES[dtype] / MIB


def weight_mb(params_b: float, dtype: str) -> float:
    return params_b * 1e9 * DTYPE_BYTES[dtype] / MIB


def token_work_cached(n: int) -> int:
    return n


def token_work_uncached(n: int) -> int:
    return n * n


def print_report(context: int, layers: int, heads: int, head_dim: int, dtype: str,
                 batch: int, params_b: float) -> None:
    kv = kv_mb(context, layers, heads, head_dim, batch, dtype)
    wt = weight_mb(params_b, dtype)
    print(RULE)
    print("lab_kv_cache - KV cache memory နှင့် attention အလုပ်ပမာဏ (offline, deterministic)")
    print(f"context={context}  layers={layers}  heads={heads}  head_dim={head_dim}  "
          f"dtype={dtype}  batch={batch}  params={params_b}B")
    print(THIN)
    print(f"KV cache size            : {kv:>14,.2f} MB  ({kv / 1024.0:.4f} GB)")
    print(f"Weight size ({params_b}B {dtype})   : {wt:>14,.2f} MB  ({wt / 1024.0:.4f} GB)")
    print(f"KV / weight ratio        : {kv / wt:>14.4f}")
    print(f"Bytes per value ({dtype})   : {DTYPE_BYTES[dtype]:>14.2f}")
    print(THIN)
    cached = token_work_cached(context)
    uncached = token_work_uncached(context)
    print("Work per generated token at n = %d (score pairs):" % context)
    print(f"  with KV cache    : {cached:>16,}")
    print(f"  without cache    : {uncached:>16,}")
    print(f"  ratio            : {uncached / cached:>16,.1f}x  (cached O(n) vs uncached O(n^2))")
    print(THIN)
    print("မှတ်ချက် - KV cache သည် ထပ်တလဲလဲ တွက်ချက်မှုကို လျှော့ချသည်၊ သို့သော် sequence အရှည်၊ "
          "layer၊ batch နှင့် model configuration အပေါ် မှီခို၍ memory ကြီးထွားသည်။")
    print(RULE)


def print_sweep(layers: int, heads: int, head_dim: int, dtype: str, batch: int) -> None:
    print(RULE)
    print("lab_kv_cache - context sweep 1024..131072 (fp16 KV memory နှင့် per-token work)")
    print(THIN)
    print("  context      KV MB (fp16)   cached work   uncached work   ratio")
    for n in SWEEP_CONTEXTS:
        kv = kv_mb(n, layers, heads, head_dim, batch, "fp16")
        c = token_work_cached(n)
        u = token_work_uncached(n)
        print(f" {n:>9,}   {kv:>14,.2f}   {c:>13,}   {u:>14,}   {u / c:>6,.0f}x")
    print(THIN)
    print("မှတ်ချက် - context နှစ်ဆ တိုးလျှင် KV cache နှစ်ဆ တိုးသည်၊ cached work သည် linear ဖြစ်သည်၊ "
          "uncached work သည် quadratic ဖြစ်သည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    base = dict(layers=32, heads=32, head_dim=128, batch=1)

    a = kv_mb(8192, dtype="fp16", **base)
    b = kv_mb(16384, dtype="fp16", **base)
    dbl = abs(b - 2.0 * a) < 1e-9
    print(f"[OK] doubling the context doubles the KV cache ({a:,.2f} -> {b:,.2f} MB): {dbl}")
    ok = ok and dbl

    fp16 = kv_mb(8192, dtype="fp16", **base)
    int8 = kv_mb(8192, dtype="int8", **base)
    int4 = kv_mb(8192, dtype="int4", **base)
    half = abs(int8 - fp16 / 2.0) < 1e-9 and abs(int4 - fp16 / 4.0) < 1e-9
    print(f"[OK] int8 halves fp16 and int4 quarters it ({fp16:,.2f} / {int8:,.2f} / {int4:,.2f} MB): {half}")
    ok = ok and half

    w16 = weight_mb(7, "fp16")
    w8 = weight_mb(7, "int8")
    w4 = weight_mb(7, "int4")
    wr = abs(w8 / w16 - 1.0 / 2.0) < 1e-12 and abs(w4 / w16 - 1.0 / 4.0) < 1e-12
    print(f"[OK] weight size scales with the dtype byte width ({w16:,.0f} / {w8:,.0f} / {w4:,.0f} MB): {wr}")
    ok = ok and wr

    n = 8192
    lin = token_work_cached(2 * n) == 2 * token_work_cached(n)
    quad = token_work_uncached(2 * n) == 4 * token_work_uncached(n)
    print(f"[OK] cached decode grows linearly and uncached grows quadratically "
          f"({token_work_cached(n):,} -> {token_work_cached(2 * n):,} vs "
          f"{token_work_uncached(n):,} -> {token_work_uncached(2 * n):,}): {lin and quad}")
    ok = ok and lin and quad

    smaller = token_work_cached(n) < token_work_uncached(n)
    print(f"[OK] the cache saves work at this context ({token_work_uncached(n) / token_work_cached(n):,.0f}x): {smaller}")
    ok = ok and smaller

    print("[PASS] lab_kv_cache self-test passed." if ok else "[FAIL] lab_kv_cache self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="KV cache memory and attention-work lab (offline, deterministic).")
    ap.add_argument("--context", type=int, default=8192)
    ap.add_argument("--layers", type=int, default=32)
    ap.add_argument("--heads", type=int, default=32)
    ap.add_argument("--head-dim", type=int, default=128)
    ap.add_argument("--dtype", choices=DTYPE_ORDER, default="fp16")
    ap.add_argument("--batch", type=int, default=1)
    ap.add_argument("--params-b", type=float, default=7.0)
    ap.add_argument("--sweep", action="store_true", help="context 1024..131072 sweep")
    ap.add_argument("--self-test", action="store_true", help="assert the real cache properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.layers, args.heads, args.head_dim, args.dtype, args.batch)
        return 0
    print_report(args.context, args.layers, args.heads, args.head_dim, args.dtype, args.batch, args.params_b)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
