# Labs — Area 08: AI-native development

ဤ lab suite သည် area 08 ၏ term များ (Progressive Disclosure, Repository Map, Token Budget,
Reviewer Agent, Cost per Successful Task, Retry with Backoff) ကို လက်တွေ့ တွက်ကြည့်ရန် ဖြစ်သည်။
Python standard library သာ အသုံးပြုသည်၊ network နှင့် GPU မလိုအပ်ပါ၊ run တိုင်း ရလဒ် တူညီသည်
(deterministic)။

Lab တိုင်းတွင် `--sweep` (knob တစ်ခုကို အပိုင်းအခြားအတွင်း လှည့်ကြည့်ခြင်း) နှင့်
`--self-test` (lab သင်ပေးသည့် ဂုဏ်သတ္တိကို assert လုပ်ခြင်း) ပါသည်။ ဤစာတမ်းရှိ
ကိန်းဂဏန်း အားလုံးသည် သတ်မှတ်ထားသည့် ယူဆချက် (assumption) များမှ တွက်ချက်ထားသည်၊
benchmark မဟုတ်ပါ။

## Run the whole suite (မဖြစ်မနေ)

```bash
cd guides/08_ai_native_development/labs
python3 run_labs.py
```

Lab တိုင်းအတွက် `--self-test` ကို run ပြီး တစ်လိုင်း စီ ပြသည်။ အားလုံး အောင်မြင်ပါက
`[PASS] All 3/3 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်သည်။

```
==========================================================================
run_labs - area 08 AI-native development (offline, deterministic)
==========================================================================
[PASS] lab_context_strategy.py: [PASS] lab_context_strategy self-test passed.
[PASS] lab_review_budget.py: [PASS] lab_review_budget self-test passed.
[PASS] lab_change_cost.py: [PASS] lab_change_cost self-test passed.
==========================================================================
[PASS] All 3/3 labs passed successfully.
```

## lab_context_strategy.py — whole-repo နှင့် scoped context

whole-repo context၊ directory-scoped context နှင့် retrieval-scoped context သုံးမျိုးအတွက်
token အရေအတွက်၊ ကုန်ကျစရိတ်၊ window ထဲ ဆံ့မှု နှင့် ချွေတာမှုကို ပြသည်။

```bash
python3 lab_context_strategy.py                        # repo-files 900, avg-file-tokens 420, scope-files 60, window 128000, price 3.00
python3 lab_context_strategy.py --scope-files 120 --window 32000
python3 lab_context_strategy.py --sweep                 # scope-files 8 .. 900
python3 lab_context_strategy.py --self-test
python3 lab_context_strategy.py --help
```

Default run ၏ အမှန်တကယ် output -

```
==========================================================================
lab_context_strategy - whole-repo vs scoped context (offline, deterministic)
repo-files=900  avg-file-tokens=420  scope-files=60  window=128,000  price=USD 3.00/Mtok
assumption - retrieval scope = 12 files; price is an assumed input-token price.
--------------------------------------------------------------------------
strategy            files  context tokens   USD/task  fits window  saving vs whole
whole-repo            900         378,000     1.1340  NO                         -
directory-scoped       60          25,200     0.0756  YES                   93.33%
retrieval-scoped       12           5,040     0.0151  YES                   98.67%
--------------------------------------------------------------------------
retrieval-scoped saves USD 1.1189 per task against whole-repo context
directory-scoped stays 19.69% of the window; whole-repo needs 2.95x the window
မှတ်ချက် - context ကို ကျဉ်းစွာ ရွေးလျှင် token နှင့် ကုန်ကျစရိတ် ကျဆင်းသည်၊ သို့သော် လိုအပ်သည့် အထောက်အထား မကျန်ခဲ့ရန် သတိထားရမည်။
==========================================================================
```

Knob ပြောင်းသည့် run (`--scope-files 120 --window 32000`) ၏ အမှန်တကယ် output -

```bash
python3 lab_context_strategy.py --scope-files 120 --window 32000
```

```
==========================================================================
lab_context_strategy - whole-repo vs scoped context (offline, deterministic)
repo-files=900  avg-file-tokens=420  scope-files=120  window=32,000  price=USD 3.00/Mtok
assumption - retrieval scope = 12 files; price is an assumed input-token price.
--------------------------------------------------------------------------
strategy            files  context tokens   USD/task  fits window  saving vs whole
whole-repo            900         378,000     1.1340  NO                         -
directory-scoped      120          50,400     0.1512  NO                    86.67%
retrieval-scoped       12           5,040     0.0151  YES                   98.67%
--------------------------------------------------------------------------
retrieval-scoped saves USD 1.1189 per task against whole-repo context
directory-scoped stays 157.50% of the window; whole-repo needs 11.81x the window
မှတ်ချက် - context ကို ကျဉ်းစွာ ရွေးလျှင် token နှင့် ကုန်ကျစရိတ် ကျဆင်းသည်၊ သို့သော် လိုအပ်သည့် အထောက်အထား မကျန်ခဲ့ရန် သတိထားရမည်။
==========================================================================
```

## lab_review_budget.py — review minutes၊ queue နှင့် လွတ်ထွက်သည့် defect

ထုတ်လုပ်လိုက်သည့် စာကြောင်းများအတွက် review minutes ကို တွက်ပြီး reviewer capacity နှင့်
နှိုင်းယှဉ်သည်။ capacity ကျော်လွန်လျှင် queue ဖြစ်ပေါ်ပြီး စစ်ဆေးမရသည့် စာကြောင်းများမှ
defect များ လွတ်ထွက်သည်။

```bash
python3 lab_review_budget.py                           # generated-lines 1200, review-min-per-100 25, defect-rate 0.08, capacity 480
python3 lab_review_budget.py --generated-lines 3000 --defect-rate 0.12
python3 lab_review_budget.py --sweep                    # generated-lines 300 .. 9600
python3 lab_review_budget.py --self-test
python3 lab_review_budget.py --help
```

Default run ၏ အမှန်တကယ် output -

```
==========================================================================
lab_review_budget - review minutes, queue, escaping defects, cost
generated-lines=1,200  review-min-per-100=25.0  defect-rate=0.080  capacity=480 min
assumption - reviewer catches 70% of defects in reviewed lines; reviewer cost USD 60.00/hour (assumed).
--------------------------------------------------------------------------
review minutes                   :      300.0
reviewer capacity (min)          :      480.0
lines reviewable this period     :    1,200.0
queue beyond capacity (min)      :        0.0
defects in generated lines       :       96.0
defects caught in review         :       67.2
defects escaping                 :       28.8
review cost (reviewer-hours)     :       5.00
review cost (USD, assumed)       :     300.00
--------------------------------------------------------------------------
review cost per 100 lines = USD 25.00 (assumed rate 60.00/hour)
မှတ်ချက် - review minutes သည် capacity ကို ကျော်လွန်လျှင် queue ဖြစ်ပေါ်ပြီး၊ စစ်ဆေးမရသည့် စာကြောင်းများမှ defect များ လွတ်ထွက်သည်။
==========================================================================
```

Knob ပြောင်းသည့် run (`--generated-lines 3000 --defect-rate 0.12`) ၏ အမှန်တကယ် output -

```bash
python3 lab_review_budget.py --generated-lines 3000 --defect-rate 0.12
```

```
==========================================================================
lab_review_budget - review minutes, queue, escaping defects, cost
generated-lines=3,000  review-min-per-100=25.0  defect-rate=0.120  capacity=480 min
assumption - reviewer catches 70% of defects in reviewed lines; reviewer cost USD 60.00/hour (assumed).
--------------------------------------------------------------------------
review minutes                   :      750.0
reviewer capacity (min)          :      480.0
lines reviewable this period     :    1,920.0
queue beyond capacity (min)      :      270.0
defects in generated lines       :      360.0
defects caught in review         :      161.3
defects escaping                 :      198.7
review cost (reviewer-hours)     :      12.50
review cost (USD, assumed)       :     750.00
--------------------------------------------------------------------------
review cost per 100 lines = USD 25.00 (assumed rate 60.00/hour)
မှတ်ချက် - review minutes သည် capacity ကို ကျော်လွန်လျှင် queue ဖြစ်ပေါ်ပြီး၊ စစ်ဆေးမရသည့် စာကြောင်းများမှ defect များ လွတ်ထွက်သည်။
==========================================================================
```

## lab_change_cost.py — retry ပါဝင်သည့် cost per merged change

သတ်မှတ်ထားသည့် success rate အောက်တွင် လုပ်ငန်း တစ်ခုလျှင် လိုအပ်သည့် attempt အရေအတွက်၊
retry အရေအတွက်၊ merged change တစ်ခုလျှင် ကုန်ကျစရိတ် နှင့် စုစုပေါင်း ကုန်ကျစရိတ်ကို ပြသည်။

```bash
python3 lab_change_cost.py                             # tasks 100, attempts 4, success-rate 0.62, tokens-per-attempt 9000, price 3.00, repo-hour 45.00
python3 lab_change_cost.py --success-rate 0.45 --attempts 5
python3 lab_change_cost.py --sweep                      # success-rate 0.30 .. 0.90
python3 lab_change_cost.py --self-test
python3 lab_change_cost.py --help
```

Default run ၏ အမှန်တကယ် output -

```
==========================================================================
lab_change_cost - cost per merged change with retries (offline, deterministic)
tasks=100  attempts=4  success-rate=0.620  tokens-per-attempt=9,000  price=USD 3.00/Mtok  repo-hour=USD 45.00
assumption - each attempt consumes 6.0 minutes of repo wall-clock time.
--------------------------------------------------------------------------
cost per attempt (tokens)        : USD   0.0270
cost per attempt (wall-clock)    : USD   4.5000
cost per attempt (total)         : USD   4.5270
expected attempts per task       :       1.5793
success probability per task     :       0.9791
retries beyond first attempt      :        57.93
merged changes                   :        97.91
cost per merged change           : USD   7.3016
total cost                       : USD   714.94
--------------------------------------------------------------------------
a failed attempt costs USD 4.5270 and yields nothing until it succeeds; the multiplier is 1.613x
မှတ်ချက် - success rate နိမ့်လျှင် retry အရေအတွက် တိုးပြီး၊ merged change တစ်ခုလျှင် ကုန်ကျစရိတ် မြင့်သည်။
==========================================================================
```

Knob ပြောင်းသည့် run (`--success-rate 0.45 --attempts 5`) ၏ အမှန်တကယ် output -

```bash
python3 lab_change_cost.py --success-rate 0.45 --attempts 5
```

```
==========================================================================
lab_change_cost - cost per merged change with retries (offline, deterministic)
tasks=100  attempts=5  success-rate=0.450  tokens-per-attempt=9,000  price=USD 3.00/Mtok  repo-hour=USD 45.00
assumption - each attempt consumes 6.0 minutes of repo wall-clock time.
--------------------------------------------------------------------------
cost per attempt (tokens)        : USD   0.0270
cost per attempt (wall-clock)    : USD   4.5000
cost per attempt (total)         : USD   4.5270
expected attempts per task       :       2.1104
success probability per task     :       0.9497
retries beyond first attempt      :       111.04
merged changes                   :        94.97
cost per merged change           : USD  10.0600
total cost                       : USD   955.37
--------------------------------------------------------------------------
a failed attempt costs USD 4.5270 and yields nothing until it succeeds; the multiplier is 2.222x
မှတ်ချက် - success rate နိမ့်လျှင် retry အရေအတွက် တိုးပြီး၊ merged change တစ်ခုလျှင် ကုန်ကျစရိတ် မြင့်သည်။
==========================================================================
```

## မှတ်ချက်

- Output အားလုံးကို `python3 verify_guide.py --guide 08 --labs --verbose` ဖြင့် စစ်ဆေးနိုင်သည်။
- `--self-test` သည် တိကျသည့် ဂုဏ်သတ္တိများကို assert လုပ်သည် (context token သည်
  ဖိုင် အရေအတွက်နှင့် အချိုးကျသည်၊ whole-repo context သည် window ထဲ မဆံ့ပါ၊ scope သည်
  whole repo နှင့် တူညီလျှင် ချွေတာမှု သုည ဖြစ်သည်၊ review minutes သည် ထုတ်လုပ်သည့်
  စာကြောင်းနှင့် အချိုးကျသည်၊ capacity ကျော်လျှင် queue ဖြစ်ပြီး လွတ်ထွက်သည့် defect တိုးသည်၊
  cost per merged change သည် cost per attempt အောက် မရောက်ပါ)။
- Flag တိုင်း၏ အဓိပ္ပာယ်ကို `python3 <lab> --help` ဖြင့် ကြည့်နိုင်သည်။
