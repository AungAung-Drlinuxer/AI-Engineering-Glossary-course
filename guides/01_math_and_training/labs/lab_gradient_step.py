#!/usr/bin/env python3
"""lab_gradient_step - quadratic function ပေါ်ရှိ gradient descent ၏ trajectory နှင့် divergence ကို ပြသည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

လုပ်ဆောင်ချက် (fixed quadratic)
    f(w) = 0.5 * (8.0 * w1^2 + 0.5 * w2^2)
    grad f = (8.0 * w1, 0.5 * w2)
update rule
    momentum = 0   : w <- w - lr * grad
    momentum > 0   : v <- momentum * v - lr * grad ; w <- w + v
divergence ဖြစ်သည့် critical learning rate (အမြင့်ဆုံး curvature lambda_max = 8.0)
    lr* = 2 * (1 + momentum) / lambda_max
lr > lr* ဖြစ်ပါက update သည် ချဲ့ထွင်လာပြီး loss သည် မတည်ငြိမ်တော့ပါ။
"""

from __future__ import annotations

import argparse
import math
import random

LAMBDA = (8.0, 0.5)
RULE = "=" * 92
THIN = "-" * 92


def start_point(seed: int) -> tuple:
    """seed မှ deterministic ဖြစ်သည့် စတင် တန်ဖိုး။"""
    rng = random.Random(seed)
    return (1.0 + 0.1 * (rng.random() - 0.5), 1.0 + 0.1 * (rng.random() - 0.5))


def loss(w) -> float:
    return 0.5 * (LAMBDA[0] * w[0] * w[0] + LAMBDA[1] * w[1] * w[1])


def gradient(w) -> tuple:
    return (LAMBDA[0] * w[0], LAMBDA[1] * w[1])


def grad_norm(w) -> float:
    g = gradient(w)
    return math.hypot(g[0], g[1])


def critical_lr(momentum: float) -> float:
    return 2.0 * (1.0 + momentum) / LAMBDA[0]


def run(lr: float, steps: int, momentum: float, seed: int) -> tuple:
    """trajectory row များ (step 0 အပါ) နှင့် loss အစဉ်ကို ပြန်ပေးသည်။"""
    w = list(start_point(seed))
    v = [0.0, 0.0]
    rows = [(0, w[0], w[1], grad_norm(w), loss(w))]
    for i in range(1, steps + 1):
        g = gradient(w)
        for k in range(2):
            v[k] = momentum * v[k] - lr * g[k]
            w[k] += v[k]
        rows.append((i, w[0], w[1], grad_norm(w), loss(w)))
    return rows, [r[4] for r in rows]


def max_abs_w(rows) -> float:
    return max(max(abs(r[1]), abs(r[2])) for r in rows)


def final_abs_w(rows) -> float:
    return max(abs(rows[-1][1]), abs(rows[-1][2]))


def start_abs_w(rows) -> float:
    return max(abs(rows[0][1]), abs(rows[0][2]))


def status(lr: float, momentum: float) -> str:
    return "STABLE" if lr < critical_lr(momentum) else "DIVERGENT"


def print_report(lr: float, steps: int, momentum: float, seed: int) -> None:
    rows, losses = run(lr, steps, momentum, seed)
    start = rows[0]
    print(RULE)
    print("lab_gradient_step - quadratic trajectory, learning rate and divergence (offline, deterministic)")
    print("f(w) = 0.5 * (%.1f * w1^2 + %.1f * w2^2)   start=(%.6f, %.6f)   seed=%d"
          % (LAMBDA[0], LAMBDA[1], start[1], start[2], seed))
    print("lr=%.4f  momentum=%.2f  steps=%d  critical lr = 2*(1+momentum)/%.1f = %.4f"
          % (lr, momentum, steps, LAMBDA[0], critical_lr(momentum)))
    print(THIN)
    print("%5s %14s %14s %14s %14s" % ("step", "w1", "w2", "|grad|", "loss"))
    for step, w1, w2, gn, ls in rows:
        print("%5d %14.6e %14.6e %14.6e %14.6e" % (step, w1, w2, gn, ls))
    print(THIN)
    print("loss step 0 -> step %d : %.6e -> %.6e    max |w| = %.6e    status %s"
          % (steps, losses[0], losses[-1], max_abs_w(rows), status(lr, momentum)))
    if lr < critical_lr(momentum):
        print("မှတ်ချက် - lr သည် critical တန်ဖိုး %.4f အောက် ရှိသဖြင့် trajectory သည် ကျုံ့ဝင်ပါသည်။"
              % critical_lr(momentum))
    else:
        print("မှတ်ချက် - lr သည် critical တန်ဖိုး %.4f ကို ကျော်လွန်သဖြင့် loss သည် ချဲ့ထွင်လာပါသည်။"
              % critical_lr(momentum))
    print(RULE)


def print_sweep(momentum: float, seed: int, steps: int) -> None:
    print(RULE)
    print("lab_gradient_step - learning rate sweep (momentum=%.2f, %d steps, critical lr=%.4f)"
          % (momentum, steps, critical_lr(momentum)))
    print(THIN)
    print("%10s %14s %14s %14s %12s" % ("lr", "final loss", "max |w|", "loss ratio", "status"))
    for lr in (0.01, 0.05, 0.10, 0.20, 0.24, 0.25, 0.26, 0.30, 0.40):
        rows, losses = run(lr, steps, momentum, seed)
        print("%10.4f %14.6e %14.6e %14.6e %12s"
              % (lr, losses[-1], max_abs_w(rows), losses[-1] / losses[0], status(lr, momentum)))
    print(THIN)
    print("မှတ်ချက် - critical lr အောက်တွင် loss ကျဆင်းသည်၊ အထက်တွင် loss ချဲ့ထွင်လာသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    crit = critical_lr(0.0)

    rows, losses = run(0.10, 100, 0.0, 0)
    stable = math.isfinite(losses[-1]) and losses[-1] < losses[0] and final_abs_w(rows) < start_abs_w(rows)
    print("[OK] lr=0.10 below the critical lr=%.4f converges (loss %.6e -> %.6e): %s"
          % (crit, losses[0], losses[-1], stable))
    ok = ok and stable

    rows, losses = run(0.30, 100, 0.0, 0)
    diverged = final_abs_w(rows) > 1e6
    print("[OK] lr=0.30 above the critical lr=%.4f diverges (final |w| %.3e): %s"
          % (crit, final_abs_w(rows), diverged))
    ok = ok and diverged

    row_below, loss_below = run(0.24, 400, 0.0, 0)
    row_above, loss_above = run(0.26, 400, 0.0, 0)
    boundary = (math.isfinite(loss_below[-1]) and final_abs_w(row_below) < start_abs_w(row_below)
                and final_abs_w(row_above) > 1e6)
    print("[OK] the boundary sits at 2*(1+momentum)/lambda_max = %.4f (0.24 converges to %.3e, 0.26 diverges to %.3e): %s"
          % (crit, final_abs_w(row_below), final_abs_w(row_above), boundary))
    ok = ok and boundary

    row_mom0, _ = run(0.40, 60, 0.0, 0)
    row_mom9, loss_mom9 = run(0.40, 200, 0.9, 0)
    raised = final_abs_w(row_mom9) < 1e-3 and final_abs_w(row_mom0) > 1e6
    print("[OK] momentum raises the critical lr to %.4f, so lr=0.40 diverges at momentum 0.00 (final |w| %.3e) "
          "and converges at 0.90 (final |w| %.3e, loss %.3e): %s"
          % (critical_lr(0.9), final_abs_w(row_mom0), final_abs_w(row_mom9), loss_mom9[-1], raised))
    ok = ok and raised

    det1 = run(0.05, 12, 0.0, 7)[0]
    det2 = run(0.05, 12, 0.0, 7)[0]
    print("[OK] the trajectory is deterministic for a fixed seed (seed=7 reproduced): %s" % (det1 == det2))
    ok = ok and det1 == det2

    print("[PASS] lab_gradient_step self-test passed." if ok else "[FAIL] lab_gradient_step self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Gradient-step trajectory, momentum and divergence (offline, deterministic).")
    ap.add_argument("--lr", type=float, default=0.05, help="learning rate (critical value for momentum 0 is 0.25)")
    ap.add_argument("--steps", type=int, default=12, help="number of optimizer steps")
    ap.add_argument("--momentum", type=float, default=0.0, help="heavy-ball momentum coefficient")
    ap.add_argument("--seed", type=int, default=0, help="seed for the fixed start point")
    ap.add_argument("--sweep", action="store_true", help="sweep the learning rate across the critical value")
    ap.add_argument("--self-test", action="store_true", help="assert the divergence property")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.momentum, args.seed, 40)
        return 0
    print_report(args.lr, args.steps, args.momentum, args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
