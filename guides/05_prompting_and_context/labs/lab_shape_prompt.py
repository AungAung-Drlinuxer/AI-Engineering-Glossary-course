#!/usr/bin/env python3
"""lab_shape_prompt - build a prompt from fixed parts and check its sections.

Offline, deterministic, standard library only.

The prompt is assembled from fixed text parts. Nothing is random: the seed only
selects one of the fixed sample requests, so the same seed always yields the
same prompt and the same token estimate.

Token estimator (stated, the only source of the token counts below)

    estimate_tokens(text) = max(1, ceil(len(text) / 4))

Structure of the built prompt

    system        role and constraints
    instructions  task statement
    format        output format
    examples      one demonstration block per requested example
    cot           reasoning request, present only when --cot on
    input         the request text

Rule-based section check: every task declares the sections it requires, and the
check reports each required section as present or missing.
"""

from __future__ import annotations

import argparse
import math

COT_INSTRUCTION = "Think step by step and show the steps before the final answer."

SYSTEM = (
    "You are a careful assistant that answers from the supplied text only. "
    "Never invent facts. Reply in the format the task requests."
)

TASKS = {
    "classify": {
        "instruction": "Classify the customer message into one of: billing, delivery, product, other.",
        "format": 'Reply with JSON: {"label": <one label>, "confidence": <0 to 1>}.',
        "example": 'Customer message: "My invoice shows a charge I did not approve." '
                   '-> {"label": "billing", "confidence": 0.94}',
        "required": ["system", "instructions", "format", "examples", "input"],
        "inputs": [
            'Customer message: "The tracking link has not updated for five days."',
            'Customer message: "I was charged twice for the same order."',
        ],
    },
    "summarise": {
        "instruction": "Summarise the supplied report in three sentences.",
        "format": "Reply with plain prose, no headings and no lists.",
        "example": "Report: quarterly revenue rose eight percent while support volume fell. "
                   "-> Revenue rose eight percent and support volume fell over the quarter.",
        "required": ["system", "instructions", "input"],
        "inputs": [
            "Report: latency fell by twelve percent after caching was enabled.",
            "Report: churn rose in the second quarter and recovered in the third.",
        ],
    },
    "extract": {
        "instruction": "Extract every date and every amount from the supplied invoice text.",
        "format": "Reply with one line per item as <type> <value>.",
        "example": 'Invoice text: "Due date 2026-03-01, total 240.50 USD" '
                   '-> date 2026-03-01 ; amount 240.50',
        "required": ["system", "instructions", "format", "input"],
        "inputs": [
            'Invoice text: "Issued 2026-01-15, due 2026-02-14, total 1840.00 USD"',
            'Invoice text: "Credit note 2026-02-02 for 320.75 USD against invoice 55"',
        ],
    },
}

RULE = "=" * 74
THIN = "-" * 74


def estimate_tokens(text: str) -> int:
    """Stated estimator: 4 ASCII characters = 1 token, rounded up."""
    return max(1, math.ceil(len(text) / 4.0)) if text else 0


def build(task: str, examples: int, cot: bool, seed: int) -> list[tuple[str, str, str]]:
    spec = TASKS[task]
    inputs = spec["inputs"]
    parts: list[tuple[str, str, str]] = [
        ("system", SYSTEM, "role and constraints"),
        ("instructions", str(spec["instruction"]), "task statement"),
        ("format", str(spec["format"]), "output format"),
    ]
    if examples > 0:
        block = "\n".join("%d. %s" % (i + 1, spec["example"]) for i in range(examples))
        parts.append(("examples", block, "%d demonstration(s)" % examples))
    if cot:
        parts.append(("cot", COT_INSTRUCTION, "reasoning request"))
    else:
        parts.append(("cot", "", "not requested"))
    parts.append(("input", str(inputs[seed % len(inputs)]), "request text"))
    return parts


def total_tokens(parts: list[tuple[str, str, str]]) -> int:
    return sum(estimate_tokens(text) for _, text, _ in parts)


def check_sections(parts: list[tuple[str, str, str]], required: list[str]) -> list[str]:
    present = {name for name, _, _ in parts if name}
    return [name for name in required if name not in present]


def print_report(task: str, examples: int, cot: bool, seed: int) -> None:
    parts = build(task, examples, cot, seed)
    total = total_tokens(parts)
    missing = check_sections(parts, TASKS[task]["required"])
    print(RULE)
    print("lab_shape_prompt - build a prompt and check its sections (offline, deterministic)")
    print("task=%s  examples=%d  cot=%s  seed=%d" % (task, examples, "on" if cot else "off", seed))
    print(THIN)
    print("token estimate (estimator: tokens = ceil(characters / 4)):")
    print("  total prompt: %d tokens" % total)
    print("structure:")
    print("  prompt")
    for name, text, note in parts:
        print("  +-- %-12s %4d tok  %s" % (name, estimate_tokens(text), note))
    print(THIN)
    print("required sections for task %s: %s" % (task, ", ".join(TASKS[task]["required"])))
    present = {name for name, _, _ in parts if name}
    for name in TASKS[task]["required"]:
        if name in present:
            print("  [OK] %s present" % name)
        else:
            print("  [MISS] %s missing" % name)
    if missing:
        print("  [WARN] %d required section(s) missing: %s" % (len(missing), ", ".join(missing)))
    else:
        print("  [OK] all required sections present")
    print(THIN)
    print("examples block: %d x one demonstration ; cot request: %s"
          % (examples, "included" if cot else "absent"))
    print("မှတ်ချက် - ပုံသေ အစိတ်အပိုင်းများမှ prompt တစ်ခု တည်ဆောက်သည်၊ လိုအပ်သည့် အပိုင်း အားလုံး "
          "ပါဝင်မှသာ format လိုက်နာမှုကို ယုံကြည်နိုင်သည်။")
    print(RULE)


def print_sweep(task: str, seed: int) -> None:
    print(RULE)
    print("lab_shape_prompt - sweep: examples 0 -> 5, cot off and on")
    print("task=%s  seed=%d" % (task, seed))
    print(THIN)
    print("%10s %14s %14s %12s" % ("examples", "cot off tok", "cot on tok", "cot adds"))
    for n in range(6):
        off = total_tokens(build(task, n, False, seed))
        on = total_tokens(build(task, n, True, seed))
        print("%10d %14d %14d %12d" % (n, off, on, on - off))
    print(THIN)
    print("trend: prompt tokens rise with the example count and with the cot request")
    print(RULE)


def self_test() -> int:
    ok = True

    off = total_tokens(build("classify", 2, False, 7))
    on = total_tokens(build("classify", 2, True, 7))
    cot_ok = on > off
    print("[OK] turning cot on raises the token count (%d -> %d): %s" % (off, on, cot_ok))
    ok = ok and cot_ok

    a = total_tokens(build("classify", 1, False, 7))
    b = total_tokens(build("classify", 3, False, 7))
    step1 = b - a
    c = total_tokens(build("classify", 5, False, 7))
    linear_ok = (c - b) == step1 and step1 > 0
    print("[OK] each extra example adds the same token amount (%d per two examples): %s"
          % (step1, linear_ok))
    ok = ok and linear_ok

    full = build("classify", 2, False, 7)
    full_missing = check_sections(full, TASKS["classify"]["required"])
    print("[OK] the default classify prompt has every required section: %s" % (not full_missing))
    ok = ok and not full_missing

    none = build("classify", 0, False, 7)
    none_missing = check_sections(none, TASKS["classify"]["required"])
    miss_ok = none_missing == ["examples"]
    print("[OK] dropping the examples block is detected as a missing section (%s): %s"
          % (none_missing, miss_ok))
    ok = ok and miss_ok

    same = total_tokens(build("extract", 2, True, 3)) == total_tokens(build("extract", 2, True, 3))
    print("[OK] the same knobs and the same seed build the same prompt: %s" % same)
    ok = ok and same

    shorter = total_tokens(build("summarise", 1, False, 0)) < total_tokens(build("summarise", 4, False, 0))
    print("[OK] the token estimate grows with the prompt size: %s" % shorter)
    ok = ok and shorter

    print("[PASS] lab_shape_prompt self-test passed." if ok
          else "[FAIL] lab_shape_prompt self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Prompt-shaping lab (offline, deterministic).")
    ap.add_argument("--examples", type=int, default=2, help="number of demonstration blocks")
    ap.add_argument("--cot", choices=("on", "off"), default="off", help="request step-by-step reasoning")
    ap.add_argument("--task", choices=sorted(TASKS), default="classify", help="task to shape for")
    ap.add_argument("--seed", type=int, default=7, help="selects one of the fixed sample requests")
    ap.add_argument("--sweep", action="store_true", help="sweep the example count with cot off and on")
    ap.add_argument("--self-test", action="store_true", help="assert the shaping properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.task, args.seed)
        return 0
    print_report(args.task, args.examples, args.cot == "on", args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
