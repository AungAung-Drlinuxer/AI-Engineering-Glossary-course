# Area 11 — Security & Governance: လေ့လာလမ်းညွှန် (Study Guide)

ဤ folder သည် [`terms/11_security_and_governance.md`](../../terms/11_security_and_governance.md) ရှိ term ၂၀ ခုကို **စာရင်း** အဖြစ်မှ
**လေ့လာနိုင်သည့် သင်ခန်းစာ** အဖြစ် တိုးချဲ့ထားသည်။ Glossary entry များသည် "ဤ term ဆိုသည်မှာ ဘာလဲ" ကို ဖြေသည်။
ဤလမ်းညွှန်သည် "ဤ term များကို မည်သည့် အစဉ်ဖြင့် ဆက်စပ်မည်၊ trust boundary တစ်ခုကို ဘယ်နေရာတွင် ဆွဲမည်၊
control တစ်ခုသည် ဘယ်လောက် လျော့ပေးသည်၊ မှတ်တမ်း တစ်ခုသည် ဘယ်လောက် ကုန်ကျသည်" ကို ဖြေသည်။

## ဤလမ်းညွှန် ထပ်တိုးပေးသည့် အချက်

Glossary သည် term တိုင်းကို သီးခြားစီ ရှင်းပြသည်။ လုံခြုံရေးနှင့် အုပ်ချုပ်မှု တွင် term တိုင်း သီးခြားစီ
မလုပ်ဆောင်ပါ — ၎င်းတို့သည် **စနစ် တစ်ခုတည်း၏ ကာကွယ်မှု အလွှာများ** ဖြစ်သည်။ ဤလမ်းညွှန်သည် ထို ဆက်စပ်မှုကို
သုံးလမ်းဖြင့် ဖော်ပြသည်။

- **အစဉ် တည်ဆောက်ခြင်း** — term ၂၀ ခုကို အဆင့် ၅ ဆင့်အဖြစ် စီထားသည်။ မည်သည့်အရာကို ကာကွယ်သည်၊ မည်သူကို
  ဆန့်ကျင်သည် (Threat Model၊ AI Risk Assessment၊ Trust Boundary၊ Data Classification) မှ စ၍ မည်သူက ဘာလုပ်နိုင်သည်
  (Zero Trust၊ Separation of Duties၊ Defense in Depth၊ Data Exfiltration)၊ data ကိုယ်တိုင် ကာကွယ်ခြင်း
  (Data Minimization၊ Purpose Limitation၊ Data Lineage၊ Datasheet for Datasets)၊ ဖြစ်ပွားခဲ့သည့် အရာ သက်သေပြခြင်း
  (Audit Log၊ Content Provenance၊ Provenance Attestation၊ Software Bill of Materials (SBOM))၊ နောက်ဆုံးတွင်
  စမ်းသပ်ခြင်းနှင့် အုပ်ချုပ်မှု (Indirect Prompt Injection၊ Jailbreak၊ Membership Inference၊ Red Teaming) အထိ တည်ဆောက်သည်။
- **ပုံဖြင့် မြင်ခြင်း** — Mermaid ပုံ ၇ ခုဖြင့် LLM application တစ်ခု၏ trust boundary၊ agent tool များ၏ least privilege၊
  key နှင့် secret ကိုင်တွယ်သည့် လမ်းကြောင်း၊ prompt အတွင်း sensitive data နှင့် redaction လမ်းကြောင်း၊
  request မှ audit record အထိ သက်သေ လမ်းကြောင်း၊ human approval gate ပါသည့် policy ဆုံးဖြတ်ချက် လမ်းကြောင်း၊
  vulnerability နှင့် exfiltration လမ်းကြောင်းတို့ကို ပြသည်။
- **ကိန်းဂဏန်းဖြင့် ချိန်ခြင်း** — risk score၊ expected annual loss၊ control ၏ ကုန်ကျစရိတ်နှင့် သက်သာမှု၊
  key rotation window နှင့် exposure time၊ audit log ပမာဏနှင့် retention ကုန်ကျစရိတ်၊ over-permissioned tool တစ်ခု၏
  blast radius တို့ကို Python (standard library သာ) ဖြင့် တွက်ပြထားသည်။

ဤလမ်းညွှန်သည် deployment အတွက် မဖြစ်မနေ လိုအပ်သည့် **policy** များကို ဖော်ထုတ်ပေးသည် — မည်သည့် data ကို
မည်သည့် class ဟု သတ်မှတ်သည်၊ မည်သည့် tool သည် မည်သည့် destination သို့ ရေးနိုင်သည်၊ မည်သည့် လုပ်ဆောင်ချက်အတွက်
လူ၏ approval လိုသည်၊ မည်သည့် ဖြစ်ရပ်ကို audit log တွင် မှတ်တမ်းတင်သည်၊ မည်သည့် အချိန်တွင် key ကို rotate လုပ်သည် ဖြစ်သည်။

## အခြေခံ အချက်

| အချက် | တန်ဖိုး |
|---|---|
| Term | ၂၀ ခု (area 11 — Security & governance) |
| အဆင့် | ၅ ဆင့် |
| ဖိုင် | document ဖိုင် ၆ ခု + lab ၃ ခု + ကိန်းဂဏန်း script ၃ ခု |
| လိုအပ်သည့် အရာ | Python 3.11+၊ standard library သာ — network၊ GPU၊ API key မလိုပါ |
| Run တိုင်း | deterministic (ရလဒ် တူညီသည်)၊ offline |
| စစ်ဆေးခြင်း | `python3 verify_guide.py --guide 11 --documents --verbose` |

## လေ့လာသည့် အစဉ် (၅ ကြိမ်)

| ကြိမ် | ဖတ်ရမည့် ဖိုင် | လက်တွေ့ run ရမည့် lab |
|---|---|---|
| ၁ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၁–၂ | `python3 labs/lab_blast_radius.py --sweep` |
| ၂ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၁–၃ | `python3 labs/lab_redaction_path.py --pattern-count 40 --false-positive-rate 0.005` |
| ၃ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၃ | `python3 labs/lab_audit_volume.py --retention-days 90 --sampling-rate 0.25` |
| ၄ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၄–၅ | `python3 labs/lab_blast_radius.py --tools 20 --over-permission 0.3 --likelihood 0.4` |
| ၅ | [`04_exercises.md`](04_exercises.md) | `python3 labs/lab_audit_volume.py --bytes-per-record 2400 --retention-days 730` + တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု |

Lab အားလုံးကို တစ်ကြိမ်တည်း စစ်ဆေးလိုပါက `python3 labs/run_labs.py` ကို run ရမည်။

## ဖိုင်များ

| ဖိုင် | ဘာကို ပေးသည် |
|---|---|
| [`01_learning_sequence.md`](01_learning_sequence.md) | term ၂၀ ခုကို အဆင့် ၅ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည် — ကြိုတင် သိရမည့် term၊ ဖွင့်ပေးသည့် အချက်၊ အဆင့်တိုင်း၏ စစ်ဆေးမေးခွန်း၊ prerequisite graph |
| [`02_visual_explanations.md`](02_visual_explanations.md) | Mermaid ပုံ ၇ ခု — trust boundary၊ tool least privilege၊ key နှင့် secret လမ်းကြောင်း၊ prompt အတွင်း sensitive data နှင့် redaction၊ audit trail၊ policy ဆုံးဖြတ်ချက်နှင့် approval gate၊ exfiltration လမ်းကြောင်း |
| [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) | term တိုင်း runtime၊ ကုန်ကျစရိတ်နှင့် operation အပေါ် သက်ရောက်မှု + ကိန်းဂဏန်း ဥပမာများ (`labs/` နှင့် `scripts/` ကို အသုံးပြုသည်) |
| [`04_exercises.md`](04_exercises.md) | လုပ်ပြထားသည့် ဥပမာ ၄ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ ဆုံးဖြတ်ချက် ၂ ခု၊ အဖြေများ အပြည့်အစုံ |
| [`labs/`](labs/) | interactive lab ၃ ခု + `run_labs.py` (usage၊ flag နှင့် ရလဒ်များ — [`labs/README.md`](labs/README.md)) |
| [`scripts/`](scripts/) | `03_theory_to_infrastructure.md` ၏ ကိန်းဂဏန်း ဥပမာများကို ထုတ်ပေးသည့် script ၃ ခု — `ex_a_guardrail_cost.py`၊ `ex_b_audit_volume.py`၊ `ex_c_control_roi.py` |

`03_theory_to_infrastructure.md`၊ `labs/README.md` နှင့် `scripts/` တို့ကို ဤလမ်းညွှန်နှင့် တွဲဖက်၍
အလုပ်လုပ်သည့် ဖိုင်များအဖြစ် ရေးသားထားသည်။ ထို ဖိုင်များ၏ lab အမည်၊ flag နှင့် script အမည်များ၏
အပြည့်အစုံ စာရင်းကို [`labs/README.md`](labs/README.md) နှင့် [`scripts/`](scripts/) တွင် ဖတ်ရမည်။

## Lab များ — ဘာကို ပြောင်း၍ ဘာကို ကြည့်မည်

Lab တိုင်းသည် **offline နှင့် deterministic** ဖြစ်သည် — parameter ပြောင်း၍ run ပါက အချိန်တိုင်း
တူညီသည့် ရလဒ် ရသည်၊ ထို့ကြောင့် မိမိ တွက်ချက်မှုနှင့် တိုက်စစ်နိုင်သည်။

| Lab (path) | ပြောင်းနိုင်သည့် flag | ကြည့်ရမည့် ရလဒ် |
|---|---|---|
| `labs/lab_blast_radius.py` | `--tools`၊ `--data-scopes`၊ `--over-permission`၊ `--likelihood`၊ `--impact`၊ `--sweep` | as-configured နှင့် least-privilege reachable scope (tool-scope pair)၊ scope လျော့မှု၊ risk နှစ်မျိုးနှင့် control မှ ရရှိသည့် risk reduction |
| `labs/lab_redaction_path.py` | `--requests-per-s`၊ `--check-ms`၊ `--workers`၊ `--pattern-count`၊ `--false-positive-rate`၊ `--base-ms`၊ `--usd-per-false-redaction`၊ `--sweep` | ထည့်လိုက်သည့် p50 နှင့် p95 latency၊ throughput ceiling၊ ceiling လျော့မှု၊ false positive ကြောင့် မှားယွင်းစွာ ပိတ်ဆို့ခံရသည့် request နှင့် ကုန်ကျစရိတ် |
| `labs/lab_audit_volume.py` | `--requests-per-day`၊ `--bytes-per-record`၊ `--retention-days`၊ `--storage-cost-per-gb-month`၊ `--records-per-request`၊ `--sampling-rate`၊ `--sweep` | records per day၊ volume per day၊ retention သိုလှောင်မှု၊ monthly cost နှင့် sampling ဖြင့် သက်သာသည့် ပမာဏ |

တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခုနှင့် ဆုံးဖြတ်ချက် ၂ ခု၏ ကိန်းဂဏန်းများကို lab တစ်ခုတည်းအပေါ် မမှီခိုဘဲ
[`04_exercises.md`](04_exercises.md) အတွင်း Python (standard library သာ) ဖြင့် ပြန်လည် ထုတ်ပေးထားသည်။

## စစ်ဆေးခြင်း

```bash
python3 verify_guide.py --guide 11 --documents --verbose   # ဖိုင်၊ register၊ term လွှမ်းခြုံမှု၊ ပုံ အရေအတွက်
python3 verify_guide.py --guide 11 --labs --verbose        # lab ၄ ခု (+ ၃ ကြိမ် စီ) နှင့် run_labs.py
python3 guides/11_security_and_governance/labs/run_labs.py
```

`--documents` စစ်ဆေးချက်သည် [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) နှင့်
[`labs/`](labs/) ကိုပါ လွှမ်းခြုံသည်၊ ထို့ကြောင့် run မလုပ်မီ ထို ဖိုင်များ တည်ရှိရမည်။
[`04_exercises.md`](04_exercises.md) အတွင်း ကူးထားသည့် Python run တိုင်းကို ပြန် run ပါက
တူညီသည့် output ကို ရရှိမည်။

## မှီခိုသည့် အခြား ဖိုင်

- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) — [`../../terms/11_security_and_governance.md`](../../terms/11_security_and_governance.md)
- အခြေခံ အချက်အလက် (JSON slice) — [`../../glossary/by_area/11_security_and_governance.json`](../../glossary/by_area/11_security_and_governance.json)
- A–Z index — [`../../terms/00_index.md`](../../terms/00_index.md)
- မော်ဒယ်၊ inference နှင့် serving အခြေခံ — [`../02_models_and_inference/README.md`](../02_models_and_inference/README.md)
- agent loop၊ tool contract နှင့် approval gate အခြေခံ — [`../06_agents_and_tools/README.md`](../06_agents_and_tools/README.md)
