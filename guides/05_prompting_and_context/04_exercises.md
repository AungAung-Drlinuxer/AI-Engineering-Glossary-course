# ၀၄ — လေ့ကျင့်ခန်းများနှင့် အဖြေများ (Prompting & Context)

ဤဖိုင်သည် နယ်ပယ် ၀၅ ၏ term ၁၅ ခုကို အသုံးပြု၍ တွက်ချက်ခြင်း၊ ပြဿနာ ရှာဖွေခြင်းနှင့် ဆုံးဖြတ်ချက်
ချခြင်း လေ့ကျင့်ခန်းများကို စုစည်းထားသည်။ အပိုင်း ၁ တွင် အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာ ၄ ခု၊
အပိုင်း ၂ တွင် တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ အပိုင်း ၃ တွင် ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊
အပိုင်း ၄ တွင် ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း ၂ ခု ပါဝင်သည်။ အပိုင်း ၅ တွင် အဖြေတိုင်းကို
ဖော်မြူလာ၊ တွက်ချက်မှု အဆင့်ဆင့်နှင့် အကြောင်းရင်း ရှင်းလင်းချက်နှင့်အတူ ပေးထားသည်။

ဤဖိုင်တွင် ပါဝင်သည့် ကိန်းဂဏန်း တိုင်းသည် Python (standard library သာ) ဖြင့် အမှန်တကယ်
လုပ်ဆောင်ခဲ့သည့် တွက်ချက်မှု၏ output ဖြစ်သည်။ ထို script ကို
`~/.hermes/profiles/ai-engineer/cache/scratch/glossary_guide_05/calc.py` တွင် ထားရှိသည်။
ဖော်ပြထားသည့် block အတိုင်း run လုပ်ပါက တူညီသည့် output ကို ပြန်လည် ရရှိမည်။
ကိန်းဂဏန်း တိုင်းသည် သတ်မှတ်ထားသည့် ယူဆချက် (assumption) အပေါ် မှီခိုသည်၊ ထို့ကြောင့်
ဖော်မြူလာ တစ်ခုစီနှင့်အတူ ၎င်း၏ ယူဆချက်ကို ဖော်ပြထားသည်။

တိုင်းတာချက် (accuracy၊ ကွာဟမှု ရာခိုင်နှုန်း) များကို အသုံးပြုသည့် နေရာတိုင်းတွင် ထို
တန်ဖိုးသည် **ဥပမာအတွက် သတ်မှတ်ထားသည့် တိုင်းတာချက်** ဖြစ်သည်၊ benchmark ရလဒ်
မဟုတ်ပါ။ တွက်ချက်မှု အဆင့်များသာ အတိအကျ ဖြစ်သည်။

လေ့ကျင့်ခန်းများကို လက်တွေ့ စမ်းသပ်ရန် `labs/lab_token_budget.py` (budget နှင့် cost)၊
`labs/lab_prefix_cache.py` (prefix cache၊ prefill token နှင့် TTFT) နှင့်
`labs/lab_shape_prompt.py` (prompt structure၊ example အရေအတွက်နှင့် chain-of-thought)
တို့ကို အသုံးပြုနိုင်သည်။ ထို lab များသည် `tokens = ceil(characters / 4)` ဟူသည့်
estimator ကို သုံးသည်။ **ဤဖိုင်၏ တွက်ချက်မှုများသည် ထို lab များအပေါ် မှီခိုမှု မရှိပါ။**

## ၁။ အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာများ (Worked Examples)

### ဥပမာ ၁ — Prompt တစ်ခုကို အပိုင်းများ ခွဲ၍ token budget တွက်ချက်ခြင်း

**ယူဆချက် —** context window 16,384 token၊ system prompt 700 token၊ tool schema 900 token၊
retrieved chunk ၄ ခု (တစ်ခုလျှင် 550 token)၊ conversation history 5,200 token၊ user turn 320 token၊
output အတွက် သီးသန့် ချန်ထားသည့် 2,048 token။

**ဖော်မြူလာ —**
- retrieved = chunk အရေအတွက် × chunk တစ်ခုလျှင် token
- used = system + tools + retrieved + history + user + reserved output
- headroom = window − used

**တွက်ချက်မှု —**
1. retrieved = 4 × 550 = 2,200 token ဖြစ်သည်။
2. used = 700 + 900 + 2,200 + 5,200 + 320 + 2,048 = 11,368 token ဖြစ်သည်။
3. headroom = 16,384 − 11,368 = 5,016 token ဖြစ်သည်၊ ဆိုလိုသည်မှာ window ၏ 30.6 % ဖြစ်သည်။
4. ညွှန်ကြားချက် အပိုင်း (system + tools) = 1,600 token၊ ဆိုလိုသည်မှာ 9.8 % သာ ဖြစ်သည်။
5. history သည် 5,200 token ဖြင့် အကြီးဆုံး အပိုင်း (31.7 %) ဖြစ်သည်။
6. headroom 5,016 token သည် chunk ၉ ခုစာ (9.12) နေရာ ဖြစ်သည်။
7. chunk ၂ ခု ထပ်တိုးပါက used = 12,468၊ headroom = 3,916 token သို့ ကျဆင်းသည်။

**ကောက်ချက် —** ဤ prompt တွင် အကြီးဆုံး အသုံးစရိတ်သည် ညွှန်ကြားချက် မဟုတ်ဘဲ
conversation history ဖြစ်သည်။ ထို့ကြောင့် အထောက်အထား ထပ်ထည့်လိုပါက history ကို
အရင် ကျုံ့ရမည်။ history 10,216 token ကျော်လာသည့်အခါ ကျန် အပိုင်းများ မပြောင်းလဲဘဲ
window ပြည့်မည် ဖြစ်သည်။

```bash
python3 - <<'PY'
W = 16384
system, tools, chunk, n, history, user, out = 700, 900, 550, 4, 5200, 320, 2048
retrieved = chunk * n
used = system + tools + retrieved + history + user + out
print("retrieved tokens      ", retrieved)
print("used total            ", used)
print("window                ", W)
print("headroom              ", W - used)
print("used share pct        ", round(100 * used / W, 1))
print("instr share pct       ", round(100 * (system + tools) / W, 1))
print("history share pct     ", round(100 * history / W, 1))
print("evidence share pct    ", round(100 * retrieved / W, 1))
print("output reserved pct   ", round(100 * out / W, 1))
print("headroom in chunks    ", round((W - used) / chunk, 2))
plus2 = used + 2 * chunk
print("used with 2 chunks more", plus2, "headroom", W - plus2)
print("break-even at history ", W - (used - history), "tokens of history")
PY
```

```text
retrieved tokens       2200
used total             11368
window                 16384
headroom               5016
used share pct         69.4
instr share pct        9.8
history share pct      31.7
evidence share pct     13.4
output reserved pct    12.5
headroom in chunks     9.12
used with 2 chunks more 12468 headroom 3916
break-even at history  10216 tokens of history
```

### ဥပမာ ၂ — Cache နှင့် retry ပါဝင်သည့် တစ်အလုပ်လျှင် ကုန်ကျစရိတ်

**ယူဆချက် —** ခေါ်ဆိုမှု 12,000 ကြိမ်၊ တည်ငြိမ်သည့် prefix 5,000 token၊
တောင်းဆိုမှုနှင့် သီးသန့်ဖြစ်သည့် အပိုင်း 2,000 token၊ output 800 token။
Input စျေးနှုန်း USD 3.00 / သန်း၊ cache read စျေးနှုန်း USD 0.30 / သန်း၊ output စျေးနှုန်း
USD 15.00 / သန်း။ ခေါ်ဆိုမှု 6 % သည် တစ်ကြိမ် retry လုပ်သည်။

**ဖော်မြူလာ —**
- cache မပါ input = စုစုပေါင်း prompt token × ခေါ်ဆိုမှု × input စျေးနှုန်း
- cache ပါ input = prefix × ခေါ်ဆိုမှု × cache read စျေးနှုန်း + သီးသန့် အပိုင်း × ခေါ်ဆိုမှု × input စျေးနှုန်း
- တစ် အောင်မြင်သည့် အလုပ်လျှင် = (cache ပါ စုစုပေါင်း) × (1 + retry အချိုး) ÷ ခေါ်ဆိုမှု

**တွက်ချက်မှု —**
1. cache မပါ input = 7,000 × 12,000 × 3.00 ÷ 10⁶ = USD 252.00 ဖြစ်သည်။
2. output = 800 × 12,000 × 15.00 ÷ 10⁶ = USD 144.00 ဖြစ်သည်။
3. cache မပါ စုစုပေါင်း = USD 396.00 ဖြစ်သည်။
4. cache ပါ input = (5,000 × 12,000 × 0.30 + 2,000 × 12,000 × 3.00) ÷ 10⁶ = 18.00 + 72.00 = USD 90.00 ဖြစ်သည်။
5. cache ပါ စုစုပေါင်း = 90.00 + 144.00 = USD 234.00 ဖြစ်သည်။
6. saving = 396.00 − 234.00 = USD 162.00၊ ဆိုလိုသည်မှာ 40.91 % ဖြစ်သည်။
7. retry 6 % = 720 ကြိမ်၊ အပိုကုန်ကျစရိတ် = 234.00 × 0.06 = USD 14.04 ဖြစ်သည်။
8. တစ် အောင်မြင်သည့် အလုပ်လျှင် = (234.00 + 14.04) ÷ 12,000 = USD 0.020670 ဖြစ်သည်။

**ကောက်ချက် —** cacheable prefix သည် prompt ၏ 71.4 % ဖြစ်သဖြင့် cache ၏ အကျိုးအမြတ်သည်
input ကုန်ကျစရိတ်၏ 64.3 % ဖြစ်သည်။ သို့သော် cache သည် output ကုန်ကျစရိတ်ကို
မလျှော့နိုင်သဖြင့် စုစုပေါင်း saving သည် 40.91 % တွင်သာ ရပ်သည်။ ထို့ကြောင့်
saving ကို တွက်သည့်အခါ output အပိုင်းကို မဖြစ်မနေ ထည့်ရမည်။ Retry သည် saving ကို
အလွယ်တကူ စားနိုင်သည် — ဤ ဥပမာတွင် 6 % retry သည် USD 14.04 ကို ပြန်ကုန်စေသည်။

```bash
python3 - <<'PY'
calls, prefix, volatile = 12000, 5000, 2000
p_in, p_cache, p_out, out_tok = 3.00, 0.30, 15.00, 800
total_in = prefix + volatile
no_cache_in = total_in * calls * p_in / 1e6
no_cache_out = out_tok * calls * p_out / 1e6
print("prompt tokens         ", total_in)
print("input USD no cache    ", round(no_cache_in, 2))
print("output USD no cache   ", round(no_cache_out, 2))
print("total USD no cache    ", round(no_cache_in + no_cache_out, 2))
cache_in = (prefix * calls * p_cache / 1e6) + (volatile * calls * p_in / 1e6)
print("input USD with cache  ", round(cache_in, 2))
print("total USD with cache  ", round(cache_in + no_cache_out, 2))
saved = (no_cache_in + no_cache_out) - (cache_in + no_cache_out)
print("USD saved             ", round(saved, 2))
print("saving pct            ", round(100 * saved / (no_cache_in + no_cache_out), 2))
print("cache read share pct  ", round(100 * prefix / total_in, 1))
print("retried calls         ", round(0.06 * calls))
print("retry extra USD       ", round((cache_in + no_cache_out) * 0.06, 2))
print("USD per successful task", round((cache_in + no_cache_out) * 1.06 / calls, 6))
PY
```

```text
prompt tokens          7000
input USD no cache     252.0
output USD no cache    144.0
total USD no cache     396.0
input USD with cache   90.0
total USD with cache   234.0
USD saved              162.0
saving pct             40.91
cache read share pct   71.4
retried calls          720
retry extra USD        14.04
USD per successful task 0.02067
```

### ဥပမာ ၃ — Conversation history ကို compaction လုပ်ခြင်း

**ယူဆချက် —** turn 40 ခု၊ turn တစ်ခုလျှင် ပျမ်းမျှ 260 token၊ စုစုပေါင်း 10,400 token။
နောက်ဆုံး turn ၆ ခုကို စာလုံးတိုင်း ထိန်းသည်၊ ကျန် turn များကို 55 token ၏ အနှစ်ချုပ်
တစ်ခုသို့ ချုံ့သည်။ Window 16,384 token ဖြစ်ပြီး ကျန် အပိုင်းများ (system၊ tools၊ evidence၊
user၊ reserved output) သည် 6,168 token ဖြစ်သည်။

**ဖော်မြူလာ —**
- raw = turn အရေအတွက် × turn တစ်ခုလျှင် token
- ချုံ့ပြီးနောက် = (စာလုံးတိုင်း ထိန်းသည့် turn × turn တစ်ခုလျှင် token) + summary token
- ကျန်သည့် နေရာ = window − (အခြား အပိုင်းများ + ချုံ့ပြီးနောက် history)

**တွက်ချက်မှု —**
1. raw = 40 × 260 = 10,400 token ဖြစ်သည်။
2. စာလုံးတိုင်း ထိန်းသည့် အပိုင်း = 6 × 260 = 1,560 token ဖြစ်သည်။
3. ချုံ့ပြီးနောက် history = 1,560 + 55 = 1,615 token ဖြစ်သည်။
4. လွတ်သည့် token = 10,400 − 1,615 = 8,785 token၊ ဆိုလိုသည်မှာ 84.5 % ဖြစ်သည်။
5. အချိုး = 10,400 ÷ 1,615 = 6.44 ဖြစ်သည်။
6. မချုံ့မီ: 6,168 + 10,400 = 16,568 token ဖြစ်သဖြင့် 184 token ကျော်လွန်သည် (headroom −184)။
7. ချုံ့ပြီးနောက်: 6,168 + 1,615 = 7,783 token ဖြစ်သဖြင့် ကျန်သည့် နေရာ 8,601 token ဖြစ်သည်။
8. Summary သည် turn တစ်ခုလျှင် 1.38 token ခန့် ရသည် — ထို့ကြောင့် စာလုံးတိုင်း ထိန်းရမည့်
   အရာ (identifier၊ ကန့်သတ်ချက်၊ မဖြေရှင်းရသေးသည့် state) ကို သီးသန့် ခွဲထားရမည်။

**ကောက်ချက် —** Compaction သည် ဤ ဥပမာတွင် window ကျော်လွန်မှုကို ဖြေရှင်းပေးသည်။
သို့သော် ချုံ့ခြင်းသည် lossy ဖြစ်သည့်အတွက် ဆုံးရှုံးလိုက်သည့် အသေးစိတ် တိုင်းသည်
မော်ဒယ်တွင် အထောက်အထား၊ ကန့်သတ်ချက် သို့မဟုတ် state များ ဆုံးရှုံးနိုင်သည့် အန္တရာယ်
ဖန်တီးသည်။ ထို့ကြောင့် ချုံ့ထားသည့် context ကို ကိုယ်စားပြုသည့် task များတွင်
မဖြစ်မနေ စမ်းသပ်ရမည်။

```bash
python3 - <<'PY'
W = 16384
turns, per_turn, verbatim, summary = 40, 260, 6, 55
others = 700 + 900 + 2200 + 320 + 2048
raw = turns * per_turn
kept = verbatim * per_turn + summary
print("history tokens raw    ", raw)
print("verbatim turns kept   ", verbatim, "->", verbatim * per_turn)
print("summary tokens        ", summary)
print("history after compact ", kept)
print("tokens freed          ", raw - kept)
print("reduction pct         ", round(100 * (raw - kept) / raw, 1))
print("ratio raw / compact   ", round(raw / kept, 2))
print("headroom before       ", W - (others + raw))
print("headroom after        ", W - (others + kept))
print("summary budget per raw turn", round(summary / turns, 2), "tokens")
PY
```

```text
history tokens raw     10400
verbatim turns kept    6 -> 1560
summary tokens         55
history after compact  1615
tokens freed           8785
reduction pct          84.5
ratio raw / compact    6.44
headroom before        -184
headroom after         8601
summary budget per raw turn 1.38 tokens
```

### ဥပမာ ၄ — Few-Shot ၏ အကျိုးအမြတ်နှင့် prompt sensitivity

**ယူဆချက် —** eval item 240 ခု။ ဤသည် **ဥပမာအတွက် သတိဖြင့် သတ်မှတ်ထားသည့်
တိုင်းတာချက်** ဖြစ်သည် — benchmark မဟုတ်ပါ။ Zero-shot တွင် 178 ခု မှန်၊ few-shot တွင် 231 ခု မှန်၊
few-shot ၏ အဓိပ္ပာယ် တူညီသည့် မူကွဲ တစ်ခုတွင် 224 ခု မှန်။

**ဖော်မြူလာ —**
- တိကျမှု = မှန်သည့် item ÷ item စုစုပေါင်း
- sensitivity ကွာဟမှု = မူကွဲ နှစ်ခု၏ တိကျမှု ကွာဟမှု

**တွက်ချက်မှု —**
1. zero-shot = 178 ÷ 240 = 74.17 % ဖြစ်သည်။
2. few-shot = 231 ÷ 240 = 96.25 % ဖြစ်သည်။
3. ကွာဟမှု = 96.25 − 74.17 = 22.08 ရာခိုင်နှုန်းအမှတ်၊ item 53 ခုစာ ဖြစ်သည်။
4. မူကွဲ = 224 ÷ 240 = 93.33 % ဖြစ်သည်။
5. sensitivity ကွာဟမှု = 96.25 − 93.33 = 2.92 ရာခိုင်နှုန်းအမှတ်၊ item 7 ခုစာ ဖြစ်သည်။
6. 99 % ရောက်ရန် few-shot မှ item 7 ခု ထပ်လိုသည် (238 − 231)။
7. zero-shot ၏ မှားသည့် item = 62 ခု၊ few-shot ၏ မှားသည့် item = 9 ခု ဖြစ်သည်။

**ကောက်ချက် —** ဤ ဥပမာတွင် few-shot သည် zero-shot ထက် ရာခိုင်နှုန်းအမှတ် 22.08 ပိုမှန်သည်။
သို့သော် မူကွဲ ကွာဟမှု 2.92 ရာခိုင်နှုန်းအမှတ် (item 7) သည် sensitivity ၏ အတိုင်းအတာကို
ပြသည်။ ထို့ကြောင့် "prompt တစ်ခုသည် အဆင်ပြေသည့် စကားလုံး ဖွဲ့စည်းမှုအောက်တွင်
အောင်မြင်သည်" ဟူသည့် အချက်သည် အမှန်တကယ် အသုံးပြုသူများအတွက် ယုံကြည်စိတ်ချရမှုကို
မပြနိုင်ပါ။ Sample size တိုးလာပါက ထို ကွာဟမှုသည် item အရေအတွက် အဖြစ် ပိုထင်ရှားလာမည်။

```bash
python3 - <<'PY'
cases, zero, few, variant = 240, 178, 231, 224
print("zero-shot  pct        ", round(100 * zero / cases, 2), "items", zero)
print("few-shot   pct        ", round(100 * few / cases, 2), "items", few)
print("difference pt         ", round(100 * few / cases - 100 * zero / cases, 2))
print("difference items      ", few - zero)
print("variant    pct        ", round(100 * variant / cases, 2))
print("sensitivity spread pt ", round(100 * (few - variant) / cases, 2), "items", few - variant)
print("items to reach 99 pct ", round(0.99 * cases) - few)
print("zero-shot failures    ", cases - zero)
print("few-shot failures     ", cases - few)
PY
```

```text
zero-shot  pct         74.17 items 178
few-shot   pct         96.25 items 231
difference pt          22.08
difference items       53
variant    pct         93.33
sensitivity spread pt  2.92 items 7
items to reach 99 pct  7
zero-shot failures     62
few-shot failures      9
```

## ၂။ တွက်ချက်ရသည့် လေ့ကျင့်ခန်းများ (Calculation Exercises)

လေ့ကျင့်ခန်း တစ်ခုစီတွင် ကိန်းဂဏန်း အဖြေ အတိအကျ ရှိသည်။ အဖြေနှင့် ဖော်မြူလာ
ရှင်းလင်းချက်ကို အပိုင်း ၅.၁ တွင် ပေးထားသည်။ ဖော်ပြထားသည့် lab ဖြင့် လက်တွေ့ စစ်ဆေးနိုင်သည်။

**လေ့ကျင့်ခန်း ၁ — Token budget နှင့် window ကျော်လွန်မှု**

Window 32,768 token၊ system prompt 1,100၊ tool schema 1,300၊ retrieved chunk 12 ခု (တစ်ခုလျှင် 640)၊
conversation history 24,000၊ user turn 450၊ reserved output 3,000။
တွက်ရမည့် အချက်များ — (က) retrieved စုစုပေါင်း၊ (ခ) used နှင့် shortfall၊ (ဂ) used သည် window ၏
မည်မျှ ရာခိုင်နှုန်း၊ (ဃ) ပုံသေ အပိုင်းများ (history အပါအဝင်) နှင့် history ၏ ရာခိုင်နှုန်း၊
(င) chunk များအတွက် ကျန်သည့် နေရာ၊ ထည့်နိုင်သည့် chunk အရေအတွက်နှင့် ဖြုတ်ရမည့် အရေအတွက်၊
(စ) ဖြုတ်ပြီးနောက် ကျန်သည့် နေရာ၊ (ဆ) history ကို မည်မျှ အထိ ကျုံ့ရမည်၊ မည်မျှ ရာခိုင်နှုန်း ဖြတ်ရမည်။
→ `labs/lab_token_budget.py --window 32768 --retrieved 7680 --history 24000`

**လေ့ကျင့်ခန်း ၂ — Token အရေအတွက်နှင့် စျေးနှုန်းမှ တစ်ကြိမ်လျှင် ကုန်ကျစရိတ်**

Input 4,800 token၊ output 950 token။ Input စျေးနှုန်း USD 2.50 / သန်း၊ output စျေးနှုန်း
USD 10.00 / သန်း။ တွက်ရမည့် အချက်များ — (က) input နှင့် output ၏ USD၊ (ခ) တစ်ကြိမ်လျှင် USD
နှင့် 1,000 ကြိမ်လျှင် USD၊ (ဂ) USD 1 လျှင် ခေါ်ဆိုမှု အရေအတွက်၊ (ဃ) စုစုပေါင်း၏ input
ရာခိုင်နှုန်း၊ (င) input နှစ်ဆ ဖြစ်ပါက နှင့် output ထက်ဝက် ဖြစ်ပါက USD၊ (စ) ကုန်ကျစရိတ်
USD 0.01 တိုးရန် ထပ်လိုအပ်သည့် input token၊ (ဆ) token သန်းတစ်သန်းလျှင် ပျမ်းမျှ USD။
→ `labs/lab_token_budget.py --system 4800 --reserve 950`

**လေ့ကျင့်ခန်း ၃ — Context window ကျော်လွန်မှုနှင့် ဘာကို ဖြုတ်မည်**

Window 8,192 token၊ ပုံသေ အပိုင်းများ (system၊ instructions၊ history၊ user၊ reserved output)
6,400 token၊ ထည့်လိုသည့် chunk ၆ ခု (တစ်ခုလျှင် 700 token)။
တွက်ရမည့် အချက်များ — (က) chunk အားလုံး၏ token နှင့် used၊ (ခ) ကျော်လွန်သည့် token နှင့်
window ၏ ရာခိုင်နှုန်း၊ (ဂ) ထည့်နိုင်သည့် chunk အရေအတွက်နှင့် ဖြုတ်ရမည့် အရေအတွက်၊
(ဃ) ဖြုတ်ပြီးနောက် ကျန်သည့် နေရာ၊ (င) chunk ၆ ခုလုံး ဝင်စေရန် chunk တစ်ခုလျှင် မည်မျှ
token သို့ ဖြတ်ရမည်။ → `labs/lab_token_budget.py --window 8192 --retrieved 4200`

**လေ့ကျင့်ခန်း ၄ — Cacheable prefix token နှင့် saving**

Prompt 6,000 token = တည်ငြိမ်သည့် prefix 4,000 + သီးသန့် အပိုင်း 2,000။ ခေါ်ဆိုမှု 10,000။
Input စျေးနှုန်း USD 3.00 / သန်း၊ cache read စျေးနှုန်း USD 0.30 / သန်း။
တွက်ရမည့် အချက်များ — (က) cacheable ရာခိုင်နှုန်း၊ (ခ) cache မပါ နှင့် cache ပါ USD၊
(ဂ) saving USD နှင့် ရာခိုင်နှုန်း၊ (ဃ) cache read နှင့် input ၏ စျေးနှုန်း အချိုး၊
(င) 1,000 ကြိမ်လျှင် saving၊ (စ) cache အောင်မြင်သည့် အခါ ၏ တကယ့် input စျေးနှုန်း (USD / သန်း)၊
(ဆ) ခေါ်ဆိုမှု 25 % တွင် cache miss ဖြစ်ပါက USD နှင့် saving ရာခိုင်နှုန်း။
→ `labs/lab_prefix_cache.py --prefix-tokens 4000 --calls 10000 --prefill-rate 2500`

**လေ့ကျင့်ခန်း ၅ — Schema ဖြင့် ကန့်သတ်ထားသည့် output နှင့် free text ၏ ယုံကြည်စိတ်ချရမှု**

Sample 400 ခု။ ဤသည် သတ်မှတ်ထားသည့် တိုင်းတာချက် ဖြစ်သည်။ Free text တွင်
352 ခု မှန်ကန်စွာ parse/validate ဖြစ်သည်၊ schema ဖြင့် ကန့်သတ်ထားသည့် output တွင် 396 ခု
ဖြစ်သည်။ တွက်ရမည့် အချက်များ — (က) တစ်မျိုးစီ၏ ရာခိုင်နှုန်းနှင့် ကျရှုံးသည့် အရေအတွက်၊
(ခ) ကျရှုံးမှု အချိုး၊ (ဂ) ရာခိုင်နှုန်းအမှတ် ကွာဟမှု၊ (ဃ) တစ်ကြိမ် retry နှင့် နှစ်ကြိမ် retry
ပြီးနောက် တစ်မျိုးစီ၏ အောင်မြင်မှု ရာခိုင်နှုန်းနှင့် ကျန်သည့် item အရေအတွက် (retry တိုင်းသည်
လွတ်လပ်သည်ဟု ယူဆသည်)၊ (င) schema က လူဖြင့် ပြင်ရမည့် item မည်မျှ လျှော့ပေးသည်။
→ `labs/lab_shape_prompt.py --task extract --examples 4`

**လေ့ကျင့်ခန်း ၆ — Prompt ရှည်လာသည့်အခါ latency သက်ရောက်မှု**

Prefill throughput 2,500 token/s၊ ပုံသေ overhead 200 ms၊ ပုံမှန် prompt 1,200 token၊
ရှည်သည့် prompt 9,600 token၊ output 200 token၊ output token တစ်ခုလျှင် 18 ms။
တွက်ရမည့် အချက်များ — (က) prompt တစ်ခုစီ၏ prefill ms (overhead မပါ)၊ (ခ) prefill ကွာဟမှု၊
(ဂ) output အတွက် ကြာချိန်၊ (ဃ) prompt တစ်ခုစီ၏ စုစုပေါင်း ms နှင့် အချိုး၊ (င) စုစုပေါင်း၏
မည်မျှ ရာခိုင်နှုန်း တိုးသည်၊ (စ) prefill ရှယ် (share) မည်သို့ ပြောင်းလဲသည်၊ (ဆ) ရှည်သည့်
prompt ဖြင့် ပုံမှန် စုစုပေါင်း အတူတူ ရရှိရန် prefill throughput မည်မျှ လိုအပ်သည်။
→ `labs/lab_prefix_cache.py --prefix-tokens 9600 --calls 1 --prefill-rate 2500 --suffix-tokens 200`

## ၃။ ပြဿနာ ရှာဖွေခြင်း (Troubleshooting Scenarios)

ပြဿနာ တစ်ခုစီကို symptom၊ တိုင်းတာရမည့် အချက်၊ ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်)၊
ဖြေရှင်းနည်းနှင့် ရှင်းလင်းသည့် term ဟူသည့် အစဉ်အတိုင်း ဖော်ပြထားသည်။
အကြောင်းရင်း အစဉ်သည် တိုင်းတာမှုဖြင့် ရှာဖွေနိုင်သည့် အစဉ်အတိုင်း ဖြစ်သည်။
အသေးစိတ် ရှင်းလင်းချက်ကို အပိုင်း ၅.၂ တွင် ပေးထားသည်။

### ပြဿနာ ၁ — ရှည်သည့် session ၏ နောက်ပိုင်းတွင် ညွှန်ကြားချက်များ လိုက်နာမှု ကျဆင်းသည်

- **Symptom —** session အစတွင် output သည် format နှင့် ကန့်သတ်ချက်များကို လိုက်နာသည်၊
  turn များစွာ ကြာပြီးနောက် အလားတူ မေးခွန်းအတွက် format လွဲသည်၊ ကန့်သတ်ချက် တစ်ခုကို
  လျစ်လျူရှုသည်၊ သို့မဟုတ် အရင် turn များတွင် ဖြေပြီးသည့် အချက်ကို ပြန်မှားသည်။
- **တိုင်းတာရမည့် အချက် —** turn တစ်ခုလျှင် input token နှင့် ၎င်း၏ ကြီးထွားမှု၊ history ၏
  window ရာခိုင်နှုန်း၊ system ညွှန်ကြားချက်၏ တည်နေရာနှင့် token အရေအတွက်၊ ကန့်သတ်ချက်
  စာသားသည် prompt ၏ အစ၊ အလယ်၊ အဆုံး မည်သည့်နေရာတွင် ရှိသည်၊ output တွင် format
  လိုက်နာမှု ရာခိုင်နှုန်း (turn အလိုက်)။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) history စုပုံလာသဖြင့် ကန့်သတ်ချက်
  စာသားသည် context ၏ အလယ်ပိုင်းသို့ ရောက်သွားခြင်း၊ (၂) compaction လုပ်သည့်အခါ
  ကန့်သတ်ချက် သို့မဟုတ် identifier များ အနှစ်ချုပ်ထဲ ပါမလာခြင်း၊ (၃) retrieved စာသားထဲမှ
  အခွင့်အာဏာ နည်းသည့် ညွှန်ကြားချက်နှင့် ပဋိပက္ခဖြစ်ခြင်း၊ (၄) system ညွှန်ကြားချက်၏
  ဦးစားပေး စည်းမျဉ်းသည် provider အလိုက် ကွာခြားသည့် အချက်ကို ထည့်မတွက်ခြင်း။
- **ဖြေရှင်းနည်း —** ဆုံးဖြတ်ချက်အတွက် အရေးပါသည့် ကန့်သတ်ချက်များကို ထင်ရှားနေဆဲ
  နေရာတွင် ထားရှိရမည်၊ history ကို အနှစ်ချုပ်ရာတွင် ကန့်သတ်ချက်နှင့် identifier များကို
  စာလုံးတိုင်း ထိန်းရမည်၊ budget ဖြင့် history ကို ကန့်သတ်ရမည်၊ မယုံကြည်ရသည့်
  tool output ကို data အနေဖြင့် အမှတ်အသားပြုရမည်။
- **ရှင်းလင်းသည့် term —** Instruction Following၊ System Prompt၊ Lost in the Middle၊ Token Budget၊
  Context Compression။

### ပြဿနာ ၂ — အလုပ်ပမာဏ များလာသည့်အခါ output format ကျိုးသည်

- **Symptom —** စမ်းသပ်မှုတွင် စနစ်သည် format မှန်သည်၊ production တွင် တစ်ပြိုင်နက်
  ခေါ်ဆိုမှု များလာသည့်အခါ parse မဖြစ်သည့် output ရာခိုင်နှုန်း တက်လာသည်၊
  retry များလာသည်၊ အသုံးပြုသူများ ဖော်ပြသည့် မူကွဲများတွင် format လွဲမှု ပိုဖြစ်သည်။
- **တိုင်းတာရမည့် အချက် —** parse/validate ကျရှုံးမှု ရာခိုင်နှုန်း (အချိန်နှင့်အမျှ)၊
  တစ်ပြိုင်နက် ခေါ်ဆိုမှု အရေအတွက်၊ decoding setting (temperature စသည်) နှင့် ၎င်း၏
  ပြောင်းလဲမှု၊ output token အရေအတွက် ဖြန့်ကျက်မှု၊ demo example အရေအတွက်၊
  prompt မူကွဲအလိုက် ကျရှုံးမှု ကွာဟမှု၊ retry တစ်ကြိမ်လျှင် ပြန်အောင်မြင်မှု ရာခိုင်နှုန်း။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) schema ကို prompt တွင် စာသားဖြင့်သာ
  ဖော်ပြထား၍ decode အဆင့်တွင် မကန့်သတ်ခြင်း၊ (၂) demonstration အရေအတွက် သို့မဟုတ်
  လွှမ်းခြုံမှု မလုံလောက်ခြင်း၊ (၃) မတည်ငြိမ်သည့် decoding setting ကြောင့်
  prompt sensitivity ပေါ်လွင်လာခြင်း၊ (၄) စမ်းသပ်သည့် eval set သည် production မူကွဲများကို
  ကိုယ်စားမပြုခြင်း။
- **ဖြေရှင်းနည်း —** schema ဖြင့် ကန့်သတ်ထားသည့် output (schema-constrained decoding)
  ကို ဖွင့်ရမည်၊ parse နှင့် schema စစ်ဆေးမှု နှစ်ဆင့် ထားရမည်၊ မအောင်မြင်ပါက retry ကို
  အရေအတွက် ကန့်သတ်ချက်နှင့်အတူ ထည့်ရမည်၊ အဓိပ္ပာယ် တူညီသည့် မူကွဲများကို
  regression test များတွင် ထိန်းသိမ်းရမည်။
- **ရှင်းလင်းသည့် term —** Prompt Sensitivity၊ Few-Shot၊ In-Context Learning၊
  Instruction Following၊ Chain of Thought (CoT)။

### ပြဿနာ ၃ — Retrieved စာရွက်စာတမ်း တစ်ခုသည် မော်ဒယ်၏ အပြုအမူကို ပြောင်းလဲသည်

- **Symptom —** အထောက်အထား အသစ် တစ်ခု ထည့်ပြီးနောက် စနစ်သည် အသုံးပြုသူ
  တောင်းဆိုသည့် အလုပ်ကို မလုပ်ဘဲ ထို စာရွက်စာတမ်းထဲ ပါသည့် အကြောင်းအရာနှင့်
  ပတ်သက်သည့် အလုပ်ကို လုပ်သည်၊ သို့မဟုတ် ပြင်ပ tool/URL ကို ခေါ်ရန် ကြိုးစားသည်။
- **တိုင်းတာရမည့် အချက် —** ပဋိပက္ခ စမ်းသပ်မှု ရလဒ် (တိုက်ရိုက် နှင့် သွယ်ဝိုက်)၊
  retrieved အကြောင်းအရာကို data အဖြစ် အမှတ်အသား ပြုထားမှု ရှိမရှိ၊
  tool ခေါ်ဆိုမှု ကြိုးစားချက် အရေအတွက်နှင့် ၎င်း၏ တန်ဖိုး၊ ထိုစာသားကို ဖယ်လိုက်ပါက
  အပြုအမူ ပြန်ကောင်းမလား၊ စာသားထဲတွင် imperative ပုံစံ စာကြောင်း အရေအတွက်။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) retrieved စာသားသည် ညွှန်ကြားချက်နှင့်
  ပုံစံ တူသဖြင့် မော်ဒယ်က ညွှန်ကြားချက် အဖြစ် ဖတ်ခြင်း (prompt injection)၊ (၂) system
  ကန့်သတ်ချက်များသည် ထို စာသားနှင့် နီးကပ်စွာ ရောနှောနေခြင်း၊ (၃) least privilege မရှိသဖြင့်
  လုပ်ဆောင်ချက် တစ်ခုကို ခွင့်ပြုချက် မတောင်းဘဲ လုပ်နိုင်ခြင်း၊ (၄) ပဋိပက္ခ စမ်းသပ်မှု
  မရှိသဖြင့် အပြုအမူ ပြောင်းလဲမှုကို ရှာမတွေ့ခြင်း။
- **ဖြေရှင်းနည်း —** မယုံကြည်ရသည့် အကြောင်းအရာကို data အနေဖြင့် အမှတ်အသားပြု၍
  ၎င်း၏ အပြင်ဘက်တွင် ဦးစားပေး မြင့်သည့် ကန့်သတ်ချက်များကို ထိန်းသိမ်းရမည်၊
  least privilege နှင့် အတည်ပြုချက် ထိန်းချုပ်မှုများဖြင့် အကျိုးဆက်ကို ကန့်သတ်ရမည်၊
  တိုက်ရိုက်နှင့် သွယ်ဝိုက်သည့် ပဋိပက္ခ အမှုများကို စမ်းသပ်ရမည်။
- **ရှင်းလင်းသည့် term —** Instruction Hierarchy၊ System Prompt၊ Context Engineering၊
  Instruction Following။

## ၄။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်းများ (Design Decisions)

### ဆုံးဖြတ်ချက် ၁ — ရှည်သည့် တည်ငြိမ် prefix ကို cache နှင့် ချိန်ညှိခြင်း

**အခြေအနေ —** ဖောက်သည်ဝန်ဆောင်မှု assistant တစ်ခု ရှိသည်။ system prompt 2,600 token နှင့်
ပုံသေ demonstration အစု 4,000 token ရှိသည်။ ခေါ်ဆိုမှု တစ်ခုလျှင် retrieved 3,000 token၊
history 1,500 token၊ reserved output 2,048 token။ ရွေးချယ်စရာ နှစ်ခု ရှိသည် — ရွေးချယ်မှု A သည်
ရှည်သည့် system prompt နှင့် ပုံသေ demonstration များကို တူညီသည့် အစဉ်အတိုင်း
အစပိုင်းတွင် ထား၍ cache ကို မှီခိုသည်၊ ရွေးချယ်မှု B သည် ထို အပိုင်းကို ခေါ်ဆိုမှု တိုင်း
ပြောင်းလဲပြီး ပိုတိုအောင် ရေးသည်။

**trade-off —** A သည် prefix 6,600 token ကို cache read စျေးနှုန်းဖြင့် ပြန်အသုံးပြုနိုင်သည်၊
သို့သော် ခေါ်ဆိုမှု တိုင်း တူညီသည့် အစဉ် ထိန်းရန် ကန့်သတ်ချက် လိုသည်၊ ထို အပိုင်းသည်
window ၏ 50.2 % ကို ယူသည်။ B သည် prompt ကို သေးငယ်စေသည်၊ သို့သော် cache hit မရတော့ဘဲ
ခေါ်ဆိုမှု တိုင်း prefix ကို အပြည့် ကျခံရသည်။

**ဆုံးဖြတ်ချက် —** ဤ အခြေအနေတွင် A ကို ရွေးရမည်၊ အကြောင်းမှာ prefix 6,600 token ကို
cache ဖြင့် ပြန်အသုံးပြုပါက ခေါ်ဆိုမှု 20,000 အတွက် USD 396.00 မှ USD 39.60 သို့
ကျဆင်းသည်၊ ဆိုလိုသည်မှာ 90.0 % သက်သာသည်၊ လစဉ် USD 356.40 ဖြစ်သည်။
Prefix သည် prompt ၏ 50.2 % ဖြစ်သဖြင့် cache ၏ အကျိုးအမြတ်သည် အကြီးအကျယ် ဖြစ်သည်။
သို့သော် ကန့်သတ်ချက်မှာ ထို အစဉ်ကို တည်ငြိမ်စွာ ထိန်းနိုင်မှု ဖြစ်သည် — cache ၏
အရည်အချင်းနှင့် သက်တမ်းသည် provider အလိုက် ကွာခြားသည့်အတွက် miss များကို
ပုံမှန် အဖြစ် သဘောထားရမည်။

**တိုင်းတာမည့် metric —** cache-hit metadata (hit rate)၊ တစ် သန်း input token လျှင် USD၊
ဖောက်သည်ဝန်ဆောင်မှု eval set အပေါ် တိကျမှု (cache ကြောင့် မကျဆင်းရမည်)။

### ဆုံးဖြတ်ချက် ၂ — ရယူသည့် အထောက်အထု အတိုင်းအတာနှင့် တည်နေရာ

**အခြေအနေ —** Window 8,192 token၊ ပုံသေ အပိုင်းများ 5,200 token။ ရရှိနိုင်သည့် chunk များသည်
တစ်ခုလျှင် 620 token ဖြစ်သည်။ အထောက်အထား တည်နေရာ သုံးမျိုးအတွက် တိုင်းတာရရှိသည့်
တိကျမှု (ဤသည် ဥပမာအတွက် သတ်မှတ်ထားသည့် တန်ဖိုး ဖြစ်သည်) — အစပိုင်း 91–93 %၊
အလယ်ပိုင်း 71–76 %၊ အဆုံးပိုင်း 88–90 %။

**trade-off —** chunk ပိုထည့်ပါက recall တိုးနိုင်သည်၊ သို့သော် window ကျန်သည့် နေရာ
2,992 token အတွင်း chunk ၄ ခုသာ ဝင်သည်၊ ထို့ကြောင့် ၆ ခု ထည့်ရန် chunk တစ်ခုလျှင်
298 token သို့ ဖြတ်ရမည်။ ဖြတ်ခြင်းသည် အထောက်အထား၏ အကြောင်းအရာကို ဆုံးရှုံးစေသည်။
အခြား trade-off မှာ တည်နေရာ ဖြစ်သည် — အလယ်ပိုင်းသည် အစပိုင်းနှင့် အဆုံးပိုင်းထက်
22.0 ရာခိုင်နှုန်းအမှတ် နိမ့်သည်။

**ဆုံးဖြတ်ချက် —** chunk အရေအတွက်ကို ၄ ခုတွင် ထား၍ chunk တိုင်း၏ စာလုံးအပြည့်ကို
ထိန်းရမည်၊ အကြောင်းမှာ 298 token သို့ ဖြတ်လိုက်သည့် chunk သည် အကြောင်းအရာ
ဆုံးရှုံးမှုကို ဖန်တီးပြီး ထို ဆုံးရှုံးမှုသည် တည်နေရာ ကွာဟမှုထက် ရှာရ ခက်သည်။
ထို့နောက် ဆုံးဖြတ်ချက်အတွက် အရေးပါသည့် ချက် အပိုင်းကို အစပိုင်း သို့မဟုတ်
အဆုံးပိုင်းတွင် ထား၍ အလယ်ပိုင်းတွင် အရေးပါမှု နည်းသည့် chunk များကို ထားရမည်။
ဖြုတ်ခြင်း၏ အကျိုးအမြတ်ကို တွက်ပါက chunk ၆ ခုမှ ၃ ခုသို့ လျှော့ခြင်းသည် 1,860 token
(22.7 %) လွတ်စေပြီး prefill 744 ms သက်သာသည် — သို့သော် ထို လွတ်သည့် နေရာကို
output အတွက် ချန်သင့်သည်၊ အထောက်အထား ထပ်ထည့်ရန် မဟုတ်ပါ။ ဤ ဆုံးဖြတ်ချက်ကို
မှီခိုမှု မပြုမီ အထောက်အထား တည်နေရာ များစွာကို ကိုယ်တိုင် စမ်းသပ်၍ မိမိ
မော်ဒယ်၏ တကယ့် အပြုအမူကို တိုင်းရမည်။

**တိုင်းတာမည့် metric —** eval set အပေါ် အဖြေ တိကျမှု (တည်နေရာ အလိုက်)၊
grounding စစ်ဆေးမှု အောင်မြင်မှု၊ TTFT p50၊ window ၏ အသုံးပြုမှု ရာခိုင်နှုန်း။

## ၅။ အဖြေများ (Answers with Explanations)

### ၅.၁ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း အဖြေများ

#### အဖြေ ၁ — Token budget နှင့် window ကျော်လွန်မှု

**ဖော်မြူလာ —** retrieved = chunk အရေအတွက် × chunk တစ်ခုလျှင် token၊
used = system + tools + retrieved + history + user + reserved output၊ shortfall = used − window။
ယူဆချက် — token တိုင်းသည် တိကျပြီး estimator အမှား မပါပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. retrieved = 12 × 640 = 7,680 token ဖြစ်သည်။
2. used = 1,100 + 1,300 + 7,680 + 24,000 + 450 + 3,000 = 37,530 token ဖြစ်သည်။
3. shortfall = 37,530 − 32,768 = 4,762 token ဖြစ်သည်။ used သည် window ၏ 114.5 % ဖြစ်သည်။
4. ပုံသေ အပိုင်းများ (history အပါအဝင်) = 1,100 + 1,300 + 24,000 + 450 + 3,000 = 29,850 token၊
   ဆိုလိုသည်မှာ 91.1 % ဖြစ်သည်။ history တစ်ခုတည်း = 24,000 token = 73.2 % ဖြစ်သည်။
5. chunk များအတွက် ကျန်သည့် နေရာ = 32,768 − 29,850 = 2,918 token ဖြစ်သည်၊
   ထို့ကြောင့် chunk ၄ ခု (2,560 token) သာ ဝင်သည်၊ ၈ ခု ဖြုတ်ရမည်။
6. ဖြုတ်ပြီးနောက် used = 32,410 token၊ ကျန်သည့် နေရာ = 358 token ဖြစ်သည်။
7. history အတွက် = 32,768 − (1,100 + 1,300 + 7,680 + 450 + 3,000) = 19,238 token သာ ခွင့်ပြုသည်၊
   ဆိုလိုသည်မှာ 24,000 မှ 19.8 % ဖြတ်ရမည်။

**အဓိပ္ပာယ် —** ဤ ဥပမာတွင် ပြဿနာ၏ အကြီးဆုံး အစိတ်အပိုင်းသည် history (73.2 %) ဖြစ်သည်၊
retrieved chunk (23.4 %) မဟုတ်ပါ။ ထို့ကြောင့် chunk ဖြုတ်ခြင်းထက် history ကို 19.8 %
ကျုံ့ခြင်းသည် ပို၍ ထိရောက်သည်။ သို့သော် ဖြုတ်ပြီးနောက် ကျန်သည့် နေရာ 358 token သည်
အလွန်သေးငယ်သဖြင့် အထောက်အထား အသစ် ထည့်ရန် မလုံလောက်ပါ — ထို့ကြောင့်
history ကို ပိုကျုံ့ရမည်။

```bash
python3 - <<'PY'
W = 32768
s, t, c, n, h, u, o = 1100, 1300, 640, 12, 24000, 450, 3000
r = c * n
used = s + t + r + h + u + o
print("retrieved             ", r)
print("used                  ", used)
print("shortfall             ", used - W)
print("used share pct        ", round(100 * used / W, 1))
print("fixed share pct       ", round(100 * (s + t + h + u + o) / W, 1))
print("history share pct     ", round(100 * h / W, 1))
room = W - (s + t + h + u + o)
print("room for chunks       ", room, "chunks that fit", room // c)
print("drop                  ", n - room // c)
kept = room // c
print("free after trim       ", W - (s + t + kept * c + h + u + o))
limit = W - (s + t + r + u + o)
print("history must shrink to", limit, "tokens")
print("history cut pct       ", round(100 * (h - limit) / h, 1))
PY
```

```text
retrieved              7680
used                   37530
shortfall              4762
used share pct         114.5
fixed share pct        91.1
history share pct      73.2
room for chunks        2918 chunks that fit 4
drop                   8
free after trim        358
history must shrink to 19238 tokens
history cut pct        19.8
```

#### အဖြေ ၂ — Token အရေအတွက်နှင့် စျေးနှုန်းမှ တစ်ကြိမ်လျှင် ကုန်ကျစရိတ်

**ဖော်မြူလာ —** cost = token အရေအတွက် × USD per token၊ USD per token = စျေးနှုန်း ÷ 10⁶။
ယူဆချက် — cache မပါ၊ retry မပါ၊ output token သည် အတိအကျ 950 ဖြစ်သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. input = 4,800 × 2.50 ÷ 10⁶ = USD 0.012 ဖြစ်သည်။
2. output = 950 × 10.00 ÷ 10⁶ = USD 0.0095 ဖြစ်သည်။
3. တစ်ကြိမ်လျှင် = USD 0.0215၊ 1,000 ကြိမ်လျှင် = USD 21.50 ဖြစ်သည်။
4. USD 1 လျှင် 1 ÷ 0.0215 = 46.5 ကြိမ် ရသည်။
5. input ရှယ် = 0.012 ÷ 0.0215 = 55.8 % ဖြစ်သည်။
6. input နှစ်ဆ ဖြစ်ပါက = USD 0.0335၊ output ထက်ဝက် ဖြစ်ပါက = USD 0.01675 ဖြစ်သည်။
7. USD 0.01 တိုးရန် ထပ်လိုအပ်သည့် input token = 0.01 × 10⁶ ÷ 2.50 = 4,000 token ဖြစ်သည်။
8. token သန်းတစ်သန်းလျှင် = 0.0215 ÷ 5,750 × 10⁶ = USD 3.74 ဖြစ်သည်။

**အဓိပ္ပာယ် —** ဤ ဥပမာတွင် input သည် ကုန်ကျစရိတ်၏ 55.8 % ဖြစ်သည်၊ ဆိုလိုသည်မှာ
prompt ရှည်လာခြင်း၏ ကုန်ကျစရိတ် သက်ရောက်မှုသည် output ရှည်လာခြင်းနှင့်
နှိုင်းယှဉ်နိုင်သည့် အတိုင်းအတာ ဖြစ်သည်။ ထို့ကြောင့် prompt ကို ကျုံ့ခြင်းသည်
တန်ဖိုးရှိသည့် လုပ်ငန်း ဖြစ်သည်။

```bash
python3 - <<'PY'
i, o = 4800, 950
pi, po = 2.50, 10.00
ci = i * pi / 1e6
co = o * po / 1e6
print("input USD             ", round(ci, 6))
print("output USD            ", round(co, 6))
print("per call USD          ", round(ci + co, 6))
print("1K calls USD          ", round((ci + co) * 1000, 2))
print("calls per USD 1       ", round(1 / (ci + co), 1))
print("input share pct       ", round(100 * ci / (ci + co), 1))
print("cost if input doubles ", round(2 * ci + co, 6))
print("cost if out halves    ", round(ci + co / 2, 6))
print("breakeven extra input tokens for +1 cent", round(0.01 * 1e6 / pi))
print("USD per 1M total tokens", round((ci + co) / (i + o) * 1e6, 2))
PY
```

```text
input USD              0.012
output USD             0.0095
per call USD           0.0215
1K calls USD           21.5
calls per USD 1        46.5
input share pct        55.8
cost if input doubles  0.0335
cost if out halves     0.01675
breakeven extra input tokens for +1 cent 4000
USD per 1M total tokens 3.74
```

#### အဖြေ ၃ — Context window ကျော်လွန်မှုနှင့် ဘာကို ဖြုတ်မည်

**ဖော်မြူလာ —** used = fixed + chunk အရေအတွက် × chunk token၊
overflow = used − window၊ ထည့်နိုင်သည့် အရေအတွက် = floor((window − fixed) ÷ chunk token)။
ယူဆချက် — fixed အပိုင်းများကို ဖြတ်၍ မရပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. chunk အားလုံး = 6 × 700 = 4,200 token ဖြစ်သည်။
2. used = 6,400 + 4,200 = 10,600 token ဖြစ်သည်။
3. overflow = 10,600 − 8,192 = 2,408 token၊ window ၏ 29.4 % ဖြစ်သည်။
4. ကျန်သည့် နေရာ = 8,192 − 6,400 = 1,792 token၊ ထို့ကြောင့် chunk ၂ ခု (1,400 token) ဝင်သည်။
5. ဖြုတ်ရမည့် အရေအတွက် = 6 − 2 = 4 ခု ဖြစ်သည်။
6. ဖြုတ်ပြီးနောက် used = 7,800 token၊ ကျန်သည့် နေရာ = 392 token ဖြစ်သည်။
7. chunk ၆ ခုလုံး ဝင်စေရန် chunk တစ်ခုလျှင် = 1,792 ÷ 6 = 298.7၊ ဆိုလိုသည်မှာ 298 token သို့ ဖြတ်ရမည်။

**အဓိပ္ပာယ် —** ဤ အခြေအနေတွင် ရွေးချယ်စရာ နှစ်ခု ရှိသည် — chunk ၄ ခု ဖြုတ်ခြင်း၊
သို့မဟုတ် chunk တိုင်းကို 57 % အထိ ဖြတ်ခြင်း။ ဖြတ်ခြင်းသည် ဘယ် အပိုင်း ဆုံးရှုံးသည်ကို
မသိဘဲ ဖြစ်သည်၊ ဖြုတ်ခြင်းသည် မည်သည့် chunk မပါသည်ကို သိသည်။ ထို့ကြောင့်
ဤ ဥပမာတွင် ဖြုတ်ခြင်းက ပို၍ ထိန်းချနိုင်သည်။

```bash
python3 - <<'PY'
W, fixed, c, want = 8192, 6400, 700, 6
r = c * want
print("wanted chunks         ", want, "->", r)
print("used                  ", fixed + r)
print("overflow              ", fixed + r - W)
print("overflow pct of window", round(100 * (fixed + r - W) / W, 1))
fit = (W - fixed) // c
print("chunks that fit       ", fit)
print("must drop             ", want - fit)
print("tokens after drop     ", fixed + fit * c)
print("headroom after drop   ", W - (fixed + fit * c))
print("chunk size to fit all ", (W - fixed) // want, "tokens each")
print("truncate each chunk to", round((W - fixed) / want, 1), "tokens")
PY
```

```text
wanted chunks          6 -> 4200
used                   10600
overflow               2408
overflow pct of window 29.4
chunks that fit        2
must drop              4
tokens after drop      7800
headroom after drop    392
chunk size to fit all  298 tokens each
truncate each chunk to 298.7 tokens
```

#### အဖြေ ၄ — Cacheable prefix token နှင့် saving

**ဖော်မြူလာ —** cache မပါ = prompt စုစုပေါင်း × ခေါ်ဆိုမှု × input စျေးနှုန်း ÷ 10⁶၊
cache ပါ = prefix × ခေါ်ဆိုမှု × cache read စျေးနှုန်း ÷ 10⁶ + သီးသန့် × ခေါ်ဆိုမှု ×
input စျေးနှုန်း ÷ 10⁶။ ယူဆချက် — output စျေးနှုန်းကို နှစ်မျိုးလုံးတွင် တူညီသည် အဖြစ်
ထားသဖြင့် ထည့်မတွက်ပါ၊ prefix သည် provider ၏ စာချုပ်ကို ပြည့်မီသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. cacheable ရာခိုင်နှုန်း = 4,000 ÷ 6,000 = 66.7 % ဖြစ်သည်။
2. cache မပါ = 6,000 × 10,000 × 3.00 ÷ 10⁶ = USD 180.00 ဖြစ်သည်။
3. cache ပါ = (4,000 × 10,000 × 0.30 + 2,000 × 10,000 × 3.00) ÷ 10⁶ = 12.00 + 60.00 = USD 72.00 ဖြစ်သည်။
4. saving = USD 108.00၊ ဆိုလိုသည်မှာ 60.0 % ဖြစ်သည်။
5. စျေးနှုန်း အချိုး = 0.30 ÷ 3.00 = 0.1၊ ဆိုလိုသည်မှာ cache read သည် 10 ပုံ 1 ပုံ ဖြစ်သည်။
6. 1,000 ကြိမ်လျှင် saving = 108.00 ÷ 10 = USD 10.80 ဖြစ်သည်။
7. cache အောင်မြင်သည့် အခါ ၏ တကယ့် input စျေးနှုန်း = 72.00 ÷ (6,000 × 10,000) × 10⁶ = USD 1.20 / သန်း ဖြစ်သည်။
8. 25 % miss ဖြစ်ပါက = 0.25 × 180.00 + 0.75 × 72.00 = USD 99.00၊ saving = 45.0 % ဖြစ်သည်။

**အဓိပ္ပာယ် —** cache ၏ အကျိုးအမြတ်သည် prefix ရာခိုင်နှုန်းနှင့် စျေးနှုန်း အချိုးအပေါ်
မှီခိုသည်။ 66.7 % cacheable ဖြစ်ပြီး read စျေးနှုန်းသည် 10 ပုံ 1 ပုံ ဖြစ်သဖြင့် saving 60.0 %
ဖြစ်သည်။ miss 25 % ဖြစ်ပါက saving သည် 45.0 % သို့ ကျဆင်းသည် — ထို့ကြောင့်
miss များကို ပုံမှန် အဖြစ် သဘောထားရမည်။

```bash
python3 - <<'PY'
stable, volatile, calls = 4000, 2000, 10000
p_in, p_read = 3.00, 0.30
base = (stable + volatile) * calls * p_in / 1e6
cached = stable * calls * p_read / 1e6 + volatile * calls * p_in / 1e6
print("cacheable share pct   ", round(100 * stable / (stable + volatile), 1))
print("USD without cache     ", round(base, 2))
print("USD with cache        ", round(cached, 2))
print("USD saved             ", round(base - cached, 2))
print("saving pct            ", round(100 * (base - cached) / base, 2))
print("read price ratio      ", round(p_read / p_in, 2))
print("USD saved per 1K calls", round((base - cached) / calls * 1000, 4))
print("effective input price ", round(cached / ((stable + volatile) * calls) * 1e6, 4), "USD per 1M")
print("cost at 25 pct misses ", round(0.25 * base + 0.75 * cached, 2))
print("saving at 25 pct miss ", round(100 * (base - (0.25 * base + 0.75 * cached)) / base, 2), "pct")
PY
```

```text
cacheable share pct    66.7
USD without cache      180.0
USD with cache         72.0
USD saved              108.0
saving pct             60.0
read price ratio       0.1
USD saved per 1K calls 10.8
effective input price  1.2 USD per 1M
cost at 25 pct misses  99.0
saving at 25 pct miss  45.0 pct
```

#### အဖြေ ၅ — Schema ဖြင့် ကန့်သတ်ထားသည့် output နှင့် free text

**ဖော်မြူလာ —** တိကျမှု = အောင်မြင်သည့် item ÷ sample size၊ retry n ကြိမ်ပြီးနောက်
အောင်မြင်မှု = 1 − (ကျရှုံးမှု ဖြစ်နိုင်ခြေ)^(n+1)။ ယူဆချက် — retry တိုင်းသည် လွတ်လပ်သည်
(မအောင်မြင်မှု သည် ယခင် ကျရှုံးမှုကို မမှီခိုပါ)။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. free text = 352 ÷ 400 = 88.0 %၊ ကျရှုံး = 48 ခု ဖြစ်သည်။
2. schema = 396 ÷ 400 = 99.0 %၊ ကျရှုံး = 4 ခု ဖြစ်သည်။
3. ကျရှုံးမှု အချိုး = 48 ÷ 4 = 12.0 အဆ ဖြစ်သည်။
4. ရာခိုင်နှုန်းအမှတ် ကွာဟမှု = 11.0 ရာခိုင်နှုန်းအမှတ် ဖြစ်သည်။
5. free text: ကျရှုံးမှု ဖြစ်နိုင်ခြေ 0.12၊ တစ်ကြိမ် retry (ကြိမ် ၂) = 1 − 0.12² = 98.56 %၊
   နှစ်ကြိမ် retry (ကြိမ် ၃) = 1 − 0.12³ = 99.83 %၊ ကျန် 0.69 item ဖြစ်သည်။
6. schema: ကျရှုံးမှု ဖြစ်နိုင်ခြေ 0.01၊ တစ်ကြိမ် retry = 99.99 %၊ နှစ်ကြိမ် retry = 100.00 %,
   ကျန် 0.0 item ဖြစ်သည်။
7. schema က လူဖြင့် ပြင်ရမည့် item = 48 − 4 = 44 ခု လျှော့ပေးသည်။

**အဓိပ္ပာယ် —** Free text တွင် retry နှစ်ကြိမ် ထည့်ပါက 99.83 % သို့ ရောက်သည်၊ သို့သော်
ထို ရာခိုင်နှုန်းကို ရရှိရန် latency နှင့် ကုန်ကျစရိတ် နှစ်ကြိမ် ကျခံရသည်။ Schema ဖြင့်
ကန့်သတ်ထားသည့် output သည် ပထမ ကြိမ်းမှာပင် 99.0 % ရသည်၊ ထို့ကြောင့် retry
ကုန်ကျစရိတ်ကို ရှောင်ရှားသည်။ သို့သော် ဤ တိုင်းတာချက်သည် **ပုံစံ** ကို သာ တိုင်းသည်၊
**အကြောင်းအရာ မှန်ကန်မှု** ကို မတိုင်းပါ — ထို အချက်ကို သီးခြားစီ စစ်ရမည်။

```bash
python3 - <<'PY'
n, free_ok, schema_ok = 400, 352, 396
print("free text ok          ", free_ok, round(100 * free_ok / n, 1), "pct")
print("schema ok             ", schema_ok, round(100 * schema_ok / n, 1), "pct")
print("free failures         ", n - free_ok)
print("schema failures       ", n - schema_ok)
print("failure ratio         ", round((n - free_ok) / (n - schema_ok), 1), "x")
print("pt difference         ", round(100 * (schema_ok - free_ok) / n, 1))
for label, ok in (("free", free_ok), ("schema", schema_ok)):
    pf = 1 - ok / n
    print(f"{label}: p_fail {pf:.4f} -> after 1 retry {100*(1-pf**2):.2f} pct,"
          f" after 2 retries {100*(1-pf**3):.2f} pct, residual {round(n*pf**3, 2)} items")
print("residual failures, free 3 attempts", round(n * (1 - free_ok / n) ** 3, 2))
print("manual fixes saved by schema   ", (n - free_ok) - (n - schema_ok))
PY
```

```text
free text ok           352 88.0 pct
schema ok              396 99.0 pct
free failures          48
schema failures        4
failure ratio          12.0 x
pt difference          11.0
free: p_fail 0.1200 -> after 1 retry 98.56 pct, after 2 retries 99.83 pct, residual 0.69 items
schema: p_fail 0.0100 -> after 1 retry 99.99 pct, after 2 retries 100.00 pct, residual 0.0 items
residual failures, free 3 attempts 0.69
manual fixes saved by schema    44
```

#### အဖြေ ၆ — Prompt ရှည်လာသည့်အခါ latency သက်ရောက်မှု

**ဖော်မြူလာ —** prefill ms = prompt token ÷ prefill throughput × 1000၊
စုစုပေါင်း ms = overhead + prefill ms + output token × output token တစ်ခုလျှင် ms။
ယူဆချက် — prefill throughput သည် prompt အရှည်နှင့် မပြောင်းလဲဘဲ တည်ငြိမ်သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. ပုံမှန် prefill = 1,200 ÷ 2,500 × 1000 = 480.0 ms ဖြစ်သည်။
2. ရှည်သည့် prefill = 9,600 ÷ 2,500 × 1000 = 3,840.0 ms ဖြစ်သည်။
3. ကွာဟမှု = 3,360.0 ms၊ prompt အချိုး = 8.0 ဆ ဖြစ်သည်။
4. output = 200 × 18 = 3,600 ms ဖြစ်သည်။
5. ပုံမှန် စုစုပေါင်း = 200 + 480 + 3,600 = 4,280.0 ms ဖြစ်သည်။
6. ရှည်သည့် စုစုပေါင်း = 200 + 3,840 + 3,600 = 7,640.0 ms ဖြစ်သည်၊ အချိုး = 1.79 ဖြစ်သည်။
7. တိုးသည့် ပမာဏ = 3,360.0 ms၊ ဆိုလိုသည်မှာ ပုံမှန် စုစုပေါင်း၏ 78.5 % ဖြစ်သည်။
8. prefill ရှယ် = 480.0 ÷ 4,280 = 11.2 % မှ 3,840 ÷ 7,640 = 50.3 % သို့ တက်သည်။
9. ပုံမှန် စုစုပေါင်း အတူတူ ရရှိရန် prefill throughput = 9,600 ÷ 0.48 = 20,000 token/s လိုအပ်သည်။

**အဓိပ္ပာယ် —** Prompt ရှစ်ဆ ရှည်လာသည့်အခါ စုစုပေါင်း latency သည် 1.79 ဆ ဖြစ်သည် —
ဆိုလိုသည်မှာ တိုးလာမှု တိုင်းသည် prefill မှ လာသည်။ ပိုရှည်သည့် prompt ကို ရွေးပါက
prefill throughput ကို ဆယ်ဆနီးပါး တိုးမှသာ မူလ latency ကို ထိန်းနိုင်သည်။ ထို့ကြောင့်
prompt token သည် ကုန်ကျစရိတ်သာ မဟုတ်၊ ခဏတာ (latency) ကိုလည်း တိုက်ရိုက် ဆုံးဖြတ်သည်။

```bash
python3 - <<'PY'
tps, overhead, base, longp, out, step = 2500.0, 200.0, 1200, 9600, 200, 18.0
bp = base / tps * 1000
lp = longp / tps * 1000
print("base prefill ms       ", round(bp, 1))
print("long prefill ms       ", round(lp, 1))
print("added prefill ms      ", round(lp - bp, 1))
print("prompt ratio          ", round(longp / base, 1))
print("decode ms             ", out * step)
bt = overhead + bp + out * step
lt = overhead + lp + out * step
print("base total ms         ", round(bt, 1))
print("long total ms         ", round(lt, 1))
print("total ratio           ", round(lt / bt, 2))
print("added total ms        ", round(lt - bt, 1))
print("added share of base   ", round(100 * (lt - bt) / bt, 1), "pct")
print("prefill share base    ", round(100 * bp / bt, 1), "pct")
print("prefill share long    ", round(100 * lp / lt, 1), "pct")
print("prefill tps to hold base total", round(longp / ((bt - overhead - out * step) / 1000), 1))
PY
```

```text
base prefill ms        480.0
long prefill ms        3840.0
added prefill ms       3360.0
prompt ratio           8.0
decode ms              3600.0
base total ms          4280.0
long total ms          7640.0
total ratio            1.79
added total ms         3360.0
added share of base    78.5 pct
prefill share base     11.2 pct
prefill share long     50.3 pct
prefill tps to hold base total 20000.0
```

### ၅.၂ ပြဿနာ ရှာဖွေခြင်း အဖြေများ

#### အဖြေ ၁ — Session နောက်ပိုင်းတွင် ညွှန်ကြားချက် လိုက်နာမှု ကျဆင်းခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** အထောက်အထား တည်နေရာအလိုက် မော်ဒယ် စွမ်းဆောင်ရည်
ပြောင်းလဲပြီး သက်ဆိုင်သည့် အချက်အလက်သည် အစနှင့် အဆုံးကြား တွင် ရှိသည့်အခါ
ကျဆင်းနိုင်သည် (Lost in the Middle)။ Session အစတွင် system ညွှန်ကြားချက်သည်
prompt အစပိုင်းတွင် ရှိသဖြင့် ထင်ရှားသည်။ history ကြီးထွားလာသည့်အခါ ထို
ညွှန်ကြားချက်သည် အလယ်ပိုင်းသို့ ရောက်သွားပြီး နောက်ဆုံးတွင် ပို၍ နက်သော
နေရာတွင် ရှိလာသည်။ ထို့ကြောင့် window အတွင်း ဝင်နေဆဲ ဖြစ်သော်လည်း
ယုံကြည်စိတ်ချစွာ အသုံးပြုခံရမှု ကျဆင်းသည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** turn တစ်ခုလျှင် input token နှင့် history ၏ ရာခိုင်နှုန်းကို
တိုင်းပါ။ history သည် window ၏ 70 % ကျော်လာပါက အကြောင်းရင်း (၁) ဖြစ်သည်။
ကန့်သတ်ချက် စာသားကို prompt အစပိုင်းတွင် ပြန်ထားပြီး စမ်းကြည့်ပါ — လိုက်နာမှု
ပြန်ကောင်းလာပါက တည်နေရာ ဖြစ်သည် (အကြောင်းရင်း ၁)။ မကောင်းလာပါက compaction
လုပ်ခဲ့မှု (အကြောင်းရင်း ၂) ကို စစ်ပါ။ retrieved စာသားကို ဖယ်၍ စမ်းကြည့်ပါ —
ပြန်ကောင်းလာပါက အကြောင်းရင်း (၃) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** ကန့်သတ်ချက်များကို အစပိုင်းတွင် ထား၍ နောက်ဆုံး
turn ၏ အနီးတွင် ပြန်လည် အကျဉ်းချုံး ဖော်ပြပါက လိုက်နာမှု ပြန်တက်လာသည်ကို
eval set အပေါ် တိုင်းရမည်။ History ကို အနှစ်ချုပ်ရာတွင် ကန့်သတ်ချက်နှင့် identifier များ
စာလုံးတိုင်း ပါမပါ စစ်ရမည်၊ အကြောင်းမှာ ချုံ့ခြင်းသည် lossy ဖြစ်သောကြောင့် ဖြစ်သည်။

#### အဖြေ ၂ — အလုပ်ပမာဏ များလာသည့်အခါ format ကျိုးခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** Output format ကို prompt တွင် စာသားဖြင့်သာ
ဖော်ပြထားပါက မော်ဒယ်သည် ထို format ကို လိုက်နာရန် ကြိုးစားသည်၊ သို့သော်
အာမခံချက် မရှိပါ။ Prompt sensitivity ကြောင့် အဓိပ္ပာယ် တူညီသည့် မူကွဲများ၏
ရလဒ်သည် ကွာဟနိုင်သည်။ စမ်းသပ်သည့် eval set သည် မူကွဲ တစ်ခုတည်းကို
ကိုယ်စားပြုပါက ထို ကွာဟမှုကို ဖုံးကွယ်ထားသည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** parse/validate ကျရှုံးမှုကို အချိန်နှင့်အမျှ တိုင်းပါ။
အချိန်နှင့်အမျှ တိုးနေပြီး decoding setting မပြောင်းလဲပါက အကြောင်းရင်း (၃) ဖြစ်သည်။
schema-constrained decoding ကို ဖွင့်၍ ပြန်တိုင်းပါ — ကျရှုံးမှု သုညနီးပါး ဖြစ်သွားပါက
အကြောင်းရင်း (၁) ဖြစ်သည်။ မပြောင်းလဲပါက demonstration အရေအတွက်နှင့်
လွှမ်းခြုံမှုကို စစ်ပါ (အကြောင်းရင်း ၂)။ မူကွဲအလိုက် ကွာဟမှု ကြီးပါက အကြောင်းရင်း (၄) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** schema ဖြင့် ကန့်သတ်ထားသည့် output သည်
ပုံစံ ကျရှုံးမှုကို ပထမ ကြိမ်းတွင် ဖယ်ရှားနိုင်သည်၊ သို့သော် အကြောင်းအရာ မှန်ကန်မှုကို
မအာမခံပါ။ ထို့ကြောင့် verification gate ကို ဆက်ထားရမည်။ မူကွဲများအားလုံးကို
regression test ထဲ ထည့်ပြီးနောက် ကျရှုံးမှု ရာခိုင်နှုန်းသည် လက်ခံနိုင်သည့် အဆင့်သို့
ရောက်မှသာ ထို prompt ကို ထားရှိရမည်။

#### အဖြေ ၃ — Retrieved စာရွက်စာတမ်းက အပြုအမူ ပြောင်းလဲခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** Agent စနစ်များသည် ယုံကြည်ရသည့် ပန်းတိုင်များနှင့်
ပြင်ပ စာသားများကို ရောနှောထားသည်။ ပြင်ပ စာသားသည် ပုံစံအားဖြင့် ညွှန်ကြားချက်နှင့်
တူနိုင်သဖြင့် မော်ဒယ်က ၎င်းကို အခွင့်အာဏာ မြင့်သည့် ညွှန်ကြားချက် အဖြစ် ဖတ်နိုင်သည်
(prompt injection)။ ဤ အခြေအနေတွင် မော်ဒယ်နှင့် harness သည် အခွင့်အာဏာ
မတူညီသည့် ညွှန်ကြားချက်များ ပဋိပက္ခဖြစ်သည့်အခါ ဖြေရှင်းသည့် စည်းမျဉ်း
(Instruction Hierarchy) ကို လိုအပ်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** ထို စာသားကို ဖယ်လိုက်ပါ — အပြုအမူ ပြန်ကောင်းလာပါက
အကြောင်းရင်း (၁) ဖြစ်သည်။ စာသားကို data အဖြစ် အမှတ်အသားပြု၍ ပြန်စမ်းပါ —
လျော့သွားပါက အမှတ်အသားပြုမှု မလုံလောက်ခြင်း ဖြစ်သည်။ tool ခွင့်ပြုချက်ကို
ကန့်သတ်၍ ပြန်စမ်းပါ — tool ခေါ်ဆိုမှု ကျဆင်းပါက အကြောင်းရင်း (၃) ဖြစ်သည်။
ပဋိပက္ခ စမ်းသပ်မှု မရှိခဲ့ပါက အကြောင်းရင်း (၄) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** အမှတ်အသားပြုခြင်းနှင့် ဦးစားပေး မြင့်သည့်
ကန့်သတ်ချက်များကို ထို အကြောင်းအရာ၏ အပြင်ဘက်တွင် ထားခြင်းသည်
အပြုအမူကို တိုးတက်စေနိုင်သည်၊ သို့သော် လုံခြုံရေး နယ်နိမိတ် တစ်ခု မဟုတ်ပါ။
ထို့ကြောင့် least privilege နှင့် အတည်ပြုချက် ထိန်းချုပ်မှုများကို အကျိုးဆက်
ကန့်သတ်မှု အဖြစ် ဆက်ထားရမည်၊ ထို့နောက် တိုက်ရိုက်နှင့် သွယ်ဝိုက်သည့်
ပဋိပက္ခ အမှုများကို regression test များတွင် ထည့်ရမည်။

### ၅.၃ ဆုံးဖြတ်ချက် အဖြေများ

#### အဖြေ ၁ — ရှည်သည့် တည်ငြိမ် prefix နှင့် cache

**ရှင်းလင်းချက် —** prefix 6,600 token သည် prompt စုစုပေါင်း 13,148 token ၏ 50.2 % ဖြစ်သည်။
Window 16,384 အတွင်း ကျန်သည့် နေရာ 3,236 token ဖြစ်သည်။ cache မပါပါက
prefix အတွက် ခေါ်ဆိုမှု 20,000 လျှင် USD 396.00 ဖြစ်သည်၊ cache ပါပါက USD 39.60 ဖြစ်သည်၊
ဆိုလိုသည်မှာ 90.0 % သက်သာသည်။

**ဆုံးဖြတ်ချက် —** ရွေးချယ်မှု A ကို ရွေးရမည် — ရှည်သည့် system prompt နှင့်
ပုံသေ demonstration များကို တူညီသည့် အစဉ်အတိုင်း အစပိုင်းတွင် ထားရမည်။
သို့သော် ဤဆုံးဖြတ်ချက်သည် **တည်ငြိမ်မှု** အပေါ် အခြေခံသည် — prefix ကို
တစ်စိတ်တစ်ပိုင်း ပြောင်းလဲတိုင်း cache ပျက်သည်၊ provider အလိုက် အရည်အချင်းနှင့်
သက်တမ်း ကွာခြားသည်။ ထို့ကြောင့် miss များကို ပုံမှန် အဖြစ် သဘောထားပြီး
hit rate ကို စောင့်ကြည့်ရမည်။

**တိုင်းတာမည့် metric —** cache hit rate၊ တစ် သန်း input token လျှင် USD၊ eval set အပေါ်
တိကျမှု၊ prefix ကို ပြောင်းလဲရသည့် အကြိမ်အရေအတွက် (တည်ငြိမ်မှု၏ တိုင်းတာချက်)။

```bash
python3 - <<'PY'
system, examples, retrieved, history, out = 2600, 4000, 3000, 1500, 2048
W, calls, p_in, p_read = 16384, 20000, 3.00, 0.30
used = system + examples + retrieved + history + out
print("stable prefix tokens  ", system + examples)
print("volatile tokens       ", retrieved + history + out)
print("used                  ", used)
print("headroom              ", W - used)
no_cache = (system + examples) * calls * p_in / 1e6
cached = (system + examples) * calls * p_read / 1e6
print("prefix USD no cache   ", round(no_cache, 2))
print("prefix USD cached     ", round(cached, 2))
print("USD saved per month   ", round(no_cache - cached, 2))
print("saving pct of prefix  ", round(100 * (no_cache - cached) / no_cache, 1))
print("prefix share of prompt", round(100 * (system + examples) / used, 1), "pct")
PY
```

```text
stable prefix tokens   6600
volatile tokens        6548
used                   13148
headroom               3236
prefix USD no cache    396.0
prefix USD cached      39.6
USD saved per month    356.4
saving pct of prefix   90.0
prefix share of prompt 50.2 pct
```

#### အဖြေ ၂ — အထောက်အထု အတိုင်းအတာနှင့် တည်နေရာ

**ရှင်းလင်းချက် —** Window 8,192 token တွင် ပုံသေ အပိုင်းများ 5,200 token ဖြစ်သဖြင့်
ကျန်သည့် နေရာ 2,992 token ဖြစ်သည်၊ ဆိုလိုသည်မှာ chunk ၄ ခု (2,480 token) ဝင်သည်။
chunk တစ်ခုလျှင် 620 token ဖြစ်သည့်အတွက် chunk ၆ ခု ထည့်လိုပါက chunk တိုင်းကို
498 token သို့ ဖြတ်ရမည်၊ ဆိုလိုသည်မှာ chunk တိုင်း၏ ပဉ္စမုခ်ခန့် ဆုံးရှုံးသည်။

**ဆုံးဖြတ်ချက် —** chunk အရေအတွက်ကို ၄ ခုတွင် ထား၍ chunk တိုင်းကို
အပြည့်အစုံ ထိန်းရမည်။ ထို့နောက် ဆုံးဖြတ်ချက်အတွက် အရေးပါသည့် အထောက်အထားကို
အစပိုင်း သို့မဟုတ် အဆုံးပိုင်းတွင် ထားရမည်၊ အကြောင်းမှာ အလယ်ပိုင်းသည်
22.0 ရာခိုင်နှုန်းအမှတ် နိမ့်သည့် အပြုအမူ ပြသည်။ chunk ၆ ခုမှ ၃ ခုသို့ လျှော့ခြင်းသည်
1,860 token (22.7 %) လွတ်စေပြီး prefill 744 ms သက်သာသည်၊ သို့သော် ထို နေရာကို
အထောက်အထား ထပ်ထည့်ရန် မဟုတ်ဘဲ output အတွက် ချန်ထားရမည်။

**တိုင်းတာမည့် metric —** eval set အပေါ် အဖြေ တိကျမှု (တည်နေရာ တစ်ခုစီအတွက်
သီးခြားစီ)၊ grounding စစ်ဆေးမှု အောင်မြင်မှု၊ TTFT p50။

```bash
python3 - <<'PY'
W, fixed, chunk, want = 8192, 5200, 620, 6
room = W - fixed
print("room for chunks       ", room, "chunks that fit", room // chunk)
for name, lo, hi in (("start", 0.91, 0.93), ("middle", 0.71, 0.76), ("end", 0.88, 0.90)):
    print(f"{name:7} accuracy {round(100*lo,1)}-{round(100*hi,1)} pct")
print("position spread pt    ", round(100 * (0.93 - 0.71), 1))
print("cost of 6 chunks      ", want * chunk, "tokens")
print("cost of 3 chunks      ", 3 * chunk, "tokens")
print("tokens freed going 6->3", 3 * chunk)
print("chunk tokens freed pct", round(100 * 3 * chunk / W, 1))
print("prefill ms saved      ", round(3 * chunk / 2500.0 * 1000, 1))
print("accuracy if middle only", round(100 * 0.71, 1), "pct")
print("accuracy if edges used ", round(100 * 0.93, 1), "pct")
print("gain by reordering pt  ", round(100 * (0.93 - 0.71), 1))
PY
```

```text
room for chunks        2992 chunks that fit 4
start   accuracy 91.0-93.0 pct
middle  accuracy 71.0-76.0 pct
end     accuracy 88.0-90.0 pct
position spread pt     22.0
cost of 6 chunks       3720 tokens
cost of 3 chunks       1860 tokens
tokens freed going 6->3 1860
chunk tokens freed pct 22.7
prefill ms saved       744.0
accuracy if middle only 71.0 pct
accuracy if edges used  93.0 pct
gain by reordering pt   22.0
```

## Self-check

၁။ အပိုင်း ၅.၁ အဖြေ ၁ တွင် window ကျော်လွန်မှု၏ အကြီးဆုံး အရင်းအမြစ်သည်
မည်သည့် အပိုင်း ဖြစ်သည်၊ ထို အပိုင်းကို မည်မျှ ဖြတ်ရမည်။

၂။ အပိုင်း ၅.၁ အဖြေ ၂ တွင် output ထက်ဝက် လျှော့ခြင်းနှင့် input နှစ်ဆ တိုးခြင်း၏
ကုန်ကျစရိတ် သက်ရောက်မှုကို နှိုင်းယှဉ်ပါ။

၃။ အပိုင်း ၅.၁ အဖြေ ၅ တွင် schema ဖြင့် ကန့်သတ်ထားသည့် output သည်
မည်သည့် အချက်ကို အာမခံပြီး၊ မည်သည့် အချက်ကို မအာမခံသနည်း။

၄။ အပိုင်း ၅.၁ အဖြေ ၆ တွင် prompt ရှစ်ဆ ရှည်လာသည့်အခါ prefill ရှယ်သည်
မည်သို့ ပြောင်းလဲသည်၊ အဘယ်ကြောင့် နည်း။

၅။ အပိုင်း ၅.၃ အဖြေ ၂ တွင် chunk များကို မည်သည့် အစဉ်အတိုင်း ထားရမည်၊
ထို ဆုံးဖြတ်ချက်သည် မည်သည့် term အပေါ် အခြေခံသည်။

<details>
<summary>အဖြေများ</summary>

၁။ conversation history ဖြစ်သည်၊ 24,000 token (window ၏ 73.2 %) ဖြစ်သည်။
history ကို 19,238 token အထိ ကျုံ့ရမည်၊ ဆိုလိုသည်မှာ 19.8 % ဖြတ်ရမည်။

၂။ output ထက်ဝက် လျှော့ပါက USD 0.0215 မှ USD 0.01675 သို့ ကျဆင်းသည် (−22.1 %)။
input နှစ်ဆ တိုးပါက USD 0.0335 သို့ တက်သည် (+55.8 %)။ ထို့ကြောင့် ဤ အခြေအနေတွင်
input တိုးခြင်း၏ သက်ရောက်မှုသည် output လျှော့ခြင်း၏ သက်ရောက်မှုထက် ကြီးသည်။

၃။ ပုံစံ (parse ဖြစ်မှု၊ schema နှင့် ကိုက်မှု) ကို အာမခံသည်၊ ဆိုလိုသည်မှာ 99.0 %
ဖြစ်သည်။ အကြောင်းအရာ မှန်ကန်မှုကို မအာမခံပါ၊ ထို့ကြောင့် verification gate ကို
ဆက်ထားရမည်။

၄။ prefill ရှယ်သည် 11.2 % မှ 50.3 % သို့ တက်သည်။ အကြောင်းမှာ output (200 token) နှင့်
ပုံသေ overhead သည် မပြောင်းလဲဘဲ prefill token သာ ရှစ်ဆ တိုးသောကြောင့် ဖြစ်သည်။

၅။ ဆုံးဖြတ်ချက်အတွက် အရေးပါသည့် အထောက်အထားကို အစပိုင်း သို့မဟုတ်
အဆုံးပိုင်းတွင် ထား၍ အရေးပါမှု နည်းသည့် chunk များကို အလယ်ပိုင်းတွင် ထားရမည်။
ဤ ဆုံးဖြတ်ချက်သည် Lost in the Middle အပေါ် အခြေခံသည်၊ ၎င်းသည် လေ့လာ
တွေ့ရှိထားသည့် အပြုအမူ ပုံစံ ဖြစ်သဖြင့် မော်ဒယ် တိုင်းအတွက် တူညီသည့် ပုံသေ နိယာမ
မဟုတ်ပါ။

</details>

## References

- နယ်ပယ် အခြေခံ အချက်အလက် — `terms/05_prompting_and_context.md` နှင့်
  `glossary/by_area/05_prompting_and_context.json`။
- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary)
  — MIT licensed, from `rohitg00/ai-engineering-from-scratch`။
- လက်တွေ့ lab များ — `labs/lab_token_budget.py`၊ `labs/lab_prefix_cache.py`၊
  `labs/lab_shape_prompt.py` (တစ်ပြိုင်နက် ရေးသားနေသည်)။
- ကိန်းဂဏန်း တိုင်း၏ ရင်းမြစ် script —
  `~/.hermes/profiles/ai-engineer/cache/scratch/glossary_guide_05/calc.py`။
- Papers: [The Instruction Hierarchy](https://arxiv.org/abs/2404.13208)၊
  [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/)၊
  [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)။
