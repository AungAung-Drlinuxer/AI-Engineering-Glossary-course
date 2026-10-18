# Labs - Area 10: Reliability & operations

ဤ lab suite သည် area 10 ၏ term များ (queueing headroom၊ saturation၊ retry amplification၊
circuit breaker၊ error budget၊ SLO၊ outage cost) ကို လက်တွေ့ တွက်ကြည့်ရန် ဖြစ်သည်။
Python standard library သာ အသုံးပြုသည်၊ network နှင့် GPU မလိုအပ်ပါ၊ run တိုင်း ရလဒ်
တူညီသည် (deterministic)။ ကိန်းဂဏန်း အားလုံးသည် ဖော်ပြထားသည့် ယူဆချက် (assumption)
မှ တွက်ချက်ထားခြင်း ဖြစ်သည်၊ တိုင်းတာမှု မဟုတ်ပါ။

## Run the whole suite (မဖြစ်မနေ)

```bash
cd guides/10_reliability_and_operations/labs
python3 run_labs.py
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
run_labs - area 10 Reliability & operations (offline, deterministic)
==========================================================================
[PASS] lab_queue_headroom.py: [PASS] lab_queue_headroom self-test passed.
[PASS] lab_retry_storm.py: [PASS] lab_retry_storm self-test passed.
[PASS] lab_error_budget.py: [PASS] lab_error_budget self-test passed.
==========================================================================
[PASS] All 3/3 labs passed successfully.
```

Lab တိုင်းအတွက် `--self-test` ကို run ပြီး တစ်လိုင်း စီ ပြသည်။ အားလုံး အောင်မြင်ပါက
`[PASS] All 3/3 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်သည်။ `--self-test` သည်
lab တိုင်း သင်ပေးသည့် ဂုဏ်သတ္တိကို assert လုပ်သည်၊ အောင်မြင်သည့် အချက်တိုင်းကို
`[OK] ...` ဖြင့် ပြသည်။

## lab_queue_headroom.py - utilisation, queue wait နှင့် SLO headroom

Poisson arrivals နှင့် exponential service time ရှိသည့် deterministic queue simulation
တစ်ခု ဖြစ်သည်။ utilisation `rho = arrivals_per_s x service_s / workers` ကို တွက်ပြီး
p50/p95 queue စောင့်ချိန်၊ queue ပြည့်၍ ကျဆင်းသည့် request အရေအတွက်နှင့်
`--p95-target-ms` ကို ဖြည့်ဆည်းသည့် အမြင့်ဆုံး utilisation (SLO ceiling) ကို ပြသည်။

```bash
python3 lab_queue_headroom.py                                # arrivals 12/s, service 50 ms, 1 worker, seed 20240
python3 lab_queue_headroom.py --arrivals-per-s 15 --workers 2
python3 lab_queue_headroom.py --sweep                        # arrivals 2.00 .. 19.00/s
python3 lab_queue_headroom.py --self-test
python3 lab_queue_headroom.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_queue_headroom - utilisation, queue wait နှင့် SLO headroom (offline, deterministic)
arrivals=12.00/s  service=50.0 ms  workers=1  sim=20000 s  seed=20240  queue=200
utilisation (offered) = 0.6000   SLO target: p95 queue wait <= 500 ms
--------------------------------------------------------------------------
  admitted requests          :    240,025
  dropped (queue full)       :          0
  p50 queue wait             :      23.60 ms
  p95 queue wait             :     310.42 ms
  p95 / p50 ratio            :     13.15x
--------------------------------------------------------------------------
headroom search (arrivals sweep, same seed):
 arrivals/s    rho     p95 ms   verdict
      10.00   0.50     230.62     meets
      12.00   0.60     310.42     meets
      14.00   0.70     442.43     meets
      15.00   0.75     555.40    misses
      16.00   0.80     713.23    misses
      18.00   0.90    1460.03    misses
--------------------------------------------------------------------------
SLO ceiling: rho 0.70 (arrivals 14.00/s, p95 442.43 ms)
headroom at 12.00 req/s: rho 0.10 (14.3% of the ceiling)
workers needed for this demand: 1
--------------------------------------------------------------------------
မှတ်ချက် - queue စောင့်ချိန်၏ p95 သည် utilisation တိုးလာသည့်အခါ အစပိုင်းတွင် နှေးစွာ တိုးပြီး saturation နီးလျှင် ခုန်တက်သည်။ SLO အဆင့်ကို utilisation မဟုတ်ဘဲ queue ကိန်းဖြင့် သတ်မှတ်ရမည်။
==========================================================================
```

**ဖတ်နည်း** — utilisation 0.60 ဖြစ်ခြင်းသည် နှစ်သိမ့်စရာ အနေအထား ပေါ်နေခြင်းသာ ဖြစ်သည်၊
SLO ceiling သည် 0.70 ဖြစ်သဖြင့် ကျန်ရှိသည့် headroom သည် utilisation 0.10 (14.3%) သာ
ဖြစ်သည်။ p50 သည် 23.60 ms ဖြစ်သော်လည်း p95 သည် 310.42 ms (13.15x) ဖြစ်သည် —
ပျမ်းမျှဖြင့် ကြည့်လျှင် SLO ကို လျစ်လျူရှုမိသည်။

### Worker တစ်ခု ထပ်ထည့်ကြည့်ခြင်း — `--workers 2`

```
$ python3 lab_queue_headroom.py --arrivals-per-s 15 --workers 2
==========================================================================
lab_queue_headroom - utilisation, queue wait နှင့် SLO headroom (offline, deterministic)
arrivals=15.00/s  service=50.0 ms  workers=2  sim=20000 s  seed=20240  queue=200
utilisation (offered) = 0.3750   SLO target: p95 queue wait <= 500 ms
--------------------------------------------------------------------------
  admitted requests          :    299,974
  dropped (queue full)       :          0
  p50 queue wait             :       0.00 ms
  p95 queue wait             :      56.58 ms
  p95 / p50 ratio            : n/a (p50 is 0)
--------------------------------------------------------------------------
headroom search (arrivals sweep, same seed):
 arrivals/s    rho     p95 ms   verdict
      10.00   0.25      23.22     meets
      12.00   0.30      36.50     meets
      14.00   0.35      49.90     meets
      15.00   0.38      56.58     meets
      16.00   0.40      63.15     meets
      18.00   0.45      78.17     meets
--------------------------------------------------------------------------
SLO ceiling: rho 0.85 (arrivals 34.00/s, p95 452.90 ms)
headroom at 15.00 req/s: rho 0.47 (55.9% of the ceiling)
workers needed for this demand: 2
--------------------------------------------------------------------------
မှတ်ချက် - queue စောင့်ချိန်၏ p95 သည် utilisation တိုးလာသည့်အခါ အစပိုင်းတွင် နှေးစွာ တိုးပြီး saturation နီးလျှင် ခုန်တက်သည်။ SLO အဆင့်ကို utilisation မဟုတ်ဘဲ queue ကိန်းဖြင့် သတ်မှတ်ရမည်။
==========================================================================
```

**ဖတ်နည်း** — worker တစ်ခု ထပ်ထည့်လျှင် တူညီသည့် demand (15.00 req/s) တွင် p95 သည်
310 ms မှ 56.58 ms သို့ ကျဆင်းပြီး SLO ceiling သည် 0.85 သို့ တက်သည်။ သို့သော်
utilisation ကိန်း တစ်ခုတည်းဖြင့် နှိုင်းယှဉ်၍ မရပါ — worker ၂ ခုတွင် utilisation 0.3750 ဖြစ်သည်
(worker ၁ ခုတွင် 0.75 နှင့် တူညီသည့် demand)။

## lab_retry_storm.py - retry amplification, jitter နှင့် circuit breaker

layer တိုင်း၏ request ပမာဏကို `rps x failure_rate^(k-1)` ဖြင့် ခွဲပြီး amplification factor
ကို တွက်သည်။ `--jitter` သည် retry delay ကို `[delay x (1 - jitter), delay]` အတွင်း
ဖြန့်သည်၊ ထို့ကြောင့် peak ကို 10 ms bucket များဖြင့် တိုင်းနိုင်သည်။ retry budget နှင့်
circuit breaker ၏ ကန့်သတ်မှုကိုလည်း ပြသည်။

```bash
python3 lab_retry_storm.py                                   # rps 200, failure 0.50, retries 3, jitter 1.00
python3 lab_retry_storm.py --rps 400 --retries 5 --jitter 0.0
python3 lab_retry_storm.py --sweep                           # retries 0 .. 6
python3 lab_retry_storm.py --self-test
python3 lab_retry_storm.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_retry_storm - retry amplification နှင့် dependency load (offline, deterministic)
rps=200.0  failure-rate=0.50  retries=3  backoff=200 ms  jitter=1.00  seed=20240
--------------------------------------------------------------------------
 layer  requests/s  cumulative/s  backoff ms
     0      200.00        200.00           0
     1      100.00        300.00         200
     2       50.00        350.00         400
     3       25.00        375.00         800
--------------------------------------------------------------------------
amplification factor              :    1.875x
dependency load during failure    :   375.00 req/s (baseline 200.00, extra 175.00)
retry budget 10%                     :    1.100x -> 220.00 req/s
circuit breaker (open 1 s)        :    1.438x -> 287.50 req/s (closed fraction 0.500)
--------------------------------------------------------------------------
jitter effect on one 1.0 s failure wave (10 ms buckets):
  jitter   retries   buckets   peak req/s
    0.00       350         3     20000.00
    1.00       350        58      2200.00
--------------------------------------------------------------------------
မှတ်ချက် - retry သည် ဝန် ကို ဆတိုး တိုးစေသည်။ ချို့ယွင်းနေသည့် dependency သည် စွမ်းရည် အနည်းဆုံး ဖြစ်နေချိန်တွင် retry များ တစ်ချိန်တည်း ရောက်လျှင် ချို့ယွင်းမှု ပို၍ ကြာသည်။
==========================================================================
```

**ဖတ်နည်း** — amplification 1.875x သည် dependency အပေါ် ဝန် 87.5% ထပ်တိုးသည်။ jitter သည်
retry အရေအတွက် (350) ကို မပြောင်းလဲဘဲ peak ကို 20000.00 req/s မှ 2200.00 req/s သို့
လျှော့ချသည်၊ ဆိုလိုသည်မှာ jitter သည် ဝန် ပမာဏကို မလျှော့ချဘဲ အချိန် ဖြန့်ခြင်းဖြင့်
အမြင့်ဆုံး ခုန်တက်မှုကို ဖျက်သည်။ ဝန် ပမာဏကို လျှော့ချရန် retry budget (1.100x) နှင့်
circuit breaker (1.438x) လိုအပ်သည်။

### Retry လွှာ တိုးပြီး jitter ကို ပိတ်ကြည့်ခြင်း — `--retries 5 --jitter 0.0`

```
$ python3 lab_retry_storm.py --rps 400 --retries 5 --jitter 0.0
==========================================================================
lab_retry_storm - retry amplification နှင့် dependency load (offline, deterministic)
rps=400.0  failure-rate=0.50  retries=5  backoff=200 ms  jitter=0.00  seed=20240
--------------------------------------------------------------------------
 layer  requests/s  cumulative/s  backoff ms
     0      400.00        400.00           0
     1      200.00        600.00         200
     2      100.00        700.00         400
     3       50.00        750.00         800
     4       25.00        775.00        1600
     5       12.50        787.50        3200
--------------------------------------------------------------------------
amplification factor              :    1.969x
dependency load during failure    :   787.50 req/s (baseline 400.00, extra 387.50)
retry budget 10%                     :    1.100x -> 440.00 req/s
circuit breaker (open 1 s)        :    1.484x -> 593.75 req/s (closed fraction 0.500)
--------------------------------------------------------------------------
jitter effect on one 1.0 s failure wave (10 ms buckets):
  jitter   retries   buckets   peak req/s
    0.00       775         5     40000.00
--------------------------------------------------------------------------
မှတ်ချက် - retry သည် ဝန် ကို ဆတိုး တိုးစေသည်။ ချို့ယွင်းနေသည့် dependency သည် စွမ်းရည် အနည်းဆုံး ဖြစ်နေချိန်တွင် retry များ တစ်ချိန်တည်း ရောက်လျှင် ချို့ယွင်းမှု ပို၍ ကြာသည်။
==========================================================================
```

**ဖတ်နည်း** — retry လွှာ တိုးလျှင် amplification သည် 1.969x သို့ ရောက်ပြီး
`1/(1 - failure_rate) = 2.0` ကို ချဉ်းကပ်သည်။ jitter 0.0 တွင် retry 775 ခုလုံး bucket
5 ခုတွင်သာ ရှိသဖြင့် peak သည် 40000.00 req/s ဖြစ်သည်။

## lab_error_budget.py - error budget, burn rate နှင့် alert threshold

SLO မှ error budget ကို request အရေအတွက်နှင့် 100% ချို့ယွင်းမှု မိနစ်အဖြစ် ဆင်းသက်သည်။
ထို့နောက် လေ့လာတွေ့ရှိသည့် failure rate မှ burn rate၊ budget ကုန်ဆုံးသည့် အချိန်နှင့်
Google SRE ပုံစံ multiwindow alert threshold များကို ပြသည်။

```bash
python3 lab_error_budget.py                                  # slo 99.9%, 1,000,000 req/day, 30-day window
python3 lab_error_budget.py --slo-percent 99.9 --failure-rate 0.002
python3 lab_error_budget.py --sweep                          # slo 99.0 .. 99.99%
python3 lab_error_budget.py --self-test
python3 lab_error_budget.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_error_budget - error budget, burn rate နှင့် alert threshold (offline, deterministic)
slo=99.900%  requests/day=1,000,000  window=30 days  failure-rate=0.0500%
--------------------------------------------------------------------------
  total requests in window    :     30,000,000
  allowed failure ratio       :       0.001000
  error budget (requests)     :         30,000
  request rate                :          11.57 req/s
  error budget (minutes)      :          43.20 min at 100% failure
--------------------------------------------------------------------------
  observed failures in window :         15,000
  burn rate                   :         0.5000x
  time to exhaust the budget  :          60.00 days
--------------------------------------------------------------------------
alert thresholds (multiwindow, Google SRE style):
 burn rate    window  budget share   exhausts in
      14.4       1 h          2.0%       2.08 d
       6.0       6 h          5.0%       5.00 d
       1.0      72 h         10.0%      30.00 d
--------------------------------------------------------------------------
မှတ်ချက် - error budget သည် incident ဖြစ်ပေါ်စေရန် ခွဲတမ်း မဟုတ်ပါ။ ၎င်းသည် SLO မှ ဆင်းသက်လာသည့် ဆုံးဖြတ်ချက် နယ်နိမိတ် ဖြစ်သည်၊ ကျန်ရှိသည့် budget အတွင်း release လုပ်ဆောင်နိုင်ပြီး ကုန်ဆုံးလျှင် ပြောင်းလဲမှုကို ရပ်ရမည်။
==========================================================================
```

**ဖတ်နည်း** — budget 30,000 requests သည် သေးငယ်သည့် ကိန်း မဟုတ်သော်လည်း 100% ချို့ယွင်းမှု
43.20 မိနစ်နှင့် ညီမျှသည် — ဆိုလိုသည်မှာ 30 ရက်တာ window တွင် စုစုပေါင်း 43 မိနစ်ခန့် သာ
ချို့ယွင်းခွင့် ရှိသည်။ burn rate 0.5000x သည် လက်ရှိ အရှိန်တွင် budget သည် 60.00 ရက်
ခံမည်ကို ပြသည်၊ alert threshold များသည် ပို၍ မြန်သည့် burn အတွက် ဖြစ်သည်။

### Failure rate ကို တိုးကြည့်ခြင်း — `--failure-rate 0.002`

```
$ python3 lab_error_budget.py --slo-percent 99.9 --failure-rate 0.002
==========================================================================
lab_error_budget - error budget, burn rate နှင့် alert threshold (offline, deterministic)
slo=99.900%  requests/day=1,000,000  window=30 days  failure-rate=0.2000%
--------------------------------------------------------------------------
  total requests in window    :     30,000,000
  allowed failure ratio       :       0.001000
  error budget (requests)     :         30,000
  request rate                :          11.57 req/s
  error budget (minutes)      :          43.20 min at 100% failure
--------------------------------------------------------------------------
  observed failures in window :         60,000
  burn rate                   :         2.0000x
  time to exhaust the budget  :          15.00 days
--------------------------------------------------------------------------
alert thresholds (multiwindow, Google SRE style):
 burn rate    window  budget share   exhausts in
      14.4       1 h          2.0%       2.08 d
       6.0       6 h          5.0%       5.00 d
       1.0      72 h         10.0%      30.00 d
--------------------------------------------------------------------------
မှတ်ချက် - error budget သည် incident ဖြစ်ပေါ်စေရန် ခွဲတမ်း မဟုတ်ပါ။ ၎င်းသည် SLO မှ ဆင်းသက်လာသည့် ဆုံးဖြတ်ချက် နယ်နိမိတ် ဖြစ်သည်၊ ကျန်ရှိသည့် budget အတွင်း release လုပ်ဆောင်နိုင်ပြီး ကုန်ဆုံးလျှင် ပြောင်းလဲမှုကို ရပ်ရမည်။
==========================================================================
```

**ဖတ်နည်း** — failure rate 0.2000% သည် allowed failure ratio 0.001000 ၏ နှစ်ဆ ဖြစ်သဖြင့်
burn rate 2.0000x ဖြစ်ပြီး budget သည် 30 ရက်အစား 15.00 ရက်အတွင်း ကုန်ဆုံးသည်။
budget ကိုယ်တိုင် (30,000 requests / 43.20 min) မပြောင်းလဲပါ — ပြောင်းလဲသည့် အရာမှာ
လေ့လာတွေ့ရှိသည့် ချို့ယွင်းမှုနှင့် တိုင်းတာမှု window အတွင်း ပြီးစီးချိန် ဖြစ်သည်။

## မှတ်ချက်

- Output အားလုံးကို `python3 verify_guide.py --labs --verbose` ဖြင့် စစ်ဆေးနိုင်သည်။
- `--self-test` သည် တိကျသည့် ဂုဏ်သတ္တိများကို assert လုပ်သည် (utilisation တိုးလျှင် p95
  တိုးသည်၊ worker ထပ်ထည့်လျှင် p95 ကျသည်၊ p95 သည် p50 အောက် မရောက်သည်၊ saturation
  နီးလျှင် p95 သည် linear ထက် မြန်စွာ တိုးသည်၊ queue သေးလျှင် drop ဖြစ်သည်၊ SLO ceiling
  သည် 1.0 အောက် ဖြစ်သည်၊ amplification သည် closed-form နှင့် ကိုက်ညီသည်၊ retry လွှာ တိုးလျှင်
  ဝန် တိုးသည်၊ jitter သည် peak ကို လျှော့ချသည်၊ budget သည် (1 - SLO) နှင့် အတိအကျ ကိုက်ညီသည်၊
  burn rate နှင့် ကုန်ဆုံးချိန်သည် ဆက်စပ်သည်)။
- Flag တိုင်း၏ အဓိပ္ပာယ်ကို `python3 <lab> --help` ဖြင့် ကြည့်နိုင်သည်။
- ဤ lab သုံးခုသည် `../../scripts/capacity_headroom.py`၊ `../../scripts/retry_amplification.py`၊
  `../../scripts/failover_cost.py` တို့နှင့် ဆက်စပ်သည် — ထို script များသည် ဖော်မြူလာ
  တစ်ခုတည်းကို တစ်ကြိမ် တွက်ပြပြီး lab များသည် knob ဖြင့် ပြန်ပြောင်း စမ်းသပ်နိုင်သည်။
