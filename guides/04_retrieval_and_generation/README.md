# Area 04 — Retrieval & Generation: လေ့လာလမ်းညွှန် (Study Guide)

ဤ folder သည် [`../../terms/04_retrieval_and_generation.md`](../../terms/04_retrieval_and_generation.md) ရှိ term **၁၄** ခုကို
**ကိုးကား စာရင်း** အဖြစ်မှ **လေ့လာနိုင်သည့် သင်ခန်းစာ** အဖြစ် တိုးချဲ့ထားသည်။ Glossary entry တစ်ခုသည်
"ဤ term ဆိုလိုသည်မှာ ဘာလဲ" ကို ဖြေသည်။ ဤလမ်းညွှန်သည် "ဤ term များကို မည်သည့် အစဉ်ဖြင့် လေ့လာမည်၊
retrieval pipeline တစ်ခုအတွင်း မည်သို့ ချိတ်ဆက်သည်၊ မည်သည့် ကိန်းဂဏန်းဖြင့် တိုင်းတာမည်" ကို ဖြေသည်။

ဤနယ်ပယ်သည် အစိတ်အပိုင်း တစ်ခုတည်း မဟုတ်ဘဲ **လုပ်ငန်းစဉ် တစ်ခု** ဖြစ်သည် — query ကို vector အဖြစ်
ကိုယ်စားပြုခြင်း၊ source material ကို ရှာဖွေနိုင်သည့် ယူနစ်များအဖြစ် ခွဲခြားခြင်း၊ index တည်ဆောက်၍
ခန့်မှန်း ရှာဖွေခြင်း၊ ရလဒ်များကို ပေါင်းစပ်၍ ပြန်စီခြင်း၊ ရလဒ် အရည်အသွေးကို တိုင်းတာခြင်း၊
နောက်ဆုံးတွင် ရွေးချယ်ထားသည့် အထောက်အထားကို generative model ထံ ပေးအပ်ခြင်း ဖြစ်သည်။

## အခြေခံ အချက်

| အချက် | တန်ဖိုး |
|---|---|
| Term | ၁၄ ခု (area 04 — Retrieval & generation) |
| ဖိုင် | လေ့လာဖိုင် ၄ ခု + lab ၃ ခု + ကိန်းဂဏန်း script ၃ ခု |
| လိုအပ်သည့် အရာ | Python 3.11+၊ standard library သာ — network၊ GPU၊ API key မလိုပါ |
| ကိန်းဂဏန်း | လေ့ကျင့်ခန်း တိုင်းကို script ဖြင့် တွက်၍ ရလဒ်ကို ဖိုင်ထဲ တိုက်ရိုက် ကူးထားသည် |
| စစ်ဆေးခြင်း | `python3 verify_guide.py --guide 04 --documents --verbose` |

## လေ့လာသည့် အစဉ် (၅ ကြိမ်)

| ကြိမ် | ဖတ်ရမည့် ဖိုင် | လက်တွေ့ လုပ်ရမည့် lab |
|---|---|---|
| ၁ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၁–၂ | `python3 labs/lab_chunking.py --tokens 12000 --chunk 400 --overlap 60` နှင့် `--sweep` |
| ၂ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၁–၃ | `python3 labs/lab_vector_index.py --chunks 4096 --dim 64 --dtype fp16` |
| ၃ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၃ | `python3 labs/lab_vector_index.py --probe 2` နှင့် `--probe 4` ကို နှိုင်းယှဉ်ခြင်း |
| ၄ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၄–၇ | `python3 labs/lab_vector_index.py --k 10 --queries 32` နှင့် `--k 3` |
| ၅ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၄–၅၊ [`04_exercises.md`](04_exercises.md) | `python3 labs/lab_prompt_budget.py --chunk 512 --k 6 --window 8192 --reserve 1024` |

Lab တိုင်းသည် **offline နှင့် deterministic** ဖြစ်သည် — parameter ပြောင်း၍ run ပါက အချိန်တိုင်း တူညီသည့်
ရလဒ် ရသည်၊ ထို့ကြောင့် မိမိ တွက်ချက်မှုနှင့် တိုက်စစ်နိုင်သည်။ Lab ဖိုင် သုံးခုကို `labs/run_labs.py` ဖြင့်
တစ်ပြိုင်နက် run နိုင်သည်၊ အသေးစိတ် run ပုံနှင့် output များကို `labs/README.md` တွင် ဖော်ပြထားသည်။
လက်တွေ့ စမ်းသပ်မှု အားလုံး Python standard library သာ သုံးသည်။

## ဖိုင်များ

| ဖိုင် | ဘာကို ပေးသည် |
|---|---|
| [`01_learning_sequence.md`](01_learning_sequence.md) | term ၁၄ ခုကို အဆင့် ၅ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည် — ကြိုတင် သိရမည့် term၊ ဖွင့်ပေးသည့် အချက်၊ အဆင့်တိုင်း၏ စစ်ဆေးမေးခွန်း၊ prerequisite graph |
| [`02_visual_explanations.md`](02_visual_explanations.md) | Mermaid ပုံ ၇ ခု — RAG တောင်းဆိုမှု လမ်းကြောင်း၊ chunking နှင့် overlap၊ embedding နှင့် index တည်ဆောက်ခြင်း၊ HNSW ရှာဖွေမှု၊ hybrid fusion၊ reranking၊ context ဘတ်ဂျက် |
| [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) | term ၁၄ ခုကို ထုတ်လုပ်မှု အခြေခံအဆောက်အအုံ အပေါ် သက်ရောက်မှု အလိုက် ချိတ်ဆက်သည် — term အလိုက် ရှင်းလင်းချက်၊ လက်တွေ့ တွက်ချက်မှု သုံးခု၊ ဆုံးဖြတ်ချက် ခြောက်ခု |
| [`04_exercises.md`](04_exercises.md) | လုပ်ပြထားသည့် ဥပမာ ၄ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ ဆုံးဖြတ်ချက် ၂ ခု — အဖြေ အပြည့်အစုံ |
| `labs/` | lab ၃ ခု (`lab_chunking.py`၊ `lab_vector_index.py`၊ `lab_prompt_budget.py`) + `labs/run_labs.py` — run ပုံနှင့် output များ `labs/README.md` တွင် |
| `scripts/` | `03_theory_to_infrastructure.md` ရှိ ကိန်းဂဏန်း ဥပမာများကို ထုတ်ပေးသည့် script ၃ ခု (`ex_a_index_memory.py`၊ `ex_b_latency_qps.py`၊ `ex_c_prompt_cost.py`) |

## Lab များ — ဘာကို ပြောင်း၍ ဘာကို ကြည့်မည်

| Lab | ပြောင်းနိုင်သည့် knob | ကြည့်ရမည့် ရလဒ် |
|---|---|---|
| `labs/lab_chunking.py` | `--tokens`၊ `--chunk`၊ `--overlap`၊ `--sweep` | chunk အရေအတွက်၊ overlap အချိုး၊ index ကုန်ကျစရိတ် |
| `labs/lab_vector_index.py` | `--chunks`၊ `--dim`၊ `--dtype`၊ `--k`၊ `--queries`၊ `--probe`၊ `--sweep` | fp16/fp32/int8 memory အချိုး၊ recall@k၊ layered search ၏ distance တွက်ချက်မှု |
| `labs/lab_prompt_budget.py` | `--chunk`၊ `--k`၊ `--window`၊ `--reserve`၊ `--sweep` | retrieved token၊ ကျန်သည့် နေရာ၊ history အတွက် နေရာ၊ query တစ်ခုလျှင် ကုန်ကျစရိတ် |

## စစ်ဆေးခြင်း

```bash
python3 verify_guide.py --guide 04 --documents --verbose   # ဖိုင်၊ register၊ term လွှမ်းခြုံမှု၊ Mermaid ပုံ
python3 verify_guide.py --guide 04 --labs --verbose        # lab များ ၃ ကြိမ် run ၍ deterministic ဖြစ်မှု
python3 labs/run_labs.py                                   # lab သုံးခုလုံး --self-test ဖြင့်
```

`--documents` သည် ဤ folder ၏ လေ့လာဖိုင် လေးခုကို စစ်သည် — ဖိုင် ရှိမှု၊ အရှည်၊ စကားပြော ပါတ်တစ်လ်လ် ကင်းမှု၊
အခြားဘာသာ အက္ခရာ နှင့် emoji ကင်းမှု၊ term ၁၄ ခုလုံး အစဉ်ဖိုင်တွင် ပါဝင်မှု၊ Mermaid ပုံ အနည်းဆုံး ၄ ခု။

## မှီခိုသည့် အခြား ဖိုင်

- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) — [`../../terms/04_retrieval_and_generation.md`](../../terms/04_retrieval_and_generation.md)
- A–Z index — [`../../terms/00_index.md`](../../terms/00_index.md)
- area 09 (Infrastructure & serving) သည် index နှင့် latency ကို ဆက်ဖတ်ရမည့် နယ်ပယ် ဖြစ်သည်
- area 05 (Prompting & context) သည် `Grounding` နှင့် context ဘတ်ဂျက် ကို ဆက်ဖတ်ရမည့် နယ်ပယ် ဖြစ်သည်
