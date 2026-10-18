# Labs - Area 01: Math & Training

ဤ lab suite သည် area 01 ၏ term များ (Gradient၊ Learning Rate၊ Learning Rate Schedule၊
Warmup၊ Activation Checkpointing၊ Mixed Precision၊ Optimizer၊ Batch Size) ကို လက်တွေ့
တွက်ကြည့်ရန် ဖြစ်ပါသည်။ Python standard library သာ အသုံးပြုပါသည်၊ network နှင့် GPU
မလိုအပ်ပါ၊ run တိုင်း ရလဒ် တူညီပါသည် (deterministic)။

## Run the whole suite (မဖြစ်မနေ)

```bash
cd guides/01_math_and_training/labs
python3 run_labs.py
```

Lab တိုင်းအတွက် `--self-test` ကို run ပြီး တစ်လိုင်း စီ ပြပါသည်။ အားလုံး အောင်မြင်ပါက `[PASS] All 3/3 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်ပါသည်။
```
==========================================================================
run_labs - area 01 Math & Training (offline, deterministic)
==========================================================================
[PASS] lab_gradient_step.py: [PASS] lab_gradient_step self-test passed.
[PASS] lab_schedule.py: [PASS] lab_schedule self-test passed.
[PASS] lab_memory.py: [PASS] lab_memory self-test passed.
==========================================================================
[PASS] All 3/3 labs passed successfully.
```
## lab_gradient_step.py - quadratic trajectory၊ momentum နှင့် divergence

f(w) = 0.5 * (8.0 * w1^2 + 0.5 * w2^2) ဟူသည့် fixed quadratic ပေါ်တွင် gradient descent ကို
run ပြီး step တိုင်း၏ w1၊ w2၊ |grad| နှင့် loss ကို ပြပါသည်။ critical lr သည်
2*(1+momentum)/8.0 ဖြစ်သဖြင့် ၎င်းအထက် သတ်မှတ်လျှင် loss သည် ချဲ့ထွင်လာပါသည်။

```bash
python3 lab_gradient_step.py                          # default: lr 0.05, steps 12, momentum 0.0, seed 0
python3 lab_gradient_step.py --lr 0.40 --momentum 0.90 --steps 8
python3 lab_gradient_step.py --sweep                 # lr 0.01 .. 0.40
python3 lab_gradient_step.py --self-test
python3 lab_gradient_step.py --help
```

Default run ၏ အမှန်တကယ် output -
```
============================================================================================
lab_gradient_step - quadratic trajectory, learning rate and divergence (offline, deterministic)
f(w) = 0.5 * (8.0 * w1^2 + 0.5 * w2^2)   start=(1.034442, 1.025795)   seed=0
lr=0.0500  momentum=0.00  steps=12  critical lr = 2*(1+momentum)/8.0 = 0.2500
--------------------------------------------------------------------------------------------
 step             w1             w2         |grad|           loss
    0   1.034442e+00   1.025795e+00   8.291416e+00   4.543347e+00
    1   6.206653e-01   1.000151e+00   4.990441e+00   1.790977e+00
    2   3.723992e-01   9.751468e-01   3.018828e+00   7.924524e-01
    3   2.234395e-01   9.507681e-01   1.849650e+00   4.256909e-01
    4   1.340637e-01   9.269989e-01   1.168379e+00   2.867241e-01
    5   8.043822e-02   9.038239e-01   7.863359e-01   2.301057e-01
    6   4.826293e-02   8.812283e-01   5.858470e-01   2.034581e-01
    7   2.895776e-02   8.591976e-01   4.880804e-01   1.879094e-01
    8   1.737466e-02   8.377177e-01   4.413196e-01   1.766502e-01
    9   1.042479e-02   8.167748e-01   4.168159e-01   1.672150e-01
   10   6.254876e-03   7.963554e-01   4.013096e-01   1.587020e-01
   11   3.752926e-03   7.764465e-01   3.893825e-01   1.507736e-01
   12   2.251755e-03   7.570353e-01   3.789461e-01   1.432959e-01
--------------------------------------------------------------------------------------------
loss step 0 -> step 12 : 4.543347e+00 -> 1.432959e-01    max |w| = 1.034442e+00    status STABLE
မှတ်ချက် - lr သည် critical တန်ဖိုး 0.2500 အောက် ရှိသဖြင့် trajectory သည် ကျုံ့ဝင်ပါသည်။
============================================================================================
```
```bash
python3 lab_gradient_step.py --lr 0.40 --momentum 0.90 --steps 8
```

`--lr 0.40 --momentum 0.90 --steps 8` run ၏ အမှန်တကယ် output (momentum က critical lr ကို 0.4750 သို့ တင်သဖြင့် တည်ငြိမ်ဆဲ ဖြစ်သည်) -
```
============================================================================================
lab_gradient_step - quadratic trajectory, learning rate and divergence (offline, deterministic)
f(w) = 0.5 * (8.0 * w1^2 + 0.5 * w2^2)   start=(1.034442, 1.025795)   seed=0
lr=0.4000  momentum=0.90  steps=8  critical lr = 2*(1+momentum)/8.0 = 0.4750
--------------------------------------------------------------------------------------------
 step             w1             w2         |grad|           loss
    0   1.034442e+00   1.025795e+00   8.291416e+00   4.543347e+00
    1  -2.275773e+00   8.206364e-01   1.821081e+01   2.088493e+01
    2   2.027507e+00   4.718659e-01   1.622177e+01   1.649880e+01
    3  -5.875632e-01   6.359932e-02   4.700613e+00   1.381933e+00
    4  -1.060924e+00  -3.165605e-01   8.488867e+00   4.527291e+00
    5   1.908008e+00  -5.953922e-01   1.526697e+01   1.465060e+01
    6  -1.525579e+00  -7.272623e-01   1.221005e+01   9.441790e+00
    7   2.660453e-01  -7.004929e-01   2.156988e+00   4.057930e-01
    8   1.027162e+00  -5.363019e-01   8.221670e+00   4.292152e+00
--------------------------------------------------------------------------------------------
loss step 0 -> step 8 : 4.543347e+00 -> 4.292152e+00    max |w| = 2.275773e+00    status STABLE
မှတ်ချက် - lr သည် critical တန်ဖိုး 0.4750 အောက် ရှိသဖြင့် trajectory သည် ကျုံ့ဝင်ပါသည်။
============================================================================================
```
## lab_schedule.py - constant၊ step၊ cosine နှင့် warmup

schedule တစ်ခုစီ၏ learning rate ကို step တိုင်းအတွက် ဇယားဖြင့် ပြပြီး max၊ min၊ mean နှင့်
decreasing step အရေအတွက်ကို အကျဉ်းချုပ် ပြပါသည်။ `--sweep` သည် schedule လေးခုကို
တစ်လိုင်းစီဖြင့် နှိုင်းယှဉ်ပါသည်။

```bash
python3 lab_schedule.py                               # default: warmup, steps 12, base-lr 1e-3, peak 3e-3
python3 lab_schedule.py --schedule cosine --steps 10 --base-lr 2e-3
python3 lab_schedule.py --sweep                       # schedule လေးခု နှိုင်းယှဉ်ခြင်း
python3 lab_schedule.py --self-test
python3 lab_schedule.py --help
```

Default run ၏ အမှန်တကယ် output -
```
============================================================================================
lab_schedule - learning rate schedule table (offline, deterministic)
schedule=warmup  steps=12  base-lr=1.000e-03  peak=3.000e-03  warmup=4
--------------------------------------------------------------------------------------------
 step               lr        delta        phase
    1      0.001500000 +0.000000000       warmup
    2      0.002000000 +0.000500000       warmup
    3      0.002500000 +0.000500000       warmup
    4      0.003000000 +0.000500000       warmup
    5      0.002923880 -0.000076120        decay
    6      0.002707107 -0.000216773        decay
    7      0.002382683 -0.000324423        decay
    8      0.002000000 -0.000382683        decay
    9      0.001617317 -0.000382683        decay
   10      0.001292893 -0.000324423        decay
   11      0.001076120 -0.000216773        decay
   12      0.001000000 -0.000076120        decay
--------------------------------------------------------------------------------------------
summary: max lr 3.000000e-03 at step 4, min lr 1.000000e-03 at step 12
         mean lr 2.000000e-03, area under the curve 2.400000e-02 lr-steps, decreasing steps 8
မှတ်ချက် - schedule သည် အစောပိုင်း တည်ငြိမ်မှုနှင့် နောက်ပိုင်း သက်သာမှုကို လဲလှယ်ပါသည်
         warmup က phase များကို ပြသည်၊ lr budget တူညီမှုကို mean lr ဖြင့် နှိုင်းယှဉ်ပါသည်။
============================================================================================
```
```bash
python3 lab_schedule.py --schedule cosine --steps 10 --base-lr 2e-3
```

`--schedule cosine --steps 10 --base-lr 2e-3` run ၏ အမှန်တကယ် output -
```
============================================================================================
lab_schedule - learning rate schedule table (offline, deterministic)
schedule=cosine  steps=10  base-lr=2.000e-03  peak=3.000e-03  warmup=4
--------------------------------------------------------------------------------------------
 step               lr        delta        phase
    1      0.002000000 +0.000000000        decay
    2      0.001939693 -0.000060307        decay
    3      0.001766044 -0.000173648        decay
    4      0.001500000 -0.000266044        decay
    5      0.001173648 -0.000326352        decay
    6      0.000826352 -0.000347296        decay
    7      0.000500000 -0.000326352        decay
    8      0.000233956 -0.000266044        decay
    9      0.000060307 -0.000173648        decay
   10      0.000000000 -0.000060307        decay
--------------------------------------------------------------------------------------------
summary: max lr 2.000000e-03 at step 1, min lr 0.000000e+00 at step 10
         mean lr 1.000000e-03, area under the curve 1.000000e-02 lr-steps, decreasing steps 9
မှတ်ချက် - schedule သည် အစောပိုင်း တည်ငြိမ်မှုနှင့် နောက်ပိုင်း သက်သာမှုကို လဲလှယ်ပါသည်
         warmup က phase များကို ပြသည်၊ lr budget တူညီမှုကို mean lr ဖြင့် နှိုင်းယှဉ်ပါသည်။
============================================================================================
```
## lab_memory.py - weights၊ gradients၊ optimizer state နှင့် activations

training VRAM ကို component အလိုက် ခွဲပြပါသည်။ d_model ကို params = 12 * layers * d_model^2
ဟူသည့် ခန့်မှန်းချက်မှ ဆင်းသက်စေပြီး activation ကို act_factor 10 (off) နှင့် 2 (on) ဖြင့်
တွက်ပါသည်။ checkpointing သည် activation ကို ၅ ဆ လျှော့ပြီး step FLOPs ကို 1.333 ဆ တင်ပါသည်။

```bash
python3 lab_memory.py                                 # default: 1.3B, batch 8, seq 2048, layers 24, fp16, off
python3 lab_memory.py --params-b 7 --layers 32 --seq 4096 --activation-checkpointing on
python3 lab_memory.py --sweep                         # batch 1, 2, 4, 8, 16, 32
python3 lab_memory.py --self-test
python3 lab_memory.py --help
```

Default run ၏ အမှန်တကယ် output -
```
============================================================================================
lab_memory - training VRAM breakdown by component (offline, deterministic)
params=1.30B  layers=24  d_model=2125  batch=8  seq=2048  dtype=fp16  checkpointing=off
assumptions: weights and gradients in fp16 (2.0 B/param), Adam keeps two fp32 moments,
             activations = batch*seq*layers*d_model*act_factor*bpp with act_factor 10 (off) / 2 (on)
--------------------------------------------------------------------------------------------
component (GiB)                   checkpointing=off   checkpointing=on
weights                                       2.421              2.421
gradients                                     2.421              2.421
optimizer state (Adam fp32)                   9.686              9.686
activations                                  15.564              3.113
--------------------------------------------------------------------------------------------
total VRAM                                   30.093             17.641
fits one 80 GB card (64 GiB usable)                yes                yes
recompute overhead (x step FLOPs)               none              1.333
မှတ်ချက် - activation checkpointing သည် activation memory ကို 5.0x လျှော့ပြီး
         compute အပိုအလွှာ (step FLOPs x 1.333) ဖြင့် ဝယ်ယူပါသည်။
============================================================================================
```
```bash
python3 lab_memory.py --params-b 7 --layers 32 --seq 4096 --activation-checkpointing on
```

`--params-b 7 --layers 32 --seq 4096 --activation-checkpointing on` run ၏ အမှန်တကယ် output -
```
============================================================================================
lab_memory - training VRAM breakdown by component (offline, deterministic)
params=7.00B  layers=32  d_model=4270  batch=8  seq=4096  dtype=fp16  checkpointing=on
assumptions: weights and gradients in fp16 (2.0 B/param), Adam keeps two fp32 moments,
             activations = batch*seq*layers*d_model*act_factor*bpp with act_factor 10 (off) / 2 (on)
--------------------------------------------------------------------------------------------
component (GiB)                   checkpointing=off   checkpointing=on
weights                                      13.039             13.039
gradients                                    13.039             13.039
optimizer state (Adam fp32)                  52.154             52.154
activations                                  83.398             16.680
--------------------------------------------------------------------------------------------
total VRAM                                  161.630             94.911
fits one 80 GB card (64 GiB usable)                 no                 no
recompute overhead (x step FLOPs)               none              1.333
မှတ်ချက် - activation checkpointing သည် activation memory ကို 5.0x လျှော့ပြီး
         compute အပိုအလွှာ (step FLOPs x 1.333) ဖြင့် ဝယ်ယူပါသည်။
============================================================================================
```
## မှတ်ချက်

- Output အားလုံးကို `python3 verify_guide.py --guide 01 --labs --verbose` ဖြင့် စစ်ဆေးနိုင်ပါသည်။
- `--self-test` သည် တိကျသည့် ဂုဏ်သတ္တိများကို assert လုပ်ပါသည် — critical lr အထက်တွင် divergence
  ဖြစ်ခြင်း၊ momentum က critical lr ကို တင်ခြင်း၊ cosine သည် အလယ်တွင် ထက်ဝက် ကျဆင်းခြင်း၊
  warmup သည် peak သို့ တင်ပြီး ပြန်ကျခြင်း၊ activation checkpointing သည် activation ကို ၅ ဆ
  လျှော့ပြီး compute ကို ပိုလိုခြင်း။
- Flag တိုင်း၏ အဓိပ္ပာယ်ကို `python3 <lab> --help` ဖြင့် ကြည့်နိုင်ပါသည်။
