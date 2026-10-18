# Labs - Area 04: Retrieval & Generation

ဤ lab suite သည် လေ့လာနယ်ပယ် 04 ၏ term များ (Vector Database, HNSW, Approximate Nearest
Neighbor (ANN), Dense Retrieval, Chunking, Recall@K, Reranker, RAG) ကို လက်တွေ့ တွက်ကြည့်ရန်
ဖြစ်သည်။ Python standard library သာ အသုံးပြုသည်၊ network နှင့် GPU မလိုအပ်ပါ၊ run တိုင်း
ရလဒ် တူညီသည် (deterministic)။

## Run the whole suite (မဖြစ်မနေ)

```bash
cd guides/04_retrieval_and_generation/labs
python3 run_labs.py
```
Lab တိုင်းအတွက် `--self-test` ကို run ပြီး တစ်လိုင်း စီ ပြသည်။ အားလုံး အောင်မြင်ပါက
`[PASS] All 3/3 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်သည်။

```
==========================================================================
run_labs - area 04 Retrieval & generation (offline, deterministic)
==========================================================================
[PASS] lab_vector_index.py: [PASS] lab_vector_index self-test passed.
[PASS] lab_chunking.py: [PASS] lab_chunking self-test passed.
[PASS] lab_prompt_budget.py: [PASS] lab_prompt_budget self-test passed.
==========================================================================
[PASS] All 3/3 labs passed successfully.
```

## lab_vector_index.py - index memory၊ recall@k၊ layered search အလုပ်ပမာဏ

group တစ်ခုလျှင် vector ၁၆ ခု ပါဝင်သည့် toy embedding set တစ်ခုကို seed ဖြင့် deterministic
ဖန်တီးသည်။ Index memory ကို fp32၊ fp16၊ int8 တို့အတွက် ပြပြီး၊ exact scan နှင့် coarse-to-fine
layered search တို့၏ distance တွက်ချက်မှု အရေအတွက်၊ work ratio နှင့် recall@k ကို နှိုင်းယှဉ်သည်။

```bash
python3 lab_vector_index.py                              # default: chunks 4096, dim 64, k 10, seed 7
python3 lab_vector_index.py --chunks 8192 --dim 128 --dtype int8 --k 10 --queries 16 --seed 11
python3 lab_vector_index.py --sweep                       # chunks 1024 .. 8192
python3 lab_vector_index.py --self-test
python3 lab_vector_index.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_vector_index - index memory, recall@k, layered-search work (offline, deterministic)
chunks=4096  dim=64  dtype=fp16  k=10  queries=32  seed=7  group=16  noise=1.1  probe=2
--------------------------------------------------------------------------
index memory (chunks=4,096, dim=64):
  dtype    bytes/vector      bytes         MiB
  fp32               256  1,048,576      1.0000
  fp16               128    524,288      0.5000
  int8                64    262,144      0.2500
--------------------------------------------------------------------------
exact scan vs layered search (per query, k=10, probe=2 of 256 groups):
  distance computations exact    :        4,096
  distance computations layered  :          288   (7.03% of the collection)
  work ratio exact / layered     :        14.22x
  modelled latency exact         :       0.0437 ms
  modelled latency layered       :       0.0031 ms
  latency ratio                  :        14.22x
  mean recall@10                 :       0.8750
  worst / best query recall@10   :       0.5000 / 1.0000
--------------------------------------------------------------------------
မှတ်ချက် - index memory သည် chunk အရေအတွက်၊ dimension နှင့် byte အကျယ်အပေါ် တိုက်ရိုက် အချိုးကျသည်။
layered search သည် distance တွက်ချက်မှုကို လျှော့ချ၍ latency ကျဆင်းစေသော်လည်း recall@k သည် 1 အောက်တွင် ရှိနေသည်။
==========================================================================
```

Knob ပြောင်းထားသည့် run (`--chunks 8192 --dim 128 --dtype int8 --seed 11`) ၏ output -
```bash
python3 lab_vector_index.py --chunks 8192 --dim 128 --dtype int8 --k 10 --queries 16 --seed 11
```
(index memory သည် chunk အရေအတွက်နှင့် dimension အလိုက် linear တိုးသည်၊ int8 သည် fp16 ၏ တစ်ဝက်
ဖြစ်သည်။)
```
==========================================================================
lab_vector_index - index memory, recall@k, layered-search work (offline, deterministic)
chunks=8192  dim=128  dtype=int8  k=10  queries=16  seed=11  group=16  noise=1.1  probe=2
--------------------------------------------------------------------------
index memory (chunks=8,192, dim=128):
  dtype    bytes/vector      bytes         MiB
  fp32               512  4,194,304      4.0000
  fp16               256  2,097,152      2.0000
  int8               128  1,048,576      1.0000
--------------------------------------------------------------------------
exact scan vs layered search (per query, k=10, probe=2 of 512 groups):
  distance computations exact    :        8,192
  distance computations layered  :          544   (6.64% of the collection)
  work ratio exact / layered     :        15.06x
  modelled latency exact         :       0.1748 ms
  modelled latency layered       :       0.0116 ms
  latency ratio                  :        15.06x
  mean recall@10                 :       1.0000
  worst / best query recall@10   :       1.0000 / 1.0000
--------------------------------------------------------------------------
မှတ်ချက် - index memory သည် chunk အရေအတွက်၊ dimension နှင့် byte အကျယ်အပေါ် တိုက်ရိုက် အချိုးကျသည်။
layered search သည် distance တွက်ချက်မှုကို လျှော့ချ၍ latency ကျဆင်းစေသော်လည်း recall@k သည် 1 အောက်တွင် ရှိနေသည်။
==========================================================================
```

## lab_chunking.py - chunk အရေအတွက်၊ နယ်နိမိတ်နှင့် index ကုန်ကျစရိတ်

token 6000 ခုရှိသည့် source တစ်ခုကို chunk အရွယ်အစားနှင့် overlap အမျိုးမျိုးဖြင့် ခွဲကြည့်သည်။
chunk အရေအတွက်၊ စာကြောင်း ဖြတ်ခံရမှု အရေအတွက်၊ ထပ်နေသည့် token အရေအတွက်နှင့် index memory
ကို ပြသည်။

```bash
python3 lab_chunking.py                                  # default: tokens 6000, chunk 256, overlap 32
python3 lab_chunking.py --tokens 8000 --chunk 512 --overlap 128
python3 lab_chunking.py --sweep                          # chunk size sweep နှင့် overlap sweep
python3 lab_chunking.py --self-test
python3 lab_chunking.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_chunking - chunk count, boundaries, index cost (offline, deterministic)
tokens=6,000  chunk=256  overlap=32  stride=224  sentence=12 tokens (assumption)
--------------------------------------------------------------------------
  chunk count                   :           27
  chunk boundaries              :           26
  boundaries cutting a sentence :           18  (69.2%)
  duplicated (overlap) tokens   :          912
  index cost (fp16, dim 768)    :       0.0396 MiB
  index MiB per 1000 source tok  :       0.0066
--------------------------------------------------------------------------
chunk size settings at overlap=32 (fp16, dim 768 = 1536 B/vector):
   chunk   stride    chunks   duplicated   cut sent     index MiB   MiB/1k tok
      64       32       187        5,968        124        0.2739      0.0457
     128       96        63        2,064          0        0.0923      0.0154
     256      224        27          912         18        0.0396      0.0066
     512      480        13          656          0        0.0190      0.0032
    1024      992         7        1,168          4        0.0103      0.0017
    2048     2016         3          144          0        0.0044      0.0007
--------------------------------------------------------------------------
မှတ်ချက် - chunk ကြီးလျှင် အရေအတွက် နည်း၍ index ချွေတာသည်၊ သို့သော် ရှာဖွေမှု တိကျမှု ကျဆင်းနိုင်သည်။
overlap တိုးလျှင် နယ်နိမိတ်တွင် ဖြတ်ခံရသည့် စာကြောင်း လျော့သော်လည်း chunk အရေအတွက်နှင့် index ကုန်ကျစရိတ် တိုးသည်။
==========================================================================
```

Knob ပြောင်းထားသည့် run (`--tokens 8000 --chunk 512 --overlap 128`) ၏ output -
```bash
python3 lab_chunking.py --tokens 8000 --chunk 512 --overlap 128
```
(chunk ကြီးလျှင် အရေအတွက်နှင့် index ကုန်ကျစရိတ် ကျဆင်းသည်၊ overlap တိုးလျှင် ထပ်နေသည့်
token အရေအတွက် တိုးသည်။)
```
==========================================================================
lab_chunking - chunk count, boundaries, index cost (offline, deterministic)
tokens=8,000  chunk=512  overlap=128  stride=384  sentence=12 tokens (assumption)
--------------------------------------------------------------------------
  chunk count                   :           21
  chunk boundaries              :           20
  boundaries cutting a sentence :            0  (0.0%)
  duplicated (overlap) tokens   :        2,752
  index cost (fp16, dim 768)    :       0.0308 MiB
  index MiB per 1000 source tok  :       0.0038
--------------------------------------------------------------------------
chunk size settings at overlap=128 (fp16, dim 768 = 1536 B/vector):
   chunk   stride    chunks   duplicated   cut sent     index MiB   MiB/1k tok
     256      128        62        7,872         41        0.0908      0.0114
     512      384        21        2,752          0        0.0308      0.0038
    1024      896         9        1,216          6        0.0132      0.0016
    2048     1920         5        2,240          0        0.0073      0.0009
--------------------------------------------------------------------------
မှတ်ချက် - chunk ကြီးလျှင် အရေအတွက် နည်း၍ index ချွေတာသည်၊ သို့သော် ရှာဖွေမှု တိကျမှု ကျဆင်းနိုင်သည်။
overlap တိုးလျှင် နယ်နိမိတ်တွင် ဖြတ်ခံရသည့် စာကြောင်း လျော့သော်လည်း chunk အရေအတွက်နှင့် index ကုန်ကျစရိတ် တိုးသည်။
==========================================================================
```

## lab_prompt_budget.py - retrieved token၊ history နေရာ၊ overflow နှင့် ကုန်ကျစရိတ်

context window တစ်ခုအတွင်း retrieved chunk token များက မည်သည့် နေရာ ယူသည်ကို တွက်သည်။
history အတွက် ကျန်နေရာ (headroom) သို့မဟုတ် လွန်ကျွံမှု (overflow) နှင့် query တစ်ခုစီ၏
input ကုန်ကျစရိတ်ကို ပြသည်။

```bash
python3 lab_prompt_budget.py                             # default: chunk 400, k 5, window 32000, reserve 4096
python3 lab_prompt_budget.py --chunk 800 --k 10 --window 9000 --reserve 2048
python3 lab_prompt_budget.py --sweep                     # k 1 .. 40
python3 lab_prompt_budget.py --self-test
python3 lab_prompt_budget.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_prompt_budget - retrieved tokens, history room, cost (offline, deterministic)
chunk=400  k=5  window=32,000  reserve=4,096  system=400  question=60 (assumptions)
--------------------------------------------------------------------------
  retrieved tokens              :        2,000
  prompt tokens                 :        2,460
  reserved for the answer       :        4,096
  room left for history         :       25,444
  status                        : FITS headroom 25,444 tokens
  input cost per query (USD)    :     0.004920
  input cost per 1000 queries   :       4.9200
  total per 1000 queries        :       7.3200
--------------------------------------------------------------------------
effect of k at chunk=400 (window=32,000, reserve=4,096):
    k   retrieved   prompt tok   room for history   USD/1k input
    1         400          860             27,044         1.7200
    2         800        1,260             26,644         2.5200
    5       2,000        2,460             25,444         4.9200
   10       4,000        4,460             23,444         8.9200
   20       8,000        8,460             19,444        16.9200
--------------------------------------------------------------------------
မှတ်ချက် - k တိုးလျှင် ရရှိသည့် အထောက်အထား တိုးသော်လည်း prompt token၊ ကုန်ကျစရိတ် နှင့် history အတွက် ကျန်နေရာ လျော့သည်။
==========================================================================
```

Knob ပြောင်းထားသည့် run (`--chunk 800 --k 10 --window 9000 --reserve 2048`) ၏ output -
```bash
python3 lab_prompt_budget.py --chunk 800 --k 10 --window 9000 --reserve 2048
```
(window ကျဉ်းလျှင် k ကြီးသည့် အခါ retrieved context သည် history အတွက် ကျန်နေရာကို
လွန်ကျွံစေသည်။)
```
==========================================================================
lab_prompt_budget - retrieved tokens, history room, cost (offline, deterministic)
chunk=800  k=10  window=9,000  reserve=2,048  system=400  question=60 (assumptions)
--------------------------------------------------------------------------
  retrieved tokens              :        8,000
  prompt tokens                 :        8,460
  reserved for the answer       :        2,048
  room left for history         :       -1,508
  status                        : OVERFLOW 1,508 tokens
  input cost per query (USD)    :     0.016920
  input cost per 1000 queries   :      16.9200
  total per 1000 queries        :      19.3200
--------------------------------------------------------------------------
effect of k at chunk=800 (window=9,000, reserve=2,048):
    k   retrieved   prompt tok   room for history   USD/1k input
    1         800        1,260              5,692         2.5200
    2       1,600        2,060              4,892         4.1200
    5       4,000        4,460              2,492         8.9200
   10       8,000        8,460             -1,508        16.9200
   20      16,000       16,460             -9,508        32.9200
--------------------------------------------------------------------------
မှတ်ချက် - k တိုးလျှင် ရရှိသည့် အထောက်အထား တိုးသော်လည်း prompt token၊ ကုန်ကျစရိတ် နှင့် history အတွက် ကျန်နေရာ လျော့သည်။
==========================================================================
```

## မှတ်ချက်

- Output အားလုံးကို `python3 verify_guide.py --guide 04 --labs --verbose` ဖြင့် စစ်ဆေးနိုင်သည်။
- `--self-test` သည် တိကျသည့် ဂုဏ်သတ္တိများကို assert လုပ်သည် (fp32 သည် fp16 ၏ နှစ်ဆ ဖြစ်ပြီး
  int8 သည် တစ်ဝက်၊ index memory သည် chunk နှင့် dimension အပေါ် linear၊ layered search သည်
  distance တွက်ချက်မှု လျော့၍ scan လုပ်သည်၊ recall@k သည် [0, 1] အတွင်း တည်ရှိသည်၊ probe တိုးလျှင်
  recall@k မကျဆင်း၊ chunk ကြီးလျှင် အရေအတွက် နည်း၊ overlap တိုးလျှင် chunk တိုး၊ retrieved
  token သည် chunk × k ဖြစ်၊ k တိုးလျှင် history နေရာ သည် chunk အရေအတွက်အတိုင်း လျော့သည်)။
- Flag တိုင်း၏ အဓိပ္ပာယ်ကို `python3 <lab> --help` ဖြင့် ကြည့်နိုင်သည်။
