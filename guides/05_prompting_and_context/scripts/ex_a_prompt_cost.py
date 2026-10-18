#!/usr/bin/env python3
"""Worked example (a): the input cost of a stated prompt at a stated price.

Token estimator (stated here, and reused by every guide script):

    estimate_tokens(text) = max(1, ceil(len(text) / 4))

that is, four ASCII characters are treated as one token. This is an estimate,
not a tokenizer: real counts depend on the tokenizer, the language and the
whitespace, so the numbers below are modelled, never measured.

Stated price assumptions (not vendor quotes; prices drift over time):

    input  price = USD 3.00 per 1e6 input tokens
    output price = USD 15.00 per 1e6 output tokens
    output length assumed for the total column = 120 tokens

Only the standard library is used and the run is deterministic.
"""

from __future__ import annotations

import math

IN_PRICE = 3.00          # USD per 1e6 input tokens (assumption)
OUT_PRICE = 15.00        # USD per 1e6 output tokens (assumption)
OUT_TOKENS = 120         # assumed answer length per call


def estimate_tokens(text: str) -> int:
    """Stated estimator: 4 ASCII characters = 1 token, rounded up."""
    return max(1, math.ceil(len(text) / 4.0))


SYSTEM_PROMPT = (
    "You are a support assistant. Answer only from the policy text supplied "
    "in the prompt. If the policy does not cover the question, say that the "
    "policy is silent and list what information is missing. Never guess a "
    "refund amount. Cite the policy clause number next to every claim."
)

LONG_SYSTEM_PROMPT = SYSTEM_PROMPT + (
    " Escalate to a human when the customer asks about a charge older than "
    "one hundred and eighty days, when the account is suspended, or when two "
    "policy clauses appear to conflict. In those cases reply with the single "
    "word ESCALATE followed by a one-sentence reason. Keep every answer under "
    "one hundred and twenty words. Use plain language and never expose internal "
    "case identifiers. When the customer writes in a language other than "
    "English, answer in that language but keep the clause numbers unchanged."
)

INSTRUCTIONS = "Answer the customer question using the policy text."

EXAMPLE = (
    "Customer question: how long do I have to return an unopened item? "
    "Policy clause 4.2: unopened items may be returned within thirty days of "
    "delivery. Answer: thirty days, per clause 4.2."
)

QUESTION = "Customer question: my package arrived damaged. Can I get a refund?"


def line(label: str, in_tokens: int) -> None:
    in_cost = in_tokens * IN_PRICE / 1e6
    out_cost = OUT_TOKENS * OUT_PRICE / 1e6
    print("%-34s %9d %14.6f %14.6f"
          % (label, in_tokens, in_cost, in_cost + out_cost))


def main() -> int:
    sys_t = estimate_tokens(SYSTEM_PROMPT)
    long_t = estimate_tokens(LONG_SYSTEM_PROMPT)
    ins_t = estimate_tokens(INSTRUCTIONS)
    ex_t = estimate_tokens(EXAMPLE)
    q_t = estimate_tokens(QUESTION)

    print("estimator: tokens = ceil(characters / 4) ; input USD %.2f/1e6 tok ; "
          "output USD %.2f/1e6 tok ; answer %d tok" % (IN_PRICE, OUT_PRICE, OUT_TOKENS))
    print("fixed parts, in tokens: system=%d  instructions=%d  example=%d  question=%d"
          % (sys_t, ins_t, ex_t, q_t))
    print()
    print("%-34s %9s %14s %14s" % ("prompt variant", "input tok", "input USD", "USD/call"))
    base = sys_t + ins_t + q_t
    line("base (system + task + question)", base)
    for n in (1, 2, 3):
        line("base + %d example(s)" % n, base + n * ex_t)
    long_base = long_t + ins_t + q_t
    line("base with longer system prompt", long_base)
    for n in (1, 2, 3):
        line("longer system + %d example(s)" % n, long_base + n * ex_t)
    print()
    print("what one example adds      : %d input tok = USD %.6f per call" % (ex_t, ex_t * IN_PRICE / 1e6))
    print("what the longer system adds: %d input tok = USD %.6f per call"
          % (long_t - sys_t, (long_t - sys_t) * IN_PRICE / 1e6))
    print("three examples add         : %d input tok = USD %.6f per call"
          % (3 * ex_t, 3 * ex_t * IN_PRICE / 1e6))
    print("the longer system prompt costs %.2fx the short one, before any example"
          % (long_t / sys_t))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
