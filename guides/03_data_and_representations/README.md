# Area 03 — Data & Representations: လေ့လာလမ်းညွှန် (Study Guide)

ဤ folder သည် `terms/03_data_and_representations.md` ရှိ term ၁၃ ခုကို **စာရင်း** အဖြစ်မှ **လေ့လာနိုင်သည့်
သင်ခန်းစာ** အဖြစ် တိုးချဲ့ထားသည်။ Glossary entry များသည် "ဤ term ဆိုသည်မှာ ဘာလဲ" ကို ဖြေသည်။
ဤလမ်းညွှန်သည် "ဤ term ကို မည်သည့် အစဉ်ဖြင့် လေ့လာမည်၊ ဘယ်လို အလုပ်လုပ်သည်၊ ဘယ်လောက်
ကုန်ကျသည်" ကို ဖြေသည်။

နယ်ပယ် ၀၂ (Models & inference) သည် **မော်ဒယ်** ကို ဗဟိုပြုသည်။ ဤနယ်ပယ် ၀၃ သည် **အချက်အလက်**
ကို ဗဟိုပြုသည်။ မော်ဒယ် တစ်ခု မတည်ဆောက်မီ အချက်အလက်သည် မည်သည့် အဆင့်များကို ဖြတ်သန်း
သည်၊ မည်သည့် ပုံစံဖြင့် ကိုယ်စားပြု (represent) လုပ်သည်၊ မည်သည့် နေရာတွင် ယိုစိမ့် (leak)
နိုင်သည်၊ ဘယ်လို ခြေရာခံ (lineage) မည် ဟူသည့် မေးခွန်းများကို ဤလမ်းညွှန်က လမ်းကြောင်း
တစ်ကြောင်းတည်း အဖြစ် ဖြေသည်။

## အခြေခံ အချက်

| အချက် | တန်ဖိုး |
|---|---|
| Term | ၁၃ ခု (area 03 — Data & representations) |
| ဖိုင် | document ၄ ခု + lab ၃ ခု + ကိန်းဂဏန်း script ၃ ခု |
| လိုအပ်သည့် အရာ | Python 3.11+၊ standard library သာ — network၊ GPU၊ API key မလိုပါ |
| Run တိုင်း | deterministic (ရလဒ် တူညီသည်)၊ offline |
| စစ်ဆေးခြင်း | `python3 verify_guide.py --guide 03 --documents --verbose` |

## လေ့လာသည့် အစဉ် (၅ ကြိမ်)

| ကြိမ် | ဖတ်ရမည့် ဖိုင် | လက်တွေ့ လုပ်ရမည့် အရာ |
|---|---|---|
| ၁ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၁–၂ | `python3 labs/lab_tokenizer.py` — `--merges` နှင့် `--vocab-target` ပြောင်း၍ token ခွဲမှုကို ကြည့်ခြင်း |
| ၂ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၁–၃ | ပုံများကို စာရွက်ပေါ် ပြန်ဆွဲခြင်း၊ `python3 scripts/ex_b_vocab_memory.py` |
| ၃ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၃ | `python3 labs/lab_pipeline_budget.py` — token၊ epoch၊ dataset GiB၊ ကုန်ကျစရိတ် |
| ၄ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၄ | `python3 labs/lab_split_leak.py` — `--leak-rate` ဖြင့် ယိုစိမ့်မှု တိုင်းတာခြင်း |
| ၅ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၅ | `python3 scripts/ex_c_dedup_epochs.py`၊ [`04_exercises.md`](04_exercises.md) ၏ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု |

**ကြိမ် တစ်ကြိမ်လျှင် ပမာဏ** — ကြိမ် တစ်ခုစီသည် အဆင့် တစ်ဆင့် သို့မဟုတ် နှစ်ဆင့်သာ ဖြစ်သည်။
ဤကြောင့် ဖတ်ခြင်းနှင့် လက်တွေ့ တွက်ချက်ခြင်းကို ခွဲထား၍ လုပ်နိုင်သည် — ဖတ်ပြီးသည့် အဆင့်၏
lab ကို ချက်ချင်း run ပါက term နှင့် ကိန်းဂဏန်း ချိတ်ဆက်မှု ရှင်းလာသည်။

## ဖိုင်များ

| ဖိုင် | ဘာကို ပေးသည် |
|---|---|
| [`01_learning_sequence.md`](01_learning_sequence.md) | term ၁၃ ခုကို အဆင့် ၅ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည် — ကြိုတင် သိရမည့် term၊ ဖွင့်ပေးသည့် အချက်၊ အဆင့်တိုင်း၏ စစ်ဆေးမေးခွန်း၊ prerequisite graph |
| [`02_visual_explanations.md`](02_visual_explanations.md) | Mermaid ပုံ ၈ ခု — စာသားမှ token သို့ (BPE merge)၊ vocabulary တည်ဆောက်ခြင်း၊ embedding lookup၊ split နှင့် leakage မြှား၊ source မှ training batch သို့ pipeline၊ versioning နှင့် lineage၊ annotation နှင့် label quality၊ token id မှ tensor သို့ |
| [`04_exercises.md`](04_exercises.md) | အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာ ၄ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ ဆုံးဖြတ်ချက် ၂ ခု၊ အဖြေများ အပြည့်အစုံ |
| [`labs/`](labs/) | interactive lab ၃ ခု (`lab_tokenizer.py`၊ `lab_split_leak.py`၊ `lab_pipeline_budget.py`) + `run_labs.py` |
| [`scripts/`](scripts/) | ၀၃ ဖိုင်ရှိ ကိန်းဂဏန်း ဥပမာ ၃ ခုကို ထုတ်ပေးသည့် script များ |

## Lab များ — ဘာကို ပြောင်း၍ ဘာကို ကြည့်မည်

Lab ဖိုင်များကို ဤနေရာတွင် path အလိုက် အမည်ပေးထားသည်။ ဖိုင် အမှန်တကယ် ရောက်ရှိလာသည့်
အခါ parameter များကို ပြောင်း၍ run နိုင်သည်၊ ထိုအခါ အောက်ပါ အချက်များကို ကြည့်ရမည်။

| Lab (path) | ပြောင်းနိုင်သည့် knob | ကြည့်ရမည့် ရလဒ် |
|---|---|---|
| `labs/lab_tokenizer.py` | `--merges`၊ `--vocab-target`၊ `--texts` | စာသား တစ်ကြောင်း၏ token အရေအတွက်၊ merge rule အစဉ်၊ encode-decode round trip |
| `labs/lab_pipeline_budget.py` | `--corpus-tokens`၊ `--epochs`၊ `--batch`၊ `--seq`၊ `--encode-cost` | epoch တိုင်း၏ token၊ step အရေအတွက်၊ dataset GiB၊ pipeline သည် accelerator ကို အပြည့် အလုပ်ပေးနိုင်မှု |
| `labs/lab_split_leak.py` | `--n`၊ `--val-fraction`၊ `--leak-rate`၊ `--seed` | leakage ဖြစ်သည့် test row အရေအတွက်၊ validation ရမှတ် မြင့်တက်မှု |
| `scripts/ex_b_vocab_memory.py`၊ `scripts/ex_c_dedup_epochs.py` | vocabulary အရွယ်အစား၊ d_model၊ dtype၊ dedup အချိုး | embedding matrix ၏ MiB၊ dedup ဖြင့် ထိရောက်သည့် epoch တိုးမှု |

Lab တိုင်းသည် **offline နှင့် deterministic** ဖြစ်မည် — parameter ပြောင်း၍ run ပါက အချိန်တိုင်း
တူညီသည့် ရလဒ် ရမည်၊ ထို့ကြောင့် [`04_exercises.md`](04_exercises.md) ရှိ မိမိ တွက်ချက်မှုနှင့်
တိုက်စစ်နိုင်သည်။

## စစ်ဆေးခြင်း

```bash
python3 verify_guide.py --guide 03 --documents --verbose
python3 verify_guide.py --guide 03 --labs
```

`--documents` သည် ဖိုင် ရှိမှု၊ အနည်းဆုံး character အရေအတွက်၊ register သန့်ရှင်းမှု၊ term ၁၃ ခု
လွှမ်းခြုံမှုနှင့် Mermaid ပုံ အနည်းဆုံး ၄ ခု ရှိမှုကို စစ်သည်။ `--labs` သည် lab တိုင်းကို
`--self-test` ဖြင့် ၃ ကြိမ် run ၍ output တူညီမှုကို စစ်သည်။

## မှီခိုသည့် အခြား ဖိုင်

- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) — [`../../terms/03_data_and_representations.md`](../../terms/03_data_and_representations.md)
- A–Z index — [`../../terms/00_index.md`](../../terms/00_index.md)
- ရှေ့ နယ်ပယ် (မော်ဒယ် ဗိသုကာ) — [`../02_models_and_inference/README.md`](../02_models_and_inference/README.md)
- ဆက်စပ် နယ်ပယ် — [`../04_retrieval_and_generation/README.md`](../04_retrieval_and_generation/README.md) (ဒေတာမှ ရှာဖွေခြင်းသို့ ဆက်သွားသည်)
