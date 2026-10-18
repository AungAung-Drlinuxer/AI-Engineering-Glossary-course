# Area 09 — Infrastructure & serving: လေ့လာလမ်းညွှန် (Study Guide)

ဤ folder သည် [`terms/09_infrastructure_and_serving.md`](../../terms/09_infrastructure_and_serving.md) ရှိ
term ၁၈ ခုကို **စာရင်း** အဖြစ်မှ **လေ့လာနိုင်သည့် သင်ခန်းစာ** အဖြစ် တိုးချဲ့ထားသည်။ Glossary entry များသည်
"ဤ term ဆိုသည်မှာ ဘာလဲ" ကို ဖြေသည်။ ဤလမ်းညွှန်သည် "ဤ term များကို မည်သည့် အစဉ်ဖြင့် ဆက်စပ်မည်၊
request တစ်ခုသည် မည်သည့် အဆင့်များမှ ဖြတ်၍ ဘယ်လောက် ကုန်ကျသည်၊ deployment တစ်ခုကောင်း/ဆိုးကို
မည်သည့် metric ဖြင့် ဆုံးဖြတ်မည်" ကို ဖြေသည်။

## ဤလမ်းညွှန် ထပ်တိုးပေးသည့် အချက်

- **အစဉ် တည်ဆောက်ခြင်း** — term ၁၈ ခုကို အဆင့် ၅ ဆင့်အဖြစ် စီထားသည်။ serving ဆိုသည်မှာ ဘာလဲ နှင့်
  request တစ်ခု၏ ကုန်ကျစရိတ်မှ စ၍ accelerator ပေါ်တွင် အလုပ် စီစဉ်ခြင်း၊ memory layout နှင့်
  ပြန်လည် အသုံးပြုခြင်း၊ မော်ဒယ်ကို device များအကြား ဖြန့်ကျက်ခြင်း၊ နောက်ဆုံးတွင်
  တိုင်းတာခြင်းနှင့် scale လုပ်ခြင်း အထိ တည်ဆောက်သည်။
- **ပုံဖြင့် မြင်ခြင်း** — Mermaid ပုံ ၉ ခုဖြင့် request လမ်းကြောင်း၊ batching timeline နှစ်မျိုး၊
  prefill နှင့် decode ၏ KV cache အပေါ် မှီခိုမှု၊ paged KV cache block layout၊ chunked prefill ၏
  ရောနှောမှု၊ tensor နှင့် pipeline parallelism layout၊ disaggregated pool များ၊ queue signal ဖြင့်
  autoscaling နှင့် rollout ကို ခွင့်ပြုသည့် metric gate များကို ပြသည်။
- **ကိန်းဂဏန်းဖြင့် ချိန်ခြင်း** — weight နှင့် KV cache memory budget၊ roofline tokens/s နှင့်
  cost per million tokens၊ batch နှင့် inter-token latency၊ replica အရေအတွက်နှင့် queue ကြီးထွားမှုတို့ကို
  Python (standard library သာ) ဖြင့် တွက်ပြထားသည်။

ဤလမ်းညွှန်သည် deployment အတွက် မဖြစ်မနေ လိုအပ်သည့် **စည်းမျဉ်း** များကို ဖော်ထုတ်ပေးသည် —
admission control၊ chunk policy၊ block အရွယ်အစား၊ sharding layout၊ latency SLO နှင့်
autoscaling signal ဖြစ်သည်။

## အခြေခံ အချက်

| အချက် | တန်ဖိုး |
|---|---|
| Term | ၁၈ ခု (area 09 — Infrastructure & serving) |
| အဆင့် | ၅ ဆင့် |
| ဖိုင် | ၅ ခု + lab ၃ ခု + ကိန်းဂဏန်း script ၃ ခု |
| လိုအပ်သည့် အရာ | Python 3.11+၊ standard library သာ — network၊ GPU၊ API key မလိုပါ |
| Run တိုင်း | deterministic (ရလဒ် တူညီသည်)၊ offline |
| စစ်ဆေးခြင်း | `python3 verify_guide.py --guide 09 --verbose` |

## လေ့လာသည့် အစဉ် (၅ ကြိမ်)

| ကြိမ် | ဖတ်ရမည့် ဖိုင် | လက်တွေ့ run ရမည့် lab |
|---|---|---|
| ၁ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၁ | `python3 labs/lab_serving_memory.py --params-b 8 --context 8192 --batch 32` |
| ၂ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၂ | `python3 labs/lab_roofline.py --sweep` |
| ၃ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၃ | `python3 labs/lab_serving_memory.py --context 32768 --dtype int8 --batch 8` |
| ၄ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၄ | `python3 labs/lab_roofline.py --params-b 70 --dtype int4 --batch 64` |
| ၅ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၅ နှင့် [`04_exercises.md`](04_exercises.md) | `python3 labs/lab_autoscale.py --rps 40 --output-tokens 300 --replicas 3` |

Lab အားလုံးကို တစ်ကြိမ်တည်း စစ်ဆေးလိုပါက `python3 labs/run_labs.py` ကို run ရမည်။
အဆင့် တိုင်းတွင် စစ်ဆေးသည့် မေးခွန်း တစ်ခု ပါဝင်သည် — ထို မေးခွန်းကို ဖြေနိုင်မှသာ နောက်အဆင့်သို့
တက်ရမည်။

## ဖိုင်များ

| ဖိုင် | ဘာကို ပေးသည် |
|---|---|
| [`01_learning_sequence.md`](01_learning_sequence.md) | term ၁၈ ခုကို အဆင့် ၅ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည် — ကြိုတင် သိရမည့် term၊ ဖွင့်ပေးသည့် အချက်၊ အဆင့်တိုင်း၏ စစ်ဆေးမေးခွန်း၊ prerequisite graph |
| [`02_visual_explanations.md`](02_visual_explanations.md) | Mermaid ပုံ ၉ ခု — serving လမ်းကြောင်း၊ static နှင့် continuous batching timeline၊ prefill နှင့် decode၊ paged KV cache block၊ chunked prefill၊ parallelism layout သုံးမျိုး၊ disaggregated pool၊ autoscaling signal၊ rollout metric gate |
| [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) | term တိုင်း GPU memory / compute / latency / throughput / ကုန်ကျစရိတ် / ထုတ်လုပ်မှု အပေါ် သက်ရောက်မှု + တွက်ချက်မှု ဥပမာ ၃ ခု |
| [`04_exercises.md`](04_exercises.md) | လုပ်ပြထားသည့် ဥပမာ ၄ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ ဆုံးဖြတ်ချက် ၂ ခု၊ အဖြေများ အပြည့်အစုံ |
| [`labs/`](labs/) | interactive lab ၃ ခု + `run_labs.py` (usage နှင့် ရလဒ်များ — [`labs/README.md`](labs/README.md)) |
| [`scripts/`](scripts/) | `03_theory_to_infrastructure.md` ၏ ကိန်းဂဏန်း ဥပမာများကို ထုတ်ပေးသည့် script ၃ ခု — `ex_a_memory_budget.py`၊ `ex_b_roofline.py`၊ `ex_c_replicas.py` |

## Lab များ — ဘာကို ပြောင်း၍ ဘာကို ကြည့်မည်

Lab တိုင်းသည် **offline နှင့် deterministic** ဖြစ်သည် — parameter ပြောင်း၍ run ပါက အချိန်တိုင်း
တူညီသည့် ရလဒ် ရသည်၊ ထို့ကြောင့် မိမိ တွက်ချက်မှုနှင့် တိုက်စစ်နိုင်သည်။

| Lab | ပြောင်းနိုင်သည့် knob | ကြည့်ရမည့် ရလဒ် |
|---|---|---|
| `lab_serving_memory.py` | `--params-b`၊ `--layers`၊ `--heads`၊ `--head-dim`၊ `--context`၊ `--batch`၊ `--dtype`၊ `--budget-gib`၊ `--sweep` | weight GiB၊ KV cache per sequence နှင့် total၊ activation workspace၊ total VRAM၊ budget အောက်တွင် တင်နိုင်သည့် အကြီးဆုံး batch |
| `lab_roofline.py` | `--bandwidth-gbps`၊ `--params-b`၊ `--dtype`၊ `--batch`၊ `--efficiency`၊ `--gpu-hour-cost`၊ `--sweep` | တစ်လှမ်းလျှင် byte၊ tokens/s အပေါ်ဘောင် နှင့် ရရှိသည့် တန်ဖိုး၊ step ကြာချိန်၊ cost per million tokens |
| `lab_autoscale.py` | `--rps`၊ `--output-tokens`၊ `--replica-tps`၊ `--replicas`၊ `--target-utilisation`၊ `--cold-start-s`၊ `--gpu-hour-cost`၊ `--sweep` | utilisation၊ queue ကြီးထွားနှုန်း၊ လိုအပ်သည့် replica၊ scale-up ကြာချိန်၊ over- နှင့် under-provisioning ကုန်ကျစရိတ် |

lab suite တစ်ခုလုံး၏ အခြေအနေ (`python3 labs/run_labs.py` ၏ ရလဒ်) —

```text
==========================================================================
run_labs - area 09 Infrastructure & Serving (offline, deterministic)
==========================================================================
[PASS] lab_serving_memory.py: [PASS] lab_serving_memory self-test passed.
[PASS] lab_roofline.py: [PASS] lab_roofline self-test passed.
[PASS] lab_autoscale.py: [PASS] lab_autoscale self-test passed.
==========================================================================
[PASS] All 3/3 labs passed successfully.
```

**သတိထားရန်** — bandwidth၊ efficiency၊ GPU-hour စျေးနှုန်းနှင့် activation factor အားလုံးသည်
ဖော်ပြထားသည့် ယူဆချက် (assumption) ဖြစ်သည်၊ benchmark တိုင်းတာမှု မဟုတ်ပါ။ accelerator၊
vendor နှင့် region အလိုက် ကွာခြားသည်၊ ထို့ကြောင့် တန်ဖိုးများကို "ဤ ယူဆချက်အောက်တွင်"
ဟု တွဲဖတ်ရမည်။

## စစ်ဆေးခြင်း

```bash
python3 verify_guide.py --guide 09 --verbose          # ဖိုင်၊ register၊ term လွှမ်းခြုံမှု၊ lab ၃ ခု (၃ ကြိမ် စီ)
python3 verify_guide.py --guide 09 --documents        # document ဖိုင်များသာ
python3 verify_guide.py --guide 09 --labs             # lab များသာ
python3 guides/09_infrastructure_and_serving/labs/run_labs.py
```

## မှီခိုသည့် အခြား ဖိုင်

- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) — [`../../terms/09_infrastructure_and_serving.md`](../../terms/09_infrastructure_and_serving.md)
- A–Z index — [`../../terms/00_index.md`](../../terms/00_index.md)
- area 02 (Models & Inference) သည် ဤနေရာမှ ဆက်ဖတ်ရမည့် နယ်ပယ် ဖြစ်သည် — [`../02_models_and_inference/README.md`](../02_models_and_inference/README.md)
