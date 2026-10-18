#!/usr/bin/env python3
"""lab_blast_radius - tool နှင့် data scope ပြန့်ကားမှု (blast radius) ကို
as-configured နှင့် least-privilege နှစ်မျိုးဖြင့် နှိုင်းယှဉ်သည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ပုံသေနည်း
    configured_scope = tools * data_scopes
    lp_scopes_per_tool = max(1, round(data_scopes * (1 - over_permission)))
    least_privilege_scope = tools * lp_scopes_per_tool
    risk_configured = configured_scope * likelihood * impact
    risk_least_privilege = least_privilege_scope * likelihood * impact
    reduction = risk_configured - risk_least_privilege
"""

from __future__ import annotations

import argparse

RULE = "=" * 102
THIN = "-" * 102

SWEEP_OVER_PERMISSION = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


def configured_scope(tools: int, data_scopes: int) -> int:
    return tools * data_scopes


def least_privilege_scope(tools: int, data_scopes: int, over_permission: float) -> int:
    per_tool = max(1, round(data_scopes * (1.0 - over_permission)))
    return tools * per_tool


def risk_usd(scope: int, likelihood: float, impact: float) -> float:
    return scope * likelihood * impact


def print_report(tools: int, data_scopes: int, over_permission: float,
                 likelihood: float, impact: float) -> None:
    cfg = configured_scope(tools, data_scopes)
    lp = least_privilege_scope(tools, data_scopes, over_permission)
    rc = risk_usd(cfg, likelihood, impact)
    rl = risk_usd(lp, likelihood, impact)
    print(RULE)
    print("lab_blast_radius - as-configured နှင့် least-privilege reachable scope")
    print(f"tools={tools}  data_scopes={data_scopes}  over_permission={over_permission:g}  "
          f"likelihood={likelihood:g}  impact_usd={impact:,.0f}")
    print("(assumption) likelihood and impact are stated assumptions; scope units are tool-scope pairs")
    print(THIN)
    print(f"as-configured reachable scope   : {cfg:>14,} tool-scope pairs")
    print(f"least-privilege reachable scope : {lp:>14,} tool-scope pairs")
    print(f"scope reduction                 : {cfg - lp:>14,} pairs "
          f"({(1.0 - lp / cfg) * 100:.1f}%)")
    print(f"risk as configured              : {rc:>14,.2f} USD/year")
    print(f"risk under least privilege      : {rl:>14,.2f} USD/year")
    print(f"risk reduction from the control : {rc - rl:>14,.2f} USD/year")
    print(f"residual risk after the control : {rl:>14,.2f} USD/year")
    print(THIN)
    print("မှတ်ချက် - agent တစ်ခုသည် လိုအပ်သည်ထက် ကျယ်သည့် scope ရှိလျှင် ခိုးယူခံရသော "
          "အခြေအနေတွင် ထိခိုက်နိုင်သည့် ပမာဏ ကြီးသည်၊ least privilege သည် scope ကို "
          "ကျဉ်းစေပြီး ခွင့်ပြုချက် တောင်းခံမှုကို မှတ်တမ်းတင်ရမည်။")
    print(RULE)


def print_sweep(tools: int, data_scopes: int, likelihood: float, impact: float) -> None:
    cfg = configured_scope(tools, data_scopes)
    print(RULE)
    print("lab_blast_radius - over_permission sweep (scope နှင့် risk)")
    print(f"tools={tools}  data_scopes={data_scopes}  likelihood={likelihood:g}  impact_usd={impact:,.0f}")
    print(THIN)
    print(f"{'over_permission':>16} {'configured':>12} {'least_privilege':>16} "
          f"{'reduction_pct':>14} {'risk_cfg_usd':>15} {'risk_lp_usd':>14}")
    for op in SWEEP_OVER_PERMISSION:
        lp = least_privilege_scope(tools, data_scopes, op)
        print(f"{op:>16.1f} {cfg:>12,} {lp:>16,} {(1.0 - lp / cfg) * 100:>14.1f} "
              f"{risk_usd(cfg, likelihood, impact):>15,.0f} {risk_usd(lp, likelihood, impact):>14,.0f}")
    print(THIN)
    print("မှတ်ချက် - over_permission မြင့်လျှင် least-privilege scope သည် ကျဉ်းသည်၊ "
          "သို့သော် scope လျှော့ချမှုသည် အလုပ် တူညီစွာ လုပ်နိုင်မှုကို မထိခိုက်ကြောင်း "
          "စမ်းသပ်ရမည်။")
    print(RULE)


def self_test() -> int:
    ok = True

    cfg = configured_scope(12, 9)
    cfg_ok = cfg == 108
    print(f"[OK] as-configured scope is tools times data_scopes ({cfg}): {cfg_ok}")
    ok = ok and cfg_ok

    lp0 = least_privilege_scope(12, 9, 0.0)
    none = lp0 == cfg
    print(f"[OK] with no over-permission the two scopes agree ({cfg} == {lp0}): {none}")
    ok = ok and none

    lp50 = least_privilege_scope(12, 9, 0.5)
    lp80 = least_privilege_scope(12, 9, 0.8)
    shrinks = lp80 < lp50 < cfg
    print(f"[OK] more over-permission means a smaller least-privilege scope ({cfg} > {lp50} > {lp80}): {shrinks}")
    ok = ok and shrinks

    r1 = risk_usd(cfg, 0.25, 400000.0)
    r2 = risk_usd(cfg, 0.50, 400000.0)
    lin = abs(r2 - 2.0 * r1) < 1e-6
    print(f"[OK] risk scales linearly with likelihood ({r1:,.0f} -> {r2:,.0f}): {lin}")
    ok = ok and lin

    dbl = configured_scope(24, 9) == 2 * configured_scope(12, 9)
    print(f"[OK] doubling the tools doubles the reachable scope ({configured_scope(12, 9)} -> "
          f"{configured_scope(24, 9)}): {dbl}")
    ok = ok and dbl

    print("[PASS] lab_blast_radius self-test passed." if ok
          else "[FAIL] lab_blast_radius self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Reachable tool and data scope, as configured vs least privilege (offline, deterministic).")
    ap.add_argument("--tools", type=int, default=12)
    ap.add_argument("--data-scopes", type=int, default=9)
    ap.add_argument("--over-permission", type=float, default=0.55)
    ap.add_argument("--likelihood", type=float, default=0.25)
    ap.add_argument("--impact", type=float, default=400000.0)
    ap.add_argument("--sweep", action="store_true", help="over_permission 0.0..0.9 sweep")
    ap.add_argument("--self-test", action="store_true", help="assert the real properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.tools, args.data_scopes, args.likelihood, args.impact)
        return 0
    print_report(args.tools, args.data_scopes, args.over_permission, args.likelihood, args.impact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
