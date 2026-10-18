# ၀၄ — လေ့ကျင့်ခန်းများနှင့် အဖြေများ (Reliability & Operations)

ဤဖိုင်သည် နယ်ပယ် ၁၀ ၏ term ၁၇ ခုကို အသုံးပြု၍ တွက်ချက်ခြင်း၊ ပြဿနာ ရှာဖွေခြင်းနှင့် ဆုံးဖြတ်ချက် ချခြင်း
လေ့ကျင့်ခန်းများကို စုစည်းထားသည်။ အပိုင်း ၁ တွင် အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာ လေးခု၊ အပိုင်း ၂ တွင်
တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ခြောက်ခု၊ အပိုင်း ၃ တွင် ပြဿနာ ရှာဖွေခြင်း သုံးခု၊ အပိုင်း ၄ တွင်
ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း နှစ်ခု ပါဝင်သည်။ အပိုင်း ၅ တွင် အဖြေတိုင်းကို ဖော်မြူလာ၊ တွက်ချက်မှု အဆင့်ဆင့်နှင့်
အကြောင်းရင်း ရှင်းလင်းချက်နှင့်အတူ ပေးထားသည်။

အပိုင်း ၁၊ ၅.၁ နှင့် ၅.၃ တွင် ပါဝင်သည့် ကိန်းဂဏန်း တိုင်းသည် Python (standard library သာ) ဖြင့်
အမှန်တကယ် လုပ်ဆောင်ခဲ့သည့် တွက်ချက်မှု၏ output ဖြစ်သည်။ ဖော်ပြထားသည့် block အတိုင်း run လုပ်ပါက
တူညီသည့် output ကို ပြန်လည် ရရှိမည်။ ကိန်းဂဏန်း တိုင်းသည် သတ်မှတ်ထားသည့် ယူဆချက် (assumption)
အပေါ် မှီခိုသဖြင့် ဖော်မြူလာ တစ်ခုစီနှင့်အတူ ၎င်း၏ ယူဆချက်ကို ဖော်ပြထားသည်။

**အသုံးပြုသည့် ယူဆချက် အခြေခံ** — SLO 99.9% အောင်မြင်မှု၊ 30-day measurement window၊ eligible request
2,000,000 ခု၊ peak demand 2,000 rps။ ဝန်ဆောင်မှု တစ်ခုလျှင် ပျမ်းမျှ service time 400 ms နှင့် server ၈ ခု
(useful capacity 20 rps) ကို queueing ဥပမာတွင် သုံးသည်။ ငွေကြေး ဂဏန်းများ (worker-hour စျေးနှုန်း၊
request တစ်ခု၏ တန်ဖိုး၊ စာချုပ် ပမာဏ) သည် အဖွဲ့အစည်း အလိုက် ကွာခြားသဖြင့် အဖြေ၏ **ပုံသဏ္ဍာန်** ကို
ကြည့်ရမည်၊ ဂဏန်း တိကျမှုကို မဟုတ်ပါ။

## ၁။ အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာများ (Worked Examples)

### ဥပမာ ၁ — SLO မှ error-budget policy သို့

**ယူဆချက် —** SLO သည် 99.9% အောင်မြင်မှု၊ measurement window သည် 30 ရက် (43,200 မိနစ်)။

**ဖော်မြူလာ —**
- error budget fraction = 1 − SLO
- error budget (requests) = (1 − SLO) × eligible requests
- error budget (minutes) = (1 − SLO) × window minutes
- burn rate = observed failure rate ÷ (1 − SLO)
- budget ကုန်သည့် အချိန် = window ÷ burn rate
- window တစ်ခုအတွင်း ကုန်သည့် % = burn rate × (window length ÷ measurement window)

**တွက်ချက်မှု —**
1. budget fraction = 1 − 0.999 = 0.001 ဖြစ်သည်။
2. budget = 2,000,000 × 0.001 = 2,000 request ဖြစ်သည်။
3. budget = 30 × 24 × 60 × 0.001 = 43.2 မိနစ် ဖြစ်သည်။
4. လေ့လာတွေ့ရှိသည့် မအောင်မြင်နှုန်း 0.5% ဖြစ်ပါက burn rate = 0.005 ÷ 0.001 = 5x ဖြစ်သည်၊
   budget သည် 30 ÷ 5 = 6 ရက် အတွင်း ကုန်သည်။
5. မအောင်မြင်နှုန်း 1% ဖြစ်ပါက burn rate = 10x၊ budget သည် 3 ရက် အတွင်း ကုန်သည်။
6. fast burn alert ကို "1 h window တွင် budget ၏ 2% ကုန်သည်" ဟု သတ်မှတ်ပါက ထို သတ်မှတ်ချက်သည်
   burn rate 14.4x နှင့် တူညီသည်။ slow burn alert ကို "6 h window တွင် 5% ကုန်သည်" ဟု သတ်မှတ်ပါက
   burn rate 6x နှင့် တူညီသည်။

**ကောက်ချက် —** error budget သည် "မည်မျှ မအောင်မြင်နိုင်" ကို **တစ်ခုတည်းသော ကိန်းဂဏန်း** အဖြစ်
ပြောင်းလဲပေးသဖြင့် release အလုပ်နှင့် reliability အလုပ်သည် တူညီသည့် နယ်နိမိတ်ကို မြင်နိုင်သည်။ alert ကို
**burn rate** အပေါ် သတ်မှတ်ခြင်းသည် မအောင်မြင်မှု ရာခိုင်နှုန်း အပေါ် သတ်မှတ်ခြင်းထက် ပို၍ အသုံးဝင်သည် —
burn rate သည် "budget ဘယ်တော့ ကုန်မည်" ကို တိုက်ရိုက် ပြောသည်။

```bash
python3 - <<'PY'
slo = 0.999
window_days = 30
window_minutes = window_days * 24 * 60
print("window minutes", window_minutes, " budget fraction", round(1 - slo, 3))
print()
print(" burn rate   budget spent per 1 h   budget spent per 6 h   exhausted in (days)")
for burn in (1.0, 2.0, 6.0, 14.4, 36.0):
    per_hour = burn / window_minutes * 60 * 100
    per_six = burn / window_minutes * 360 * 100
    print(f"{burn:>10.1f}x {per_hour:>21.3f}% {per_six:>23.2f}% {window_days / burn:>19.2f}")
print()
print("fast burn alert: page when a 1 h window spends 2% of the budget -> burn =",
      round(0.02 * window_minutes / 60, 1), "x")
print("slow burn alert: page when a 6 h window spends 5% of the budget -> burn =",
      round(0.05 * window_minutes / 360, 1), "x")
PY
```


```text
window minutes 43200  budget fraction 0.001

 burn rate   budget spent per 1 h   budget spent per 6 h   exhausted in (days)
       1.0x                 0.139%                    0.83%               30.00
       2.0x                 0.278%                    1.67%               15.00
       6.0x                 0.833%                    5.00%                5.00
      14.4x                 2.000%                   12.00%                2.08
      36.0x                 5.000%                   30.00%                0.83

fast burn alert: page when a 1 h window spends 2% of the budget -> burn = 14.4 x
slow burn alert: page when a 6 h window spends 5% of the budget -> burn = 6.0 x
```


### ဥပမာ ၂ — Admission Control တွင် request ၏ ကုန်ကျစရိတ်ကို ခန့်မှန်းခြင်း

**ယူဆချက် —** request ၏ ကုန်ကျစရိတ်ကို `base 40 ms + 0.35 ms × prompt token` ဖြင့် ခန့်မှန်းသည်။
admission capacity ကို 2,000 slot-ms/second ဟု သတ်မှတ်သည်။

**ဖော်မြူလာ —**
- estimated cost (ms) = base + ms_per_token × prompt tokens
- admitted requests per second = capacity (slot-ms/s) ÷ estimated cost (ms)

**တွက်ချက်မှု —**
1. prompt 200 token: 40 + 0.35 × 200 = 110 ms ဖြစ်သည်၊ ထို့ကြောင့် တစ်စက္ကန့်လျှင် 2,000 ÷ 110 = 18.18
   request လက်ခံနိုင်သည်။
2. prompt 1,000 token: 390 ms → 5.13 request/s ဖြစ်သည်။
3. prompt 3,000 token: 1,090 ms → 1.83 request/s ဖြစ်သည်။
4. prompt 8,000 token: 2,840 ms ဖြစ်သည် — ဤအရာသည် တစ်စက္ကန့် capacity (2,000 slot-ms) ကို
   တစ်ခုတည်းဖြင့် ကျော်လွန်သဖြင့် admission သည် ထို request ကို budget သိမ်းဆည်း၍ serialise လုပ်ရမည်။
5. prompt 32,000 token: 11,240 ms → 0.18 request/s ဖြစ်သည်။

**ကောက်ချက် —** request တိုင်း၏ ကုန်ကျစရိတ်သည် **အလွန်ကွာခြားသည်**၊ ထို့ကြောင့် request အရေအတွက်
ဖြင့်သာ ကန့်သတ်ခြင်း (rate limit) သည် capacity ကို မကာကွယ်နိုင်ပါ — ကြီးသည့် request အပိုင်းက
capacity တစ်ခုလုံးကို ကုန်စေနိုင်သည်။ Admission Control သည် ကုန်ကျစရိတ် ခန့်မှန်းချက်ကို
စစ်ဆေးပြီး လိုအပ်သည့် budget ကို atomically သိမ်းဆည်းရမည်။

```bash
python3 - <<'PY'
base_ms = 40.0
ms_per_token = 0.35
slot_ms_per_s = 2000.0
print("cost estimate = base", base_ms, "ms +", ms_per_token, "ms per prompt token")
print("admission capacity =", slot_ms_per_s, "slot-ms per second")
print()
print(" prompt tokens   estimated cost ms   admitted requests per second")
for tokens in (200, 1000, 3000, 8000, 32000):
    cost = base_ms + ms_per_token * tokens
    rps = slot_ms_per_s / cost
    print(f"{tokens:>14d} {cost:>19.1f} {rps:>31.2f}")
print()
mixed = 3000
print("a", mixed, "token request needs", round(base_ms + ms_per_token * mixed, 1),
      "slot-ms, so a single request may have to be serialised when the budget is low")
PY
```


```text
cost estimate = base 40.0 ms + 0.35 ms per prompt token
admission capacity = 2000.0 slot-ms per second

 prompt tokens   estimated cost ms   admitted requests per second
           200               110.0                           18.18
          1000               390.0                            5.13
          3000              1090.0                            1.83
          8000              2840.0                            0.70
         32000             11240.0                            0.18

a 3000 token request needs 1090.0 slot-ms, so a single request may have to be serialised when the budget is low
```


### ဥပမာ ၃ — Circuit breaker ၏ window၊ threshold နှင့် probe ဝန်

**ယူဆချက် —** rolling window သည် request 20 ခု၊ အနည်းဆုံး sample 10 ခု ရရှိမှ ဆုံးဖြတ်သည်၊
failure threshold သည် 50%။ ချို့ယွင်းနေသည့် dependency သည် 80% ကျဆင်းသည်။ open duration သည်
30 စက္ကန့် ဖြစ်ပြီး half-open တွင် probe 5 ခု ပို့သည်၊ 5 ခုအနက် 4 ခု အောင်မြင်ပါက breaker ပြန်ပိတ်သည်
(`closed`)။

**ဖော်မြူလာ —**
- trip ဖြစ်သည့် အချက် = ပထမ ဆုံး sample အရေအတွက် (min_samples) ပြည့်ပြီး failure rate ≥ threshold ဖြစ်သည့် request
- open အခြေအနေတွင် probe rate = probes ÷ open duration
- load reduction = 1 − (probe rate ÷ offered rate)
- probe များ လုံလောက်စွာ မအောင်မြင်ဘဲ ပြန်ပိတ်သည့် ဖြစ်နိုင်ခြေ = P(successes ≥ 4 | 5 probes, p)

**တွက်ချက်မှု —**
1. min_samples 10 ပြည့်သည့် အချိန်တွင် request 10 ခုအနက် 8 ခု ကျဆင်းသဖြင့် failure rate 80% ဖြစ်သည်၊
   threshold 50% ကို ကျော်လွန်သဖြင့် breaker သည် request 10 ခုတွင် trip ဖြစ်သည်။
2. open အခြေအနေတွင် offered 20 rps မှ 5 ÷ 30 = 0.167 rps အထိ ကျသဖြင့် ဝန် လျော့မှုသည် 99.17% ဖြစ်သည်။
3. dependency သည် ယခုတိုင် 20% သာ အောင်မြင်ပါက half-open တွင် ပြန်ပိတ်သည့် ဖြစ်နိုင်ခြေ = 0.00672
   (0.67%) ဖြစ်သည်၊ ဆိုလိုသည်မှာ probe 5 ခု ဖြင့် လုံလောက်သည်။
4. dependency ကောင်းမွန်ပါက ပထမ probe round တွင် ပြန်ပိတ်သဖြင့် recovery ကို 30 စက္ကန့် အတွင်း
   ဖော်ထုတ်နိုင်သည်။

**ကောက်ချက် —** breaker ၏ **probe ဝန်** သည် အဓိက အချက် ဖြစ်သည် — open အခြေအနေသည်
dependency ကို မထိခိုက်စေရန် ဝန်ကို 99% ကျော် လျှော့ပေးသဖြင့် dependency သည် ပြန်လည်
ကောင်းမွန်နိုင်သည်။ half-open တွင် probe အရေအတွက် ကန့်သတ်ချက် မရှိပါက ဤ အကျိုးအမြတ်
လျော့သွားသည်။

```bash
python3 - <<'PY'
import math
from math import comb

window = 20
min_samples = 10
threshold = 0.50
outcomes = ["F"] * 8 + ["S"] * 2          # 80% failure over the first 10 requests
seen = 0
tripped_at = None
for i, o in enumerate(outcomes, start=1):
    seen += 1
    if seen >= min_samples:
        failures = outcomes[:i].count("F")
        if failures / i >= threshold:
            tripped_at = i
            break
print("rolling window", window, "requests, minimum", min_samples, "samples, failure threshold", threshold)
print("observed failure rate", outcomes.count("F") / len(outcomes))
print("breaker trips after request", tripped_at, "with", outcomes[:tripped_at].count("F"), "failures")
print()
open_s = 30
probes = 5
offered_rps = 20.0
probe_rps = probes / open_s
print("while open: offered", offered_rps, "rps -> probe", probes, "requests per", open_s, "s =", round(probe_rps, 3), "rps")
print("load reduction", f"{(1 - probe_rps / offered_rps) * 100:.2f}%")
print()
dep_success = 0.20
p_close = sum(comb(probes, s) * dep_success ** s * (1 - dep_success) ** (probes - s) for s in range(4, probes + 1))
print("half-open needs 4 of 5 successes; dependency still 20% healthy -> close probability", round(p_close, 5))
print("healthy dependency -> closes after the first probe round, i.e. about", open_s, "s after opening")
PY
```


```text
rolling window 20 requests, minimum 10 samples, failure threshold 0.5
observed failure rate 0.8
breaker trips after request 10 with 8 failures

while open: offered 20.0 rps -> probe 5 requests per 30 s = 0.167 rps
load reduction 99.17%

half-open needs 4 of 5 successes; dependency still 20% healthy -> close probability 0.00672
healthy dependency -> closes after the first probe round, i.e. about 30 s after opening
```


### ဥပမာ ၄ — Incident timeline နှင့် ၎င်း စားသုံးသည့် budget

**ယူဆချက် —** incident တစ်ခုတွင် error rate သည် 1% ဖြစ်သည်၊ peak demand သည် 2,000 rps။
monthly budget သည် 2,000 failed request (SLO 99.9%၊ 30-day window၊ eligible request 2,000,000 ခု)။
timeline — detect 4 မိနစ်၊ contain and mitigate 12 မိနစ်၊ verify recovery 8 မိနစ်။

**ဖော်မြူလာ —**
- failures per second = rps × error rate
- budget ကုန်သည့် အချိန် = monthly budget ÷ failures per second
- အပိုင်း တစ်ခုစီ စားသုံးသည့် budget = failures per second × minutes × 60 ÷ monthly budget

**တွက်ချက်မှု —**
1. failures per second = 2,000 × 0.01 = 20 ဖြစ်သည်၊ ထို့ကြောင့် monthly budget သည်
   2,000 ÷ 20 = 100 စက္ကန့် (1 မိနစ် 40 စက္ကန့်) အတွင်း ကုန်သည်။
2. detect အပိုင်း (4 မိနစ်) = 4,800 failures = budget ၏ 2.40 ဆ ဖြစ်သည်။
3. mitigate အပိုင်း (12 မိနစ်) = 14,400 failures = 7.20 ဆ ဖြစ်သည်။
4. recovery အပိုင်း (8 မိနစ်) = 9,600 failures = 4.80 ဆ ဖြစ်သည်။
5. စုစုပေါင်း 24 မိနစ် = 28,800 failures = monthly budget ၏ 14.40 ဆ ဖြစ်သည်။

**ကောက်ချက် —** 1% error rate ဖြင့် 24 မိနစ်သာ ကြာသည့် incident တစ်ခုသည် **တစ်လစာ budget ကို
14 ဆ ကျော် စားသုံး** သည်။ ထို့ကြောင့် incident တစ်ခုကို "budget ကုန်သွားသည်" ဟူသည့်
အဖြစ်အပျက်အဖြစ် သတ်မှတ်ရမည်၊ ထို့ကြောင့် error budget policy သည် မည်သည့် လုပ်ဆောင်ချက် ရပ်မည်
(ဥပမာ release freeze၊ reliability အလုပ်သို့ ဦးစားပေး ပြောင်းခြင်း) ကို ကြိုတင် သတ်မှတ်ရမည်။
**ဖော်ထုတ်ချိန် (detect) ကို တိုစေခြင်း** သည် timeline အပိုင်း တိုင်းကို တိုစေသဖြင့် အကြီးမားဆုံး
အကျိုးအမြတ် ရရှိသည့် နေရာ ဖြစ်သည်။

```bash
python3 - <<'PY'
rps = 2000
err = 0.01
budget = 2000
fail_per_s = rps * err
print("failure rate", err, "at", rps, "rps ->", fail_per_s, "failures per second")
print("monthly budget", budget, "failed requests -> exhausted in", round(budget / fail_per_s, 1), "s")
print()
print("incident phase              minutes   failures   monthly budgets")
for label, minutes in (("detect (alert to ack)", 4), ("contain and mitigate", 12), ("verify recovery", 8)):
    fails = fail_per_s * minutes * 60
    print(f"{label:<24} {minutes:>6d} {int(fails):>10d} {fails / budget:>15.2f}x")
total = fail_per_s * 24 * 60
print(f"{'total':<24} {24:>6d} {int(total):>10d} {total / budget:>15.2f}x")
PY
```


```text
failure rate 0.01 at 2000 rps -> 20.0 failures per second
monthly budget 2000 failed requests -> exhausted in 100.0 s

incident phase              minutes   failures   monthly budgets
detect (alert to ack)         4       4800            2.40x
contain and mitigate         12      14400            7.20x
verify recovery               8       9600            4.80x
total                        24      28800           14.40x
```


## ၂။ တွက်ချက်ရသည့် လေ့ကျင့်ခန်းများ (Calculation Exercises)

**၁။ Error budget ကို SLO မှ ဆင်းသက်ခြင်း** — SLO သည် 99.9% အောင်မြင်မှု၊ measurement window သည်
30 ရက်၊ eligible request သည် 2,000,000 ခု။ (က) error budget ကို request အရေအတွက်နှင့် မိနစ်ဖြင့်
ဖော်ပြပါ။ (ခ) လေ့လာတွေ့ရှိသည့် မအောင်မြင်နှုန်းသည် 0.5% ဖြစ်ပါက budget သည် မည်သည့် အချိန်တွင် ကုန်မည်။
(ဂ) မအောင်မြင်နှုန်း 1% နှင့် 4% အတွက် တူညီသည့် ကိန်းဂဏန်းများကို ဖော်ပြပါ။ (ဃ) SLO ကို 99.95% သို့
တိုးပါက budget သည် မည်သို့ ပြောင်းသနည်း။

**၂။ Retry storm ၏ အတိုင်းအတာ** — dependency တစ်ခုတွင် failure rate သည် 50%၊ client တိုင်းသည်
retry ၃ ကြိမ် အထိ ထပ်ကြိုးစားသည်။ (က) request တစ်ခုလျှင် ပျမ်းမျှ ခေါ်ဆိုမှု အရေအတွက်။ (ခ) origin
demand သည် 2,000 rps ဖြစ်ပါက dependency မြင်သည့် ဝန်။ (ဂ) ထို ခေါ်ဆိုမှုကို အလွှာ ၂ နှင့် ၃ အထိ
ဆင့်ဆက်လုပ်ပါက (အလွှာ တိုင်း retry ၃ ကြိမ်) ဝန်သည် မည်သို့ တိုးသနည်း။ (ဃ) retry budget သည်
original request ၏ 10% ဖြစ်ပါက ထို ဝန်ကို ခွင့်ပြုသလား။

**၃။ Queueing latency နှင့် saturation** — server ၈ ခု၊ ပျမ်းမျှ service time 400 ms၊ arrival rate 18 rps
(useful capacity 20 rps)။ (က) utilization၊ (ခ) request တစ်ခု စောင့်ရသည့် ဖြစ်နိုင်ခြေ P(wait)၊ (ဂ) queue
တွင် စောင့်ချိန် (Wq) နှင့် စုစုပေါင်း response time (W)၊ (ဃ) arrival rate 12 rps၊ 15 rps၊ 19 rps နှင့်
19.6 rps ဖြစ်ပါက response time သည် မည်သို့ ပြောင်းသနည်း။

**၄။ Timeout budget ကို chain တစ်လျှောက် ခွဲဝေခြင်း** — ingress deadline သည် 2,000 ms။ chain သည်
auth 150 ms၊ retrieval 300 ms၊ model 1,400 ms၊ format 150 ms (allocated)။ (က) hop တိုင်း ပြီးနောက်
ကျန်ရှိသည့် budget ကို ဖော်ပြပါ။ (ခ) model hop သည် timeout ဖြစ်ပါက ကျန်ရှိသည့် budget ဖြင့်
retry တစ်ကြိမ် လုပ်နိုင်သလား။ (ဂ) hop တိုင်း မိမိ၏ timeout ကို သီးခြား 2,000 ms သတ်မှတ်ပါက
အဆိုးဆုံး အခြေအနေသည် မည်မျှ ကြာနိုင်သနည်း။

**၅။ Over-provisioning နှင့် incident ၏ ကုန်ကျစရိတ်** — peak demand 2,000 rps အတွက် worker ၂၀
လိုအပ်သည်၊ အဖွဲ့အစည်းသည် 1.5 ဆ headroom ထားသည်၊ worker-hour တစ်နာရီ USD 0.40၊ တစ်လ 730 နာရီ။
peak အချိန် 45 မိနစ် ပြတ်တောက်မှုတွင် request အားလုံး မပြီးမြောက်ဘဲ request တစ်ခု၏ အလျင်အမြန်
တန်ဖိုးသည် USD 0.02 ဖြစ်သည်၊ SLA credit သည် လစဉ် USD 30,000 ၏ 10%။ (က) headroom ၏ တစ်လနှင့်
တစ်နှစ် ကုန်ကျစရိတ်။ (ခ) incident တစ်ခု၏ ကုန်ကျစရိတ်။ (ဂ) break-even — headroom တစ်လသည်
မည်သည့် request အရေအတွက် (မည်သည့် စက္ကန့်) နှင့် တူညီသည်။

**၆။ Alert နှုန်းနှင့် ဖော်ထုတ်ချိန်** — ဝန်ဆောင်မှုသည် 20 rps၊ SLO သည် 99.9%။ alert သတ်မှတ်ချက်သည်
SLO error rate အထက် 3σ။ window သုံးမျိုး — 1 min၊ 5 min၊ 60 min။ (က) window တိုင်း ယုံကြည်စွာ
ဖမ်းနိုင်သည့် အနည်းဆုံး burn rate။ (ခ) ထို burn rate ဖြင့် 30-day budget ကုန်သည့် ရက်။ (ဂ) ဝန်ဆောင်မှု
ကျန်းမာနေစဉ်တွင် တစ်ရက် မှားယွင်းစွာ alert ဖြစ်သည့် အရေအတွက် (3σ = 0.135% ဖြစ်သည်)။ (င) ထို
စည်းမျဉ်းကို 2,000 rps ဝန်ဆောင်မှုတွင် သုံးပါက အနည်းဆုံး ဖမ်းနိုင်သည့် burn rate သည် မည်သို့ ပြောင်းသနည်း။

## ၃။ ပြဿနာ ရှာဖွေခြင်း (Troubleshooting Scenarios)

### ပြဿနာ ၁ — ဝန်အောက်တွင် latency ခုန်တက်ခြင်း

**လက္ခဏာ (symptom) —** ဝန်သည် ပုံမှန် အနေအထားသို့ ရောက်သည့်အခါ p50 latency သည် မပြောင်းလဲပါ၊
သို့သော် p99 latency သည် 800 ms မှ 8 စက္ကန့် အထိ ခုန်တက်သည်။ host level utilization သည်
60% သာ ပြသည်၊ request အားလုံးနီးပါး ပြီးမြောက်နေဆဲ ဖြစ်သည်။

**တိုင်းတာရမည့် အရာ —** route နှင့် workload အလိုက် percentile များ၊ queue depth နှင့် စောင့်နေသည့်
အလုပ်၊ အရင်းအမြစ် တစ်ခုချင်း၏ saturation (accelerator slot၊ KV memory၊ connection pool၊ disk)၊
retry အရေအတွက်၊ timeout ဖြတ်တောက်ခံရသည့် request အချိုး။

**ဖြစ်နိုင်သည့် အကြောင်းရင်းများ —** queue ကို ကန့်သတ်မထားသဖြင့် queueing ကြောင့် tail ခုန်တက်ခြင်း။
ချို့ယွင်းလာသည့် dependency အပေါ် retry များ ဆင့်ပွားခြင်း။ request ကုန်ကျစရိတ် ကွဲပြားခြင်း
(prompt အလွန်ရှည်သည့် request အနည်းငယ်က slot များကို ဖမ်းထားခြင်း)။ tenant တစ်ခုက ဝန်ကို
အချိုးအစား မမှန်စွာ သုံးခြင်း။ warmup မပြီးသေးသည့် instance များ traffic ရရှိခြင်း။

**ပြုပြင်ရမည့် အရာ —** queue length ကို ကန့်သတ်ပြီး အစောဆုံး အချက်အလက် ရရှိသည့် နယ်နိမိတ်တွင်
load shedding လုပ်ခြင်း။ retry budget သတ်မှတ်ပြီး jitter ပါသည့် backoff သုံးခြင်း။
deadline propagation ဖြင့် budget ကုန်သွားသည့် အလုပ်ကို ပလပ်ဖျက်ခြင်း။ tenant အလိုက် rate limit ထားခြင်း။
readiness probe ဖြင့် traffic ရရှိခွင့်ကို ထိန်းချုပ်ခြင်း။

**သက်ဆိုင်သည့် term —** Saturation, Tail Latency, Admission Control, Load Shedding, Retry Budget

### ပြဿနာ ၂ — dependency တစ်ခု ချို့ယွင်းပါက ဝန်ဆောင်မှု ပြိုလဲခြင်း

**လက္ခဏာ (symptom) —** အရေးမကြီးသည့် retrieval index ချို့ယွင်းသည့်အခါ ဝန်ဆောင်မှုသည်
တစ်ခုလုံး မပြီးမြောက်တော့ပါ၊ မည်သည့် route မျှ အလုပ်မလုပ်ပါ။ instance အားလုံး traffic မရရှိတော့ပါ။

**တိုင်းတာရမည့် အရာ —** dependency အလိုက် error attribution၊ ခေါ်ဆိုမှု အလိုက် ကုန်ဆုံးသည့် အချိန်
(timeout ဖြစ်သည့် အချိုး)၊ readiness probe စစ်ဆေးသည့် dependency စာရင်း၊ blast radius —
မည်သည့် feature များ မလုပ်နိုင်တော့သည်၊ မည်သည့် အလုပ်များ ဆက်လုပ် နိုင်သည်။

**ဖြစ်နိုင်သည့် အကြောင်းရင်းများ —** circuit breaker မရှိသဖြင့် ခေါ်ဆိုမှု တိုင်း timeout အထိ စောင့်ပြီး
အလုပ်သမား အားလုံးကို ကိုင်ထားခြင်း။ timeout များကို hop တိုင်း သီးခြား သတ်မှတ်ထားသဖြင့်
အသုံးပြုသူ deadline ကို ကျော်လွန်ခြင်း။ degradation mode နှင့် fallback မရှိခြင်း။ readiness probe သည်
အရေးမကြီးသည့် dependency ကို မဖြစ်မနေ စစ်သဖြင့် instance အားလုံး ချက်ချင်း unready ဖြစ်ခြင်း။

**ပြုပြင်ရမည့် အရာ —** circuit breaker ထည့်၍ ချို့ယွင်းနေသည့် dependency ကို ခေါ်ဆိုမှုများဖြင့်
မတိုက်ခိုက်စေခြင်း။ degradation ladder ရေးဆွဲ၍ မည်သည့် capability ပိတ်နိုင်သည်ကို ကြိုတင်
သတ်မှတ်ခြင်း။ ကျန်ရှိသည့် အချိန် budget ကို downstream သို့ ပေးပို့ခြင်း။ readiness probe ကို
ဝန်ဆောင်မှု ပေးရန် လိုအပ်သည့် **အနည်းဆုံး** dependency ဖြင့်သာ စစ်စေခြင်း။ fallback ကို
dependency ချို့ယွင်းမှု အောက်တွင် စမ်းသပ်ခြင်း။

**သက်ဆိုင်သည့် term —** Graceful Degradation, Readiness Probe, Deadline Propagation, Availability, Tail Latency

### ပြဿနာ ၃ — မြင်တွေ့နိုင်သည့် incident မရှိဘဲ error budget ကုန်နေခြင်း

**လက္ခဏာ (symptom) —** 30-day budget ၏ 60% ကုန်သွားပြီ ဖြစ်သည်၊ သို့သော် page မဖြစ်ခဲ့ပါ၊ dashboard
သည် "ကျန်းမာ" ဟု ပြသည်၊ incident မှတ်တမ်း တစ်ခုမျှ မရှိပါ။

**တိုင်းတာရမည့် အရာ —** SLI ၏ numerator၊ denominator နှင့် exclusions သည် မည်သည့် အချိန်တွင်
ပြောင်းလဲခဲ့သည်၊ မအောင်မြင်မှုကို route၊ tenant နှင့် canary cohort အလိုက် ခွဲကြည့်ခြင်း၊
"အောင်မြင်သည်" ဟု ရေတွက်ခံရသည့် retryable နှင့် timeout ဖြစ်သည့် request များ၊ degraded mode
ဖွင့်ထားသည့် စုစုပေါင်း အချိန်၊ multi-window burn rate များ။

**ဖြစ်နိုင်သည့် အကြောင်းရင်းများ —** SLI ၏ အဓိပ္ပာယ်ဖွင့်ဆိုချက် (numerator၊ exclusions) သည် တိတ်ဆိတ်စွာ
ပြောင်းလဲခြင်း။ degradation mode က cached သို့မဟုတ် ရှေးဟောင်း အဖြေကို အောင်မြင်မှုအဖြစ်
ရေတွက်ခြင်း။ timeout ဖြစ်သည့် request ကို "ဖယ်ထားသည့် အခြေအနေ" အဖြစ် သတ်မှတ်ခြင်း။
canary cohort တစ်ခုတွင် သေးငယ်သည့် ချို့ယွင်းမှု ရက်ရှည် စုပုံခြင်း။ နှေးကွေးသည့် burn (slow burn)
ကို ဖမ်းနိုင်သည့် window မရှိခြင်း။

**ပြုပြင်ရမည့် အရာ —** SLI ၏ အဓိပ္ပာယ်ဖွင့်ဆိုချက်ကို version control တွင် ထားပြီး ပြောင်းလဲမှု တိုင်းကို
မှတ်တမ်းတင်ခြင်း။ fast burn နှင့် slow burn window နှစ်ခု တွဲသုံးခြင်း။ budget ကို အသုံးပြုသူ
အုပ်စု အလိုက် ခွဲကြည့်ခြင်း။ degraded mode ဖွင့်ထားသည့် အချိန်ကို SLI တွင် ထည့်သွင်း စဉ်းစားခြင်း။
shadow traffic ဖြင့် ကိုယ်စားလှယ်ကို အစစ်အမှန် input ဖြင့် စမ်းသပ်ခြင်း။ canary cohort များကို
သီးခြား ကြည့်ခြင်း။

**သက်ဆိုင်သည့် term —** Service Level Indicator (SLI), Error Budget, Graceful Degradation, Canary Release, Shadow Traffic

## ၄။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်းများ (Design Decisions)

### ဆုံးဖြတ်ချက် ၁ — SLO ကို 99.9% သို့မဟုတ် 99.99% ရွေးချယ်ခြင်း

လုပ်ငန်း ဝန်ဆောင်မှု တစ်ခုသည် လစဉ် စာချုပ် USD 30,000 ဖြင့် B2B အသုံးပြုသူများကို
ဝန်ဆောင်မှု ပေးသည်။ ပြတ်တောက်မှု တစ်မိနစ်လျှင် ရောင်းရငွေ ဆုံးရှုံးမှုနှင့် SLA credit စုစုပေါင်း
USD 1,000 ဖြစ်သည်။ ရွေးချယ်စရာ နှစ်ခု ရှိသည်။

- **Option A** — SLO 99.9%၊ လက်ရှိ ဗိသုကာ၊ infrastructure USD 12,000/လ။
- **Option B** — SLO 99.99%၊ redundancy နှင့် ဒုတိယ ဒေသ ထည့်ရသည်၊ USD 29,000/လ။

**ဖြေရမည့် မေးခွန်း —** မည်သည့် ပန်းတိုင်ကို ကတိပြုမည်၊ ဆုံးဖြတ်ချက်ကို မည်သည့် ကိန်းဂဏန်းဖြင့်
ပြောင်းလဲနိုင်သည်။ (အဖြေကို အပိုင်း ၅.၃ တွင် ဖော်မြူလာ၊ ယူဆချက်နှင့် တွက်ချက်မှုနှင့်အတူ ကြည့်ပါ။)

**ဆုံးဖြတ်သည့် စံနှုန်းများ —** error budget ၏ ရလဒ် (မအောင်မြင်နိုင်သည့် မိနစ်)၊ ကုန်ကျစရိတ် ကွာခြားမှု၊
အသုံးပြုသူ ကတိနှင့် စာချုပ် လျော်ကြေး၊ budget ကုန်သွားပါက မည်သည့် release လုပ်ဆောင်ချက်
ရပ်မည်။

### ဆုံးဖြတ်ချက် ၂ — Accept-all သို့မဟုတ် admission control နှင့် load shedding

useful capacity သည် 2,000 rps ဖြစ်ပြီး လက်ရှိ demand သည် 2,600 rps။

- **Policy A (accept-all)** — request အားလုံးကို လက်ခံသည်၊ ထို့ကြောင့် 40% သည် deadline ကို
  ကျော်လွန်၍ client များက retry ၂ ကြိမ် ထပ်လုပ်သည်။
- **Policy B (admission control + load shedding)** — 2,000 rps တွင် ကန့်သတ်၍ ကျန်ရှိသည့် request
  များကို overload scope ဖော်ထုတ်လျက် ငြင်းပယ်သည်၊ high-priority အလုပ်ကို ဦးစားပေးသည်။

**ဖြေရမည့် မေးခွန်း —** မည်သည့် policy သည် အသုံးဝင်သည့် ရလဒ် (useful throughput) ပိုပေးသည်၊
SLO 99.9% နှင့် ထို policy သည် မည်သို့ ဆက်စပ်သည်။ (အဖြေကို အပိုင်း ၅.၃ တွင် ကြည့်ပါ။)

## ၅။ အဖြေများ (Answers with Explanations)

### ၅.၁ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း အဖြေများ

#### အဖြေ ၁ — Error budget ကို SLO မှ ဆင်းသက်ခြင်း

**ဖော်မြူလာ —**
- error budget fraction = 1 − SLO
- budget (requests) = (1 − SLO) × eligible requests
- budget (minutes) = (1 − SLO) × window minutes
- burn rate = observed failure rate ÷ (1 − SLO)
- budget ကုန်သည့် အချိန် = window ÷ burn rate

**တွက်ချက်မှု —** (က) budget fraction = 0.001၊ budget = 2,000 request = 43.2 မိနစ်။
(ခ) မအောင်မြင်နှုန်း 0.5% ဖြစ်ပါက burn rate 5x၊ budget သည် 6 ရက် အတွင်း ကုန်သည်။
(ဂ) 1% → burn rate 10x → 3 ရက်၊ 4% → burn rate 40x → 0.75 ရက် (18 နာရီ)။
(ဃ) SLO 99.95% ဖြစ်ပါက budget = 1,000 request = 21.6 မိနစ်၊ ဆိုလိုသည်မှာ budget သည် **တစ်ဝက်** ဖြစ်သွားသည်။

**ရလဒ် —**
1. budget = 2,000 failed request သို့မဟုတ် 43.2 မိနစ် ဖြစ်သည်။
2. 0.5% မအောင်မြင်နှုန်းသည် budget ကို 6 ရက် အတွင်း ကုန်စေသည်။
3. SLO ကို 99.95% သို့ တိုးခြင်းသည် budget ကို တစ်ဝက် (21.6 မိနစ်) ဖြစ်စေသည်။

**အကြောင်းရင်း —** error budget သည် SLO ၏ ဖြည့်စွက်ကိန်း ဖြစ်သဖြင့် SLO ကို အနည်းငယ်
မြှင့်ခြင်း (99.9 → 99.95) သည် ခွင့်ပြုသည့် မအောင်မြင်မှုကို **တစ်ဝက်** ဖြစ်စေသည်။ ထို့ကြောင့်
"တစ်ခု ပိုသော nine" တိုင်းသည် budget ကို 10 ဆ လျော့စေပြီး ဗိသုကာ အလုပ်ကို သိသိသာသာ
တိုးစေသည်။

```bash
python3 - <<'PY'
slo = 0.999
window_days = 30
requests = 2_000_000
budget_frac = round(1 - slo, 6)
budget_requests = budget_frac * requests
budget_minutes = budget_frac * window_days * 24 * 60
print("SLO                        ", slo)
print("measurement window (days)  ", window_days)
print("eligible requests          ", requests)
print("error budget fraction      ", budget_frac)
print("error budget (requests)    ", int(budget_requests))
print("error budget (minutes)     ", round(budget_minutes, 1))
print()
print("observed failure rate   burn rate   days to exhaust   hours to exhaust")
for observed in (0.001, 0.002, 0.005, 0.01, 0.04):
    burn = observed / budget_frac
    days = window_days / burn
    print(f"{observed:>19.3%} {burn:>11.1f}x {days:>16.2f} {days * 24:>17.2f}")
print()
tighter = 0.0005
print("SLO 99.95% -> budget (requests)", int(tighter * requests),
      "budget (minutes)", round(tighter * window_days * 24 * 60, 1))
PY
```


```text
SLO                         0.999
measurement window (days)   30
eligible requests           2000000
error budget fraction       0.001
error budget (requests)     2000
error budget (minutes)      43.2

observed failure rate   burn rate   days to exhaust   hours to exhaust
             0.100%         1.0x            30.00            720.00
             0.200%         2.0x            15.00            360.00
             0.500%         5.0x             6.00            144.00
             1.000%        10.0x             3.00             72.00
             4.000%        40.0x             0.75             18.00

SLO 99.95% -> budget (requests) 1000 budget (minutes) 21.6
```


#### အဖြေ ၂ — Retry storm ၏ အတိုင်းအတာ

**ဖော်မြူလာ —**
- attempts per request = Σ f^k, k = 0 … retries (f = failure rate)
- offered load = origin demand × attempts per request
- အလွှာ L အတွက် amplification = (per-layer amplification)^L
- retry demand = origin demand × (amplification − 1)

**တွက်ချက်မှု —** f = 0.5၊ retry 3 ကြိမ် ဖြစ်ပါက attempts = 1 + 0.5 + 0.25 + 0.125 = 1.875 ဖြစ်သည်။
origin 2,000 rps ဖြစ်ပါက dependency မြင်သည့် ဝန်သည် 3,750 rps ဖြစ်သည်။ အလွှာ ၂ တွင်
1.875² = 3.516 → 7,031 rps၊ အလွှာ ၃ တွင် 1.875³ = 6.592 → 13,184 rps ဖြစ်သည်။ retry demand သည်
2,000 × 0.875 = 1,750 rps ဖြစ်ပြီး၊ 10% retry budget က ခွင့်ပြုသည့် 200 rps ကို ကျော်လွန်သည်။

**ရလဒ် —** request တစ်ခုလျှင် 1.875 attempt၊ အလွှာ ၃ ဆင့် ဆိုပါက 6.592 attempt (13,184 rps) ဖြစ်သည်။
retry budget 10% ဖြင့် ဤ ဝန်ကို ခွင့်ပြုနိုင်မည် မဟုတ်ပါ။

**အကြောင်းရင်း —** retry သည် **တစ်ဦးချင်း ကြည့်ပါက အသေးအဖွဲ** ဖြစ်သည်၊ သို့သော် အလွှာ
များစွာ ဆင့်ဆက်လုပ်ပါက အတိုင်းအတာသည် အလွှာ အရေအတွက်နှင့် တိုးသည် (exponential)။
ထို့ကြောင့် retry ကို ခွင့်ပြုသင့်သည့် နေရာကို **တစ်လွှာတည်း** သတ်မှတ်ပြီး၊ deadline နှင့်
retry budget ကို တစ်ချိန်တည်း စစ်ရမည်။ failure rate 90% တွင် per-layer amplification သည်
3.439 အထိ ရောက်သဖြင့် အန္တရာယ် ပို၍ ကြီးသည်။

```bash
python3 - <<'PY'
def amplification(f, retries):
    return sum(f ** k for k in range(retries + 1))

baseline_rps = 2000
print("failure rate   retries   attempts per request   offered rps")
for f in (0.3, 0.5, 0.7, 0.9):
    for r in (1, 2, 3):
        amp = amplification(f, r)
        print(f"{f:>11.0%} {r:>9d} {amp:>21.3f} {baseline_rps * amp:>13.0f}")
print()
f, r = 0.5, 3
per_layer = amplification(f, r)
print("per layer, f = 50%, retries = 3:", round(per_layer, 3), "attempts per request")
for layers in (1, 2, 3):
    total = per_layer ** layers
    print(f"layers {layers}: amplification {total:>8.3f}   attempts at 2000 rps {baseline_rps * total:>9.0f} rps")
print()
print("retry budget at 10% of originals allows", int(0.10 * baseline_rps), "retry rps")
print("retries that f = 50%, retries = 3 demand", int(baseline_rps * (per_layer - 1)), "rps")
PY
```


```text
failure rate   retries   attempts per request   offered rps
        30%         1                 1.300          2600
        30%         2                 1.390          2780
        30%         3                 1.417          2834
        50%         1                 1.500          3000
        50%         2                 1.750          3500
        50%         3                 1.875          3750
        70%         1                 1.700          3400
        70%         2                 2.190          4380
        70%         3                 2.533          5066
        90%         1                 1.900          3800
        90%         2                 2.710          5420
        90%         3                 3.439          6878

per layer, f = 50%, retries = 3: 1.875 attempts per request
layers 1: amplification    1.875   attempts at 2000 rps      3750 rps
layers 2: amplification    3.516   attempts at 2000 rps      7031 rps
layers 3: amplification    6.592   attempts at 2000 rps     13184 rps

retry budget at 10% of originals allows 200 retry rps
retries that f = 50%, retries = 3 demand 1750 rps
```


#### အဖြေ ၃ — Queueing latency နှင့် saturation

**ဖော်မြူလာ —** server c ခု၊ ပျမ်းမျှ service time S အတွက် offered load a = λ × S၊ utilization
ρ = a ÷ c။ P(wait) ကို Erlang C (Erlang B recursion မှ ဆင်းသက်သည်) ဖြင့် တွက်သည်။
- Wq = P(wait) × S ÷ (c − a)
- W = Wq + S

**တွက်ချက်မှု —** c = 8၊ S = 400 ms (useful capacity 20 rps)၊ λ = 18 rps ဖြစ်ပါက ρ = 0.9၊
P(wait) = 0.702၊ Wq = 350.8 ms၊ W = 750.8 ms ဖြစ်သည်။ λ = 19.6 rps (ρ = 0.98) ဖြစ်ပါက
Wq = 2,340.3 ms၊ W = 2,740.3 ms အထိ တက်သည်။

**ရလဒ် —** ρ = 0.9 တွင် response time သည် 750.8 ms ဖြစ်သည်၊ ρ = 0.98 တွင် 2,740.3 ms ဖြစ်သည်။
utilization သည် 8% ခန့်သာ တိုးသော်လည်း response time သည် 3.6 ဆ တိုးသည်။

**အကြောင်းရင်း —** queueing သည် **ရုပ်ပိုင်းဆိုင်ရာ** အပေါ် linear မဟုတ်ပါ — utilization သည် 1
သို့ နီးကပ်လာသည့်အခါ အလုပ်သမား အားလုံး အလုပ်လုပ်နေပြီး အသစ် ဝင်လာသည့် request တိုင်း
စောင့်ရသဖြင့် စောင့်ချိန် အလျင်အမြန် ကြီးထွားသည်။ ထို့ကြောင့် (က) utilization တစ်ခုတည်းက
လုံလောက်သည့် အချက်အလက် မပေးပါ — queue depth နှင့် waiting work ကို တိုင်းရမည်၊
(ခ) capacity ကို ρ နည်းသည့် အဆင့်တွင် ထားရမည်၊ (ဂ) tail latency နှင့် error များကို
queue မတည်ငြိမ်သည့် အဆင့်သို့ မရောက်မီ alert လုပ်ရမည်။

```bash
python3 - <<'PY'
def erlang_b(c, a):
    b = 1.0
    for i in range(1, c + 1):
        b = a * b / (i + a * b)
    return b

def mmc(c, service_s, lam):
    a = lam * service_s
    rho = a / c
    if rho >= 1:
        return rho, 1.0, float("inf"), float("inf")
    b = erlang_b(c, a)
    p_wait = b / (1 - rho + rho * b)
    wq = p_wait * service_s / (c - a)
    return rho, p_wait, wq, wq + service_s

c = 8
service_s = 0.4
print(f"servers {c}, mean service time {service_s} s, maximum useful rate {c / service_s:.1f} rps")
print()
print(" arrival rps   utilization   P(wait)   queue ms   response ms   queue length")
for lam in (12.0, 15.0, 17.0, 18.0, 19.0, 19.6):
    rho, p_wait, wq, w = mmc(c, service_s, lam)
    print(f"{lam:>12.1f} {rho:>13.3f} {p_wait:>10.3f} {wq * 1000:>10.1f} {w * 1000:>13.1f} {lam * wq:>14.2f}")
print()
rho, p_wait, wq, w = mmc(c, service_s, 18.0)
print("stated case 18 rps: utilization", round(rho, 3), "queue ms", round(wq * 1000, 1),
      "response ms", round(w * 1000, 1), "queue length", round(18.0 * wq, 2))
PY
```


```text
servers 8, mean service time 0.4 s, maximum useful rate 20.0 rps

 arrival rps   utilization   P(wait)   queue ms   response ms   queue length
        12.0         0.600      0.140       17.4         417.4           0.21
        15.0         0.750      0.357       71.4         471.4           1.07
        17.0         0.850      0.573      190.9         590.9           3.24
        18.0         0.900      0.702      350.8         750.8           6.31
        19.0         0.950      0.844      844.2        1244.2          16.04
        19.6         0.980      0.936     2340.3        2740.3          45.87

stated case 18 rps: utilization 0.9 queue ms 350.8 response ms 750.8 queue length 6.31
```


#### အဖြေ ၄ — Timeout budget ကို chain တစ်လျှောက် ခွဲဝေခြင်း

**ဖော်မြူလာ —**
- ကျန်ရှိသည့် budget = ingress deadline − ကုန်ဆုံးသွားသည့် allocated အချိန် စုစုပေါင်း
- retry တစ်ကြိမ် လိုအပ်သည့် အချိန် = backoff + jitter + ခေါ်ဆိုမှု ကြာချိန်
- သီးခြား timeout များ၏ အဆိုးဆုံး အခြေအနေ = hops × timeout

**တွက်ချက်မှု —** allocated စုစုပေါင်း 150 + 300 + 1,400 + 150 = 2,000 ms ဖြစ်သည်။ auth ပြီးနောက် 1,850 ms၊
retrieval ပြီးနောက် 1,550 ms၊ model ပြီးနောက် 150 ms၊ format ပြီးနောက် 0 ms ကျန်သည်။ model hop သည်
1,400 ms တွင် timeout ဖြစ်ပါက ကျန်ရှိသည့် budget သည် 150 ms သာ ဖြစ်သည်၊ retry တစ်ကြိမ်အတွက်
backoff 200 ms နှင့် jitter 100 ms ပင် မလုံလောက်ပါ။ hop တိုင်း သီးခြား 2,000 ms ထားပါက
အဆိုးဆုံး အခြေအနေသည် 4 × 2,000 = 8,000 ms (8 စက္ကန့်) ဖြစ်သည် — အသုံးပြုသူ deadline ၏ 4 ဆ။

**ရလဒ် —** model hop ပြီးနောက် 150 ms ကျန်သည်၊ retry မလုပ်နိုင်ပါ။ deadline propagation မရှိပါက
hop လေးခု၏ အဆိုးဆုံး ကြာချိန်သည် 8,000 ms ဖြစ်သည်။

**အကြောင်းရင်း —** "deadline" သည် **စုစုပေါင်း** နယ်နိမိတ် တစ်ခုတည်း ဖြစ်သည်၊ hop တိုင်း၏
timeout များသည် ထို budget ကို ခွဲဝေသည့် အပိုင်းများ ဖြစ်သည်။ ထို့ကြောင့် retry delay နှင့်
backoff သည် ထို budget အတွင်းတွင် ပါရမည်။ မပါပါက ရလဒ်သည် အသုံးဝင်တော့မည် မဟုတ်သည့်တိုင်
အလုပ်များက capacity ကို စားသုံးနေစေသည်။

```bash
python3 - <<'PY'
deadline_ms = 2000
chain = [("auth", 150, 40), ("retrieval", 300, 200), ("model", 1400, 1200), ("format", 150, 60)]
remaining = deadline_ms
print("hop          allocated ms   observed ms   budget left after the hop")
for name, alloc, observed in chain:
    remaining -= alloc
    print(f"{name:<12} {alloc:>12d} {observed:>13d} {remaining:>23d}")
print()
print("allocated total", sum(a for _, a, _ in chain), "ms  = ingress deadline", deadline_ms, "ms")
print("observed total ", sum(o for _, _, o in chain), "ms")
print()
independent = len(chain) * deadline_ms
print("if each hop kept its own independent", deadline_ms, "ms timeout, worst case =",
      independent, "ms =", independent / 1000, "s")
print()
after_model = deadline_ms - (150 + 300 + 1400)
print("after the model hop times out: remaining budget", after_model, "ms")
print("one retry needs backoff 200 ms + jitter up to 100 ms, then a full model call of 1400 ms")
print("a retry starting at", 1400 + 150 + 300, "+ 200 .. 300 ms would finish at",
      1900 + 200 + 1400, "..", 1900 + 300 + 1400, "ms -> outside the", deadline_ms, "ms deadline")
PY
```


```text
hop          allocated ms   observed ms   budget left after the hop
auth                  150            40                    1850
retrieval             300           200                    1550
model                1400          1200                     150
format                150            60                       0

allocated total 2000 ms  = ingress deadline 2000 ms
observed total  1500 ms

if each hop kept its own independent 2000 ms timeout, worst case = 8000 ms = 8.0 s

after the model hop times out: remaining budget 150 ms
one retry needs backoff 200 ms + jitter up to 100 ms, then a full model call of 1400 ms
a retry starting at 1850 + 200 .. 300 ms would finish at 3500 .. 3600 ms -> outside the 2000 ms deadline
```


#### အဖြေ ၅ — Over-provisioning နှင့် incident ၏ ကုန်ကျစရိတ်

**ဖော်မြူလာ —**
- extra workers = needed × headroom − needed
- headroom cost = extra workers × USD/worker-hour × hours per month
- incident cost = (peak rps × 60 × outage minutes × USD/request) + SLA credit
- break-even requests = headroom cost ÷ USD/request

**တွက်ချက်မှု —** extra workers = 20 × 1.5 − 20 = 10 ဖြစ်သည်၊ headroom cost = 10 × 0.40 × 730
= USD 2,920/လ = USD 35,040/နှစ် ဖြစ်သည်။ incident တစ်ခုတွင် request 2,000 × 60 × 45 = 5,400,000 ခု
ဆုံးရှုံးသဖြင့် ရောင်းရငွေ USD 108,000၊ SLA credit USD 3,000၊ စုစုပေါင်း USD 111,000 ဖြစ်သည်။
break-even = 2,920 ÷ 0.02 = 146,000 request = 2,000 rps တွင် 73 စက္ကန့် ဖြစ်သည်။

**ရလဒ် —** headroom တစ်လသည် USD 2,920၊ incident တစ်ခုသည် USD 111,000 ဖြစ်သည် —
headroom တစ်နှစ်စာ (USD 35,040) နှင့် နှိုင်းယှဉ်ပါက incident တစ်ခုသည် 3.17 ဆ ပို၍ ကုန်ကျသည်။
headroom တစ်လ၏ တန်ဖိုးသည် **73 စက္ကန့်** အတွင်း ဆုံးရှုံးသည့် request နှင့် တူညီသည်။

**အကြောင်းရင်း —** ဤ ကိန်းဂဏန်းသည် **headroom ၏ အကျိုးအမြတ်ကို incident ၏ ကုန်ကျစရိတ်နှင့်
နှိုင်းယှဉ်** ရမည် ဟူသည့် အချက်ကို ပြသည် — over-provisioning သည် "အလွန်ကုန်သည်" ဟု ထင်ရသော်လည်း
incident တစ်ခု၏ ကုန်ကျစရိတ်ထက် များစွာ နည်းနိုင်သည်။ ထို့ကြောင့် break-even ကို downtime
တစ်မိနစ်၏ တန်ဖိုးနှင့် တွဲဖက်တွက်ရမည်။ ရောင်းရငွေ ဆုံးရှုံးမှုအပြင် ယုံကြည်မှု (trust) ဆုံးရှုံးမှုကို
ထည့်တွက်ပါက headroom ၏ တန်ဖိုးသည် ပို၍ မြင့်သည်။

```bash
python3 - <<'PY'
workers_needed = 20
headroom = 1.5
worker_hour_usd = 0.40
hours_month = 730
extra_workers = workers_needed * headroom - workers_needed
over_month = extra_workers * worker_hour_usd * hours_month
print("workers for the measured peak          ", workers_needed)
print("provisioned workers (1.5x headroom)    ", int(workers_needed * headroom))
print("extra workers                          ", int(extra_workers))
print("over-provisioning cost per month (USD) ", round(over_month, 2))
print("over-provisioning cost per year (USD)  ", round(over_month * 12, 2))
print()
peak_rps = 2000
outage_minutes = 45
usd_per_request = 0.02
lost_requests = peak_rps * 60 * outage_minutes
lost_revenue = lost_requests * usd_per_request
monthly_contract = 30000
credit = 0.10 * monthly_contract
incident_total = lost_revenue + credit
print("requests lost in a", outage_minutes, "minute peak outage:", int(lost_requests))
print("lost revenue (USD)                     ", round(lost_revenue, 2))
print("SLA credit, 10% of USD 30000 (USD)     ", round(credit, 2))
print("one incident total (USD)               ", round(incident_total, 2))
print("incident / one year of headroom        ", round(incident_total / (over_month * 12), 2), "x")
print()
break_even_requests = over_month / usd_per_request
print("break-even: one month of headroom equals", int(break_even_requests), "lost requests")
print("at", peak_rps, "rps that is", round(break_even_requests / peak_rps, 1), "s of full outage")
PY
```


```text
workers for the measured peak           20
provisioned workers (1.5x headroom)     30
extra workers                           10
over-provisioning cost per month (USD)  2920.0
over-provisioning cost per year (USD)   35040.0

requests lost in a 45 minute peak outage: 5400000
lost revenue (USD)                      108000.0
SLA credit, 10% of USD 30000 (USD)      3000.0
one incident total (USD)                111000.0
incident / one year of headroom         3.17 x

break-even: one month of headroom equals 146000 lost requests
at 2000 rps that is 73.0 s of full outage
```


#### အဖြေ ၆ — Alert နှုန်းနှင့် ဖော်ထုတ်ချိန်

**ဖော်မြူလာ —** window တစ်ခုအတွင်း request n = rps × seconds၊ SLO အရ မျှော်မှန်းသည့် error
e = f × n (f = 0.001)၊ ထို ကိန်းဂဏန်း၏ စံလွဲမှု σ = √e။ အကယ်၍ threshold ကို SLO error rate အထက်
k σ ဟု ထားပါက ဖမ်းနိုင်သည့် အနည်းဆုံး burn rate = 1 + k ÷ σ။ မှားယွင်းသည့် alert နှုန်းသည်
window တိုင်း P(Z > k) ဖြစ်သဖြင့် တစ်ရက်လျှင် (86,400 ÷ window seconds) × P(Z > k) ဖြစ်သည်။

**တွက်ချက်မှု —**
1. 1 min window တွင် n = 1,200၊ e = 1.2၊ σ = 1.10၊ ဖမ်းနိုင်သည့် အနည်းဆုံး burn rate = 3.74x ဖြစ်သည်
   (budget သည် 8.02 ရက် အတွင်း ကုန်မည်)၊ မှားယွင်းသည့် alert = 1.944/ရက် ဖြစ်သည်။
2. 5 min window တွင် n = 6,000၊ σ = 2.45၊ burn rate = 2.22x (budget 13.48 ရက်)၊ alert = 0.389/ရက်။
3. 60 min window တွင် n = 72,000၊ σ = 8.49၊ burn rate = 1.35x (budget 22.16 ရက်)၊ alert = 0.032/ရက်။
4. 2,000 rps ဝန်ဆောင်မှုတွင် 1 min window ၏ n = 120,000၊ σ = 10.95 ဖြစ်သဖြင့် ဖမ်းနိုင်သည့်
   အနည်းဆုံး burn rate သည် 1.35x မှ 1.274x အထိ ကျသည် — ဝန် မြင့်သည့် ဝန်ဆောင်မှုတွင်
   window တိုကို ပို၍ စောစော သုံးနိုင်သည်။

**ရလဒ် —** 1 min window သည် ဖမ်းနိုင်သည့် burn rate ကြီး (3.74x) သော်လည်း တုံ့ပြန်ချိန် တို (1 မိနစ်)
ဖြစ်သည်၊ သို့သော် တစ်ရက် 1.94 alert မှားယွင်းသည်။ 60 min window သည် burn rate 1.35x ကို
ဖမ်းနိုင်သော်လည်း တုံ့ပြန်ချိန်သည် 60 မိနစ် ဖြစ်သည်။

**အကြောင်းရင်း —** window တို၏ မှားယွင်းမှု အရင်းအမြစ်သည် **ကိန်းဂဏန်း ဆူညံသံ** ဖြစ်သည် —
window အတွင်း expectation error e နည်းသည့်အခါ σ သည် e ၏ အချိုးအစား အလွန်ကြီးသဖြင့်
တကယ့် ကျဆင်းမှုကို ဆူညံသံမှ ခွဲမထုတ်နိုင်ပါ။ ထို့ကြောင့် **window နှစ်ခု** ကို တွဲသုံးရမည် —
window တိုသည် အလျင်အမြန် ဖြစ်ပွားသည့် incident ကို လျင်မြန်စွာ ဖမ်းသည်၊ window ရှည်သည်
နှေးကွေးသည့် ယုတ်လျော့မှု (slow burn) ကို ဆူညံသံ နည်းစွာဖြင့် ဖမ်းသည်။ ဝန် မြင့်သည့်
ဝန်ဆောင်မှုတွင် request အရေအတွက် များသဖြင့် window တို၏ σ သည် ပို၍ ငယ်သည်။

```bash
python3 - <<'PY'
import math

def upper_tail(z):
    return 0.5 * math.erfc(z / math.sqrt(2.0))

rps = 20
slo_fail = 0.001
k = 3.0
window_days = 30
print("service", rps, "rps, SLO error fraction", slo_fail, ", threshold", k, "sigma above the SLO rate")
print()
print(" window   requests   errors at SLO   sigma   burn to cross   detect within   false alerts/day")
for label, seconds in (("1 min", 60), ("5 min", 300), ("60 min", 3600)):
    n = rps * seconds
    err = slo_fail * n
    sigma = math.sqrt(err)
    burn = 1 + k / sigma
    per_day = 86400 / seconds
    false_alerts = per_day * upper_tail(k)
    print(f"{label:>7} {n:>10.0f} {err:>15.1f} {sigma:>8.2f} {burn:>15.2f} {label:>15} {false_alerts:>17.3f}")
print()
print("budget exhausted in days at a steady burn rate")
for label, seconds in (("1 min", 60), ("5 min", 300), ("60 min", 3600)):
    n = rps * seconds
    sigma = math.sqrt(slo_fail * n)
    burn = 1 + k / sigma
    print(f"  smallest burn a {label} window can see: {burn:>5.2f}x -> exhausts the 30-day budget in {window_days / burn:>5.2f} days")
print()
big = 2000
n = big * 60
sigma = math.sqrt(slo_fail * n)
print("same rule on a", big, "rps service, 1 min window:", n, "requests, sigma", round(sigma, 2),
      "-> burn", round(1 + k / sigma, 3), "x")
print("false alerts per day at 3 sigma:", round(0.5 * math.erfc(k / math.sqrt(2.0)) * 1440, 4))
PY
```


```text
service 20 rps, SLO error fraction 0.001 , threshold 3.0 sigma above the SLO rate

 window   requests   errors at SLO   sigma   burn to cross   detect within   false alerts/day
  1 min       1200             1.2     1.10            3.74           1 min             1.944
  5 min       6000             6.0     2.45            2.22           5 min             0.389
 60 min      72000            72.0     8.49            1.35          60 min             0.032

budget exhausted in days at a steady burn rate
  smallest burn a 1 min window can see:  3.74x -> exhausts the 30-day budget in  8.02 days
  smallest burn a 5 min window can see:  2.22x -> exhausts the 30-day budget in 13.48 days
  smallest burn a 60 min window can see:  1.35x -> exhausts the 30-day budget in 22.16 days

same rule on a 2000 rps service, 1 min window: 120000 requests, sigma 10.95 -> burn 1.274 x
false alerts per day at 3 sigma: 1.9439
```


### ၅.၂ ပြဿနာ ရှာဖွေခြင်း အဖြေများ

#### အဖြေ ၁ — ဝန်အောက်တွင် latency ခုန်တက်ခြင်း

**ရောဂါရှာဖွေသည့် လမ်း —** p50 မပြောင်းဘဲ p99 ခုန်တက်ခြင်းသည် **queueing** ၏ လက္ခဏာ ဖြစ်သည်
(average ကောင်းနေသော်လည်း tail သည် ရှည်သည်)။ host utilization 60% ဖြစ်ခြင်းသည်
saturation မရှိဟု မဆိုလိုပါ — ကန့်သတ်သည့် အရင်းအမြစ်သည် accelerator slot၊ KV memory
သို့မဟုတ် connection pool ဖြစ်နိုင်သည်။

**ဖြေရှင်းချက် —** queue length ကို သတ်မှတ်ချက်ဖြင့် ကန့်သတ်၍ ကျော်လွန်သည့် အလုပ်ကို
အစောဆုံး အချက်အလက် ရရှိသည့် နယ်နိမိတ်တွင် shed လုပ်ခြင်း၊ retry များကို retry budget
ဖြင့် ကန့်သတ်ပြီး jitter ထည့်ခြင်း၊ prompt အရှည်ကြီးသည့် request ကို ကန့်သတ်ခြင်း၊
tenant အလိုက် rate limit ထားခြင်း၊ readiness probe ဖြင့် warmup မပြီးသည့် instance များကို
traffic မပေးခြင်း။

**မည်သည့် ကိန်းဂဏန်းက ဆုံးဖြတ်သည် —** utilization 60% ဆိုသည့် အချက်သည် queue depth နှင့်
P(wait) ကို မဖော်ပြပါ။ queueing ဖော်မြူလာ (အဖြေ ၃) အရ ρ သည် 0.9 ကျော်သည့်အခါ
response time သည် အလွန်လျင်မြန်စွာ တက်သဖြင့် **queue depth ≠ 0 ဖြစ်သည့် အချိန်** တွင်
ဆောင်ရွက်ရမည်။

**သက်ဆိုင်သည့် term —** Saturation, Tail Latency, Admission Control, Load Shedding, Retry Budget

#### အဖြေ ၂ — dependency တစ်ခု ချို့ယွင်းပါက ဝန်ဆောင်မှု ပြိုလဲခြင်း

**ရောဂါရှာဖွေသည့် လမ်း —** ဤ လက္ခဏာသည် **ချို့ယွင်းမှု ပျံ့နှံ့ခြင်း (cascade)** ဖြစ်သည်။
ခေါ်ဆိုမှု တိုင်းသည် timeout အထိ စောင့်သဖြင့် အလုပ်သမား (worker) အားလုံး ကိုင်ထားခံရပြီး၊
ကျန်ရှိသည့် feature များလည်း အလုပ်မလုပ်နိုင်တော့ပါ။ instance အားလုံး ချက်ချင်း unready
ဖြစ်ခြင်းသည် readiness probe သည် အရေးမကြီးသည့် dependency ကို မဖြစ်မနေ စစ်နေခြင်းကို ပြသည်။

**ဖြေရှင်းချက် —** (၁) circuit breaker ဖြင့် ချို့ယွင်းနေသည့် dependency ကို ချက်ချင်း ငြင်းပယ်ပြီး
ဝန်ကို 99% ကျော် လျှော့ခြင်း (ဥပမာ ၃)။ (၂) degradation ladder ဖြင့် ထို dependency မပါဘဲ
အဓိက အဖြေကို ဆက်ပေးခြင်း၊ လျှော့ချ mode ကို operator နှင့် အသုံးပြုသူ သိစေခြင်း။
(၃) deadline propagation ဖြင့် ကျန်ရှိသည့် budget ကုန်သည့် အလုပ်ကို ပလပ်ဖျက်ခြင်း။
(၄) readiness probe ကို ဝန်ဆောင်မှု ပေးရန် လိုအပ်သည့် အနည်းဆုံး dependency ဖြင့်သာ စစ်ခြင်း။
(၅) fallback ကို dependency ချို့ယွင်းမှု အောက်တွင် စမ်းသပ်ပြီး၊ shadow traffic ဖြင့်
အစစ်အမှန် input ဖြင့် စစ်ဆေးခြင်း။

**မည်သည့် ကိန်းဂဏန်းက ဆုံးဖြတ်သည် —** error attribution သည် မည်သည့် dependency က
ချို့ယွင်းမှုကို ဖြစ်စေသည်ကို ပြသည်။ circuit breaker ၏ probe ဝန်နှင့် open အချိန် သည်
"dependency ကို အသက်ရှူခွင့်" ပေးသည့် အတိုင်းအတာ ဖြစ်သည်။

**သက်ဆိုင်သည့် term —** Graceful Degradation, Readiness Probe, Deadline Propagation, Availability, Tail Latency

#### အဖြေ ၃ — မြင်တွေ့နိုင်သည့် incident မရှိဘဲ error budget ကုန်နေခြင်း

**ရောဂါရှာဖွေသည့် လမ်း —** budget ကုန်နေသော်လည်း alert မဖြစ်ခြင်းသည် **တိုင်းတာမှု နှင့်
လုပ်ဆောင်ချက် အကြား ကွာဟမှု** ဖြစ်သည် — SLI သည် အသုံးပြုသူ ခံစားသည့် ရလဒ်ကို
ခြေရာခံနေခြင်း မရှိတော့ပါ၊ သို့မဟုတ် alert သည် slow burn ကို ဖမ်းနိုင်သည့် window
မရှိပါ။

**ဖြေရှင်းချက် —** (၁) SLI ၏ numerator၊ denominator၊ exclusions ကို version control ထဲတွင်
ထား၍ ပြောင်းလဲမှု တိုင်းကို မှတ်တမ်းတင်ခြင်း။ (၂) fast burn နှင့် slow burn window နှစ်ခု
တွဲသုံးခြင်း (ဥပမာ ၁ နှင့် အဖြေ ၆)။ (၃) budget ကို route၊ tenant နှင့် canary cohort အလိုက်
ခွဲကြည့်ခြင်း။ (၄) degradation mode က cached အဖြေ ပြန်ပေးသည့် အချိန်ကို SLI တွင်
အသိအမှတ်ပြုခြင်း — "အောင်မြင်သည်" ဟု ရေတွက်ခြင်းသည် အသုံးပြုသူ ခံစားသည့်
အရည်အသွေးနှင့် ကွာဟပါက SLI သည် အဓိပ္ပာယ် မရှိတော့ပါ။ (၅) shadow traffic ဖြင့်
ကိုယ်စားလှယ် စနစ်ကို အစစ်အမှန် input ဖြင့် စမ်းသပ်ခြင်း။

**မည်သည့် ကိန်းဂဏန်းက ဆုံးဖြတ်သည် —** budget အသုံးပြုမှု ရာခိုင်နှုန်းသည် 60% ဖြစ်ပြီး
incident မှတ်တမ်း မရှိပါက **accounting နှင့် definition ကို ဦးစွာ စစ်ရမည်**၊ ထို့နောက်
burn rate window များကို စစ်ရမည်။

**သက်ဆိုင်သည့် term —** Service Level Indicator (SLI), Error Budget, Graceful Degradation, Canary Release, Shadow Traffic

### ၅.၃ ဆုံးဖြတ်ချက် အဖြေများ

#### အဖြေ ၁ — SLO ကို 99.9% သို့မဟုတ် 99.99% ရွေးချယ်ခြင်း

**ယူဆချက် —** ပြတ်တောက်မှု တစ်မိနစ်လျှင် ရောင်းရငွေ ဆုံးရှုံးမှုနှင့် SLA credit စုစုပေါင်း
USD 1,000။ တစ်နှစ်တွင် 525,600 မိနစ် ရှိသည်။ infrastructure ကုန်ကျစရိတ်သည် A တွင်
USD 12,000/လ၊ B တွင် USD 29,000/လ။

**ဖော်မြူလာ —** yearly cost = infrastructure (USD/လ × 12) + downtime minutes × cost per minute။
break-even cost per minute = (infra_B − infra_A) × 12 ÷ (minutes lost A − minutes lost B)။

**တွက်ချက်မှု —** A ၏ ပြတ်တောက်ချိန် = 0.001 × 525,600 = 525.6 မိနစ်၊ B ၏ ပြတ်တောက်ချိန်
= 52.56 မိနစ်။ yearly cost A = 144,000 + 525,600 = USD 669,600၊ B = 348,000 + 52,560 = USD 400,560
ဖြစ်သည်။ break-even = (29,000 − 12,000) × 12 ÷ 473.04 = USD 431.25/မိနစ် ဖြစ်သည်။

**ရလဒ် —** ထို ယူဆချက်များအောက်တွင် Option B သည် အနှစ် USD 269,040 သက်သာသည်။
သို့သော် ပြတ်တောက်မှု တစ်မိနစ်၏ ကုန်ကျစရိတ်သည် USD 431.25 အောက် ကျပါက
Option A သည် သက်သာသည်။

**အကြောင်းရင်း —** SLO ကို တိုးနိုင်သည့် ပမာဏ တစ်ခုအဖြစ် မဆုံးဖြတ်ရ — တစ်ခု ပိုသော nine သည်
ကုန်ကျစရိတ်ကို တိုးပြီး၊ ခွင့်ပြုသည့် ပြတ်တောက်ချိန်ကို 10 ဆ လျှော့သည်။ ထို ဆုံးဖြတ်ချက်သည်
**ပြတ်တောက်မှု တစ်မိနစ်၏ တန်ဖိုး** အပေါ် မူတည်သဖြင့် break-even ကိန်းဂဏန်းကို
တွက်ရမည်။ ငွေကြေး ဂဏန်းများသည် အဖွဲ့အစည်း အလိုက် ကွာခြားသဖြင့် ရလဒ်သည်
"ပြတ်တောက်မှု တစ်မိနစ်လျှင် USD 431 ကျော်ပါက B ကို ရွေးပါ" ဟူသည့် ပုံသဏ္ဍာန်ကို
မှတ်ရမည်။

```bash
python3 - <<'PY'
infra_a = 12000.0
infra_b = 29000.0
minutes_year = 365 * 24 * 60
down_a = (1 - 0.999) * minutes_year
down_b = (1 - 0.9999) * minutes_year
rev_per_min = 1000.0
year_a = infra_a * 12 + down_a * rev_per_min
year_b = infra_b * 12 + down_b * rev_per_min
print("option A: SLO 99.9%  infra USD", infra_a, "per month, downtime minutes per year", round(down_a, 1))
print("option B: SLO 99.99% infra USD", infra_b, "per month, downtime minutes per year", round(down_b, 1))
print()
print("option A yearly cost (USD)", round(year_a, 2), "= infrastructure", round(infra_a * 12, 2),
      "+ lost minutes", round(down_a * rev_per_min, 2))
print("option B yearly cost (USD)", round(year_b, 2), "= infrastructure", round(infra_b * 12, 2),
      "+ lost minutes", round(down_b * rev_per_min, 2))
print("option B is cheaper by (USD)", round(year_a - year_b, 2))
print()
break_even = (infra_b - infra_a) * 12 / (down_a - down_b)
print("minutes of downtime saved per year", round(down_a - down_b, 2))
print("break-even cost of one minute of downtime (USD)", round(break_even, 2))
print("below that price the cheaper option is A, above it option B pays for itself")
PY
```


```text
option A: SLO 99.9%  infra USD 12000.0 per month, downtime minutes per year 525.6
option B: SLO 99.99% infra USD 29000.0 per month, downtime minutes per year 52.6

option A yearly cost (USD) 669600.0 = infrastructure 144000.0 + lost minutes 525600.0
option B yearly cost (USD) 400560.0 = infrastructure 348000.0 + lost minutes 52560.0
option B is cheaper by (USD) 269040.0

minutes of downtime saved per year 473.04
break-even cost of one minute of downtime (USD) 431.25
below that price the cheaper option is A, above it option B pays for itself
```


#### အဖြေ ၂ — Accept-all သို့မဟုတ် admission control နှင့် load shedding

**ယူဆချက် —** useful capacity 2,000 rps၊ demand 2,600 rps၊ accept-all တွင် request ၏ 40% သည်
deadline ကျော်လွန်၍ client များက retry ၂ ကြိမ် ထပ်လုပ်သည်။

**ဖော်မြူလာ —**
- offered work = demand × (1 + timeout share × retries)
- useful throughput (accept-all) = capacity ÷ (1 + timeout share × retries)
- shed reject rate = (demand − capacity) ÷ demand
- budget ကုန်သည့် အချိန် = monthly budget ÷ rejected rps

**တွက်ချက်မှု —** accept-all တွင် offered work = 2,600 × 1.8 = 4,680 rps ဖြစ်သည်၊ capacity ၏
2.34 ဆ ဖြစ်သဖြင့် queue သည် တည်ငြိမ်မှု မရှိတော့ပါ။ ပြီးမြောက်သည့် request တိုင်းသည်
1.8 ဆ အလုပ်ဖြင့် "ပေးဆောင်" သဖြင့် useful throughput သည် 2,000 ÷ 1.8 = 1,111 rps အထိ ကျသည်။
admission control + shedding တွင် shed reject rate = 600 ÷ 2,600 = 23.1% ဖြစ်ပြီး
useful throughput သည် 2,000 rps ဖြစ်သည် — accept-all ထက် 888.9 rps ပိုသည်။

**SLO နှင့် ဆက်စပ်မှု —** shed လုပ်သည့် 600 rps သည် "မအောင်မြင်သည့်" request ဖြစ်သဖြင့်
2,000 request budget ကို 3.33 စက္ကန့်အတွင်း ကုန်စေသည် — ၁ မိနစ်စာ shedding သည် တစ်လစာ
budget ၏ 18 ဆ ဖြစ်သည်။ overload သည် ၁ နာရီ ကြာပါက budget ခွင့်ပြုသည့် မအောင်မြင်နှုန်းသည်
0.0214% သာ ဖြစ်ပြီး shedding သည် 23.1% ကို ငြင်းပယ်ရမည် ဖြစ်သည်။

**ရလဒ်နှင့် အကြံပြုချက် —** (၁) **load shedding ကို ရွေးရမည်** — ၎င်းသည် useful throughput
ကို 1,111 rps မှ 2,000 rps အထိ တိုးပေးပြီး လက်ခံပြီးသား အလုပ်ကို deadline အတွင်း
ပြီးမြောက်စေသည်။ (၂) သို့သော် shedding သည် SLO 99.9% ကို **စက္ကန့်ပိုင်းအတွင်း ကုန်စေ** သဖြင့်
overload အခြေအနေကို "မှတ်တမ်းတင်ထားသည့် ဖယ်ထားသည့် အခြေအနေ" (documented exclusion)
အဖြစ် သတ်မှတ်ခြင်း သို့မဟုတ် SLO ကို overload အခြေအနေနှင့် ကိုက်ညီစေရန် error-budget
policy တွင် ရေးဆွဲခြင်း လိုအပ်သည်။ (၃) ငြင်းပယ်သည့်အခါ အခြေအနေသည် ယာယီ ဖြစ်ပြီး
caller ၏ retry budget က ခွင့်ပြုသည့်အခါမှသာ retryable အဖြစ် သတ်မှတ်ရမည် — မဟုတ်ပါက
retry များသည် (အဖြေ ၂ တွင် တွက်ပြသည့်အတိုင်း) ဝန်ကို ဆင့်ပွားစေသည်။

```bash
python3 - <<'PY'
capacity_rps = 2000.0
demand_rps = 2600.0
budget_failures = 2000
slo_requests = 2_000_000
print("useful capacity", capacity_rps, "rps, offered demand", demand_rps, "rps")
print()
print("policy A - accept everything")
timeout_share = 0.40
retries_each = 2
offered = demand_rps * (1 + timeout_share * retries_each)
goodput_accept_all = capacity_rps / (1 + timeout_share * retries_each)
print("  requests that time out and retry", timeout_share, "each retrying", retries_each, "times")
print("  offered work after retries", offered, "rps =", round(offered / capacity_rps, 2), "x capacity")
print("  useful throughput", round(goodput_accept_all, 1), "rps because every served request is paid for",
      round(1 + timeout_share * retries_each, 1), "times")
print()
print("policy B - admission control and load shedding at", capacity_rps, "rps")
shed_rps = demand_rps - capacity_rps
print("  rejected requests", shed_rps, "rps =", f"{shed_rps / demand_rps:.1%}", "of demand")
print("  useful throughput", capacity_rps, "rps, admitted work keeps its deadline")
print("  extra useful throughput over policy A:", round(capacity_rps - goodput_accept_all, 1), "rps")
print()
print("cost of shedding for the 99.9% SLO: budget is", budget_failures, "failed requests in a 30 day window")
print("  at", shed_rps, "rejected rps the budget is gone in", round(budget_failures / shed_rps, 2), "s")
print("  1 minute of shedding costs", int(shed_rps * 60), "failures =",
      round(shed_rps * 60 / budget_failures, 1), "x the whole monthly budget")
allowed = budget_failures / (demand_rps * 3600)
print("  if overload lasted 1 h, the failure share the budget allows is", f"{allowed:.4%}",
      "but shedding rejects", f"{shed_rps / demand_rps:.1%}")
PY
```


```text
useful capacity 2000.0 rps, offered demand 2600.0 rps

policy A - accept everything
  requests that time out and retry 0.4 each retrying 2 times
  offered work after retries 4680.0 rps = 2.34 x capacity
  useful throughput 1111.1 rps because every served request is paid for 1.8 times

policy B - admission control and load shedding at 2000.0 rps
  rejected requests 600.0 rps = 23.1% of demand
  useful throughput 2000.0 rps, admitted work keeps its deadline
  extra useful throughput over policy A: 888.9 rps

cost of shedding for the 99.9% SLO: budget is 2000 failed requests in a 30 day window
  at 600.0 rejected rps the budget is gone in 3.33 s
  1 minute of shedding costs 36000 failures = 18.0 x the whole monthly budget
  if overload lasted 1 h, the failure share the budget allows is 0.0214% but shedding rejects 23.1%
```


## Self-check

1. `Admission Control` နှင့် `Load Shedding` သည် မည်သည့် နေရာတွင် ကွာခြားသနည်း။
2. SLO 99.9% နှင့် 30-day window အတွက် error budget သည် request 2,000,000 တွင် မည်မျှ ဖြစ်သနည်း။
3. Retry ၃ ကြိမ်၊ failure rate 50% ဖြစ်ပါက amplification သည် မည်မျှ ဖြစ်သနည်း၊ အလွှာ ၃ ဆင့်
   ဆိုပါက မည်သို့ ပြောင်းသနည်း။
4. Error budget ကို alert မလုပ်ဘဲ ကုန်စေနိုင်သည့် အကြောင်းရင်း သုံးခုကို ဖော်ပြပါ။
5. Incident တစ်ခု၏ timeline တွင် မည်သည့် အပိုင်းကို တိုစေခြင်းသည် budget အပေါ် အကြီးမားဆုံး
   သက်ရောက်မှု ရှိသနည်း။

<details>
<summary>အဖြေများ</summary>

1. `Admission Control` သည် လက်ခံမှု **မပြုမီ** အလုပ်လုပ်သည့် gate ဖြစ်သည်။ `Load Shedding` သည်
   ingress၊ queue များ၊ dependency များ သို့မဟုတ် အခြား overload နယ်နိမိတ်များတွင် အလုပ်ကို
   ငြင်းပယ် သို့မဟုတ် ဖယ်ရှားနိုင်သည် — လက်ခံပြီးသား အလုပ်အပေါ်တွင်လည်း သက်ရောက်နိုင်သည်။
2. budget fraction = 0.001 ဖြစ်သဖြင့် 2,000,000 × 0.001 = 2,000 request = 43.2 မိနစ် ဖြစ်သည်။
3. amplification = 1 + 0.5 + 0.25 + 0.125 = 1.875 ဖြစ်သည်။ အလွှာ ၃ ဆင့်တွင် 1.875³ = 6.592 ဖြစ်သဖြင့်
   origin 2,000 rps သည် 13,184 rps အထိ တိုးသည်။
4. ဥပမာ — (က) SLI ၏ exclusions သည် တိတ်ဆိတ်စွာ ပြောင်းလဲခြင်း၊ (ခ) degradation mode က cached
   အဖြေကို အောင်မြင်မှုအဖြစ် ရေတွက်ခြင်း၊ (ဂ) slow burn ကို ဖမ်းနိုင်သည့် window မရှိခြင်း။
5. ဖော်ထုတ်မှု (detect) အပိုင်း ဖြစ်သည် — ထို အပိုင်းကို တိုစေခြင်းသည် မည်သည့် incident တွင်မဆို
   စားသုံးသည့် budget ကို တိုက်ရိုက် လျှော့ပေးသည့်အပြင် ပြန်လည် ကောင်းမွန်စေသည့် အချိန်ကိုပါ
   တိုစေသည်။

</details>

## References

- Source glossary — https://aiengineeringfromscratch.com/glossary
- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် — [`../../terms/10_reliability_and_operations.md`](../../terms/10_reliability_and_operations.md)
- ပုံရှင်းလင်းချက်များ — [`02_visual_explanations.md`](02_visual_explanations.md)
- Google SRE — [Handling Overload](https://sre.google/sre-book/handling-overload/), [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/), [Error Budget Policy](https://sre.google/workbook/error-budget-policy/), [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/), [Managing Incidents](https://sre.google/sre-book/managing-incidents/), [Postmortem Culture](https://sre.google/sre-book/postmortem-culture/), [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- gRPC — [Deadlines](https://grpc.io/docs/guides/deadlines/); Kubernetes — [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- The Tail at Scale — https://research.google/pubs/the-tail-at-scale/
