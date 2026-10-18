#!/usr/bin/env python3
"""ex_c_control_roi - ထိန်းချုပ်မှု (control) တစ်ခု၏ မျှော်မှန်း ဆုံးရှုံးမှု လျော့ချမှုနှင့်
break-even ကုန်ကျစရိတ်ကို တွက်ချက်သည်။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ပုံသေနည်း
    loss_without = likelihood_per_year * impact_usd
    loss_with(e) = likelihood_per_year * (1 - e) * impact_usd
    reduction(e) = loss_without - loss_with(e)
    net_benefit(e) = reduction(e) - control_cost_usd_per_year
    break_even_control_cost = reduction at the stated effectiveness

ယူဆချက် အားလုံးကို output တွင် (assumption) ဟု မှတ်သားထားသည်။
"""

from __future__ import annotations

RULE = "=" * 102
THIN = "-" * 102

LIKELIHOOD_PER_YEAR = 0.25
IMPACT_USD = 400000.0
CONTROL_EFFECTIVENESS = 0.80
CONTROL_COST_USD_PER_YEAR = 60000.0

EFFECTIVENESS_SWEEP = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95]


def loss_without_control(likelihood_per_year: float, impact_usd: float) -> float:
    return likelihood_per_year * impact_usd


def loss_with_control(likelihood_per_year: float, impact_usd: float, effectiveness: float) -> float:
    return likelihood_per_year * (1.0 - effectiveness) * impact_usd


def loss_reduction(likelihood_per_year: float, impact_usd: float, effectiveness: float) -> float:
    return loss_without_control(likelihood_per_year, impact_usd) - loss_with_control(
        likelihood_per_year, impact_usd, effectiveness)


def main() -> int:
    without = loss_without_control(LIKELIHOOD_PER_YEAR, IMPACT_USD)
    with_ = loss_with_control(LIKELIHOOD_PER_YEAR, IMPACT_USD, CONTROL_EFFECTIVENESS)
    reduction = loss_reduction(LIKELIHOOD_PER_YEAR, IMPACT_USD, CONTROL_EFFECTIVENESS)
    print(RULE)
    print("ex_c_control_roi - ထိန်းချုပ်မှု တစ်ခု၏ မျှော်မှန်း ဆုံးရှုံးမှု လျော့ချမှုနှင့် break-even ကုန်ကျစရိတ်")
    print(f"(assumption) incidents_per_year={LIKELIHOOD_PER_YEAR}  impact_usd={IMPACT_USD:,.0f}  "
          f"control_effectiveness={CONTROL_EFFECTIVENESS}  "
          f"control_cost_usd_per_year={CONTROL_COST_USD_PER_YEAR:,.0f}")
    print(THIN)
    print(f"expected loss without control        : {without:>14,.2f} USD/year")
    print(f"expected loss with control           : {with_:>14,.2f} USD/year")
    print(f"expected loss reduction              : {reduction:>14,.2f} USD/year")
    print(f"break-even control cost              : {reduction:>14,.2f} USD/year")
    print(f"net benefit at the stated cost       : {reduction - CONTROL_COST_USD_PER_YEAR:>14,.2f} USD/year")
    print(f"benefit / cost ratio                 : {reduction / CONTROL_COST_USD_PER_YEAR:>14.2f}")
    print(THIN)
    print(f"{'effectiveness':>13} {'loss_with_usd':>15} {'reduction_usd':>15} "
          f"{'net_benefit_usd':>16} {'worth_it':>9}")
    for e in EFFECTIVENESS_SWEEP:
        lw = loss_with_control(LIKELIHOOD_PER_YEAR, IMPACT_USD, e)
        red = loss_reduction(LIKELIHOOD_PER_YEAR, IMPACT_USD, e)
        net = red - CONTROL_COST_USD_PER_YEAR
        print(f"{e:>13.2f} {lw:>15,.2f} {red:>15,.2f} {net:>16,.2f} "
              f"{('yes' if net > 0 else 'no'):>9}")
    print(THIN)
    print(f"the control pays for itself while effectiveness stays above "
          f"{CONTROL_COST_USD_PER_YEAR / IMPACT_USD / LIKELIHOOD_PER_YEAR:.2f} at this likelihood and impact")
    print("မှတ်ချက် - likelihood နှင့် impact သည် ခန့်မှန်း ယူဆချက် ဖြစ်သည်၊ effectiveness ကို "
          "red team နှင့် monitoring ဖြင့် တိုင်းတာရမည်။ residual risk ကို မှတ်တမ်းတင်ထားရမည်။")
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
