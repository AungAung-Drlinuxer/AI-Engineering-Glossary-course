#!/usr/bin/env python3
"""lab_quantization - Symmetric group-wise quantization ကို တိုင်းတာသည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

Weight matrix ကို seed မှ deterministic အနေဖြင့် ဖန်တီးသည် (64 x 64 = 4096 weight)။
Symmetric group-wise quantization -
    scale  = max(|w| in group) / qmax        qmax = 2^(bits-1) - 1
    q      = clamp(round(w / scale), -qmax, qmax)
    w_hat  = q * scale
ပြီးနောက် max absolute error, RMSE, cosine similarity နှင့် matvec output error ကို တိုင်းတာသည်။
"""

from __future__ import annotations

import argparse
import math
import random

ROWS = 64
COLS = 64
NUM_WEIGHTS = ROWS * COLS
MODEL_PARAMS_B = 7.0
SWEEP_BITS = [2, 3, 4, 5, 8]
RULE = "=" * 74
THIN = "-" * 74


def make_weights(seed: int) -> list[float]:
    rng = random.Random(seed)
    return [rng.gauss(0.0, 1.0) for _ in range(NUM_WEIGHTS)]


def make_input() -> list[float]:
    return [math.sin(0.7 * j) + math.cos(1.3 * j) for j in range(COLS)]


def quantize_groupwise(weights: list[float], bits: int, group_size: int) -> list[float]:
    qmax = (1 << (bits - 1)) - 1
    out = list(weights)
    for start in range(0, len(weights), group_size):
        group = weights[start:start + group_size]
        peak = max(abs(w) for w in group)
        scale = peak / qmax if peak > 0.0 else 1.0
        for j, w in enumerate(group):
            q = int(round(w / scale))
            if q > qmax:
                q = qmax
            elif q < -qmax:
                q = -qmax
            out[start + j] = q * scale
    return out


def matvec(matrix: list[float], vector: list[float]) -> list[float]:
    result = []
    for r in range(ROWS):
        row = matrix[r * COLS:(r + 1) * COLS]
        result.append(sum(row[c] * vector[c] for c in range(COLS)))
    return result


def metrics(weights: list[float], deq: list[float], x: list[float]) -> dict[str, float]:
    errs = [abs(a - b) for a, b in zip(weights, deq)]
    max_abs = max(errs)
    rmse = math.sqrt(sum(e * e for e in errs) / len(errs))
    dot = sum(a * b for a, b in zip(weights, deq))
    na = math.sqrt(sum(a * a for a in weights))
    nb = math.sqrt(sum(b * b for b in deq))
    cosine = dot / (na * nb)
    y = matvec(weights, x)
    yq = matvec(deq, x)
    diffs = [a - b for a, b in zip(yq, y)]
    rel = math.sqrt(sum(d * d for d in diffs)) / math.sqrt(sum(v * v for v in y))
    return {"max_abs": max_abs, "rmse": rmse, "cosine": cosine,
            "matvec_rel": rel, "matvec_max_abs": max(abs(d) for d in diffs)}


def run_point(bits: int, group_size: int, seed: int) -> dict[str, float]:
    weights = make_weights(seed)
    x = make_input()
    deq = quantize_groupwise(weights, bits, group_size)
    m = metrics(weights, deq, x)
    m["bits"] = float(bits)
    m["bytes_per_weight"] = bits / 8.0
    m["model_gb"] = MODEL_PARAMS_B * 1e9 * (bits / 8.0) / 1e9
    return m


def print_report(bits: int, group_size: int, seed: int) -> None:
    p = run_point(bits, group_size, seed)
    print(RULE)
    print("lab_quantization - symmetric group-wise quantization (offline, deterministic)")
    print(f"bits={bits}  group-size={group_size}  seed={seed}  matrix={ROWS}x{COLS} weights")
    print(THIN)
    print(f"Bytes per weight              : {p['bytes_per_weight']:>10.4f}")
    print(f"7B model size at this precision: {p['model_gb']:>9.4f} GB")
    print(f"Max absolute error            : {p['max_abs']:>10.6f}")
    print(f"RMSE                          : {p['rmse']:>10.6f}")
    print(f"Cosine similarity to fp32     : {p['cosine']:>10.6f}")
    print(f"Matvec output rel. error      : {p['matvec_rel']:>10.6f}")
    print(f"Matvec output max abs error   : {p['matvec_max_abs']:>10.6f}")
    print(THIN)
    print("မှတ်ချက် - bit အလုံးအစု လျှော့ချလျှင် memory ကျဆင်းသည်၊ quantization error တက်သည်။ "
          "bit အလုံးအစု တစ်ခုမှ တစ်ခုသို့ ရွေ့ခြင်းသည် end-to-end memory သို့မဟုတ် အရှိန် အချိုးကို "
          "အာမမခံနိုင်ပါ။")
    print(RULE)


def print_sweep(group_size: int, seed: int) -> None:
    print(RULE)
    print("lab_quantization - precision sweep (bits 2, 3, 4, 5, 8)")
    print(THIN)
    print("  bits  bytes/w   7B size GB   max abs err      RMSE   cosine   matvec rel")
    for bits in SWEEP_BITS:
        p = run_point(bits, group_size, seed)
        print(f" {bits:>5}  {p['bytes_per_weight']:>7.4f}  {p['model_gb']:>11.4f}  "
              f"{p['max_abs']:>13.6f}  {p['rmse']:>8.6f}  {p['cosine']:>7.5f}  {p['matvec_rel']:>11.6f}")
    print(THIN)
    print("မှတ်ချက် - bits တိုးလျှင် error ကျဆင်းသည်၊ size သည် bits/8 အချိုးအတိုင်း တိုးသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    seed = 0
    group_size = 64

    p8 = run_point(8, group_size, seed)
    p4 = run_point(4, group_size, seed)
    p2 = run_point(2, group_size, seed)

    lower_err = p8["rmse"] < p4["rmse"] < p2["rmse"]
    print(f"[OK] int8 error is below int4 error ({p8['rmse']:.6f} < {p4['rmse']:.6f}): {lower_err}")
    ok = ok and lower_err

    higher_cos = p8["cosine"] > p4["cosine"] > p2["cosine"]
    print(f"[OK] cosine similarity to fp32 improves with precision ({p2['cosine']:.5f} < "
          f"{p4['cosine']:.5f} < {p8['cosine']:.5f}): {higher_cos}")
    ok = ok and higher_cos

    ratio = p4["model_gb"] / p8["model_gb"]
    size_ok = abs(ratio - 0.5) < 1e-12 and abs(p2["model_gb"] / p8["model_gb"] - 0.25) < 1e-12
    print(f"[OK] size ratio matches bits/8 (int4/int8 = {ratio:.4f}): {size_ok}")
    ok = ok and size_ok

    rmses = [run_point(b, group_size, seed)["rmse"] for b in SWEEP_BITS]
    mono = all(rmses[i] > rmses[i + 1] for i in range(len(rmses) - 1))
    print(f"[OK] error falls monotonically across bits 2,3,4,5,8 ({rmses[0]:.4f} -> {rmses[-1]:.6f}): {mono}")
    ok = ok and mono

    again = run_point(4, group_size, seed)
    det_ok = again == p4
    print(f"[OK] quantization is deterministic for a fixed seed: {det_ok}")
    ok = ok and det_ok

    mat_ok = p8["matvec_rel"] < p4["matvec_rel"]
    print(f"[OK] matvec output error is smaller at higher precision ({p8['matvec_rel']:.6f} < "
          f"{p4['matvec_rel']:.6f}): {mat_ok}")
    ok = ok and mat_ok

    print("[PASS] lab_quantization self-test passed." if ok else "[FAIL] lab_quantization self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Symmetric group-wise quantization lab (offline, deterministic).")
    ap.add_argument("--bits", type=int, choices=[2, 3, 4, 5, 8], default=4)
    ap.add_argument("--group-size", type=int, default=64)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sweep", action="store_true", help="all precisions side by side")
    ap.add_argument("--self-test", action="store_true", help="assert the real quantization properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.group_size, args.seed)
        return 0
    print_report(args.bits, args.group_size, args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
