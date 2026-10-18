#!/usr/bin/env python3
"""Worked example (b): latency and throughput a guardrail adds to the request path.

DERIVATION, not a benchmark. The guardrail runs synchronously in front of the
answer model, so it adds service time to every request and therefore both adds
latency and lowers the request rate the same worker pool can hold.

Queueing model: M/M/c (Erlang C). One worker = one slot that serves both the
guardrail check and the model call for a request.

Assumptions (all labelled, all setup-dependent):
    arrival rate            = 50 requests/s
    answer model service    = 900 ms per request (p50, single request)
    guardrail service       = 120 ms per request (classifier call, same pool)
    workers                 = 32
    worker price            = USD 0.42 per worker-hour  (stated assumption)
    added p95 factor        = 2.0 x guardrail service for the guardrail itself
    queue tail factor       = 3.0 x mean queue wait, used to report p95

Formulas:
    service_ms      = model_ms (+ guardrail_ms when the guardrail is on)
    offered load a  = rps * service_ms / 1000          (erlangs)
    utilisation rho = a / workers
    P(wait)         = Erlang C
    Wq_ms           = P(wait) * service_ms / (workers * (1 - rho))
    added p50 ms    = guardrail_ms + (Wq_on - Wq_off)
    added p95 ms    = p95_factor * guardrail_ms + tail_factor * (Wq_on - Wq_off)
"""

import math

RPS = 50.0
MODEL_MS = 900.0
GUARD_MS = 120.0
WORKERS = 64
WORKER_USD_HOUR = 0.42
P95_FACTOR = 2.0
TAIL_FACTOR = 3.0
DAY_SECONDS = 86400.0

RULE = "=" * 74
THIN = "-" * 74


def erlang_c(workers: int, offered: float):
    """M/M/c probability that an arriving request has to wait. None if saturated."""
    rho = offered / workers
    if rho >= 1.0:
        return None
    term = 1.0
    before = 1.0          # sum of a^k / k! for k = 0 .. workers-1
    for k in range(1, workers + 1):
        term = term * offered / k
        if k < workers:
            before += term
    last = term * workers / (workers - offered)     # a^c/(c! (1-rho))
    return last / (before + last)


def queue(workers: int, service_ms: float, rps: float):
    """Return a dict of queueing quantities for one configuration."""
    offered = rps * service_ms / 1000.0
    rho = offered / workers
    if rho >= 1.0:
        return {"offered": offered, "rho": rho, "p_wait": 1.0, "wq_ms": float("inf"),
                "saturated": True, "capacity_rps": workers * 1000.0 / service_ms}
    p_wait = erlang_c(workers, offered)
    wq_ms = p_wait * service_ms / (workers * (1.0 - rho))
    return {"offered": offered, "rho": rho, "p_wait": p_wait, "wq_ms": wq_ms,
            "saturated": False, "capacity_rps": workers * 1000.0 / service_ms}


def main() -> None:
    off = queue(WORKERS, MODEL_MS, RPS)
    on = queue(WORKERS, MODEL_MS + GUARD_MS, RPS)
    added_p50 = GUARD_MS + (on["wq_ms"] - off["wq_ms"])
    added_p95 = P95_FACTOR * GUARD_MS + TAIL_FACTOR * (on["wq_ms"] - off["wq_ms"])
    workers_needed = math.ceil(WORKERS * (MODEL_MS + GUARD_MS) / MODEL_MS)
    extra_workers = workers_needed - WORKERS
    extra_usd_day = extra_workers * WORKER_USD_HOUR * 24.0
    requests_day = RPS * DAY_SECONDS
    guard_usd = requests_day * (GUARD_MS / 1000.0) / 3600.0 * WORKER_USD_HOUR
    throughput_loss = 1.0 - (on["capacity_rps"] / off["capacity_rps"])

    print(RULE)
    print("ex_b_guardrail_latency - guardrail cost in the request path (offline, deterministic)")
    print("assumptions: rps %.0f, model %.0f ms, guardrail %.0f ms, workers %d, "
          "worker USD %.2f/hour" % (RPS, MODEL_MS, GUARD_MS, WORKERS, WORKER_USD_HOUR))
    print("             queue model M/M/c (Erlang C); one worker serves guardrail plus model")
    print(THIN)
    print("%-26s %14s %14s" % ("quantity", "no guardrail", "with guardrail"))
    print("%-26s %14.3f %14.3f" % ("offered load (erlangs)", off["offered"], on["offered"]))
    print("%-26s %14.4f %14.4f" % ("utilisation rho", off["rho"], on["rho"]))
    print("%-26s %14.4f %14.4f" % ("P(request waits)", off["p_wait"], on["p_wait"]))
    print("%-26s %14.2f %14.2f" % ("mean queue wait Wq (ms)", off["wq_ms"], on["wq_ms"]))
    print("%-26s %14.2f %14.2f" % ("service time (ms)", MODEL_MS, MODEL_MS + GUARD_MS))
    print("%-26s %14.1f %14.1f" % ("sustainable requests/s", off["capacity_rps"], on["capacity_rps"]))
    print(THIN)
    print("added p50 latency : %8.2f ms  (%.0f ms guardrail + %.2f ms extra queue wait)"
          % (added_p50, GUARD_MS, on["wq_ms"] - off["wq_ms"]))
    print("added p95 latency : %8.2f ms  (%.1f x guardrail + %.1f x extra queue wait)"
          % (added_p95, P95_FACTOR, TAIL_FACTOR))
    print("throughput loss   : %8.2f %%  (%.1f -> %.1f requests/s at the same pool)"
          % (100.0 * throughput_loss, off["capacity_rps"], on["capacity_rps"]))
    print("workers to hold the same capacity : %d (extra %d, USD %.2f per day)"
          % (workers_needed, extra_workers, extra_usd_day))
    print("guardrail compute at %.0f rps : %.2f worker-hours/day = USD %.2f/day (%.4f USD per 1e6 requests)"
          % (RPS, requests_day * (GUARD_MS / 1000.0) / 3600.0, guard_usd, guard_usd / (RPS * DAY_SECONDS) * 1e6))
    print(THIN)
    print("မှတ်ချက် - guardrail သည် service time ကို တိုးစေသည့်အတွက် တူညီသည့် worker အရေအတွက်ဖြင့်")
    print("ရရှိနိုင်သည့် request အရေအတွက် ကျဆင်းသည်။ rho သည် ၁ နှင့် နီးလာလျှင် queue wait သည်")
    print("လျင်မြန်စွာ ကြီးထွားသည့်အတွက် guardrail ကို queue ရှေ့တွင် မထည့်ဘဲ အလွှာလိုက် စီစဉ်ရမည်။")
    print("ကိန်းဂဏန်း အားလုံးသည် worker အရေအတွက်နှင့် service time အပေါ် မှီခိုသည့်အတွက်")
    print("'တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်'။")
    print(RULE)


if __name__ == "__main__":
    main()
