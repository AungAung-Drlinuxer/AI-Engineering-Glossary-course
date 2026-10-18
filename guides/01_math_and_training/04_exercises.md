# ၀၄ — လေ့ကျင့်ခန်းများနှင့် အဖြေများ (Math & Training)

ဤဖိုင်သည် နယ်ပယ် ၀၁ ၏ term ၄၂ ခုကို အသုံးပြု၍ တွက်ချက်ခြင်း၊ ပြဿနာ ရှာဖွေခြင်းနှင့် ဆုံးဖြတ်ချက် ချခြင်း
လေ့ကျင့်ခန်းများကို စုစည်းထားသည်။ အပိုင်း ၁ တွင် အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာ လေးခု၊ အပိုင်း ၂ တွင်
တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ခြောက်ခု၊ အပိုင်း ၃ တွင် ပြဿနာ ရှာဖွေခြင်း သုံးခု၊ အပိုင်း ၄ တွင်
ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း နှစ်ခု ပါဝင်သည်။ အပိုင်း ၅ တွင် အဖြေတိုင်းကို ဖော်မြူလာ၊ တွက်ချက်မှု
အဆင့်ဆင့်နှင့် အကြောင်းရင်း ရှင်းလင်းချက်နှင့်အတူ ပေးထားသည်။

အပိုင်း ၁ နှင့် အပိုင်း ၅ တွင် ပါဝင်သည့် ကိန်းဂဏန်း တိုင်းသည် Python (standard library သာ) ဖြင့်
အမှန်တကယ် လုပ်ဆောင်ခဲ့သည့် တွက်ချက်မှု၏ output ဖြစ်သည်။ ဖော်ပြထားသည့် command အတိုင်း run
လုပ်ပါက တူညီသည့် output ကို ပြန်လည် ရရှိမည်။ ကိန်းဂဏန်း တိုင်းသည် သတ်မှတ်ထားသည့် geometry၊
dtype နှင့် ယူဆချက် အပေါ် မှီခိုသည်၊ ထို့ကြောင့် ဖော်မြူလာ တစ်ခုစီနှင့်အတူ ၎င်း၏ ယူဆချက်
(assumption) ကို ဖော်ပြထားသည်။ ဤ ကိန်းဂဏန်းများသည် **တိုင်းတာချက် (benchmark) မဟုတ်ပါ** —
ဖော်ပြထားသည့် ယူဆချက်အောက်တွင် ရရှိသည့် တန်ဖိုးများ ဖြစ်သည်။

လေ့ကျင့်ခန်းများကို လက်တွေ့ စမ်းသပ်ရန် `labs/lab_gradient_step.py` (gradient step နှင့် ပြိုလဲမှု)၊
`labs/lab_schedule.py` (learning rate schedule အမျိုးအစားများ) နှင့် `labs/lab_memory.py`
(weights၊ gradients၊ optimizer state၊ activations) တို့ကို အသုံးပြုနိုင်သည်။ regularization
အတွက် lab မရှိသေးသဖြင့် ထို အပိုင်းကို ဤဖိုင်၏ Python block များဖြင့် စစ်ရမည်။ ဤဖိုင်၏
တွက်ချက်မှုများသည် lab များအပေါ် မှီခိုမှု မရှိပါ — ထို့ကြောင့် ကိန်းဂဏန်း တိုင်းကို ကိုယ်တိုင်
ပြန်ထုတ်နိုင်သည်။

## ၁။ အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာများ (Worked Examples)

### ဥပမာ ၁ — forward/backward ၏ shape နှင့် memory စာရင်း

**ယူဆချက် —** d_model 512၊ attention head 8 ခု (head_dim 64)၊ FFN အတွင်း dimension 2048၊ block 12 ခု၊
vocabulary 32000၊ sequence 1024၊ batch 4။ weight နှင့် activation တို့ကို fp16 ဖြင့် ထားသည်၊
optimizer သည် AdamW ဖြစ်၍ gradient နှင့် optimizer state ကို fp32 ဖြင့် ထားသည်။
layer တစ်ခုလျှင် activation tensor A = 10 ခုကို သိမ်းဆည်းသည်ဟု ယူဆသည် (activation checkpointing
မလုပ်ပါ။) bias နှင့် layer norm parameter များကို ထည့်မတွက်ပါ။

**ဖော်မြူလာ —**
- attention parameter (block တစ်ခုလျှင်) = 4 × d²
- FFN parameter (block တစ်ခုလျှင်) = 2 × d × ffn
- embedding parameter = vocabulary × d
- activation bytes = A × sequence × batch × d × element byte × block အရေအတွက်
- checkpointing ဖြင့် သိမ်းသည့် activation = 2 × sequence × batch × d × element byte × block အရေအတွက်

**တွက်ချက်မှု —**
1. attention = 4 × 512² = 1,048,576၊ FFN = 2 × 512 × 2048 = 2,097,152၊ ထို့ကြောင့် block တစ်ခုလျှင်
   3,145,728 ဖြစ်သည်။
2. block 12 ခုအတွက် 37,748,736၊ embedding 16,384,000၊ စုစုပေါင်း 54,132,736 ≈ 54.1 M ဖြစ်သည်။
3. weight fp32 = 206.5 MiB၊ fp16 = 103.2 MiB၊ gradient fp32 = 206.5 MiB၊ AdamW ၏ m နှင့် v = 413.0 MiB
   ဖြစ်သည်။
4. activation fp16 = 480.0 MiB ဖြစ်သည်။ ၎င်းသည် weight နှင့် optimizer state စုစုပေါင်း (413.0 + 103.2)
   ထက် ကြီးသည်။
5. activation checkpointing ဖြင့် 96.0 MiB သို့ ကျဆင်းသည်၊ ဆိုလိုသည်မှာ 0.2 အချိုး (80 % လျော့) ဖြစ်သည်။

**ကောက်ချက် —** parameter 54.1 M သာ ရှိသည့် model တွင်ပင် activation သည် weight ထက် ကြီးသည်။
ထို့ကြောင့် memory ပြဿနာ၏ အရင်းအမြစ်ကို ရှာသည့်အခါ weight ကို ရှေးဦး စစ်ခြင်းသည် လမ်းလွဲစေနိုင်သည်။

```bash
python3 - <<'PY'
d, heads, head_dim, ffn, layers, vocab, seq, batch = 512, 8, 64, 2048, 12, 32000, 1024, 4
qkv, ff = 4 * d * d, 2 * d * ffn
block, body, emb = qkv + ff, (qkv + ff) * layers, vocab * d
total = body + emb
print("params per block     ", block)
print("body params          ", body)
print("embedding params     ", emb)
print("total params         ", total)
print("weights fp32 MiB     ", round(total * 4 / 2**20, 1))
print("weights fp16 MiB     ", round(total * 2 / 2**20, 1))
print("grads fp32 MiB       ", round(total * 4 / 2**20, 1))
print("adamw m+v fp32 MiB   ", round(total * 8 / 2**20, 1))
A = 10
print("activations fp16 MiB ", round(A * seq * batch * d * 2 * layers / 2**20, 1))
print("act with ckpt MiB    ", round(2 * seq * batch * d * 2 * layers / 2**20, 1))
PY
```

```text
params per block      3145728
body params           37748736
embedding params      16384000
total params          54132736
weights fp32 MiB      206.5
weights fp16 MiB      103.2
grads fp32 MiB        206.5
adamw m+v fp32 MiB    413.0
activations fp16 MiB  480.0
act with ckpt MiB     96.0
```

### ဥပမာ ၂ — logits မှ cross-entropy နှင့် ၎င်း၏ gradient

**ယူဆချက် —** logits = [2.5, 0.5, -1.0, 3.0]၊ ရည်မှန်း index = 3။ softmax ကို max နုတ်သည့်
numerical stabilization ဖြင့် အကောင်အထည်ဖော်သည်။ log ၏ base ကို e ဟု ယူသည်။

**ဖော်မြူလာ —**
- softmax(x_i) = exp(x_i - max x) / ပေါင်းလဒ် (exp(x_j - max x))
- loss = -log(softmax ၏ ရည်မှန်း index တန်ဖိုး)
- perplexity = exp(loss)
- dL/dlogit_i = softmax_i - (i သည် ရည်မှန်း index ဖြစ်ပါက 1၊ မဟုတ်ပါက 0)

**တွက်ချက်မှု —**
1. max = 3.0၊ exp(z - 3) = [0.606531, 0.082085, 0.018316, 1.0]၊ ပေါင်းလဒ် = 1.706931 ဖြစ်သည်။
2. softmax = [0.355334, 0.048089, 0.010730, 0.585847] ဖြစ်သည်၊ ပေါင်းလဒ် = 1.0 ဖြစ်သည်။
3. ရည်မှန်း index ၏ probability = 0.585847၊ ထို့ကြောင့် loss = -ln(0.585847) = 0.534697 nats ဖြစ်သည်။
   3 - 1 ၏ အကျိုးအမြတ်မှာ 0.771405 bits ဖြစ်သည်။
4. perplexity = exp(0.534697) = 1.706931 ဖြစ်သည် (မှတ်သားရန် — ဤတန်ဖိုးသည် exp(z - max) ၏
   ပေါင်းလဒ်နှင့် တူညီသည်၊ တိုက်ဆိုင်မှု မဟုတ်ပါ)။
5. gradient = [0.355334, 0.048089, 0.010730, -0.414153] ဖြစ်သည်၊ ပေါင်းလဒ် = 0 ဖြစ်သည်။
6. model က ရည်မှန်း token ကို 0.936912 probability ဖြင့် မှန်ကန်စွာ သတ်မှတ်ပါက loss သည်
   0.065166 သို့ ကျဆင်းသည်၊ ဆိုလိုသည်မှာ ဤဥပမာ၏ 0.12 အချိုးသာ ဖြစ်သည်။

**ကောက်ချက် —** cross-entropy သည် ရည်မှန်း token ၏ probability ၏ log ပေါ်တွင်သာ မှီခိုသည်။
gradient ၏ ပုံစံသည် ရိုးရှင်းသည် (softmax မှ one-hot ကို နုတ်ခြင်း)၊ သို့သော် တန်ဖိုးများသည်
softmax မှ တိုက်ရိုက် လာသဖြင့် numerical stabilization မရှိပါက ပျက်စီးသည်။

```bash
python3 - <<'PY'
import math
logits, target = [2.5, 0.5, -1.0, 3.0], 3
m = max(logits)
ex = [math.exp(z - m) for z in logits]
p = [e / sum(ex) for e in ex]
ce = -math.log(p[target])
print("exp values  ", [round(e, 6) for e in ex], "sum", round(sum(ex), 6))
print("softmax     ", [round(v, 6) for v in p], "sum", round(sum(p), 6))
print("loss nats   ", round(ce, 6), "bits", round(ce / math.log(2), 6))
print("perplexity  ", round(math.exp(ce), 6))
print("dL/dlogit   ", [round(pi - (1.0 if i == target else 0.0), 6) for i, pi in enumerate(p)])
bad = [0.1, 0.2, 0.3, 4.0]
exb = [math.exp(z - max(bad)) for z in bad]
pb = [e / sum(exb) for e in exb]
print("sharp case p(target)", round(pb[3], 6), "CE", round(-math.log(pb[3]), 6),
      "ratio", round(-math.log(pb[3]) / ce, 2))
PY
```

```text
exp values   [0.606531, 0.082085, 0.018316, 1.0] sum 1.706931
softmax      [0.355334, 0.048089, 0.01073, 0.585847] sum 1.0
loss nats    0.534697 bits 0.771405
perplexity   1.706931
dL/dlogit    [0.355334, 0.048089, 0.01073, -0.414153]
sharp case p(target) 0.936912 CE 0.065166 ratio 0.12
```

### ဥပမာ ၃ — optimizer လေးခု၏ update trace ကို နှိုင်းယှဉ်ခြင်း

**ယူဆချက် —** L(w) = (w - 3)²၊ w0 = 1.0၊ learning rate = 0.1။ ထို့ကြောင့် gradient = 2 (w - 3) ဖြစ်ပြီး
w0 တွင် -4.0 ဖြစ်သည်။ Adam ၏ beta1 = 0.9၊ beta2 = 0.999၊ epsilon = 1e-8။ AdamW ၏ weight decay = 0.01
ဖြစ်ပြီး decoupled အနေဖြင့် w = w - lr × wd × w ကို gradient update ပြီးနောက် သီးခြား လုပ်သည်။

**ဖော်မြူလာ —**
- SGD: w ← w - lr × g
- momentum: v ← μ v + g၊ ထို့နောက် w ← w - lr × v
- Adam: m ← β₁m + (1-β₁)g၊ v ← β₂v + (1-β₂)g²၊ m̂ = m/(1-β₁ᵗ)၊ v̂ = v/(1-β₂ᵗ)၊ w ← w - lr × m̂/(√v̂ + ε)
- AdamW: Adam update ပြီးနောက် w ← w - lr × wd × w
- တည်ငြိမ်မှု အခြေအနေ (curvature 2): |1 - 2 lr| သေး 1၊ ဆိုလိုသည်မှာ lr သေး 1.0

**တွက်ချက်မှု —**
1. SGD = [1.4, 1.72, 1.976, 2.1808, 2.3446, 2.4757] ဖြစ်သည်၊ အနိမ့်ဆုံးအမှတ် 3 ကို step ၂၄ တွင်
   (|w - 3| သေး 0.01 ဖြစ်သည့်အခါ) ရောက်သည်။
2. momentum 0.9 = [1.4, 2.08, 2.876, 3.6172, 4.1608, 4.4179] ဖြစ်သည်၊ step ၄ တွင် 3.6172 ဖြစ်၍
   **ကျော်လွန် (overshoot)** သည်၊ ထို့နောက် ပြန်ကျသည်။
3. Adam = [1.1, 1.1998, 1.2994, 1.3985, 1.497, 1.5949] ဖြစ်သည်၊ update တစ်ကြိမ်လျှင် 0.1 ခန့် ဖြစ်သည်
   (bias correction ကြောင့် ပထမ step တွင် update = lr × m̂/(√v̂ + ε) = 0.1 × 4/4 = 0.1)။
4. AdamW = [1.0989, 1.1975, 1.2958, 1.3935, 1.4906, 1.5869] ဖြစ်သည်၊ ပထမ step တွင် ကျုံ့ဝင်မှုသည်
   lr × wd × 1.1 = 0.0011 ဖြစ်သည်။
5. lr = 1.0 တွင် 5 နှင့် 1 အကြား လှည့်နေသည် (တိုးတက်မှု သုည)၊ lr = 1.1 တွင် 5.4၊ 0.12၊ 6.456၊
   -1.1472 ဟု ပြန့်ထွက်သည်။

**ကောက်ချက် —** gradient တူညီသည့် အခြေအနေတွင် optimizer ရွေးချယ်မှုသည် update ၏ ပုံစံကို
လုံးလုံး ပြောင်းလဲသည်။ momentum သည် အရှိန်ဖြင့် ကျော်လွန်သည်၊ Adam သည် ပထမ step တွင်
အလေးသာစွာ ရွှေ့သည်၊ AdamW သည် ထို update အပေါ် ကျုံ့ဝင်မှု ထပ်ထည့်သည်။

```bash
python3 - <<'PY'
import math
g = lambda w: 2.0 * (w - 3.0)
def sgd(w, lr, n, mu=0.0):
    v, out = 0.0, []
    for _ in range(n):
        v = mu * v + g(w); w = w - lr * v; out.append(w)
    return out
def adam(w, lr, n, wd=0.0, decoupled=False):
    m = v = 0.0; out = []
    for t in range(1, n + 1):
        gg = g(w) + (0.0 if decoupled else wd * w)
        m = 0.9 * m + 0.1 * gg
        v = 0.999 * v + 0.001 * gg * gg
        w = w - lr * (m / (1 - 0.9 ** t)) / (math.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
        if decoupled:
            w = w - lr * wd * w
        out.append(w)
    return out
print("grad at w0 ", g(1.0))
print("sgd        ", [round(x, 4) for x in sgd(1.0, 0.1, 6)])
print("momentum   ", [round(x, 4) for x in sgd(1.0, 0.1, 6, mu=0.9)])
print("adam       ", [round(x, 4) for x in adam(1.0, 0.1, 6)])
print("adamw      ", [round(x, 4) for x in adam(1.0, 0.1, 6, wd=0.01, decoupled=True)])
print("lr 1.0     ", [round(x, 4) for x in sgd(1.0, 1.0, 6)])
print("lr 1.1     ", [round(x, 4) for x in sgd(1.0, 1.1, 6)])
PY
```

```text
grad at w0  -4.0
sgd         [1.4, 1.72, 1.976, 2.1808, 2.3446, 2.4757]
momentum    [1.4, 2.08, 2.876, 3.6172, 4.1608, 4.4179]
adam        [1.1, 1.1998, 1.2994, 1.3985, 1.497, 1.5949]
adamw       [1.0989, 1.1975, 1.2958, 1.3935, 1.4906, 1.5869]
lr 1.0      [5.0, 1.0, 5.0, 1.0, 5.0, 1.0]
lr 1.1      [5.4, 0.12, 6.456, -1.1472, 7.9766, -2.972]
```

### ဥပမာ ၄ — training memory ဘတ်ဂျက် (350 M model)

**ယူဆချက် —** parameter 350 M၊ d_model 1024၊ block 24 ခု၊ sequence 1024၊ batch 64၊ layer တစ်ခုလျှင်
activation tensor 12 ခု သိမ်းသည်။ weight ကို fp16၊ master weight၊ gradient နှင့် AdamW state ကို fp32
ဖြင့် ထားသည်။ device တွင် အသုံးပြုနိုင်သည့် memory 24.0 GiB ရှိသည် (usable အနေဖြင့် ထိုတန်ဖိုးကို
တိုက်ရိုက် သုံးသည်၊ framework overhead မထည့်ပါ။)

**ဖော်မြူလာ —**
- weight (fp16) = parameter × 2 bytes၊ master / gradient = parameter × 4 bytes
- AdamW state = parameter × 8 bytes (m နှင့် v၊ fp32)
- activation = A × sequence × batch × d × element byte × block အရေအတွက်
- checkpointing ဖြင့် activation = 2 × sequence × batch × d × element byte × block အရေအတွက်
- ထည့်နိုင်သည့် micro-batch = (usable GiB - optimizer side GiB) / sample တစ်ခုလျှင် activation GiB

**တွက်ချက်မှု —**
1. weight fp16 = 0.652 GiB၊ master = 1.304 GiB၊ gradient = 1.304 GiB၊ AdamW state = 2.608 GiB ဖြစ်သည်။
   optimizer side စုစုပေါင်း = 5.867 GiB ဖြစ်သည်။
2. activation = 12 × 1024 × 64 × 1024 × 2 × 24 bytes = 36.0 GiB ဖြစ်သည်၊ sample တစ်ခုလျှင် 0.5625 GiB
   ဖြစ်သည်။
3. စုစုပေါင်း = 41.867 GiB ဖြစ်သည်ဟု တွက်ရသည်၊ ဆိုလိုသည်မှာ 24 GiB device တွင် မဆံ့ပါ။
   activation ၏ share = 86.0 % ဖြစ်သည်။
4. activation checkpointing ဖြင့် activation = 6.0 GiB သို့ ကျဆင်းသည်၊ စုစုပေါင်း = 11.867 GiB ဖြစ်သည်။
5. 24.0 GiB device တွင် ထည့်နိုင်သည့် အနီးစပ်ဆုံး micro-batch = 32 (checkpointing မပါ)၊
   checkpointing ပါက 193 ဖြစ်သည်။
6. checkpointing ၏ ကုန်ကျစရိတ် — forward ၏ FLOPs ကို 1၊ backward ကို 2 ဟု ရေတွက်ပါက၊ ပြန်လည်
   တွက်ချက်မှု 1 သည် training step ၏ 33.33 % ထပ်တိုးစေသည်။

**ကောက်ချက် —** ဤ အခြေအနေတွင် memory ၏ 86 % သည် activation ဖြစ်သည်။ ထို့ကြောင့် batch ကို
ထက်ဝက်လျှော့ခြင်းနှင့် checkpointing ဖွင့်ခြင်းသည် activation ကို အဓိက ထိန်းညှိသည့် knob နှစ်ခု
ဖြစ်သည်၊ weight ကို quantize လုပ်ခြင်းသည် ဤပြဿနာအတွက် အသေးဆုံး အကျိုးသက်ရောက်မှုသာ ရှိသည်။

```bash
python3 - <<'PY'
params, d, layers, seq, batch, A = 350e6, 1024, 24, 1024, 64, 12
gib = lambda b: b / 2**30
w16, master, grads, opt = params * 2, params * 4, params * 4, params * 8
act = A * seq * batch * d * 2 * layers
act_ck = 2 * seq * batch * d * 2 * layers
side = w16 + master + grads + opt
print("weights fp16 GiB    ", round(gib(w16), 3))
print("master fp32 GiB     ", round(gib(master), 3))
print("grads fp32 GiB      ", round(gib(grads), 3))
print("adamw m,v GiB       ", round(gib(opt), 3))
print("optimizer side GiB  ", round(gib(side), 3))
print("activations GiB     ", round(gib(act), 3))
print("act per sample GiB  ", round(gib(A * seq * d * 2 * layers), 4))
print("act with ckpt GiB   ", round(gib(act_ck), 3))
print("total GiB           ", round(gib(side + act), 3))
print("total with ckpt GiB ", round(gib(side + act_ck), 3))
print("activation share pct", round(100 * act / (side + act), 1))
print("max micro no ckpt   ", int((24.0 - gib(side)) / gib(A * seq * d * 2 * layers)))
print("max micro with ckpt ", int((24.0 - gib(side)) / gib(2 * seq * d * 2 * layers)))
print("ckpt overhead pct   ", round(100 / 3, 2))
PY
```

```text
weights fp16 GiB     0.652
master fp32 GiB      1.304
grads fp32 GiB       1.304
adamw m,v GiB        2.608
optimizer side GiB   5.867
activations GiB      36.0
act per sample GiB   0.5625
act with ckpt GiB    6.0
total GiB            41.867
total with ckpt GiB  11.867
activation share pct 86.0
max micro no ckpt    32
max micro with ckpt  193
ckpt overhead pct    33.33
```

## ၂။ တွက်ချက်ရသည့် လေ့ကျင့်ခန်းများ (Calculation Exercises)

လေ့ကျင့်ခန်း တစ်ခုစီတွင် ကိန်းဂဏန်း အဖြေ အတိအကျ ရှိသည်။ အဖြေနှင့် ဖော်မြူလာ ရှင်းလင်းချက်ကို
အပိုင်း ၅.၁ တွင် ပေးထားသည်။

**လေ့ကျင့်ခန်း ၁ — softmax နှင့် cross-entropy ကို လက်ဖြင့် တွက်ခြင်း**

logits = [1.0, 2.0, 3.0]၊ ရည်မှန်း index = 0။ (က) exp တန်ဖိုးများနှင့် ပေါင်းလဒ်၊ (ခ) softmax၊
(ဂ) cross-entropy ကို nats နှင့် bits ဖြင့်၊ (ဃ) perplexity၊ (င) logit တိုင်းအပေါ် gradient နှင့်
၎င်း၏ ပေါင်းလဒ်၊ (စ) logits = [1000, 1001] ဖြစ်ပါက stabilization မပါဘဲ ဘာဖြစ်သနည်း၊
stabilization ပါက probability မည်မျှ ရသနည်း။ → ဤဖိုင်၏ Python block (softmax နှင့် cross-entropy အတွက် lab မရှိပါ။)

**လေ့ကျင့်ခန်း ၂ — function ငယ်တစ်ခု၏ gradient**

input x = [1.0, 2.0]။ ပထမ layer — W1 = [[0.5, -0.5], [1.0, 0.25]]၊ b1 = [0.0, -0.5]၊ activation = ReLU။
ဒုတိယ layer — w2 = [1.0, -2.0]၊ b2 = 0.0။ loss = 0.5 (z - 1)²။ (က) hidden pre-activation နှင့်
post-activation၊ (ခ) z နှင့် loss၊ (ဂ) dL/dz၊ dL/dw2၊ dL/db2၊ (ဃ) dL/dh နှင့် ReLU ၏ derivative
ဖြင့် ချိန်ညှိပြီးနောက် dL/dh_pre၊ (င) dL/dW1 နှင့် dL/db1၊ (စ) learning rate 0.1 ဖြင့် update
တစ်ကြိမ် လုပ်ပြီးနောက် loss၊ (ဆ) finite difference ဖြင့် dL/dw2[0] ကို အတည်ပြုခြင်း။
→ ဤဖိုင်၏ Python block (chain rule ကို `labs/lab_gradient_step.py` ၏ trajectory နှင့် တွဲဖတ်ပါ။)

**လေ့ကျင့်ခန်း ၃ — optimizer step တစ်ကြိမ်**

L(w) = (w - 3)²၊ w0 = 5.0။ (က) w0 တွင် gradient၊ (ခ) SGD lr 0.2 ဖြင့် step သုံးကြိမ်၏ trace၊
(ဂ) momentum 0.9 ဖြင့် ထို trace နှင့် overshoot ဖြစ်သည့် step၊ (ဃ) Adam lr 0.05 ဖြင့် ထို trace၊
bias correction ပြီးနောက် m̂ နှင့် v̂၊ (င) Adam ၏ ပထမ step update သည် lr နှင့် ညီမျှသည့်
အကြောင်းရင်း၊ (စ) lr 1.1 ဖြင့် step ရှစ်ကြိမ်၏ လမ်းကြောင်း။ → `labs/lab_gradient_step.py --sweep`

**လေ့ကျင့်ခန်း ၄ — learning rate schedule တန်ဖိုး**

warmup 400 step (0 မှ 6e-4 အထိ linear)၊ ထို့နောက် step 5000 အထိ cosine decay ဖြင့် peak ၏ 5 %
သို့ ကျသည်။ (က) step 100၊ 200၊ 399၊ 400 တို့၏ rate၊ (ခ) step 1000၊ 2500၊ 4000 ၏ rate နှင့်
peak ၏ အချိုး၊ (ဂ) decay ၏ အလယ်အမှတ် (step 2700) ၏ rate၊ (ဃ) step 5000 ၏ rate၊
(င) step 0 မှ 5000 အထိ ပျမ်းမျှ rate နှင့် ၎င်းသည် peak ၏ မည်မျှ၊ (စ) batch 32 နှင့် sequence
1024 ဖြင့် warmup 400 step သည် token မည်မျှ နှင့် ညီသနည်း။ → `labs/lab_schedule.py --sweep`

**လေ့ကျင့်ခန်း ၅ — weight decay ၏ အကျိုးသက်ရောက်မှု**

w0 = 1.0၊ gradient သည် step တိုင်းတွင် 0.2 ဟု ကိန်းသေ ထားသည်၊ lr = 0.1၊ weight decay = 0.01၊
step 50။ (က) weight decay မပါဘဲ w၊ (ခ) L2 penalty ကို gradient အတွင်း ထည့်ပါက w၊
(ဂ) decoupled ဖြစ်ပါက w၊ ထို နှစ်ခု၏ ကွာခြားမှု၊ (ဃ) တူညီသည့် ဆက်တင်ကို Adam ဖြင့်
(adam_l2 နှင့် decoupled) လုပ်ပါက w နှစ်ခုနှင့် ကွာခြားမှု၊ (င) SGD တွင် တူညီပြီး Adam တွင်
မတူညီသည့် အကြောင်းရင်း၊ (စ) wd 0.0၊ 0.01၊ 0.05၊ 0.1 တို့အတွက် lr 3e-4 ဖြင့် step 10,000
ပြီးနောက် ကျန်သည့် weight အချိုး။ → `labs/lab_gradient_step.py` (update များကို ကြည့်ပါ) + ဤဖိုင်၏ Python block

**လေ့ကျင့်ခန်း ၆ — batch နှင့် model တစ်ခုအတွက် memory**

parameter 1.3 B၊ d_model 2048၊ block 24 ခု၊ sequence 2048၊ batch 32၊ layer တစ်ခုလျှင် activation
tensor 12 ခု။ weight fp16၊ master နှင့် gradient fp32၊ AdamW state fp32။ (က) weight (fp16)၊
(ခ) master weight၊ gradient နှင့် optimizer state ၏ GiB နှင့် optimizer side စုစုပေါင်း၊
(ဂ) activation GiB နှင့် sample တစ်ခုလျှင် GiB၊ (ဃ) checkpointing ပါက activation GiB နှင့်
စုစုပေါင်း၊ (င) activation ၏ share ရာခိုင်နှုန်း၊ (စ) micro-batch 8 ဖြင့် checkpointing မပါဘဲ
နှင့် ပါဘဲ စုစုပေါင်း GiB။ → `labs/lab_memory.py --sweep`

## ၃။ ပြဿနာ ရှာဖွေခြင်း (Troubleshooting Scenarios)

ပြဿနာ တစ်ခုစီကို symptom၊ တိုင်းတာရမည့် အချက်၊ ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်)၊
ဖြေရှင်းနည်းနှင့် ရှင်းလင်းသည့် term ဟူသည့် အစဉ်အတိုင်း ဖော်ပြထားသည်။ အကြောင်းရင်း အစဉ်သည်
တိုင်းတာမှုဖြင့် ရှာဖွေနိုင်သည့် အစဉ်အတိုင်း ဖြစ်သည်။ အသေးစိတ် ရှင်းလင်းချက်ကို အပိုင်း ၅.၂ တွင်
ပေးထားသည်။

### ပြဿနာ ၁ — loss သည် NaN ဖြစ်သွားသည်

- **Symptom —** ပထမ step များ ပုံမှန် ဖြစ်သည်၊ ရုတ်တရက် loss သည် `nan` ဖြစ်ပြီး ထိုနောက် weight
  အားလုံး `nan` ဖြစ်သွားသည်၊ training သည် ပြန်မထူနိုင်တော့ပါ။
- **တိုင်းတာရမည့် အချက် —** ပထမဆုံး non-finite tensor သည် မည်သည့် operation တွင် ဖြစ်သနည်း၊
  ထို step မတိုင်မီ gradient norm နှင့် update ၏ အရွယ်အစား၊ learning rate နှင့် schedule အဆင့်၊
  dtype (fp16/logit range)၊ loss scale ၏ တန်ဖိုး၊ normalization တွင် variance သုည ဖြစ်မှု ရှိမရှိ။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) learning rate ကြီးလွန်း၍ update ပြန့်ထွက်ခြင်း
  (ဥပမာ — lr 1.1 တွင် step ၈ အတွင်း 10.17 ရောက်သည်၊ fp16 တွင် step 28 ၌ loss non-finite ဖြစ်သည်)၊
  (၂) fp16 ၏ range ကျော်လွန်ခြင်း (fp16 အမြင့်ဆုံး ≈ 65504၊ fp32 ≈ 3.4e38 — တူညီသည့် အစီအစဉ်တွင်
  fp32 နောက်ကျသည်)၊ (၃) loss scale ကို unscale မလုပ်ဘဲ clip လုပ်ခြင်း၊ (၄) normalization တွင်
  သုည ဖြင့် စားခြင်း၊ (၅) အစောပိုင်း ပျက်စီးနေသည့် တန်ဖိုး တစ်ခုမှ ဆင်းသက်လာခြင်း။
- **ဖြေရှင်းနည်း —** ပထမဆုံး non-finite tensor ကို ရှာပြီး ၎င်း၏ input များကို စစ်ရမည်၊ ထို
  operation အနီးတွင် assertion သို့မဟုတ် anomaly detection ထည့်ရမည်၊ learning rate ကို လျှော့ပြီး
  `Warmup` ထည့်ရမည်၊ global norm ဖြင့် `Gradient Clipping` လုပ်ရမည်၊ loss scale ကို unscale
  ပြီးမှ clip လုပ်ရမည်။
- **ရှင်းလင်းသည့် term —** NaN (Not a Number)၊ Mixed Precision၊ Gradient Clipping၊ Learning Rate၊
  Warmup၊ Normalization။

### ပြဿနာ ၂ — loss သည် အစောပိုင်းတွင် ရပ်တန့်သည် (plateau)

- **Symptom —** loss သည် ပထမ epoch များတွင် သိသိသာသာ ကျသည်၊ ထို့နောက် တန်ဖိုး တစ်ခုတွင်
  လုံးဝ မကျတော့ဘဲ ရပ်နေသည်၊ သို့မဟုတ် အလွန်နှေးစွာ ကျသည်။
- **တိုင်းတာရမည့် အချက် —** loss ရပ်သည့် တန်ဖိုးသည် uniform prediction ၏ တန်ဖိုး ဖြစ်နေသလား
  (class 10 ခုအတွက် 2.302585၊ vocabulary 32000 အတွက် 10.373491)၊ learning rate ၏ တကယ့် တန်ဖိုး
  (schedule ၏ peak မဟုတ်၊ step တိုင်း၏ တန်ဖိုး)၊ warmup အရှည်၊ gradient norm (သုညနီးပါး ဖြစ်နေသလား)၊
  ReLU unit များ ရပ်နေမှု၊ data နှင့် label အရည်အသွေး၊ regularization coefficient ကြီးလွန်းမှု။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) learning rate သေးလွန်း၍ update အလွန်နည်းခြင်း
  (lr 0.05 ဖြင့် step ၅ အတွင်း 1.819 ရောက်သည်၊ lr 0.1 ဖြင့် 2.3446 ရောက်သည် — ကွာခြားမှု ရှိသည်)၊
  (၂) warmup ရှည်လွန်း၍ အစောပိုင်း step အရေအတွက် အလဟသ ဖြစ်ခြင်း၊ (၃) gradient သုည ဖြစ်သည့်
  unit များ (ReLU ၏ negative ဘက်)၊ (၄) capacity သို့မဟုတ် feature မလုံလောက်မှု (underfitting)၊
  (၅) weight decay သို့မဟုတ် dropout ကြီးလွန်း၍ အသုံးဝင်သည့် signal ပါ ကျုံ့ခံရခြင်း။
- **ဖြေရှင်းနည်း —** step တိုင်း၏ တကယ့် learning rate ကို log မှတ်ရမည်၊ warmup ကို step ယူနစ်ဖြင့်
  သတ်မှတ်ရမည်၊ gradient norm ကို တိုင်းရမည်၊ gradient သုည ဖြစ်နေပါက activation function ကို
  စစ်ရမည်၊ ထို့နောက်မှ capacity နှင့် regularization ကို ချိန်ညှိရမည်။
- **ရှင်းလင်းသည့် term —** Learning Rate Schedule၊ Learning Rate၊ Warmup၊ ReLU၊ Activation Function၊
  Underfitting၊ Weight Decay၊ Dropout။

### ပြဿနာ ၃ — train နှင့် validation ကွဲထွက်သည်

- **Symptom —** training metric သည် ဆက်လက် တိုးတက်နေသည်၊ သို့သော် held-out metric သည်
  ပြန်၍ ဆိုးလာသည်၊ ကွာဟမှု (gap) သည် epoch တိုင်းတွင် ကြီးလာသည်။
- **တိုင်းတာရမည့် အချက် —** training loss နှင့် held-out loss ကို epoch တိုင်း၊ ကွာဟမှု၏ အချိုး
  (held-out / training)၊ subgroup အလိုက် ကျရှုံးမှု၊ epoch အရေအတွက်နှင့် ပြီးဆုံးသည့် step၊
  data leakage ရှိမရှိ၊ data augmentation ၏ transformation သည် task signal ကို ထိန်းသလား။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) epoch များလွန်း၍ memorization ဖြစ်ခြင်း၊
  (၂) regularization မလုံလောက်ခြင်း၊ (၃) training data သည် held-out data ကို ကိုယ်စားမပြုခြင်း
  (distribution ကွာခြားမှု)၊ (၄) validation split တွင် leakage ရှိခြင်း၊ (၅) augmentation သည်
  label ကို ပျက်စီးစေခြင်း။
- **ဖြေရှင်းနည်း —** held-out metric ဖြင့် early stopping သတ်မှတ်ရမည်၊ `Weight Decay`၊ `Dropout`
  နှင့် `Data Augmentation` ကို တစ်ခုချင်း စမ်းရမည်၊ subgroup များကို စစ်ရမည်၊ data အရည်အသွေးကို
  အရင် စစ်ရမည်။
- **ရှင်းလင်းသည့် term —** Overfitting၊ Weight Decay၊ Dropout၊ Data Augmentation၊ Epoch၊
  Loss Function။

## ၄။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်းများ (Design Decisions)

### ဆုံးဖြတ်ချက် ၁ — memory ကန့်သတ်ချက်အောက်တွင် batch နှင့် learning rate ကို ရွေးချယ်ခြင်း

**အခြေအနေ —** parameter 350 M model တစ်ခုကို sequence 1024 ဖြင့် train လုပ်မည်။ device တွင်
အသုံးပြုနိုင်သည့် memory 24.0 GiB ရှိသည်။ ရည်မှန်းသည့် effective batch သည် 64 ဖြစ်သည်။
effective batch 32 တွင် peak learning rate 3e-4 ဖြင့် ကောင်းသည့် ရလဒ် ရရှိထားသည်။
ရွေးချယ်စရာ သုံးခု ရှိသည် — (က) micro 16 × accum 4 (checkpointing မပါ)၊ (ခ) micro 64 × accum 1
(checkpointing ပါ)၊ (ဂ) micro 16 × accum 4 (checkpointing ပါ)။

**trade-off —** (က) သည် step အချိန် အနည်းဆုံး ဖြစ်သော်လည်း activation 9.0 GiB ယူသဖြင့်
ကျန်သည့် နေရာ ကျဉ်းသည်။ (ခ) သည် memory အသက်သာဆုံး ဖြစ်သော်လည်း activation 1.5 GiB ဖြစ်သည့်တိုင်
step အချိန်သည် 33.33 % တိုးသည်။ (ဂ) သည် memory 1.5 GiB ဖြစ်ပြီး (က) နှင့် တူညီသည့် micro-batch
ဖြစ်သဖြင့် step အရေအတွက်လည်း တူညီသည်။

**ဆုံးဖြတ်ချက် —** (ဂ) ကို ရွေးရမည်၊ အကြောင်းမှာ optimizer side 5.867 GiB အပေါ် activation 1.5 GiB
ထပ်ထည့်ပါက 7.367 GiB သာ ဖြစ်သဖြင့် ကျန်သည့် နေရာသည် activation memory ၏ လှိုင်းလုံးများအတွက်
လုံလောက်သည်။ learning rate ကို effective batch 64 အတွက် **linear rule** ဖြင့် 6.0e-4၊ **sqrt rule**
ဖြင့် 4.24e-4 ရရှိသည်။ ရှေးဦး run တွင် sqrt rule (4.24e-4) ဖြင့် စ၍ gradient norm နှင့် held-out
metric ကို တိုင်းရမည်။ warmup ကို optimizer step 200 ဟု သတ်မှတ်ပါက micro-step 800 ဖြစ်သည်။

**တိုင်းတာမည့် metric —** step တစ်ကြိမ်၏ အချိန်၊ peak memory အသုံးပြုမှု GiB၊ တူညီသည့် token
budget တွင် held-out loss၊ gradient norm ၏ p99။

### ဆုံးဖြတ်ချက် ၂ — generalization gap အတွက် regularization ကို ချိန်ညှိခြင်း

**အခြေအနေ —** epoch ၃ တွင် training loss 0.42၊ held-out loss 0.98 ဖြစ်သည် (gap 0.56၊ အချိုး 2.333)။
learning rate 3e-4၊ step စုစုပေါင်း 10,000၊ dropout မပါ၊ weight decay မပါ၊ augmentation မပါ။
ရွေးချယ်စရာ နှစ်ခု ရှိသည် — (က) dropout 0.1 ကို ထည့်၍ weight decay 0.1 ဖြင့် ထားသည်၊
(ခ) dropout 0.1 + weight decay 0.05 + data augmentation ကို အနည်းငယ် ထည့်သည်။

**trade-off —** (က) တွင် weight decay 0.1 ဖြင့် step 10,000 ပြီးနောက် weight ၏ 74.1 % သာ ကျန်သည် —
ဆိုလိုသည်မှာ 25.9 % ကျုံ့သည်၊ အသုံးဝင်သည့် coefficient များပါ ဆုံးရှုံးနိုင်သည်။ (ခ) တွင် 86.1 % ကျန်သည်
(13.9 % ကျုံ့သည်)၊ ထို့ကြောင့် သင်ယူထားသည့် signal ကို ထိန်းပြီး gap ကို လျှော့သည့် အစီအစဉ် ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** (ခ) ကို ရွေးရမည်။ ဤ အစီအစဉ်ဖြင့် တိုင်းတာရရှိသည့် ရလဒ်မှာ training loss 0.51၊
held-out loss 0.71 ဖြစ်သည် ဟု ယူဆပါက gap သည် 0.20 သို့ ကျဆင်းသည် (held-out loss 27.55 % ကျသည်၊
gap 64.29 % ကျဉ်းသည်၊ training loss 21.43 % တက်သည်။) ဤအခြေအနေတွင် gap ကျဉ်းမှုသည် ရရှိသည့်
အကျိုးအမြတ် ဖြစ်ပြီး training loss တက်မှုသည် အလုပ်အမြှောက် ဖြစ်သည်။ weight decay ကို 0.05 အထက်
တင်ခြင်းသည် (က) ၏ အန္တရာယ်သို့ ပြန်ရောက်သည်။

**တိုင်းတာမည့် metric —** held-out loss နှင့် training loss ၏ အချိုး၊ gap ၏ ကျဉ်းမှု ရာခိုင်နှုန်း၊
subgroup အလိုက် ကျရှုံးမှု၊ epoch အလိုက် held-out loss ၏ အနိမ့်ဆုံးအမှတ် (early stopping ၏ နေရာ)။

## ၅။ အဖြေများ (Answers with Explanations)

### ၅.၁ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း အဖြေများ

#### အဖြေ ၁ — softmax နှင့် cross-entropy

**ဖော်မြူလာ —** p_i = exp(z_i) / Σ exp(z_j)၊ loss = -log(p_target)၊ dL/dz_i = p_i - onehot_i။
**ယူဆချက် —** logits = [1.0, 2.0, 3.0]၊ target index = 0၊ ဤ logits များသည် ပြန့်ထွက်မှု မရှိသဖြင့်
stabilization မပါဘဲ တွက်နိုင်သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. exp တန်ဖိုးများ = [2.718282, 7.389056, 20.085537]၊ ပေါင်းလဒ် = 30.192875 ဖြစ်သည်။
2. softmax = [0.090031, 0.244728, 0.665241] ဖြစ်သည်၊ ပေါင်းလဒ် = 1.0 ဖြစ်သည်။
3. -ln(0.090031) = 2.407606 nats = 3.473441 bits ဖြစ်သည်။
4. perplexity = exp(2.407606) = 11.107338 ဖြစ်သည်။
5. gradient = [0.090031 - 1, 0.244728, 0.665241] = [-0.909969, 0.244728, 0.665241] ဖြစ်သည်၊
   ပေါင်းလဒ် = 0 ဖြစ်သည်။
6. logits = [1000, 1001] ဖြစ်ပါက stabilization မပါဘဲ `math.exp(1000)` သည် overflow ဖြစ်သည်
   (Python တွင် `math range error`၊ ကိန်းဂဏန်း library အများစုတွင် `inf` ဖြစ်ပြီး ထို့နောက် `inf/inf`
   မှ NaN ဖြစ်သည်။) max နုတ်ပါက exp([-1, 0]) = [0.367879, 1.0] ဖြစ်သဖြင့် probability =
   [0.268941, 0.731059] ကို တိကျစွာ ရသည်။

**အဓိပ္ပာယ် —** cross-entropy သည် ရည်မှန်း token ၏ probability ၏ log ပေါ်တွင် မှီခိုသဖြင့်၊
probability သေးလာသည့်အလိုက် loss သည် အကန့်အသတ် မရှိ တိုးသည်။ ဤအချက်သည် NaN ဖြစ်ပေါ်မှုနှင့်
တိုက်ရိုက် ဆက်စပ်သည် — logits သည် ကြီးလွန်းပါက exponentiation ကို stabilization မလုပ်ဘဲ
တွက်မိသည်။

```bash
python3 - <<'PY'
import math
z, target = [1.0, 2.0, 3.0], 0
e = [math.exp(v) for v in z]
p = [v / sum(e) for v in e]
ce = -math.log(p[target])
print("exp   ", [round(v, 6) for v in e], "sum", round(sum(e), 6))
print("softmax", [round(v, 6) for v in p], "sum", round(sum(p), 6))
print("CE nats", round(ce, 6), "bits", round(ce / math.log(2), 6), "ppl", round(math.exp(ce), 6))
print("grad  ", [round(pi - (1.0 if i == target else 0.0), 6) for i, pi in enumerate(p)])
m = max([1000.0, 1001.0])
st = [math.exp(v - m) for v in [1000.0, 1001.0]]
print("stabilised [1000,1001]:", [round(v / sum(st), 6) for v in st])
PY
```

```text
exp    [2.718282, 7.389056, 20.085537] sum 30.192875
softmax [0.090031, 0.244728, 0.665241] sum 1.0
CE nats 2.407606 bits 3.473441 ppl 11.107338
grad   [-0.909969, 0.244728, 0.665241]
stabilised [1000,1001]: [0.268941, 0.731059]
```

#### အဖြေ ၂ — function ငယ်တစ်ခု၏ gradient

**ဖော်မြူလာ —** chain rule — dL/dW1 = (dL/dh_pre) ⊗ x၊ dL/dh_pre = dL/dh × relu'(h_pre)။
**ယူဆချက် —** x = [1.0, 2.0]၊ W1 ၏ အတန်း ၁ = [0.5, -0.5] (bias 0.0)၊ အတန်း ၂ = [1.0, 0.25]
(bias -0.5)၊ w2 = [1.0, -2.0]၊ b2 = 0.0၊ loss = 0.5 (z - 1)²။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. h_pre = [0.5 - 1.0 + 0.0, 1.0 + 0.5 - 0.5] = [-0.5, 1.0] ဖြစ်သည်။
2. h = relu(h_pre) = [0.0, 1.0] ဖြစ်သည်၊ ဆိုလိုသည်မှာ ပထမ unit ပိတ်နေသည်။
3. z = 1.0 × 0.0 + (-2.0) × 1.0 + 0.0 = -2.0 ဖြစ်သည်။
4. loss = 0.5 × (-2.0 - 1.0)² = 4.5 ဖြစ်သည်။
5. dL/dz = z - 1 = -3.0 ဖြစ်သည်။
6. dL/dw2 = dL/dz × h = [0.0, -3.0]၊ dL/db2 = -3.0 ဖြစ်သည်။
7. dL/dh = dL/dz × w2 = [-3.0, 6.0] ဖြစ်သည်။
8. relu'(h_pre) = [0.0, 1.0] (h_pre သည် 0 ဖြစ်သော အခါ 0 ဟု သတ်မှတ်သည်)၊ ထို့ကြောင့်
   dL/dh_pre = [0.0, 6.0] ဖြစ်သည်။
9. dL/dW1 = [[0.0 × 1.0, 0.0 × 2.0], [6.0 × 1.0, 6.0 × 2.0]] = [[0.0, 0.0], [6.0, 12.0]] ဖြစ်သည်၊
   dL/db1 = [0.0, 6.0] ဖြစ်သည်။
10. finite difference ဖြင့် dL/dw2[0] = 0.0 ရသည်၊ analytic တန်ဖိုး 0.0 နှင့် တူညီသည်။
11. learning rate 0.1 ဖြင့် update တစ်ကြိမ် ပြီးနောက် w2 = [1.0, -1.7]၊ W1 ၏ အတန်း ၂ =
    [0.4, -0.95]၊ W1 ၏ အတန်း ၁ = [0.5, -0.5] (မပြောင်းလဲပါ)၊ loss = 0.245 ဖြစ်သည်။

**အဓိပ္ပာယ် —** ReLU ပိတ်နေသည့် unit ၏ gradient သည် သုည ဖြစ်သဖြင့် ထို unit သို့ သွားသည့်
parameter အားလုံး မပြောင်းလဲပါ။ ဤအချက်သည် "loss မကျခြင်း" ၏ အကြောင်းရင်း တစ်ခု ဖြစ်နိုင်သည်၊
သို့သော် ဤဥပမာတွင် loss သည် 4.5 မှ 0.245 သို့ ကျသဖြင့် ကျန်သည့် unit က သင်ယူနိုင်ဆဲ ဖြစ်သည်။

```bash
python3 - <<'PY'
x = [1.0, 2.0]
W1, b1, w2, b2 = [[0.5, -0.5], [1.0, 0.25]], [0.0, -0.5], [1.0, -2.0], 0.0
def fwd(W1, b1, w2, b2):
    hp = [W1[i][0] * x[0] + W1[i][1] * x[1] + b1[i] for i in range(2)]
    h = [max(0.0, v) for v in hp]
    z = w2[0] * h[0] + w2[1] * h[1] + b2
    return hp, h, z, 0.5 * (z - 1.0) ** 2
hp, h, z, loss = fwd(W1, b1, w2, b2)
dl_dz = z - 1.0
dl_dw2 = [dl_dz * hi for hi in h]
dl_dh = [dl_dz * w2[j] for j in range(2)]
drelu = [1.0 if v > 0 else 0.0 for v in hp]
dl_dhp = [dl_dh[j] * drelu[j] for j in range(2)]
dl_dW1 = [[dl_dhp[i] * x[j] for j in range(2)] for i in range(2)]
print("h_pre", hp, "h", h, "z", z, "loss", loss)
print("dL/dz", dl_dz, "dL/dw2", dl_dw2, "dL/db2", dl_dz)
print("dL/dh", dl_dh, "relu'", drelu, "dL/dh_pre", dl_dhp)
print("dL/dW1", dl_dW1)
lr = 0.1
W1n = [[W1[i][j] - lr * dl_dW1[i][j] for j in range(2)] for i in range(2)]
b1n = [b1[i] - lr * dl_dhp[i] for i in range(2)]
w2n = [w2[i] - lr * dl_dw2[i] for i in range(2)]
b2n = b2 - lr * dl_dz
print("w2 after", w2n, "W1 row2 after", W1n[1], "W1 row1 after", W1n[0])
print("loss after", round(fwd(W1n, b1n, w2n, b2n)[3], 4))
eps = 1e-6
fd = (fwd(W1, b1, [w2[0] + eps, w2[1]], b2)[3] - loss) / eps
print("finite diff dL/dw2[0]", round(fd, 6))
PY
```

```text
h_pre [-0.5, 1.0] h [0.0, 1.0] z -2.0 loss 4.5
dL/dz -3.0 dL/dw2 [-0.0, -3.0] dL/db2 -3.0
dL/dh [-3.0, 6.0] relu' [0.0, 1.0] dL/dh_pre [-0.0, 6.0]
dL/dW1 [[-0.0, -0.0], [6.0, 12.0]]
w2 after [1.0, -1.7] W1 row2 after [0.3999999999999999, -0.9500000000000002] W1 row1 after [0.5, -0.5]
loss after 0.245
finite diff dL/dw2[0] 0.0
```

#### အဖြေ ၃ — optimizer step တစ်ကြိမ်

**ဖော်မြူလာ —** SGD: w ← w - lr g၊ momentum: v ← μv + g ထို့နောက် w ← w - lr v၊
Adam: m̂ = m/(1-β₁ᵗ)၊ v̂ = v/(1-β₂ᵗ)၊ w ← w - lr m̂/(√v̂ + ε)။
**ယူဆချက် —** L(w) = (w - 3)²၊ gradient = 2(w - 3)၊ w0 = 5.0၊ ထို့ကြောင့် gradient = 4.0၊
μ = 0.9၊ β₁ = 0.9၊ β₂ = 0.999၊ ε = 1e-8။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. SGD (lr 0.2): w1 = 5.0 - 0.2 × 4.0 = 4.2၊ w2 = 4.2 - 0.2 × 2.4 = 3.72၊ w3 = 3.72 - 0.2 × 1.44 = 3.432 ဖြစ်သည်။
2. momentum (lr 0.2): v1 = 4.0၊ w1 = 4.2၊ v2 = 0.9 × 4.0 + 2.4 = 6.0၊ w2 = 4.2 - 1.2 = 3.0၊
   v3 = 0.9 × 6.0 + 0.0 = 5.4၊ w3 = 3.0 - 1.08 = 1.92 ဖြစ်သည်။
3. step ၂ တွင် w = 3.0 (အနိမ့်ဆုံးအမှတ်) ရောက်ပြီး step ၃ တွင် 1.92 သို့ **ကျော်လွန်** သည်။
4. Adam (lr 0.05): m1 = 0.4၊ v1 = 0.001 × 16 = 0.016၊ m̂1 = 0.4/(1-0.9) = 4.0၊
   v̂1 = 0.016/(1-0.999) = 16.0၊ √v̂ = 4.0၊ update = 0.05 × 4.0/4.0 = 0.05၊ ထို့ကြောင့် w1 = 4.95 ဖြစ်သည်။
   ထို့နောက် w2 = 4.9၊ w3 = 4.8501 ဖြစ်သည်။
5. ပထမ step တွင် m̂/√v̂ = g/|g| = 1 ဖြစ်သဖြင့် Adam ၏ update သည် learning rate နှင့် ညီမျှသည်။
   ဤအချက်သည် "Adam သည် learning rate 0.05 ဖြင့် step တစ်ကြိမ်လျှင် 0.05 သာ ရွှေ့သည်" ဟု
   ဆိုနိုင်သည့် အကြောင်းရင်း ဖြစ်သည်။
6. lr 1.1 ဖြင့် SGD — w0 = 5.0 မှ စပါက [0.6, 5.88, -0.456, 7.1472, -1.9766, 8.972, -4.1664, 11.5996]
   ဖြစ်သည်၊ w0 = 1.0 မှ စပါက [5.4, 0.12, 6.456, -1.1472, 7.9766, -2.972, 10.1664, -5.5996] ဖြစ်သည်။
   နှစ်ခုလုံးတွင် step တိုင်း၏ အရွယ်အစားသည် 1.2 အချိုးဖြင့် တိုးနေသည်၊ ဆိုလိုသည်မှာ ပြန့်ထွက်ခြင်း
   ဖြစ်သည်။

**အဓိပ္ပာယ် —** optimizer တစ်ခုစီ၏ bias correction၊ momentum accumulation နှင့် overshoot ကို
ကိန်းဂဏန်းဖြင့် မြင်နိုင်သည်။ ဤအချက်များသည် "loss မကျခြင်း" နှင့် "မတည်ငြိမ်ခြင်း" ကို ခွဲခြားရန်
အခြေခံ ဖြစ်သည်။

```bash
python3 - <<'PY'
import math
g = lambda w: 2.0 * (w - 3.0)
def sgd(w, lr, n, mu=0.0):
    v, out = 0.0, []
    for _ in range(n):
        v = mu * v + g(w); w = w - lr * v; out.append(w)
    return out
def adam(w, lr, n):
    m = v = 0.0; out = []
    for t in range(1, n + 1):
        gg = g(w); m = 0.9 * m + 0.1 * gg; v = 0.999 * v + 0.001 * gg * gg
        out.append(w - lr * (m / (1 - 0.9 ** t)) / (math.sqrt(v / (1 - 0.999 ** t)) + 1e-8))
        w = out[-1]
    return out
print("grad at 5.0     ", g(5.0))
print("sgd lr 0.2      ", [round(x, 4) for x in sgd(5.0, 0.2, 3)])
print("momentum 0.9    ", [round(x, 4) for x in sgd(5.0, 0.2, 3, mu=0.9)])
print("adam lr 0.05    ", [round(x, 4) for x in adam(5.0, 0.05, 3)])
print("adam vhat       ", round(0.016 / (1 - 0.999), 4))
print("lr 1.1 from 5.0 ", [round(x, 4) for x in sgd(5.0, 1.1, 8)])
print("lr 1.1 from 1.0 ", [round(x, 4) for x in sgd(1.0, 1.1, 8)])
PY
```

```text
grad at 5.0      4.0
sgd lr 0.2       [4.2, 3.72, 3.432]
momentum 0.9     [4.2, 3.0, 1.92]
adam lr 0.05     [4.95, 4.9, 4.8501]
adam vhat        16.0
lr 1.1 from 5.0  [0.6, 5.88, -0.456, 7.1472, -1.9766, 8.972, -4.1664, 11.5996]
lr 1.1 from 1.0  [5.4, 0.12, 6.456, -1.1472, 7.9766, -2.972, 10.1664, -5.5996]
```

#### အဖြေ ၄ — learning rate schedule တန်ဖိုး

**ဖော်မြူလာ —** t သေး warmup ဖြစ်ပါက lr(t) = peak × t/warmup။
မဟုတ်ပါက lr(t) = peak × (floor + (1 - floor) × 0.5 × (1 + cos(π (t - warmup)/(total - warmup)))
**ယူဆချက် —** warmup = 400 step၊ peak = 6e-4၊ total = 5000 step၊ floor = 0.05 (peak ၏ 5 %)။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. step 100 = 6e-4 × 100/400 = 1.5e-4 (peak ၏ 25 %)၊ step 200 = 3.0e-4 (50 %)၊
   step 399 = 5.985e-4 (99.75 %)၊ step 400 = 6.0e-4 (100 %) ဖြစ်သည်။
2. step 1000 တွင် (t - 400)/4600 = 0.130435 ဖြစ်သဖြင့် lr = 5.7641e-4 (peak ၏ 96.07 %) ဖြစ်သည်။
3. step 2500 တွင် 3.5381e-4 (58.97 %) ဖြစ်သည်။
4. decay ၏ အလယ်အမှတ် step 2700 တွင် cos(π/2) = 0 ဖြစ်သဖြင့် lr = peak × (0.05 + 0.475) = 3.15e-4
   ဖြစ်သည်။
5. step 4000 တွင် 9.392e-5 (15.65 %)၊ step 5000 တွင် floor 3.0e-5 (5 %) ဖြစ်သည်။
6. ပျမ်းမျှ rate = 3.138e-4 = peak ၏ 52.3 % ဖြစ်သည်။
7. batch 32 နှင့် sequence 1024 ဖြင့် warmup 400 step = 400 × 32 × 1024 = 13,107,200 token ဖြစ်သည်။

**အဓိပ္ပာယ် —** schedule တစ်ခုကို နှိုင်းယှဉ်သည့်အခါ peak တန်ဖိုးဖြင့် နှိုင်းယှဉ်ခြင်းသည်
အမှားဖြစ်စေသည်၊ အကြောင်းမှာ ပျမ်းမျှ rate သည် peak ၏ 52.3 % သာ ဖြစ်သည်။ schedule တိုင်းတွင်
ပျမ်းမျှ rate နှင့် ပြီးဆုံးသည့် rate (floor) ကို အတူ တိုင်းရမည်။

```bash
python3 - <<'PY'
import math
warm, peak, total, floor = 400, 6e-4, 5000, 0.05
def lr_at(t):
    if t < warm:
        return peak * t / warm
    prog = (t - warm) / (total - warm)
    return peak * (floor + (1 - floor) * 0.5 * (1 + math.cos(math.pi * prog)))
for t in (100, 200, 399, 400, 1000, 2500, 4000, 5000):
    print(f"step {t:5d} lr {lr_at(t):.8f} share {lr_at(t)/peak:.6f}")
print("midpoint step 2700 lr", round(lr_at(2700), 8))
avg = sum(lr_at(t) for t in range(total)) / total
print("average lr", round(avg, 8), "share", round(avg / peak, 6))
print("warmup tokens", 400 * 32 * 1024)
PY
```

```text
step   100 lr 0.00015000 share 0.250000
step   200 lr 0.00030000 share 0.500000
step   399 lr 0.00059850 share 0.997500
step   400 lr 0.00060000 share 1.000000
step  1000 lr 0.00057641 share 0.960675
step  2500 lr 0.00035381 share 0.589679
step  4000 lr 0.00009392 share 0.156537
step  5000 lr 0.00003000 share 0.050000
midpoint step 2700 lr 0.000315
average lr 0.0003138 share 0.522995
warmup tokens 13107200
```

#### အဖြေ ၅ — weight decay ၏ အကျိုးသက်ရောက်မှု

**ဖော်မြူလာ —** L2 ကို gradient အတွင်း — g_eff = g + wd × w၊ ထို့နောက် w ← w - lr g_eff။
Decoupled — w ← w - lr g၊ ထို့နောက် w ← w - lr × wd × w။
**ယူဆချက် —** w0 = 1.0၊ gradient = 0.2 (ကိန်းသေ)၊ lr = 0.1၊ wd = 0.01၊ step = 50။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. wd မပါဘဲ SGD: w50 = 1.0 - 50 × 0.1 × 0.2 = 0.0 ဖြစ်သည် (ရလဒ် -0.000000)။
2. L2 ကို gradient အတွင်း ထည့်ပါက w50 = -0.024682 ဖြစ်သည်၊ decoupled ဖြစ်ပါက လည်း
   -0.024682 ဖြစ်သည်၊ ကွာခြားမှုသည် 2.19e-16 သာ ဖြစ်သည် (floating-point အဝိုင်းချုပ်မှု
   အတွင်း သုည ဖြစ်သည်။)
3. Adam ဖြင့် — L2-in-gradient ၏ w50 = -3.842787၊ decoupled (AdamW) ၏ w50 = -3.923352 ဖြစ်သည်၊
   ကွာခြားမှု = 0.080565 ဖြစ်သည်။
4. step တစ်ကြိမ်၏ decay factor = 1 - lr × wd = 0.999၊ step 50 ပြီးနောက် 0.951206 ဖြစ်သည်။
5. lr 3e-4 နှင့် step 10,000 အတွက် — wd 0.0 ဖြင့် 1.000000၊ 0.01 ဖြင့် 0.970445၊ 0.05 ဖြင့်
   0.860707၊ 0.1 ဖြင့် 0.740815 ဖြစ်သည်။
6. SGD တွင် တူညီပြီး Adam တွင် မတူညီရသည့် အကြောင်းရင်းမှာ Adam သည် gradient ကို squared
   gradient ၏ exponential average ဖြင့် စားသဖြင့်၊ gradient အတွင်း ထည့်သည့် L2 penalty သည်လည်း
   ထို adaptive scaling ခံရသည်။ Decoupled ဖြစ်ပါက ကျုံ့ဝင်မှုသည် scaling နှင့် ကင်းကွာသည်။

**အဓိပ္ပာယ် —** wd coefficient ၏ အကျိုးသက်ရောက်မှုကို "step တစ်ကြိမ်စာ ကျုံ့ခြင်း" ဖြင့်
တွက်နိုင်သည် (1 - lr × wd)၊ ထို့ကြောင့် learning rate ပြောင်းလဲပါက ကျုံ့မှုလည်း ပြောင်းလဲသည်။
ထို အချက်သည် schedule ပြီးဆုံးချိန်တွင် weight မည်မျှ ကျန်သည်ကို တွက်ရာတွင် အရေးပါသည်။

```bash
python3 - <<'PY'
import math
w0, lr, steps, wd = 1.0, 0.1, 50, 0.01
def run(kind, w=w0, n=steps):
    m = v = 0.0
    for t in range(1, n + 1):
        g = 0.2
        if kind == "sgd_none":
            w = w - lr * g
        elif kind == "sgd_l2":
            w = w - lr * (g + wd * w)
        elif kind == "sgd_decoupled":
            w = w - lr * g - lr * wd * w
        else:
            if kind == "adam_l2":
                g = g + wd * w
            m = 0.9 * m + 0.1 * g; v = 0.999 * v + 0.001 * g * g
            w = w - lr * (m / (1 - 0.9 ** t)) / (math.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
            if kind == "adam_decoupled":
                w = w - lr * wd * w
    return w
for k in ("sgd_none", "sgd_l2", "sgd_decoupled", "adam_l2", "adam_decoupled"):
    print(f"{k:16s} {run(k):.6f}")
print("sgd difference  ", run("sgd_l2") - run("sgd_decoupled"))
print("adam difference ", round(run("adam_l2") - run("adam_decoupled"), 6))
for w in (0.0, 0.01, 0.05, 0.1):
    print(f"wd {w:4.2f} weight left after 10k steps {(1 - 3e-4 * w) ** 10000:.6f}")
PY
```

```text
sgd_none         -0.000000
sgd_l2           -0.024682
sgd_decoupled    -0.024682
adam_l2          -3.842787
adam_decoupled   -3.923352
sgd difference   2.185751579730777e-16
adam difference  0.080565
wd 0.00 weight left after 10k steps 1.000000
wd 0.01 weight left after 10k steps 0.970445
wd 0.05 weight left after 10k steps 0.860707
wd 0.10 weight left after 10k steps 0.740815
```

#### အဖြေ ၆ — batch နှင့် model တစ်ခုအတွက် memory

**ဖော်မြူလာ —** weight(fp16) = parameter × 2၊ master / gradient = parameter × 4၊ AdamW state =
parameter × 8၊ activation = A × sequence × batch × d × 2 × block။
**ယူဆချက် —** parameter 1.3e9၊ d = 2048၊ block 24၊ sequence 2048၊ batch 32၊ A = 12၊
checkpointing ဖြင့် သိမ်းသည့် tensor 2 ခု။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. weight fp16 = 1.3e9 × 2 / 2³⁰ = 2.421 GiB၊ master = 4.843 GiB၊ gradient = 4.843 GiB၊
   AdamW state = 9.686 GiB ဖြစ်သည်။
2. optimizer side စုစုပေါင်း = 21.793 GiB ဖြစ်သည်။
3. activation = 12 × 2048 × 32 × 2048 × 2 × 24 bytes = 72.0 GiB ဖြစ်သည်၊ sample တစ်ခုလျှင်
   2.25 GiB ဖြစ်သည်။
4. စုစုပေါင်း = 93.793 GiB ဖြစ်သည်၊ activation ၏ share = 76.8 % ဖြစ်သည်။
5. checkpointing ပါက activation = 12.0 GiB ဖြစ်သဖြင့် စုစုပေါင်း = 33.793 GiB ဖြစ်သည်
   (69.6 GiB လျော့သည်။)
6. micro-batch 8 ဖြင့် — checkpointing မပါဘဲ စုစုပေါင်း 39.793 GiB၊ ပါဘဲ 24.793 GiB ဖြစ်သည်၊
   ဆိုလိုသည်မှာ 40 GiB device တွင် ပထမရွေးချယ်မှု မဆံ့ဘဲ ဒုတိယရွေးချယ်မှု ဆံ့သည်။

**အဓိပ္ပာယ် —** model အရွယ်အစား တိုးသည့်အလိုက် activation ၏ share သည် 86.0 % မှ 76.8 % သို့
ကျဆင်းသော်လည်း အကြီးဆုံး အစိတ်အပိုင်း အဖြစ် ဆက်လက် ရှိနေသည်။ ထို့ကြောင့် batch ကို
ထိန်းညှိခြင်းနှင့် checkpointing သည် memory ဘတ်ဂျက် သတ်မှတ်ရာတွင် ပထမဦးစားပေး knob များ ဖြစ်သည်။

```bash
python3 - <<'PY'
params, d, layers, seq, batch, A = 1.3e9, 2048, 24, 2048, 32, 12
gib = lambda b: b / 2**30
w16, master, grads, opt = params * 2, params * 4, params * 4, params * 8
side = w16 + master + grads + opt
act = A * seq * batch * d * 2 * layers
act_ck = 2 * seq * batch * d * 2 * layers
print("weights fp16 GiB ", round(gib(w16), 3))
print("master fp32 GiB  ", round(gib(master), 3))
print("grads fp32 GiB   ", round(gib(grads), 3))
print("adamw m,v GiB    ", round(gib(opt), 3))
print("optimizer side   ", round(gib(side), 3))
print("activations GiB  ", round(gib(act), 3))
print("act per sample   ", round(gib(A * seq * d * 2 * layers), 4))
print("act with ckpt    ", round(gib(act_ck), 3))
print("total GiB        ", round(gib(side + act), 3))
print("total with ckpt  ", round(gib(side + act_ck), 3))
print("act share pct    ", round(100 * act / (side + act), 1))
print("micro 8 no ckpt  ", round(gib(side + A * seq * 8 * d * 2 * layers), 3))
print("micro 8 ckpt     ", round(gib(side + 2 * seq * 8 * d * 2 * layers), 3))
PY
```

```text
weights fp16 GiB  2.421
master fp32 GiB   4.843
grads fp32 GiB    4.843
adamw m,v GiB     9.686
optimizer side    21.793
activations GiB   72.0
act per sample    2.25
act with ckpt     12.0
total GiB         93.793
total with ckpt   33.793
act share pct     76.8
micro 8 no ckpt   39.793
micro 8 ckpt      24.793
```

### ၅.၂ ပြဿနာ ရှာဖွေခြင်း အဖြေများ

#### အဖြေ ၁ — loss NaN ဖြစ်ခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** NaN သည် ရလဒ် ဖြစ်သည်၊ အကြောင်းရင်း မဟုတ်ပါ။ ကြီးလွန်းသည့်
learning rate ဖြင့် update သည် ပြန့်ထွက်သည် (lr 1.1 တွင် 1.2 အချိုးဖြင့် တိုးသည်၊ step ၈ တွင်
10.1664 ရောက်သည်)၊ တန်ဖိုး တစ်ခု dtype ၏ အမြင့်ဆုံးကို ကျော်လွန်သည့်အခါ `inf` ဖြစ်သည်၊
`inf - inf` မှ NaN ဖြစ်သည်။ ဤဥပမာ တူညီအစီအစဉ်တွင် fp16 ၏ loss သည် step 28 ၌ non-finite
ဖြစ်ပြီး weight သည် step 56 ၌ NaN ဖြစ်သည်၊ fp32 တွင် step 241 တွင်မှ non-finite ဖြစ်သည်။
ထို့ကြောင့် dtype သည် "မည်မျှ မြန်စွာ ပြိုလဲသည်" ကို ဆုံးဖြတ်သည်၊ "ပြိုလဲမည် ဟုတ်" ကို
မဆုံးဖြတ်ပါ။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** ပထမဆုံး non-finite tensor ကို ရှာပါ (framework တိုင်းတွင် anomaly
detection ရှိသည်)။ ထို operation သည် loss ဖြစ်ပါက exponentiation ၏ input range ကို စစ်ပါ။
gradient norm သည် clip threshold ကို အမြဲ ကျော်နေပါက learning rate သည် ကြီးလွန်းသည်၊
norm သည် သုည အဖြစ်မှ ရုတ်တရက် ကြီးလာပါက data သို့မဟုတ် normalization ကို စစ်ပါ။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** learning rate ကို ထက်ဝက်လျှော့၍ warmup ထည့်ပြီးနောက် gradient
norm ၏ p99 သည် threshold အောက် ရောက်ပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ fp32 တွင် ပြဿနာ
မရှိဘဲ fp16 တွင်သာ ရှိပါက အကြောင်းရင်း (၂) ဖြစ်သည်၊ ထိုအခါ loss scaling နှင့် unscale အစီအစဉ်ကို
စစ်ရမည်။

#### အဖြေ ၂ — loss plateau ဖြစ်ခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** loss ရပ်သည့် တန်ဖိုးသည် uniform prediction ၏ တန်ဖိုးနှင့်
တူညီပါက model သည် distribution ကို လုံးဝ မခွဲခြားရသေးပါ (class 10 ခုအတွက် 2.302585၊
vocabulary 32000 အတွက် 10.373491)။ ဤအခြေအနေတွင် update သည် လုံးဝ မဖြစ်နေခြင်း (gradient သုည၊
ReLU unit များ ရပ်နေခြင်း) သို့မဟုတ် update သည် အလွန်နည်းနေခြင်း (learning rate သေးလွန်းခြင်း၊
warmup ရှည်လွန်းခြင်း) ဖြစ်နိုင်သည်။ lr 0.05 ဖြင့် step ၅ ပြီးနောက် w = 1.819 ဖြစ်ပြီး lr 0.1
ဖြင့် 2.3446 ဖြစ်သည် — ထို့ကြောင့် rate နှစ်ဆ ကွာခြားမှုသည် လမ်းကြောင်းကို တိုက်ရိုက်
သက်ရောက်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** step တိုင်း၏ တကယ့် learning rate ကို log မှတ်ပါ၊ ပထမ step များတွင်
rate သုညနီးပါး ဖြစ်နေပါက warmup ရှည်လွန်းသည် (အကြောင်းရင်း ၂)။ rate ပုံမှန် ဖြစ်သော်လည်း
gradient norm သုညဖြစ်နေပါက dead unit ဖြစ်သည် (အကြောင်းရင်း ၃)။ norm ပုံမှန်ဖြစ်ပြီး loss ရပ်နေပါက
capacity သို့မဟုတ် regularization ကို စစ်ပါ (အကြောင်းရင်း ၄ နှင့် ၅)။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** learning rate ကို တိုး၍ (schedule ရှိပါက peak ကို တင်ခြင်း၊ warmup
ကို တိုခြင်း) loss ကျလာပါက အကြောင်းရင်း (၁) သို့မဟုတ် (၂) ဖြစ်သည်။ activation function ကို
ပြောင်းပြီးနောက် gradient norm တက်လာပါက အကြောင်းရင်း (၃) ဖြစ်သည်။ ဤအဆင့်များ မအောင်မြင်မှ
capacity နှင့် feature ကို စဉ်းစားရမည် — ထို အခြေအနေသည် `Underfitting` ဖြစ်သည်။

#### အဖြေ ၃ — train နှင့် validation ကွဲထွက်ခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** training loss နည်းခြင်းသည် unseen data အပေါ်
စွမ်းဆောင်ရည်ကို အာမမခံပါ။ gap သည် epoch တိုင်းတွင် ကြီးလာပါက model သည် training data ကို
မှတ်မိနေသည် (`Overfitting`)။ ထို အခြေအနေတွင် ရွေးချယ်စရာ နှစ်ခု ရှိသည် — regularization
တိုးခြင်း (dropout၊ weight decay၊ augmentation) နှင့် ပြီးဆုံးသည့် step ကို စောစီးစွာ ရပ်ခြင်း
(early stopping)။ regularization အလွန်အကျွံ တိုးပါက model ၏ signal ပါ ဆုံးရှုံးနိုင်သည် —
wd 0.1 ဖြင့် step 10,000 ပြီးနောက် weight ၏ 74.1 % သာ ကျန်သည်၊ wd 0.05 ဖြင့် 86.1 % ကျန်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** gap ၏ အချိုး (held-out / training) ကို epoch အလိုက် ဆွဲပါ၊
၎င်းသည် တိုးနေပါက regularization ကို တစ်ခုချင်း စမ်းပါ။ augmentation ထည့်ပြီးနောက် gap
ကျဉ်းပါက အကြောင်းရင်း (၂) ဖြစ်သည်၊ အခကြေးငွေ မလျော့ဘဲ gap မပြောင်းပါက data ၏
ကိုယ်စားပြုနိုင်မှုကို စစ်ရမည် (အကြောင်းရင်း ၃)။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** held-out loss ၏ အနိမ့်ဆုံးအမှတ်ကို early stopping အဖြစ်
သတ်မှတ်ပြီး ထို step တွင် ရပ်ပါ။ ထို့နောက် regularization ထည့်ပြီး အနိမ့်ဆုံးအမှတ် ပြန်ကျမှ
(hold-out loss ကောင်းလာမှ) ထို ဆက်တင် လက်ခံရမည်။

### ၅.၃ ဆုံးဖြတ်ချက် အဖြေများ

#### အဖြေ ၁ — batch နှင့် learning rate ရွေးချယ်ခြင်း

**ရှင်းလင်းချက် —** optimizer side memory သည် 5.867 GiB ဖြစ်သည်ဟု အပိုင်း ၁ ဥပမာ ၄ တွင်
တွက်ထားသည်၊ ၎င်းသည် batch အပေါ် မမှီခိုပါ။ activation သည် sample တစ်ခုလျှင် 0.5625 GiB
ဖြစ်သဖြင့် micro 16 တွင် 9.0 GiB (checkpointing မပါ) သို့မဟုတ် 1.5 GiB (ပါ) ဖြစ်သည်။
ထို့ကြောင့် checkpointing သည် 7.5 GiB လျော့ပေးပြီး 33.33 % step အချိန် အပိုကုန်သည်။

**ဆုံးဖြတ်ချက် —** micro 16 × accum 4 ကို checkpointing ဖြင့် ရွေးရမည် — ဤအစီအစဉ်တွင်
ကျန်သည့် နေရာသည် 18.1 GiB ဖြစ်သဖြင့် activation ၏ လှိုင်းလုံးများနှင့် framework overhead အတွက်
လုံလောက်သည်။ learning rate ကို sqrt rule ဖြင့် 4.24e-4 ဖြင့် စတင်ရမည် (linear rule ဖြင့် 6.0e-4 သည်
batch ၂ ဆ တိုးသည့် အချိုးအစား အလွန်တက်သည့်အတွက် ရှေးဦး run ၏ ရလဒ်ကို ဆက်လက် တိုင်းတာရမည်)။
warmup "step 200" ဟု ဆိုပါက micro-step 800 ဖြစ်သည်၊ ရေတွက်သည့် ယူနစ်ကို log တွင် အတိအကျ
မှတ်ရမည်။

**တိုင်းတာမည့် metric —** peak memory (GiB)၊ step တစ်ကြိမ်၏ အချိန်၊ တူညီသည့် token budget တွင်
held-out loss၊ gradient norm ၏ p99။ ဤဆုံးဖြတ်ချက်တွင် memory သည် ကန့်သတ်သည့် အရင်းအမြစ်
ဖြစ်သည်၊ ထို့ကြောင့် ကျန်သည့် နေရာ (headroom) ကို အတိအကျ သတ်မှတ်ရမည်။

#### အဖြေ ၂ — regularization ကို ချိန်ညှိခြင်း

**ရှင်းလင်းချက် —** gap 0.56 (အချိုး 2.333) သည် overfitting ၏ လက္ခဏာ ဖြစ်သည်။ weight decay
တစ်ခုတည်းဖြင့် ပြဿနာ ဖြေရှင်းသည့်အခါ coefficient ကို ကြီးလွန်းထားပါက အသုံးဝင်သည့်
coefficient များပါ ကျုံ့ခံရသည် — wd 0.1 ဖြင့် weight ၏ 25.9 % ဆုံးရှုံးသည်။ ထို့ကြောင့်
coefficient ကို 0.05 တွင် ထား၍ dropout 0.1 နှင့် augmentation ကို ပေါင်းထည့်ခြင်းသည်
ကျုံ့မှုကို ထိန်းပြီး gap ကို လျှော့သည့် အစီအစဉ် ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** ဆုံးဖြတ်ချက် (ခ) ကို ရွေးရမည်။ တိုင်းတာရရှိသည့် ရလဒ် (training 0.51၊
held-out 0.71) ဖြင့် gap သည် 0.20 ဖြစ်သည်၊ ဆိုလိုသည်မှာ 64.29 % ကျဉ်းသည်။ ဤ အစီအစဉ်တွင်
training loss သည် 21.43 % တက်သည်၊ သို့သော် held-out loss သည် 27.55 % ကျသည်ဖြစ်သဖြင့်
လဲလှယ်မှုသည် အကျိုးရှိသည်။ gap ကျဉ်းလာသည့် အချက်ကို epoch အလိုက် ဆက်တိုင်းရမည်။

**တိုင်းတာမည့် metric —** held-out loss နှင့် training loss ၏ အချိုး၊ gap ကျဉ်းမှု ရာခိုင်နှုန်း၊
subgroup အလိုက် ကျရှုံးမှု၊ early stopping အတွက် အနိမ့်ဆုံး held-out loss ရရှိသည့် step။

## Self-check

၁။ အပိုင်း ၅.၁ အဖြေ ၁ တွင် cross-entropy အတွက် numerical stabilization မရှိပါက မည်သည့်အရာ
ဖြစ်ပေါ်သည်၊ ၎င်းသည် မည်သည့် term နှင့် တိုက်ရိုက် ဆက်စပ်သနည်း။

၂။ အပိုင်း ၅.၁ အဖြေ ၃ တွင် Adam ၏ ပထမ step update သည် learning rate နှင့် ညီမျှသည့်
အကြောင်းရင်းကို ဖော်ပြပါ။

၃။ အပိုင်း ၅.၁ အဖြေ ၅ တွင် SGD ၌ လမ်းကြောင်း နှစ်ခု တူညီပြီး Adam ၌ မတူညီသည့်
အကြောင်းရင်းကား အဘယ်နည်း။

၄။ အပိုင်း ၁ ဥပမာ ၁ နှင့် ဥပမာ ၄ တွင် memory ၏ အကြီးဆုံး အစိတ်အပိုင်းသည် မည်သည့်အရာ ဖြစ်သနည်း။

၅။ အပိုင်း ၅.၂ အဖြေ ၂ တွင် loss ရပ်နေခြင်း၏ အကြောင်းရင်းနှစ်ခုကို ခွဲခြားစစ်ဆေးသည့် အစဉ်ကို
ဖော်ပြပါ။

<details>
<summary>အဖြေများ</summary>

၁။ exp တန်ဖိုးများ ပြန့်ထွက်သဖြင့် `inf` ဖြစ်ပြီး ထို့နောက် `inf/inf` မှ NaN ဖြစ်သည်။ ထို့ကြောင့်
ဖော်မြူလာ တူညီသော်လည်း အကောင်အထည်ဖော်မှုတွင် stabilization လိုအပ်သည် — ၎င်းသည်
`Softmax` နှင့် `NaN (Not a Number)` နှင့် တိုက်ရိုက် ဆက်စပ်သည်။

၂။ ပထမ step တွင် m̂ = g နှင့် v̂ = g² ဖြစ်သဖြင့် m̂/√v̂ = g/|g| = 1 (gradient လက္ခဏာ) ဖြစ်သည်။
ထို့ကြောင့် update အရွယ်အစားသည် learning rate နှင့် ညီမျှသည်၊ ဤဥပမာတွင် 0.05 ဖြစ်သည်။

၃။ SGD တွင် L2 penalty သည် gradient ထဲ ဝင်သော်လည်း learning rate ဖြင့် တူညီစွာ မြှောက်ခံရသဖြင့်
decoupled ဖြစ်သည့် အခြေအနေနှင့် တိတိကျကျ တူညီသည်။ Adam တွင် L2 penalty သည် squared
gradient ၏ average ဖြင့် စားခံရသဖြင့် ကျုံ့ဝင်မှု၏ အာနိသင်သည် parameter တိုင်းအတွက် ကွာခြားသည်။
ထို့ကြောင့် ကွာခြားမှု 0.080565 ပေါ်လာသည်။

၄။ နှစ်ခုလုံးတွင် activation ဖြစ်သည် — ဥပမာ ၁ တွင် 480.0 MiB (activation share 86.0 % အထိ
ရောက်သည့် အခြေအနေ)၊ ဥပမာ ၄ တွင် 36.0 GiB (share 86.0 %)။ ထို့ကြောင့် memory ပြဿနာကို
ဖြေရှင်းရာတွင် activation ကို အရင် ကြည့်ရမည်။

၅။ ပထမဦးစွာ step တိုင်း၏ တကယ့် learning rate ကို စစ်သည် — သုညနီးပါး ဖြစ်နေပါက warmup
ရှည်လွန်းခြင်း ဖြစ်သည်။ ထို့နောက် gradient norm ကို စစ်သည် — သုည ဖြစ်နေပါက activation
function (ReLU) ကြောင့် dead unit ဖြစ်နေသည်။ နောက်ဆုံးတွင် capacity နှင့် regularization ကို
စစ်သည် — ထို အခြေအနေသည် `Underfitting` ဖြစ်သည်။

</details>

## References

- နယ်ပယ် အခြေခံ အချက်အလက် — `terms/01_math_and_training.md` နှင့် `glossary/by_area/01_math_and_training.json`။
- Source glossary — [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary)။
- Source repository — https://github.com/rohitg00/ai-engineering-from-scratch (MIT license)။
- လက်တွေ့ lab များ — `labs/lab_gradient_step.py`၊ `labs/lab_schedule.py`၊ `labs/lab_memory.py`၊
  `labs/run_labs.py` (usage နှင့် ရလဒ်များ — `labs/README.md`)။
