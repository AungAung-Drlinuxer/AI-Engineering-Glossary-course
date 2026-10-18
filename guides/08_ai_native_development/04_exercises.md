# ၀၄ — လေ့ကျင့်ခန်းများနှင့် အဖြေများ (AI-native development)

ဤဖိုင်သည် နယ်ပယ် ၀၈ ၏ term ၂၃ ခုကို အသုံးပြု၍ တွက်ချက်ခြင်း၊ ပြဿနာ ရှာဖွေခြင်း နှင့်
ဆုံးဖြတ်ချက် ချခြင်း လေ့ကျင့်ခန်းများကို စုစည်းထားသည်။ အပိုင်း ၁ တွင် အလုပ်လုပ်ပြီး ဖြေသည့်
ဥပမာ ၄ ခု၊ အပိုင်း ၂ တွင် တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ အပိုင်း ၃ တွင် ပြဿနာ ရှာဖွေခြင်း
၃ ခု၊ အပိုင်း ၄ တွင် ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း ၂ ခု ပါဝင်သည်။ အပိုင်း ၅ တွင် အဖြေ တိုင်းကို
ဖော်မြူလာ၊ တွက်ချက်မှု အဆင့်ဆင့် နှင့် အကြောင်းရင်း ရှင်းလင်းချက်နှင့်အတူ ပေးထားသည်။

ဤဖိုင်ရှိ ကိန်းဂဏန်း တိုင်းသည် Python (standard library သာ) ဖြင့် အမှန်တကယ် လုပ်ဆောင်ခဲ့သည့်
တွက်ချက်မှု၏ output ဖြစ်သည်။ ဖော်ပြထားသည့် block အတိုင်း run လုပ်ပါက တူညီသည့် output ကို
ပြန်လည် ရရှိမည်။ ကိန်းဂဏန်း တိုင်းသည် သတ်မှတ်ထားသည့် ယူဆချက် (assumption) အပေါ် မှီခိုသည်၊
ထို့ကြောင့် ဖော်မြူလာ တစ်ခုစီနှင့်အတူ ၎င်း၏ ယူဆချက်ကို ဖော်ပြထားသည်။ ထို ယူဆချက်များ
ပြောင်းလဲပါက ရလဒ်လည်း အချိုးအစား အလိုက် ပြောင်းလဲသည် — ကိန်းဂဏန်း တန်ဖိုးကို မှတ်သည်ထက်
ဖော်မြူလာ နှင့် ယူဆချက် ကို မှတ်ရမည်။

လေ့ကျင့်ခန်းများကို လက်တွေ့ စမ်းသပ်ရန် [`labs/`](labs/) ရှိ `lab_context_strategy.py`၊
`lab_review_budget.py` နှင့် `lab_change_cost.py` တို့ကို အသုံးပြုနိုင်သည်။ ဤဖိုင်၏ တွက်ချက်မှုများသည် ထို lab များအပေါ်
မှီခိုမှု မရှိပါ။

## ၁။ အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာများ (Worked Examples)

### ဥပမာ ၁ — လုပ်ငန်းတစ်ခုအတွက် context စုစည်းမှု နှင့် budget

**ယူဆချက် —** context window 16,000 token၊ system prompt 900 token၊ repository instructions
1,500 token၊ repository map 2,200 token၊ issue သို့မဟုတ် spec 350 token၊ ရွေးထားသည့် ဖိုင် ၆ ခု
(တစ်ခုလျှင် 480 token)၊ test output 1,200 token၊ output အတွက် ချန်ထားသည့်အရာ 3,000 token။
Progressive disclosure ဖြင့် ဖိုင် ၂ ခုသာ အစတွင် load လုပ်သော အခြေအနေကို နှိုင်းယှဉ်သည်။

**ဖော်မြူလာ —**
- used = system + instructions + map + issue + (files × per_file) + test output + reserved output
- headroom = window − used
- saving = used − used_with_scoped_files

**တွက်ချက်မှု —**
1. ရွေးထားသည့် ဖိုင် = 6 × 480 = 2,880 token ဖြစ်သည်။
2. used = 900 + 1,500 + 2,200 + 350 + 2,880 + 1,200 + 3,000 = 12,030 token ဖြစ်သည်၊ window ၏ 75.19 % ဖြစ်သည်။
3. headroom = 16,000 − 12,030 = 3,970 token ဖြစ်သည်။
4. ဖိုင် ၂ ခုသာ load လုပ်ပါက used = 10,110 token ဖြစ်သည်၊ ဆိုလိုသည်မှာ 1,920 token (prompt ၏ 15.96 %) သက်သာသည်။
5. ထို prompt ကို တစ်ကြိမ် ပို့သည့် input ကုန်ကျစရိတ်သည် $3 / သန်း token ဖြင့် $0.036090 ဖြစ်သည်။

**ကောက်ချက် —** reserved output token ကို မနုတ်ပါက budget သည် လုံခြုံသည်ဟု ထင်ရသော်လည်း
အဖြေသည် အလယ်တွင် ပြတ်တောက်သည်။ ဤဥပမာတွင် ဖိုင် အရေအတွက် လျှော့ခြင်းသည် prompt ၏
ခြောက်ပုံ တစ်ပုံခန့် သက်သာစေသည် — progressive disclosure ၏ တန်ဖိုးကို ဤနေရာတွင် တိုင်းသည်။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

window = 16000
system, instructions, rmap, issue, per_file, files = 900, 1500, 2200, 350, 480, 6
tests, reserved = 1200, 3000
used = system + instructions + rmap + issue + per_file * files + tests + reserved
print("window                 ", window)
print("system prompt          ", system)
print("repository instructions", instructions)
print("repository map         ", rmap)
print("issue text             ", issue)
print(f"retrieved files        {per_file * files} ({files} x {per_file})")
print("test output            ", tests)
print("reserved for output    ", reserved)
print("used                   ", used, f"({100 * used / window:.2f}% of window)")
print("headroom               ", window - used)
scoped_files = 2
scoped = system + instructions + rmap + issue + per_file * scoped_files + tests + reserved
print("used when scoped       ", scoped, f"({100 * scoped / window:.2f}% of window)")
print("tokens saved           ", used - scoped, f"({100 * (used - scoped) / used:.2f}% of the prompt)")
print("input cost per task USD", money(used / 1e6 * IN, 6))
```

```text
window                  16000
system prompt           900
repository instructions 1500
repository map          2200
issue text              350
retrieved files        2880 (6 x 480)
test output             1200
reserved for output     3000
used                    12030 (75.19% of window)
headroom                3970
used when scoped        10110 (63.19% of window)
tokens saved            1920 (15.96% of the prompt)
input cost per task USD 0.036090
```

### ဥပမာ ၂ — cost per successful task နှင့် cost per token

**ယူဆချက် —** repository လုပ်ငန်း ၁၀၀ ခုအတွက် provider ခေါ်ဆိုမှု စုစုပေါင်း ၁၃၀ ကြိမ် (retry အပါ)၊
စံချိန်စံညွှန်း ဖြည့်ဆည်းသည့် လုပ်ငန်း ၇၈ ခု၊ တစ်ကြိမ်လျှင် input 12,030 token နှင့် output
2,500 token၊ input $3 / သန်း၊ output $15 / သန်း။ ထို လုပ်ငန်းများအနက် ၂၂ ခုကို လူက ၁၂ မိနစ် စီ
ပြုပြင်ရသည်၊ လူ၏ တန်ဖိုးနှုန်း နာရီ $60။

**ဖော်မြူလာ —**
- cost per attempt = input tokens × price_in + output tokens × price_out
- cost per successful task = (attempts × cost per attempt + human correction cost) ÷ successes

**တွက်ချက်မှု —**
1. တစ်ကြိမ်လျှင် token = 12,030 + 2,500 = 14,530 ဖြစ်သည်။
2. cost per attempt = 12,030 / 10⁶ × 3 + 2,500 / 10⁶ × 15 = 0.036090 + 0.037500 = $0.073590 ဖြစ်သည်။
3. run ကုန်ကျစရိတ် = 130 × 0.073590 = $9.5667 ဖြစ်သည်။
4. cost per successful task သည် လူ၏ ပြုပြင်မှု မပါဘဲ $9.5667 ÷ 78 = $0.122650 ဖြစ်သည်။
5. cost per 1M token = 9.5667 ÷ (130 × 14,530) × 10⁶ = $5.064694 ဖြစ်သည်။
6. လုပ်ငန်း တစ်ခုလျှင် ပျမ်းမျှ ကြိမ်ရေ = 130 ÷ 78 = 1.6667 ဖြစ်သည်။
7. လူ၏ ပြုပြင်မှု = 22 × 12 ÷ 60 = 4.4 နာရီ = $264.00 ဖြစ်သည်။
8. စုစုပေါင်း = 9.5667 + 264.00 = $273.5667 ဖြစ်သည်၊ ထို့ကြောင့် အောင်မြင်သည့် လုပ်ငန်း တစ်ခုလျှင် $3.507265 ဖြစ်သည်၊ လူ၏ ပြုပြင်မှုသည် စုစုပေါင်း၏ 96.50 % ဖြစ်သည်။

**ကောက်ချက် —** provider ကောက်ခံငွေ သာ ကြည့်ပါက လုပ်ငန်း တစ်ခုလျှင် တစ်ဆယ့်နှစ် ဆင့် ခန့်
($0.1227) ဖြစ်သည်၊ လူ၏ အချိန် ထည့်ပါက $3.51 ဖြစ်သည်။ စျေးသက်သာသည့် မော်ဒယ် ခေါ်ဆိုမှုတစ်ခုသည်
မကြာခဏ ကျရှုံးခြင်း သို့မဟုတ် လူဖြင့် ထပ်ခါတလဲလဲ ပြုပြင်ရခြင်း ဖြစ်ပါက ကုန်ကျစရိတ် ကြီးမားသည့်
workflow တစ်ခု ဖြစ်လာနိုင်သည် — ထို့ကြောင့် cost per successful task ကို တိုင်းရမည်။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

tasks, attempts, successes = 100, 130, 78
in_tok, out_tok = 12030, 2500
tokens = in_tok + out_tok
attempt_cost = in_tok / 1e6 * IN + out_tok / 1e6 * OUT
print("tokens per attempt     ", tokens)
print("USD per attempt        ", money(attempt_cost, 6))
run_cost = attempts * attempt_cost
print("run cost USD           ", money(run_cost, 4))
print("cost per successful task USD", money(run_cost / successes, 6))
print("cost per 1M tokens USD ", money(run_cost / (attempts * tokens) * 1e6, 6))
print("attempts per success   ", round(attempts / successes, 4))
human_tasks, human_min, rate = 22, 12.0, 60.0
human_h = human_tasks * human_min / 60
print("human correction hours ", round(human_h, 2))
print("human correction USD   ", money(human_h * rate, 2))
total = run_cost + human_h * rate
print("total cost USD         ", money(total, 4))
print("cost per successful task with human USD", money(total / successes, 6))
print("human share of total   ", f"{100 * human_h * rate / total:.2f}%")
```

```text
tokens per attempt      14530
USD per attempt         0.073590
run cost USD            9.5667
cost per successful task USD 0.122650
cost per 1M tokens USD  5.064694
attempts per success    1.6667
human correction hours  4.4
human correction USD    264.00
total cost USD          273.5667
cost per successful task with human USD 3.507265
human share of total    96.50%
```

### ဥပမာ ၃ — ကျဉ်းသည့် patch နှင့် ကျယ်သည့် refactor ၏ review effort

**ယူဆချက် —** ကျဉ်းသည့် patch တစ်ခုတွင် ပြောင်းလဲသည့် စာကြောင်း ၂၄၀ (အနက် test စာကြောင်း ၈၀)၊
scope contract မပါဘဲ ကျယ်လာသည့် refactor တစ်ခုတွင် ဖိုင် ၄၀ အတွင်း စာကြောင်း ၃,၂၀၀။
လူ၏ ထိရောက်သည့် review နှုန်းသည် နာရီ တစ်နာရီလျှင် စာကြောင်း ၂၅၀၊ လူ၏ တန်ဖိုးနှုန်း နာရီ $60။
reviewer agent တစ်ခုက စာကြောင်း ၆၀ % ကို အန္တရာယ် မရှိဟု ကြိုတင် အမှတ်ပေးပါက လူသည် ကျန် ၄၀ %
ကိုသာ ဖတ်ရသည်၊ agent ကုန်ကျစရိတ် တစ်ကြိမ်လျှင် $0.20။

**ဖော်မြူလာ —**
- review hours = changed lines ÷ review rate
- saving with agent pre-pass = (human hours × rate) − ((remaining lines ÷ review rate) × rate + agent cost)

**တွက်ချက်မှု —**
1. ကျဉ်းသည့် patch = 240 ÷ 250 = 0.96 နာရီ = $57.60 ဖြစ်သည်။
2. refactor = 3,200 ÷ 250 = 12.8 နာရီ = $768.00 ဖြစ်သည်၊ ကျဉ်းသည့် patch ၏ 13.33 ဆ ဖြစ်သည်။
3. reviewer agent pre-pass ပြီးနောက် လူသည် 240 × 0.40 = 96 စာကြောင်း ဖတ်ရသည်၊ ဆိုလိုသည်မှာ 0.384 နာရီ ဖြစ်သည်။
4. ကုန်ကျစရိတ် = 0.384 × 60 + 0.20 = $23.24 ဖြစ်သည်၊ ဆိုလိုသည်မှာ 59.7 % သက်သာသည်။

**ကောက်ချက် —** scope contract တစ်ခု၏ တန်ဖိုးကို ဤနေရာတွင် ကိန်းဂဏန်း အဖြစ် တွက်နိုင်သည် —
ပြောင်းလဲမှု သည် ၂၄၀ မှ ၃,၂၀၀ သို့ တိုးပါက review သည် 0.96 နာရီ မှ 12.8 နာရီ သို့ တိုးသည်။
ထို့ကြောင့် scope contract သည် စာရွက်ပေါ်ရှိ ကန့်သတ်ချက် မဟုတ်ဘဲ review နာရီကို ဝယ်ယူသည့်
ကိရိယာ ဖြစ်သည်။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

scoped_lines, test_share = 240, 80
eff_rate = 250.0           # reviewable lines per hour
human_rate = 60.0
scoped_h = scoped_lines / eff_rate
refactor_lines, refactor_files = 3200, 40
refactor_h = refactor_lines / eff_rate
print("scoped patch lines     ", scoped_lines, f"({test_share} test lines)")
print("scoped review hours    ", round(scoped_h, 3))
print("scoped review USD      ", money(scoped_h * human_rate, 2))
print("refactor changed lines ", refactor_lines, f"across {refactor_files} files")
print("refactor review hours  ", round(refactor_h, 3))
print("refactor review USD    ", money(refactor_h * human_rate, 2))
print("ratio refactor/scoped  ", round(refactor_h / scoped_h, 2))
pre_pass = 0.60
after_h = scoped_lines * (1 - pre_pass) / eff_rate
agent_cost = 0.20
print("reviewer agent cost USD", money(agent_cost, 2))
print("human hours after agent pre-pass", round(after_h, 3))
print("scoped cost with agent pre-pass USD", money(after_h * human_rate + agent_cost, 2))
print("saving vs human only pct", f"{100 * (scoped_h * human_rate - (after_h * human_rate + agent_cost)) / (scoped_h * human_rate):.1f}%")
```

```text
scoped patch lines      240 (80 test lines)
scoped review hours     0.96
scoped review USD       57.60
refactor changed lines  3200 across 40 files
refactor review hours   12.8
refactor review USD     768.00
ratio refactor/scoped   13.33
reviewer agent cost USD 0.20
human hours after agent pre-pass 0.384
scoped cost with agent pre-pass USD 23.24
saving vs human only pct 59.7%
```

### ဥပမာ ၄ — test-after နှင့် test-first ၏ ကွာခြားချက်

**ယူဆချက် —** ပြောင်းလဲမှု ၆၀ ခုကို နည်းလမ်း နှစ်မျိုးဖြင့် လုပ်သည်။ test-after တွင် review က
defect ၁၈ ခု ဖမ်းသည်၊ ၇ ခု production သို့ လွတ်မြောက်သည်။ test-first တွင် ၂၁ ခု ဖမ်းသည်၊
၃ ခု လွတ်မြောက်သည်။ review အဆင့်တွင် ဖမ်းသည့် defect တစ်ခုလျှင် ကုန်ကျစရိတ် $55၊
production သို့ လွတ်မြောက်ပါက $420။

**ဖော်မြူလာ —**
- escape rate = escaped ÷ (found + escaped)
- cost = found × cost_review + escaped × cost_prod

**တွက်ချက်မှု —**
1. test-after ၏ escape rate = 7 ÷ 25 = 28.0 % ဖြစ်သည်၊ ကုန်ကျစရိတ် = 18 × 55 + 7 × 420 = $3,930 ဖြစ်သည်၊ ပြောင်းလဲမှု တစ်ခုလျှင် $65.50 ဖြစ်သည်။
2. test-first ၏ escape rate = 3 ÷ 24 = 12.5 % ဖြစ်သည်၊ ကုန်ကျစရိတ် = 21 × 55 + 3 × 420 = $2,415 ဖြစ်သည်၊ ပြောင်းလဲမှု တစ်ခုလျှင် $40.25 ဖြစ်သည်။
3. escape လျော့နည်းမှု = 57.1 % ဖြစ်သည်၊ ကုန်ကျစရိတ် လျော့နည်းမှု = 38.5 % ဖြစ်သည်။

**ကောက်ချက် —** test-first ၏ အကျိုးအမြတ်သည် test ရေးခြင်း အချိန်မှ မဟုတ်ဘဲ **oracle သည် ကုဒ်နှင့်
မှီခိုမှု မရှိခြင်း** မှ လာသည်။ defect တစ်ခုကို production တွင် ဖမ်းသည့် ကုန်ကျစရိတ်သည်
review အဆင့်တွင် ဖမ်းသည့် ကုန်ကျစရိတ်၏ 7.64 ဆ ဖြစ်သဖြင့် အစောပိုင်း အတည်ပြုမှု တိုင်း၏
တန်ဖိုးသည် အချိုးအစား ကြီးသည်။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

changes = 60
found_after, escaped_after = 18, 7
found_first, escaped_first = 21, 3
cost_review, cost_prod = 55.0, 420.0
tot_after = found_after * cost_review + escaped_after * cost_prod
tot_first = found_first * cost_review + escaped_first * cost_prod
print("changes                ", changes)
print("test-after found       ", found_after, "escaped", escaped_after)
print("test-after escape rate ", f"{100 * escaped_after / (found_after + escaped_after):.1f}%")
print("test-after cost USD    ", money(tot_after, 2), "per change", money(tot_after / changes, 2))
print("test-first found       ", found_first, "escaped", escaped_first)
print("test-first escape rate ", f"{100 * escaped_first / (found_first + escaped_first):.1f}%")
print("test-first cost USD    ", money(tot_first, 2), "per change", money(tot_first / changes, 2))
print("escape reduction pct   ", f"{100 * (escaped_after - escaped_first) / escaped_after:.1f}%")
print("cost reduction pct     ", f"{100 * (tot_after - tot_first) / tot_after:.1f}%")
```

```text
changes                 60
test-after found        18 escaped 7
test-after escape rate  28.0%
test-after cost USD     3930.00 per change 65.50
test-first found        21 escaped 3
test-first escape rate  12.5%
test-first cost USD     2415.00 per change 40.25
escape reduction pct    57.1%
cost reduction pct      38.5%
```

## ၂။ တွက်ချက်ရသည့် လေ့ကျင့်ခန်းများ (Calculation Exercises)

လေ့ကျင့်ခန်း တစ်ခုစီတွင် ကိန်းဂဏန်း အဖြေ အတိအကျ ရှိသည်။ အဖြေ နှင့် ဖော်မြူလာ ရှင်းလင်းချက်ကို
အပိုင်း ၅.၁ တွင် ပေးထားသည်။ ဖော်ပြထားသည့် lab ဖြင့် လက်တွေ့ စစ်ဆေးနိုင်သည်။

**လေ့ကျင့်ခန်း ၁ — repository context budget နှင့် ကုန်ကျစရိတ်**

window 32,000 token၊ system prompt 700၊ repository instructions 1,800၊ repository map 2,600၊
task ဖော်ပြချက် 400၊ ရွေးထားသည့် ဖိုင် ၁၀ ခု (တစ်ခုလျှင် 520)၊ history 6,000၊ output အတွက်
ချန်ထားသည့်အရာ 4,096။ input $3 / သန်း၊ output $15 / သန်း။
(က) used နှင့် headroom၊ (ခ) window ၏ မည်မျှ ရာခိုင်နှုန်း ဖြစ်သည်၊ (ဂ) request တစ်ခုလျှင် နှင့်
request ၁,၀၀၀ လျှင် USD၊ (ဃ) ဖိုင်ကို ၆ ခုသို့ လျှော့ပါက သက်သာသည့် token။ → `labs/lab_context_strategy.py`

**လေ့ကျင့်ခန်း ၂ — review အချိန် နှင့် ထုတ်လုပ်သည့် စာကြောင်း**

ထုတ်လုပ်သည့် စာကြောင်း 1,800၊ အနက် ၄၅ % သည် generated သို့မဟုတ် vendored ဖိုင်များ ဖြစ်သဖြင့်
လိုင်းချင်း ဖတ်ရန် မလိုပါ၊ hunk ၄၂ ခု၊ hunk တစ်ခုလျှင် 1.5 မိနစ် ကြိုတင် နားလည်ရန် ကြာသည်၊
လိုင်း ဖတ်နှုန်း နာရီ တစ်နာရီလျှင် 300 စာကြောင်း၊ လူ၏ တန်ဖိုးနှုန်း နာရီ $75၊ reviewer agent
pre-pass သည် လိုင်း ၄၅ % ကိုသာ လူ ဖတ်ရန် ချန်ထားသည်၊ agent ကုန်ကျစရိတ် $0.35။
(က) လိုင်းချင်း ဖတ်ရမည့် စာကြောင်း အရေအတွက်၊ (ခ) လိုင်း ဖတ်သည့် နာရီ၊ (ဂ) hunk overhead နာရီ၊
(ဃ) စုစုပေါင်း နာရီ နှင့် USD၊ (င) agent pre-pass ပြီးနောက် နာရီ၊ USD နှင့် သက်သာသည့် နာရီ။
→ `labs/lab_review_budget.py`

**လေ့ကျင့်ခန်း ၃ — defect escape rate**

ပြောင်းလဲမှု ၂၀၀ ခုတွင် defect ၁၄၀ ခု ဝင်သည်။ ပထမ အခြေအနေတွင် review က ၁၁၂ ခု ဖမ်းသည်၊
၂၈ ခု လွတ်မြောက်သည်။ verification gate အသစ် ထည့်ပြီးနောက် ၁၂၆ ခု ဖမ်းသည်၊ ၁၄ ခု လွတ်မြောက်သည်။
review အဆင့် ဖမ်းသည့် defect တစ်ခုလျှင် $60၊ production လွတ်မြောက်ပါက $500။
(က) escape rate နှစ်မျိုး နှင့် review catch rate၊ (ခ) အခြေအနေ တစ်ခုစီ၏ စုစုပေါင်း USD နှင့်
ပြောင်းလဲမှု တစ်ခုလျှင် USD၊ (ဂ) escape လျော့နည်းမှု % နှင့် ကုန်ကျစရိတ် လျော့နည်းမှု %၊
(ဃ) တားဆီးလိုက်သည့် လွတ်မြောက် defect တစ်ခုလျှင် သက်သာသည့် USD။ → `labs/lab_review_budget.py`

**လေ့ကျင့်ခန်း ၄ — merged change တစ်ခုလျှင် ကုန်ကျစရိတ်**

ပြောင်းလဲမှု ၁၈၀ ခုအတွက် agent ကြိုးစားမှု ၂၅၀ ကြိမ်၊ merge ဖြစ်သည် ၁၅၀ ခု၊ ကြိုးစားမှု တစ်ကြိမ်လျှင်
$0.084၊ အခြေခံအဆောက်အအုံ $40၊ လူသည် ပြောင်းလဲမှု တစ်ခုလျှင် ၂၂ မိနစ် review လုပ်သည်၊
လူ၏ တန်ဖိုးနှုန်း နာရီ $75။
(က) run ကုန်ကျစရိတ်၊ (ခ) လူ၏ review နာရီ နှင့် USD၊ (ဂ) ပယ်ချခံရသည့် အချိုး၊ (ဃ) စုစုပေါင်း နှင့်
merged change တစ်ခုလျှင် USD၊ (င) လူ၏ အချိန် မပါဘဲ machine-only USD၊ (စ) စုစုပေါင်းတွင် လူ၏ ရှယ် %။
→ `labs/lab_change_cost.py`

**လေ့ကျင့်ခန်း ၅ — repository တစ်ခုလုံး မဝင်သည့်အခါ context overflow**

repository တွင် token 480,000 ရှိသည်၊ ဖိုင် ၁၆၀၊ ပျမ်းမျှ ဖိုင် တစ်ခုလျှင် 3,000 token၊
window 128,000။ scoped context တွင် repository map 2,600 နှင့် သက်ဆိုင်သည့် ဖိုင် ၈ ခုသာ ထည့်သည်။
(က) repository / window အချိုး၊ overflow token နှင့် window ၏ %၊ (ခ) unscoped အနေဖြင့် ဝင်နိုင်သည့်
ဖိုင် အရေအတွက် နှင့် repository ၏ %၊ (ဂ) scoped token၊ window ၏ % နှင့် repository ၏ %၊
(ဃ) scoped input USD ကို request တစ်ခုလျှင် နှင့် ၁,၀၀၀ လျှင်။ → `labs/lab_context_strategy.py`

**လေ့ကျင့်ခန်း ၆ — scope ကျဉ်းသည့် context ၏ saving**

naive လုပ်နည်းတွင် task တစ်ခုလျှင် prompt token 128,000 ပို့သည်၊ scope ကျဉ်းသည့် လုပ်နည်းတွင် 22,000။
task ၁,၀၀၀၊ input $3 / သန်း၊ prefill သည် window ၏ token ၁,၀၀၀ လျှင် 12 ms ကြာသည်။
(က) token အချိုး၊ (ခ) USD ကို task တစ်ခုလျှင် နှစ်မျိုး၊ (ဂ) task ၁,၀၀၀ လျှင် USD နှစ်မျိုး နှင့် သက်သာငွေ၊
(ဃ) saving %၊ (င) prefill ms နှစ်မျိုး နှင့် သက်သာသည့် ms။ → `labs/lab_context_strategy.py`

## ၃။ ပြဿနာ ရှာဖွေခြင်း (Troubleshooting Scenarios)

ပြဿနာ တစ်ခုစီကို symptom၊ တိုင်းတာရမည့် အချက်၊ ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်)၊
ဖြေရှင်းနည်း နှင့် ရှင်းလင်းသည့် term ဟူသည့် အစဉ်အတိုင်း ဖော်ပြထားသည်။ အကြောင်းရင်း အစဉ်သည်
တိုင်းတာမှုဖြင့် ရှာဖွေနိုင်သည့် အစဉ်အတိုင်း ဖြစ်သည်။ အသေးစိတ် ရှင်းလင်းချက်ကို အပိုင်း ၅.၂ တွင်
ပေးထားသည်။

### ပြဿနာ ၁ — agent သည် လုပ်ငန်းနှင့် မသက်ဆိုင်သည့် ဖိုင်များကို တည်းဖြတ်သည်

- **Symptom —** scope contract တွင် parser module နှင့် ၎င်း၏ test များသာ ပါသော်လည်း patch သည်
  configuration၊ documentation နှင့် အခြား module များကို ပါ ထိသည်။ review တွင် ဖိုင် စာရင်း
  ကျယ်လာသည့်အတွက် စာကြောင်း ၂၄၀ အစား ၃,၂၀၀ ဖတ်ရသည်။
- **တိုင်းတာရမည့် အချက် —** patch ထိသည့် ဖိုင် စာရင်း နှင့် scope contract ၏ ခွင့်ပြုထားသည့်
  ဖိုင် စာရင်း တိုက်စစ်ခြင်း၊ ပြောင်းလဲသည့် စာကြောင်း အရေအတွက်၊ ပြုပြင်သည့် public API အရေအတွက်၊
  ထို ဖိုင်များသို့ ရောက်သည့် လမ်းကြောင်း (repository map တွင် ဖော်ပြထားသလား)။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) repository instructions တွင် generated ဖိုင်၊
  configuration နှင့် မထိရမည့် directory များကို ဖော်ပြမထားခြင်း၊ (၂) scope contract တွင်
  တားမြစ်ထားသည့် မျက်နှာပြင်ကို စာရင်း အနေဖြင့် မသတ်မှတ်ထားခြင်း၊ (၃) agent သည် repository map
  မပါဘဲ မှားသည့် subsystem ကို ရှာတွေ့ခြင်း၊ (၄) patch ကို review မလုပ်မီ merge လုပ်ခြင်း။
- **ဖြေရှင်းနည်း —** scope contract တွင် ခွင့်ပြုထားသည့် path ကို အတိအကျ ရေးရမည်၊ တားမြစ်သည့်
  ဖိုင်များကို repository instructions တွင် ဖော်ပြရမည်၊ patch တွင် ထိသည့် ဖိုင် စာရင်းကို ပြရမည်၊
  diff review ကို ဖိုင် စာရင်း စစ်ခြင်းမှ စတင်ရမည်။
- **ရှင်းလင်းသည့် term —** Scope Contract၊ Repository Instructions၊ Repository Map၊ Patch၊ Reviewer Agent။

### ပြဿနာ ၂ — ဒေသတွင် test အောင်သည်၊ CI တွင် ကျရှုံးသည်

- **Symptom —** မိမိ စက်တွင် test command run ပါက အောင်သည်၊ CI တွင် တူညီသည့် commit က
  ကျရှုံးသည်။ တစ်ခါတစ်ရံ ကျရှုံးသည့် test သည် CI တွင် run တိုင်း မကျရှုံးပါ။
- **တိုင်းတာရမည့် အချက် —** ကျရှုံးသည့် test အမည် နှင့် seed၊ ဒေသ နှင့် CI ၏ toolchain
  ဗားရှင်း၊ dependency lock ဖိုင် နှင့် ကွာခြားမှု၊ timezone၊ locale နှင့် အချိန် မှီခိုမှု၊ test
  အစဉ်၊ တစ်ပြိုင်နက် run သည့် test အရေအတွက်၊ network မှီခိုမှု၊ ပြောင်းလဲထားသည့် ဖိုင် စာရင်း။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) ဒေသ နှင့် CI တွင် dependency ဗားရှင်း မတူခြင်း၊
  ဆိုလိုသည်မှာ build သည် ပြန်လည် ထုတ်လုပ်နိုင်မှု မရှိခြင်း၊ (၂) test သည် အချိန်၊ locale၊ အစဉ်
  သို့မဟုတ် shared state အပေါ် မှီခိုခြင်း၊ ဆိုလိုသည်မှာ flaky test ဖြစ်ခြင်း၊ (၃) ဒေသတွင် run သည့်
  test အစုနှင့် CI တွင် run သည့် အစု မတူခြင်း၊ (၄) CI သည် environment variable သို့မဟုတ် secret
  မပါဘဲ run ခြင်း။
- **ဖြေရှင်းနည်း —** ကျရှုံးသည့် seed နှင့် ပတ်ဝန်းကျင်ကို ထိန်းသိမ်းထားရမည်၊ toolchain နှင့်
  dependency ကို pin လုပ်ရမည်၊ ထိန်းချုပ်မထားသည့် အချိန်၊ concurrency၊ network၊ အစဉ်လိုက်မှု
  မှီခိုမှုများကို ပြုပြင်ရမည်၊ quarantine လုပ်မည်ဆိုပါက ပိုင်ရှင် နှင့် သတ်မှတ်ရက် ပါရမည်။
- **ရှင်းလင်းသည့် term —** Reproducible Build၊ Flaky Test၊ Regression Test၊ Repository Instructions၊ Verification Gate။

### ပြဿနာ ၃ — တူညီသည့် prompt သည် နောက်တစ်နေ့တွင် မတူညီသည့် ရလဒ် ပေးသည်

- **Symptom —** တူညီသည့် prompt၊ တူညီသည့် repository commit ဖြင့် ခေါ်ဆိုသော်လည်း
  ရလဒ်သည် အရည်အသွေး ကွာခြားသည်၊ တစ်ခါတစ်ရံ မှားသည်။ code review ၏ ကျရှုံးမှုနှုန်းသည်
  တစ်နေ့နှင့် တစ်နေ့ မတူပါ။
- **တိုင်းတာရမည့် အချက် —** အသုံးပြုသည့် မော်ဒယ် နှင့် provider၊ model version နှင့်
  serving configuration၊ temperature နှင့် sampling parameter၊ prompt version နှင့် hash၊
  retrieved context ၏ ပါဝင်မှု၊ cache hit rate၊ trace တွင် tool call အစဉ်။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) model router သည် တူညီသည့် request ကို
  မတူညီသည့် မော်ဒယ် သို့မဟုတ် provider သို့ ပို့ခြင်း၊ (၂) sampling parameter မပြောင်းလဲဘဲ
  မှတ်တမ်းတင်မထားခြင်း၊ (၃) semantic cache သည် ရည်ရွယ်ချက် မတူသည့် request ကို
  ကိုက်ညီသည်ဟု ဆုံးဖြတ်ပြီး ယခင် ရလဒ်ကို ပြန်ပေးခြင်း၊ (၄) prompt သို့မဟုတ် retrieved
  context ပြောင်းလဲခြင်းကို version မတင်ခြင်း။
- **ဖြေရှင်းနည်း —** request တိုင်းတွင် မော်ဒယ်၊ provider၊ prompt version နှင့် sampling
  parameter ကို trace တွင် မှတ်တမ်းတင်ရမည်၊ routing policy ကို အစဉ်လိုက် မှတ်တမ်းတင်ရမည်၊
  cache key တွင် tenant နှင့် policy version ထည့်ရမည်၊ ရလဒ် ကွာခြားမှုကို regression test
  သို့မဟုတ် eval case အဖြစ် ပြောင်းရမည်။
- **ရှင်းလင်းသည့် term —** Model Router၊ Observability၊ Trace၊ Semantic Cache၊ Test Oracle။

## ၄။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်းများ (Design Decisions)

### ဆုံးဖြတ်ချက် ၁ — window တစ်ခုလုံး ထည့်ခြင်း နှင့် scope ကျဉ်းသည့် context

**အခြေအနေ —** repository ပြုပြင်သည့် agent တစ်ခုကို task ၁,၀၀၀ လုပ်ခိုင်းမည်။ ရွေးချယ်စရာ နှစ်ခု ရှိသည် —
ရွေးချယ်မှု A သည် 128,000 token window ကို အပြည့် အသုံးပြု၍ repository အကြောင်းအရာ အားလုံး
(သို့မဟုတ် တတ်နိုင်သမျှ) ပို့သည်၊ ရွေးချယ်မှု B သည် repository map နှင့် သက်ဆိုင်သည့် ဖိုင်များဖြင့်
22,000 token သာ ပို့သည်။ output token 1,200၊ input $3 / သန်း၊ output $15 / သန်း၊ prefill သည်
token ၁,၀၀၀ လျှင် 14 ms။ A တွင် context ဆူညံမှုကြောင့် ပထမ ကြိုးစားမှု ကျရှုံးနှုန်း 18 %၊ B တွင် 7 %၊
ကြိုးစားမှု တစ်ခုလျှင် ထပ်ဆောင်း ကုန်ကျစရိတ် $0.31။

**trade-off —** A သည် အချက်အလက် ပိုပြီး တွေ့မြင်နိုင်သည်၊ သို့သော် token ကုန်ကျစရိတ်၊ prefill
အချိန် နှင့် ကျရှုံးနှုန်း သုံးခုစလုံး မြင့်သည်။ B သည် ကုန်ကျစရိတ် နှင့် အချိန် လျှော့သည်၊
သို့သော် map နှင့် progressive disclosure မှန်ကန်ရန် လိုသည်။

**တိုင်းတာမည့် metric —** task ၁,၀၀၀ လျှင် USD၊ TTFT၊ context recall (သက်ဆိုင်သည့် အထောက်အထား
ပါဝင်မှု)၊ ပထမ ကြိုးစားမှု အောင်နှုန်း။

### ဆုံးဖြတ်ချက် ၂ — ခေတ္တ ပျက်ကွက်သည့် tool အတွက် retry အရေအတွက် နှင့် idempotency

**အခြေအနေ —** agent တစ်ခုက repository ပြင်ပ system တစ်ခုသို့ ရေးသားသည့် tool ကို ခေါ်သည်။
ခေါ်ဆိုမှု တိုင်း၏ ၈ % သည် ခေတ္တ ပျက်ကွက်သည်၊ များသောအားဖြင့် response သည် မသေချာသည့်
အခြေအနေတွင် ပြတ်သည်။ ခေါ်ဆိုမှု တစ်ကြိမ်လျှင် $0.084၊ retry ကို ၃ ကြိမ် အထိ ခွင့်ပြုနိုင်သည်။
မသေချာသည့် ခေါ်ဆိုမှုများတွင် မူလ ရေးသားမှု တကယ် အောင်မြင်ခဲ့သည့် အခန်းကဏ္ဍ ၅၀ % ရှိသည်။
ထပ်နှစ်ဆ ဖြစ်သည့် ရေးသားမှု တစ်ခုကို လက်ဖြင့် ပြန်ဖျက်ရန် $250။

**trade-off —** idempotency key မပါဘဲ retry လုပ်ပါက ကုန်ကျစရိတ် နည်းသော်လည်း ထပ်နှစ်ဆ
ဖြစ်မှုကို သည်ပိုးရသည်။ idempotency key နှင့် ပြီးစီးသည့် ရလဒ်ကို မှတ်တမ်းတင်ခြင်းသည်
ကုန်ကျစရိတ် အနည်းငယ် တိုးသော်လည်း ထပ်နှစ်ဆ ဖြစ်မှုကို ဖယ်ရှားသည်။

**တိုင်းတာမည့် metric —** task ၁,၀၀၀ လျှင် ထပ်နှစ်ဆ ဖြစ်မှု အရေအတွက်၊ retry ကြောင့် ဖြစ်သည့်
ထပ်ဆောင်း ကုန်ကျစရိတ်၊ လက်ဖြင့် ပြန်ဖျက်ရသည့် USD။

## ၅။ အဖြေများ (Answers with Explanations)

### ၅.၁ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း အဖြေများ

#### အဖြေ ၁ — repository context budget နှင့် ကုန်ကျစရိတ်

**ဖော်မြူလာ —** used = ပုံသေ အပိုင်းများ + (ဖိုင် အရေအတွက် × ဖိုင် တစ်ခုလျှင် token)။
request ကုန်ကျစရိတ် = input token × price_in + reserved output token × price_out။
ယူဆချက် — ပုံသေ အပိုင်း = system 700 + instructions 1,800 + map 2,600 + task 400 + history 6,000
= 11,500 token၊ ဖိုင် တစ်ခုလျှင် 520 token၊ reserved output 4,096 token ကို output အတွက် အမှန်
သုံးစွဲသည်ဟု ယူသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. ရွေးထားသည့် ဖိုင် = 10 × 520 = 5,200 token ဖြစ်သည်။
2. used = 11,500 + 5,200 + 4,096 = 20,796 token ဖြစ်သည်။
3. headroom = 32,000 − 20,796 = 11,204 token ဖြစ်သည်၊ used သည် window ၏ 64.99 % ဖြစ်သည်။
4. request ကုန်ကျစရိတ် = 20,796 / 10⁶ × 3 + 4,096 / 10⁶ × 15 = 0.062388 + 0.061440 = $0.123828 ဖြစ်သည်။
5. request ၁,၀၀၀ လျှင် = $123.828 ဖြစ်သည်။
6. ဖိုင်ကို ၆ ခုသို့ လျှော့ပါက 4 × 520 = 2,080 token သက်သာသည်။

**အဓိပ္ပာယ် —** reserved output 4,096 token သည် request ကုန်ကျစရိတ်၏ ထက်ဝက် နီးပါး
(0.061440 / 0.123828 = 49.6 %) ဖြစ်သည်။ ထို့ကြောင့် budget ကို တွက်သည့်အခါ output အတွက်
နေရာ ကို မဖြစ်မနေ ထည့်ရမည် — ၎င်းသည် အလွတ် နေရာ မဟုတ်ဘဲ အမှန် ကုန်ကျသည့် token ဖြစ်သည်။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

window = 32000
system, instructions, rmap, task, per_file, files = 700, 1800, 2600, 400, 520, 10
history, reserved = 6000, 4096
used = system + instructions + rmap + task + per_file * files + history + reserved
print("window                 ", window)
print("fixed parts            ", system + instructions + rmap + task + history)
print(f"retrieved files        {per_file * files} ({files} x {per_file})")
print("reserved for output    ", reserved)
print("used                   ", used)
print("headroom               ", window - used)
print("used share of window   ", f"{100 * used / window:.2f}%")
req_cost = used / 1e6 * IN + reserved / 1e6 * OUT
print("USD per request        ", money(req_cost, 6))
print("USD per 1000 requests  ", money(req_cost * 1000, 3))
print("files reduced to 6, tokens freed", per_file * (files - 6))
```

```text
window                  32000
fixed parts             11500
retrieved files        5200 (10 x 520)
reserved for output     4096
used                    20796
headroom                11204
used share of window    64.99%
USD per request         0.123828
USD per 1000 requests   123.828
files reduced to 6, tokens freed 2080
```

#### အဖြေ ၂ — review အချိန် နှင့် ထုတ်လုပ်သည့် စာကြောင်း

**ဖော်မြူလာ —** လိုင်းချင်း ဖတ်ရမည့် စာကြောင်း = ထုတ်လုပ်သည့် စာကြောင်း × (1 − generated share)။
နာရီ = စာကြောင်း ÷ ဖတ်နှုန်း + hunk အရေအတွက် × hunk တစ်ခုလျှင် ကြာချိန်။
ယူဆချက် — generated/vendored share 45 %၊ ဖတ်နှုန်း နာရီ တစ်နာရီလျှင် 300 စာကြောင်း၊
hunk ၄၂ ခု၊ hunk တစ်ခုလျှင် 1.5 မိနစ်၊ လူ၏ တန်ဖိုးနှုန်း နာရီ $75။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. လိုင်းချင်း ဖတ်ရမည့် စာကြောင်း = 1,800 × 0.55 = 990.0 ဖြစ်သည်။
2. လိုင်း ဖတ်သည့် နာရီ = 990 ÷ 300 = 3.3 နာရီ ဖြစ်သည်။
3. hunk overhead = 42 × 1.5 = 63 မိနစ် = 1.05 နာရီ ဖြစ်သည်။
4. စုစုပေါင်း = 3.3 + 1.05 = 4.35 နာရီ = $326.25 ဖြစ်သည်။
5. reviewer agent pre-pass ပြီးနောက် = 990 × 0.45 ÷ 300 + 1.05 = 2.535 နာရီ ဖြစ်သည်၊ $190.47 ဖြစ်သည်။
6. သက်သာသည့် အချိန် = 4.35 − 2.535 = 1.815 နာရီ ဖြစ်သည်။

**အဓိပ္ပာယ် —** hunk overhead (1.05 နာရီ) သည် လိုင်း ဖတ်သည့် အချိန်၏ သုံးပုံ တစ်ပုံ နီးပါး
ဖြစ်သည်။ ထို့ကြောင့် patch သည် စာကြောင်း အနည်းငယ်သာ ပြောင်းသော်လည်း hunk များစွာ ဖြန့်နေပါက
review စျေးကြီးသည် — scope contract တွင် "ဖိုင်တစ်ခုတည်း၊ hunk အနည်းဆုံး" ဟု သတ်မှတ်ခြင်းသည်
ဤ ကိန်းဂဏန်း နှစ်ခုကို တိုက်ရိုက် ထိသည်။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

gen_lines, generated_share = 1800, 0.45
eff_lines = gen_lines * (1 - generated_share)
rate = 300.0
hunks, per_hunk_min = 42, 1.5
line_h = eff_lines / rate
hunk_h = hunks * per_hunk_min / 60
human_rate = 75.0
print("generated lines        ", gen_lines)
print("generated/vendored share", f"{100 * generated_share:.0f}%")
print("lines needing eye review", round(eff_lines, 1))
print("line review hours      ", round(line_h, 3))
print("hunks                  ", hunks, f"at {per_hunk_min} min ->", round(hunk_h, 3), "hours")
print("total review hours     ", round(line_h + hunk_h, 3))
print("review USD             ", money((line_h + hunk_h) * human_rate, 2))
kept = 0.45
h2 = eff_lines * kept / rate + hunk_h
print("after agent pre-pass hours", round(h2, 3))
print("after agent pre-pass USD  ", money(h2 * human_rate + 0.35, 2))
print("hours saved            ", round(line_h + hunk_h - h2, 3))
```

```text
generated lines         1800
generated/vendored share 45%
lines needing eye review 990.0
line review hours       3.3
hunks                   42 at 1.5 min -> 1.05 hours
total review hours      4.35
review USD              326.25
after agent pre-pass hours 2.535
after agent pre-pass USD   190.47
hours saved             1.815
```

#### အဖြေ ၃ — defect escape rate

**ဖော်မြူလာ —** escape rate = escaped ÷ (found + escaped)၊ review catch rate = found ÷ introduced။
ကုန်ကျစရိတ် = found × cost_review + escaped × cost_prod။
ယူဆချက် — defect ၁၄၀ ခု ဝင်သည်၊ verification gate အသစ်သည် defect အသစ် မထုတ်ဘဲ
ဖမ်းနိုင်မှုကိုသာ တိုးစေသည်ဟု ယူသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. escape rate = 28 ÷ 140 = 20.0 % ဖြစ်သည်၊ catch rate = 112 ÷ 140 = 80.0 % ဖြစ်သည်။
2. ကုန်ကျစရိတ် = 112 × 60 + 28 × 500 = 6,720 + 14,000 = $20,720 ဖြစ်သည်၊ ပြောင်းလဲမှု တစ်ခုလျှင် $103.60 ဖြစ်သည်။
3. gate အသစ် ပြီးနောက် escape rate = 14 ÷ 140 = 10.0 % ဖြစ်သည်၊ ကုန်ကျစရိတ် = 7,560 + 7,000 = $14,560၊ ပြောင်းလဲမှု တစ်ခုလျှင် $72.80 ဖြစ်သည်။
4. escape လျော့နည်းမှု = 50.0 % ဖြစ်သည်၊ ကုန်ကျစရိတ် လျော့နည်းမှု = 29.7 % ဖြစ်သည်။
5. တားဆီးလိုက်သည့် လွတ်မြောက် defect တစ်ခုလျှင် သက်သာငွေ = 6,160 ÷ 14 = $440.00 ဖြစ်သည်။

**အဓိပ္ပာယ် —** escape rate သည် ထက်ဝက် လျော့သော်လည်း ကုန်ကျစရိတ်သည် 29.7 % သာ လျော့သည်၊
အကြောင်းမှာ review အဆင့် ဖမ်းသည့် defect အရေအတွက် တိုးလာသဖြင့် ဖမ်းသည့် ကုန်ကျစရိတ်လည်း
တိုးသည်။ ထို့ကြောင့် verification gate တစ်ခု၏ တန်ဖိုးကို escape rate တစ်ခုတည်းဖြင့် မတိုင်းရ —
ဖမ်းသည့် ကုန်ကျစရိတ် နှင့် လွတ်မြောက်သည့် ကုန်ကျစရိတ် နှစ်ခုလုံးကို တိုင်းရမည်။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

changes, introduced = 200, 140
found_b, escaped_b = 112, 28
found_a, escaped_a = 126, 14
cr, cp = 60.0, 500.0
print("changes                ", changes, "defects introduced", introduced)
print("before: found", found_b, "escaped", escaped_b)
print("before escape rate     ", f"{100 * escaped_b / introduced:.1f}%")
print("before review catch    ", f"{100 * found_b / introduced:.1f}%")
cost_b = found_b * cr + escaped_b * cp
print("before cost USD        ", money(cost_b, 2), "per change", money(cost_b / changes, 2))
print("after: found", found_a, "escaped", escaped_a)
print("after escape rate      ", f"{100 * escaped_a / introduced:.1f}%")
cost_a = found_a * cr + escaped_a * cp
print("after cost USD         ", money(cost_a, 2), "per change", money(cost_a / changes, 2))
print("escape reduction pct   ", f"{100 * (escaped_b - escaped_a) / escaped_b:.1f}%")
print("cost reduction pct     ", f"{100 * (cost_b - cost_a) / cost_b:.1f}%")
print("cost per escaped defect avoided USD", money((cost_b - cost_a) / (escaped_b - escaped_a), 2))
```

```text
changes                 200 defects introduced 140
before: found 112 escaped 28
before escape rate      20.0%
before review catch     80.0%
before cost USD         20720.00 per change 103.60
after: found 126 escaped 14
after escape rate       10.0%
after cost USD          14560.00 per change 72.80
escape reduction pct    50.0%
cost reduction pct      29.7%
cost per escaped defect avoided USD 440.00
```

#### အဖြေ ၄ — merged change တစ်ခုလျှင် ကုန်ကျစရိတ်

**ဖော်မြူလာ —** run ကုန်ကျစရိတ် = ကြိုးစားမှု အရေအတွက် × ကြိုးစားမှု တစ်ခုလျှင် USD။
လူ၏ ကုန်ကျစရိတ် = ပြောင်းလဲမှု အရေအတွက် × မိနစ် ÷ 60 × နာရီနှုန်း။
cost per merged change = (run + အခြေခံအဆောက်အအုံ + လူ၏ ကုန်ကျစရိတ်) ÷ merge ဖြစ်သည့် အရေအတွက်။
ယူဆချက် — လူသည် ပြောင်းလဲမှု တိုင်းကို review လုပ်သည် (merge ဖြစ်သည် သို့မဟုတ် မဖြစ်သည်)။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. run = 250 × 0.084 = $21.00 ဖြစ်သည်။
2. အခြေခံအဆောက်အအုံ = $40.00 ဖြစ်သည်။
3. လူ၏ review = 180 × 22 ÷ 60 = 66.0 နာရီ = $4,950.00 ဖြစ်သည်။
4. ပယ်ချခံရသည့် အချိုး = 30 ÷ 180 = 16.7 % ဖြစ်သည်။
5. စုစုပေါင်း = 21.00 + 40.00 + 4,950.00 = $5,011.00 ဖြစ်သည်၊ merged change တစ်ခုလျှင် $33.4067 ဖြစ်သည်။
6. လူ၏ အချိန် မပါဘဲ = (21.00 + 40.00) ÷ 150 = $0.4067 ဖြစ်သည်၊ ဆိုလိုသည်မှာ လူသည် စုစုပေါင်း၏ 98.78 % ဖြစ်သည်။

**အဓိပ္ပာယ် —** merged change တစ်ခုလျှင် machine-only ကုန်ကျစရိတ်သည် ဆယ့်လေး ဆင့် ခန့်
($0.4067) ဖြစ်သည်၊ လူ၏ review ထည့်ပါက $33.41 ဖြစ်သည်။ ထို့ကြောင့် "agent ကုန်ကျစရိတ်" ကို
လျှော့ခြင်းသည် စုစုပေါင်း အပေါ် သက်ရောက်မှု နည်းသည် — review အချိန်ကို လျှော့သည့်
 scope contract နှင့် test အရည်အသွေးသည် အကျိုးသက်ရောက်မှု ပိုကြီးသည်။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

changes, attempts, merged = 180, 250, 150
attempt_cost = 0.084
infra = 40.0
review_min, human_rate = 22.0, 75.0
run = attempts * attempt_cost
human_h = changes * review_min / 60
human = human_h * human_rate
total = run + infra + human
print("changes", changes, "attempts", attempts, "merged", merged)
print("USD per attempt        ", money(attempt_cost, 4))
print("run cost USD           ", money(run, 2))
print("infrastructure USD     ", money(infra, 2))
print("human review hours     ", round(human_h, 2), "USD", money(human, 2))
print("rejected share         ", f"{100 * (changes - merged) / changes:.1f}%")
print("total USD              ", money(total, 2))
print("cost per merged change USD", money(total / merged, 4))
print("machine-only per merged USD", money((run + infra) / merged, 4))
print("human share of total   ", f"{100 * human / total:.2f}%")
```

```text
changes 180 attempts 250 merged 150
USD per attempt         0.0840
run cost USD            21.00
infrastructure USD      40.00
human review hours      66.0 USD 4950.00
rejected share          16.7%
total USD               5011.00
cost per merged change USD 33.4067
machine-only per merged USD 0.4067
human share of total    98.78%
```

#### အဖြေ ၅ — repository တစ်ခုလုံး မဝင်သည့်အခါ context overflow

**ဖော်မြူလာ —** overflow = repo token − window။ ဝင်နိုင်သည့် ဖိုင် = window ÷ ပျမ်းမျှ ဖိုင် token။
scoped = map + (သက်ဆိုင်သည့် ဖိုင် × ပျမ်းမျှ ဖိုင် token)။
ယူဆချက် — ဖိုင် တိုင်း၏ အရှည် တူညီသည်၊ output အတွက် နေရာ ချန်ထားခြင်းကို ဤနေရာတွင်
မထည့်သွင်းပါ (ထို့ကြောင့် အမှန် ဝင်နိုင်သည့် ဖိုင် အရေအတွက်သည် ဤ ကိန်းဂဏန်းထက် နည်းသည်)။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. repo ÷ window = 480,000 ÷ 128,000 = 3.75 ဆ ဖြစ်သည်။
2. overflow = 480,000 − 128,000 = 352,000 token ဖြစ်သည်၊ window ၏ 275 % ဖြစ်သည်။
3. window အတွင်း ဝင်နိုင်သည့် ဖိုင် = 128,000 ÷ 3,000 = 42.67 ဖြစ်သည်၊ ဆိုလိုသည်မှာ ဖိုင် ၄၂ ခု၊ repository ၏ 26.25 % ဖြစ်သည်။
4. scoped = 2,600 + 8 × 3,000 = 26,600 token ဖြစ်သည်၊ window ၏ 20.78 %၊ repository ၏ 5.54 % ဖြစ်သည်။
5. scoped input = 26,600 / 10⁶ × $3 = $0.0798 ဖြစ်သည်၊ ၁,၀၀၀ လျှင် $79.80 ဖြစ်သည်။

**အဓိပ္ပာယ် —** repository တစ်ခုလုံးကို ပို့ခြင်းသည် window ကြောင့် မဖြစ်နိုင်ရုံသာမက
လုပ်နိုင်ပါကလည်း မှားသည့် လုပ်နည်း ဖြစ်သည် — ဖိုင် ၄၂ ခုသာ ဝင်သဖြင့် ကျန် ၁၁၈ ခု မပါဘဲ
အချက်အလက် မပြည့်စုံသည့် context တစ်ခု ဖြစ်လာသည်။ ထို့ကြောင့် repository map နှင့်
progressive disclosure သည် ရွေးချယ်မှု မဟုတ်ဘဲ လိုအပ်ချက် ဖြစ်သည်။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

repo_tokens, repo_files, avg_file = 480000, 160, 3000
window = 128000
print("repo tokens            ", repo_tokens, f"across {repo_files} files")
print("average file tokens    ", avg_file)
print("window                 ", window)
print("repo / window          ", round(repo_tokens / window, 3), "x")
print("overflow tokens        ", repo_tokens - window, f"({100 * (repo_tokens - window) / window:.0f}% of window)")
room = window
files_fit = room // avg_file
print("files that fit unscoped", files_fit, f"of {repo_files} ({100 * files_fit / repo_files:.2f}% of repo)")
rmap, relevant = 2600, 8
scoped = rmap + relevant * avg_file
print("scoped context tokens  ", scoped)
print("scoped share of window ", f"{100 * scoped / window:.2f}%")
print("scoped share of repo   ", f"{100 * scoped / repo_tokens:.2f}%")
print("scoped input USD per task", money(scoped / 1e6 * IN, 6))
print("scoped input USD per 1000 tasks", money(scoped / 1e6 * IN * 1000, 2))
```

```text
repo tokens             480000 across 160 files
average file tokens     3000
window                  128000
repo / window           3.75 x
overflow tokens         352000 (275% of window)
files that fit unscoped 42 of 160 (26.25% of repo)
scoped context tokens   26600
scoped share of window  20.78%
scoped share of repo    5.54%
scoped input USD per task 0.079800
scoped input USD per 1000 tasks 79.80
```

#### အဖြေ ၆ — scope ကျဉ်းသည့် context ၏ saving

**ဖော်မြူလာ —** USD = prompt token × price_in ÷ 10⁶။ prefill ms = prompt token ÷ 1,000 × ms per 1,000 tokens။
ယူဆချက် — output token နှင့် output ကုန်ကျစရိတ် နှစ်နည်းလုံးတွင် တူညီသည်၊ ထို့ကြောင့်
input သာ ကွာခြားသည်။ prefill သည် window အရှည်နှင့် အချိုးကျသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. token အချိုး = 128,000 ÷ 22,000 = 5.818 ဆ ဖြစ်သည်။
2. task တစ်ခုလျှင် = $0.384 (naive) နှင့် $0.066 (scoped) ဖြစ်သည်။
3. task ၁,၀၀၀ လျှင် = $384 နှင့် $66 ဖြစ်သည်၊ သက်သာငွေ $318 ဖြစ်သည်။
4. saving = 318 ÷ 384 = 82.8 % ဖြစ်သည်။
5. prefill = 128,000 ÷ 1,000 × 12 = 1,536.0 ms နှင့် 22,000 ÷ 1,000 × 12 = 264.0 ms ဖြစ်သည်၊ သက်သာသည့် အချိန် 1,272.0 ms ဖြစ်သည်။

**အဓိပ္ပာယ် —** scoped context သည် ကုန်ကျစရိတ်ကို ၈၂.၈ % လျှော့သည်၊ prefill ကို ၁.၂၇ စက္ကန့်
လျှော့သည်။ သို့သော် ဤ saving သည် context recall မကျဆင်းမှသာ အမှန် ဖြစ်သည် — recall ကျဆင်းပါက
ပထမ ကြိုးစားမှု ကျရှုံးနှုန်း တိုးလာပြီး saving ကို retry က ပြန်စားသည် (ဆုံးဖြတ်ချက် ၁ ကို ကြည့်ပါ)။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

naive, scoped, tasks = 128000, 22000, 1000
prefill_ms_per_1k = 12.0
c_naive = naive / 1e6 * IN
c_scoped = scoped / 1e6 * IN
print("naive prompt tokens    ", naive)
print("scoped prompt tokens   ", scoped)
print("token ratio            ", round(naive / scoped, 3))
print("USD per task naive     ", money(c_naive, 6))
print("USD per task scoped    ", money(c_scoped, 6))
print("USD per 1000 tasks naive ", money(c_naive * tasks, 3))
print("USD per 1000 tasks scoped", money(c_scoped * tasks, 3))
print("USD saved per 1000 tasks ", money((c_naive - c_scoped) * tasks, 3))
print("saving pct             ", f"{100 * (c_naive - c_scoped) / c_naive:.1f}%")
print("prefill ms naive       ", round(naive / 1000 * prefill_ms_per_1k, 1))
print("prefill ms scoped      ", round(scoped / 1000 * prefill_ms_per_1k, 1))
print("prefill ms saved       ", round((naive - scoped) / 1000 * prefill_ms_per_1k, 1))
```

```text
naive prompt tokens     128000
scoped prompt tokens    22000
token ratio             5.818
USD per task naive      0.384000
USD per task scoped     0.066000
USD per 1000 tasks naive  384.000
USD per 1000 tasks scoped 66.000
USD saved per 1000 tasks  318.000
saving pct              82.8%
prefill ms naive        1536.0
prefill ms scoped       264.0
prefill ms saved        1272.0
```

### ၅.၂ ပြဿနာ ရှာဖွေခြင်း အဖြေများ

#### အဖြေ ၁ — agent သည် မသက်ဆိုင်သည့် ဖိုင်များကို တည်းဖြတ်ခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** patch တစ်ခုသည် ဖိုင် ပြောင်းလဲမှုများကို ဖမ်းယူသည်၊
၎င်းတို့ကို ဖြန့်ချိရန် လိုအပ်သည့် ကျိုးကြောင်းဆင်ခြင်မှု၊ test အထောက်အထား သို့မဟုတ်
ခွင့်ပြုချက်ကို ဖမ်းယူခြင်း မဟုတ်ပါ။ ထို့ကြောင့် ဖိုင် စာရင်း ကျယ်လာခြင်းကို patch တစ်ခုတည်းက
မတားဆီးနိုင်ပါ — scope contract တွင် ခွင့်ပြုထားသည့် နှင့် တားမြစ်ထားသည့် မျက်နှာပြင်ကို
အတိအကျ ရေးထားမှသာ တားဆီးနိုင်သည်။ ဖိုင် ၄၀ ကို ထိသည့် ပြောင်းလဲမှုသည် review ကို
၁၃ ဆ ခန့် ကြီးစေသည် (ဥပမာ ၃)၊ ထို ကုန်ကျစရိတ်သည် လုပ်ငန်း၏ တန်ဖိုးထက် ကြီးနိုင်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** patch ထိသည့် ဖိုင် စာရင်းကို ဦးစွာ ထုတ်ပါ၊ ထို့နောက်
repository instructions တွင် generated ဖိုင်၊ lock ဖိုင် နှင့် configuration ကို ဖော်ပြထားသလား စစ်ပါ။
ဖော်ပြထားပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ ဖော်ပြထားပြီး ဖြစ်ပါက ဖိုင် စာရင်းကို repository map
နှင့် တိုက်စစ်ပါ — (၃) ဖြစ်နိုင်သည်။ နှစ်ခုလုံး မဖြစ်ပါက agent သည် scope contract ကို မလိုက်နာခြင်း
ဖြစ်သည်၊ ထို အခြေအနေတွင် patch ကို ပယ်ချပြီး scope contract ကို ပိုတိကျအောင် ပြန်ရေးရမည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** ပြင်ပြီးနောက် patch တိုင်း၏ ဖိုင် စာရင်းသည် scope contract ၏
စာရင်းအတွင်းသာ ရှိပါက ဆုံးဖြတ်ချက် မှန်ကန်သည်။ ထို အချက်ကို diff review checklist ၏
ပထမ ဂိတ် အဖြစ် သတ်မှတ်ထားပါက လူသည် မိနစ်ပိုင်းအတွင်း စစ်နိုင်သည်။

#### အဖြေ ၂ — ဒေသတွင် အောင်သည်၊ CI တွင် ကျရှုံးခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** build တစ်ခုသည် ကြေညာထားသည့် source၊ ပတ်ဝန်းကျင်
နှင့် လမ်းညွှန်ချက်များဖြင့် သီးခြားစီ ပြန်လည် ထုတ်လုပ်နိုင်မှသာ artifact ကို မူလ စက်ကို
ကျော်လွန်၍ စစ်ဆေးနိုင်သည်။ ဒေသ နှင့် CI တွင် dependency ဗားရှင်း၊ environment variable,
locale သို့မဟုတ် အစဉ်လိုက်မှု ကွာခြားပါက test သည် ဒေသတွင် အောင်ပြီး CI တွင် ကျရှုံးသည်။
ကျရှုံးသည့် test သည် ထပ်ခါတလဲလဲ မတည်ငြိမ်ပါက flakiness သည် verification gate ကို
အားနည်းစေပြီး လူများ သို့မဟုတ် agent များက ကျရှုံးမှုကို လျစ်လျူရှုရန် လေ့ကျင့်ပေးသည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** ကျရှုံးသည့် test ကို ဒေသတွင် အစဉ်လိုက် run ပါ၊
ကျရှုံးမှု ပြန်ပေါ်ပါက flakiness ဖြစ်သည် (အကြောင်းရင်း ၂)။ ပြန်မပေါ်ဘဲ CI တွင်သာ
ကျရှုံးပါက toolchain နှင့် dependency lock ကို နှိုင်းယှဉ်ပါ (အကြောင်းရင်း ၁)။ lock
တူညီပါက CI တွင် run သည့် test အစုနှင့် environment variable ကို စစ်ပါ (အကြောင်းရင်း ၃ နှင့် ၄)။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** ပြင်ပြီးနောက် ဒေသ နှင့် CI ၏ ရလဒ် ကွာခြားမှု မရှိတော့ပါက
ပြဿနာသည် ပြန်လည် ထုတ်လုပ်နိုင်မှု ဖြစ်သည် ဟု အတည်ပြုနိုင်သည်။ ထို့ကြောင့် ဤပြဿနာကို
ဖြေရှင်းရာတွင် "test ကို ပြင်သည်" မဟုတ်ဘဲ "ပတ်ဝန်းကျင်ကို ကြေညာ၍ pin လုပ်သည်" ဖြစ်သည်။

#### အဖြေ ၃ — တူညီသည့် prompt သည် မတူညီသည့် ရလဒ် ပေးခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** prompt တူညီခြင်းသည် request တူညီခြင်းကို မဆိုလိုပါ။
routing သည် policy ဆုံးဖြတ်ချက် ဖြစ်သဖြင့် လက်ရှိ ရရှိနိုင်မှု၊ latency နှင့် ကုန်ကျစရိတ်
အလိုက် မော်ဒယ် သို့မဟုတ် provider ကို ရွေးချယ်နိုင်သည်။ semantic cache သည်
ဆင်တူသည့် request တစ်ခုကို ကိုက်ညီသည်ဟု ဆုံးဖြတ်ပါက ယခင် ရလဒ်ကို ပြန်ပေးနိုင်သည် —
ထို ရလဒ်သည် ခေတ်မမီတော့ခြင်း သို့မဟုတ် user အတွက် မသင့်လျော်ခြင်း ဖြစ်နိုင်သည်။
trace မရှိပါက ဤ ကွာခြားမှု၏ အရင်းအမြစ်ကို ရှာဖွေ၍ မရနိုင်ပါ။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** trace ထဲမှ မော်ဒယ် နှင့် provider ကို ကြည့်ပါ — ကွာခြားပါက
routing ဖြစ်သည် (အကြောင်းရင်း ၁)။ တူညီပါက cache hit rate ကို ကြည့်ပါ (အကြောင်းရင်း ၃)။
sampling parameter နှင့် prompt version ကို မှတ်တမ်းတင် မထားပါက နှစ်ခုကို ခွဲခြား၍
မရနိုင်ပါ (အကြောင်းရင်း ၂ နှင့် ၄) — ထို့ကြောင့် ဤပြဿနာကို ဖြေရှင်းရာတွင် observability
သည် အခြေခံ လိုအပ်ချက် ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** trace တွင် မော်ဒယ်၊ provider၊ prompt version နှင့်
sampling parameter အားလုံး ပါပြီးနောက် ရလဒ် ကွာခြားမှု တိုင်းကို အကြောင်းရင်း တစ်ခုခုသို့
ပြန်ချိတ်နိုင်ပါက အတည်ပြုပြီး ဖြစ်သည်။ ထို့နောက် ကွာခြားသည့် ဖြစ်ရပ် တိုင်းကို
regression test အဖြစ် ပြောင်းပါက ဤ ပြဿနာ ပြန်မပေါ်နိုင်ပါ။

### ၅.၃ ဆုံးဖြတ်ချက် အဖြေများ

#### အဖြေ ၁ — window တစ်ခုလုံး ထည့်ခြင်း နှင့် scope ကျဉ်းသည့် context

**ရှင်းလင်းချက် —** prompt token အရေအတွက်သည် prefill အလုပ်ပမာဏ၊ TTFT နှင့် input
ကုန်ကျစရိတ်ကို တိုက်ရိုက် သတ်မှတ်သည်။ 128,000 မှ 22,000 သို့ လျှော့ချသည့်အခါ token
သည် 5.818 ဆ လျော့သည်၊ task တစ်ခုလျှင် $0.402 မှ $0.084 သို့ ကျဆင်းသည်၊ TTFT သည်
1,792.0 ms မှ 308.0 ms သို့ ကျဆင်းသည်။ သို့သော် ဤ saving တစ်ခုတည်းဖြင့် မဆုံးဖြတ်ရ —
ပထမ ကြိုးစားမှု ကျရှုံးနှုန်းကို ထည့်သွင်းရမည်။

**ဆုံးဖြတ်ချက် —** ရွေးချယ်မှု B (repository map နှင့် scope ကျဉ်းသည့် context) ကို ရွေးရမည်၊
အကြောင်းမှာ task ၁,၀၀၀ လျှင် စုစုပေါင်းကုန်ကျစရိတ်သည် $840.16 မှ $421.58 သို့ ကျဆင်း၍
$418.58 သက်သာသည်။ ထို saving တွင် ကျရှုံးနှုန်း (18 % → 7 %) ကြောင့် ဖြစ်သည့် retry
ကုန်ကျစရိတ် လျော့နည်းမှုလည်း ပါဝင်ပြီး ဖြစ်သည်။ B ကို ရွေးသည့်အခါ repository map ကို
အမှန် ထိန်းသိမ်းထားရမည် — map မှားပါက context recall ကျဆင်းပြီး saving ကို ပြန်စားမည်။

**တိုင်းတာမည့် metric —** task ၁,၀၀၀ လျှင် စုစုပေါင်း USD၊ TTFT၊ context recall၊
ပထမ ကြိုးစားမှု အောင်နှုန်း။ ဤဆုံးဖြတ်ချက်တွင် ကုန်ကျစရိတ်သည် ပြတ်သားစွာ ကျဆင်းသည်၊
အန္တရာယ်မှာ map ၏ အရည်အသွေး ဖြစ်သဖြင့် recall သည် အဓိက အတည်ပြုချက် ဖြစ်သည်။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

window, scoped = 128000, 22000
tasks = 1000
ttft_ms_per_1k = 14.0
recall_full, recall_scoped = 0.94, 0.985
retry_full, retry_scoped = 0.18, 0.07
attempt_cost = 0.31
cost_full = window / 1e6 * IN + 1200 / 1e6 * OUT
cost_scoped = scoped / 1e6 * IN + 1200 / 1e6 * OUT
print("window tokens          ", window, "scoped tokens", scoped)
print("output tokens per task ", 1200)
print("USD per task full      ", money(cost_full, 6))
print("USD per task scoped    ", money(cost_scoped, 6))
print("USD per 1000 tasks full  ", money(cost_full * tasks, 2))
print("USD per 1000 tasks scoped", money(cost_scoped * tasks, 2))
print("wasted USD per 1000 tasks (full)", money((cost_full - cost_scoped) * tasks, 2))
print("TTFT ms full           ", round(window / 1000 * ttft_ms_per_1k, 1))
print("TTFT ms scoped         ", round(scoped / 1000 * ttft_ms_per_1k, 1))
print("context recall full    ", f"{100 * recall_full:.1f}%", "scoped", f"{100 * recall_scoped:.1f}%")
print("first-attempt failure full  ", f"{100 * retry_full:.1f}%", "scoped", f"{100 * retry_scoped:.1f}%")
attempts_full = tasks * (1 + retry_full)
attempts_scoped = tasks * (1 + retry_scoped)
print("attempts full          ", round(attempts_full, 1), "scoped", round(attempts_scoped, 1))
print("attempt cost USD       ", money(attempt_cost, 2))
print("total USD full         ", money(cost_full * attempts_full + attempts_full * attempt_cost, 2))
print("total USD scoped       ", money(cost_scoped * attempts_scoped + attempts_scoped * attempt_cost, 2))
print("total saving USD per 1000 tasks", money(cost_full * attempts_full + attempts_full * attempt_cost - cost_scoped * attempts_scoped - attempts_scoped * attempt_cost, 2))
```

```text
window tokens           128000 scoped tokens 22000
output tokens per task  1200
USD per task full       0.402000
USD per task scoped     0.084000
USD per 1000 tasks full   402.00
USD per 1000 tasks scoped 84.00
wasted USD per 1000 tasks (full) 318.00
TTFT ms full            1792.0
TTFT ms scoped          308.0
context recall full     94.0% scoped 98.5%
first-attempt failure full   18.0% scoped 7.0%
attempts full           1180.0 scoped 1070.0
attempt cost USD        0.31
total USD full          840.16
total USD scoped        421.58
total saving USD per 1000 tasks 418.58
```

#### အဖြေ ၂ — retry အရေအတွက် နှင့် idempotency

**ရှင်းလင်းချက် —** retry ကို ၃ ကြိမ် အထိ ခွင့်ပြုပါက မျှော်မှန်း ခေါ်ဆိုမှု အရေအတွက်သည်
task တစ်ခုလျှင် 1.0864 ဖြစ်သည်၊ ဆိုလိုသည်မှာ task ၁၀၀ အတွက် ထပ်ဆောင်း ခေါ်ဆိုမှု ၈.၆ ကြိမ်၊
ကုန်ကျစရိတ် $0.7258 ဖြစ်သည်။ idempotency key မရှိပါက မသေချာသည့် ခေါ်ဆိုမှုများအနက်
တစ်ဝက်ခန့် (task ၁၀၀ လျှင် ၄ ခု) သည် ထပ်နှစ်ဆ ဖြစ်နိုင်သည်၊ တစ်ခုလျှင် $250 ဖြင့်
$1,000 ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** idempotency key ကို မဖြစ်မနေ ထည့်ရမည်၊ retry ကို ၃ ကြိမ်တွင် ကန့်သတ်ရမည်။
အကြောင်းမှာ task ၁၀၀ လျှင် retry ကုန်ကျစရိတ် $0.7258 ဖြင့် ထပ်နှစ်ဆ ဖြစ်မှု ကုန်ကျစရိတ်
$1,000 ကို ဖယ်ရှားနိုင်သည်၊ ဆိုလိုသည်မှာ အသားတင် သက်သာငွေ $999.27 ဖြစ်သည် (task
၁,၀၀၀ လျှင် $9,992.74)။ retry overhead သည် သက်သာငွေ၏ 0.073 % သာ ဖြစ်သဖြင့်
idempotency မထည့်ရန် အကြောင်းပြချက် မရှိပါ။

**တိုင်းတာမည့် metric —** task ၁,၀၀၀ လျှင် ထပ်နှစ်ဆ ဖြစ်မှု အရေအတွက်၊ ထပ်ဆောင်း ခေါ်ဆိုမှု
ကုန်ကျစရိတ် နှင့် လက်ဖြင့် ပြန်ဖျက်ရသည့် USD။ ဤ ဆုံးဖြတ်ချက်တွင် ကိန်းဂဏန်း နှစ်ခုသည်
အဆင့် ကွာခြားသဖြင့် ဆုံးဖြတ်ချက်သည် ရှင်းလင်းသည် — retry အရေအတွက် ကန့်သတ်ခြင်းထက်
idempotency မရှိခြင်းသည် အန္တရာယ် ပိုကြီးသည်။

```bash
IN = 3.00    # USD per million input tokens
OUT = 15.00  # USD per million output tokens


def money(x, d=4):
    return f"{x:.{d}f}"

tasks, p_fail = 100, 0.08
attempt_cost = 0.084
p_uncertain_success = 0.5
dup_cleanup = 250.0
limit = 3
q = 1 - p_fail
exp_attempts = sum(k * q * p_fail ** (k - 1) for k in range(1, limit + 1)) + limit * p_fail ** limit
print("tasks                  ", tasks, "transient failure rate", f"{100 * p_fail:.0f}%")
print("retry limit            ", limit, "(1 first attempt +", limit - 1, "retries)")
print("USD per attempt        ", money(attempt_cost, 4))
print("expected attempts per task", round(exp_attempts, 4))
print("expected attempts total", round(exp_attempts * tasks, 1))
retry_attempts = exp_attempts * tasks - tasks
print("extra retry attempts   ", round(retry_attempts, 1), "USD", money(retry_attempts * attempt_cost, 4))
uncertain = tasks * p_fail * p_uncertain_success
print("uncertain successes per 100 tasks", round(uncertain, 1))
print("duplicate side effects without idempotency", round(uncertain, 1))
print("cleanup USD without idempotency", money(uncertain * dup_cleanup, 2))
print("cleanup USD with idempotency   ", money(0.0, 2))
print("net saving per 100 tasks USD   ", money(uncertain * dup_cleanup - retry_attempts * attempt_cost, 2))
print("net saving per 1000 tasks USD  ", money(10 * (uncertain * dup_cleanup - retry_attempts * attempt_cost), 2))
print("retry overhead share of saving ", f"{100 * retry_attempts * attempt_cost / (uncertain * dup_cleanup):.3f}%")
```

```text
tasks                   100 transient failure rate 8%
retry limit             3 (1 first attempt + 2 retries)
USD per attempt         0.0840
expected attempts per task 1.0864
expected attempts total 108.6
extra retry attempts    8.6 USD 0.7258
uncertain successes per 100 tasks 4.0
duplicate side effects without idempotency 4.0
cleanup USD without idempotency 1000.00
cleanup USD with idempotency    0.00
net saving per 100 tasks USD    999.27
net saving per 1000 tasks USD   9992.74
retry overhead share of saving  0.073%

```

## Self-check

၁။ ဥပမာ ၁ တွင် reserved output token သည် budget တွက်ချက်မှုကို မည်သို့ သက်ရောက်သည်။

၂။ ဥပမာ ၂ တွင် လူ၏ ပြုပြင်မှု မပါဘဲ နှင့် ပါဝင်သည့် cost per successful task သည် မည်သို့ ကွာခြားသည်၊
မည်သည့်အရာက ပိုကြီးသည်။

၃။ ဥပမာ ၃ တွင် scope ကျယ်လာပါက review နာရီ မည်မျှ ကွာခြားသည်။

၄။ အဖြေ ၅ တွင် repository တစ်ခုလုံး ပို့ခြင်း၏ ပြဿနာသည် window မလုံလောက်ခြင်း တစ်ခုတည်း ဖြစ်သလား။

၅။ အဖြေ ၂ (retry နှင့် idempotency) တွင် ဆုံးဖြတ်ချက် ကို ထောက်ခံသည့် ကိန်းဂဏန်း နှစ်ခုကို ဖော်ပြပါ။

<details>
<summary>အဖြေများ</summary>

၁။ reserved output token 3,000 ကို used တွင် ထည့်ရမည်။ မထည့်ပါက used သည် 9,030 token ဖြစ်၍
window အတွင်း ဝင်သည်ဟု ထင်ရသော်လည်း output အတွက် နေရာ မကျန်သဖြင့် အဖြေသည် အလယ်တွင်
ပြတ်တောက်သည်။ ထည့်ပါက used = 12,030 token ဖြစ်သည်။

၂။ လူ၏ ပြုပြင်မှု မပါဘဲ $0.122650၊ ပါဝင်ပါက $3.507265 ဖြစ်သည်။ လူ၏ ပြုပြင်မှု ($264.00) သည်
စုစုပေါင်း၏ 96.50 % ဖြစ်သဖြင့် လူ၏ အချိန် ပါသည့် တန်ဖိုး ပိုကြီးသည်။

၃။ scope ကျဉ်းသည့် patch သည် 0.96 နာရီ၊ refactor သည် 12.8 နာရီ ဖြစ်သည်၊ ဆိုလိုသည်မှာ
13.33 ဆ ကွာခြားသည်။

၄။ မဟုတ်ပါ။ repository ၏ token သည် window ထက် 3.75 ဆ ကြီးသဖြင့် မည်သည့် window ဖြင့်မျှ
အပြည့် မဝင်နိုင်ပါ။ ထို အခြေအနေတွင် window ကြီးခြင်းသည် အန္တရာယ် ဖြစ်သည် —
context အချက်အလက် မပြည့်စုံဘဲ token ကုန်ကျစရိတ်သာ တိုးသည်။

၅။ retry ကြောင့် ထပ်ဆောင်း ကုန်ကျစရိတ်သည် task ၁၀၀ လျှင် $0.7258 ဖြစ်သည်၊ idempotency
မရှိခြင်းကြောင့် ထပ်နှစ်ဆ ဖြစ်မှု ကုန်ကျစရိတ်သည် $1,000 ဖြစ်သည်၊ အသားတင် သက်သာငွေ
$999.27 ဖြစ်သည်။

</details>

## References

- နယ်ပယ် အခြေခံ အချက်အလက် — `terms/08_ai_native_development.md` နှင့် `glossary/by_area/08_ai_native_development.json`။
- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed၊ `rohitg00/ai-engineering-from-scratch` မှ။
- Source lesson လင့်များ — [Scope Contracts](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/36-scope-contracts/)၊
  [Reviewer Agent](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/39-reviewer-agent/)၊
  [Multi-Session Handoff](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/40-multi-session-handoff/)၊
  [Eval-Driven Agent Development](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/30-eval-driven-agent-development/)။
- လက်တွေ့ lab များ — `labs/lab_context_strategy.py`၊ `labs/lab_review_budget.py`၊
  `labs/lab_change_cost.py`။
- ကိန်းဂဏန်း အားလုံးကို standard library သာ အသုံးပြု၍ တွက်ချက်သည် — Python 3.11+။
