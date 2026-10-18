#!/usr/bin/env python3
"""lab_context_budget - Token Budget (context window) ကို တွက်ပြီး ဖြေရှင်းနည်းများ ပြသည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

Token budget
    used = system + retrieved + history + reserve_output
    fits = used <= window        headroom = window - used
    overflow = used - window     (used > window ဖြစ်ပါကသာ)

KV cache ပုံသေနည်းသည် lab_kv_cache.py မှ အတူတူ ဖြစ်သည် -
    kv_mb = layers * 2 * n * heads * head_dim * bytes_per_element / MiB
"""

from __future__ import annotations

import argparse

DTYPE_BYTES = {"fp16": 2.0, "bf16": 2.0, "int8": 1.0, "int4": 0.5}
DEFAULT_LAYERS = 32
DEFAULT_HEADS = 32
DEFAULT_HEAD_DIM = 128
DEFAULT_DTYPE = "fp16"
KEEP_RETRIEVED = 8000
HISTORY_KEEP_FRACTION = 0.25
MIB = 1024.0 * 1024.0
RULE = "=" * 74
THIN = "-" * 74


def kv_mb(context: int, layers: int = DEFAULT_LAYERS, heads: int = DEFAULT_HEADS,
          head_dim: int = DEFAULT_HEAD_DIM, dtype: str = DEFAULT_DTYPE, batch: int = 1) -> float:
    """lab_kv_cache.py ၏ ပုံသေနည်း အတူတူ (batch 1)။"""
    return batch * layers * 2 * context * heads * head_dim * DTYPE_BYTES[dtype] / MIB


def budget(window: int, system: int, retrieved: int, history: int, reserve: int) -> dict[str, float]:
    used = system + retrieved + history + reserve
    return {
        "used": float(used),
        "headroom": float(window - used),
        "overflow": float(max(0, used - window)),
        "fits": 1.0 if used <= window else 0.0,
        "window": float(window),
    }


def remedies(retrieved: int, history: int, system: int) -> list[tuple[str, int]]:
    return [
        (f"shrink retrieved context to {KEEP_RETRIEVED:,} tokens",
         max(0, retrieved - KEEP_RETRIEVED)),
        (f"summarise history to {int(HISTORY_KEEP_FRACTION * 100)}% of its size",
         max(0, history - int(history * HISTORY_KEEP_FRACTION))),
        ("trim the system prompt by half", max(0, system // 2)),
    ]


def print_report(window: int, system: int, retrieved: int, history: int, reserve: int) -> None:
    b = budget(window, system, retrieved, history, reserve)
    rem = remedies(retrieved, history, system)
    total_freed = sum(v for _, v in rem)
    used_after = b["used"] - total_freed
    print(RULE)
    print("lab_context_budget - token budget breakdown (offline, deterministic)")
    print(f"window={window:,}  system={system:,}  retrieved={retrieved:,}  "
          f"history={history:,}  reserve-output={reserve:,}")
    print(THIN)
    print(f"  system prompt             : {system:>10,}")
    print(f"  retrieved context         : {retrieved:>10,}")
    print(f"  conversation history      : {history:>10,}")
    print(f"  reserved for output       : {reserve:>10,}")
    print(f"  used                      : {b['used']:>10,.0f}  ({b['used'] / window * 100:.2f}% of window)")
    if b["fits"]:
        print(f"  status                    : {'FITS':>10}  headroom {b['headroom']:,.0f} tokens")
    else:
        print(f"  status                    : {'OVERFLOW':>10}  shortfall {b['overflow']:,.0f} tokens")
    print(THIN)
    print("Remedies (each frees tokens):")
    for label, freed in rem:
        print(f"  {label:<58} frees {freed:>8,}")
    print(f"  total freed {total_freed:,} tokens -> used after remedies {used_after:,.0f}, "
          f"headroom {window - used_after:,.0f}")
    kv = kv_mb(window)
    print(THIN)
    print(f"KV cache this window costs : {kv:>12,.2f} MB  ({kv / 1024.0:.2f} GB, "
          f"layers={DEFAULT_LAYERS}, heads={DEFAULT_HEADS}, head_dim={DEFAULT_HEAD_DIM}, {DEFAULT_DTYPE})")
    print("မှတ်ချက် - budget သည် reserved output ပါဝင်မှသာ လုံခြုံသည်၊ ထို့ကြောင့် reserve-output ကို "
          "နုတ်မထားရ။")
    print(RULE)


def self_test() -> int:
    ok = True

    fits = budget(128000, 600, 24000, 30000, 4096)
    fit_ok = fits["fits"] == 1.0 and fits["headroom"] > 0 and fits["used"] + fits["headroom"] == 128000.0
    print(f"[OK] a budget that fits stays positive (headroom {fits['headroom']:,.0f} tokens): {fit_ok}")
    ok = ok and fit_ok

    over = budget(128000, 600, 24000, 100000, 4096)
    over_ok = (over["fits"] == 0.0 and over["overflow"] > 0
               and abs(over["overflow"] - (over["used"] - 128000.0)) < 1e-9
               and over["headroom"] < 0)
    print(f"[OK] an overflow reports the shortfall ({over['overflow']:,.0f} tokens): {over_ok}")
    ok = ok and over_ok

    rem = remedies(24000, 100000, 600)
    freed = sum(v for _, v in rem)
    fixed = over["used"] - freed <= 128000.0
    positive = all(v > 0 for _, v in rem)
    print(f"[OK] the remedies free {freed:,} tokens and resolve the overflow: {positive and fixed}")
    ok = ok and positive and fixed

    kv1 = kv_mb(8192)
    kv2 = kv_mb(16384)
    kv_ok = abs(kv2 - 2.0 * kv1) < 1e-9
    print(f"[OK] the KV cache for the window doubles with the window ({kv1:,.2f} -> {kv2:,.2f} MB): {kv_ok}")
    ok = ok and kv_ok

    smaller = budget(128000, 600, 24000, 30000, 4096)
    shrink = remedies(24000, 30000, 600)
    shrink_ok = shrink[0][1] == 16000 and shrink[1][1] == 22500 and shrink[2][1] == 300
    print(f"[OK] each remedy reports the token amount it frees: {shrink_ok}")
    ok = ok and shrink_ok and smaller["fits"] == 1.0

    print("[PASS] lab_context_budget self-test passed." if ok else "[FAIL] lab_context_budget self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Context window token-budget lab (offline, deterministic).")
    ap.add_argument("--window", type=int, default=128000)
    ap.add_argument("--system", type=int, default=600)
    ap.add_argument("--retrieved", type=int, default=24000)
    ap.add_argument("--history", type=int, default=30000)
    ap.add_argument("--reserve-output", type=int, default=4096)
    ap.add_argument("--self-test", action="store_true", help="assert the real budget properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    print_report(args.window, args.system, args.retrieved, args.history, args.reserve_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
