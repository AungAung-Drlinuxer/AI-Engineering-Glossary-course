#!/usr/bin/env python3
"""Worked example (a): tokens and cost of one eval run for a stated eval size, model and price.

DERIVATION, not a benchmark. Every price and token count below is a stated
assumption that a real project must replace with its own vendor numbers.

Assumptions (all labelled, all setup-dependent):
    eval size                 = 500 items (also swept over 100 / 500 / 2000)
    answer prompt per item    = 1200 tokens
    answer output per item    = 300 tokens
    answer model price        = USD 0.50 / 1e6 input tokens, USD 1.50 / 1e6 output tokens
    judge rubric per item     = 200 tokens, judge output = 60 tokens
    judge model price         = USD 0.30 / 1e6 input tokens, USD 0.10 / 1e6 output tokens
    judge input per item      = prompt (1200) + answer (300) + rubric (200)
    human review              = 5% of items, USD 2.00 per reviewed item
    stored per run per item   = 4 KiB transcript + 1 KiB judge verdict

Formulas:
    answer_in_tokens  = items * 1200
    answer_out_tokens = items * 300
    judge_in_tokens   = items * 1700
    judge_out_tokens  = items * 60
    answer_usd        = in_tok/1e6 * 0.50 + out_tok/1e6 * 1.50
    judge_usd         = in_tok/1e6 * 0.30 + out_tok/1e6 * 0.10
    human_usd         = items * 0.05 * 2.00
"""

ITEMS = 500
PROMPT_TOKENS = 1200
ANSWER_TOKENS = 300
RUBRIC_TOKENS = 200
JUDGE_OUT_TOKENS = 60
ANSWER_PRICE_IN = 0.50
ANSWER_PRICE_OUT = 1.50
JUDGE_PRICE_IN = 0.30
JUDGE_PRICE_OUT = 0.10
HUMAN_FRACTION = 0.05
HUMAN_USD = 2.00
TRANSCRIPT_KIB = 4.0
VERDICT_KIB = 1.0
RUNS_PER_DAY = 4

RULE = "=" * 74
THIN = "-" * 74


def run_cost(items: int, judge: bool) -> dict:
    """Return the token and cost breakdown of one eval pass over `items` items."""
    answer_in = items * PROMPT_TOKENS
    answer_out = items * ANSWER_TOKENS
    judge_in = items * (PROMPT_TOKENS + ANSWER_TOKENS + RUBRIC_TOKENS) if judge else 0
    judge_out = items * JUDGE_OUT_TOKENS if judge else 0
    answer_usd = answer_in / 1e6 * ANSWER_PRICE_IN + answer_out / 1e6 * ANSWER_PRICE_OUT
    judge_usd = judge_in / 1e6 * JUDGE_PRICE_IN + judge_out / 1e6 * JUDGE_PRICE_OUT
    human_usd = items * HUMAN_FRACTION * HUMAN_USD
    storage_mib = items * (TRANSCRIPT_KIB + VERDICT_KIB) / 1024.0
    return {
        "items": items,
        "answer_in": answer_in,
        "answer_out": answer_out,
        "judge_in": judge_in,
        "judge_out": judge_out,
        "answer_usd": answer_usd,
        "judge_usd": judge_usd,
        "human_usd": human_usd,
        "total_usd": answer_usd + judge_usd + human_usd,
        "storage_mib": storage_mib,
    }


def main() -> None:
    print(RULE)
    print("ex_a_eval_run_cost - one eval run: tokens, USD and storage (offline, deterministic)")
    print("assumptions: prompt 1200 tok, answer 300 tok, judge rubric 200 tok, judge out 60 tok")
    print("             answer model USD 0.50/1e6 in, USD 1.50/1e6 out")
    print("             judge  model USD 0.30/1e6 in, USD 0.10/1e6 out")
    print("             human review 5% at USD 2.00/item, storage 5 KiB/item/run")
    print(THIN)
    print("%6s %10s %11s %11s %10s %10s %10s %12s %11s"
          % ("items", "answer_in", "answer_out", "judge_in", "answer$", "judge$", "human$", "total$", "storage_MiB"))
    for items in (100, 500, 2000):
        for judge in (False, True):
            r = run_cost(items, judge)
            print("%6d %10d %11d %11d %10.4f %10.4f %10.4f %12.4f %11.2f"
                  % (r["items"], r["answer_in"], r["answer_out"], r["judge_in"],
                     r["answer_usd"], r["judge_usd"], r["human_usd"], r["total_usd"], r["storage_mib"]))
    print(THIN)
    r_no = run_cost(ITEMS, judge=False)
    r_yes = run_cost(ITEMS, judge=True)
    print("at the default eval size of %d items:" % ITEMS)
    print("  answer model only        : USD %8.4f per run  (%.6f USD per item)" % (r_no["total_usd"], r_no["total_usd"] / ITEMS))
    print("  with an LLM judge        : USD %8.4f per run  (%.6f USD per item)" % (r_yes["total_usd"], r_yes["total_usd"] / ITEMS))
    print("  judge share of the run   : %6.1f%%  (judge USD %.4f of total USD %.4f)"
          % (100.0 * r_yes["judge_usd"] / r_yes["total_usd"], r_yes["judge_usd"], r_yes["total_usd"]))
    print("  human review share       : %6.1f%%  (USD %.4f)" % (100.0 * r_yes["human_usd"] / r_yes["total_usd"], r_yes["human_usd"]))
    print("  cost ratio judge / no judge : %.2fx" % (r_yes["total_usd"] / r_no["total_usd"]))
    print("  storage per run            : %.2f MiB ; %d runs/day -> %.1f MiB/day"
          % (r_yes["storage_mib"], RUNS_PER_DAY, r_yes["storage_mib"] * RUNS_PER_DAY))
    print("  cost at %d runs/day        : USD %.2f per day ; USD %.2f per 30 days"
          % (RUNS_PER_DAY, r_yes["total_usd"] * RUNS_PER_DAY, r_yes["total_usd"] * RUNS_PER_DAY * 30))
    print(THIN)
    print("မှတ်ချက် - eval run ၏ ကုန်ကျစရိတ်ကို item အရေအတွက်က အဓိက ဆုံးဖြတ်သည်၊ token ကုန်ကျစရိတ်သည်")
    print("item အရေအတွက်နှင့် တိုက်ရိုက် အချိုးကျ တိုးသည်။ ဤယူဆချက်များ အောက်တွင် လူသား ပြန်လည်")
    print("စစ်ဆေးမှုသည် စုစုပေါင်း၏ ၉၈.၅ ရာခိုင်နှုန်းကို စားပြီး judge token သည် ၀.၅ ရာခိုင်နှုန်းသာ ဖြစ်သည်။")
    print("ထို့ကြောင့် ကုန်ကျစရိတ်ကို လျှော့ချရန် ဦးစားပေးရမည့်အရာသည် review အရေအတွက် ဖြစ်သည်။")
    print("စျေးနှုန်း တိုင်းသည် vendor အလိုက် ကွာခြားသည့်အတွက် ကိန်းဂဏန်း အားလုံးသည်")
    print("'တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်' ဖြစ်သည်။")
    print(RULE)


if __name__ == "__main__":
    main()
