# Labs - Area 03: Data & Representations

ဤ lab suite သည် area 03 ၏ term များ (Tokenization, Token, Vocabulary, Byte Pair Encoding,
Embedding, Tensor, Dataset Split, Data Leakage, Data Deduplication, Data Provenance)
ကို လက်တွေ့ တွက်ကြည့်ရန် ဖြစ်သည်။ Python standard library သာ အသုံးပြုသည်၊ network နှင့်
GPU မလိုအပ်ပါ၊ run တိုင်း ရလဒ် တူညီသည် (deterministic)။

## Run the whole suite (မဖြစ်မနေ)

```bash
cd guides/03_data_and_representations/labs
python3 run_labs.py
```

Lab တိုင်းအတွက် `--self-test` ကို run ပြီး တစ်လိုင်း စီ ပြသည်။ အားလုံး အောင်မြင်ပါက
`[PASS] All 3/3 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်သည်။

```
==========================================================================
run_labs - area 03 Data & representations (offline, deterministic)
==========================================================================
[PASS] lab_tokenizer.py: [PASS] lab_tokenizer self-test passed.
[PASS] lab_split_leak.py: [PASS] lab_split_leak self-test passed.
[PASS] lab_pipeline_budget.py: [PASS] lab_pipeline_budget self-test passed.
==========================================================================
[PASS] All 3/3 labs passed successfully.
```

## lab_tokenizer.py - BPE-style merge trainer

မြန်မာ၊ အင်္ဂလိပ် နှင့် code စာသား သုံးခုပါသည့် ပုံသေ corpus ပေါ်တွင် character-level
BPE merge များကို သင်ယူသည်။ Merge sequence၊ vocabulary အရွယ်အစား နှင့် စာသားတိုင်း
မည်သို့ ခွဲခြမ်းခြင်း ကို ပြသည်။ `--vocab-target` ဖြင့် သတ်မှတ်သည့် အရွယ်အစားတွင်
merge ရပ်သည်၊ `--texts` ဖြင့် ခွဲခြမ်းပြသည့် စာသားများကို ရွေးသည်။

```bash
python3 lab_tokenizer.py                              # default: merges 10, vocab-target 0, all texts
python3 lab_tokenizer.py --merges 20 --vocab-target 72
python3 lab_tokenizer.py --texts english
python3 lab_tokenizer.py --sweep                      # merges 0 .. 20
python3 lab_tokenizer.py --self-test
python3 lab_tokenizer.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_tokenizer - BPE-style merge trainer (offline, deterministic)
corpus: burmese 136 chars / english 86 chars / code 31 chars / total 253
merges=10  vocab-target=0  base symbols=60  final vocab=70
--------------------------------------------------------------------------
  idx  merged pair                 count   vocab
    1  ် +                           7      61
    2  t + o                         5      62
    3    + s                         4      63
    4  e + n                         4      64
    5  k + en                        4      65
    6  to + ken                      4      66
    7  သ + ည                         4      67
    8    +                           3      68
    9    + b                         3      69
   10    + မ                         3      70
--------------------------------------------------------------------------
 text      chars  tokens  bytes/token  merge depth
 burmese     136     110         2.96            7
 english      86      76         1.13            6
 code         31      27         1.15            2
--------------------------------------------------------------------------
segmentation (10 merges):
 burmese   အ ခ ျ က ် အ လ က ်  က ိ ု   token  မ ျ ာ း ... (+92 more)
 english   t h e   token i z e r  s p l i t s   t e ... (+58 more)
 code      d e f   a d d ( a ,  b ) : \n       r e ... (+9 more)
==========================================================================
```

Knob-changed run (`--merges`၊ `--vocab-target` နှင့် `--texts` ပြောင်းသည်) -
```bash
python3 lab_tokenizer.py --merges 18 --texts burmese,code --vocab-target 66
```

Output -
```
==========================================================================
lab_tokenizer - BPE-style merge trainer (offline, deterministic)
corpus: burmese 136 chars / english 86 chars / code 31 chars / total 253
merges=18  vocab-target=66  base symbols=60  final vocab=66
--------------------------------------------------------------------------
  idx  merged pair                 count   vocab
    1  ် +                           7      61
    2  t + o                         5      62
    3    + s                         4      63
    4  e + n                         4      64
    5  k + en                        4      65
    6  to + ken                      4      66
--------------------------------------------------------------------------
 text      chars  tokens  bytes/token  merge depth
 burmese     136     117         2.79            5
 code         31      31         1.00            0
--------------------------------------------------------------------------
segmentation (6 merges):
 burmese   အ ခ ျ က ် အ လ က ်  က ိ ု   token   မ ျ ာ ... (+99 more)
 code      d e f   a d d ( a ,   b ) : \n       ... (+13 more)
==========================================================================
```

Sweep run -
```bash
python3 lab_tokenizer.py --sweep
```

Output -
```
==========================================================================
lab_tokenizer - merge-count sweep (token အရေအတွက် နှင့် chars/token)
--------------------------------------------------------------------------
 merges  vocab  burmese       english       code        
      0     60  136 tok       86 tok        31 tok      
      2     62  126 tok       84 tok        31 tok      
      4     64  123 tok       79 tok        31 tok      
      6     66  117 tok       77 tok        31 tok      
      8     68  113 tok       77 tok        29 tok      
     10     70  110 tok       76 tok        27 tok      
     12     72  109 tok       71 tok        27 tok      
     16     76  103 tok       65 tok        27 tok      
     20     80  97 tok        63 tok        25 tok      
--------------------------------------------------------------------------
မှတ်ချက် - merge တိုးလျှင် vocabulary ကြီးပြီး token အရေအတွက် ကျဆင်းသည်။
==========================================================================
```

## lab_split_leak.py - Split နယ်နိမိတ် ဖြတ်ကျော်သည့် leakage

record တိုင်းကို entity group တစ်ခုထဲ ထည့်ပြီး `--leak-rate` အလိုက် record အချို့ကို
၎င်း၏ ရှေ့ record ၏ အနီးစပ်ဆုံး တူညီသည့် မိတ္တူ အဖြစ် ဖန်တီးသည်။ ကျပန်း row split နှင့်
entity group split နှစ်ခုကို နှိုင်းယှဉ်ပြီး 5-gram shingle နှင့် Jaccard ဆင်တူမှုဖြင့်
ယိုစိမ့်မှုကို တကယ် တိုင်းတာသည်။

```bash
python3 lab_split_leak.py                              # default: n 2000, val-fraction 0.2, seed 0, leak-rate 0.10
python3 lab_split_leak.py --n 1500 --val-fraction 0.3 --seed 7 --leak-rate 0.30
python3 lab_split_leak.py --leak-rate 0.0
python3 lab_split_leak.py --sweep                      # leak-rate 0.00 .. 0.30
python3 lab_split_leak.py --self-test
python3 lab_split_leak.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_split_leak - random row split vs entity-group split (offline, deterministic)
records=2000  val-fraction=0.2  seed=0  leak-rate=0.10  group-size=6
detection: 5-gram shingles, Jaccard >= 0.80
--------------------------------------------------------------------------
                               row split   group split
 train records                      1600          1598
 val records                         400           402
 planted near-duplicates             174           174
 val records with a train twin         63             0
 contamination rate               15.75%         0.00%
 clean val accuracy               0.7491        0.7502
 reported val accuracy            0.7845        0.7502
 score inflation                 +0.0354       +0.0000
--------------------------------------------------------------------------
မှတ်ချက် - ကျပန်း ခွဲခြားမှုသည် အနီးစပ်ဆုံး တူညီသည့် နမူနာများကို split နယ်နိမိတ် ဖြတ်ကျော်စေသည်၊ entity အလိုက် ခွဲခြားလျှင် ထို ဖြတ်ကျော်မှု မရှိပါ။
==========================================================================
```

Knob-changed run (`--n`၊ `--val-fraction`၊ `--seed` နှင့် `--leak-rate` ပြောင်းသည်) -
```bash
python3 lab_split_leak.py --n 1500 --val-fraction 0.3 --seed 7 --leak-rate 0.30
```

Output -
```
==========================================================================
lab_split_leak - random row split vs entity-group split (offline, deterministic)
records=1500  val-fraction=0.3  seed=7  leak-rate=0.30  group-size=6
detection: 5-gram shingles, Jaccard >= 0.80
--------------------------------------------------------------------------
                               row split   group split
 train records                      1050          1050
 val records                         450           450
 planted near-duplicates             371           371
 val records with a train twin        157             0
 contamination rate               34.89%         0.00%
 clean val accuracy               0.7421        0.7409
 reported val accuracy            0.8315        0.7409
 score inflation                 +0.0894       +0.0000
--------------------------------------------------------------------------
မှတ်ချက် - ကျပန်း ခွဲခြားမှုသည် အနီးစပ်ဆုံး တူညီသည့် နမူနာများကို split နယ်နိမိတ် ဖြတ်ကျော်စေသည်၊ entity အလိုက် ခွဲခြားလျှင် ထို ဖြတ်ကျော်မှု မရှိပါ။
==========================================================================
```

Sweep run -
```bash
python3 lab_split_leak.py --sweep
```

Output -
```
==========================================================================
lab_split_leak - leak-rate sweep (row split)
--------------------------------------------------------------------------
 leak-rate  planted  val twins  contamination  reported acc  inflation
      0.00        0          0          0.00%        0.7491    +0.0000
      0.05       93         36          9.00%        0.7711    +0.0221
      0.10      174         63         15.75%        0.7845    +0.0354
      0.20      321        108         27.00%        0.8120    +0.0629
      0.30      472        147         36.75%        0.8379    +0.0888
--------------------------------------------------------------------------
မှတ်ချက် - leak-rate တက်လျှင် contamination rate တက်ပြီး ပြသသည့် accuracy လည်း တက်သည်။
==========================================================================
```

## lab_pipeline_budget.py - Data pipeline နှင့် accelerator လိုအပ်ချက်

tokens per epoch၊ steps၊ လိုအပ်သည့် examples per second၊ storage၊ wall clock နှင့်
စျေးနှုန်း တစ်ခုအောက်တွင် ကုန်ကျစရိတ်ကို တွက်ပြီး data pipeline သည် accelerator ကို
ကျွေးနိုင်မှု ရှိမရှိ ဆုံးဖြတ်သည်။

```bash
python3 lab_pipeline_budget.py                         # default: 1e10 tokens, epochs 2, batch 64, seq 4096, 20 us/token
python3 lab_pipeline_budget.py --corpus-tokens 20000000000 --epochs 3 --batch 128 --seq 2048 --encode-cost 6.0
python3 lab_pipeline_budget.py --encode-cost 200.0
python3 lab_pipeline_budget.py --sweep                 # encode-cost 2 .. 200 us/token
python3 lab_pipeline_budget.py --self-test
python3 lab_pipeline_budget.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_pipeline_budget - data pipeline vs accelerator demand (offline, deterministic)
corpus-tokens=10,000,000,000  epochs=2  batch=64  seq=4096  encode-cost=20.0 us/token
reference: 8 accelerators, 990 TFLOP/s peak, MFU 0.40, 7.0B params, USD 2.50/h
--------------------------------------------------------------------------
 tokens per epoch              :       10,000,000,000
 total tokens over epochs      :       20,000,000,000
 tokens per step (batch*seq)   :              262,144
 steps per epoch               :               38,147
 accelerator demand (tok/s)    :              75428.6
 pipeline supply (tok/s)       :              50000.0
 examples per second needed    :                18.42
 step time accelerator (s)     :                3.475
 step time pipeline (s)        :                5.243
 accelerator utilisation       :               66.29%
 effective tokens/s            :              50000.0
--------------------------------------------------------------------------
 storage, uint32 token ids     :             37.25 GiB
 storage, raw UTF-8 text       :             37.25 GiB
 storage, both copies          :             74.51 GiB
 wall clock                    :               111.11 h
 accelerator-hours             :               888.89
 cost at USD 2.50/accel-hour    :            2222.22 USD
 verdict                       : PIPELINE-BOUND - the accelerator waits for data
--------------------------------------------------------------------------
မှတ်ချက် - pipeline သည် accelerator လိုအပ်သည့် tokens/s ကို မမီလျှင် accelerator သည် data ကို စောင့်ရသည်။
==========================================================================
```

Knob-changed run (corpus၊ epochs၊ batch၊ seq နှင့် encode-cost ပြောင်းသည်) -
```bash
python3 lab_pipeline_budget.py --corpus-tokens 20000000000 --epochs 3 --batch 128 --seq 2048 --encode-cost 6.0
```

Output -
```
==========================================================================
lab_pipeline_budget - data pipeline vs accelerator demand (offline, deterministic)
corpus-tokens=20,000,000,000  epochs=3  batch=128  seq=2048  encode-cost=6.0 us/token
reference: 8 accelerators, 990 TFLOP/s peak, MFU 0.40, 7.0B params, USD 2.50/h
--------------------------------------------------------------------------
 tokens per epoch              :       20,000,000,000
 total tokens over epochs      :       60,000,000,000
 tokens per step (batch*seq)   :              262,144
 steps per epoch               :               76,294
 accelerator demand (tok/s)    :              75428.6
 pipeline supply (tok/s)       :             166666.7
 examples per second needed    :                36.83
 step time accelerator (s)     :                3.475
 step time pipeline (s)        :                1.573
 accelerator utilisation       :              100.00%
 effective tokens/s            :              75428.6
--------------------------------------------------------------------------
 storage, uint32 token ids     :             74.51 GiB
 storage, raw UTF-8 text       :             74.51 GiB
 storage, both copies          :            149.01 GiB
 wall clock                    :               220.96 h
 accelerator-hours             :              1767.68
 cost at USD 2.50/accel-hour    :            4419.19 USD
 verdict                       : COMPUTE-BOUND - the pipeline keeps the accelerator fed
--------------------------------------------------------------------------
မှတ်ချက် - pipeline သည် accelerator လိုအပ်သည့် tokens/s ကို မမီလျှင် accelerator သည် data ကို စောင့်ရသည်။
==========================================================================
```

Sweep run -
```bash
python3 lab_pipeline_budget.py --sweep
```

Output -
```
==========================================================================
lab_pipeline_budget - encode-cost sweep
--------------------------------------------------------------------------
 us/token  pipeline tok/s  utilisation  effective tok/s  wall hours  verdict
      2.0        500000.0      100.00%          75428.6       73.65  compute-bound
      5.0        200000.0      100.00%          75428.6       73.65  compute-bound
     10.0        100000.0      100.00%          75428.6       73.65  compute-bound
     20.0         50000.0       66.29%          50000.0      111.11  pipeline-bound
     50.0         20000.0       26.52%          20000.0      277.78  pipeline-bound
    200.0          5000.0        6.63%           5000.0     1111.11  pipeline-bound
--------------------------------------------------------------------------
မှတ်ချက် - encode-cost ကျဆင်းလျှင် utilisation တက်သည်၊ wall clock ကျဆင်းသည်။
==========================================================================
```

## မှတ်ချက်

- Output အားလုံးကို `python3 verify_guide.py --labs --verbose` ဖြင့် စစ်ဆေးနိုင်သည်။
- `--self-test` သည် တိကျသည့် ဂုဏ်သတ္တိများကို assert လုပ်သည် (merge တစ်ခုလျှင်
  vocabulary တစ်ခု တက်၊ merge ကို 0 ထားလျှင် token အရေအတွက်သည် character အရေအတွက်
  နှင့် တူ၊ merge များလျှင် token မတက်၊ group split တွင် leakage မရှိ၊ leak-rate တက်လျှင်
  contamination rate တက်၊ pipeline supply ကျလျှင် utilisation ကျ)။
- Flag တိုင်း၏ အဓိပ္ပာယ်ကို `python3 <lab> --help` ဖြင့် ကြည့်နိုင်သည်။
