#!/usr/bin/env python3
"""lab_roofline - memory-bandwidth roofline for autoregressive decode.

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

ပုံသေနည်းများ —
    weight_bytes    = params_b * 1e9 * bytes_per_element
    kv_per_token    = 2 (K နှင့် V) * layers * heads * head_dim * bytes_per_element
    bytes_per_step  = weight_bytes + batch * kv_per_token
    ceiling_tps     = batch * bandwidth_bytes_per_s / bytes_per_step
    achieved_tps    = ceiling_tps * efficiency
    usd_per_million = price_per_hour / (achieved_tps * 3600) * 1e6

bandwidth၊ efficiency၊ GPU-hour စျေးနှုန်းနှင့် KV geometry သည် stated assumption ဖြစ်သည်။
decode သည် compute မဟုတ်ဘဲ memory bandwidth ဖြင့် ကန့်သတ်ခံရသည်ဟု ယူဆသည်။
"""

from __future__ import annotations

import argparse

GB = 1_000_000_000.0
KIB = 1024.0
DTYPE_BYTES = {"fp16": 2.0, "bf16": 2.0, "int8": 1.0, "int4": 0.5}
KV_LAYERS, KV_HEADS, KV_HEAD_DIM = 32, 32, 128
RULE = "=" * 74
THIN = "-" * 74
BATCHES = (1, 2, 4, 8, 16, 32, 64, 128, 256)


def kv_per_token_kib(dtype: str) -> float:
    return 2.0 * KV_LAYERS * KV_HEADS * KV_HEAD_DIM * DTYPE_BYTES[dtype] / KIB


def ceiling_tps(batch: float, weight_bytes: float, bandwidth_bps: float,
                kv_bytes: float) -> float:
    return batch * bandwidth_bps / (weight_bytes + batch * kv_bytes)


def cost_per_million(tps: float, price_per_hour: float) -> float:
    return price_per_hour / (tps * 3600.0) * 1e6


def print_report(args: argparse.Namespace) -> None:
    bpw = DTYPE_BYTES[args.dtype]
    weight_bytes = args.params_b * 1e9 * bpw
    kv_bytes = kv_per_token_kib(args.dtype) * KIB
    bandwidth_bps = args.bandwidth_gbps * GB
    step = weight_bytes + args.batch * kv_bytes
    top = ceiling_tps(args.batch, weight_bytes, bandwidth_bps, kv_bytes)
    achieved = top * args.efficiency
    cpm = cost_per_million(achieved, args.gpu_hour_cost)
    print(RULE)
    print("lab_roofline - memory-bandwidth roofline for decode (offline, deterministic)")
    print(f"bandwidth={args.bandwidth_gbps:.1f} GB/s (assumption)  "
          f"params={args.params_b:.1f}B {args.dtype}  batch={args.batch}")
    print(f"KV={kv_per_token_kib(args.dtype):.1f} KiB per token per sequence "
          f"({KV_LAYERS}L/{KV_HEADS}H/{KV_HEAD_DIM}D, assumption)  "
          f"efficiency={args.efficiency * 100:.1f}% (assumption)")
    print(f"GPU-hour price=USD {args.gpu_hour_cost:.2f} (assumption, varies by vendor)")
    print(THIN)
    print(f"weight bytes per step        : {int(weight_bytes):>14} B  "
          f"({weight_bytes / GB:.3f} GB)")
    print(f"KV bytes per token per seq   : {int(kv_bytes):>14} B  "
          f"({kv_bytes / KIB:.3f} KiB)")
    print(f"bytes per decode step        : {int(step):>14} B  (weights + batch * KV)")
    print(f"tokens/s ceiling             : {top:>14.1f}")
    print(f"tokens/s at {args.efficiency * 100:.1f}% efficiency  : {achieved:>14.1f}")
    print(f"time per decode step (ms)    : {1000.0 / top:>14.3f}")
    print(f"cost per million tokens      : {cpm:>14.4f} USD")
    print(THIN)
    print("batch sweep (weights are read once per step, KV cache once per sequence):")
    print(f"{'batch':<8}{'bytes/step':>15}{'tok/s ceiling':>16}{'tok/s achieved':>16}"
          f"{'USD/1e6 tokens':>16}")
    for batch in BATCHES:
        b_step = weight_bytes + batch * kv_bytes
        top_b = ceiling_tps(batch, weight_bytes, bandwidth_bps, kv_bytes)
        ach_b = top_b * args.efficiency
        print(f"{batch:<8}{b_step:>15.4e}{top_b:>16.1f}{ach_b:>16.1f}"
              f"{cost_per_million(ach_b, args.gpu_hour_cost):>16.4f}")
    print(THIN)
    print("မှတ်ချက် - batch တိုးလျှင် weight byte သည် sequence အရေအတွက်ဖြင့် ပြန်လည် "
          "အသုံးပြုခံရသည်၊ ထို့ကြောင့် cost per million tokens ကျဆင်းသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    bandwidth = 3350.0 * GB
    weights = 8.0 * 1e9 * 2.0
    kv = kv_per_token_kib("fp16") * KIB

    kv_ok = abs(kv_per_token_kib("int8") - kv_per_token_kib("fp16") / 2.0) < 1e-9
    print(f"[OK] int8 halves the KV bytes per token "
          f"({kv_per_token_kib('fp16'):.1f} -> {kv_per_token_kib('int8'):.1f} KiB): {kv_ok}")
    ok = ok and kv_ok

    w1 = 8.0 * 1e9 * DTYPE_BYTES["fp16"]
    w2 = 8.0 * 1e9 * DTYPE_BYTES["int8"]
    w_ok = abs(w2 - w1 / 2.0) < 1e-9
    print(f"[OK] int8 halves the weight bytes ({w1:.3e} -> {w2:.3e} B): {w_ok}")
    ok = ok and w_ok

    t1 = ceiling_tps(1, weights, bandwidth, kv)
    t2 = ceiling_tps(2, weights, bandwidth, kv)
    mono = t2 > t1 and t2 < 2.0 * t1
    print(f"[OK] throughput rises sublinearly with batch ({t1:.1f} -> {t2:.1f} tok/s "
          f"for 2x batch): {mono}")
    ok = ok and mono

    c1 = cost_per_million(1000.0, 2.50)
    c2 = cost_per_million(2000.0, 2.50)
    cost_ok = abs(c1 - 2.0 * c2) < 1e-9
    print(f"[OK] doubling throughput halves cost per million tokens "
          f"({c1:.4f} -> {c2:.4f} USD): {cost_ok}")
    ok = ok and cost_ok

    step = weights + 4 * kv
    step_ok = abs(step - (weights + 4 * kv)) < 1e-9
    kvc = ceiling_tps(4, weights, bandwidth, kv)
    form_ok = abs(kvc - 4 * bandwidth / step) < 1e-6
    print(f"[OK] bytes per step = weights + batch * KV and defines the ceiling "
          f"({step:.3e} B -> {kvc:.1f} tok/s): {step_ok and form_ok}")
    ok = ok and step_ok and form_ok

    print("[PASS] lab_roofline self-test passed." if ok
          else "[FAIL] lab_roofline self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Roofline throughput and cost lab (offline, deterministic).")
    ap.add_argument("--bandwidth-gbps", type=float, default=3350.0)
    ap.add_argument("--params-b", type=float, default=8.0)
    ap.add_argument("--dtype", default="fp16", choices=sorted(DTYPE_BYTES))
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--gpu-hour-cost", type=float, default=2.50)
    ap.add_argument("--efficiency", type=float, default=0.75)
    ap.add_argument("--sweep", action="store_true", help="sweep batch 1 .. 256")
    ap.add_argument("--self-test", action="store_true", help="assert the roofline properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    print_report(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
