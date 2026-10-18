#!/usr/bin/env python3
"""Worked example (c): replicas held for failover vs the expected cost of an outage.

ဤ script သည် failover အတွက် ထားရှိသည့် replica များ၏ ကုန်ကျစရိတ်နှင့်
ချို့ယွင်းမှုကြောင့် ရရှိမည့် ဆုံးရှုံးမှု၏ မျှော်မှန်း တန်ဖိုးကို နှိုင်းယှဉ်သည်။

Assumptions (ဤစာတမ်းတွင် ဖော်ပြထားသည်):
  replica တစ်ခုလျှင် USD 800 / လ (ထိန်းသိမ်းမှုနှင့် အခြေခံအဆောက်အအုံ အပါအဝင်)
  outage တစ်နာရီလျှင် ဆုံးရှုံးမှု USD 5000 (revenue နှင့် လုပ်ငန်း သက်ရောက်မှု)
  outage သည် တစ်နှစ်လျှင် 4 ကြိမ် ဖြစ်ပေါ်သည် (အစီအစဉ် မပါသည့် ကြိမ်ရေ)
  redundancy မရှိလျှင် outage တစ်ကြိမ်လျှင် 2.0 နာရီ ကြာသည်
  hot standby failover ဖြင့် တစ်ကြိမ်လျှင် 5 မိနစ်၊ warm standby ဖြင့် 30 မိနစ် ကြာသည်

No third-party import, no wall-clock, deterministic arithmetic only.
"""

from __future__ import annotations

import argparse

RULE = "=" * 74
THIN = "-" * 74


def main() -> int:
    ap = argparse.ArgumentParser(description="Replica failover cost vs expected outage cost.")
    ap.add_argument("--replica-month", type=float, default=800.0, help="USD per replica per month (assumed)")
    ap.add_argument("--outage-hour", type=float, default=5000.0, help="USD per outage hour (assumed)")
    ap.add_argument("--outages-per-year", type=float, default=4.0, help="stated outage frequency (assumed)")
    ap.add_argument("--outage-hours", type=float, default=2.0, help="stated outage duration, no failover (assumed)")
    ap.add_argument("--hot-failover-min", type=float, default=5.0, help="failover time, hot standby (assumed)")
    ap.add_argument("--warm-failover-min", type=float, default=30.0, help="failover time, warm standby (assumed)")
    args = ap.parse_args()

    replica_year = args.replica_month * 12.0
    print(RULE)
    print("failover_cost - replica ကုန်ကျစရိတ် နှင့် မျှော်မှန်း outage ဆုံးရှုံးမှု (offline, deterministic)")
    print(f"assumptions: replica USD {args.replica_month:.0f}/month = USD {replica_year:.0f}/year, "
          f"outage USD {args.outage_hour:.0f}/hour,")
    print(f"             outage {args.outages_per_year:.0f}/year x {args.outage_hours:.1f} h with no failover")
    print(THIN)
    print(f"{'mode':<22} {'replicas':>8} {'downtime h/yr':>13} {'replica USD/yr':>14} "
          f"{'outage USD/yr':>13} {'total USD/yr':>12}")
    plans = [
        ("no redundancy", 1, args.outage_hours),
        ("warm standby", 2, args.warm_failover_min / 60.0),
        ("hot standby", 2, args.hot_failover_min / 60.0),
        ("hot standby + AZ", 3, args.hot_failover_min / 60.0),
    ]
    rows = []
    for name, replicas, downtime_h in plans:
        downtime = args.outages_per_year * downtime_h
        replica_cost = replica_year * replicas
        outage_cost = downtime * args.outage_hour
        total = replica_cost + outage_cost
        rows.append((name, replicas, downtime, replica_cost, outage_cost, total))
        print(f"{name:<22} {replicas:>8} {downtime:>13.2f} {replica_cost:>14.0f} "
              f"{outage_cost:>13.0f} {total:>12.0f}")
    print(THIN)
    base = rows[0]
    print("marginal trade-off against no redundancy:")
    for row in rows[1:]:
        extra = row[3] - base[3]
        saved = base[4] - row[4]
        print(f"  {row[0]:<22} extra capacity USD {extra:>7.0f}/yr, outage saved USD {saved:>7.0f}/yr, "
              f"net {'saving' if saved > extra else 'cost'} USD {abs(saved - extra):>7.0f}/yr")
    hot = rows[2]
    extra = hot[3] - base[3]
    per_hour = args.outage_hour
    break_even_hours = extra / per_hour if per_hour else 0.0
    break_even_outages = break_even_hours / (args.outage_hours - args.hot_failover_min / 60.0)
    print(THIN)
    print(f"break-even for hot standby: extra USD {extra:.0f}/yr buys "
          f"{extra / per_hour:.2f} outage hours")
    print(f"  = {break_even_outages:.2f} outages/year at {args.outage_hours:.1f} h each, "
          f"i.e. the replica pays for itself above {break_even_outages:.2f} outages/year")
    print(f"  stated frequency {args.outages_per_year:.2f}/year -> "
          f"{'replica is cheaper' if args.outages_per_year > break_even_outages else 'no replica is cheaper'}")
    print(THIN)
    print("မှတ်ချက် - reliability အတွက် ထားရှိသည့် replica သည် ကုန်ကျစရိတ် အမြဲ တိုးစေသည်၊ သို့သော် "
          "မျှော်မှန်း outage ဆုံးရှုံးမှုကို လျှော့ချသည်။ ဆုံးဖြတ်ချက်သည် outage အကြိမ်ရေ၊ "
          "တစ်ကြိမ် ကြာချိန် နှင့် တစ်နာရီ ဆုံးရှုံးမှု သုံးခုအပေါ် မှီခိုသည်။")
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
