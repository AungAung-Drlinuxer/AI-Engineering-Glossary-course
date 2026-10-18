#!/usr/bin/env python3
"""lab_tool_schema - tool schema သည် turn တိုင်း ကုန်ကျသည့် token နှင့် cache saving ကို ပြသည့် lab။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။
မော်ဒယ် ကို ခေါ်ယူခြင်း မပြုပါ။

Schema token model (assumption များ)
    schema_tokens = wrapper 30 + tools * (tool overhead 42 + fields * field cost 18)
    tool တိုင်း၏ ဖော်ပြချက်၊ နာမည်နှင့် routing စာသားသည် 42 token ခန့် ဖြစ်သည်။
    field တိုင်း၏ နာမည်၊ အမျိုးအစားနှင့် ဖော်ပြချက်သည် 18 token ခန့် ဖြစ်သည်။
    schema prefix ကို turn တိုင်း ပြန်လည် ပေးပို့သည်။

Prefix caching (assumption များ)
    ပထမ ရေးသွင်းမှုတွင် prefix ကို 1.25x ဖြင့် ကျသင့်သည်၊ နောက်ပိုင်း turn တိုင်းတွင်
    0.25x ဖြင့် ကျသင့်သည်။ တူညီသည့် prefix ကို ထပ်ခါတလဲလဲ ပေးပို့သည့်အခါ ဤနှုန်းသည်
    saving ကို ဖြစ်ပေါ်စေသည်။

Tool call validation - ပုံသေ tool spec နှစ်ခု (read_file၊ search_docs) အတွက် ပုံသေ
ခေါ်ယူမှု စာရင်းကို စစ်ဆေးသည်။ ဤစစ်ဆေးမှုသည် deterministic ဖြစ်သည်။
"""

from __future__ import annotations

import argparse
import json

WRAPPER_TOKENS = 30
TOOL_OVERHEAD_TOKENS = 42
FIELD_TOKENS = 18
CACHE_WRITE_MULT = 1.25
CACHE_READ_MULT = 0.25
SWEEP_TURNS = (1, 2, 4, 8, 16)
REQUIRED = {"read_file": {"path": "string"},
            "search_docs": {"query": "string", "limit": "integer"}}
ALLOWED = {"read_file": {"path": "string"},
           "search_docs": {"query": "string", "limit": "integer"}}
SAMPLES = [
    ("valid read_file call",
     '{"tool": "read_file", "args": {"path": "/srv/app/main.py"}}'),
    ("unknown tool name",
     '{"tool": "write_file", "args": {"path": "/srv/app/main.py"}}'),
    ("required field missing",
     '{"tool": "read_file", "args": {}}'),
    ("wrong field type",
     '{"tool": "search_docs", "args": {"query": 42}}'),
    ("unexpected field",
     '{"tool": "search_docs", "args": {"query": "kv cache", "limit": 5, "top_k": 3}}'),
    ("duplicate key in args",
     '{"tool": "read_file", "args": {"path": "/a", "path": "/b"}}'),
]
RULE = "=" * 74
THIN = "-" * 74


def schema_tokens(tools: int, fields: int) -> int:
    return WRAPPER_TOKENS + tools * (TOOL_OVERHEAD_TOKENS + fields * FIELD_TOKENS)


def prefix_cost(prefix_tokens: int, turns: int, price_per_mtok: float) -> tuple[float, float]:
    """(no cache cost, cache cost) ကို USD ဖြင့် ပြန်ပေးသည်။"""
    plain = prefix_tokens * turns * price_per_mtok / 1e6
    cached = prefix_tokens * (CACHE_WRITE_MULT + CACHE_READ_MULT * (turns - 1)) \
        * price_per_mtok / 1e6
    return plain, cached


def validate(raw: str) -> tuple[bool, str]:
    """JSON စာသားတစ်ခုကို tool spec နှင့် စစ်ဆေးသည်။"""
    try:
        pairs = json.loads(raw, object_pairs_hook=lambda p: p)
    except json.JSONDecodeError as exc:
        return False, f"invalid JSON: {exc.msg}"
    if not isinstance(pairs, list):
        return False, "top level must be an object"
    seen: list[str] = []
    for key, value in pairs:
        if key in seen:
            return False, f"duplicate key: {key}"
        seen.append(key)
    body = dict(pairs)
    name = body.get("tool")
    if name not in REQUIRED:
        return False, f"unknown tool name: {name}"
    args_pairs = body.get("args")
    if not isinstance(args_pairs, list):
        return False, "args must be an object"
    arg_keys = [k for k, _ in args_pairs]
    for key, _ in args_pairs:
        if arg_keys.count(key) > 1:
            return False, f"duplicate key: {key}"
    args = dict(args_pairs)
    for field, kind in REQUIRED[name].items():
        if field not in args:
            return False, f"missing required field: {field}"
        expected = {"string": str, "integer": int}[kind]
        value = args[field]
        if isinstance(value, bool) or not isinstance(value, expected):
            return False, f"field {field} must be {kind}"
    for field in args:
        if field not in ALLOWED[name]:
            return False, f"unexpected field: {field}"
    return True, "accepted"


def print_report(tools: int, fields: int, turns: int, price_per_mtok: float) -> None:
    schema = schema_tokens(tools, fields)
    plain, cached = prefix_cost(schema, turns, price_per_mtok)
    print(RULE)
    print("lab_tool_schema - schema tokens per turn, cache saving, call validation")
    print(f"tools={tools}  fields={fields}  turns={turns}  price={price_per_mtok} USD/Mtok")
    print(f"assumption: wrapper {WRAPPER_TOKENS} + tools x (tool {TOOL_OVERHEAD_TOKENS} + "
          f"fields x field {FIELD_TOKENS}) = {schema} tokens of schema, sent every turn")
    print(f"assumption: cache write {CACHE_WRITE_MULT}x on turn 1, "
          f"cache read {CACHE_READ_MULT}x afterwards")
    print(THIN)
    print(f"{'turn':>4} {'schema tok':>11} {'sent so far':>12} {'plain USD':>11} "
          f"{'cached USD':>11} {'saved USD':>11}")
    for turn in range(1, turns + 1):
        p, c = prefix_cost(schema, turn, price_per_mtok)
        print(f"{turn:>4} {schema:>11,} {schema * turn:>12,} {p:>11.6f} {c:>11.6f} "
              f"{p - c:>11.6f}")
    print(THIN)
    saving = 100.0 * (plain - cached) / plain if plain else 0.0
    print(f"schema overhead over {turns} turn(s): {schema * turns:,} tokens, "
          f"USD {plain:.6f} plain vs USD {cached:.6f} cached (saving {saving:.2f}%)")
    print(THIN)
    print("deterministic validation of sample tool calls:")
    print(f"{'sample':<32} {'verdict':>8}  reason")
    accepted = 0
    for label, raw in SAMPLES:
        good, reason = validate(raw)
        accepted += 1 if good else 0
        print(f"{label:<32} {('OK' if good else 'REJECT'):>8}  {reason}")
    print(THIN)
    print(f"samples: {accepted} accepted, {len(SAMPLES) - accepted} rejected before execution")
    print("မှတ်ချက် - schema ကို turn တိုင်း ပေးပို့ခြင်းသည် token ကုန်ကျသည်၊ prefix cache "
          "ဖြင့် ပြန်လည် အသုံးပြုနိုင်သည်။ validated tool contract မပါဘဲ malformed call ကို "
          "လုပ်ဆောင်ခြင်း မပြုရ။")
    print(RULE)


def print_sweep(tools: int, fields: int, price_per_mtok: float) -> None:
    schema = schema_tokens(tools, fields)
    print(RULE)
    print("lab_tool_schema - turn sweep (saving of a cached schema prefix)")
    print(THIN)
    print(f"{'turns':>6} {'schema tok':>11} {'tokens sent':>12} {'plain USD':>11} "
          f"{'cached USD':>11} {'saving %':>9}")
    for turns in SWEEP_TURNS:
        plain, cached = prefix_cost(schema, turns, price_per_mtok)
        print(f"{turns:>6} {schema:>11,} {schema * turns:>12,} {plain:>11.6f} "
              f"{cached:>11.6f} {100.0 * (plain - cached) / plain:>9.2f}")
    print(THIN)
    print("မှတ်ချက် - cached prefix သည် turn အရေအတွက် တိုးလာသည်နှင့်အမျှ 75 ရာခိုင်နှုန်း "
          "ကန့်သတ်ချက်သို့ ချဉ်းကပ်သည်၊ အကြောင်းမှာ ပထမ ရေးသွင်းမှု၏ အပိုအလွှာသည် "
          "turn အရေအတွက် တိုးလာသည်နှင့်အမျှ ပျောက်ကွယ်သည်။")
    print(RULE)


def self_test() -> int:
    ok = True

    linear_tools = schema_tokens(5, 4) - schema_tokens(4, 4) == TOOL_OVERHEAD_TOKENS + 4 * FIELD_TOKENS
    print(f"[OK] schema tokens grow linearly in tools "
          f"({schema_tokens(4, 4)} -> {schema_tokens(5, 4)}): {linear_tools}")
    ok = ok and linear_tools

    linear_fields = schema_tokens(3, 6) - schema_tokens(3, 5) == 3 * FIELD_TOKENS
    print(f"[OK] schema tokens grow linearly in fields "
          f"({schema_tokens(3, 5)} -> {schema_tokens(3, 6)}): {linear_fields}")
    ok = ok and linear_fields

    one_plain, one_cached = prefix_cost(schema_tokens(3, 4), 1, 3.0)
    five_plain, five_cached = prefix_cost(schema_tokens(3, 4), 5, 3.0)
    save1 = (one_plain - one_cached) / one_plain * 100.0
    save5 = (five_plain - five_cached) / five_plain * 100.0
    print(f"[OK] caching a prefix saves more the longer it is reused "
          f"({save1:.2f}% at 1 turn -> {save5:.2f}% at 5 turns): {save1 < save5}")
    ok = ok and save1 < save5

    long_plain, long_cached = prefix_cost(schema_tokens(3, 4), 400, 3.0)
    save400 = (long_plain - long_cached) / long_plain * 100.0
    ceiling_ok = 60.0 < save400 < 75.0
    print(f"[OK] the saving approaches but never passes the 75% cache-read ceiling "
          f"({save400:.2f}% at 400 turns): {ceiling_ok}")
    ok = ok and ceiling_ok

    verdicts = [validate(raw) for _, raw in SAMPLES]
    verdict_ok = verdicts[0] == (True, "accepted") and all(
        not good for good, _ in verdicts[1:])
    print(f"[OK] the validator accepts the valid sample and rejects all "
          f"{len(SAMPLES) - 1} malformed samples: {verdict_ok}")
    ok = ok and verdict_ok

    reasons = {reason for _, reason in verdicts[1:]}
    distinct = len(reasons) == len(SAMPLES) - 1
    print(f"[OK] every malformed sample carries its own reason "
          f"({len(reasons)} distinct reasons): {distinct}")
    ok = ok and distinct

    dup_ok = validate('{"tool": "read_file", "args": {"path": "/a", "path": "/b"}}') == \
        (False, "duplicate key: path")
    print(f"[OK] a duplicate argument key is caught before execution: {dup_ok}")
    ok = ok and dup_ok

    again = [validate(raw) for _, raw in SAMPLES]
    det = again == verdicts and schema_tokens(3, 4) == 372
    print(f"[OK] validation and schema arithmetic are deterministic: {det}")
    ok = ok and det

    print("[PASS] lab_tool_schema self-test passed." if ok
          else "[FAIL] lab_tool_schema self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Tool schema token overhead, prefix-cache saving, call validation.")
    ap.add_argument("--tools", type=int, default=3, help="number of tools in the schema")
    ap.add_argument("--fields", type=int, default=4, help="fields per tool")
    ap.add_argument("--turns", type=int, default=5, help="model turns in which the schema is sent")
    ap.add_argument("--price-per-mtok", type=float, default=3.0,
                    help="input price in USD per million tokens (assumption)")
    ap.add_argument("--sweep", action="store_true", help="sweep turns 1..16")
    ap.add_argument("--self-test", action="store_true",
                    help="assert the properties this lab teaches")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.tools, args.fields, args.price_per_mtok)
        return 0
    print_report(args.tools, args.fields, args.turns, args.price_per_mtok)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
