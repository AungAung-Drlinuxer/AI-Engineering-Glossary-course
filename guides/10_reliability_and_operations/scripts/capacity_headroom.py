#!/usr/bin/env python3
"""Worked example (a): the capacity headroom a stated SLO needs.

ဤ script သည် ယူဆချက် (assumption) အပေါ် အခြေခံသည့် deterministic queue simulation
တစ်ခုဖြင့် utilisation တက်လာသည့်အခါ queue စောင့်ချိန် မည်သို့ ကြီးထွားသည်ကို တွက်သည်။

Assumptions (ဤစာတမ်းတွင် ဖော်ပြထားသည်):
  service time သည် exponential ဖြစ်ပြီး ပျမ်းမျှ 50 ms (mu = 20.0 req/s) ဖြစ်သည်
  arrivals သည် Poisson process ဖြစ်သည် (exponential inter-arrival time)
  worker ၁ ခု၊ FIFO စီစဉ်မှု၊ စောင့်နေသည့် request အတွက် ကန့်သတ်ထားသည့် queue = 200
  စမ်းသပ်သည့် SLO သည် p95 queue wait <= 500 ms ဖြစ်သည်
  simulation သည် deterministic ဖြစ်သည် — seed 20240၊ wall-clock မပါဝင်ပါ

No third-party import, no wall-clock, no temp path.
"""

from __future__ import annotations

import argparse
import collections
import heapq
import random

RULE = "=" * 74
THIN = "-" * 74


def simulate(arrivals_per_s: float, service_s: float, workers: int, sim_seconds: float,
             seed: int, max_queue: int) -> dict:
    """Deterministic discrete-event simulation ဖြင့် queue wait ကိန်းများကို ရှာသည်။"""
    rnd = random.Random(seed)
    arrivals: list[float] = []
    t = 0.0
    while True:
        t += rnd.expovariate(arrivals_per_s)
        if t >= sim_seconds:
            break
        arrivals.append(t)
    svc = random.Random(seed + 1)
    free_times: list[float] = []
    queue: collections.deque[float] = collections.deque()
    waits: list[float] = []
    dropped = 0
    i = 0
    n = len(arrivals)
    while i < n or queue:
        next_arrival = arrivals[i] if i < n else float("inf")
        next_departure = free_times[0] if free_times else float("inf")
        if next_arrival <= next_departure:
            now = next_arrival
            i += 1
            if len(free_times) < workers:
                heap_push(free_times, now + svc.expovariate(1.0 / service_s))
                waits.append(0.0)
            elif len(queue) >= max_queue:
                dropped += 1
            else:
                queue.append(now)
        else:
            now = heapq.heappop(free_times)
            if queue:
                start = queue.popleft()
                waits.append(now - start)
                heap_push(free_times, now + svc.expovariate(1.0 / service_s))
            else:
                pass  # the server becomes idle: free_times stays empty
    waits.sort()
    utilisation = arrivals_per_s * service_s / workers
    return {
        "arrivals": n,
        "utilisation": utilisation,
        "p50_ms": percentile(waits, 0.50) * 1000.0,
        "p95_ms": percentile(waits, 0.95) * 1000.0,
        "dropped": dropped,
    }


def heap_push(heap: list[float], value: float) -> None:
    heapq.heappush(heap, value)


def percentile(sorted_values: list[float], q: float) -> float:
    """Nearest-rank percentile (library မလိုအပ်ပါ)။"""
    if not sorted_values:
        return 0.0
    idx = int(q * (len(sorted_values) - 1) + 0.5)
    return sorted_values[min(idx, len(sorted_values) - 1)]


def main() -> int:
    ap = argparse.ArgumentParser(description="Capacity headroom from a deterministic queue simulation.")
    ap.add_argument("--service-ms", type=float, default=50.0, help="mean service time in ms (assumed)")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--sim-seconds", type=float, default=20000.0)
    ap.add_argument("--seed", type=int, default=20240)
    ap.add_argument("--max-queue", type=int, default=200, help="waiting requests before shedding")
    ap.add_argument("--p95-target-ms", type=float, default=500.0, help="the stated SLO (assumed)")
    ap.add_argument("--demand-rps", type=float, default=12.0, help="the demand to plan for (assumed)")
    args = ap.parse_args()

    service_s = args.service_ms / 1000.0
    grid = [round(0.20 + 0.05 * k, 2) for k in range(16)]

    print(RULE)
    print("capacity_headroom - utilisation နှင့် queue wait (offline, deterministic)")
    print(f"assumptions: service {args.service_ms:.0f} ms (mu = {1.0 / service_s:.1f} req/s), "
          f"workers {args.workers}, sim {args.sim_seconds:.0f} s, queue {args.max_queue}, seed {args.seed}")
    print(f"SLO under test: p95 queue wait <= {args.p95_target_ms:.0f} ms")
    print(THIN)
    print(f"{'rho':>6} {'arrivals/s':>11} {'p50 ms':>9} {'p95 ms':>9} {'dropped':>8} {'verdict':>9}")
    ceiling = 0.0
    ceiling_row = None
    for rho in grid:
        lam = rho * args.workers / service_s
        r = simulate(lam, service_s, args.workers, args.sim_seconds, args.seed, args.max_queue)
        verdict = "meets" if r["p95_ms"] <= args.p95_target_ms else "misses"
        if verdict == "meets":
            ceiling = rho
            ceiling_row = r
        print(f"{rho:>6.2f} {lam:>11.2f} {r['p50_ms']:>9.2f} {r['p95_ms']:>9.2f} "
              f"{r['dropped']:>8} {verdict:>9}")
    print(THIN)
    print("headroom for the stated SLO:")
    if ceiling_row is None:
        print(f"  no grid point meets p95 <= {args.p95_target_ms:.0f} ms")
    else:
        print(f"  highest utilisation that meets the SLO : {ceiling:>6.2f}  "
              f"(arrivals {ceiling * args.workers / service_s:>6.2f}/s, p95 {ceiling_row['p95_ms']:.2f} ms)")
    demand_rho = args.demand_rps * service_s / args.workers
    workers_needed = 1
    while demand_rho > ceiling and workers_needed < 64:
        workers_needed += 1
        demand_rho = args.demand_rps * service_s / workers_needed
    headroom = ceiling - demand_rho
    print(f"  demand {args.demand_rps:.2f} req/s at {args.workers} worker(s): utilisation {demand_rho:>6.2f}")
    print(f"  workers needed to keep that demand under the SLO : {workers_needed}")
    print(f"  utilisation headroom left : {headroom:>6.2f} "
          f"({headroom / ceiling * 100.0:.1f}% of the SLO ceiling)")
    print(THIN)
    print("မှတ်ချက် - utilisation 0.70 တွင် p95 queue wait သည် SLO အဆင့်ကို စတင် ထိသည်၊ 0.90 တွင် "
          "ခန့်မှန်းခြေ 3 s အထိ ခုန်တက်သည်။ ထို့ကြောင့် SLO ကို ကတိပြုရန် utilisation ceiling ကို "
          "queue ကိန်းဖြင့် သတ်မှတ်ရမည်၊ CPU အသုံးပြုမှု ရာခိုင်နှုန်းဖြင့် မသတ်မှတ်ရ။")
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
