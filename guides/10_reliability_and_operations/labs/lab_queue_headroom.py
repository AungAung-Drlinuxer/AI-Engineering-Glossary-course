#!/usr/bin/env python3
"""lab_queue_headroom - utilisation တက်လာသည့်အခါ queue စောင့်ချိန် မည်သို့ ကြီးထွားသည်၊
သတ်မှတ်ထားသည့် SLO အတွက် utilisation headroom မည်မျှ လိုသည်ကို စမ်းသပ်သည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

model —
    arrivals သည် Poisson process ဖြစ်သည် (exponential inter-arrival time)
    service time သည် exponential ဖြစ်သည် (mean = --service-ms)
    worker = --workers၊ FIFO စီစဉ်မှု၊ စောင့်နေသည့် queue ကန့်သတ်ချက် = --max-queue
    utilisation rho = arrivals_per_s * service_s / workers  (offered load)

SLO စမ်းသပ်ချက် — p95 queue wait <= --p95-target-ms ဖြစ်သည့် အမြင့်ဆုံး utilisation ကို ရှာသည်။
"""

from __future__ import annotations

import argparse
import collections
import heapq
import random

RULE = "=" * 74
THIN = "-" * 74
SWEEP_RPS = (10.0, 12.0, 14.0, 15.0, 16.0, 18.0)


def simulate(arrivals_per_s: float, service_s: float, workers: int, sim_seconds: float,
             seed: int, max_queue: int) -> dict:
    """Deterministic discrete-event queue simulation။"""
    rnd = random.Random(seed)
    arrivals: list[float] = []
    t = 0.0
    while True:
        t += rnd.expovariate(arrivals_per_s)
        if t >= sim_seconds:
            break
        arrivals.append(t)
    svc = random.Random(seed + 1)
    free: list[float] = []
    waiting: collections.deque[float] = collections.deque()
    waits: list[float] = []
    dropped = 0
    i = 0
    n = len(arrivals)
    while i < n or waiting:
        next_arrival = arrivals[i] if i < n else float("inf")
        next_departure = free[0] if free else float("inf")
        if next_arrival <= next_departure:
            now = next_arrival
            i += 1
            if len(free) < workers:
                heapq.heappush(free, now + svc.expovariate(1.0 / service_s))
                waits.append(0.0)
            elif len(waiting) >= max_queue:
                dropped += 1
            else:
                waiting.append(now)
        else:
            now = heapq.heappop(free)
            if waiting:
                start = waiting.popleft()
                waits.append(now - start)
                heapq.heappush(free, now + svc.expovariate(1.0 / service_s))
    waits.sort()
    return {
        "admitted": len(waits),
        "dropped": dropped,
        "p50_ms": percentile(waits, 0.50) * 1000.0,
        "p95_ms": percentile(waits, 0.95) * 1000.0,
        "rho": arrivals_per_s * service_s / workers,
    }


def percentile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        return 0.0
    idx = int(q * (len(sorted_values) - 1) + 0.5)
    return sorted_values[min(idx, len(sorted_values) - 1)]


def slo_ceiling(service_s: float, workers: int, sim_seconds: float, seed: int,
                max_queue: int, target_ms: float) -> tuple[float, float, float]:
    """p95 target ကို ဖြည့်ဆည်းသည့် အမြင့်ဆုံး utilisation ကို grid ဖြင့် ရှာသည်။"""
    best_rho, best_rps, best_p95 = 0.0, 0.0, 0.0
    for rho in [round(0.20 + 0.05 * k, 2) for k in range(16)]:
        rps = rho * workers / service_s
        r = simulate(rps, service_s, workers, sim_seconds, seed, max_queue)
        if r["p95_ms"] <= target_ms:
            best_rho, best_rps, best_p95 = rho, rps, r["p95_ms"]
    return best_rho, best_rps, best_p95


def print_report(args: argparse.Namespace) -> None:
    service_s = args.service_ms / 1000.0
    r = simulate(args.arrivals_per_s, service_s, args.workers, args.sim_seconds, args.seed, args.max_queue)
    ceiling, ceiling_rps, ceiling_p95 = slo_ceiling(service_s, args.workers, args.sim_seconds,
                                                    args.seed, args.max_queue, args.p95_target_ms)
    print(RULE)
    print("lab_queue_headroom - utilisation, queue wait နှင့် SLO headroom (offline, deterministic)")
    print(f"arrivals={args.arrivals_per_s:.2f}/s  service={args.service_ms:.1f} ms  workers={args.workers}  "
          f"sim={args.sim_seconds:.0f} s  seed={args.seed}  queue={args.max_queue}")
    print(f"utilisation (offered) = {r['rho']:.4f}   SLO target: p95 queue wait <= {args.p95_target_ms:.0f} ms")
    print(THIN)
    print(f"  admitted requests          : {r['admitted']:>10,}")
    print(f"  dropped (queue full)       : {r['dropped']:>10,}")
    p50, p95 = r['p50_ms'], r['p95_ms']
    ratio = f"{p95 / p50:.2f}x" if p50 > 0 else "n/a (p50 is 0)"
    print(f"  p50 queue wait             : {p50:>10.2f} ms")
    print(f"  p95 queue wait             : {p95:>10.2f} ms")
    print(f"  p95 / p50 ratio            : {ratio:>10}")
    print(THIN)
    print("headroom search (arrivals sweep, same seed):")
    print(f"{'arrivals/s':>11} {'rho':>6} {'p95 ms':>10} {'verdict':>9}")
    for rps in SWEEP_RPS:
        s = simulate(rps, service_s, args.workers, args.sim_seconds, args.seed, args.max_queue)
        verdict = "meets" if s["p95_ms"] <= args.p95_target_ms else "misses"
        print(f"{rps:>11.2f} {s['rho']:>6.2f} {s['p95_ms']:>10.2f} {verdict:>9}")
    print(THIN)
    print(f"SLO ceiling: rho {ceiling:.2f} (arrivals {ceiling_rps:.2f}/s, p95 {ceiling_p95:.2f} ms)")
    headroom = ceiling - r["rho"]
    print(f"headroom at {args.arrivals_per_s:.2f} req/s: rho {headroom:.2f} "
          f"({headroom / ceiling * 100.0:.1f}% of the ceiling)")
    workers_needed = args.workers
    while args.arrivals_per_s * service_s / workers_needed > ceiling and workers_needed < 64:
        workers_needed += 1
    print(f"workers needed for this demand: {workers_needed}")
    print(THIN)
    print("မှတ်ချက် - queue စောင့်ချိန်၏ p95 သည် utilisation တိုးလာသည့်အခါ အစပိုင်းတွင် နှေးစွာ တိုးပြီး "
          "saturation နီးလျှင် ခုန်တက်သည်။ SLO အဆင့်ကို utilisation မဟုတ်ဘဲ queue ကိန်းဖြင့် သတ်မှတ်ရမည်။")
    print(RULE)


def print_sweep(args: argparse.Namespace) -> None:
    service_s = args.service_ms / 1000.0
    print(RULE)
    print("lab_queue_headroom - arrivals sweep 2.00 .. 19.00/s (workers %d)" % args.workers)
    print(f"{'arrivals/s':>11} {'rho':>6} {'p50 ms':>9} {'p95 ms':>10} {'dropped':>8} {'verdict':>9}")
    rps = 2.0
    while rps <= 19.0:
        s = simulate(rps, service_s, args.workers, args.sim_seconds, args.seed, args.max_queue)
        verdict = "meets" if s["p95_ms"] <= args.p95_target_ms else "misses"
        print(f"{rps:>11.2f} {s['rho']:>6.2f} {s['p50_ms']:>9.2f} {s['p95_ms']:>10.2f} "
              f"{s['dropped']:>8} {verdict:>9}")
        rps = round(rps + 1.0, 2)
    print(THIN)
    print("မှတ်ချက် - utilisation 1.0 အနီးတွင် queue သည် မတည်ငြိမ်စွာ ကြီးထွားပြီး queue ကန့်သတ်ချက် "
          "ပြည့်လျှင် request များ ကျဆင်းသည် (load shedding)။")
    print(RULE)


def self_test() -> int:
    ok = True
    service_s = 0.050
    base = dict(service_s=service_s, workers=1, sim_seconds=6000.0, seed=20240, max_queue=1000)

    lo = simulate(10.0, **base)
    hi = simulate(18.0, **base)
    grows = hi["p95_ms"] > lo["p95_ms"]
    print(f"[OK] higher utilisation lengthens the p95 queue wait "
          f"({lo['p95_ms']:.2f} ms at rho {lo['rho']:.2f} -> {hi['p95_ms']:.2f} ms at rho {hi['rho']:.2f}): {grows}")
    ok = ok and grows

    one = simulate(18.0, service_s=service_s, workers=1, sim_seconds=6000.0, seed=20240, max_queue=1000)
    four = simulate(18.0, service_s=service_s, workers=4, sim_seconds=6000.0, seed=20240, max_queue=1000)
    helps = four["p95_ms"] < one["p95_ms"]
    print(f"[OK] adding workers removes queueing at the same demand "
          f"({one['p95_ms']:.2f} ms -> {four['p95_ms']:.2f} ms, p95): {helps}")
    ok = ok and helps

    ordered = hi["p95_ms"] >= hi["p50_ms"] >= 0.0
    print(f"[OK] p95 is never below p50 (p50 {hi['p50_ms']:.2f} ms <= p95 {hi['p95_ms']:.2f} ms): {ordered}")
    ok = ok and ordered

    half = simulate(10.0, **base)
    nine = simulate(18.0, **base)
    superlinear = nine["p95_ms"] > 2.0 * half["p95_ms"]
    print(f"[OK] near saturation the p95 queue wait grows faster than linearly "
          f"({half['p95_ms']:.2f} -> {nine['p95_ms']:.2f} ms, ratio {nine['p95_ms'] / half['p95_ms']:.2f}x): {superlinear}")
    ok = ok and superlinear

    repeat = simulate(10.0, **base)
    deterministic = abs(repeat["p95_ms"] - lo["p95_ms"]) < 1e-12
    print(f"[OK] the same seed reproduces the same p95 queue wait ({lo['p95_ms']:.2f} ms twice): {deterministic}")
    ok = ok and deterministic

    shedding = simulate(19.0, service_s=service_s, workers=1, sim_seconds=6000.0, seed=20240, max_queue=5)
    sheds = shedding["dropped"] > 0
    print(f"[OK] a small queue at rho 0.95 sheds work instead of queueing forever "
          f"(dropped {shedding['dropped']:,} of {shedding['admitted'] + shedding['dropped']:,}): {sheds}")
    ok = ok and sheds

    ceiling, rps, p95 = slo_ceiling(service_s, 1, 6000.0, 20240, 1000, 500.0)
    ceiling_ok = 0.0 < ceiling < 1.0 and p95 <= 500.0
    print(f"[OK] the SLO ceiling is a utilisation below 1.0 that still meets the p95 target "
          f"(rho {ceiling:.2f}, arrivals {rps:.2f}/s, p95 {p95:.2f} ms): {ceiling_ok}")
    ok = ok and ceiling_ok

    print("[PASS] lab_queue_headroom self-test passed." if ok else "[FAIL] lab_queue_headroom self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Queueing headroom lab (offline, deterministic).")
    ap.add_argument("--arrivals-per-s", type=float, default=12.0)
    ap.add_argument("--service-ms", type=float, default=50.0)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--sim-seconds", type=float, default=20000.0)
    ap.add_argument("--seed", type=int, default=20240)
    ap.add_argument("--max-queue", type=int, default=200, help="waiting requests before shedding")
    ap.add_argument("--p95-target-ms", type=float, default=500.0)
    ap.add_argument("--sweep", action="store_true", help="arrivals 2.00 .. 19.00/s sweep")
    ap.add_argument("--self-test", action="store_true", help="assert the real queueing properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args)
        return 0
    print_report(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
