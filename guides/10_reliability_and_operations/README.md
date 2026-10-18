# Area 10 — Reliability & Operations: လေ့လာလမ်းညွှန် (Study Guide)

ဤ folder သည် [`terms/10_reliability_and_operations.md`](../../terms/10_reliability_and_operations.md) ရှိ term ၁၇ ခုကို **စာရင်း** အဖြစ်မှ
**လေ့လာနိုင်သည့် သင်ခန်းစာ** အဖြစ် တိုးချဲ့ထားသည်။ Glossary entry များသည် "ဤ term ဆိုသည်မှာ ဘာလဲ" ဟူသည့် မေးခွန်းကို ဖြေသည်။
ဤလမ်းညွှန်သည် "ဤ term များသည် မည်သည့် အစဉ်ဖြင့် ဆက်စပ်သည်၊ ဝန်ပို တစ်ခုသည် မည်သည့် နေရာတွင် စတင် ပျက်စီးသည်၊
incident တစ်ခုသည် error budget မည်မျှ ကုန်သည်" ဟူသည့် မေးခွန်းများကို ဖြေသည်။

## ဤလမ်းညွှန် ထပ်တိုးပေးသည့် အချက်

Glossary သည် term တိုင်းကို သီးခြားစီ ရှင်းပြသည်။ ထုတ်လုပ်မှု စနစ် တစ်ခုတွင် ထို term များသည် သီးခြားစီ မလုပ်ဆောင်ပါ —
ဝန်ပို တစ်ခု ဖြစ်သည့်အခါ admission control၊ load shedding၊ backpressure၊ circuit breaker နှင့် degradation သည်
တစ်ချိန်တည်းတွင် အလုပ်လုပ်သည်။ ဤလမ်းညွှန်သည် ထို ဆက်စပ်မှုကို သုံးလမ်းဖြင့် ဖော်ပြသည်။

- **အစဉ် တည်ဆောက်ခြင်း** — term ၁၇ ခုကို အဆင့် ၅ ဆင့်အဖြစ် စီထားသည်။ မည်သည့် အရာ မှားနိုင်သည်၊ မည်သို့ တိုင်းတာမည် ဟူသည့်
  အဆင့်မှ စ၍ ဝန်ပို ကာကွယ်ခြင်း၊ လျှော့ချခြင်းနှင့် ပြန်လည် ရယူခြင်း၊ ပြောင်းလဲမှု လွှတ်ခြင်း၊ နောက်ဆုံးတွင် incident လည်ပတ်ခြင်းနှင့်
  သင်ယူခြင်း အထိ တည်ဆောက်သည်။
- **ပုံဖြင့် မြင်ခြင်း** — Mermaid ပုံ ၇ ခုဖြင့် request လမ်းကြောင်း၏ ချို့ယွင်းသည့် အမှတ်များ၊ queue ပေါ်ရှိ backpressure နှင့် load shedding၊
  circuit breaker အခြေအနေစက်၊ timeout နှင့် jitter ပါသည့် retry၊ degradation လှေကား၊ incident timeline နှင့် SLO error budget တို့ကို ပြသည်။
- **ကိန်းဂဏန်းဖြင့် ချိန်ခြင်း** — error budget၊ retry တိုးပွားမှု (amplification)၊ queueing latency၊ timeout budget၊
  ကုန်ကျစရိတ်နှင့် alert နှုန်းကို Python (standard library သာ) ဖြင့် တွက်ပြထားသည်။

ဤလမ်းညွှန်သည် deployment အတွက် မဖြစ်မနေ လိုအပ်သည့် **policy** များကို ဖော်ထုတ်ပေးသည် — မည်သည့် နယ်နိမိတ်တွင် shed မည်၊
error budget ကုန်သည့်အခါ မည်သည့် လုပ်ဆောင်ချက် ရပ်တန့်မည်၊ မည်သည့် အချိန်တွင် rollback လုပ်မည် ဖြစ်သည်။

## အခြေခံ အချက်

| အချက် | တန်ဖိုး |
|---|---|
| Term | ၁၇ ခု (area 10 — Reliability & operations) |
| အဆင့် | ၅ ဆင့် |
| ဖိုင် | ၅ ခု + lab ၃ ခု + ကိန်းဂဏန်း script |
| လိုအပ်သည့် အရာ | Python 3.11+၊ standard library သာ — network၊ GPU၊ API key မလိုပါ |
| Run တိုင်း | deterministic (ရလဒ် တူညီသည်)၊ offline |
| စစ်ဆေးခြင်း | `python3 verify_guide.py --guide 10 --documents --verbose` |

## လေ့လာသည့် အစဉ် (၅ ကြိမ်)

| ကြိမ် | ဖတ်ရမည့် ဖိုင် | လက်တွေ့ run ရမည့် lab |
|---|---|---|
| ၁ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၁–၂ | `python3 labs/lab_error_budget.py --slo-percent 99.9 --requests-per-day 1000000 --window-days 30 --failure-rate 0.0005` |
| ၂ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၁–၃ | `python3 labs/lab_queue_headroom.py --arrivals-per-s 12 --service-ms 50 --workers 1` |
| ၃ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၃ | `python3 labs/lab_queue_headroom.py --sweep --max-queue 200 --p95-target-ms 500` |
| ၄ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၄–၅၊ [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၄–၇ | `python3 labs/lab_retry_storm.py --retries 3 --failure-rate 0.5 --jitter 1.0 --retry-budget 0.10` |
| ၅ | [`04_exercises.md`](04_exercises.md) | `python3 labs/run_labs.py` |

Lab တိုင်းသည် **offline နှင့် deterministic** ဖြစ်သည် — parameter ပြောင်း၍ run ပါက အချိန်တိုင်း
တူညီသည့် ရလဒ် ရသည်၊ ထို့ကြောင့် မိမိ တွက်ချက်မှုနှင့် byte တူညီစွာ တိုက်စစ်နိုင်သည်။ Flag အားလုံး၏
အပြည့်အစုံ စာရင်းနှင့် run တိုင်း၏ output ကို [`labs/README.md`](labs/README.md) တွင် ကြည့်ပါ။

| Lab | ပြောင်းနိုင်သည့် knob | ကြည့်ရမည့် ရလဒ် |
|---|---|---|
| `lab_error_budget.py` | `--slo-percent`၊ `--requests-per-day`၊ `--window-days`၊ `--failure-rate`၊ `--sweep` | error budget (request နှင့် မိနစ်)၊ burn rate၊ ကုန်ဆုံးချိန်၊ alert threshold |
| `lab_queue_headroom.py` | `--arrivals-per-s`၊ `--service-ms`၊ `--workers`၊ `--max-queue`၊ `--p95-target-ms`၊ `--sweep` | utilisation တက်လာသည့်အခါ queue စောင့်ချိန် ကြီးထွားပုံ၊ SLO အတွက် လိုအပ်သည့် headroom |
| `lab_retry_storm.py` | `--rps`၊ `--failure-rate`၊ `--retries`၊ `--backoff-ms`၊ `--jitter`၊ `--retry-budget`၊ `--breaker-open-ms`၊ `--sweep` | amplification၊ dependency ပေါ် ထပ်တိုးသည့် ဝန်၊ jitter နှင့် circuit breaker ၏ အလျော့အကျ |

## ဖိုင်များ

| ဖိုင် | ဘာကို ပေးသည် |
|---|---|
| [`01_learning_sequence.md`](01_learning_sequence.md) | term ၁၇ ခုကို အဆင့် ၅ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည် — ကြိုတင် သိရမည့် term၊ ဖွင့်ပေးသည့် အချက်၊ အဆင့်တိုင်း၏ စစ်ဆေးမေးခွန်း၊ prerequisite graph |
| [`02_visual_explanations.md`](02_visual_explanations.md) | Mermaid ပုံ ၇ ခု — request လမ်းကြောင်းနှင့် ချို့ယွင်းသည့် အမှတ်၊ backpressure နှင့် load shedding၊ circuit breaker၊ timeout နှင့် retry၊ degradation လှေကား၊ incident timeline၊ SLO error budget |
| [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) | term တိုင်း၏ capacity၊ queueing၊ ကုန်ကျစရိတ်နှင့် on-call အပေါ် သက်ရောက်မှု + ကိန်းဂဏန်း ဥပမာများ (ပြိုင်တူ ရေးသားသည်) |
| [`04_exercises.md`](04_exercises.md) | လုပ်ပြထားသည့် ဥပမာ ၄ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ ဆုံးဖြတ်ချက် ၂ ခု၊ အဖြေများ အပြည့်အစုံ |
| [`labs/`](labs/) | interactive lab ၃ ခု + `run_labs.py` (usage နှင့် flag များ — [`labs/README.md`](labs/README.md)) |
| [`scripts/`](scripts/) | `03_theory_to_infrastructure.md` ၏ ကိန်းဂဏန်း ဥပမာများကို ထုတ်ပေးသည့် script များ |

## လေ့ကျင့်ခန်း တစ်ခုကို ဖတ်ပြီးနောက် ကိုယ်တိုင် စစ်ဆေးနည်း

တွက်ချက်ရသည့် လေ့ကျင့်ခန်း တိုင်းတွင် ဖော်မြူလာ၊ ယူဆချက် (assumption) နှင့် Python block တစ်ခု ပါဝင်သည်။
Block ကို ကိုယ်တိုင် run ၍ ဖော်ပြထားသည့် output နှင့် တိုက်စစ်ပါ — ကိန်းဂဏန်း တိုင်းသည်
**ရေးသားထားသည့် ယူဆချက်** အပေါ် မှီခိုသဖြင့် ယူဆချက် ပြောင်းပါက ရလဒ် ပြောင်းသည်။ ထို့ကြောင့် ဂဏန်း တိကျမှုထက်
**ပုံသဏ္ဍာန်** (ဥပမာ queueing latency သည် utilization 0.9 ကျော်သည့်အခါ မည်သို့ တက်သည်) ကို ကြည့်ရမည်။

## စစ်ဆေးခြင်း

```bash
python3 verify_guide.py --guide 10 --documents --verbose   # ဖိုင်၊ register၊ term လွှမ်းခြုံမှု၊ ပုံ အရေအတွက်
python3 verify_guide.py --guide 10 --labs --verbose        # lab ၃ ခု (+ ၃ ကြိမ် စီ) နှင့် run_labs.py
python3 guides/10_reliability_and_operations/labs/run_labs.py
```

`--documents` စစ်ဆေးချက်သည် [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) နှင့်
[`labs/`](labs/) ကိုပါ လွှမ်းခြုံသည်၊ ထို့ကြောင့် run မလုပ်မီ lab များနှင့် ပုံများ တည်ရှိရမည်။

## မှီခိုသည့် အခြား ဖိုင်

- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) — [`../../terms/10_reliability_and_operations.md`](../../terms/10_reliability_and_operations.md)
- အခြေခံ အချက်အလက် (JSON slice) — [`../../glossary/by_area/10_reliability_and_operations.json`](../../glossary/by_area/10_reliability_and_operations.json)
- A–Z index — [`../../terms/00_index.md`](../../terms/00_index.md)
- ဤနယ်ပယ်၏ အခြေခံ ဖြစ်သည့် serving အလွှာ — [`../09_infrastructure_and_serving/README.md`](../09_infrastructure_and_serving/README.md)
