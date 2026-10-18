# Labs - Area 07: Evaluation & Safety

ဤ lab suite သည် area 07 ၏ term များ (Eval Set, Evaluation, Guardrails, Distribution Shift,
LLM-as-a-Judge, Calibration) ကို လက်တွေ့ တွက်ကြည့်ရန် ဖြစ်သည်။ Python standard library သာ
အသုံးပြုသည်၊ network နှင့် GPU မလိုအပ်ပါ၊ run တိုင်း ရလဒ် တူညီသည် (deterministic)။
lab သုံးခုလုံးတွင် `--sweep` နှင့် `--self-test` ပါသည်။

## Run the whole suite (မဖြစ်မနေ)

```bash
cd guides/07_evaluation_and_safety/labs
python3 run_labs.py
```

Lab တိုင်းအတွက် `--self-test` ကို run ပြီး တစ်လိုင်း စီ ပြသည်။ အားလုံး အောင်မြင်ပါက
`[PASS] All 3/3 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်သည်။

```
==========================================================================
run_labs - area 07 Evaluation & safety (offline, deterministic)
==========================================================================
[PASS] lab_eval_size.py: [PASS] lab_eval_size self-test passed.
[PASS] lab_guardrail_cost.py: [PASS] lab_guardrail_cost self-test passed.
[PASS] lab_drift_monitor.py: [PASS] lab_drift_monitor self-test passed.
==========================================================================
[PASS] All 3/3 labs passed successfully.
```

## lab_eval_size.py - eval အရွယ်အစား နှင့် model နှစ်ခု ခွဲခြားနိုင်မှု

ကိန်း သုံးခုကို ပြသည် — ရွေးထားသည့် n တွင် လက်တွေ့ ကွာဟမှု နှင့် ၎င်း၏ standard error၊
trial များအကြား ကွာဟမှု၏ ပျံ့နှံ့မှု၊ နှင့် model နှစ်ခုကို ခွဲခြားနိုင်သည့် အနိမ့်ဆုံး n။
ခွဲခြားသည့် စည်းမျဉ်းမှာ ကွာဟမှုသည် `1.96 × standard error` ကို ကျော်လွန်ခြင်း ဖြစ်သည်။

```bash
python3 lab_eval_size.py                                 # default: n 500, acc-a 0.72, acc-b 0.80, seed 1, trials 50
python3 lab_eval_size.py --n 200 --seed 3 --trials 20     # ပြောင်းထားသည့် knob
python3 lab_eval_size.py --sweep                          # n 64 .. 32768
python3 lab_eval_size.py --self-test
python3 lab_eval_size.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_eval_size - how large an eval set must be to separate two models
offline, deterministic simulation; n=500  acc-a=0.720  acc-b=0.800  seed=1  trials=50
--------------------------------------------------------------------------
1) point estimate at n=500 (seed=1)
   observed gap a->b        :    0.08200
   standard error of gap    :    0.02689
   separation threshold     :    0.05271   (1.96 x se)
   verdict                  :  SEPARATED
--------------------------------------------------------------------------
2) spread of the observed gap over 50 trials
          n     min gap     mean gap      max gap  separation rate
        500     0.02400      0.07692      0.14200            88.0%
       1000     0.04700      0.07856      0.11900           100.0%
       2000     0.05000      0.07915      0.10800           100.0%
--------------------------------------------------------------------------
3) smallest eval size that separates them
   analytic n* for delta=0.080  :      218 items (se 0.04073, delta/se 1.96)
   se at n* x 4              :    0.02036
   first size where every trial separates :     2048 items
   ratio (every-size / n*)   :       9.39
--------------------------------------------------------------------------
မှတ်ချက် - eval size သေးငယ်လျှင် ကွာဟမှု၏ standard error ကြီးသည့်အတွက် model နှစ်ခုကို
ခွဲခြားနိုင်ခြင်း မရှိပါ။ n လေးဆ တိုးလျှင် standard error ထက်ဝက် ကျဆင်းသည်။ analytic n*
သည် ပျမ်းမျှအားဖြင့် ခွဲခြားနိုင်သည့် အရေအတွက် ဖြစ်ပြီး run တိုင်း ခွဲခြားရန် ပို၍ လိုသည်။
==========================================================================
```

Knob ပြောင်းထားသည့် run (`--n 200 --seed 3 --trials 20`) ၏ အမှန်တကယ် output -
```bash
python3 lab_eval_size.py --n 200 --seed 3 --trials 20
```

```
==========================================================================
lab_eval_size - how large an eval set must be to separate two models
offline, deterministic simulation; n=200  acc-a=0.720  acc-b=0.800  seed=3  trials=20
--------------------------------------------------------------------------
1) point estimate at n=200 (seed=3)
   observed gap a->b        :    0.04000
   standard error of gap    :    0.04252
   separation threshold     :    0.08334   (1.96 x se)
   verdict                  : NOT SEPARATED
--------------------------------------------------------------------------
2) spread of the observed gap over 20 trials
          n     min gap     mean gap      max gap  separation rate
        200     0.01000      0.08950      0.16000            50.0%
        400     0.03750      0.07700      0.13500            60.0%
        800     0.03000      0.07581      0.11625            95.0%
--------------------------------------------------------------------------
3) smallest eval size that separates them
   analytic n* for delta=0.080  :      218 items (se 0.04073, delta/se 1.96)
   se at n* x 4              :    0.02036
   first size where every trial separates :     2048 items
   ratio (every-size / n*)   :       9.39
--------------------------------------------------------------------------
မှတ်ချက် - eval size သေးငယ်လျှင် ကွာဟမှု၏ standard error ကြီးသည့်အတွက် model နှစ်ခုကို
ခွဲခြားနိုင်ခြင်း မရှိပါ။ n လေးဆ တိုးလျှင် standard error ထက်ဝက် ကျဆင်းသည်။ analytic n*
သည် ပျမ်းမျှအားဖြင့် ခွဲခြားနိုင်သည့် အရေအတွက် ဖြစ်ပြီး run တိုင်း ခွဲခြားရန် ပို၍ လိုသည်။
==========================================================================
```

## lab_guardrail_cost.py - guardrail ၏ latency၊ throughput နှင့် ကုန်ကျစရိတ်

guardrail သည် request လမ်းကြောင်း အတွင်း run သည့်အခါ service time တိုးခြင်း၊ queue wait
တိုးခြင်း၊ ဆောင်ရွက်နိုင်သည့် request အရေအတွက် ကျဆင်းခြင်း နှင့် capacity ကို ပြန်ထိန်းရန်
လိုသည့် worker အရေအတွက် နှင့် USD ကုန်ကျစရိတ်ကို ပြသည်။ Queue model မှာ M/M/c (Erlang C) ဖြစ်သည်။

```bash
python3 lab_guardrail_cost.py                            # default: rps 50, model 900 ms, guardrail 120 ms, workers 64
python3 lab_guardrail_cost.py --rps 55 --latency-ms 200 --model-ms 900 --workers 64   # ပြောင်းထားသည့် knob
python3 lab_guardrail_cost.py --sweep                     # rps 10 .. 100
python3 lab_guardrail_cost.py --self-test
python3 lab_guardrail_cost.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_guardrail_cost - the price of a synchronous guardrail (offline, deterministic)
queue model M/M/c (Erlang C); rps=50  model-ms=900  guardrail-ms=120  workers=64
assumption: worker price USD 0.42 per hour; added p95 = 2.0 x guardrail + 3.0 x extra queue wait
--------------------------------------------------------------------------
quantity                         no guardrail   with guardrail
offered load (erlangs)                 45.000           51.000
utilisation rho                        0.7031           0.7969
P(request waits)                       0.0049           0.0525
mean queue wait Wq (ms)                  0.23             4.12
sustainable requests/s                   71.1             62.7
--------------------------------------------------------------------------
added p50 latency (ms)    :     123.89
added p95 latency (ms)    :     251.67
throughput loss           :      11.76 %  (71.1 -> 62.7 requests/s)
workers for same capacity :         73  (extra 9, USD 90.72 per day)
guardrail cpu cost        : USD  14.0000 per 1e6 requests  (60.48 USD/day at 50 rps)
--------------------------------------------------------------------------
မှတ်ချက် - guardrail သည် service time ကို တိုးစေသည့်အတွက် တူညီသည့် worker အရေအတွက်ဖြင့်
ရရှိနိုင်သည့် request အရေအတွက် ကျဆင်းပြီး queue wait တိုးသည်။ utilisation သည် ၁ နှင့်
နီးလာလျှင် queue wait သည် လျင်မြန်စွာ ကြီးထွားသည့်အတွက် guardrail ကို request လမ်းကြောင်း
အတွင်း မထည့်ဘဲ အလွှာလိုက် စီစဉ်ခြင်းသည် ကုန်ကျစရိတ် သက်သာစေသည်။
==========================================================================
```

Knob ပြောင်းထားသည့် run (`--rps 55 --latency-ms 200`) ၏ အမှန်တကယ် output -
```bash
python3 lab_guardrail_cost.py --rps 55 --latency-ms 200 --model-ms 900 --workers 64
```

```
==========================================================================
lab_guardrail_cost - the price of a synchronous guardrail (offline, deterministic)
queue model M/M/c (Erlang C); rps=55  model-ms=900  guardrail-ms=200  workers=64
assumption: worker price USD 0.42 per hour; added p95 = 2.0 x guardrail + 3.0 x extra queue wait
--------------------------------------------------------------------------
quantity                         no guardrail   with guardrail
offered load (erlangs)                 49.500           60.500
utilisation rho                        0.7734           0.9453
P(request waits)                       0.0314           0.5566
mean queue wait Wq (ms)                  1.95           174.93
sustainable requests/s                   71.1             58.2
--------------------------------------------------------------------------
added p50 latency (ms)    :     372.99
added p95 latency (ms)    :     918.96
throughput loss           :      18.18 %  (71.1 -> 58.2 requests/s)
workers for same capacity :         79  (extra 15, USD 151.20 per day)
guardrail cpu cost        : USD  23.3333 per 1e6 requests  (110.88 USD/day at 55 rps)
--------------------------------------------------------------------------
မှတ်ချက် - guardrail သည် service time ကို တိုးစေသည့်အတွက် တူညီသည့် worker အရေအတွက်ဖြင့်
ရရှိနိုင်သည့် request အရေအတွက် ကျဆင်းပြီး queue wait တိုးသည်။ utilisation သည် ၁ နှင့်
နီးလာလျှင် queue wait သည် လျင်မြန်စွာ ကြီးထွားသည့်အတွက် guardrail ကို request လမ်းကြောင်း
အတွင်း မထည့်ဘဲ အလွှာလိုက် စီစဉ်ခြင်းသည် ကုန်ကျစရိတ် သက်သာစေသည်။
==========================================================================
```

## lab_drift_monitor.py - window များ၊ drift statistic နှင့် သတိပေးချက် ကုန်ကျစရိတ်

window တိုင်း၏ accuracy နှင့် z တန်ဖိုး၊ သတိပေးချက် ဆုံးဖြတ်ချက်၊ ရွေးထားသည့် threshold
အတွက် false-alarm rate နှင့် တစ်ရက်လျှင် အလဟဿ စုံစမ်းစစ်ဆေးမှု အရေအတွက်နှင့် USD ကို ပြသည်။
window သေးလျှင် standard error ကြီးပြီး ပြောင်းလဲမှုကို ဖော်ထုတ်ရန် window အရေအတွက် ပိုလိုသည်။

```bash
python3 lab_drift_monitor.py                             # default: window 200, baseline 0.92, observed 0.85, threshold 3.0
python3 lab_drift_monitor.py --window 100 --observed 0.89 --threshold 2.5 --seed 3   # ပြောင်းထားသည့် knob
python3 lab_drift_monitor.py --sweep                     # shift 0.00 .. 0.12
python3 lab_drift_monitor.py --self-test
python3 lab_drift_monitor.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_drift_monitor - window rates, drift statistic, alert and false-positive cost
offline, deterministic; window=200  baseline=0.920  observed=0.850  threshold=3.00  seed=7
assumption: se = sqrt(p0(1-p0)/window) = 0.01918; alert when |z| >= 3.00
--------------------------------------------------------------------------
1) per-window accuracy and drift statistic (shift = -0.070)
  window  successes   rate          z     decision
       1        170  0.8500     -3.649     ALERT
       2        174  0.8700     -2.606     ok
       3        166  0.8300     -4.692     ALERT
       4        174  0.8700     -2.606     ok
       5        168  0.8400     -4.170     ALERT
       6        171  0.8550     -3.388     ALERT
--------------------------------------------------------------------------
2) decision: ALERT at window 1
   pooled rate 0.8525 over 6 windows -> pooled z -8.619
   analytic windows for the pooled z to reach 3.00 : 0.68
--------------------------------------------------------------------------
3) cost of the false alarms this threshold buys
   false-alarm rate per window     : 0.002700
   windows per day 144 -> false alerts per day : 0.3888
   investigation USD 25.00 per alert -> USD 9.72/day, USD 291.58 per 30 days
--------------------------------------------------------------------------
မှတ်ချက် - window သေးလျှင် standard error ကြီးသည့်အတွက် ပြောင်းလဲမှုကို ဖော်ထုတ်ရန်
window အရေအတွက် ပိုလိုသည်။ threshold ကို နိမ့်လျှင် ဖမ်းယူနိုင်မှု တိုးသော်လည်း false alert
အရေအတွက် တိုးသည့်အတွက် စုံစမ်းစစ်ဆေးမှု ကုန်ကျစရိတ် တိုးသည်။ ကိန်းဂဏန်းများသည်
baseline၊ window အရွယ်အစားနှင့် ကုန်ကျစရိတ် ယူဆချက်အပေါ် မှီခိုသည်။
==========================================================================
```

Knob ပြောင်းထားသည့် run (`--window 100 --observed 0.89 --threshold 2.5`) ၏ အမှန်တကယ် output -
```bash
python3 lab_drift_monitor.py --window 100 --observed 0.89 --threshold 2.5 --seed 3
```

```
==========================================================================
lab_drift_monitor - window rates, drift statistic, alert and false-positive cost
offline, deterministic; window=100  baseline=0.920  observed=0.890  threshold=2.50  seed=3
assumption: se = sqrt(p0(1-p0)/window) = 0.02713; alert when |z| >= 2.50
--------------------------------------------------------------------------
1) per-window accuracy and drift statistic (shift = -0.030)
  window  successes   rate          z     decision
       1         90  0.9000     -0.737     ok
       2         89  0.8900     -1.106     ok
       3         89  0.8900     -1.106     ok
       4         93  0.9300      0.369     ok
       5         91  0.9100     -0.369     ok
       6         86  0.8600     -2.212     ok
--------------------------------------------------------------------------
2) decision: no alert
   pooled rate 0.8967 over 6 windows -> pooled z -2.107
   analytic windows for the pooled z to reach 2.50 : 5.11
--------------------------------------------------------------------------
3) cost of the false alarms this threshold buys
   false-alarm rate per window     : 0.012419
   windows per day 144 -> false alerts per day : 1.7884
   investigation USD 25.00 per alert -> USD 44.71/day, USD 1341.29 per 30 days
--------------------------------------------------------------------------
မှတ်ချက် - window သေးလျှင် standard error ကြီးသည့်အတွက် ပြောင်းလဲမှုကို ဖော်ထုတ်ရန်
window အရေအတွက် ပိုလိုသည်။ threshold ကို နိမ့်လျှင် ဖမ်းယူနိုင်မှု တိုးသော်လည်း false alert
အရေအတွက် တိုးသည့်အတွက် စုံစမ်းစစ်ဆေးမှု ကုန်ကျစရိတ် တိုးသည်။ ကိန်းဂဏန်းများသည်
baseline၊ window အရွယ်အစားနှင့် ကုန်ကျစရိတ် ယူဆချက်အပေါ် မှီခိုသည်။
==========================================================================
```

## မှတ်ချက်

- Output အားလုံးကို `python3 verify_guide.py --guide 07 --labs --verbose` ဖြင့် စစ်ဆေးနိုင်သည်။
- `--self-test` သည် တိကျသည့် ဂုဏ်သတ္တိများကို assert လုပ်သည် (n လေးဆ တိုးလျှင် standard
  error ထက်ဝက် ကျဆင်းခြင်း၊ n ကြီးလျှင် ခွဲခြားနိုင်မှု တိုးခြင်း၊ guardrail သည် latency
  တင်ပြီး throughput စားခြင်း၊ window လေးဆ တိုးလျှင် standard error ထက်ဝက် ကျဆင်းခြင်း၊
  threshold နိမ့်လျှင် false alert တိုးခြင်း)။
- စျေးနှုန်း၊ rate နှင့် accuracy အားလုံးသည် ယူဆချက် (assumption) ဖြစ်သည့်အတွက် ကိန်းဂဏန်း
  တိုင်းကို `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်` ဟု မှတ်သားရမည်။
- Flag တိုင်း၏ အဓိပ္ပာယ်ကို `python3 <lab> --help` ဖြင့် ကြည့်နိုင်သည်။
