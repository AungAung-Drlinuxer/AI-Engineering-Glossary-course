#!/usr/bin/env python3
"""lab_pipeline_budget - data-pipeline throughput against accelerator demand
(offline, deterministic).

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

ယူဆချက် (guide တွင် ဖော်ပြထားသည်):
  - accelerator 8 လုံး၊ တစ်လုံးလျှင် peak 990 TFLOP/s၊ MFU 0.40၊ model parameter 7.0B
    -> accelerator သည် တစ်စက္ကန့်လျှင် `6 * params` FLOPs နှုန်းဖြင့် token စားသည်။
  - `--encode-cost` သည် pipeline ၏ ကုန်ကျစရိတ် — token တစ်လုံးအတွက် မိုက်ခရိုစက္ကန့်
    (encode၊ pack၊ shard ဖတ်ခြင်း စသည့် CPU အလုပ်ပမာဏ၊ stream တစ်ခုတည်း)။
  - storage — token id တစ်လုံးလျှင် uint32 4 byte၊ raw UTF-8 သည် token တစ်လုံးလျှင် 4 byte ခန့်။
  - စျေးနှုန်း — USD 2.50 per accelerator-hour။

step တစ်ခုအတွက် အချိန်သည် accelerator အချိန် နှင့် pipeline အချိန် အနက် ကြီးသည့်
တန်ဖိုး ဖြစ်သည်။ pipeline ပိုနှေးလျှင် accelerator သည် data ကို စောင့်ရသည်။
"""

from __future__ import annotations

import argparse
import math

GIB = 1024 ** 3
ACCELERATORS = 8
PEAK_TFLOPS = 990.0
MFU = 0.40
PARAMS = 7.0e9
PRICE_PER_HOUR = 2.50
BYTES_PER_TOKEN_ID = 4
BYTES_PER_RAW_TOKEN = 4.0
SWEEP_COSTS = (2.0, 5.0, 10.0, 20.0, 50.0, 200.0)
RULE = "=" * 74
THIN = "-" * 74


def budget(corpus_tokens: int, epochs: int, batch: int, seq: int,
           encode_cost: float) -> dict:
    """တန်ဖိုး အားလုံးကို ဖော်မြူလာ အရ တွက်ချက်သည် — wall-clock မပါဝင်ပါ။"""
    tokens_per_step = batch * seq
    total_tokens = corpus_tokens * epochs
    steps_per_epoch = math.ceil(corpus_tokens / tokens_per_step)

    accelerator_tokens_per_second = (
        PEAK_TFLOPS * 1e12 * MFU * ACCELERATORS / (6.0 * PARAMS))
    pipeline_tokens_per_second = 1e6 / encode_cost

    step_time_accelerator = tokens_per_step / accelerator_tokens_per_second
    step_time_pipeline = tokens_per_step * encode_cost / 1e6
    step_time = max(step_time_accelerator, step_time_pipeline)
    utilisation = step_time_accelerator / step_time
    effective_tokens_per_second = tokens_per_step / step_time

    wall_seconds = total_tokens / effective_tokens_per_second
    wall_hours = wall_seconds / 3600.0
    accelerator_hours = wall_hours * ACCELERATORS
    cost_usd = accelerator_hours * PRICE_PER_HOUR

    return {
        "tokens_per_epoch": corpus_tokens,
        "total_tokens": total_tokens,
        "tokens_per_step": tokens_per_step,
        "steps_per_epoch": steps_per_epoch,
        "accelerator_tokens_per_second": accelerator_tokens_per_second,
        "pipeline_tokens_per_second": pipeline_tokens_per_second,
        "examples_per_second_needed": accelerator_tokens_per_second / seq,
        "step_time_accelerator": step_time_accelerator,
        "step_time_pipeline": step_time_pipeline,
        "utilisation": utilisation,
        "effective_tokens_per_second": effective_tokens_per_second,
        "wall_hours": wall_hours,
        "accelerator_hours": accelerator_hours,
        "cost_usd": cost_usd,
        "storage_ids_gib": corpus_tokens * BYTES_PER_TOKEN_ID / GIB,
        "storage_raw_gib": corpus_tokens * BYTES_PER_RAW_TOKEN / GIB,
        "compute_bound": utilisation >= 0.999,
    }


def verdict(result: dict) -> str:
    if result["compute_bound"]:
        return "COMPUTE-BOUND - the pipeline keeps the accelerator fed"
    return "PIPELINE-BOUND - the accelerator waits for data"


def print_report(corpus_tokens: int, epochs: int, batch: int, seq: int,
                 encode_cost: float) -> None:
    result = budget(corpus_tokens, epochs, batch, seq, encode_cost)
    print(RULE)
    print("lab_pipeline_budget - data pipeline vs accelerator demand (offline, deterministic)")
    print("corpus-tokens=%s  epochs=%d  batch=%d  seq=%d  encode-cost=%.1f us/token"
          % ("{:,}".format(corpus_tokens), epochs, batch, seq, encode_cost))
    print("reference: %d accelerators, %.0f TFLOP/s peak, MFU %.2f, %.1fB params, USD %.2f/h"
          % (ACCELERATORS, PEAK_TFLOPS, MFU, PARAMS / 1e9, PRICE_PER_HOUR))
    print(THIN)
    print(" tokens per epoch              : %20s" % "{:,}".format(result["tokens_per_epoch"]))
    print(" total tokens over epochs      : %20s" % "{:,}".format(result["total_tokens"]))
    print(" tokens per step (batch*seq)   : %20s" % "{:,}".format(result["tokens_per_step"]))
    print(" steps per epoch               : %20s" % "{:,}".format(result["steps_per_epoch"]))
    print(" accelerator demand (tok/s)    : %20.1f" % result["accelerator_tokens_per_second"])
    print(" pipeline supply (tok/s)       : %20.1f" % result["pipeline_tokens_per_second"])
    print(" examples per second needed    : %20.2f" % result["examples_per_second_needed"])
    print(" step time accelerator (s)     : %20.3f" % result["step_time_accelerator"])
    print(" step time pipeline (s)        : %20.3f" % result["step_time_pipeline"])
    print(" accelerator utilisation       : %19.2f%%" % (result["utilisation"] * 100.0))
    print(" effective tokens/s            : %20.1f" % result["effective_tokens_per_second"])
    print(THIN)
    print(" storage, uint32 token ids     : %17.2f GiB" % result["storage_ids_gib"])
    print(" storage, raw UTF-8 text       : %17.2f GiB" % result["storage_raw_gib"])
    print(" storage, both copies          : %17.2f GiB"
          % (result["storage_ids_gib"] + result["storage_raw_gib"]))
    print(" wall clock                    : %20.2f h" % result["wall_hours"])
    print(" accelerator-hours             : %20.2f" % result["accelerator_hours"])
    print(" cost at USD %.2f/accel-hour    : %18.2f USD" % (PRICE_PER_HOUR, result["cost_usd"]))
    print(" verdict                       : %s" % verdict(result))
    print(THIN)
    print("မှတ်ချက် - pipeline သည် accelerator လိုအပ်သည့် tokens/s ကို မမီလျှင် "
          "accelerator သည် data ကို စောင့်ရသည်။")
    print(RULE)


def print_sweep(corpus_tokens: int, epochs: int, batch: int, seq: int) -> None:
    print(RULE)
    print("lab_pipeline_budget - encode-cost sweep")
    print(THIN)
    print(" us/token  pipeline tok/s  utilisation  effective tok/s  wall hours  verdict")
    for encode_cost in SWEEP_COSTS:
        result = budget(corpus_tokens, epochs, batch, seq, encode_cost)
        print(" %8.1f %15.1f %11.2f%% %16.1f %11.2f  %s"
              % (encode_cost, result["pipeline_tokens_per_second"],
                 result["utilisation"] * 100.0, result["effective_tokens_per_second"],
                 result["wall_hours"],
                 "compute-bound" if result["compute_bound"] else "pipeline-bound"))
    print(THIN)
    print("မှတ်ချက် - encode-cost ကျဆင်းလျှင် utilisation တက်သည်၊ wall clock ကျဆင်းသည်။")
    print(RULE)


def self_test() -> int:
    ok = True

    result = budget(10000000000, 2, 64, 4096, 20.0)
    supply_ok = abs(result["pipeline_tokens_per_second"] - 1e6 / 20.0) < 1e-9
    print("[OK] pipeline supply is 1e6 / encode-cost: %.1f tok/s" % result["pipeline_tokens_per_second"])
    ok = ok and supply_ok

    capped = result["utilisation"] <= 1.0 and result["utilisation"] > 0.0
    print("[OK] utilisation stays inside (0, 1]: %.4f" % result["utilisation"])
    ok = ok and capped

    fast = budget(10000000000, 2, 64, 4096, 0.5)
    fed_ok = fast["compute_bound"] and abs(fast["utilisation"] - 1.0) < 1e-12
    print("[OK] a cheap pipeline reaches full utilisation on every step: %s" % fed_ok)
    ok = ok and fed_ok

    slow = budget(10000000000, 2, 64, 4096, 200.0)
    starved_ok = (not slow["compute_bound"]
                  and slow["utilisation"] < result["utilisation"] < fast["utilisation"])
    print("[OK] a more expensive pipeline lowers utilisation (%.2f%% < %.2f%% < %.2f%%): %s"
          % (slow["utilisation"] * 100.0, result["utilisation"] * 100.0,
             fast["utilisation"] * 100.0, starved_ok))
    ok = ok and starved_ok

    doubled = budget(20000000000, 2, 64, 4096, 20.0)
    linear_ok = abs(doubled["storage_ids_gib"] - 2 * result["storage_ids_gib"]) < 1e-9
    print("[OK] token-id storage scales linearly with the corpus: %s" % linear_ok)
    ok = ok and linear_ok

    again = budget(10000000000, 2, 64, 4096, 20.0)
    det_ok = again == result
    print("[OK] identical arguments produce identical figures: %s" % det_ok)
    ok = ok and det_ok

    print("[PASS] lab_pipeline_budget self-test passed." if ok
          else "[FAIL] lab_pipeline_budget self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Data-pipeline budget against accelerator demand "
                                             "(offline, deterministic).")
    ap.add_argument("--corpus-tokens", type=int, default=10000000000,
                    help="tokens in the corpus, one pass")
    ap.add_argument("--epochs", type=int, default=2, help="number of passes over the corpus")
    ap.add_argument("--batch", type=int, default=64, help="sequences per step")
    ap.add_argument("--seq", type=int, default=4096, help="tokens per sequence")
    ap.add_argument("--encode-cost", type=float, default=20.0,
                    help="pipeline microseconds per token (encode, pack, shard read)")
    ap.add_argument("--sweep", action="store_true", help="encode-cost 2 .. 200 us/token sweep")
    ap.add_argument("--self-test", action="store_true", help="assert the properties this lab teaches")
    args = ap.parse_args()

    if args.corpus_tokens <= 0 or args.epochs <= 0 or args.batch <= 0 or args.seq <= 0:
        raise SystemExit("--corpus-tokens, --epochs, --batch and --seq must be positive")
    if args.encode_cost <= 0.0:
        raise SystemExit("--encode-cost must be positive")
    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.corpus_tokens, args.epochs, args.batch, args.seq)
        return 0
    print_report(args.corpus_tokens, args.epochs, args.batch, args.seq, args.encode_cost)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
