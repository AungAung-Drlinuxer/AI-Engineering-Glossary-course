# ၀၄ — လေ့ကျင့်ခန်းများနှင့် အဖြေများ (Agents & Tools)

ဤဖိုင်သည် နယ်ပယ် ၀၆ ၏ term ၂၇ ခုကို အသုံးပြု၍ တွက်ချက်ခြင်း၊ ပြဿနာ ရှာဖွေခြင်းနှင့် ဆုံးဖြတ်ချက် ချခြင်း
လေ့ကျင့်ခန်းများကို စုစည်းထားသည်။ အပိုင်း ၁ တွင် အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာ လေးခု၊ အပိုင်း ၂ တွင်
တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ခြောက်ခု၊ အပိုင်း ၃ တွင် ပြဿနာ ရှာဖွေခြင်း သုံးခု၊ အပိုင်း ၄ တွင်
ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း နှစ်ခု ပါဝင်သည်။ အပိုင်း ၅ တွင် အဖြေတိုင်းကို ဖော်မြူလာ၊ တွက်ချက်မှု အဆင့်ဆင့်နှင့်
အကြောင်းရင်း ရှင်းလင်းချက်နှင့်အတူ ပေးထားသည်။

အပိုင်း ၁၊ အပိုင်း ၅.၁ နှင့် အပိုင်း ၅.၃ တွင် ပါဝင်သည့် ကိန်းဂဏန်း တိုင်းသည် Python (standard library သာ) ဖြင့်
အမှန်တကယ် လုပ်ဆောင်ခဲ့သည့် တွက်ချက်မှု၏ output ဖြစ်သည်။ ဖော်ပြထားသည့် block အတိုင်း run လုပ်ပါက
တူညီသည့် output ကို ပြန်လည် ရရှိမည်။ ကိန်းဂဏန်း တိုင်းသည် သတ်မှတ်ထားသည့် ယူဆချက် (assumption)
အပေါ် မှီခိုသည်၊ ထို့ကြောင့် ဖော်မြူလာ တစ်ခုစီနှင့်အတူ ၎င်း၏ ယူဆချက်ကို ဖော်ပြထားသည်။

**အသုံးပြုသည့် စျေးနှုန်း ယူဆချက်** — input token သန်း တစ်သန်းလျှင် USD 2.50၊ output token သန်း
တစ်သန်းလျှင် USD 10.00၊ prompt cache ရေးသွင်းခြင်း 1.25 ဆ၊ cache ပြန်ဖတ်ခြင်း 0.10 ဆ။ ဤ တန်ဖိုးများသည်
provider အလိုက် ကွာခြားသည်၊ ထို့ကြောင့် အဖြေ၏ ပုံသဏ္ဍာန်ကို ကြည့်ရမည်၊ ဂဏန်း တိကျမှုကို မဟုတ်ပါ။

## ၁။ အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာများ (Worked Examples)

### ဥပမာ ၁ — မော်ဒယ် call တစ်ခုနှင့် loop တစ်ခု

**ယူဆချက် —** call တစ်ခုတည်း၏ input သည် 5,100 token၊ output သည် 240 token။ loop တစ်ခုတွင် step ခြောက်ခု
ရှိသည်၊ step တိုင်း၏ output သည် 260 token၊ step တိုင်း၏ input သည် base 3,000 token မှ စ၍ step တိုင်း
2,170 token တိုးသည် (ယခင် step ၏ tool result နှင့် မော်ဒယ် ပြန်ကြားချက် စုပုံလာခြင်း)။ tool execution
ကုန်ကျစရိတ်ကို မထည့်သွင်းပါ။

**ဖော်မြူလာ —**
- call တစ်ခု၏ USD = input × price_in + output × price_out
- loop ၏ input = ∑ (base + growth × k), k = 0 … steps − 1
- loop ၏ output = steps × output_per_step
- loop ၏ USD = loop input × price_in + loop output × price_out

**တွက်ချက်မှု —**
1. call တစ်ခု = 5,100 × 2.50 / 10⁶ + 240 × 10.00 / 10⁶ = 0.01275 + 0.00240 = USD 0.01515 ဖြစ်သည်။
2. loop input = 6 × 3,000 + 2,170 × (0 + 1 + 2 + 3 + 4 + 5) = 18,000 + 32,550 = 50,550 token ဖြစ်သည်။
3. loop output = 6 × 260 = 1,560 token ဖြစ်သည်။
4. loop USD = 50,550 × 2.50 / 10⁶ + 1,560 × 10.00 / 10⁶ = 0.126375 + 0.015600 = USD 0.141975 ဖြစ်သည်။
5. အချိုး = 0.141975 / 0.01515 = 9.37 ဆ ဖြစ်သည်။
6. step ခြောက်ခုမြောက်၏ input = 3,000 + 2,170 × 5 = 13,850 token ဖြစ်သည်။

**ကောက်ချက် —** loop ၏ ကုန်ကျစရိတ်သည် call တစ်ခုထက် 9.37 ဆ ဖြစ်သည်၊ သို့သော် တိုးလာသည့် အပိုင်း
အားလုံးသည် **input** ဖြစ်သည် (USD 0.01515 မှ USD 0.141975 သို့ premium USD 0.126825 ၏ အများစုသည်
input မှ လာသည်)။ ဤ အချက်သည် loop ကို စနစ် ပုံစံ ချရာတွင် **input ကို ထိန်းခြင်း** သည် **output ကို
ထိန်းခြင်း** ထက် ပို၍ အရေးပါကြောင်း ပြသည်။

```bash
python3 - <<'PY'
def usd(t, ppm):
    return t / 1e6 * ppm

single_in, single_out = 5100, 240
single = usd(single_in, 2.50) + usd(single_out, 10.00)
print("single call input tokens      ", single_in)
print("single call output tokens     ", single_out)
print("single call USD               ", round(single, 6))

base_in, per_step_growth = 3000, 2170
steps, out_per_step = 6, 260
loop_in = sum(base_in + per_step_growth * k for k in range(steps))
loop_out = steps * out_per_step
loop = usd(loop_in, 2.50) + usd(loop_out, 10.00)
print("loop input tokens total       ", loop_in)
print("loop output tokens total      ", loop_out)
print("loop USD                      ", round(loop, 6))
print("loop / single ratio           ", round(loop / single, 2))
print("step 6 input tokens           ", base_in + per_step_growth * 5)
print("USD premium over single call  ", round(loop - single, 6))
PY
```

```text
single call input tokens       5100
single call output tokens      240
single call USD                0.01515
loop input tokens total        50550
loop output tokens total       1560
loop USD                       0.141975
loop / single ratio            9.37
step 6 input tokens            13850
USD premium over single call   0.126825
```

### ဥပမာ ၂ — Tool contract ၏ validation အဆင့်များနှင့် ၎င်း၏ ကုန်ကျစရိတ်

**ယူဆချက် —** request 50 ခုကို နမူနာ စစ်သည်။ အဆင့် ၁ (JSON Schema) သည် 3 ခုကို ငြင်းပယ်သည်၊
အဆင့် ၂ (semantic check — allowed root, maximum size, base revision) သည် 1 ခုကို ငြင်းပယ်သည်။
ငြင်းပယ်ခံရသည့် request တိုင်းသည် မော်ဒယ်ထံ ပြန်လည်ပေးအပ်၍ ပြန်လည်ကြိုးစားရသဖြင့် call တစ်ခု
ပိုကုန်သည် (input 7,400 token၊ output 300 token)။

**ဖော်မြူလာ —**
- ငြင်းပယ်ခံရသည့် call ၏ USD = retry_in × price_in + retry_out × price_out
- မျှော်မှန်း ကုန်ကျစရိတ် / request = ငြင်းပယ်နှုန်း × retry USD

**တွက်ချက်မှု —**
1. retry USD = 7,400 × 2.50 / 10⁶ + 300 × 10.00 / 10⁶ = 0.0185 + 0.0030 = USD 0.0215 ဖြစ်သည်။
2. ငြင်းပယ်နှုန်း = (3 + 1) / 50 = 8.0 % ဖြစ်သည်။
3. မျှော်မှန်း ကုန်ကျစရိတ် / request = 0.08 × 0.0215 = USD 0.00172 ဖြစ်သည်။
4. call 1,000 ခုအတွက် = USD 1.72 ဖြစ်သည်။
5. အဆင့် ၂ တွင် ငြင်းပယ်ခြင်းသည် **ဆောင်ရွက်မှု မဖြစ်မီ** ဖြစ်သဖြင့် idempotency key မလိုအပ်ပါ။
   အဆင့် ၂ မရှိဘဲ ဆောင်ရွက်ပြီးမှ စစ်ပါက ထို request 1 ခုတွင် write တစ်ခု ပြီးသွားပြီး
   `Compensating Action` လိုအပ်လာသည်။

**ကောက်ချက် —** validation ကို ဘယ်ဘက်သို့ (schema အဆင့်သို့) ရွှေ့ခြင်းသည် USD အနည်းငယ်သာ
သက်သာစေသော်လည်း **လုံခြုံရေး နယ်နိမိတ်** ကို တိုက်ရိုက် ပြောင်းလဲသည် — ငြင်းပယ်ခြင်းသည် ဘေးထွက်ဆိုးကျိုး
မဖြစ်မီ ဖြစ်လာသည်။ ထို့ကြောင့် contract ကို စျေးနှုန်းဖြင့် မဆုံးဖြတ်ရ။

```bash
python3 - <<'PY'
retry_in, retry_out = 7400, 300
retry = retry_in / 1e6 * 2.50 + retry_out / 1e6 * 10.00
print("rejected call retry USD       ", round(retry, 6))
sample, schema_reject, semantic_reject = 50, 3, 1
print("schema layer rejections / 50  ", schema_reject)
print("semantic layer rejections / 50", semantic_reject)
print("executions saved by semantic  ", semantic_reject)
print("reject rate pct               ", round(100 * (schema_reject + semantic_reject) / sample, 1))
per_req = (schema_reject + semantic_reject) / sample * retry
print("expected retry USD per request", round(per_req, 6))
print("USD per 1000 calls            ", round(per_req * 1000, 4))
print("blast radius without semantic ", semantic_reject, "write(s) already done before rejection")
PY
```

```text
rejected call retry USD        0.0215
schema layer rejections / 50   3
semantic layer rejections / 50 1
executions saved by semantic   1
reject rate pct                8.0
expected retry USD per request 0.00172
USD per 1000 calls             1.72
blast radius without semantic  1 write(s) already done before rejection
```

### ဥပမာ ၃ — Explicit state နှင့် transcript ပြန်ဖတ်ခြင်း

**ယူဆချက် —** turn 12 ခု ရှိသည်။ prefix (system prompt + tool schema) သည် 3,000 token၊ turn တိုင်း
2,170 token တိုးသည်။ ရွေးချယ်မှု A သည် transcript တစ်ခုလုံးကို ပို့သည်။ ရွေးချယ်မှု B သည်
`Agent State` object (420 token) နှင့် နောက်ဆုံး turn နှစ်ခုကို သာ ပို့သည်။

**ဖော်မြူလာ —**
- ရွေးချယ်မှု A ၏ input = ∑ (prefix + growth × k), k = 0 … turns − 1
- ရွေးချယ်မှု B ၏ input = turns × (prefix + growth × kept_turns + state_size)

**တွက်ချက်မှု —**
1. A ၏ နောက်ဆုံး turn = 3,000 + 2,170 × 12 = 29,040 token ဖြစ်သည်။
2. A ၏ input စုစုပေါင်း = 12 × 3,000 + 2,170 × (0 + … + 11) = 36,000 + 143,220 = 179,220 token ဖြစ်သည်။
3. A ၏ USD = 179,220 × 2.50 / 10⁶ = USD 0.44805 ဖြစ်သည်။
4. B ၏ turn တစ်ခုလျှင် = 3,000 + 2,170 × 2 + 420 = 7,760 token ဖြစ်သည်။
5. B ၏ input = 12 × 7,760 = 93,120 token ဖြစ်သည်၊ USD 0.23280 ဖြစ်သည်။
6. သက်သာသည့် token = 86,100 ဖြစ်သည်၊ ဆိုလိုသည်မှာ 48.0 % ဖြစ်သည်။

**ကောက်ချက် —** explicit state သည် transcript ကို အစားထိုးခြင်း မဟုတ်ဘဲ **တိုချုံ့ခြင်း** ဖြစ်သည်။
state object 420 token ကို ထည့်ခြင်းသည် အလွန်အကျွံ မဖြစ်ပါ၊ အကြောင်းမှာ ၎င်းသည် turn ရှစ်ခုစာ
transcript (≈ 17,360 token) ကို အစားထိုးပေးသောကြောင့် ဖြစ်သည်။

```bash
python3 - <<'PY'
prefix, per_turn, turns = 3000, 2170, 12
full_input = sum(prefix + per_turn * k for k in range(turns))
print("full transcript last turn tok ", prefix + per_turn * turns)
print("full transcript input total   ", full_input)
print("full input USD                ", round(full_input / 1e6 * 2.50, 6))
state_obj, kept = 420, 2
per_turn_trim = prefix + per_turn * kept + state_obj
trim_input = turns * per_turn_trim
print("trimmed last turn tokens      ", per_turn_trim)
print("trimmed input total           ", trim_input)
print("trimmed input USD             ", round(trim_input / 1e6 * 2.50, 6))
print("tokens saved                  ", full_input - trim_input)
print("saving pct                    ", round(100 * (full_input - trim_input) / full_input, 1))
PY
```

```text
full transcript last turn tok  29040
full transcript input total    179220
full input USD                 0.44805
trimmed last turn tokens       7760
trimmed input total            93120
trimmed input USD              0.2328
tokens saved                   86100
saving pct                     48.0
```

### ဥပမာ ၄ — Sandbox နှင့် approval gate ၏ ဘတ်ဂျက်

**ယူဆချက် —** agent run 200 ခု / နေ့။ sandbox မရှိပါက run ၏ 3.0 % သည် လူက ပြုပြင်ရမည့်
ဘေးထွက်ဆိုးကျိုး ဖြစ်စေသည်၊ ပြုပြင်ချိန် 40 မိနစ်၊ မိနစ်လျှင် USD 1.20။ sandbox ရှိပါက 0.3 % သို့
ကျဆင်းသည်။ approval gate ကို run ၏ 5.0 % က ထိသည်၊ စောင့်ချိန် 240 စက္ကန့်။

**ဖော်မြူလာ —**
- incident / နေ့ = runs × rate
- ပြုပြင် USD = incident × repair_min × rate_per_min
- ပျမ်းမျှ စောင့်ချိန် / run = gated_runs × wait_s / runs

**တွက်ချက်မှု —**
1. sandbox မရှိပါက incident 6.00 ခု / နေ့၊ USD 288.00 / နေ့ ဖြစ်သည်။
2. sandbox ရှိပါက incident 0.60 ခု / နေ့၊ USD 28.80 / နေ့ ဖြစ်သည်။
3. နေ့စဉ် သက်သာမှု = USD 259.20 ဖြစ်သည်၊ တစ်နှစ်လျှင် USD 94,608.00 ဖြစ်သည်။
4. approval gate ထိသည့် run = 10.0 ခု / နေ့ ဖြစ်သည်။
5. ပျမ်းမျှ စောင့်ချိန် = 10 × 240 / 200 = 12.0 စက္ကန့် / run ဖြစ်သည်၊ နေ့စဉ် 0.67 နာရီ စောင့်သည်။

**ကောက်ချက် —** sandbox သည် နယ်နိမိတ်သာ ကန့်သတ်ခြင်း မဟုတ်ဘဲ **ကုန်ကျစရိတ်ကို** တိုက်ရိုက် လျှော့ပေးသည်။
approval gate သည် ပျမ်းမျှ 12 စက္ကန့် ပေါင်းထည့်သော်လည်း ၎င်းသည် run တိုင်းတွင် မဟုတ်ဘဲ 5 % တွင်သာ
ဖြစ်သဖြင့် ခံစားမှု သက်ရောက်မှု သေးငယ်သည်။

```bash
python3 - <<'PY'
runs, repair_min, rate = 200, 40, 1.20
for label, pct in (("no sandbox", 3.0), ("sandbox", 0.3)):
    bad = runs * pct / 100
    print(f"{label:12} incidents/day {bad:6.2f} repair USD/day {bad * repair_min * rate:8.2f}")
no_sb, sb = runs * 0.03 * repair_min * rate, runs * 0.003 * repair_min * rate
print("daily saving USD              ", round(no_sb - sb, 2))
print("annual saving USD             ", round((no_sb - sb) * 365, 2))
gate_pct, wait_s = 5.0, 240
gated = runs * gate_pct / 100
print("runs hitting approval gate/day", gated)
print("average wait added per run s  ", round(gated * wait_s / runs, 1))
print("hours waiting per day         ", round(gated * wait_s / 3600, 2))
PY
```

```text
no sandbox   incidents/day   6.00 repair USD/day   288.00
sandbox      incidents/day   0.60 repair USD/day    28.80
daily saving USD               259.2
annual saving USD              94608.0
runs hitting approval gate/day 10.0
average wait added per run s   12.0
hours waiting per day          0.67
```

## ၂။ တွက်ချက်ရသည့် လေ့ကျင့်ခန်းများ (Calculation Exercises)

လေ့ကျင့်ခန်း တစ်ခုစီတွင် ကိန်းဂဏန်း အဖြေ အတိအကျ ရှိသည်။ အဖြေ၊ ဖော်မြူလာ နှင့် အဆင့်ဆင့်
တွက်ချက်မှုကို အပိုင်း ၅.၁ တွင် ပေးထားသည်။

**လေ့ကျင့်ခန်း ၁ — Tool schema ကို turn တိုင်း ပို့ခြင်း**

tool schema ၏ serialized JSON သည် အက္ခရာ 9,200 ခု ရှိသည်၊ token တစ်ခုလျှင် အက္ခရာ 4 ခု ဟု
ယူဆသည်၊ session တွင် turn 12 ခု ရှိသည်၊ input သန်း တစ်သန်းလျှင် USD 2.50။ တွက်ရမည့် အချက်များ —
(က) schema token အရေအတွက်၊ (ခ) turn 12 ခုအတွင်း schema အတွက် ကုန်သည့် token၊ (ဂ) ထို token ၏ USD၊
(ဃ) 3,000 token ရှိသည့် prefix ထဲတွင် schema ၏ ရာခိုင်နှုန်း၊ (င) turn 200 ခုအထိ တိုးပါက USD။

**လေ့ကျင့်ခန်း ၂ — Tool result အရွယ်အစားနှင့် context ကြီးထွားမှု**

system prompt 700 token၊ tool schema 2,300 token၊ turn တိုင်း tool result 1,800 token၊ မော်ဒယ်
ပြန်ကြားချက် 250 token၊ လုပ်ဆောင်ချက် ဖော်ပြချက် 120 token။ context window 12,000 token။
တွက်ရမည့် အချက်များ — (က) turn 1 မှ turn 10 အထိ context အရွယ်အစား၊ (ခ) turn 10 ခုအတွင်း
စုစုပေါင်း input token နှင့် USD၊ (ဂ) window ကို ကျော်လွန်သည့် ပထမဆုံး turn၊ (ဃ) tool result ကို
400 token သို့ ကန့်သတ်ပါက စုစုပေါင်း input နှင့် သက်သာသည့် ရာခိုင်နှုန်း။

**လေ့ကျင့်ခန်း ၃ — တာဝန် တစ်ခုအတွက် step အရေအတွက်နှင့် ကုန်ကျစရိတ်**

တာဝန်တစ်ခုကို step ခြောက်ခုဖြင့် ဆောင်ရွက်သည် — read issue (input 4,200၊ output 180)၊
read file (5,100၊ 240)၊ run tests (6,000၊ 320)၊ write patch (7,400၊ 900)၊ run tests again (8,600၊ 260)၊
open PR (9,100၊ 420)။ တွက်ရမည့် အချက်များ — (က) step အရေအတွက်နှင့် စုစုပေါင်း input/output token၊
(ခ) input အပိုင်းနှင့် output အပိုင်း၏ USD၊ (ဂ) စုစုပေါင်း USD၊ (ဃ) step 5 ကို တစ်ကြိမ် ပြန်ကြိုးစားပါက
ထပ်ကုန်သည့် USD နှင့် တိုးလာသည့် ရာခိုင်နှုန်း။

**လေ့ကျင့်ခန်း ၄ — Retry policy ၏ မျှော်မှန်း attempt နှင့် ကုန်ကျစရိတ်**

attempt တစ်ခုစီ၏ အောင်မြင်နိုင်ခြေ p = 0.70 ဖြစ်သည် (transient failure 30 %)၊ attempt တစ်ခု၏
ကုန်ကျစရိတ် USD 0.0045။ တွက်ရမည့် အချက်များ — (က) အများဆုံး attempt 1၊ 2၊ 3၊ 4၊ 5 အတွက်
မျှော်မှန်း attempt အရေအတွက်၊ (ခ) ထို attempt များ၏ မျှော်မှန်း USD၊ (ဂ) escalation ဖြစ်နိုင်ခြေ
ရာခိုင်နှုန်း၊ (ဃ) attempt 3 မှ 4 သို့ တိုးခြင်း၏ အကျိုးအမြတ် (USD နှင့် escalation ရာခိုင်နှုန်းအမှတ်)၊
(င) request 10,000 ခုအတွက် မျှော်မှန်း USD။

**လေ့ကျင့်ခန်း ၅ — Loop ၏ latency**

step တိုင်းတွင် မော်ဒယ် call 900 ms၊ ၎င်းနောက် tool execution 250 ms ရှိသည်။ loop တွင် မော်ဒယ်
step ခြောက်ခု ရှိသည်။ တွက်ရမည့် အချက်များ — (က) model အချိန်၊ tool အချိန် နှင့် စုစုပေါင်း
latency၊ (ခ) tool call သုံးခုကို တစ်ပြိုင်နက် ဆောင်ရွက်ပါက သက်သာသည့် မီလီစက္ကန့်နှင့် ရာခိုင်နှုန်း၊
(ဂ) မော်ဒယ် call သည် 20 % ကြာလာပါက စုစုပေါင်း၊ (ဃ) tool အပိုင်း၏ latency ရှယ် (share)။

**လေ့ကျင့်ခန်း ၆ — Schema prefix တည်ငြိမ်သည့်အခါ cache ၏ အလျော့အကျ**

တည်ငြိမ်သည့် prefix (system prompt 700 + tool schema 2,300) = 3,000 token၊ turn 12 ခု၊ input
သန်း တစ်သန်းလျှင် USD 2.50။ cache ရေးသွင်းခြင်းသည် 1.25 ဆ၊ cache ပြန်ဖတ်ခြင်းသည် 0.10 ဆ။
တွက်ရမည့် အချက်များ — (က) cache မပါဘဲ ကျခံရသည့် token နှင့် USD၊ (ခ) cache ရေးသွင်းခြင်း
(turn 1) ၏ USD၊ (ဂ) cache ပြန်ဖတ်ခြင်း (turn 2–12) ၏ USD၊ (ဃ) cache ပါသည့် စုစုပေါင်း USD နှင့်
သက်သာသည့် ရာခိုင်နှုန်း၊ (င) cache မပါသည့် ကုန်ကျစရိတ်သည် cache ပါသည့် ကုန်ကျစရိတ်၏
မည်မျှဆ ဖြစ်သည်။

## ၃။ ပြဿနာ ရှာဖွေခြင်း (Troubleshooting Scenarios)

ပြဿနာ တစ်ခုစီကို symptom၊ တိုင်းတာရမည့် အချက်၊ ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်)၊
ဖြေရှင်းနည်းနှင့် ရှင်းလင်းသည့် term ဟူသည့် အစဉ်အတိုင်း ဖော်ပြထားသည်။ အကြောင်းရင်း အစဉ်သည်
တိုင်းတာမှုဖြင့် ရှာဖွေနိုင်သည့် အစဉ်အတိုင်း ဖြစ်သည်။ အသေးစိတ် ရှင်းလင်းချက်ကို အပိုင်း ၅.၂ တွင် ပေးထားသည်။

### ပြဿနာ ၁ — Loop သည် ဘယ်တော့မှ မဆုံး

- **Symptom —** agent သည် ရပ်တန့်ခြင်း မရှိဘဲ tool များကို ထပ်ခါတလဲလဲ ခေါ်သည်၊ တူညီသည့်
  အလုပ်များ ပြန်ဖြစ်သည်၊ ကုန်ကျစရိတ် စဉ်ဆက်မပြတ် တိုးသည်။
- **တိုင်းတာရမည့် အချက် —** step အရေအတွက်၊ စုစုပေါင်း token နှင့် USD၊ ထပ်ခါတလဲလဲ ဖြစ်သည့်
  tool call အရေအတွက်၊ အောင်မြင်မှု အထောက်အထား ရှိမရှိ၊ ပြီးစီးခြင်းကို ဆုံးဖြတ်သည့် စည်းမျဉ်း ရှိမရှိ။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) အောင်မြင်မှု အထောက်အထားကို မသတ်မှတ်ထားခြင်း၊
  (၂) step အများဆုံးနှင့် ကုန်ကျစရိတ် ကန့်သတ်ချက် မရှိခြင်း၊ (၃) ပြန်လည်ကြိုးစား၍ မရနိုင်သည့်
  အမှားကို retry အဖြစ် ရေတွက်ခြင်း၊ (၄) observation သည် မော်ဒယ်အား ရှေ့သို့ မတွန်းအားပေးသဖြင့်
  တူညီသည့် လုပ်ဆောင်ချက်သို့ ပြန်ရောက်ခြင်း၊ (၅) escalation အခြေအနေကို မသတ်မှတ်ထားခြင်း။
- **ဖြေရှင်းနည်း —** loop မစတင်မီ အောင်မြင်မှု အထောက်အထား၊ step အများဆုံး၊ ကုန်ကျစရိတ်
  ကန့်သတ်ချက်၊ non-retryable error စာရင်းနှင့် escalation အခြေအနေများကို သတ်မှတ်ရမည်။
  အလားတူ လုပ်ဆောင်ချက် သုံးကြိမ် ထပ်ဖြစ်ပါက loop ကို ရပ်ရမည်။
- **ရှင်းလင်းသည့် term —** Termination Condition, Agent Harness, Orchestration, Verification Gate၊
  Stop Sequence (`Termination Condition` နှင့် မတူပါ)။

### ပြဿနာ ၂ — မော်ဒယ်သည် tool က ငြင်းပယ်သည့် argument များကို ရေးထုတ်သည်

- **Symptom —** tool call များ၏ အချို့သည် validation တွင် ငြင်းပယ်ခံရသည်၊ မှန်ကန်ပုံရသည့်
  field အမည်များ ပါသော်လည်း တန်ဖိုးများ မှားသည် (ဥပမာ ခွင့်မပြုသည့် path၊ ပျောက်ဆုံးနေသည့်
  base revision၊ သတ်မှတ်ထက်ကြီးသည့် အရွယ်အစား)။ retry များ၍ ကုန်ကျစရိတ် တိုးသည်။
- **တိုင်းတာရမည့် အချက် —** tool call တိုင်း၏ ငြင်းပယ်နှုန်း (schema အဆင့်နှင့် semantic အဆင့်
  ခွဲခြား၍)၊ retry အရေအတွက်၊ schema နှင့် tool description တွင် ဖော်ပြထားသည့် အချက်နှင့်
  contract တွင် တကယ် စစ်ဆေးသည့် အချက် ကွာခြားမှု၊ ငြင်းပယ်ခံရသည့် argument တန်ဖိုးများ၏ ပုံစံ။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) မော်ဒယ်က မြင်နိုင်သည့် schema သည်
  contract ၏ စစ်ဆေးချက်များကို ဖော်ပြမထားခြင်း (မော်ဒယ်က ခန့်မှန်းရသည်)၊ (၂) error message သည်
  ဘာကို မှန်အောင် ပြင်ရမည်ကို ပြန်မပြောခြင်း၊ (၃) enum၊ range သို့မဟုတ် format ကို schema တွင်
  မကန့်သတ်ထားခြင်း၊ (၄) tool description နှင့် tool အမည်သည် တူညီလုနီးပါး ဖြစ်နေသဖြင့်
  မှားယွင်းသည့် tool ကို ရွေးခြင်း၊ (၅) ငြင်းပယ်ခြင်း အားလုံးကို retry ဖြင့် ဖြေရှင်းရန် ကြိုးစားခြင်း။
- **ဖြေရှင်းနည်း —** contract ၏ စစ်ဆေးချက်ကို schema ထဲ ရောင်ပြန်ဟပ်စေရမည် (allowed root၊ maximum
  size၊ base revision ကို required field အဖြစ်)၊ error တိုင်းတွင် ငြင်းပယ်သည့် အကြောင်းရင်းနှင့်
  ပြင်ရမည့် field ကို ဖော်ပြရမည်၊ non-retryable error ကို သီးခြား သတ်မှတ်ရမည်၊ tool အမည်များကို
  ခွဲခြားနိုင်အောင် ထားရမည်။
- **ရှင်းလင်းသည့် term —** Tool Contract, Function Calling, Structured Output, Termination Condition,
  Agent Harness။

### ပြဿနာ ၃ — Cost သည် turn တိုင်း ကြီးထွားသည်

- **Symptom —** request အရေအတွက်နှင့် တာဝန် အမျိုးအစား မပြောင်းလဲသော်လည်း session အရှည်နှင့်အတူ
  turn တိုင်း၏ ကုန်ကျစရိတ် တိုးလာသည်၊ နောက်ပိုင်း turn များသည် အစ turn များထက် များစွာ ကုန်သည်။
- **တိုင်းတာရမည့် အချက် —** turn အလိုက် input token ပမာဏနှင့် ၎င်း၏ တိုးနှုန်း၊ tool result
  တစ်ခုလျှင် token၊ transcript တွင် ထည့်သည့် အပိုင်းများ၏ အချိုး၊ cache hit rate၊ context window
  နှင့် နှိုင်းယှဉ်ချက်၊ အနှစ်ချုပ်ခြင်း ရှိမရှိ။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) turn တိုင်းသည် ယခင် context အားလုံးကို ပြန်ပို့သဖြင့်
  input သည် quadratic နီးပါး စုပုံခြင်း၊ (၂) tool result ကြီးများကို တိုချုံ့ခြင်း မရှိဘဲ ထည့်ခြင်း၊
  (၃) `Agent State` မရှိဘဲ transcript ကို တစ်ခုတည်းသော မှတ်တမ်း အဖြစ် အသုံးပြုခြင်း၊
  (၄) prefix cache မကိုက်အောင် prompt ၏ အစကို turn တိုင်း ပြောင်းခြင်း၊ (၅) retry များ၍
  တူညီသည့် turn ကို နှစ်ကြိမ် ကျခံရခြင်း။
- **ဖြေရှင်းနည်း —** `Agent State` object ကို တစ်ခုတည်းသော အခြေခံ အဖြစ် ထားရမည်၊ transcript ကို
  နောက်ဆုံး turn အနည်းငယ်သာ ထားရမည်၊ tool result များ၏ အရွယ်အစားကို ကန့်သတ်ရမည်၊
  prefix ကို တူညီသည့် အစဉ်အတိုင်း ထား၍ cache ကို အသုံးချရမည်၊ prompt token ကို turn အလိုက်
  မှတ်တမ်းတင်ရမည်။
- **ရှင်းလင်းသည့် term —** Agent Memory, Agent State, Checkpoint, Context Engineering, Semantic Cache။

## ၄။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်းများ (Design Decisions)

### ဆုံးဖြတ်ချက် ၁ — Routing autonomy သို့မဟုတ် တိကျသည့် workflow

**အခြေအနေ —** tool များကို ခေါ်သည့် internal assistant တစ်ခုသည် request 10,000 ခု / လ ရှိသည်။
ရွေးချယ်မှု A သည် မော်ဒယ်ကို routing လုပ်ခွင့် ပေးသည် (free routing)၊ ရွေးချယ်မှု B သည်
အဆင့်များကို workflow သို့မဟုတ် state machine အဖြစ် ရေးပြီး ကန့်သတ်ထားသည့် ဆုံးဖြတ်ချက်များကိုသာ
မော်ဒယ်ထံ ဖော်ထုတ်သည် (bounded routing)။ မှားယွင်းသည့် လုပ်ဆောင်ချက် တစ်ခု၏ ဆုံးရှုံးမှုသည်
USD 0.85 (ပြန်လည်ဖျက်သိမ်းခြင်း) နှင့် လူက ပြုပြင်ရပါက USD 48.00 ဖြစ်သည်။ A တွင် မှားယွင်းနှုန်း 4.0 %၊
B တွင် 0.8 % ဖြစ်သည်။ workflow ကို ရေးသွင်းရန် USD 300 / လ ကုန်သည်။

**trade-off —** A သည် အလုပ်အသစ်များအတွက် လိုက်လျောညီထွေ ဖြစ်သည်၊ သို့သော် မှားယွင်းမှု၏
သက်ရောက်နိုင်သည့် အတိုင်းအတာ ကြီးသည်။ B သည် လိုက်လျောညီထွေ မှု လျော့သော်လည်း ရလဒ်
ခန့်မှန်းနိုင်သည်။

**ဆုံးဖြတ်ချက် —** B ကို ရွေးရမည်၊ အကြောင်းမှာ လစဉ် အန္တရာယ် ကုန်ကျစရိတ်သည် USD 19,540.00 မှ
USD 3,908.00 သို့ ကျဆင်းသည်၊ workflow ရေးသွင်းခြင်း USD 300 ကို နုတ်ပြီးနောက် လစဉ်
USD 15,332.00 သက်သာသည်။ သို့သော် workflow သည် ကာလအလိုက် ပြောင်းလဲသည့် တာဝန်များအတွက်
free routing လမ်းကြောင်း တစ်ခုကို ချန်ထားရမည်။

**တိုင်းတာမည့် metric —** 1,000 request လျှင် မှားယွင်းနှုန်း၊ လစဉ် အန္တရာယ် USD၊ workflow
တွင် ပိတ်မိသည့် request အရေအတွက်။

```bash
python3 - <<'PY'
reqs, bad_cost, manual_cost = 10000, 0.85, 48.0
for label, rate in (("free routing", 0.04), ("bounded routing", 0.008)):
    bads = reqs * rate
    print(f"{label:16} bad actions {bads:7.1f} USD {bads * bad_cost:9.2f} manual repair USD {bads * manual_cost:9.2f}")
free = reqs * 0.04 * (bad_cost + manual_cost)
bound = reqs * 0.008 * (bad_cost + manual_cost)
print("monthly risk USD free        ", round(free, 2))
print("monthly risk USD bounded     ", round(bound, 2))
print("monthly saving USD           ", round(free - bound, 2))
print("workflow engine USD/month    ", 300.0)
print("net saving USD/month         ", round(free - bound - 300.0, 2))
PY
```

```text
free routing     bad actions   400.0 USD    340.00 manual repair USD  19200.00
bounded routing  bad actions    80.0 USD     68.00 manual repair USD   3840.00
monthly risk USD free         19540.0
monthly risk USD bounded      3908.0
monthly saving USD            15632.0
workflow engine USD/month     300.0
net saving USD/month          15332.0
```

### ဆုံးဖြတ်ချက် ၂ — Loop ကို အဆင့် မည်မျှအထိ ခွင့်ပြုမည်

**အခြေအနေ —** ထို assistant တွင် loop တစ်ခုအတွက် အဆင့် အများဆုံး (cap) ကို သတ်မှတ်ရမည်။
step တိုင်း၏ အောင်မြင်နိုင်ခြေ p = 0.45၊ step တစ်ခု၏ input သည် base 3,000 token မှ စ၍ 2,170 token
တိုးသည်၊ output 260 token၊ window ကျော်လွန်၍ မပြီးစီးသည့် run ကို လူက စစ်ဆေးရသည်။
လူ၏ စစ်ဆေးမှု ကုန်ကျစရိတ်ကို USD 48.00၊ USD 12.00 နှင့် USD 4.00 ဟူသည့် အခြေအနေ သုံးမျိုးဖြင့်
စမ်းသပ်ရမည်။

**trade-off —** cap တိုးပါက မပြီးစီးမှု လျော့သော်လည်း compute ကုန်ကျစရိတ် အချိုးမကျ တိုးသည်။
cap 6 တွင် compute USD 0.141975 ဖြစ်ပြီး cap 12 တွင် USD 0.479250 ဖြစ်သည်၊ ဆိုလိုသည်မှာ 3.38 ဆ
ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** cap ကို ဖော်မြူလာဖြင့် ရွေးရမည် — `total(cap) = compute(cap) + P_unfinished(cap) × escalation_cost`။
escalation USD 48.00 ဖြစ်ပါက cap 10 တွင် total အနည်းဆုံး ဖြစ်သည် (USD 0.466707)၊
USD 12.00 ဖြစ်ပါက cap 8 (USD 0.333181)၊ USD 4.00 ဖြစ်ပါက cap 7 (USD 0.245522) ဖြစ်သည်။
ထို့ကြောင့် **escalation cost ကို အရင် တိုင်းရမည်**၊ ထို့နောက်မှ cap ကို ဆုံးဖြတ်ရမည်။ ဖြစ်နိုင်ခြေ
မြင့်သည့် တာဝန်များအတွက် cap 6 ကို လည်း အသုံးပြုနိုင်သည်၊ အကြောင်းမှာ ၎င်းသည် compute ကို
67.6 % လျှော့ပေးသောကြောင့် ဖြစ်သည်။

**တိုင်းတာမည့် metric —** cap ရောက်၍ မပြီးစီးသည့် run အရေအတွက်၊ run တစ်ခုလျှင် ပျမ်းမျှ
step အရေအတွက်၊ run တစ်ခုလျှင် USD နှင့် escalation စစ်ဆေးမှု USD။

```bash
python3 - <<'PY'
base, growth, out_step = 3000, 2170, 260
p_done = 0.45
def cost(cap):
    tin = sum(base + growth * k for k in range(cap))
    return tin / 1e6 * 2.50 + cap * out_step / 1e6 * 10.00
for esc in (48.0, 12.0, 4.0):
    rows = []
    for cap in range(4, 13):
        c, pu = cost(cap), (1 - p_done) ** cap
        rows.append((cap, c, pu, c + pu * esc))
    best = min(rows, key=lambda r: r[3])
    print("escalation cost USD", esc)
    for cap, c, pu, tot in rows:
        mark = "  <-- min" if cap == best[0] else ""
        print(f"  cap {cap:2} compute USD {c:.6f} P_unfinished {pu:.6f} total USD {tot:.6f}{mark}")
PY
```

```text
escalation cost USD 48.0
  cap  4 compute USD 0.072950 P_unfinished 0.091506 total USD 4.465250
  cap  5 compute USD 0.104750 P_unfinished 0.050328 total USD 2.520515
  cap  6 compute USD 0.141975 P_unfinished 0.027681 total USD 1.470646
  cap  7 compute USD 0.184625 P_unfinished 0.015224 total USD 0.915394
  cap  8 compute USD 0.232700 P_unfinished 0.008373 total USD 0.634623
  cap  9 compute USD 0.286200 P_unfinished 0.004605 total USD 0.507258
  cap 10 compute USD 0.345125 P_unfinished 0.002533 total USD 0.466707  <-- min
  cap 11 compute USD 0.409475 P_unfinished 0.001393 total USD 0.476345
  cap 12 compute USD 0.479250 P_unfinished 0.000766 total USD 0.516028
escalation cost USD 12.0
  cap  4 compute USD 0.072950 P_unfinished 0.091506 total USD 1.171025
  cap  5 compute USD 0.104750 P_unfinished 0.050328 total USD 0.708691
  cap  6 compute USD 0.141975 P_unfinished 0.027681 total USD 0.474143
  cap  7 compute USD 0.184625 P_unfinished 0.015224 total USD 0.367317
  cap  8 compute USD 0.232700 P_unfinished 0.008373 total USD 0.333181  <-- min
  cap  9 compute USD 0.286200 P_unfinished 0.004605 total USD 0.341464
  cap 10 compute USD 0.345125 P_unfinished 0.002533 total USD 0.375520
  cap 11 compute USD 0.409475 P_unfinished 0.001393 total USD 0.426192
  cap 12 compute USD 0.479250 P_unfinished 0.000766 total USD 0.488445
escalation cost USD 4.0
  cap  4 compute USD 0.072950 P_unfinished 0.091506 total USD 0.438975
  cap  5 compute USD 0.104750 P_unfinished 0.050328 total USD 0.306064
  cap  6 compute USD 0.141975 P_unfinished 0.027681 total USD 0.252698
  cap  7 compute USD 0.184625 P_unfinished 0.015224 total USD 0.245522  <-- min
  cap  8 compute USD 0.232700 P_unfinished 0.008373 total USD 0.266194
  cap  9 compute USD 0.286200 P_unfinished 0.004605 total USD 0.304621
  cap 10 compute USD 0.345125 P_unfinished 0.002533 total USD 0.355257
  cap 11 compute USD 0.409475 P_unfinished 0.001393 total USD 0.415047
  cap 12 compute USD 0.479250 P_unfinished 0.000766 total USD 0.482315
```

## ၅။ အဖြေများ (Answers with Explanations)

### ၅.၁ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း အဖြေများ

#### အဖြေ ၁ — Tool schema ကို turn တိုင်း ပို့ခြင်း

**ဖော်မြူလာ —** schema token = အက္ခရာ အရေအတွက် / အက္ခရာ တစ်ခုလျှင် token အရေအတွက်။
ယူဆချက် — အက္ခရာ 4 ခုလျှင် token 1 ခု၊ schema သည် ပြောင်းလဲခြင်း မရှိဘဲ turn တိုင်း ပြန်ပို့သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. schema token = 9,200 / 4 = 2,300 token ဖြစ်သည်။
2. turn 12 ခုအတွင်း = 2,300 × 12 = 27,600 token ဖြစ်သည်။
3. USD = 27,600 × 2.50 / 10⁶ = USD 0.0690 ဖြစ်သည်။
4. 3,000 token prefix ထဲတွင် schema ၏ ရာခိုင်နှုန်း = 2,300 / 3,000 = 76.7 % ဖြစ်သည်။
5. turn 200 ဖြစ်ပါက USD = 2300 × 200 × 2.50 / 10⁶ = USD 1.15 ဖြစ်သည်။

**အဓိပ္ပာယ် —** tool schema သည် request တစ်ခုလျှင် 2,300 token ကို အမြဲ ကျခံစေပြီး ၎င်းသည်
prefix ၏ 76.7 % ဖြစ်သည်။ ထို့ကြောင့် tool အရေအတွက် လျှော့ချခြင်းနှင့် schema ကို တည်ငြိမ်အောင်
ထားခြင်း (cache အတွက်) သည် loop ၏ ကုန်ကျစရိတ်အပေါ် တိုက်ရိုက် သက်ရောက်သည်။

```bash
python3 - <<'PY'
schema_chars, chars_per_token = 9200, 4
schema_tok = schema_chars // chars_per_token
turns, in_price = 12, 2.50
print("schema characters             ", schema_chars)
print("schema tokens                 ", schema_tok)
print("schema tokens over 12 turns   ", schema_tok * turns)
print("USD for schema over 12 turns  ", round(schema_tok * turns / 1e6 * in_price, 6))
print("share of a 3,000 token prefix pct", round(100 * schema_tok / 3000, 1))
print("USD if sent 200 turns         ", round(schema_tok * 200 / 1e6 * in_price, 4))
PY
```

```text
schema characters              9200
schema tokens                  2300
schema tokens over 12 turns    27600
USD for schema over 12 turns   0.069
share of a 3,000 token prefix pct 76.7
USD if sent 200 turns          1.15
```

#### အဖြေ ၂ — Tool result အရွယ်အစားနှင့် context ကြီးထွားမှု

**ဖော်မြူလာ —** context(n) = base + growth × n၊ base = system + schema၊ growth = tool result +
reply + action၊ စုစုပေါင်း input = ∑ context(k), k = 0 … n − 1။ ယူဆချက် — tool result သည် ပြောင်းလဲခြင်း
မရှိဘဲ turn တိုင်း ထပ်တူ ထည့်သည်၊ context ကို turn တိုင်း အစမှ ပြန်ပို့သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. base = 700 + 2,300 = 3,000 token ဖြစ်သည်။
2. growth = 1,800 + 250 + 120 = 2,170 token ဖြစ်သည်။
3. context(n) = 3,000 + 2,170n ဖြစ်သည်၊ ထို့ကြောင့် turn 1 = 5,170၊ turn 5 = 13,850၊ turn 10 = 24,700 ဖြစ်သည်။
4. စုစုပေါင်း input (turn 10) = 10 × 3,000 + 2,170 × 45 = 30,000 + 97,650 = 127,650 token ဖြစ်သည်၊
   USD 0.319125 ဖြစ်သည်။
5. window 12,000 token ကို ကျော်လွန်သည့် ပထမဆုံး turn = 5 ဖြစ်သည် (turn 4 = 11,680၊ turn 5 = 13,850)။
6. tool result ကို 400 token သို့ ကန့်သတ်ပါက turn တစ်ခုလျှင် = 3,000 + 400 + 250 + 120 = 3,770 token
   ဖြစ်သည်၊ turn 10 အတွက် စုစုပေါင်း = 37,700 token ဖြစ်သည်၊ သက်သာမှု = 70.5 % ဖြစ်သည်။

**အဓိပ္ပာယ် —** စုစုပေါင်း input သည် turn အရေအတွက်နှင့်အတူ **quadratic** နီးပါး တိုးသည်၊
အကြောင်းမှာ turn တိုင်းသည် ယခင် context အားလုံးကို ပြန်ပို့သောကြောင့် ဖြစ်သည်။ တိုးနှုန်းကို
ထိန်းသည့် တစ်ခုတည်းသော လီဗာ မှာ **turn တစ်ခုလျှင် ထည့်သည့် token** ဖြစ်သည်၊ ထို့ကြောင့် tool result ကို
ကန့်သတ်ခြင်းသည် context window ကို ကယ်ရုံသာမက စုစုပေါင်း ကုန်ကျစရိတ်ကို အချိုးအစား လျှော့ပေးသည်။

```bash
python3 - <<'PY'
system, schema_tok = 700, 2300
result_tok, reply_tok, action_tok = 1800, 250, 120
base, growth = system + schema_tok, result_tok + reply_tok + action_tok
print("system prompt tokens          ", system)
print("base prefix tokens            ", base)
print("per-turn growth tokens        ", growth)
for n in range(1, 11):
    print(f"  turn {n:2} context {base + growth * n:7}")
cum = sum(base + growth * k for k in range(10))
print("cumulative input over 10 turns", cum)
print("USD cumulative 10 turns       ", round(cum / 1e6 * 2.50, 6))
window = 12000
print("window tokens                 ", window)
print("first turn exceeding window   ", min(n for n in range(1, 100) if base + growth * n > window))
trimmed = 400
cum_trim = (base + trimmed + reply_tok + action_tok) * 10
print("with 400-token truncated result cumulative", cum_trim)
print("saving pct                    ", round(100 * (cum - cum_trim) / cum, 1))
PY
```

```text
system prompt tokens           700
base prefix tokens             3000
per-turn growth tokens         2170
  turn  1 context    5170
  turn  2 context    7340
  turn  3 context    9510
  turn  4 context   11680
  turn  5 context   13850
  turn  6 context   16020
  turn  7 context   18190
  turn  8 context   20360
  turn  9 context   22530
  turn 10 context   24700
cumulative input over 10 turns 127650
USD cumulative 10 turns        0.319125
window tokens                  12000
first turn exceeding window    5
with 400-token truncated result cumulative 37700
saving pct                     70.5
```

#### အဖြေ ၃ — တာဝန် တစ်ခုအတွက် step အရေအတွက်နှင့် ကုန်ကျစရိတ်

**ဖော်မြူလာ —** input USD = ∑ input × price_in၊ output USD = ∑ output × price_out။ ယူဆချက် —
step တိုင်း တစ် ကြိမ် သာ run သည်၊ tool execution အချိန်ကို မထည့်သွင်းပါ၊ retry မရှိပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. step အရေအတွက် = 6 ဖြစ်သည်။
2. input စုစုပေါင်း = 4,200 + 5,100 + 6,000 + 7,400 + 8,600 + 9,100 = 40,400 token ဖြစ်သည်။
3. output စုစုပေါင်း = 180 + 240 + 320 + 900 + 260 + 420 = 2,320 token ဖြစ်သည်။
4. input USD = 40,400 × 2.50 / 10⁶ = USD 0.1010 ဖြစ်သည်။
5. output USD = 2,320 × 10.00 / 10⁶ = USD 0.0232 ဖြစ်သည်။
6. စုစုပေါင်း = USD 0.1242 ဖြစ်သည်။
7. step 5 ကို တစ်ကြိမ် ပြန်ကြိုးစားပါက ထပ်ကုန်သည့် USD = 8,600 × 2.50 / 10⁶ + 260 × 10.00 / 10⁶ = USD 0.0241
   ဖြစ်သည်၊ စုစုပေါင်း USD 0.1483 ဖြစ်သည်၊ တိုးလာမှု = 19.4 % ဖြစ်သည်။

**အဓိပ္ပာယ် —** input အပိုင်းသည် USD 0.1010 ဖြစ်၍ စုစုပေါင်း၏ 81.3 % ဖြစ်သည်။ ထို့ကြောင့် tool အရေအတွက်နှင့်
context အရွယ်အစားသည် step အရေအတွက်ထက် ကုန်ကျစရိတ်ကို ပို၍ ဆုံးဖြတ်သည်။ retry တစ်ကြိမ်သည်
step အရေအတွက် တစ်ခုခန့် ကုန်ကျသဖြင့် retry များခြင်းသည် ကုန်ကျစရိတ်ကို လျင်မြန်စွာ တိုးစေသည်။

```bash
python3 - <<'PY'
steps = [("read issue", 4200, 180), ("read file", 5100, 240), ("run tests", 6000, 320),
         ("write patch", 7400, 900), ("run tests again", 8600, 260), ("open PR", 9100, 420)]
tin, tout = sum(s[1] for s in steps), sum(s[2] for s in steps)
for name, i, o in steps:
    print(f"  {name:16} in {i:6} out {o:5}")
print("steps                         ", len(steps))
print("input tokens total            ", tin)
print("output tokens total           ", tout)
print("USD total                     ", round(tin / 1e6 * 2.50 + tout / 1e6 * 10.00, 6))
print("USD input part                ", round(tin / 1e6 * 2.50, 6))
print("USD output part               ", round(tout / 1e6 * 10.00, 6))
retry = 8600 / 1e6 * 2.50 + 260 / 1e6 * 10.00
print("one retry of step 5 USD       ", round(retry, 6))
total = tin / 1e6 * 2.50 + tout / 1e6 * 10.00
print("USD total with one retry      ", round(total + retry, 6))
print("retry premium pct             ", round(100 * retry / total, 1))
PY
```

```text
  read issue       in   4200 out   180
  read file        in   5100 out   240
  run tests        in   6000 out   320
  write patch      in   7400 out   900
  run tests again  in   8600 out   260
  open PR          in   9100 out   420
steps                          6
input tokens total             40400
output tokens total            2320
USD total                      0.1242
USD input part                 0.101
USD output part                0.0232
one retry of step 5 USD        0.0241
USD total with one retry       0.1483
retry premium pct              19.4
```

#### အဖြေ ၄ — Retry policy ၏ မျှော်မှန်း attempt နှင့် ကုန်ကျစရိတ်

**ဖော်မြူလာ —** E[attempts] = ∑ (1 − p)^k, k = 0 … max − 1။ escalation ဖြစ်နိုင်ခြေ = (1 − p)^max။
မျှော်မှန်း USD = E[attempts] × attempt_cost။ ယူဆချက် — attempt တိုင်း၏ အောင်မြင်နိုင်ခြေ
တူညီသည်၊ failure များသည် သီးခြားစီ ဖြစ်သည် (independent)။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. max 1: E = 1.0000၊ USD 0.004500၊ escalation 30.00 % ဖြစ်သည်။
2. max 2: E = 1 + 0.30 = 1.3000၊ USD 0.005850၊ escalation 9.00 % ဖြစ်သည်။
3. max 3: E = 1 + 0.30 + 0.09 = 1.3900၊ USD 0.006255၊ escalation 2.70 % ဖြစ်သည်။
4. max 4: E = 1.4170၊ USD 0.006376၊ escalation 0.81 % ဖြစ်သည်။
5. max 5: E = 1.4251၊ USD 0.006413၊ escalation 0.24 % ဖြစ်သည်။
6. attempt 3 မှ 4 သို့ တိုးခြင်း၏ အကျိုးအမြတ် = USD 0.000121 ဖြစ်သည်၊ escalation သည်
   1.89 ရာခိုင်နှုန်းအမှတ် ကျဆင်းသည်။
7. request 10,000 ခုအတွက် (max 3) = USD 62.55 ဖြစ်သည်။

**အဓိပ္ပာယ် —** attempt အရေအတွက်သည် **logarithmically** အကျိုးအမြတ် လျော့သည် — attempt 3 သည်
escalation ကို 30 % မှ 2.7 % သို့ လျှော့ပေးသည်၊ သို့သော် attempt 5 သည် ထပ်လျှော့သည့် ပမာဏ
အလွန်နည်းသည်။ သို့သော် escalation တစ်ခု၏ ကုန်ကျစရိတ် (လူ၏ အချိန်) သည် attempt တစ်ခု၏
ကုန်ကျစရိတ်ထက် များစွာ ကြီးသဖြင့် escalation ဖြစ်နိုင်ခြေနှင့် ၎င်း၏ ကုန်ကျစရိတ်ကို ထည့်တွက်ရမည်။

```bash
python3 - <<'PY'
p, attempt_cost = 0.70, 0.0045
for mx in (1, 2, 3, 4, 5):
    e = sum((1 - p) ** k for k in range(mx))
    print(f"max {mx}: expected attempts {e:.4f} expected USD {e * attempt_cost:.6f} "
          f"escalation pct {100 * (1 - p) ** mx:.2f}")
base_e = sum((1 - p) ** k for k in range(3))
print("3-attempt expected USD        ", round(base_e * attempt_cost, 6))
print("versus single attempt USD     ", round(attempt_cost, 6))
print("USD per 10,000 requests       ", round(base_e * attempt_cost * 10000, 4))
e4 = sum((1 - p) ** k for k in range(4))
print("marginal 4th attempt USD gain ", round((e4 - base_e) * attempt_cost, 6))
print("escalation drop 3 -> 4 pct pt ", round(100 * ((1 - p) ** 3 - (1 - p) ** 4), 3))
PY
```

```text
max 1: expected attempts 1.0000 expected USD 0.004500 escalation pct 30.00
max 2: expected attempts 1.3000 expected USD 0.005850 escalation pct 9.00
max 3: expected attempts 1.3900 expected USD 0.006255 escalation pct 2.70
max 4: expected attempts 1.4170 expected USD 0.006376 escalation pct 0.81
max 5: expected attempts 1.4251 expected USD 0.006413 escalation pct 0.24
3-attempt expected USD         0.006255
versus single attempt USD      0.0045
USD per 10,000 requests        62.55
marginal 4th attempt USD gain  0.000121
escalation drop 3 -> 4 pct pt  1.89
```

#### အဖြေ ၅ — Loop ၏ latency

**ဖော်မြူလာ —** serial = steps × model_ms + (steps − 1) × tool_ms။ tool call များကို တစ်ပြိုင်နက်
ဆောင်ရွက်ပါက သက်သာမှု = (parallel − 1) × tool_ms။ ယူဆချက် — tool call တိုင်း၏ အချိန် တူညီသည်၊
တစ်ပြိုင်နက် လုပ်ရန် မှီခိုမှု မရှိပါ၊ နောက်ဆုံး step တွင် tool မခေါ်ပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. model အချိန် = 6 × 900 = 5,400 ms ဖြစ်သည်။
2. tool အချိန် = 5 × 250 = 1,250 ms ဖြစ်သည်။
3. စုစုပေါင်း = 6,650 ms = 6.65 s ဖြစ်သည်။
4. tool call သုံးခုကို တစ်ပြိုင်နက် ဆောင်ရွက်ပါက သက်သာမှု = 2 × 250 = 500 ms ဖြစ်သည်၊
   ပြောင်းလဲသည့် စုစုပေါင်း = 6,150 ms ဖြစ်သည်၊ သက်သာမှု = 7.5 % ဖြစ်သည်။
5. မော်ဒယ် call သည် 20 % ကြာလာပါက စုစုပေါင်း = 7,730.0 ms ဖြစ်သည်၊ ဆိုလိုသည်မှာ 16.2 % တိုးသည်။
6. tool အပိုင်း၏ latency ရှယ် = 1,250 / 6,650 = 18.8 % ဖြစ်သည်။

**အဓိပ္ပာယ် —** loop ၏ latency တွင် 81.2 % သည် မော်ဒယ် call ဖြစ်သည်။ ထို့ကြောင့် tool parallelism
သည် အနည်းငယ်သာ ကူညီသည်၊ latency ကို တကယ် လျှော့လိုပါက step အရေအတွက် (မော်ဒယ် call
အရေအတွက်) ကို လျှော့ရမည် — ဥပမာ တစ်ကြိမ် တည်းတွင် tool သုံးခုကို parallel ခေါ်ပါက မော်ဒယ်
call နှစ်ခု လျော့သည်။

```bash
python3 - <<'PY'
model_ms, tool_ms, n_steps = 900, 250, 6
serial = n_steps * model_ms + (n_steps - 1) * tool_ms
print("model steps                   ", n_steps)
print("tool calls between steps      ", n_steps - 1)
print("model time ms                 ", n_steps * model_ms)
print("tool time ms                  ", (n_steps - 1) * tool_ms)
print("serial total ms               ", serial)
print("serial total s                ", round(serial / 1000, 2))
parallel_tools, saved = 3, 2 * 250
print("parallel tool calls           ", parallel_tools)
print("ms saved by parallel tools    ", saved)
print("ms with parallel tools        ", serial - saved)
print("saving pct                    ", round(100 * saved / serial, 1))
print("if model call grows 20 pct ms ", round(n_steps * model_ms * 1.2 + (n_steps - 1) * tool_ms, 1))
print("tool share of latency pct     ", round(100 * (n_steps - 1) * tool_ms / serial, 1))
PY
```

```text
model steps                    6
tool calls between steps       5
model time ms                  5400
tool time ms                   1250
serial total ms                6650
serial total s                 6.65
parallel tool calls            3
ms saved by parallel tools     500
ms with parallel tools         6150
saving pct                     7.5
if model call grows 20 pct ms  7730.0
tool share of latency pct      18.8
```

#### အဖြေ ၆ — Schema prefix တည်ငြိမ်သည့်အခါ cache ၏ အလျော့အကျ

**ဖော်မြူလာ —** cache မပါသည့် USD = prefix × turns × price_in။ cache ပါသည့် USD =
prefix × write_mult × price_in + prefix × (turns − 1) × read_mult × price_in။ ယူဆချက် — prefix သည်
turn တိုင်း တိကျစွာ တူညီသည် (byte တူညီသည်)၊ cache သည် turn 2 မှ စ၍ ထိသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. cache မပါဘဲ ကျခံရသည့် token = 3,000 × 12 = 36,000 ဖြစ်သည်၊ USD 0.0900 ဖြစ်သည်။
2. cache ရေးသွင်းခြင်း (turn 1) = 3,000 × 1.25 × 2.50 / 10⁶ = USD 0.009375 ဖြစ်သည်။
3. cache ပြန်ဖတ်ခြင်း (turn 2–12) = 3,000 × 11 × 0.10 × 2.50 / 10⁶ = USD 0.008250 ဖြစ်သည်။
4. cache ပါသည့် စုစုပေါင်း = USD 0.017625 ဖြစ်သည်၊ သက်သာမှု = USD 0.072375 = 80.4 % ဖြစ်သည်။
5. cache မပါသည့် ကုန်ကျစရိတ်သည် cache ပါသည့် ကုန်ကျစရိတ်၏ 5.11 ဆ ဖြစ်သည်။

**အဓိပ္ပာယ် —** cache ၏ အကျိုးအမြတ်သည် prefix ၏ **တည်ငြိမ်မှု** အပေါ် လုံးလုံး မှီခိုသည်။
prompt ၏ အစတွင် timestamp၊ request id သို့မဟုတ် session id ကို ထည့်ပါက prefix သည် turn တိုင်း
ပြောင်းသွားပြီး cache သည် မထိပါ — ထိုအခါ ကုန်ကျစရိတ်သည် 5.11 ဆ ပြန်တက်သည်။ ထို့ကြောင့်
cache ကို ရည်ရွယ်ပါက **ပြောင်းလဲသည့် အပိုင်းများကို prompt ၏ အဆုံးတွင်သာ** ထားရမည်။

```bash
python3 - <<'PY'
prefix, turns = 3000, 12
write_mult, read_mult = 1.25, 0.10
nocache = prefix * turns / 1e6 * 2.50
first = prefix * write_mult / 1e6 * 2.50
reads = prefix * (turns - 1) * read_mult / 1e6 * 2.50
print("stable prefix tokens          ", prefix)
print("turns                         ", turns)
print("no cache tokens billed        ", prefix * turns)
print("no cache USD                  ", round(nocache, 6))
print("cache write USD (turn 1)      ", round(first, 6))
print("cache read USD (turns 2-12)   ", round(reads, 6))
print("cached USD                    ", round(first + reads, 6))
print("saving USD                    ", round(nocache - first - reads, 6))
print("saving pct                    ", round(100 * (nocache - first - reads) / nocache, 1))
print("cost multiple without cache   ", round(nocache / (first + reads), 2))
PY
```

```text
stable prefix tokens           3000
turns                          12
no cache tokens billed         36000
no cache USD                   0.09
cache write USD (turn 1)       0.009375
cache read USD (turns 2-12)    0.00825
cached USD                     0.017625
saving USD                     0.072375
saving pct                     80.4
cost multiple without cache    5.11
```

### ၅.၂ ပြဿနာ ရှာဖွေခြင်း အဖြေများ

#### အဖြေ ၁ — Loop ဘယ်တော့မှ မဆုံးခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** loop တစ်ခုသည် "ဆက်လုပ်ရမည် သို့မဟုတ် ရပ်ရမည်" ဟူသည့်
ဆုံးဖြတ်ချက်ကို ပြင်ပမှ ရရှိရမည်။ ထို ဆုံးဖြတ်ချက် မရှိပါက မော်ဒယ်သည် အလုပ်ပြီးသည်ဟု မည်သည့်အခါမျှ
သေချာစွာ မဆိုနိုင်သဖြင့် နောက် tool call ကို ဆက်တောင်းသည်။ အဆင့် တစ်ခုလျှင် output 260 token
သာ ဖြစ်သော်လည်း step တိုင်း၏ input သည် base 3,000 token မှ စ၍ 2,170 token တိုးသဖြင့်
step 12 တွင် input တစ်ခုတည်းမှာ 26,870 token ရောက်သည်။ ထို့ကြောင့် မရပ်ခြင်းသည်
**စဉ်ဆက်မပြတ် တိုးနေသည့် ကုန်ကျစရိတ်** အဖြစ် ပြောင်းလဲသည်၊ မြင့်မားသည့် တစ်ကြိမ်တည်း
ကုန်ကျစရိတ် မဟုတ်ပါ။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** ဦးစွာ အောင်မြင်မှု အထောက်အထား သတ်မှတ်ထားခြင်း ရှိမရှိ စစ်ပါ။
မရှိပါက အကြောင်းရင်း (၁) ဖြစ်သည်၊ ဤ အခြေအနေသည် အဖြစ်အများဆုံး ဖြစ်သည်။ ထို့နောက် step
အများဆုံး သတ်မှတ်ချက် ရှိမရှိ စစ်ပါ (အကြောင်းရင်း ၂)။ တူညီသည့် tool call ဘယ်နှစ်ကြိမ်
ထပ်ဖြစ်သည်ကို ရေတွက်ပါ — သုံးကြိမ် ကျော်ပါက အကြောင်းရင်း (၄) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** သတ်မှတ်ချက်များကို ထည့်ပြီးနောက် ပျမ်းမျှ step အရေအတွက်ကို
တိုင်းပါ။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း ၂ ၏ ရလဒ်အတိုင်း အောင်မြင်နိုင်ခြေ p = 0.45 ဖြစ်ပါက
cap 10 တွင် မပြီးစီးနိုင်ခြေ 0.2533 % သို့ ကျဆင်းသည်၊ ထို့ကြောင့် ဖြေရှင်းနည်းသည် အလုပ်ဖြစ်သည်။
မပြီးစီးမှုနှုန်း ကျဆင်းခြင်း မရှိပါက ဆုံးဖြတ်ချက် စည်းမျဉ်းကိုယ်တိုင် မှားနေသည်။

#### အဖြေ ၂ — Tool က ငြင်းပယ်သည့် argument များ

**အကြောင်းရင်း ရှင်းလင်းချက် —** `Function Calling` တွင် မော်ဒယ်သည် ဖွဲ့စည်းထားသည့် တောင်းဆိုမှုကို
ထုတ်လွှတ်သည်၊ သို့သော် **မည်သည့် တန်ဖိုး လက်ခံနိုင်သည်** ကို မော်ဒယ် မသိနိုင်ပါ — schema
နှင့် description တွင် ဖော်ပြထားသည့် အချက်ကိုသာ သိသည်။ `Tool Contract` သည် schema တွင်
မပါသည့် စစ်ဆေးချက်များ (allowed root၊ base revision၊ maximum size) ကို ထပ်ထည့်ထားပါက
မော်ဒယ်သည် ထို အချက်များကို ခန့်မှန်းရသဖြင့် ငြင်းပယ်ခံရသည်။ ငြင်းပယ်ခံရသည့် request တစ်ခုလျှင်
USD 0.0215 ထပ်ကုန်သည် (ဥပမာ ၂)၊ ငြင်းပယ်နှုန်း 8 % ဖြစ်ပါက request 1,000 လျှင် USD 1.72 ဖြစ်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** ငြင်းပယ်ခံရသည့် tool call များကို layer အလိုက် ခွဲပါ။ အဆင့် ၁ (schema) တွင်
ငြင်းခံရပါက အကြောင်းရင်း (၃) ဖြစ်သည် — ကန့်သတ်ချက်ကို schema ထဲ မထည့်ထားပါ။ အဆင့် ၂
(semantic) တွင် ငြင်းခံရပါက အကြောင်းရင်း (၁) ဖြစ်သည် — မော်ဒယ် မမြင်နိုင်သည့် စစ်ဆေးချက် ရှိသည်။
မော်ဒယ် ပြန်လည်ပေးအပ်သည့် အဖြေကို ကြည့်ပါ — error message မှ မှန်ကန်အောင် ပြင်နိုင်ခြင်း မရှိပါက
အကြောင်းရင်း (၂) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** contract ၏ စစ်ဆေးချက်များကို schema ထဲ ရောင်ပြန်ဟပ်ပြီးနောက်
ငြင်းပယ်နှုန်းကို ပြန်တိုင်းပါ။ ငြင်းပယ်နှုန်း 8 % မှ 2 % အောက်သို့ ကျဆင်းပါက အကြောင်းရင်း (၁)
ဖြစ်ကြောင်း အတည်ပြုသည်။ မကျဆင်းပါက မော်ဒယ်သည် tool ကို မှားရွေးနေသည် (အကြောင်းရင်း ၄)
ဖြစ်သဖြင့် tool အမည်နှင့် description များကို ခွဲခြားနိုင်အောင် ပြန်ရေးရမည်။

#### အဖြေ ၃ — Cost သည် turn တိုင်း ကြီးထွားခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** အပိုင်း ၅.၁ အဖြေ ၂ တွင် တွက်ချက်ထားသည့်အတိုင်း context(n) = base +
growth × n ဖြစ်သည်၊ ထို့ကြောင့် စုစုပေါင်း input သည် ∑ context(k) = n × base + growth × n(n − 1)/2
ဖြစ်သည်၊ ဆိုလိုသည်မှာ **quadratic** ဖြစ်သည်။ turn 10 တွင် စုစုပေါင်း 127,650 token ဖြစ်သော်လည်း
turn 10 တစ်ခုတည်း၏ context သည် 24,700 token သာ ဖြစ်သည် — ထို့ကြောင့် ကုန်ကျစရိတ် ကြီးထွားခြင်း၏
အရင်းအမြစ်သည် **turn အရေအတွက်** ဖြစ်ပြီး၊ turn တစ်ခုလျှင် ထည့်သည့် token များ စုပုံခြင်း ဖြစ်သည်။
ဥပမာ ၃ တွင် ပြထားသည့်အတိုင်း state ဖြင့် တိုချုံ့ပါက စုစုပေါင်း သည် 48.0 % ကျဆင်းသည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** turn အလိုက် input token ကို ဆွဲပါ။ တိုးနှုန်းသည် ကိန်းသေ ဖြစ်ပါက
အကြောင်းရင်း (၁) ဖြစ်သည်။ တိုးနှုန်းတွင် tool result တစ်ခုတည်းက လွှမ်းမိုးပါက အကြောင်းရင်း (၂) ဖြစ်သည်။
cache hit rate သည် သုည ဖြစ်နေပါက အကြောင်းရင်း (၄) ဖြစ်သည်၊ ဤ အခြေအနေကို အပိုင်း ၅.၁ အဖြေ ၆ တွင်
တိုင်းထားသည် (cache မရှိပါက 5.11 ဆ ပိုကုန်သည်)။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** `Agent State` ကို အခြေခံအဖြစ် ထားပြီးနောက် turn တိုင်း၏ input
သည် ကိန်းသေ ဖြစ်လာသည် (ဥပမာ ၃ တွင် 7,760 token)။ ထိုအခါ စုစုပေါင်း input သည် n နှင့်
**linear** ဖြစ်လာသည်၊ ဆိုလိုသည်မှာ ပြဿနာ ပြီးဆုံးသည်။ ပြင်ဆင်ပြီးနောက် turn အလိုက် USD ကို
ပြန်တိုင်း၍ တိုးနှုန်း ကိန်းသေ ဖြစ်ခြင်းကို အတည်ပြုရမည်။

### ၅.၃ ဆုံးဖြတ်ချက် အဖြေများ

#### အဖြေ ၁ — Routing autonomy နှင့် တိကျသည့် workflow

**ရှင်းလင်းချက် —** ကုန်ကျစရိတ် နှစ်မျိုး ရှိသည် — compute ကုန်ကျစရိတ် (အနည်းငယ်) နှင့်
မှားယွင်းသည့် လုပ်ဆောင်ချက်၏ ကုန်ကျစရိတ် (ကြီးမား)။ free routing တွင် request 10,000 ခုအနက် 400 ခု
မှားသည်၊ လစဉ် အန္တရာယ် USD 19,540.00 ဖြစ်သည်။ bounded routing တွင် 80 ခု မှားသည်၊
USD 3,908.00 ဖြစ်သည်။ ကွာခြားချက်မှာ USD 15,632.00 ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** workflow သို့မဟုတ် state machine ဖြင့် တည်ငြိမ်သည့် အဆင့်များကို ရေးသွင်းပြီး
ကန့်သတ်ထားသည့် ဆုံးဖြတ်ချက်များကိုသာ မော်ဒယ်ထံ ဖော်ထုတ်ရမည်။ workflow ရေးသွင်းခြင်း
USD 300 ကို နုတ်ပြီးနောက် လစဉ် USD 15,332.00 သက်သာသည်။ `Orchestration` သည် autonomy
နှင့် တူညီသည် မဟုတ်ပါ — agent တစ်ခုတည်းကို workflow ဖြင့် orchestrate လုပ်နိုင်သည်။
သို့သော် တာဝန် အသစ်များအတွက် free routing လမ်းကြောင်း တစ်ခုကို ချန်ထားရမည်၊ မချန်ထားပါက
workflow သည် လျင်မြန်စွာ ခေတ်နောက်ကျသည်။

**တိုင်းတာမည့် metric —** request 1,000 လျှင် မှားယွင်းသည့် လုပ်ဆောင်ချက် အရေအတွက်၊
လစဉ် အန္တရာယ် USD၊ workflow တွင် ပိတ်မိ၍ လူက လွှတ်ရသည့် request အရေအတွက်။

#### အဖြေ ၂ — Loop cap ရွေးချယ်ခြင်း

**ရှင်းလင်းချက် —** cap တိုးခြင်း၏ အကျိုးအမြတ်သည် **exponentially** လျော့သည်၊ ကုန်ကျစရိတ်သည်
**linearly** တိုးသည်။ ထို့ကြောင့် အနည်းဆုံး ကုန်ကျစရိတ်သည် ကန့်သတ်ထားသည့် တစ်နေရာတွင် ရှိသည်။
escalation USD 48.00 ဖြစ်ပါက cap 10 (total USD 0.466707)၊ USD 12.00 ဖြစ်ပါက cap 8
(USD 0.333181)၊ USD 4.00 ဖြစ်ပါက cap 7 (USD 0.245522) ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** cap ကို ကိန်းဂဏန်းဖြင့် ဆုံးဖြတ်ရမည်၊ ခံစားချက်ဖြင့် မဟုတ်ပါ။ escalation
ကုန်ကျစရိတ်သည် cap ကို အဓိက ရွှေ့ပေးသည့် ကိန်းသေ ဖြစ်သဖြင့် ထို တန်ဖိုးကို အရင် တိုင်းရမည်။
ဖြစ်နိုင်ခြေ မြင့်သည့် တာဝန်များအတွက် cap 6 သည် compute ကို 67.6 % လျှော့ပေးသော်လည်း
မပြီးစီးနိုင်ခြေသည် 2.77 % ရှိသဖြင့် escalation စရိတ် မြင့်ပါက မသင့်လျော်ပါ။

**တိုင်းတာမည့် metric —** cap ရောက်၍ မပြီးစီးသည့် run အရေအတွက်၊ run တစ်ခုလျှင် ပျမ်းမျှ
step အရေအတွက်၊ run တစ်ခုလျှင် USD၊ escalation စစ်ဆေးမှု USD။

## Self-check

၁။ အပိုင်း ၁ ဥပမာ ၁ တွင် loop ၏ ကုန်ကျစရိတ် တိုးလာမှုသည် အဓိကအားဖြင့် input မှ လာသလော၊
output မှ လာသလော။

၂။ အပိုင်း ၅.၁ အဖြေ ၂ တွင် စုစုပေါင်း input သည် turn အရေအတွက်နှင့်အတူ မည်သည့် ပုံစံဖြင့်
တိုးသည်၊ အကြောင်းရင်း က ဘာလဲ။

၃။ အပိုင်း ၅.၁ အဖြေ ၄ တွင် escalation ဖြစ်နိုင်ခြေသည် attempt အရေအတွက် တိုးသည့်အခါ
မည်သို့ ပြောင်းလဲသည်။

၄။ အပိုင်း ၅.၁ အဖြေ ၆ တွင် cache ၏ အကျိုးအမြတ်သည် မည်သည့် အချက်အပေါ် မှီခိုသည်။

၅။ ဆုံးဖြတ်ချက် ၂ တွင် cap ကို ဆုံးဖြတ်သည့် ဖော်မြူလာ နှင့် escalation ကုန်ကျစရိတ် ကွာခြားသည့်အခါ
cap ပြောင်းလဲပုံကို ဖော်ပြပါ။

<details>
<summary>အဖြေများ</summary>

၁။ input မှ လာသည်။ call တစ်ခု၏ USD သည် 0.01515 ဖြစ်ပြီး loop ၏ USD သည် 0.141975 ဖြစ်သည်၊
ထို့ကြောင့် premium သည် 0.126825 ဖြစ်သည်။ ထို premium ၏ အများစုသည် step တိုင်း context
အားလုံးကို ပြန်ပို့ရခြင်းမှ လာသည့် input token ဖြစ်သည်။ output သည် step ခြောက်ခုအတွက် 1,560 token
သာ ဖြစ်သည်။

၂။ ∑ context(k) = n × base + growth × n(n − 1) / 2 ဖြစ်သဖြင့် quadratic ဖြစ်သည်။ အကြောင်းရင်းမှာ
turn တိုင်းသည် ယခင် context အားလုံးကို အစမှ ပြန်ပို့သောကြောင့် ဖြစ်သည်။

၃။ (1 − p)^max ဖြစ်သဖြင့် attempt တိုးသည့်အခါ လျင်မြန်စွာ ကျဆင်းသည် — 30.00 % (max 1)၊
9.00 % (max 2)၊ 2.70 % (max 3)၊ 0.81 % (max 4)၊ 0.24 % (max 5) ဖြစ်သည်။

၄။ prefix ၏ တည်ငြိမ်မှု (byte တူညီမှု) အပေါ် မှီခိုသည်။ prefix တူညီပါက ကုန်ကျစရိတ်သည်
80.4 % သက်သာသည်၊ မတူညီပါက 5.11 ဆ ပိုကုန်သည်။

၅။ total(cap) = compute(cap) + P_unfinished(cap) × escalation_cost ဖြစ်သည်။ escalation USD 48.00 တွင်
cap 10၊ USD 12.00 တွင် cap 8၊ USD 4.00 တွင် cap 7 သည် total အနည်းဆုံး ဖြစ်သည်။

</details>

## References

- နယ်ပယ် အခြေခံ အချက်အလက် — [`../../terms/06_agents_and_tools.md`](../../terms/06_agents_and_tools.md) နှင့်
  [`../../glossary/by_area/06_agents_and_tools.json`](../../glossary/by_area/06_agents_and_tools.json)။
- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) —
  MIT licensed, from `rohitg00/ai-engineering-from-scratch`။
- စံ protocol နှင့် သတ်မှတ်ချက် — [MCP 2026-07-28 key changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog)၊
  [Agent Skills specification](https://agentskills.io/specification)။
- ပုံစံ နှင့် နည်းလမ်း — [ReAct](https://arxiv.org/abs/2210.03629)၊
  [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)၊
  [Sagas](https://dl.acm.org/doi/10.1145/38713.38742)။
