#!/usr/bin/env python3
"""lab_schedule - learning rate schedule (constant / step / cosine / warmup) ကို ပြသည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

schedule များ (step index i = 1 .. steps)
    constant : lr = base_lr
    step     : lr = base_lr * 0.5^k, k = ကျော်လွန်ပြီးသော milestone အရေအတွက်
               (milestone များ = steps//3 နှင့် 2*(steps//3))
    cosine   : t = (i-1)/(steps-1), lr = base_lr * 0.5 * (1 + cos(pi * t))
    warmup   : i <= warmup တွင် base_lr မှ peak သို့ linear တိုးသည်၊
               ထို့နောက် peak မှ base_lr သို့ cosine ဖြင့် ပြန်ကျသည်။
"""

from __future__ import annotations

import argparse
import math

SCHEDULES = ("constant", "step", "cosine", "warmup")
RULE = "=" * 92
THIN = "-" * 92


def lr_values(kind: str, steps: int, base_lr: float, warmup: int, peak: float) -> list:
    values = []
    for i in range(1, steps + 1):
        if kind == "constant":
            lr = base_lr
        elif kind == "step":
            k = sum(1 for m in (steps // 3, 2 * (steps // 3)) if i > m)
            lr = base_lr * (0.5 ** k)
        elif kind == "cosine":
            t = (i - 1) / (steps - 1) if steps > 1 else 0.0
            lr = base_lr * 0.5 * (1.0 + math.cos(math.pi * t))
        else:
            if i <= warmup:
                lr = base_lr + (peak - base_lr) * i / warmup
            else:
                t = (i - warmup) / (steps - warmup) if steps > warmup else 1.0
                lr = base_lr + (peak - base_lr) * 0.5 * (1.0 + math.cos(math.pi * t))
        values.append(lr)
    return values


def phase(kind: str, i: int, warmup: int, steps: int) -> str:
    if kind == "warmup":
        return "warmup" if i <= warmup else "decay"
    if kind == "constant":
        return "constant"
    if kind == "step":
        return "milestone" if i in (steps // 3 + 1, 2 * (steps // 3) + 1) else "hold"
    return "decay"


def drops(values: list) -> int:
    return sum(1 for a, b in zip(values, values[1:]) if b < a - 1e-15)


def print_report(kind: str, steps: int, base_lr: float, warmup: int, peak: float) -> None:
    values = lr_values(kind, steps, base_lr, warmup, peak)
    peak_at = values.index(max(values)) + 1
    floor_at = values.index(min(values)) + 1
    print(RULE)
    print("lab_schedule - learning rate schedule table (offline, deterministic)")
    print("schedule=%s  steps=%d  base-lr=%.3e  peak=%.3e  warmup=%d"
          % (kind, steps, base_lr, peak, warmup))
    print(THIN)
    print("%5s %16s %12s %12s" % ("step", "lr", "delta", "phase"))
    previous = None
    for i, lr in enumerate(values, 1):
        delta = 0.0 if previous is None else lr - previous
        print("%5d %16.9f %+12.9f %12s" % (i, lr, delta, phase(kind, i, warmup, steps)))
        previous = lr
    print(THIN)
    print("summary: max lr %.6e at step %d, min lr %.6e at step %d"
          % (max(values), peak_at, min(values), floor_at))
    print("         mean lr %.6e, area under the curve %.6e lr-steps, decreasing steps %d"
          % (sum(values) / len(values), sum(values), drops(values)))
    print("မှတ်ချက် - schedule သည် အစောပိုင်း တည်ငြိမ်မှုနှင့် နောက်ပိုင်း သက်သာမှုကို လဲလှယ်ပါသည်")
    print("         warmup က phase များကို ပြသည်၊ lr budget တူညီမှုကို mean lr ဖြင့် နှိုင်းယှဉ်ပါသည်။")
    print(RULE)


def print_sweep(steps: int, base_lr: float, warmup: int, peak: float) -> None:
    print(RULE)
    print("lab_schedule - schedule comparison (steps=%d, base-lr=%.3e, peak=%.3e, warmup=%d)"
          % (steps, base_lr, peak, warmup))
    print(THIN)
    print("%10s %14s %14s %14s %10s %12s"
          % ("schedule", "first lr", "middle lr", "last lr", "drops", "mean lr"))
    for kind in SCHEDULES:
        values = lr_values(kind, steps, base_lr, warmup, peak)
        print("%10s %14.9f %14.9f %14.9f %10d %12.9f"
              % (kind, values[0], values[len(values) // 2], values[-1], drops(values),
                 sum(values) / len(values)))
    print(THIN)
    print("မှတ်ချက် - constant သည် ပြောင်းလဲမှု မရှိ၊ step သည် milestone နှစ်ကြိမ် ခွဲချလျှော့သည်၊")
    print("         cosine သည် ဖြည်းညှင်းစွာ အဆက်မပြတ် လျော့သည်၊ warmup သည် အရင် တင်ပြီး နောက် လျော့သည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    steps, base, warmup, peak = 12, 1e-3, 4, 3e-3

    values = lr_values("constant", steps, base, warmup, peak)
    flat = all(abs(v - base) < 1e-15 for v in values)
    print("[OK] constant holds one rate for every step (%.3e at all %d steps): %s"
          % (base, steps, flat))
    ok = ok and flat

    values = lr_values("step", steps, base, warmup, peak)
    monotone = all(b <= a + 1e-15 for a, b in zip(values, values[1:]))
    stepped = monotone and drops(values) == 2 and len({round(v, 12) for v in values}) == 3
    print("[OK] step decays monotonically with exactly two halvings (%s): %s"
          % (", ".join("%.3e" % v for v in (values[0], values[4], values[-1])), stepped))
    ok = ok and stepped

    values = lr_values("cosine", steps, base, warmup, peak)
    monotone = all(b <= a + 1e-15 for a, b in zip(values, values[1:]))
    ends = abs(values[0] - base) < 1e-15 and abs(values[-1]) < 1e-15
    cross = next(i for i, v in enumerate(values, 1) if v < base / 2.0)
    middle = cross in ((steps + 1) // 2, (steps + 1) // 2 + 1)
    print("[OK] cosine starts at %.3e, crosses half of it at step %d of %d and reaches 0: %s"
          % (values[0], cross, steps, monotone and ends and middle))
    ok = ok and monotone and ends and middle

    values = lr_values("warmup", steps, base, warmup, peak)
    ramp = all(b > a for a, b in zip(values[:warmup - 1], values[1:warmup]))
    top = abs(values[warmup - 1] - peak) < 1e-12
    tail = all(b <= a + 1e-15 for a, b in zip(values[warmup - 1:], values[warmup:]))
    floor = abs(values[-1] - base) < 1e-12
    print("[OK] warmup ramps %d steps to the peak %.3e then decays back to %.3e: %s"
          % (warmup, peak, base, ramp and top and tail and floor))
    ok = ok and ramp and top and tail and floor

    print("[PASS] lab_schedule self-test passed." if ok else "[FAIL] lab_schedule self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Learning rate schedules: constant, step, cosine, warmup (offline, deterministic).")
    ap.add_argument("--schedule", choices=SCHEDULES, default="warmup", help="schedule family")
    ap.add_argument("--steps", type=int, default=12, help="number of steps in the table")
    ap.add_argument("--base-lr", type=float, default=1e-3, help="base learning rate")
    ap.add_argument("--warmup", type=int, default=4, help="warmup length for the warmup schedule")
    ap.add_argument("--peak", type=float, default=3e-3, help="peak learning rate for the warmup schedule")
    ap.add_argument("--sweep", action="store_true", help="compare all four schedules side by side")
    ap.add_argument("--self-test", action="store_true", help="assert the schedule shapes")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.steps, args.base_lr, args.warmup, args.peak)
        return 0
    print_report(args.schedule, args.steps, args.base_lr, args.warmup, args.peak)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
