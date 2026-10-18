#!/usr/bin/env python3
"""lab_concurrency - parallel agent session များ၏ memory၊ queue နှင့် throughput ကို ပြသည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။
GPU မလိုအပ်ပါ။

Memory model (assumption များ)
    per_session_gib = session overhead 0.25 GiB + turn_tokens * kv_per_token_mb / 1024
    usable_gib      = gpu_memory_gb - reserved 16.0 GiB - weights 14.0 GiB
    session သည် task တစ်ခုလုံး အတွင်း context တစ်ခုလုံးကို ကိုင်ထားသည်၊ ထို့ကြောင့်
    concurrency ကို KV cache က ကန့်သတ်သည်။

Queue model (assumption များ)
    sessions that fit = floor(usable_gib / per_session_gib)
    requested sessions ထက် ဤအရေအတွက် နည်းလျှင် ကျန် session များသည် queue တွင် စောင့်သည်။
    step တစ်ခု = --step-ms ; task တစ်ခု = --task-steps step
    throughput သည် served session အရေအတွက်အပေါ်သာ မှီခိုသည်။
"""

from __future__ import annotations

import argparse
import math

SESSION_OVERHEAD_GIB = 0.25
DEFAULT_WEIGHT_GIB = 14.0
DEFAULT_RESERVED_GIB = 16.0
SWEEP_SESSIONS = (8, 16, 32, 64, 128)
MIB_IN_GIB = 1024.0
RULE = "=" * 74
THIN = "-" * 74


def per_session_gib(turn_tokens: int, kv_mib_per_token: float) -> float:
    return SESSION_OVERHEAD_GIB + turn_tokens * kv_mib_per_token / MIB_IN_GIB


def capacity(gpu_memory_gb: float, reserved_gib: float, weight_gib: float,
             turn_tokens: int, kv_mib_per_token: float) -> dict[str, float]:
    usable = gpu_memory_gb - reserved_gib - weight_gib
    per = per_session_gib(turn_tokens, kv_mib_per_token)
    return {"usable": usable, "per_session": per, "fits": float(int(usable // per))}


def print_report(sessions: int, turn_tokens: int, kv_mib_per_token: float,
                 gpu_memory_gb: float, weight_gib: float, reserved_gib: float,
                 step_ms: float, task_steps: int) -> None:
    cap = capacity(gpu_memory_gb, reserved_gib, weight_gib, turn_tokens, kv_mib_per_token)
    fits = int(cap["fits"])
    served = min(sessions, fits)
    queue = max(0, sessions - fits)
    step_s = step_ms / 1000.0
    steps_per_min = served * 60.0 / step_s
    task_s = step_s * task_steps
    clear_s = math.ceil(queue / served) * task_s if served and queue else 0.0
    print(RULE)
    print("lab_concurrency - sessions, KV memory, queue and throughput (offline, deterministic)")
    print(f"sessions={sessions}  turn-tokens={turn_tokens:,}  kv-per-token={kv_mib_per_token} MiB  "
          f"gpu-memory={gpu_memory_gb:g} GB  step={step_s:g} s")
    print(f"assumption: weights {weight_gib:g} GiB, reserved {reserved_gib:g} GiB, "
          f"per-session overhead {SESSION_OVERHEAD_GIB} GiB, task {task_steps} steps")
    print(THIN)
    print(f"  gpu memory                 : {gpu_memory_gb:>10,.3f} GB")
    print(f"  usable after reserve+weight: {cap['usable']:>10,.3f} GiB")
    print(f"  memory per session         : {cap['per_session']:>10,.3f} GiB  "
          f"({SESSION_OVERHEAD_GIB} overhead + {turn_tokens * kv_mib_per_token / MIB_IN_GIB:.3f} KV)")
    print(f"  memory for all sessions    : {cap['per_session'] * sessions:>10,.3f} GiB")
    print(f"  sessions that fit          : {fits:>10d}")
    print(f"  queue                      : {queue:>10d} session(s) wait "
          f"({served} served in parallel)")
    print(f"  steps per minute           : {steps_per_min:>10,.2f}")
    print(f"  tasks per minute           : {steps_per_min / task_steps:>10,.2f} "
          f"(task = {task_steps} steps = {task_s:g} s)")
    print(f"  queue clears in            : {clear_s:>10,.1f} s")
    print(THIN)
    if queue:
        print("မှတ်ချက် - ဤ session အရေအတွက်ကို one accelerator ပေါ် တွင် မထားနိုင်ပါ၊ "
              "turn တိုင်း context တစ်ခုလုံးကို ပြန်လည် ပေးပို့သောကြောင့် KV cache သည် "
              "concurrency ကို ကန့်သတ်သည်။")
    else:
        print("မှတ်ချက် - session အားလုံး တစ်ပြိုင်နက် နေရာရသည်၊ ကျန် memory ဖြင့် "
              "session ထပ်တိုးနိုင်ဆဲ ဖြစ်သည်။")
    print(RULE)


def print_sweep(turn_tokens: int, kv_mib_per_token: float, gpu_memory_gb: float,
                weight_gib: float, reserved_gib: float, step_ms: float,
                task_steps: int) -> None:
    print(RULE)
    print("lab_concurrency - session sweep (capacity, queue, throughput)")
    print(THIN)
    print(f"{'requested':>9} {'served':>7} {'queue':>6} {'steps/min':>11} {'tasks/min':>10}")
    for sessions in SWEEP_SESSIONS:
        cap = capacity(gpu_memory_gb, reserved_gib, weight_gib, turn_tokens, kv_mib_per_token)
        fits = int(cap["fits"])
        served = min(sessions, fits)
        steps_per_min = served * 60.0 / (step_ms / 1000.0)
        print(f"{sessions:>9} {served:>7} {max(0, sessions - fits):>6} "
              f"{steps_per_min:>11,.2f} {steps_per_min / task_steps:>10,.2f}")
    print(THIN)
    print("မှတ်ချက် - throughput သည် served session အရေအတွက် တွင် ပြည့်သွားသည်၊ "
          "ထို့ကြောင့် session ထပ်တိုးခြင်းသည် queue ကိုသာ ရှည်စေသည်။")
    print(RULE)


def self_test() -> int:
    ok = True

    per = per_session_gib(8192, 0.5)
    per_ok = abs(per - (SESSION_OVERHEAD_GIB + 4.0)) < 1e-9
    print(f"[OK] per-session memory is overhead plus context KV "
          f"({per:.3f} GiB at 8,192 tokens): {per_ok}")
    ok = ok and per_ok

    cap = capacity(80.0, 16.0, 14.0, 8192, 0.5)
    usable_ok = abs(cap["usable"] - 50.0) < 1e-9 and cap["fits"] == 11.0
    print(f"[OK] usable memory is gpu minus reserved and weights "
          f"({cap['usable']:.3f} GiB -> {int(cap['fits'])} sessions): {usable_ok}")
    ok = ok and usable_ok

    served = min(64, int(cap["fits"]))
    queue = max(0, 64 - int(cap["fits"]))
    served_ok = served == 11 and queue == 53
    print(f"[OK] a request for 64 sessions is split into served and queued "
          f"({served} + {queue}): {served_ok}")
    ok = ok and served_ok

    steps_per_min = served * 60.0 / 1.2
    tput_ok = abs(steps_per_min - 550.0) < 1e-9
    print(f"[OK] throughput follows the served sessions and the step time "
          f"({steps_per_min:.2f} steps/min at 1.2 s): {tput_ok}")
    ok = ok and tput_ok

    small = capacity(80.0, 16.0, 14.0, 4096, 0.5)["fits"]
    big = capacity(80.0, 16.0, 14.0, 32768, 0.5)["fits"]
    monotone = small > cap["fits"] > big and big == 3.0
    print(f"[OK] a longer context fits fewer sessions "
          f"(4096 -> {int(small)}, 8192 -> {int(cap['fits'])}, 32768 -> {int(big)}): {monotone}")
    ok = ok and monotone

    again = capacity(80.0, 16.0, 14.0, 8192, 0.5)
    det = again == cap and per_session_gib(8192, 0.5) == per
    print(f"[OK] the capacity model is deterministic for fixed inputs: {det}")
    ok = ok and det

    print("[PASS] lab_concurrency self-test passed." if ok
          else "[FAIL] lab_concurrency self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Concurrent agent sessions: KV memory, queue, throughput (offline).")
    ap.add_argument("--sessions", type=int, default=64, help="parallel agent sessions requested")
    ap.add_argument("--turn-tokens", type=int, default=8192, help="context tokens held per session")
    ap.add_argument("--kv-per-token-mb", type=float, default=0.5,
                    help="KV cache MB per token (assumption)")
    ap.add_argument("--gpu-memory-gb", type=float, default=80.0, help="accelerator memory in GB")
    ap.add_argument("--weight-gb", type=float, default=DEFAULT_WEIGHT_GIB,
                    help="serving weights in GiB (assumption)")
    ap.add_argument("--reserved-gb", type=float, default=DEFAULT_RESERVED_GIB,
                    help="memory reserved for runtime and fragmentation (assumption)")
    ap.add_argument("--step-ms", type=float, default=1200.0, help="wall clock of one agent step")
    ap.add_argument("--task-steps", type=int, default=10, help="steps in one task")
    ap.add_argument("--sweep", action="store_true", help="sweep requested sessions 8..128")
    ap.add_argument("--self-test", action="store_true",
                    help="assert the properties this lab teaches")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.turn_tokens, args.kv_per_token_mb, args.gpu_memory_gb,
                    args.weight_gb, args.reserved_gb, args.step_ms, args.task_steps)
        return 0
    print_report(args.sessions, args.turn_tokens, args.kv_per_token_mb,
                 args.gpu_memory_gb, args.weight_gb, args.reserved_gb,
                 args.step_ms, args.task_steps)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
