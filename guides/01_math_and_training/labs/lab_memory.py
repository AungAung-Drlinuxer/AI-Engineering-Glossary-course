#!/usr/bin/env python3
"""lab_memory - training VRAM ကို component အလိုက် ခွဲပြသည့် lab (weights, gradients, optimizer, activations)။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

Assumption များ
    d_model ကို params = 12 * layers * d_model^2 ဟူသည့် ခန့်မှန်းချက်မှ ဆင်းသက်စေသည်။
    weights   = params * bytes_per_parameter        (dtype)
    gradients = params * bytes_per_parameter        (dtype)
    optimizer = 2 * params * 4 bytes                (Adam fp32 moments)
    activations = batch * seq * layers * d_model * act_factor * bytes_per_parameter
                  act_factor = 10 (checkpointing off) / 2 (checkpointing on)
    activation checkpointing သည် forward တစ်ကြိမ် ပြန်တွက်သဖြင့် step FLOPs ကို 8/6 = 1.333 ဆ တင်သည်။
"""

from __future__ import annotations

import argparse
import math

DTYPE_BYTES = {"fp32": 4.0, "fp16": 2.0, "bf16": 2.0}
DTYPE_ORDER = ["fp32", "fp16", "bf16"]
ACT_FACTOR_OFF = 10.0
ACT_FACTOR_ON = 2.0
RECOMPUTE_MULTIPLIER = 8.0 / 6.0
USABLE_GIB = 64.0
GIB = 1024 ** 3
BATCH_SWEEP = (1, 2, 4, 8, 16, 32)
RULE = "=" * 92
THIN = "-" * 92


def gib(value_bytes: float) -> float:
    return value_bytes / GIB


def d_model_of(params_b: float, layers: int) -> int:
    return int(round(math.sqrt(params_b * 1e9 / (12.0 * layers))))


def components(params_b: float, batch: int, seq: int, layers: int, dtype: str, act_factor: float) -> dict:
    bpp = DTYPE_BYTES[dtype]
    params = params_b * 1e9
    d_model = d_model_of(params_b, layers)
    return {
        "weights": params * bpp,
        "gradients": params * bpp,
        "optimizer": 2.0 * params * 4.0,
        "activations": batch * seq * layers * d_model * act_factor * bpp,
    }


def total_gib(params_b: float, batch: int, seq: int, layers: int, dtype: str, act_factor: float) -> float:
    return gib(sum(components(params_b, batch, seq, layers, dtype, act_factor).values()))


def activation_gib(params_b: float, batch: int, seq: int, layers: int, dtype: str, act_factor: float) -> float:
    return gib(components(params_b, batch, seq, layers, dtype, act_factor)["activations"])


def print_report(params_b: float, batch: int, seq: int, layers: int, dtype: str, checkpointing: str) -> None:
    bpp = DTYPE_BYTES[dtype]
    d_model = d_model_of(params_b, layers)
    off = components(params_b, batch, seq, layers, dtype, ACT_FACTOR_OFF)
    on = components(params_b, batch, seq, layers, dtype, ACT_FACTOR_ON)
    total_off = gib(sum(off.values()))
    total_on = gib(sum(on.values()))
    print(RULE)
    print("lab_memory - training VRAM breakdown by component (offline, deterministic)")
    print("params=%.2fB  layers=%d  d_model=%d  batch=%d  seq=%d  dtype=%s  checkpointing=%s"
          % (params_b, layers, d_model, batch, seq, dtype, checkpointing))
    print("assumptions: weights and gradients in %s (%.1f B/param), Adam keeps two fp32 moments,"
          % (dtype, bpp))
    print("             activations = batch*seq*layers*d_model*act_factor*bpp with act_factor 10 (off) / 2 (on)")
    print(THIN)
    print("%-32s %18s %18s" % ("component (GiB)", "checkpointing=off", "checkpointing=on"))
    for key, label in (("weights", "weights"), ("gradients", "gradients"),
                       ("optimizer", "optimizer state (Adam fp32)"), ("activations", "activations")):
        print("%-32s %18.3f %18.3f" % (label, gib(off[key]), gib(on[key])))
    print(THIN)
    print("%-32s %18.3f %18.3f" % ("total VRAM", total_off, total_on))
    print("%-32s %18s %18s" % ("fits one 80 GB card (64 GiB usable)",
                               "yes" if total_off <= USABLE_GIB else "no",
                               "yes" if total_on <= USABLE_GIB else "no"))
    print("%-32s %18s %18.3f" % ("recompute overhead (x step FLOPs)", "none", RECOMPUTE_MULTIPLIER))
    print("မှတ်ချက် - activation checkpointing သည် activation memory ကို %.1fx လျှော့ပြီး"
          % (ACT_FACTOR_OFF / ACT_FACTOR_ON))
    print("         compute အပိုအလွှာ (step FLOPs x %.3f) ဖြင့် ဝယ်ယူပါသည်။" % RECOMPUTE_MULTIPLIER)
    print(RULE)


def print_sweep(params_b: float, seq: int, layers: int, dtype: str) -> None:
    print(RULE)
    print("lab_memory - batch sweep (params=%.2fB, seq=%d, layers=%d, dtype=%s)"
          % (params_b, seq, layers, dtype))
    print(THIN)
    print("%8s %18s %18s %18s %18s"
          % ("batch", "act off (GiB)", "total off (GiB)", "act on (GiB)", "total on (GiB)"))
    for batch in BATCH_SWEEP:
        print("%8d %18.3f %18.3f %18.3f %18.3f"
              % (batch,
                 activation_gib(params_b, batch, seq, layers, dtype, ACT_FACTOR_OFF),
                 total_gib(params_b, batch, seq, layers, dtype, ACT_FACTOR_OFF),
                 activation_gib(params_b, batch, seq, layers, dtype, ACT_FACTOR_ON),
                 total_gib(params_b, batch, seq, layers, dtype, ACT_FACTOR_ON)))
    print(THIN)
    print("မှတ်ချက် - batch နှစ်ဆ ဖြစ်လျှင် activation နှစ်ဆ တိုးသည်၊ weights၊ gradients နှင့်")
    print("         optimizer state သည် batch အပေါ် မမှီခိုပါ။")
    print(RULE)


def self_test() -> int:
    ok = True
    params_b, batch, seq, layers = 1.3, 8, 2048, 24

    def act(dtype: str, act_factor: float) -> float:
        return activation_gib(params_b, batch, seq, layers, dtype, act_factor)

    def tot(dtype: str, act_factor: float, b: int = batch) -> float:
        return total_gib(params_b, b, seq, layers, dtype, act_factor)

    def comp(dtype: str, act_factor: float) -> dict:
        return components(params_b, batch, seq, layers, dtype, act_factor)

    act_off = act("fp16", ACT_FACTOR_OFF)
    act_on = act("fp16", ACT_FACTOR_ON)
    ratio = abs(act_off / act_on - ACT_FACTOR_OFF / ACT_FACTOR_ON) < 1e-9
    print("[OK] activation checkpointing cuts activation memory %.1fx (%.3f -> %.3f GiB): %s"
          % (ACT_FACTOR_OFF / ACT_FACTOR_ON, act_off, act_on, ratio))
    ok = ok and ratio

    t_off = tot("fp16", ACT_FACTOR_OFF)
    t_on = tot("fp16", ACT_FACTOR_ON)
    lower = t_on < t_off
    print("[OK] the same settings need less total VRAM with checkpointing (%.3f -> %.3f GiB): %s"
          % (t_off, t_on, lower))
    ok = ok and lower

    w32 = gib(comp("fp32", ACT_FACTOR_OFF)["weights"])
    w16 = gib(comp("fp16", ACT_FACTOR_OFF)["weights"])
    scales = abs(w32 / w16 - 2.0) < 1e-9
    print("[OK] weights scale with the dtype byte width (fp32 %.3f GiB = 2 x fp16 %.3f GiB): %s"
          % (w32, w16, scales))
    ok = ok and scales

    o16 = comp("fp16", ACT_FACTOR_OFF)["optimizer"]
    o32 = comp("fp32", ACT_FACTOR_OFF)["optimizer"]
    state_free = o16 == o32
    print("[OK] the fp32 optimizer state does not change with the weight dtype (%.3f GiB): %s"
          % (gib(o16), state_free))
    ok = ok and state_free

    totals = [tot("fp16", ACT_FACTOR_OFF, b) for b in (1, 2, 4, 8)]
    growing = all(b > a for a, b in zip(totals, totals[1:]))
    print("[OK] total VRAM grows with the batch (%s): %s"
          % (", ".join("%.2f" % t for t in totals), growing))
    ok = ok and growing

    recompute = t_on < t_off and RECOMPUTE_MULTIPLIER > 1.0
    print("[OK] checkpointing trades compute for memory (step FLOPs x %.3f, VRAM falls): %s"
          % (RECOMPUTE_MULTIPLIER, recompute))
    ok = ok and recompute

    print("[PASS] lab_memory self-test passed." if ok else "[FAIL] lab_memory self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Training VRAM breakdown: weights, gradients, optimizer, activations (offline, deterministic).")
    ap.add_argument("--params-b", type=float, default=1.3, help="trainable parameters in billions")
    ap.add_argument("--batch", type=int, default=8, help="sequences per step")
    ap.add_argument("--seq", type=int, default=2048, help="tokens per sequence")
    ap.add_argument("--layers", type=int, default=24, help="number of layers")
    ap.add_argument("--dtype", choices=DTYPE_ORDER, default="fp16", help="weight and gradient dtype")
    ap.add_argument("--activation-checkpointing", choices=("on", "off"), default="off",
                    help="recompute activations during backward")
    ap.add_argument("--sweep", action="store_true", help="sweep the batch size")
    ap.add_argument("--self-test", action="store_true", help="assert the memory properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.params_b, args.seq, args.layers, args.dtype)
        return 0
    print_report(args.params_b, args.batch, args.seq, args.layers, args.dtype,
                 args.activation_checkpointing)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
