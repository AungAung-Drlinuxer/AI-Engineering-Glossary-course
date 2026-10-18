#!/usr/bin/env python3
"""lab_agent_loop - agent loop တစ်ခု၏ step တိုင်း token၊ context နှင့် cost ကို ပြသည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။
မော်ဒယ် ကို ခေါ်ယူခြင်း မပြုပါ၊ loop ကို တွက်ချက်မှုဖြင့် တူညီစွာ ဖော်ပြသည်။

Loop model (assumption များ)
    context သည် system prompt၊ tool schema နှင့် task ဖြင့် စတင်သည် (--context token)။
    step တိုင်းတွင် prompt token အားလုံးကို ပြန်လည် ပေးပို့သည်။
    step တိုင်း assistant သည် reasoning 120 + tool call 40 = 160 token ထုတ်သည်။
    --tool-calls အရေအတွက် အထိ tool call တိုင်းသည် --result-tokens token ရလဒ်
    တစ်ခု ပြန်လည် ရရှိသည်၊ ထို့နောက် step များတွင် ရလဒ် ထပ်မံ မထည့်တော့ပါ။
    cost = prompt_token * price + output_token * price * 5.0
    KV = context token * 0.5 MiB (layers 32, heads 32, head_dim 128, fp16)

stop ဖြစ်သည့် အခြေအနေ နှစ်ခု - step budget (--max-steps) သို့မဟုတ် cost budget
(--cost-budget)။ lab သည် မည်သည့် တစ်ခုက အရင် ရပ်တန့်စေသည်ကို ပြသည်။
"""

from __future__ import annotations

import argparse

OUTPUT_PRICE_MULT = 5.0
REASONING_TOKENS = 120
TOOL_CALL_TOKENS = 40
KV_MIB_PER_TOKEN = 0.5
SWEEP_STEPS = (2, 4, 8, 16, 32)
RULE = "=" * 74
THIN = "-" * 74


def simulate(max_steps: int, tool_calls: int, result_tokens: int, context: int,
             price_per_mtok: float, cost_budget: float) -> tuple[list[dict], str]:
    """Loop ကို တွက်သည်။ (rows, stop_reason) ကို ပြန်ပေးသည်။"""
    rows: list[dict] = []
    ctx = context
    cumulative = 0.0
    stop = "step"
    for step in range(1, max_steps + 1):
        prompt = ctx
        output = REASONING_TOKENS + TOOL_CALL_TOKENS
        step_cost = (prompt * price_per_mtok
                     + output * price_per_mtok * OUTPUT_PRICE_MULT) / 1e6
        cumulative += step_cost
        uses_tool = step <= tool_calls
        ctx += output + (result_tokens if uses_tool else 0)
        rows.append({"step": step, "prompt": prompt, "output": output, "ctx": ctx,
                     "kv_mib": ctx * KV_MIB_PER_TOKEN, "step_cost": step_cost,
                     "cum": cumulative, "tool": uses_tool})
        if cumulative > cost_budget:
            stop = "cost"
            break
    return rows, stop


def print_report(max_steps: int, tool_calls: int, result_tokens: int, context: int,
                 price_per_mtok: float, cost_budget: float) -> None:
    rows, stop = simulate(max_steps, tool_calls, result_tokens, context,
                          price_per_mtok, cost_budget)
    print(RULE)
    print("lab_agent_loop - per-step tokens, context growth and cost (offline, deterministic)")
    print(f"max-steps={max_steps}  tool-calls={tool_calls}  result-tokens={result_tokens}  "
          f"context={context:,}  price={price_per_mtok} USD/Mtok  cost-budget={cost_budget} USD")
    print(f"assumption: output tokens cost {OUTPUT_PRICE_MULT}x input, "
          f"KV {KV_MIB_PER_TOKEN} MiB/token (layers 32, heads 32, head_dim 128, fp16)")
    print(THIN)
    print(f"{'step':>4} {'prompt-tok':>11} {'out-tok':>8} {'ctx-after':>10} "
          f"{'ctx KV MiB':>11} {'step USD':>10} {'cum USD':>10} {'call':>5}")
    for r in rows:
        print(f"{r['step']:>4} {r['prompt']:>11,} {r['output']:>8,} {r['ctx']:>10,} "
              f"{r['kv_mib']:>11,.1f} {r['step_cost']:>10.6f} {r['cum']:>10.6f} "
              f"{'tool' if r['tool'] else '-':>5}")
    print(THIN)
    last = rows[-1]
    print(f"stopped by: {'cost budget' if stop == 'cost' else 'step budget'} at step "
          f"{last['step']} of {max_steps} (cost budget {cost_budget} USD)")
    print(f"final context {last['ctx']:,} tokens = {last['kv_mib'] / 1024:.3f} GiB KV ; "
          f"total cost USD {last['cum']:.6f}")
    print(f"prompt tokens billed by re-sending the context: "
          f"{sum(r['prompt'] for r in rows):,} over {len(rows)} step(s)")
    print("မှတ်ချက် - termination condition မရှိလျှင် loop သည် context နှင့် cost ကို "
          "အဆက်မပြတ် ကြီးထွားစေသည်။ step budget နှင့် cost budget နှစ်ခုလုံးကို ကြိုတင် "
          "သတ်မှတ်ရမည်။")
    print(RULE)


def print_sweep(tool_calls: int, result_tokens: int, context: int,
                price_per_mtok: float, cost_budget: float) -> None:
    print(RULE)
    print("lab_agent_loop - step-budget sweep (which limit stops the loop first)")
    print(THIN)
    print(f"{'max-steps':>9} {'final ctx':>11} {'final KV GiB':>13} "
          f"{'total USD':>11} {'stopped by':>11}")
    for steps in SWEEP_STEPS:
        rows, stop = simulate(steps, tool_calls, result_tokens, context,
                              price_per_mtok, cost_budget)
        last = rows[-1]
        print(f"{steps:>9} {last['ctx']:>11,} {last['kv_mib'] / 1024:>13.3f} "
              f"{last['cum']:>11.6f} {('cost' if stop == 'cost' else 'step'):>11}")
    print(THIN)
    print("မှတ်ချက် - step budget တိုးလျှင် context နှင့် ကုန်ကျစရိတ် နှစ်ခုလုံး တိုးသည်။ "
          "cost budget သည် သတ်မှတ် ကန့်သတ်ချက် ဖြစ်လာသည့်အခါ loop သည် အချိန်မတိုင်မီ ရပ်သည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    rows, stop = simulate(8, 3, 900, 4096, 3.0, 0.5)

    step_ok = rows[0]["prompt"] == 4096 and all(
        rows[i]["prompt"] == rows[i - 1]["ctx"] for i in range(1, len(rows)))
    print(f"[OK] each step re-sends the previous context as its prompt: {step_ok}")
    ok = ok and step_ok

    grow = all(rows[i]["ctx"] > rows[i - 1]["ctx"] for i in range(1, len(rows)))
    print(f"[OK] the context grows at every step (4096 -> {rows[-1]['ctx']:,} tokens): {grow}")
    ok = ok and grow

    cost_up = all(rows[i]["cum"] > rows[i - 1]["cum"] for i in range(1, len(rows)))
    print(f"[OK] cumulative cost rises at every step (USD {rows[-1]['cum']:.6f} total): {cost_up}")
    ok = ok and cost_up

    few, _ = simulate(8, 1, 900, 4096, 3.0, 0.5)
    many, _ = simulate(8, 5, 900, 4096, 3.0, 0.5)
    tool_ok = many[-1]["ctx"] > few[-1]["ctx"]
    print(f"[OK] more tool calls mean a bigger final context "
          f"({many[-1]['ctx']:,} > {few[-1]['ctx']:,} tokens): {tool_ok}")
    ok = ok and tool_ok

    tight, tight_stop = simulate(64, 3, 900, 4096, 3.0, 0.06)
    loose, loose_stop = simulate(64, 3, 900, 4096, 3.0, 5.0)
    stop_ok = tight_stop == "cost" and loose_stop == "step" and len(tight) < len(loose)
    print(f"[OK] the cost budget stops the loop first and sooner "
          f"(step {tight[-1]['step']} < step {loose[-1]['step']}): {stop_ok}")
    ok = ok and stop_ok

    again, _ = simulate(8, 3, 900, 4096, 3.0, 0.5)
    det = again == rows and stop == "step"
    print(f"[OK] the loop is deterministic for fixed inputs: {det}")
    ok = ok and det

    print("[PASS] lab_agent_loop self-test passed." if ok
          else "[FAIL] lab_agent_loop self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Simulate a deterministic agent loop: tokens, context, cost (offline).")
    ap.add_argument("--max-steps", type=int, default=8, help="step budget of the loop")
    ap.add_argument("--tool-calls", type=int, default=3,
                    help="how many of the first steps return a tool result")
    ap.add_argument("--result-tokens", type=int, default=900,
                    help="tokens appended by one tool result")
    ap.add_argument("--context", type=int, default=4096,
                    help="starting prompt tokens (system + tool schema + task)")
    ap.add_argument("--price-per-mtok", type=float, default=3.0,
                    help="input price in USD per million tokens (assumption)")
    ap.add_argument("--cost-budget", type=float, default=0.5,
                    help="USD budget that can stop the loop before the step budget")
    ap.add_argument("--sweep", action="store_true", help="sweep the step budget 2..32")
    ap.add_argument("--self-test", action="store_true",
                    help="assert the properties this lab teaches")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.tool_calls, args.result_tokens, args.context,
                    args.price_per_mtok, args.cost_budget)
        return 0
    print_report(args.max_steps, args.tool_calls, args.result_tokens, args.context,
                 args.price_per_mtok, args.cost_budget)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
