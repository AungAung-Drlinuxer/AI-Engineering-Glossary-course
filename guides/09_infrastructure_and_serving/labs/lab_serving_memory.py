#!/usr/bin/env python3
"""lab_serving_memory - served-model memory budget: weights, KV cache, activations.

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

ပုံသေနည်းများ —
    weights        = params_b * 1e9 * bytes_per_element
    kv_per_seq     = 2 (K နှင့် V) * layers * heads * head_dim * context * bytes_per_element
    kv_total       = kv_per_seq * batch
    act_per_seq    = context * d_model * ACTIVATION_FACTOR * bytes_per_element
    act_total      = act_per_seq * batch
    total_vram     = weights + kv_total + act_total
    max_batch      = floor((budget - weights) / (kv_per_seq + act_per_seq))

ACTIVATION_FACTOR နှင့် budget သည် stated assumption ဖြစ်သည်။
"""

from __future__ import annotations

import argparse

GIB = 1024.0 ** 3
DTYPE_BYTES = {"fp16": 2.0, "bf16": 2.0, "int8": 1.0, "int4": 0.5}
ACTIVATION_FACTOR = 4.0
RULE = "=" * 74
THIN = "-" * 74


def weights_gib(params_b: float, dtype: str) -> float:
    return params_b * 1e9 * DTYPE_BYTES[dtype] / GIB


def kv_per_seq_gib(layers: int, heads: int, head_dim: int, context: int,
                   dtype: str) -> float:
    return 2.0 * layers * heads * head_dim * context * DTYPE_BYTES[dtype] / GIB


def act_per_seq_gib(heads: int, head_dim: int, context: int, dtype: str) -> float:
    return context * (heads * head_dim) * DTYPE_BYTES[dtype] * ACTIVATION_FACTOR / GIB


def total_gib(params_b: float, layers: int, heads: int, head_dim: int,
              context: int, batch: int, dtype: str) -> float:
    return (weights_gib(params_b, dtype)
            + batch * kv_per_seq_gib(layers, heads, head_dim, context, dtype)
            + batch * act_per_seq_gib(heads, head_dim, context, dtype))


def max_batch(params_b: float, layers: int, heads: int, head_dim: int,
              context: int, dtype: str, budget_gib: float) -> int:
    per_seq = (kv_per_seq_gib(layers, heads, head_dim, context, dtype)
               + act_per_seq_gib(heads, head_dim, context, dtype))
    return int((budget_gib - weights_gib(params_b, dtype)) // per_seq)


def print_report(args: argparse.Namespace) -> None:
    d_model = args.heads * args.head_dim
    w = weights_gib(args.params_b, args.dtype)
    per_seq = kv_per_seq_gib(args.layers, args.heads, args.head_dim, args.context, args.dtype)
    act_seq = act_per_seq_gib(args.heads, args.head_dim, args.context, args.dtype)
    kv_tot = per_seq * args.batch
    act_tot = act_seq * args.batch
    total = w + kv_tot + act_tot
    fit = max_batch(args.params_b, args.layers, args.heads, args.head_dim,
                    args.context, args.dtype, args.budget_gib)
    print(RULE)
    print("lab_serving_memory - weights, KV cache, activations and batch headroom")
    print(f"params={args.params_b:.1f}B  layers={args.layers}  heads={args.heads}  "
          f"head_dim={args.head_dim}  d_model={d_model}  context={args.context}  "
          f"batch={args.batch}  dtype={args.dtype}")
    print(f"budget={args.budget_gib:.3f} GiB (assumption)   "
          f"activation factor={ACTIVATION_FACTOR:.2f} (assumption)")
    print(THIN)
    print(f"weights                     : {w:>11.3f} GiB  ({int(w * GIB)} B)")
    print(f"KV cache per sequence       : {per_seq:>11.3f} GiB  ({int(per_seq * GIB)} B)")
    print(f"KV cache total ({args.batch:>3})        : {kv_tot:>11.3f} GiB")
    print(f"activations per sequence    : {act_seq:>11.3f} GiB")
    print(f"activations total ({args.batch:>3})     : {act_tot:>11.3f} GiB")
    print(f"total VRAM (weights+KV+act) : {total:>11.3f} GiB")
    if total <= args.budget_gib:
        print(f"fits budget {args.budget_gib:.3f} GiB    : yes (headroom "
              f"{args.budget_gib - total:.3f} GiB)")
    else:
        print(f"fits budget {args.budget_gib:.3f} GiB    : no  (over by "
              f"{total - args.budget_gib:.3f} GiB)")
    print(f"largest batch that fits     : {fit}")
    print(THIN)
    print("batch sweep (KV cache and activations scale with batch, weights do not):")
    print(f"{'batch':<7}{'KV total GiB':>15}{'act GiB':>11}{'total GiB':>12}"
          f"{'headroom GiB':>15}")
    for batch in (1, 8, 16, 32):
        tot = total_gib(args.params_b, args.layers, args.heads, args.head_dim,
                        args.context, batch, args.dtype)
        print(f"{batch:<7}{per_seq * batch:>15.3f}{act_seq * batch:>11.3f}"
              f"{tot:>12.3f}{args.budget_gib - tot:>15.3f}")
    print(THIN)
    print("မှတ်ချက် - KV cache သည် context နှင့် batch အပေါ် မှီခို၍ ကြီးထွားသည်၊ weight သည် "
          "batch အပေါ် မမှီခိုပါ။")
    print(RULE)


def print_sweep(args: argparse.Namespace) -> None:
    print(RULE)
    print("lab_serving_memory - batch sweep (weights fixed, KV cache and activations grow)")
    print(f"params={args.params_b:.1f}B  context={args.context}  dtype={args.dtype}  "
          f"budget={args.budget_gib:.3f} GiB")
    print(THIN)
    print(f"{'batch':<8}{'KV total GiB':>15}{'act GiB':>11}{'total GiB':>12}"
          f"{'fits':>7}{'headroom GiB':>15}")
    for batch in (1, 2, 4, 8, 16, 32, 64, 128, 256):
        tot = total_gib(args.params_b, args.layers, args.heads, args.head_dim,
                        args.context, batch, args.dtype)
        kv_tot = kv_per_seq_gib(args.layers, args.heads, args.head_dim,
                                args.context, args.dtype) * batch
        act_tot = act_per_seq_gib(args.heads, args.head_dim, args.context,
                                  args.dtype) * batch
        print(f"{batch:<8}{kv_tot:>15.3f}{act_tot:>11.3f}{tot:>12.3f}"
              f"{'yes' if tot <= args.budget_gib else 'no':>7}"
              f"{args.budget_gib - tot:>15.3f}")
    print(THIN)
    print(f"largest batch that fits {args.budget_gib:.3f} GiB = "
          f"{max_batch(args.params_b, args.layers, args.heads, args.head_dim, args.context, args.dtype, args.budget_gib)}")
    print(RULE)


def self_test() -> int:
    ok = True

    kv1 = kv_per_seq_gib(32, 32, 128, 8192, "fp16")
    kv2 = kv_per_seq_gib(32, 32, 128, 16384, "fp16")
    dbl_ok = abs(kv2 - 2.0 * kv1) < 1e-9
    print(f"[OK] doubling context doubles the KV cache ({kv1:.3f} -> {kv2:.3f} GiB): {dbl_ok}")
    ok = ok and dbl_ok

    kv_int8 = kv_per_seq_gib(32, 32, 128, 8192, "int8")
    half_ok = abs(kv_int8 - kv1 / 2.0) < 1e-9
    print(f"[OK] int8 halves the KV cache against fp16 ({kv1:.3f} -> {kv_int8:.3f} GiB): {half_ok}")
    ok = ok and half_ok

    tot1 = total_gib(8.0, 32, 32, 128, 8192, 1, "fp16")
    tot2 = total_gib(8.0, 32, 32, 128, 8192, 2, "fp16")
    kv_act = kv1 + act_per_seq_gib(32, 128, 8192, "fp16")
    grow_ok = abs((tot2 - tot1) - kv_act) < 1e-9
    print(f"[OK] one extra batch slot adds one KV cache plus one activation workspace "
          f"({kv_act:.3f} GiB): {grow_ok}")
    ok = ok and grow_ok

    w1 = weights_gib(8.0, "fp16")
    w_batch = total_gib(8.0, 32, 32, 128, 8192, 64, "fp16") - w1 - 64 * kv_act
    weights_ok = abs(w_batch) < 1e-9
    print(f"[OK] the weights footprint is independent of batch "
          f"({w1:.3f} GiB): {weights_ok}")
    ok = ok and weights_ok

    mb = max_batch(8.0, 32, 32, 128, 8192, "fp16", 72.0)
    fits_ok = total_gib(8.0, 32, 32, 128, 8192, mb, "fp16") <= 72.0
    over_ok = total_gib(8.0, 32, 32, 128, 8192, mb + 1, "fp16") > 72.0
    print(f"[OK] largest batch that fits is tight ({mb} fits, {mb + 1} overflows): "
          f"{fits_ok and over_ok}")
    ok = ok and fits_ok and over_ok

    print("[PASS] lab_serving_memory self-test passed." if ok
          else "[FAIL] lab_serving_memory self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Served-model memory budget lab (offline, deterministic).")
    ap.add_argument("--params-b", type=float, default=8.0)
    ap.add_argument("--layers", type=int, default=32)
    ap.add_argument("--heads", type=int, default=32)
    ap.add_argument("--head-dim", type=int, default=128)
    ap.add_argument("--context", type=int, default=8192)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--dtype", default="fp16", choices=sorted(DTYPE_BYTES))
    ap.add_argument("--budget-gib", type=float, default=72.0)
    ap.add_argument("--sweep", action="store_true", help="sweep batch 1 .. 256")
    ap.add_argument("--self-test", action="store_true", help="assert the memory properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args)
        return 0
    print_report(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
