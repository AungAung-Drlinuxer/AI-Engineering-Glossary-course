#!/usr/bin/env python3
"""lab_batching - Static batching နှင့် Continuous batching ကို နှိုင်းယှဉ်သည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

Request အရေအတွက်နှင့် output အရှည်များကို ပုံသေ seed (REQUEST_SEED) မှ ဆွဲထုတ်သည်၊ ထို့ကြောင့်
run တိုင်း ရလဒ် တူညီသည်။

Cost model (assumption များ)
    decode step တစ်ခု၏ ကြာချိန် = DECODE_BASE_MS + DECODE_PER_ACTIVE_MS * active_decode
                                 + PREFILL_MS_PER_TOKEN * prefill_tokens_in_this_step
    prefill ကို PREFILL_TOKENS_PER_STEP token အလိုက် chunk လုပ်သည်။

Static batching  - slot တစ်ခုသည် batch ထဲရှိ အရှည်ဆုံး request ပြီးဆုံးသည်အထိ ချုပ်ထားသည်။
Continuous batching - request တစ်ခု ပြီးဆုံးသည်နှင့် လွတ်လာသည့် slot သည် စောင့်နေသည့်
                      request နောက်တစ်ခုကို ချက်ချင်း လက်ခံသည်။
"""

from __future__ import annotations

import argparse
import random

REQUEST_SEED = 20240
DECODE_BASE_MS = 4.0
DECODE_PER_ACTIVE_MS = 3.0
PREFILL_MS_PER_TOKEN = 0.03
PREFILL_TOKENS_PER_STEP = 256
SWEEP_SLOTS = [1, 2, 4, 8, 16, 32]
RULE = "=" * 74
THIN = "-" * 74


def output_lengths(requests: int, output_tokens: int) -> list[int]:
    """seed မှ deterministic output အရှည်များ (mean ~= output_tokens၊ [0.2, 1.8] အချိုး ပြန့်သည်)။"""
    rng = random.Random(REQUEST_SEED)
    return [max(1, int(round(output_tokens * (0.2 + 1.6 * rng.random())))) for _ in range(requests)]


def simulate(lengths: list[int], slots: int, prompt_tokens: int, continuous: bool,
             itl_budget_ms: float, gpu_hour_cost: float) -> dict[str, float]:
    n = len(lengths)
    if n == 0 or slots < 1:
        return {"tokens": 0.0, "steps": 0.0, "wall_ms": 0.0, "ttft_first": 0.0, "ttft_last": 0.0,
                "mean_itl": 0.0, "tps": 0.0, "goodput": 0.0, "gpu_seconds": 0.0,
                "cost_per_million": 0.0}
    next_id = 0
    active: list[dict] = []
    t = 0.0
    steps = 0
    tokens = 0
    good_tokens = 0
    ttft: dict[int, float] = {}
    itl_sum = 0.0
    itl_count = 0

    def admit() -> None:
        nonlocal next_id
        active.append({"id": next_id, "prefill_left": prompt_tokens,
                       "out_left": lengths[next_id], "last": t})
        next_id += 1

    while next_id < n or active:
        if continuous:
            while next_id < n and len(active) < slots:
                admit()
        else:
            if not active:  # new batch
                for _ in range(min(slots, n - next_id)):
                    admit()
        if not active:
            break

        prefill_tokens = sum(min(r["prefill_left"], PREFILL_TOKENS_PER_STEP)
                             for r in active if r["prefill_left"] > 0)
        decode_active = sum(1 for r in active if r["prefill_left"] == 0 and r["out_left"] > 0)
        duration = (DECODE_BASE_MS + DECODE_PER_ACTIVE_MS * decode_active
                    + PREFILL_MS_PER_TOKEN * prefill_tokens)

        for r in active:
            if r["prefill_left"] > 0:
                r["prefill_left"] -= min(r["prefill_left"], PREFILL_TOKENS_PER_STEP)
                if r["prefill_left"] == 0:
                    if r["out_left"] > 0:
                        r["out_left"] -= 1
                        tokens += 1
                        ttft[r["id"]] = t + duration
                        r["last"] = t + duration
                        if duration <= itl_budget_ms:
                            good_tokens += 1
            elif r["out_left"] > 0:
                r["out_left"] -= 1
                tokens += 1
                itl_sum += (t + duration) - r["last"]
                itl_count += 1
                r["last"] = t + duration
                if duration <= itl_budget_ms:
                    good_tokens += 1

        t += duration
        steps += 1

        if continuous:
            active = [r for r in active if r["out_left"] > 0]
        else:
            if all(r["out_left"] <= 0 for r in active):
                active = []

    wall_s = t / 1000.0
    gpu_hours = t / 3600.0 / 1000.0
    return {
        "tokens": float(tokens),
        "steps": float(steps),
        "wall_ms": t,
        "ttft_first": ttft.get(0, 0.0),
        "ttft_last": ttft.get(n - 1, 0.0),
        "mean_itl": (itl_sum / itl_count) if itl_count else 0.0,
        "tps": tokens / wall_s if wall_s > 0 else 0.0,
        "goodput": good_tokens / wall_s if wall_s > 0 else 0.0,
        "gpu_seconds": wall_s,
        "cost_per_million": gpu_hours * gpu_hour_cost / (tokens / 1e6) if tokens else 0.0,
    }


def print_strategy(name: str, m: dict[str, float], itl_budget_ms: float) -> None:
    def line(label: str, value: str) -> None:
        print(f"  {label:<30}: {value:>14}")

    print(f"{name}")
    line("total tokens generated", f"{m['tokens']:,.0f}")
    line("wall-clock steps", f"{m['steps']:,.0f}")
    line("TTFT first/last request (ms)", f"{m['ttft_first']:,.2f} / {m['ttft_last']:,.2f}")
    line(f"mean ITL (ms, budget {itl_budget_ms:g})", f"{m['mean_itl']:,.2f}")
    line("tokens/second", f"{m['tps']:,.2f}")
    line("goodput in ITL budget (tok/s)", f"{m['goodput']:,.2f}")
    line("GPU-seconds", f"{m['gpu_seconds']:,.3f}")
    line("cost per million tokens (USD)", f"{m['cost_per_million']:,.4f}")


def run_both(requests: int, slots: int, prompt_tokens: int, output_tokens: int,
             gpu_hour_cost: float, itl_budget_ms: float) -> tuple[dict, dict, list[int]]:
    lengths = output_lengths(requests, output_tokens)
    static = simulate(lengths, slots, prompt_tokens, False, itl_budget_ms, gpu_hour_cost)
    cont = simulate(lengths, slots, prompt_tokens, True, itl_budget_ms, gpu_hour_cost)
    return static, cont, lengths


def print_report(requests: int, slots: int, prompt_tokens: int, output_tokens: int,
                 gpu_hour_cost: float, itl_budget_ms: float) -> None:
    static, cont, lengths = run_both(requests, slots, prompt_tokens, output_tokens,
                                     gpu_hour_cost, itl_budget_ms)
    print(RULE)
    print("lab_batching - static batching vs continuous batching")
    print(f"requests={requests}  slots={slots}  prompt-tokens={prompt_tokens}  "
          f"output-tokens~{output_tokens}  gpu-hour={gpu_hour_cost} USD")
    print(f"output lengths: min={min(lengths)}  max={max(lengths)}  "
          f"mean={sum(lengths) / len(lengths):.1f}  (seed {REQUEST_SEED})")
    print(THIN)
    print_strategy("Static batching", static, itl_budget_ms)
    print(THIN)
    print_strategy("Continuous batching", cont, itl_budget_ms)
    print(THIN)
    print(f"Continuous / static throughput ratio: {cont['tps'] / static['tps']:.4f}x  |  "
          f"goodput ratio: {cont['goodput'] / static['goodput']:.4f}x")
    print("မှတ်ချက် - request အားလုံးကို t=0 တွင် တင်သွင်းသည်၊ ထို့ကြောင့် TTFT တွင် queueing အချိန် "
          "ပါဝင်သည်။ Static batching တွင် slot သည် batch အရှည်ဆုံး request ပြီးသည်အထိ ချုပ်ထားသည်။")
    print(RULE)


def print_sweep(requests: int, prompt_tokens: int, output_tokens: int,
                gpu_hour_cost: float, itl_budget_ms: float) -> None:
    print(RULE)
    print("lab_batching - slot sweep (static vs continuous)")
    print(THIN)
    print("  slots   static tok/s   cont tok/s   ratio   static USD/M   cont USD/M")
    for slots in SWEEP_SLOTS:
        static, cont, _ = run_both(requests, slots, prompt_tokens, output_tokens,
                                   gpu_hour_cost, itl_budget_ms)
        print(f" {slots:>6}   {static['tps']:>12.2f}   {cont['tps']:>11.2f}   "
              f"{cont['tps'] / static['tps']:>5.2f}x   {static['cost_per_million']:>11.4f}   "
              f"{cont['cost_per_million']:>10.4f}")
    print(THIN)
    print("မှတ်ချက် - slot အရေအတွက် တိုးလာသည်နှင့်အမျှ two strategy ကွာခြားမှု ကျဆင်းသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    static, cont, lengths = run_both(64, 8, 512, 128, 2.49, 50.0)

    same = static["tokens"] == cont["tokens"] == float(sum(lengths))
    print(f"[OK] both strategies generate the same total tokens ({static['tokens']:,.0f}): {same}")
    ok = ok and same

    thr = cont["tps"] > static["tps"]
    print(f"[OK] continuous batching beats static on throughput ({cont['tps']:.2f} > "
          f"{static['tps']:.2f} tok/s): {thr}")
    ok = ok and thr

    gp = cont["goodput"] > static["goodput"]
    print(f"[OK] continuous batching beats static on goodput inside the ITL budget "
          f"({cont['goodput']:.2f} > {static['goodput']:.2f} tok/s): {gp}")
    ok = ok and gp

    wall = cont["wall_ms"] < static["wall_ms"]
    print(f"[OK] continuous batching finishes sooner ({cont['wall_ms']:.0f} < "
          f"{static['wall_ms']:.0f} ms): {wall}")
    ok = ok and wall

    cheaper = cont["cost_per_million"] < static["cost_per_million"]
    print(f"[OK] cost per million output tokens is lower ({cont['cost_per_million']:.4f} < "
          f"{static['cost_per_million']:.4f} USD): {cheaper}")
    ok = ok and cheaper

    again = simulate(output_lengths(64, 128), 8, 512, True, 50.0, 2.49)
    det = again == cont
    print(f"[OK] the simulation is deterministic for fixed inputs: {det}")
    ok = ok and det

    print("[PASS] lab_batching self-test passed." if ok else "[FAIL] lab_batching self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Static vs continuous batching simulation (offline, deterministic).")
    ap.add_argument("--requests", type=int, default=64)
    ap.add_argument("--slots", type=int, default=8)
    ap.add_argument("--prompt-tokens", type=int, default=512)
    ap.add_argument("--output-tokens", type=int, default=128)
    ap.add_argument("--gpu-hour-cost", type=float, default=2.49, help="USD per GPU-hour")
    ap.add_argument("--itl-budget-ms", type=float, default=50.0)
    ap.add_argument("--sweep", action="store_true", help="slot sweep 1..32")
    ap.add_argument("--self-test", action="store_true", help="assert the real batching properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.requests, args.prompt_tokens, args.output_tokens,
                    args.gpu_hour_cost, args.itl_budget_ms)
        return 0
    print_report(args.requests, args.slots, args.prompt_tokens, args.output_tokens,
                 args.gpu_hour_cost, args.itl_budget_ms)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
