#!/usr/bin/env python3
"""lab_sampling - Temperature, Top-k Sampling နှင့် Nucleus Sampling (Top-p) ကို လက်တွေ့ စမ်းသပ်သည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

Fixed 10-token logits vector (peaked middle, two tail tokens):
    index  token    logit
    0      the       2.0
    1      a         2.4
    2      cat       2.9
    3      sat       3.4
    4      on        4.6   <- peak (အလယ်)
    5      mat       3.2
    6      dog       2.7
    7      ran       2.1
    8      zebra    -1.5   <- tail token
    9      quokka   -2.5   <- tail token

Pipeline အစဉ်: temperature -> top-k -> top-p။ Temperature သည် logits ကို အတိုင်းအတာ ချိန်ညှိသည်။
Top-k သည် အမြင့်ဆုံး score ရှိသည့် candidate k လုံးကို ချန်ထားသည်။ Top-p သည် cumulative
probability သတ်မှတ်ချက် ပြည့်သည့် အသေးဆုံး အစုကို ချန်ထားသည်။ Temperature 0 ကို greedy
decoding အဖြစ် သတ်မှတ်သည် (argmax သည် probability 1.0 ရရှိသည်)။
"""

from __future__ import annotations

import argparse
import math
import random

TOKENS = ["the", "a", "cat", "sat", "on", "mat", "dog", "ran", "zebra", "quokka"]
LOGITS = [2.0, 2.4, 2.9, 3.4, 4.6, 3.2, 2.7, 2.1, -1.5, -2.5]
SWEEP_TEMPERATURES = [0.1, 0.25, 0.5, 1.0, 1.5, 2.0]
RULE = "=" * 74
THIN = "-" * 74


def softmax(logits: list[float], temperature: float) -> list[float]:
    """logits / temperature ကို softmax လုပ်သည်။ temperature <= 0 ဖြစ်ပါက one-hot (greedy)။"""
    n = len(logits)
    if temperature <= 0.0:
        best = 0
        for i in range(1, n):
            if logits[i] > logits[best]:
                best = i
        out = [0.0] * n
        out[best] = 1.0
        return out
    scaled = [x / temperature for x in logits]
    top = max(scaled)
    exps = [math.exp(x - top) for x in scaled]
    total = sum(exps)
    return [e / total for e in exps]


def apply_top_k(probs: list[float], k: int) -> list[float]:
    """အမြင့်ဆုံး k လုံးကို ချန်ထားပြီး ပြန်လည် normalize လုပ်သည်။ k <= 0 သို့မဟုတ် k >= len ဖြစ်ပါက မပြောင်းလဲ။"""
    n = len(probs)
    if k <= 0 or k >= n:
        return list(probs)
    order = sorted(range(n), key=lambda i: (-probs[i], i))[:k]
    out = [0.0] * n
    total = sum(probs[i] for i in order)
    for i in order:
        out[i] = probs[i] / total
    return out


def apply_top_p(probs: list[float], p: float) -> list[float]:
    """cumulative probability သတ်မှတ်ချက် p ပြည့်သည့် အသေးဆုံး အစုကို ချန်ထားသည်။"""
    n = len(probs)
    if p >= 1.0:
        return list(probs)
    order = sorted(range(n), key=lambda i: (-probs[i], i))
    keep: list[int] = []
    cum = 0.0
    for i in order:
        keep.append(i)
        cum += probs[i]
        if cum >= p:
            break
    if p <= 0.0:
        keep = order[:1]
    out = [0.0] * n
    total = sum(probs[i] for i in keep)
    for i in keep:
        out[i] = probs[i] / total
    return out


def entropy(probs: list[float]) -> float:
    """နာကျယ်လ်အတွင်း Shannon entropy (nats)။"""
    h = 0.0
    for p in probs:
        if p > 0.0:
            h -= p * math.log(p)
    return h


def sample_index(probs: list[float], seed: int) -> int:
    """index အစဉ်အတိုင်း inverse-CDF ဖြင့် token တစ်လုံး ဆွဲထုတ်သည် (seed အတူညီပါက ရလဒ် တူညီသည်)။"""
    r = random.Random(seed).random()
    cum = 0.0
    pick = len(probs) - 1
    for i, p in enumerate(probs):
        cum += p
        if r < cum:
            pick = i
            break
    return pick


def distribution(temperature: float, top_k: int, top_p: float) -> list[float]:
    probs = softmax(LOGITS, temperature)
    probs = apply_top_k(probs, top_k)
    probs = apply_top_p(probs, top_p)
    return probs


def print_report(temperature: float, top_k: int, top_p: float, seed: int) -> None:
    p_temp = softmax(LOGITS, temperature)
    p_topk = apply_top_k(p_temp, top_k)
    p_topp = apply_top_p(p_topk, top_p)
    order = sorted(range(len(LOGITS)), key=lambda i: (-LOGITS[i], i))

    print(RULE)
    print("lab_sampling - temperature / top-k / top-p (deterministic, offline)")
    print(f"temperature={temperature}  top-k={top_k}  top-p={top_p}  seed={seed}")
    print("Pipeline: logits -> temperature -> top-k -> top-p -> cumulative sum")
    print(THIN)
    print(" rank  token      logit    p(T)     p(top-k)  p(top-p)   cumsum")
    cum = 0.0
    for rank, i in enumerate(order, start=1):
        cum += p_topp[i]
        print(f" {rank:>4}  {TOKENS[i]:<9} {LOGITS[i]:>6.2f}  {p_temp[i]:>8.4f}  "
              f"{p_topk[i]:>8.4f}  {p_topp[i]:>8.4f}  {cum:>7.4f}")
    print(THIN)
    pick = sample_index(p_topp, seed)
    kept = sum(1 for p in p_topp if p > 0.0)
    print(f"Sampled token: {TOKENS[pick]} (index {pick})")
    print(f"Candidates kept: {kept}/10   entropy: {entropy(p_topp):.4f} nats")
    print("မှတ်ချက် - temperature မြင့်လျှင် ဖြန့်ဖြူးမှု ပိုပြန့်သည်၊ top-k နှင့် top-p သည် "
          "အမြီးရှည် candidate များကို ဖယ်ရှားသည်။")
    print(RULE)


def print_sweep(top_k: int, top_p: float) -> None:
    print(RULE)
    print("lab_sampling - temperature sweep (temperature သာ ပြောင်းလဲသည်၊ top-k/top-p မပါဝင်ပါ)")
    print(THIN)
    print(" temperature   P(top token)     entropy (nats)")
    for t in SWEEP_TEMPERATURES:
        probs = softmax(LOGITS, t)
        print(f" {t:>11.2f}   {max(probs):>12.4f}     {entropy(probs):>13.4f}")
    print(THIN)
    print("မှတ်ချက် - temperature မြင့်လာသည်နှင့်အမျှ P(top token) ကျဆင်းပြီး entropy တက်သည်။")
    print(RULE)


def run_interactive() -> None:
    print("Interactive mode - Enter သီးသန့်ထည့်ပါက ထွက်မည်။")
    while True:
        try:
            raw = input("temperature [1.0]: ").strip()
            if raw == "":
                break
            temperature = float(raw)
            top_k = int(input("top-k [5]: ").strip() or "5")
            top_p = float(input("top-p [0.9]: ").strip() or "0.9")
            seed = int(input("seed [0]: ").strip() or "0")
        except EOFError:
            break
        except ValueError:
            print("တန်ဖိုး မမှန်ပါ - နံပါတ် ထည့်ပါ။")
            continue
        print_report(temperature, top_k, top_p, seed)
    print("Interactive mode ပြီးဆုံးပါသည်။")


def self_test() -> int:
    ok = True

    one_hot = softmax(LOGITS, 0.0)
    argmax = max(range(len(LOGITS)), key=lambda i: LOGITS[i])
    greedy_ok = one_hot[argmax] == 1.0 and sum(one_hot) == 1.0
    picks = {sample_index(softmax(LOGITS, 0.0), s) for s in (0, 1, 2, 7, 42)}
    greedy_ok = greedy_ok and picks == {argmax} and argmax == 4
    print(f"[OK] temperature 0 keeps the argmax token '{TOKENS[argmax]}' with probability 1.0: {greedy_ok}")
    ok = ok and greedy_ok

    ents = [entropy(softmax(LOGITS, t)) for t in SWEEP_TEMPERATURES]
    rising = all(ents[i] < ents[i + 1] for i in range(len(ents) - 1))
    print(f"[OK] higher temperature flattens the distribution (entropy {ents[0]:.4f} -> {ents[-1]:.4f}): {rising}")
    ok = ok and rising

    tk = apply_top_k(softmax(LOGITS, 1.0), 3)
    nz = sum(1 for p in tk if p > 0.0)
    tk_ok = nz == 3 and abs(sum(tk) - 1.0) < 1e-12
    print(f"[OK] top-k keeps exactly k candidates and renormalizes to 1.0: {tk_ok}")
    ok = ok and tk_ok

    tp = apply_top_p(softmax(LOGITS, 1.0), 0.9)
    order = sorted(range(len(tp)), key=lambda i: (-LOGITS[i], i))
    run = 0.0
    smallest = 0
    for i in order:
        run += softmax(LOGITS, 1.0)[i]
        smallest += 1
        if run >= 0.9:
            break
    tp_ok = sum(1 for p in tp if p > 0.0) == smallest and abs(sum(tp) - 1.0) < 1e-12
    print(f"[OK] top-p keeps the smallest set reaching the cumulative threshold: {tp_ok}")
    ok = ok and tp_ok

    d1 = distribution(0.8, 5, 0.9)
    s1 = sample_index(d1, 11)
    s2 = sample_index(d1, 11)
    s3 = sample_index(d1, 12)
    det_ok = s1 == s2 and 0 <= s3 < len(TOKENS)
    print(f"[OK] sampling is deterministic for a fixed seed: {det_ok}")
    ok = ok and det_ok

    print("[PASS] lab_sampling self-test passed." if ok else "[FAIL] lab_sampling self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Temperature / top-k / top-p sampling lab (offline, deterministic).")
    ap.add_argument("--temperature", type=float, default=1.0, help="logits scaling before softmax (0 = greedy)")
    ap.add_argument("--top-k", type=int, default=5, help="keep the k highest-scoring candidates (0 = off)")
    ap.add_argument("--top-p", type=float, default=0.9, help="nucleus cumulative probability threshold (1.0 = off)")
    ap.add_argument("--seed", type=int, default=0, help="sampling seed")
    ap.add_argument("--sweep", action="store_true", help="temperature 0.1..2.0 sweep")
    ap.add_argument("--interactive", action="store_true", help="prompt for the knobs and re-print")
    ap.add_argument("--self-test", action="store_true", help="assert the real sampling properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.top_k, args.top_p)
        return 0
    if args.interactive:
        run_interactive()
        return 0
    print_report(args.temperature, args.top_k, args.top_p, args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
