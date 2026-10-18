#!/usr/bin/env python3
"""lab_guardrail_cost - what a synchronous guardrail costs in the request path.

Offline and deterministic: the queue is modelled analytically (M/M/c, Erlang C),
so nothing here depends on the wall clock or on random draws.

Model
    service_ms     = model_ms (+ latency_ms when the guardrail is on)
    offered (a)    = rps * service_ms / 1000          erlangs
    utilisation    = a / workers                      (>= 1 means saturated)
    P(wait)        = Erlang C
    Wq_ms          = P(wait) * service_ms / (workers * (1 - utilisation))
    added p50 ms   = latency_ms + (Wq_on - Wq_off)
    added p95 ms   = p95_factor * latency_ms + tail_factor * (Wq_on - Wq_off)
    throughput     = workers * 1000 / service_ms      requests/s

Flags
    --rps FLOAT        arrival rate (default 50)
    --latency-ms FLOAT guardrail service time per request (default 120)
    --model-ms FLOAT   answer model service time per request (default 900)
    --workers INT      worker slots shared by guardrail and model (default 64)
    --price FLOAT      USD per worker-hour (default 0.42)
    --sweep            rps from 10 to 100
    --self-test        assert the properties this lab teaches
"""

from __future__ import annotations

import argparse
import math

RULE = "=" * 74
THIN = "-" * 74
SWEEP_RPS = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
P95_FACTOR = 2.0
TAIL_FACTOR = 3.0
DAY_SECONDS = 86400.0


def erlang_c(workers: int, offered: float):
    """P(an arriving request waits) for M/M/c; None when the system is saturated."""
    if offered / workers >= 1.0:
        return None
    term = 1.0
    before = 1.0          # sum of a^k / k! for k = 0 .. workers-1
    for k in range(1, workers + 1):
        term = term * offered / k
        if k < workers:
            before += term
    last = term * workers / (workers - offered)     # a^c/(c! (1-rho))
    return last / (before + last)


def queue(workers: int, service_ms: float, rps: float) -> dict:
    """Queueing quantities for one (workers, service_ms, rps) configuration."""
    offered = rps * service_ms / 1000.0
    saturation = workers * 1000.0 / service_ms
    rho = offered / workers
    if rho >= 1.0:
        return {"offered": offered, "rho": rho, "p_wait": 1.0,
                "wq_ms": float("inf"), "throughput": saturation, "ok": False}
    p_wait = erlang_c(workers, offered)
    wq = p_wait * service_ms / (workers * (1.0 - rho))
    return {"offered": offered, "rho": rho, "p_wait": p_wait,
            "wq_ms": wq, "throughput": saturation, "ok": True}


def report(rps: float, guard_ms: float, model_ms: float, workers: int, price: float) -> None:
    off = queue(workers, model_ms, rps)
    on = queue(workers, model_ms + guard_ms, rps)
    both_ok = off["ok"] and on["ok"]
    extra_wait = (on["wq_ms"] - off["wq_ms"]) if both_ok else float("nan")
    added_p50 = guard_ms + extra_wait
    added_p95 = P95_FACTOR * guard_ms + TAIL_FACTOR * extra_wait
    needed = math.ceil(workers * (model_ms + guard_ms) / model_ms)
    extra_workers = needed - workers
    guard_hours = rps * DAY_SECONDS * (guard_ms / 1000.0) / 3600.0
    guard_usd_day = guard_hours * price
    guard_usd_per_million = guard_usd_day / (rps * DAY_SECONDS) * 1e6

    print(RULE)
    print("lab_guardrail_cost - the price of a synchronous guardrail (offline, deterministic)")
    print("queue model M/M/c (Erlang C); rps=%.0f  model-ms=%.0f  guardrail-ms=%.0f  workers=%d"
          % (rps, model_ms, guard_ms, workers))
    print("assumption: worker price USD %.2f per hour; added p95 = %.1f x guardrail + %.1f x extra queue wait"
          % (price, P95_FACTOR, TAIL_FACTOR))
    print(THIN)
    print("%-28s %16s %16s" % ("quantity", "no guardrail", "with guardrail"))
    print("%-28s %16.3f %16.3f" % ("offered load (erlangs)", off["offered"], on["offered"]))
    print("%-28s %16.4f %16.4f" % ("utilisation rho", off["rho"], on["rho"]))
    print("%-28s %16.4f %16.4f" % ("P(request waits)", off["p_wait"], on["p_wait"]))
    wq_off = "%16.2f" % off["wq_ms"] if off["ok"] else "%16s" % "saturated"
    wq_on = "%16.2f" % on["wq_ms"] if on["ok"] else "%16s" % "saturated"
    print("%-28s %s %s" % ("mean queue wait Wq (ms)", wq_off, wq_on))
    print("%-28s %16.1f %16.1f" % ("sustainable requests/s", off["throughput"], on["throughput"]))
    print(THIN)
    if both_ok:
        print("added p50 latency (ms)    : %10.2f" % added_p50)
        print("added p95 latency (ms)    : %10.2f" % added_p95)
    else:
        print("added p50 latency (ms)    : %10s" % "saturated")
        print("added p95 latency (ms)    : %10s" % "saturated")
    print("throughput loss           : %10.2f %%  (%.1f -> %.1f requests/s)"
          % (100.0 * (1.0 - on["throughput"] / off["throughput"]), off["throughput"], on["throughput"]))
    print("workers for same capacity : %10d  (extra %d, USD %.2f per day)"
          % (needed, extra_workers, extra_workers * price * 24.0))
    print("guardrail cpu cost        : USD %8.4f per 1e6 requests  (%.2f USD/day at %.0f rps)"
          % (guard_usd_per_million, guard_usd_day, rps))
    print(THIN)
    print("မှတ်ချက် - guardrail သည် service time ကို တိုးစေသည့်အတွက် တူညီသည့် worker အရေအတွက်ဖြင့်")
    print("ရရှိနိုင်သည့် request အရေအတွက် ကျဆင်းပြီး queue wait တိုးသည်။ utilisation သည် ၁ နှင့်")
    print("နီးလာလျှင် queue wait သည် လျင်မြန်စွာ ကြီးထွားသည့်အတွက် guardrail ကို request လမ်းကြောင်း")
    print("အတွင်း မထည့်ဘဲ အလွှာလိုက် စီစဉ်ခြင်းသည် ကုန်ကျစရိတ် သက်သာစေသည်။")
    print(RULE)


def sweep(guard_ms: float, model_ms: float, workers: int, price: float) -> None:
    print(RULE)
    print("lab_guardrail_cost - rps sweep 10..100 (offline, deterministic)")
    print("model-ms=%.0f  guardrail-ms=%.0f  workers=%d  worker price USD %.2f/hour"
          % (model_ms, guard_ms, workers, price))
    print(THIN)
    print("%6s %9s %9s %12s %12s %10s %10s"
          % ("rps", "rho_off", "rho_on", "added p50", "added p95", "thr_off", "thr_on"))
    for rps in SWEEP_RPS:
        off = queue(workers, model_ms, rps)
        on = queue(workers, model_ms + guard_ms, rps)
        if off["ok"] and on["ok"]:
            extra = on["wq_ms"] - off["wq_ms"]
            p50 = guard_ms + extra
            p95 = P95_FACTOR * guard_ms + TAIL_FACTOR * extra
            print("%6d %9.3f %9.3f %12.2f %12.2f %10.1f %10.1f"
                  % (rps, off["rho"], on["rho"], p50, p95, off["throughput"], on["throughput"]))
        else:
            print("%6d %9.3f %9.3f %12s %12s %10.1f %10.1f"
                  % (rps, off["rho"], on["rho"], "saturated", "saturated", off["throughput"], on["throughput"]))
    print(THIN)
    print("မှတ်ချက် - rps တိုးလျှင် utilisation တိုးပြီး queue wait သည် nonlinear ဖြစ်သည်။ guardrail")
    print("ထည့်လျှင် တူညီသည့် capacity အတွက် saturated အမှတ်သို့ စောစွာ ရောက်သည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    workers, model_ms, guard_ms, rps, price = 64, 900.0, 120.0, 50.0, 0.42

    off = queue(workers, model_ms, rps)
    on = queue(workers, model_ms + guard_ms, rps)
    adds = (on["wq_ms"] + guard_ms) > off["wq_ms"]
    print("[OK] the guardrail adds latency (%.2f ms -> %.2f ms of service+wait): %s"
          % (off["wq_ms"], on["wq_ms"] + guard_ms, adds))
    ok = ok and adds

    costly = on["throughput"] < off["throughput"]
    print("[OK] the guardrail costs throughput (%.1f -> %.1f requests/s): %s"
          % (off["throughput"], on["throughput"], costly))
    ok = ok and costly

    loss = 1.0 - on["throughput"] / off["throughput"]
    expected = guard_ms / (model_ms + guard_ms)
    matches = abs(loss - expected) < 1e-12
    print("[OK] the throughput loss equals guardrail/(model+guardrail) (%.6f vs %.6f): %s"
          % (loss, expected, matches))
    ok = ok and matches

    wait_grows = queue(workers, model_ms, 10.0)["wq_ms"] < queue(workers, model_ms, 60.0)["wq_ms"]
    print("[OK] queue wait grows with the arrival rate (rps 10 -> 60): %s" % wait_grows)
    ok = ok and wait_grows

    saturated = queue(workers, model_ms, 90.0)["ok"] is False
    print("[OK] the pool saturates above its capacity at rps=90: %s" % saturated)
    ok = ok and saturated

    extra_workers = math.ceil(workers * (model_ms + guard_ms) / model_ms) - workers
    print("[OK] holding the same capacity takes more workers (%d extra): %s" % (extra_workers, extra_workers > 0))
    ok = ok and extra_workers > 0

    print("[PASS] lab_guardrail_cost self-test passed." if ok else "[FAIL] lab_guardrail_cost self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Guardrail latency / throughput / cost lab (offline, deterministic).")
    ap.add_argument("--rps", type=float, default=50.0)
    ap.add_argument("--latency-ms", type=float, default=120.0)
    ap.add_argument("--model-ms", type=float, default=900.0)
    ap.add_argument("--workers", type=int, default=64)
    ap.add_argument("--price", type=float, default=0.42, help="USD per worker-hour (stated assumption)")
    ap.add_argument("--sweep", action="store_true", help="rps sweep 10..100")
    ap.add_argument("--self-test", action="store_true", help="assert the properties this lab teaches")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        sweep(args.latency_ms, args.model_ms, args.workers, args.price)
        return 0
    report(args.rps, args.latency_ms, args.model_ms, args.workers, args.price)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
