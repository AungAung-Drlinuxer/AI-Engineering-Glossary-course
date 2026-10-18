# Labs - Area 11: Security & Governance

ဤ lab suite သည် area 11 ၏ term များ (Guardrail နှင့် redaction cost, Audit Log volume,
Trust Boundary နှင့် blast radius) ကို လက်တွေ့ တွက်ကြည့်ရန် ဖြစ်သည်။ Python standard
library သာ အသုံးပြုသည်၊ network မလိုအပ်ပါ၊ run တိုင်း ရလဒ် တူညီသည် (deterministic)။
rate၊ စျေးနှုန်း နှင့် likelihood အားလုံးသည် assumption ဖြစ်သည်။

## Run the whole suite (မဖြစ်မနေ)

```bash
cd guides/11_security_and_governance/labs
python3 run_labs.py
```

Lab တိုင်းအတွက် `--self-test` ကို run ပြီး တစ်လိုင်း စီ ပြသည်။ အားလုံး အောင်မြင်ပါက
`[PASS] All 3/3 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်သည်။

```
==========================================================================
run_labs - area 11 Security & Governance (offline, deterministic)
==========================================================================
[PASS] lab_redaction_path.py: [PASS] lab_redaction_path self-test passed.
[PASS] lab_audit_volume.py: [PASS] lab_audit_volume self-test passed.
[PASS] lab_blast_radius.py: [PASS] lab_blast_radius self-test passed.
==========================================================================
[PASS] All 3/3 labs passed successfully.
```

## lab_redaction_path.py - redaction စစ်ဆေးမှု၏ latency နှင့် throughput ကုန်ကျစရိတ်

Request path တွင် redaction စစ်ဆေးမှု ထည့်လျှင် တိုးလာသည့် p50 နှင့် p95 latency၊
throughput ceiling၊ ceiling ဆုံးရှုံးမှု၊ utilisation၊ false positive ကြောင့်
မှားယွင်းစွာ ပိတ်ဆို့ခံရသည့် request အရေအတွက်နှင့် ၎င်းတို့၏ ကုန်ကျစရိတ်ကို ပြသည်။

```bash
python3 lab_redaction_path.py                          # default: 50 req/s, check 35 ms, 8 workers, 12 patterns
python3 lab_redaction_path.py --check-ms 140 --workers 16 --pattern-count 40
python3 lab_redaction_path.py --pattern-count 40 --false-positive-rate 0.005
python3 lab_redaction_path.py --sweep                  # check_ms 0..140
python3 lab_redaction_path.py --self-test
python3 lab_redaction_path.py --help
```

Default run ၏ အမှန်တကယ် output -
```
======================================================================================================
lab_redaction_path - request path တွင် redaction စစ်ဆေးမှု၏ latency နှင့် throughput ကုန်ကျစရိတ်
requests_per_s=50  check_ms=35  workers=8  pattern_count=12  false_positive_rate=0.0005
(assumption) ms_per_pattern=0.15  p95_factor=1.8  base_ms=90  usd_per_false_redaction=0.35
------------------------------------------------------------------------------------------------------
total redaction check latency   :          36.80 ms per request
added p50 latency               :          36.80 ms
added p95 latency               :          66.24 ms
throughput ceiling with check   :           63.1 req/s
throughput ceiling without check:           88.9 req/s
ceiling lost to the check       :           29.0 %
utilisation of the ceiling      :          0.792
requests falsely redacted / day :        2,160.0
cost of false redactions / day  :         756.00 USD
cost of false redactions / month:      22,680.00 USD
------------------------------------------------------------------------------------------------------
မှတ်ချက် - redaction စစ်ဆေးမှု တိုင်းသည် request တိုင်း၏ လမ်းကြောင်းတွင် latency ထည့်သည်၊ pattern တိုးလျှင် latency linear တိုးသည်၊ false positive သည် အသုံးပြုသူကို မှားယွင်းစွာ ပိတ်ဆို့သည်။
======================================================================================================
```

Knob ပြောင်းထားသည့် run (`--check-ms 140 --workers 16 --pattern-count 40`) ၏ output -
```
======================================================================================================
lab_redaction_path - request path တွင် redaction စစ်ဆေးမှု၏ latency နှင့် throughput ကုန်ကျစရိတ်
requests_per_s=50  check_ms=140  workers=16  pattern_count=40  false_positive_rate=0.0005
(assumption) ms_per_pattern=0.15  p95_factor=1.8  base_ms=90  usd_per_false_redaction=0.35
------------------------------------------------------------------------------------------------------
total redaction check latency   :         146.00 ms per request
added p50 latency               :         146.00 ms
added p95 latency               :         262.80 ms
throughput ceiling with check   :           67.8 req/s
throughput ceiling without check:          177.8 req/s
ceiling lost to the check       :           61.9 %
utilisation of the ceiling      :          0.737
requests falsely redacted / day :        2,160.0
cost of false redactions / day  :         756.00 USD
cost of false redactions / month:      22,680.00 USD
------------------------------------------------------------------------------------------------------
မှတ်ချက် - redaction စစ်ဆေးမှု တိုင်းသည် request တိုင်း၏ လမ်းကြောင်းတွင် latency ထည့်သည်၊ pattern တိုးလျှင် latency linear တိုးသည်၊ false positive သည် အသုံးပြုသူကို မှားယွင်းစွာ ပိတ်ဆို့သည်။
======================================================================================================
```

## lab_audit_volume.py - audit log ပမာဏ၊ သိုလှောင်မှု နှင့် ကုန်ကျစရိတ်

Records per day၊ volume per day၊ retention သိုလှောင်မှု၊ monthly cost နှင့်
sampling rate ပြောင်းလျှင် သိုလှောင်မှု နှင့် ကုန်ကျစရိတ် မည်သို့ ပြောင်းသည်ကို ပြသည်။

```bash
python3 lab_audit_volume.py                            # default: 2000000 req/day, 1200 B/record, 365 days, 0.023 USD/GB-month
python3 lab_audit_volume.py --retention-days 90 --sampling-rate 0.25 --requests-per-day 5000000
python3 lab_audit_volume.py --bytes-per-record 2400 --retention-days 730
python3 lab_audit_volume.py --sweep                    # retention 30..730 days
python3 lab_audit_volume.py --self-test
python3 lab_audit_volume.py --help
```

Default run ၏ အမှန်တကယ် output -
```
======================================================================================================
lab_audit_volume - audit log ပမာဏ၊ သိုလှောင်မှု နှင့် ကုန်ကျစရိတ်
requests_per_day=2,000,000  bytes_per_record=1200  retention_days=365  storage_cost_per_gb_month=0.023
(assumption) records_per_request=3  sampling_rate=0.1  retention basis=steady state, 1 GB = 10^9 bytes
------------------------------------------------------------------------------------------------------
records per day               :      6,000,000
volume per day                :           7.20 GB/day
storage at 100% retention     :       2,628.00 GB
storage at 10% sampling      :         262.80 GB
monthly cost at 100% retention:          60.44 USD
monthly cost at 10% sampling :           6.04 USD
saving from sampling          :          54.40 USD/month
records dropped per day       :      5,400,000
------------------------------------------------------------------------------------------------------
မှတ်ချက် - retention window နှင့် sampling rate သည် သိုလှောင်မှုကို ဆုံးဖြတ်သည်၊ sampling လုပ်လျှင် မှတ်တမ်း ပြည့်စုံမှု ဆုံးရှုံးသည်၊ ထို့ကြောင့် မည်သည့် event ကို sampling မလုပ်ရမည်ကို ရေးမှတ်ထားရမည်။
======================================================================================================
```

Knob ပြောင်းထားသည့် run (`--retention-days 90 --sampling-rate 0.25 --requests-per-day 5000000`) ၏ output -
```
======================================================================================================
lab_audit_volume - audit log ပမာဏ၊ သိုလှောင်မှု နှင့် ကုန်ကျစရိတ်
requests_per_day=5,000,000  bytes_per_record=1200  retention_days=90  storage_cost_per_gb_month=0.023
(assumption) records_per_request=3  sampling_rate=0.25  retention basis=steady state, 1 GB = 10^9 bytes
------------------------------------------------------------------------------------------------------
records per day               :     15,000,000
volume per day                :          18.00 GB/day
storage at 100% retention     :       1,620.00 GB
storage at 25% sampling      :         405.00 GB
monthly cost at 100% retention:          37.26 USD
monthly cost at 25% sampling :           9.31 USD
saving from sampling          :          27.95 USD/month
records dropped per day       :     11,250,000
------------------------------------------------------------------------------------------------------
မှတ်ချက် - retention window နှင့် sampling rate သည် သိုလှောင်မှုကို ဆုံးဖြတ်သည်၊ sampling လုပ်လျှင် မှတ်တမ်း ပြည့်စုံမှု ဆုံးရှုံးသည်၊ ထို့ကြောင့် မည်သည့် event ကို sampling မလုပ်ရမည်ကို ရေးမှတ်ထားရမည်။
======================================================================================================
```

## lab_blast_radius.py - as-configured နှင့် least-privilege reachable scope

As-configured နှင့် least-privilege tool-scope reach၊ scope reduction၊ risk
နှစ်မျိုးနှင့် ထိန်းချုပ်မှုမှ ရရှိသည့် risk reduction ကို ပြသည်။

```bash
python3 lab_blast_radius.py                            # default: 12 tools, 9 scopes, over-permission 0.55
python3 lab_blast_radius.py --tools 20 --over-permission 0.3 --likelihood 0.4
python3 lab_blast_radius.py --tools 40 --data-scopes 15 --over-permission 0.7
python3 lab_blast_radius.py --sweep                    # over_permission 0.0..0.9
python3 lab_blast_radius.py --self-test
python3 lab_blast_radius.py --help
```

Default run ၏ အမှန်တကယ် output -
```
======================================================================================================
lab_blast_radius - as-configured နှင့် least-privilege reachable scope
tools=12  data_scopes=9  over_permission=0.55  likelihood=0.25  impact_usd=400,000
(assumption) likelihood and impact are stated assumptions; scope units are tool-scope pairs
------------------------------------------------------------------------------------------------------
as-configured reachable scope   :            108 tool-scope pairs
least-privilege reachable scope :             48 tool-scope pairs
scope reduction                 :             60 pairs (55.6%)
risk as configured              :  10,800,000.00 USD/year
risk under least privilege      :   4,800,000.00 USD/year
risk reduction from the control :   6,000,000.00 USD/year
residual risk after the control :   4,800,000.00 USD/year
------------------------------------------------------------------------------------------------------
မှတ်ချက် - agent တစ်ခုသည် လိုအပ်သည်ထက် ကျယ်သည့် scope ရှိလျှင် ခိုးယူခံရသော အခြေအနေတွင် ထိခိုက်နိုင်သည့် ပမာဏ ကြီးသည်၊ least privilege သည် scope ကို ကျဉ်းစေပြီး ခွင့်ပြုချက် တောင်းခံမှုကို မှတ်တမ်းတင်ရမည်။
======================================================================================================
```

Knob ပြောင်းထားသည့် run (`--tools 20 --over-permission 0.3 --likelihood 0.4`) ၏ output -
```
======================================================================================================
lab_blast_radius - as-configured နှင့် least-privilege reachable scope
tools=20  data_scopes=9  over_permission=0.3  likelihood=0.4  impact_usd=400,000
(assumption) likelihood and impact are stated assumptions; scope units are tool-scope pairs
------------------------------------------------------------------------------------------------------
as-configured reachable scope   :            180 tool-scope pairs
least-privilege reachable scope :            120 tool-scope pairs
scope reduction                 :             60 pairs (33.3%)
risk as configured              :  28,800,000.00 USD/year
risk under least privilege      :  19,200,000.00 USD/year
risk reduction from the control :   9,600,000.00 USD/year
residual risk after the control :  19,200,000.00 USD/year
------------------------------------------------------------------------------------------------------
မှတ်ချက် - agent တစ်ခုသည် လိုအပ်သည်ထက် ကျယ်သည့် scope ရှိလျှင် ခိုးယူခံရသော အခြေအနေတွင် ထိခိုက်နိုင်သည့် ပမာဏ ကြီးသည်၊ least privilege သည် scope ကို ကျဉ်းစေပြီး ခွင့်ပြုချက် တောင်းခံမှုကို မှတ်တမ်းတင်ရမည်။
======================================================================================================
```

## မှတ်ချက်

- Output အားလုံးကို `python3 verify_guide.py --labs --verbose` ဖြင့် စစ်ဆေးနိုင်သည်။
- `--self-test` သည် တိကျသည့် ဂုဏ်သတ္တိများကို assert လုပ်သည် (p95 သည် p50 အောက်
  မနိမ့်ခြင်း၊ pattern တိုးလျှင် latency linear တိုးခြင်း၊ check time တိုးလျှင် ceiling
  ကျဆင်းခြင်း၊ false redaction သည် request rate အပေါ် linear မှီခိုခြင်း၊ retention
  နှစ်ဆ ဖြစ်လျှင် storage နှစ်ဆ ဖြစ်ခြင်း၊ sampling သည် storage ကို rate အတိုင်း
  လျှော့ခြင်း၊ over-permission မြင့်လျှင် least-privilege scope ကျဉ်းခြင်း၊ risk သည်
  likelihood အပေါ် linear မှီခိုခြင်း)။
- Flag တိုင်း၏ အဓိပ္ပာယ်ကို `python3 <lab> --help` ဖြင့် ကြည့်နိုင်သည်။
- ဤ lab များသည် မည်သည့် credential၊ key သို့မဟုတ် token တန်ဖိုးကိုမျှ
  အသုံးမပြုပါ၊ placeholder များ လည်း မလိုအပ်ပါ။
