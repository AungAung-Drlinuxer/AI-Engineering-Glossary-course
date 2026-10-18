# 03 — သီအိုရီမှ ထုတ်လုပ်မှု အခြေခံအဆောက်အအုံသို့ (Theory to Infrastructure)

ဤစာတမ်းသည် နယ်ပယ် ၀၁ ၏ term ၄၂ ခုလုံးကို training အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ပြန်လည် ဖတ်ပါသည်။ loss၊ gradient၊ optimizer၊ learning rate၊ precision စသည့် term များသည် စာတမ်းအတွင်း သီအိုရီ အဖြစ်သာ မကျန်ရပါ၊ term တစ်ခုစီသည် training memory (VRAM)၊ compute အသုံးပြုမှု အချိုး၊ step တစ်ခုစီ၏ wall-clock၊ scaling အပြုအမူ၊ training run တစ်ခုလုံး၏ ကုန်ကျစရိတ် သို့မဟုတ် ထုတ်လုပ်မှုတွင် ကျိုးပျက်သည့် အချက် အနက် တစ်ခုခုကို ရွေ့လျားစေပါသည်။

ဤစာတမ်းရှိ ကိန်းဂဏန်း အားလုံးသည် `guides/01_math_and_training/scripts/` အောက်ရှိ Python script များမှ ရရှိသည့် တန်ဖိုးများ ဖြစ်ပါသည်။ ထို script များ၏ ဖော်မြူလာများ၊ parameter အရေအတွက်၊ batch size၊ sequence အရှည်၊ accelerator ၏ စွမ်းရည်နှင့် GPU တစ်နာရီ စျေးနှုန်းသည် ဤစာတမ်းတွင် ကြေညာထားသည့် ယူဆချက် (assumption) များ ဖြစ်ပါသည်၊ တိုင်းတာထားသည့် benchmark မဟုတ်ပါ။ hardware၊ library version၊ kernel၊ model ဖွဲ့စည်းပုံနှင့် vendor စျေးနှုန်း အလိုက် ကွာခြားသည့် တန်ဖိုးတိုင်းကို `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်` ဟု မှတ်သားထားပါသည်။

## ၁။ ဝင်ရိုး ခြောက်ခု၏ ဝေါဟာရ သတ်မှတ်ချက်

နောက်ပိုင်း အပိုင်းများနှင့် ဇယားအတွင်း ဤဝေါဟာရ ခြောက်ခုကို တူညီသည့် အဓိပ္ပာယ်ဖြင့်သာ အသုံးပြုပါမည်။

**training memory (VRAM)** — accelerator တစ်လုံး၏ memory ပေါ်တွင် training အတွင်း တစ်ပြိုင်နက် နေရာယူသည့် byte ပမာဏ ဖြစ်ပါသည်။ weight၊ gradient၊ optimizer state၊ activation နှင့် runtime buffer အားလုံး ပါဝင်ပါသည်။ ဤဝင်ရိုးသည် အမာခံ ကန့်သတ်ချက် ဖြစ်ပါသည်၊ VRAM ပြည့်လျှင် run သည် နှေးလာခြင်းဖြင့် မဟုတ်ဘဲ ရပ်တန့်ခြင်းဖြင့် ကျိုးပျက်ပါသည်။

**compute (FLOPs utilisation)** — step တစ်ခုအတွက် လိုအပ်သည့် floating-point operation ပမာဏနှင့် accelerator ၏ peak စွမ်းရည်ကို နှိုင်းယှဉ်သည့် အချိုး ဖြစ်ပါသည်။ ဖော်မြူလာအရ လိုအပ်သည့် FLOPs ကို peak ဖြင့် စားလျှင် အနည်းဆုံး အချိန် ရပါသည်၊ ရရှိသည့် အချိုး နည်းခြင်းသည် hardware ရှိပြီး အလုပ်မဖြစ်ခြင်း ဖြစ်ပါသည်။

**wall-clock per step** — optimizer step တစ်ခု (forward၊ backward၊ update) ပြီးစီးသည့် အချိန် ဖြစ်ပါသည်။ ဤဝင်ရိုးသည် compute၊ data pipeline၊ communication နှင့် kernel overhead တို့ ပေါင်းစပ်သည့် ရလဒ် ဖြစ်ပါသည်။ run တစ်ခုလုံး၏ အချိန်သည် step အရေအတွက်နှင့် step တစ်ခုစီ၏ အချိန် မြှောက်လဒ် ဖြစ်ပါသည်။

**scaling behaviour** — အရေအတွက် တစ်ခု (model အရွယ်အစား၊ batch၊ sequence အရှည်၊ token budget) ပြောင်းလျှင် memory၊ compute၊ step အချိန် သို့မဟုတ် ကုန်ကျစရိတ် မည်သို့ တိုးသည်ကို ဖော်ပြသည့် ဝင်ရိုး ဖြစ်ပါသည်။ linear တိုးခြင်း၊ quadratic တိုးခြင်းနှင့် ပြောင်းလဲမှု မရှိခြင်းတို့သည် မတူညီသည့် ဆုံးဖြတ်ချက်များကို ဖြစ်ပေါ်စေပါသည်။

**cost per training run** — accelerator အချိန် အရေအတွက်ကို တစ်နာရီ စျေးနှုန်းဖြင့် မြှောက်ထားသည့် တန်ဖိုး ဖြစ်ပါသည်။ ဤဝင်ရိုးကို token budget၊ utilisation၊ wall-clock၊ parallelism အရေအတွက်နှင့် ပြန်လည် လုပ်ရသည့် အကြိမ်အရေအတွက် တို့က ဆုံးဖြတ်ပါသည်။ စျေးနှုန်းသည် vendor နှင့် region အလိုက် ကွာခြားသည့်အတွက် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

**production consequence** — ထို concept ကို လျစ်လျူရှုလျှင် ထုတ်လုပ်မှု run တွင် မည်သည့် အရာ ကျိုးပျက်မည်ကို ဆိုလိုပါသည်။ ဥပမာ learning rate ကို critical တန်ဖိုး အထက် သတ်မှတ်လျှင် loss သည် မတိုးဘဲ ချဲ့ထွင်လာသဖြင့် GPU-hours အားလုံး အလဟသ ဖြစ်ခြင်းသည် ထုတ်လုပ်မှု အကျိုးဆက် ဖြစ်ပါသည်။

## ၂။ Master table — term ၄၂ ခုလုံး

ဇယားရှိ term အစဉ်သည် `glossary/by_area/01_math_and_training.json` ၏ အစဉ်အတိုင်း ဖြစ်ပါသည်၊ term တစ်ခုစီအတွက် တစ်လိုင်း စီ ပါဝင်ပါသည်။

| Term | primary axis | ကုန်ကျခြင်း / ချွေတာခြင်း | ရွေ့လျားသည့် ကိန်း | ထုတ်လုပ်မှု အကျိုးဆက် |
|---|---|---|---|---|
| Activation Checkpointing | training memory | activation memory ၅ ဆ ချွေတာပြီး step FLOPs ကို 8/6 ဆ တင်သည် | act_factor 10 မှ 2 | batch ကြီးကို accelerator တစ်လုံးပေါ် တင်နိုင်သည် |
| Activation Function | compute | nonlinearity မရှိလျှင် layer များစွာ affine တစ်ခုသို့ ကျုံ့ဝင်သည် | per-token FLOPs | gradient စီးဆင်းမှု ပျက်လျှင် run သည် အလုပ်မဖြစ်ပါ |
| Adam (Optimizer) | training memory | parameter တစ်ခုလျှင် fp32 moment ၂ ခု = 8 byte ထပ်တင်သည် | optimizer bytes/param (0 → 8) | VRAM ကုန်ခန်း၍ step တစ်ခုလျှင် batch ကျဆင်းသည် |
| AdamW | training memory | state ပမာဏသည် Adam နှင့် တူညီဆဲ ဖြစ်သည် | state bytes/param = 8 | weight decay ကို schedule နှင့် တွဲ၍ tune ရသည် |
| Autograd | wall-clock per step | forward graph ကို မှတ်တမ်းတင်သဖြင့် step အချိန် တင်သည် | step milliseconds | graph ကို retain လုပ်လျှင် VRAM ထပ်စားသည် |
| Backpropagation | compute | backward သည် forward ၏ နှစ်ဆ (4N vs 2N) ဖြစ်သည် | FLOPs per step ≈ 6N | step တစ်ခု၏ အချိန်သည် forward ၏ သုံးဆ ဖြစ်သည် |
| Batch Size | training memory | activation နှင့် VRAM ကို အချိုးကျ တင်သည် | batch × act per sequence | memory မလုံလောက်လျှင် run သည် ချက်ချင်း ရပ်သည် |
| Contrastive Learning | compute | pair အရေအတွက်ဖြင့် similarity matrix ကို တွက်သည် | batch တစ်ခုလျှင် pair ပမာဏ | ကြီးသည့် batch လိုအပ်သဖြင့် VRAM ဖိအား တင်သည် |
| Cross-Entropy | compute | vocabulary အတွက် log နှင့် sum ကို step တိုင်း တွက်သည် | vocabulary × tokens | tokenizer မတူလျှင် loss ကို တိုက်ရိုက် နှိုင်းယှဉ်၍ မရပါ |
| Data Augmentation | wall-clock per step | input pipeline ကို host CPU တွင် တင်သည် | augment milliseconds/step | host သည် accelerator ကို စောင့်စေသဖြင့် utilisation ကျသည် |
| DPO (Direct Preference Optimization) | cost per run | reward model နှင့် RL loop ကို ဖယ်ရှားသည် | run အရေအတွက်၊ GPU-hours | pipeline အဆင့် နည်းသဖြင့် ကုန်ကျစရိတ် ခန့်မှန်းရ လွယ်သည် |
| Dropout | compute | training တွင် mask ထည့်ပြီး inference တွင် ဖြုတ်သည် | active unit အချိုး | train နှင့် inference အပြုအမူ ကွာခြားမှုကို စမ်းသပ်ရသည် |
| Eigenvalue | scaling behaviour | အမြင့်ဆုံး curvature သည် တည်ငြိမ်သည့် lr ကို ဆုံးဖြတ်သည် | lambda_max | lr ကို မှန်းဆရာတွင် upper bound အဖြစ် သုံးသည် |
| Epoch | cost per run | dataset ကို ဖြတ်သည့် အကြိမ် ဖြစ်သည် | epochs × tokens | epoch ဖြင့်သာ နှိုင်းယှဉ်လျှင် token budget မတူဘဲ မှားနိုင်သည် |
| Fine-tuning | cost per run | pretrained checkpoint မှ စတင်သဖြင့် အစမှ လေ့ကျင့်ခြင်းကို ဖယ်သည် | run ၏ token budget | full fine-tune သည် base model ၏ VRAM အတိုင်း လိုသည် |
| Gradient | compute | loss ၏ derivative ကို parameter တိုင်းအတွက် ထုတ်သည် | gradient tensor bytes | gradient မရှိလျှင် optimizer သည် update မလုပ်နိုင်ပါ |
| Gradient Accumulation | training memory | microbatch အပေါ်တွင် ချုံ့တင်သည် | microbatch × act per sequence | step အရေအတွက် နည်းသော်လည်း step အချိန် တိုးသည် |
| Gradient Clipping | wall-clock per step | norm တွက်ချက်မှုကို step တစ်ခုစီအတွက် ပေါင်းထည့်သည် | gradient norm | clip မလုပ်လျှင် step တစ်ခုတည်းက run ကို ဖျက်နိုင်သည် |
| Gradient Descent | compute | negative gradient ကို update အဖြစ် အသုံးပြုသည် | update တစ်ကြိမ်၏ အရွယ်အစား | divergence ဖြစ်လျှင် GPU-hours အားလုံး ဆုံးရှုံးသည် |
| Hyperparameter | production consequence | configuration ရွေးချယ်မှုတိုင်းအတွက် run တစ်ခု လိုသည် | tuning run အရေအတွက် | tuning budget သည် run ကုန်ကျစရိတ်၏ အဓိက အစိတ်အပိုင်း ဖြစ်သည် |
| JAX | compute | function များကို compile လုပ်၍ vectorize လုပ်သည် | achieved ÷ peak FLOPs | transform မကိုက်ညီလျှင် model code ကို ပြန်ရေးရသည် |
| Knowledge Distillation | cost per run | teacher run ကို ဦးစွာ လိုသည် | teacher + student GPU-hours | serve ကုန်ကျစရိတ် ကို ရေရှည်တွင် လျှော့နိုင်သည် |
| Learning Rate | scaling behaviour | update တစ်ကြိမ်၏ အရွယ်အစားကို သတ်မှတ်သည် | lr နှင့် critical တန်ဖိုး 2/lambda_max | lr လွန်လျှင် loss ချဲ့ထွင်လာပြီး run ပျက်သည် |
| Learning Rate Schedule | scaling behaviour | အစောပိုင်း တည်ငြိမ်မှုနှင့် နောက်ပိုင်း ချွေတာမှုကို လဲလှယ်သည် | mean lr၊ area under the curve | schedule မတူလျှင် run နှစ်ခုကို တိုက်ရိုက် နှိုင်းယှဉ်၍ မရပါ |
| LoRA (Low-Rank Adaptation) | training memory | trainable parameter ကို low-rank matrix အထိ လျှော့သည် | trainable params | adapter ကို သီးခြား serve လုပ်နိုင်သည် |
| Loss Function | compute | objective တစ်ခုတည်းကို သတ်မှတ်သည် | loss value | loss မှားလျှင် GPU-hours အားလုံး အလဟသ ဖြစ်သည် |
| Mixed Precision | compute | matrix operation များအတွက် ကျဉ်းသည့် dtype သုံးသည် | achieved TFLOPs | range မပြည့်လျှင် NaN ဖြစ်ပြီး run ရပ်သည် |
| NaN (Not a Number) | production consequence | ဆင်းသက်သည့် တန်ဖိုး အားလုံးကို ပျက်စီးစေသည် | non-finite tensor အရေအတွက် | checkpoint မရှိလျှင် run ကို အစမှ ပြန်စရသည် |
| Normalization | compute | statistics တွက်ချက်မှုကို forward ထဲ ထပ်တိုးသည် | step FLOPs | batch statistics သည် batch size နှင့် တွဲလျက် ရှိသည် |
| Optimizer | training memory | parameter တစ်ခုလျှင် state byte ကို သတ်မှတ်သည် | bytes/param (0၊ 4၊ 8) | optimizer ရွေးချယ်မှုသည် အကြီးဆုံး batch ကို ဆုံးဖြတ်သည် |
| Overfitting | cost per run | ပိုလေ့ကျင့်ခြင်းသည် generalization ကို မတိုးစေပါ | held-out metric နှင့် training metric | မလိုအပ်သည့် GPU-hours ကို ဖြုန်းတီးသည် |
| QLoRA | training memory | base model ကို low-bit ဖြင့် ရပ်တန့်ထားသည် | base bytes + adapter bytes | ကတ်တစ်လုံးတည်းဖြင့် ကြီးသည့် model ကို adapt လုပ်နိုင်သည် |
| ReLU | compute | `max(0, x)` ဖြစ်သဖြင့် တွက်ချက်မှု သက်သာသည် | element-wise FLOPs | negative ဘက်တွင် gradient သုည ဖြစ်၍ unit သေနိုင်သည် |
| RLHF (Reinforcement Learning from Human Feedback) | cost per run | reward model နှင့် RL အဆင့် နှစ်ခု ထပ်တင်သည် | GPU-hours အဆင့်အလိုက် | pipeline အဆင့် များသဖြင့် ကုန်ကျစရိတ် ခန့်မှန်းရ ခက်သည် |
| SFT (Supervised Fine-Tuning) | cost per run | ပြသထားသည့် နမူနာများအပေါ် ချိန်ညှိသည် | tokens × epochs | နမူနာ အရည်အသွေးသည် ရလဒ်ကို တိုက်ရိုက် ဆုံးဖြတ်သည် |
| Softmax | compute | exp နှင့် normalization ကို vocabulary တစ်လျှောက် တွက်သည် | vocabulary ops | stabilization မလုပ်လျှင် overflow ဖြစ်ပြီး non-finite ထွက်သည် |
| Stochastic Gradient Descent (SGD) | scaling behaviour | state မလိုသော baseline ဖြစ်သည် | bytes/param = 0 | optimizer state အတွက် VRAM မကုန်သဖြင့် batch ကြီးစွာ တင်နိုင်သည် |
| Transfer Learning | cost per run | representation များကို ပြန်လည် အသုံးချသည် | pretraining token budget | task အသစ်အတွက် လိုသည့် token ပမာဏ ကျဆင်းသည် |
| Underfitting | cost per run | capacity၊ signal သို့မဟုတ် optimization မလုံလောက်ပါ | training loss ၏ အောက်ဆုံးတန်ဖိုး | လေ့ကျင့်ချိန် ထပ်တိုးခြင်းသည် အလဟသ ဖြစ်သည် |
| Warmup | wall-clock per step | အစောပိုင်း step များကို သေးငယ်သည့် update ဖြင့် စသည် | warmup steps | warmup မရှိလျှင် အစောပိုင်း run ပျက်စီးနိုင်သည် |
| Weight | training memory | parameter တစ်ခုလျှင် byte ပမာဏကို သတ်မှတ်သည် | params × bytes/param | တစ်ကတ်ပေါ် တင်နိုင်မှုကို ဆုံးဖြတ်သည် |
| Weight Decay | scaling behaviour | parameter ၏ magnitude ကို လျှော့ချသည် | decay coefficient | generalization နှင့် model capacity ကို လဲလှယ်သည် |

## ၃။ term အလိုက် ရှင်းလင်းချက်

term များကို မိသားစု ခုနစ်ခုဖြင့် စုစည်းထားပါသည် — (က) gradient နှင့် update ယန္တရား၊ (ခ) learning rate၊ schedule နှင့် training loop၊ (ဂ) training memory၊ precision နှင့် regularization၊ (ဃ) objective နှင့် သင်္ချာ အခြေခံ၊ (င) generalization၊ data နှင့် ဖွဲ့စည်းပုံ၊ (စ) adaptation နှင့် alignment၊ (ဆ) compute framework။ ဤအုပ်စုခွဲမှုသည် အပိုင်း ၂ ၏ ဇယားနှင့် တိုက်ရိုက် ကိုက်ညီပါသည်။

### မိသားစု (က) — gradient နှင့် update ယန္တရား

#### Gradient

Gradient သည် loss ၏ partial derivative များ စုစည်းထားသည့် vector ဖြစ်ပြီး တန်ဖိုး အမြန်ဆုံး တိုးပွားသည့် ဦးတည်ချက်ကို ညွှန်းပါသည်။ training တွင် optimizer အားလုံးနီးပါးသည် ဤ vector ကို အသုံးပြု၍ parameter များကို ရွှေ့ပါသည်။ compute အရ gradient ၏ တန်ဖိုးတိုင်းသည် backward pass ၏ operation အရေအတွက်မှ ဆင်းသက်လာပါသည်။ memory အရ ၎င်းသည် parameter အရေအတွက်နှင့် တူညီသည့် byte ပမာဏကို နေရာယူပါသည်၊ ဥပမာ (ခ) တွင် 7.0B parameter ၏ gradient သည် fp16 ဖြင့် 13.039 GiB ဖြစ်ပါသည်။

#### Gradient Descent

Gradient Descent သည် negative gradient ကို အသုံးပြု၍ parameter များကို ရွှေ့သည့် update အုပ်စု ဖြစ်ပါသည်။ ၎င်း၏ အပြုအမူကို learning rate က ဆုံးဖြတ်သဖြင့် compute ဝင်ရိုးနှင့် တိုက်ရိုက် ချိတ်ဆက်ပါသည်။ ရိုးရှင်းသည့် quadratic တွင် update သည် `1 − lr × lambda` အချိုးဖြင့် ကျုံ့ သို့မဟုတ် ချဲ့ပါသည်၊ ဤအချိုး၏ ပမာဏသည် ၁ ကျော်လျှင် trajectory သည် ချဲ့ထွင်လာပါသည်။ ထို့ကြောင့် divergence သည် မတော်တဆ ဖြစ်စဉ် မဟုတ်ဘဲ learning rate နှင့် curvature ၏ အချိုးဖြင့် တိကျစွာ သတ်မှတ်သည့် အခြေအနေ ဖြစ်ပါသည်။

#### Stochastic Gradient Descent (SGD)

SGD သည် dataset တစ်ခုလုံး အစား နမူနာတစ်ခု သို့မဟုတ် minibatch တစ်ခုမှ ခန့်မှန်းထားသည့် gradient ဖြင့် update လုပ်ပါသည်။ memory အရ အရေးအကြီးဆုံး အချက်မှာ SGD သည် optimizer state ကို မသိမ်းဆည်းခြင်း ဖြစ်ပါသည်၊ ဥပမာ (ခ) တွင် ၎င်း၏ state သည် parameter တစ်ခုလျှင် 0 byte ဖြစ်ပါသည်။ ထို့ကြောင့် 7.0B model တွင် fixed memory သည် 26.077 GiB သာ ဖြစ်ပြီး တစ်ကတ်ပေါ် sequence ၇ ခု ဆံ့ပါသည်။ momentum ထည့်လျှင် state 4 byte ဖြစ်လာသဖြင့် ဆံ့သည့် batch သည် ၂ ခုသို့ ကျဆင်းပါသည်။

#### Backpropagation

Backpropagation သည် scalar loss မှ computation graph အတွင်း chain rule ဖြင့် derivative များကို ဖြန့်ပေးပါသည်။ compute အရ backward pass သည် forward pass ၏ နှစ်ဆ ခန့် လိုသဖြင့် step တစ်ခု၏ FLOPs သည် parameter နှင့် token ၏ မြှောက်လဒ် ၆ ဆ ခန့် ဖြစ်ပါသည်။ ဥပမာ (ဂ) တွင် ဤဖော်မြူလာအရ token 16384 အတွက် step တစ်ခုသည် 6.8813e+14 FLOPs လိုပါသည်။ ဤကိန်းသည် step အချိန်နှင့် run ကုန်ကျစရိတ် နှစ်ခုလုံးကို တိုက်ရိုက် ဆုံးဖြတ်ပါသည်။

#### Autograd

Autograd သည် tensor operation များကို မှတ်တမ်းတင်ပြီး derivative များကို အလိုအလျောက် တွက်ပေးသည့် စနစ် ဖြစ်ပါသည်။ ဤမှတ်တမ်းတင်မှုသည် အခမဲ့ မဟုတ်ပါ၊ forward graph ကို သိမ်းထားသဖြင့် step အချိန်နှင့် VRAM နှစ်ခုလုံး တင်လာပါသည်။ graph ကို မလိုအပ်ဘဲ retain လုပ်ထားလျှင် activation များကို ရှင်းမပစ်နိုင်သဖြင့် memory ပြည့်လာပါသည်။ ထို့ကြောင့် step အချိန်နှင့် memory ကို စောင့်ကြည့်ရာတွင် graph မူဝါဒသည် ပထမဆုံး စစ်ရမည့် အချက် ဖြစ်ပါသည်။

#### Optimizer

Optimizer သည် gradient များကို parameter update များအဖြစ် အသွင်ပြောင်းပါသည်။ ဤနယ်ပယ်တွင် optimizer ရွေးချယ်မှုသည် memory ဆုံးဖြတ်ချက် ဖြစ်ပါသည်၊ အကြောင်းမှာ optimizer တိုင်းသည် state byte အနည်းအများ ကွဲပြားသောကြောင့် ဖြစ်ပါသည်။ ဥပမာ (ခ) တွင် bytes per parameter သည် 0 မှ 8 အထိ ကွာခြားသဖြင့် fixed memory သည် 26.077 GiB မှ 78.231 GiB အထိ ရွေ့ပါသည်။ ထို ရွေ့လျားမှုသည် တစ်ကတ်ပေါ် တင်နိုင်သည့် batch ကို ၇ မှ ၀ အထိ ပြောင်းစေပါသည်။

#### Adam (Optimizer)

Adam သည် gradient ၏ exponential average နှင့် squared gradient ၏ exponential average ကို ပေါင်းစပ်ပြီး parameter တစ်ခုချင်းစီအတွက် update scale ကို ချိန်ညှိပါသည်။ ဤချိန်ညှိမှုအတွက် parameter တစ်ခုလျှင် fp32 moment နှစ်ခု လိုသဖြင့် state သည် parameter တစ်ခုလျှင် 8 byte ဖြစ်ပါသည်။ 7.0B model တွင် ထို state သည် 52.154 GiB ဖြစ်ပြီး weight နှင့် gradient စုစုပေါင်း 26.077 GiB ကို ကျော်လွန်ပါသည်။ ထို့ကြောင့် Adam ကို ရွေးချယ်ခြင်းသည် update အရည်အသွေးနှင့် တစ်ကတ်ပေါ် batch ဆံ့မှု အကြား လဲလှယ်မှု ဖြစ်ပါသည်။

#### AdamW

AdamW သည် weight decay ကို gradient အပေါ် အခြေခံသည့် update မှ ခွဲထုတ်ထားသည့် Adam မျိုးကွဲ ဖြစ်ပါသည်။ memory အရ AdamW သည် Adam နှင့် တူညီပါသည်၊ ဥပမာ (ခ) တွင် နှစ်ခုလုံး၏ state သည် 52.154 GiB ဖြစ်ပါသည်။ သို့သော် ခွဲထုတ်မှုကြောင့် decay နှင့် learning rate ကို သီးခြား tune နိုင်သဖြင့် tuning run အရေအတွက် ကွာခြားနိုင်ပါသည်။ tuning run တစ်ခုစီသည် GPU-hours ကုန်ကျသဖြင့် ဤရွေးချယ်မှုသည် ကုန်ကျစရိတ် အပေါ် သက်ရောက်ပါသည်။

#### Gradient Clipping

Gradient Clipping သည် gradient ၏ norm ကို ရွေးချယ်ထားသည့် threshold အောက် ကန့်သတ်ပါသည်။ တွက်ချက်မှု အရ ၎င်းသည် step တစ်ခုစီတွင် norm တစ်ခု တွက်ချက်ရသဖြင့် wall-clock ကို အနည်းငယ် တင်စေပါသည်။ ပေးသည့် အကျိုးအမြတ်မှာ step တစ်ခုတည်း၏ ပုံမှန်မဟုတ်သည့် gradient က run ကို မတည်ငြိမ်စေခြင်းမှ ကာကွယ်ခြင်း ဖြစ်ပါသည်။ ထို့ကြောင့် ဤအပိုအလွှာသည် ရှည်လျားသည့် run တစ်ခုလုံး၏ ကုန်ကျစရိတ်ကို ကာကွယ်သည့် အာမခံ ဖြစ်ပါသည်။

#### Gradient Accumulation

Gradient Accumulation သည် optimizer update တစ်ကြိမ် မလုပ်မီ microbatch အများအပြားမှ gradient များကို ပေါင်းပါသည်။ memory အရ ၎င်းသည် တစ်ကြိမ်စာ activation ကိုသာ သိမ်းသဖြင့် VRAM လိုအပ်ချက် ကျဆင်းပါသည်။ အစားပေးရသည့် ကုန်ကျစရိတ်မှာ step အရေအတွက် တိုးလာခြင်း ဖြစ်ပါသည်၊ ခေါ်သည့် အကြိမ်အရေအတွက် အချိုးအစားအတိုင်း step တစ်ခု၏ wall-clock တင်လာပါသည်။ ထို့ကြောင့် ပိုကြီးသည့် effective batch ကို memory အစား အချိန်ဖြင့် ဝယ်ယူခြင်း ဖြစ်ပါသည်။

### မိသားစု (ခ) — learning rate၊ schedule နှင့် training loop

#### Learning Rate

Learning rate သည် optimizer update တစ်ကြိမ်၏ အရွယ်အစားကို ဆုံးဖြတ်သည့် scale factor ဖြစ်ပါသည်။ ၎င်းသည် scaling ဝင်ရိုး အပေါ် တိုက်ရိုက် သက်ရောက်ပါသည်၊ အကြောင်းမှာ ရိုးရှင်းသည့် quadratic တွင် update အချိုးသည် `1 − lr × lambda_max` ဖြစ်သောကြောင့် ဖြစ်ပါသည်။ lr သည် `2 / lambda_max` ကို ကျော်လွန်လျှင် trajectory သည် ချဲ့ထွင်လာပြီး loss သည် မတိုးတော့ပါ။ ဤတန်ဖိုးသည် objective ၏ curvature အပေါ် မှီခိုသဖြင့် ပုံသေ ကိန်းသေ တစ်ခု မဟုတ်ပါ။

#### Learning Rate Schedule

Schedule သည် training တိုးတက်လာသည့်အလိုက် learning rate ကို ပြောင်းလဲသည့် မူဝါဒ ဖြစ်ပါသည်။ အစောပိုင်း step များနှင့် နောက်ပိုင်း step များသည် update scale အမျိုးမျိုးမှ အကျိုးရနိုင်သဖြင့် schedule သည် ထို လဲလှယ်မှုကို ထိန်းချုပ်သည့် knob ဖြစ်ပါသည်။ ဤဝင်ရိုးကို တိုင်းတာရာတွင် mean lr နှင့် area under the curve သည် ပိုမို သင့်လျော်ပါသည်၊ အကြောင်းမှာ step တိုင်း၏ rate ကို တစ်ခုတည်းသော ကိန်းဖြင့် ဖော်ပြ၍ မရသောကြောင့် ဖြစ်ပါသည်။ schedule နှစ်ခုကို တူညီသည့် token budget အောက်တွင်သာ နှိုင်းယှဉ်ရပါသည်။

#### Warmup

Warmup သည် learning rate ကို သေးငယ်သည့် တန်ဖိုးမှ စတင်၍ အဓိက schedule ၏ ရည်မှန်း တန်ဖိုးသို့ တဖြည်းဖြည်း တင်သည့် အစောပိုင်း အဆင့် ဖြစ်ပါသည်။ အစောပိုင်း gradient များနှင့် optimizer statistics များ မတည်ငြိမ်နိုင်သဖြင့် ချက်ချင်း အရွယ်အစားပြည့် update လုပ်ခြင်းသည် အစောပိုင်း step များကို ဖျက်စီးနိုင်ပါသည်။ ဤအဆင့်သည် accelerator အချိန် အနည်းငယ် ကုန်ကျပါသည်၊ အကြောင်းမှာ warmup step များတွင် learning rate သေးငယ်သဖြင့် loss အကျဆင်းနှုန်း နည်းသောကြောင့် ဖြစ်ပါသည်။ ထို့ကြောင့် warmup ကို step သို့မဟုတ် processed token အနေဖြင့် သတ်မှတ်၍ လျှော့ချခြင်းသည် run ကို ကာကွယ်သည့် ကုန်ကျစရိတ် ဖြစ်ပါသည်။

#### Hyperparameter

Hyperparameter သည် model parameter အဖြစ် သင်ယူခြင်း မရှိဘဲ configuration ကို ပုံဖော်သည့် ရွေးချယ်မှု ဖြစ်ပါသည်။ ၎င်း၏ ထုတ်လုပ်မှု အကျိုးဆက်မှာ ရွေးချယ်မှု တစ်ခုစီကို စမ်းသပ်ရန် training run တစ်ခု လိုခြင်း ဖြစ်ပါသည်။ ထို့ကြောင့် tuning budget သည် run ကုန်ကျစရိတ်၏ အဓိက အစိတ်အပိုင်း ဖြစ်လာပါသည်။ ဥပမာ (ဂ) အရ token ၁၀၀B run တစ်ခုသည် USD 7291.67 ခန့် ကုန်ကျသဖြင့် run အနည်းအများသည် ချက်ချင်း ကွာခြားလာပါသည်။

#### Batch Size

Batch Size သည် optimizer update တစ်ကြိမ်၏ gradient အတွက် ပါဝင်သည့် နမူနာ အရေအတွက် ဖြစ်ပါသည်။ memory အရ activation သည် batch အပေါ် linear တိုးသဖြင့် ဤအရေအတွက်သည် VRAM ၏ အဓိက knob ဖြစ်ပါသည်။ ဥပမာ (က) တွင် batch 8၊ seq 2048 အတွက် activation သည် checkpointing off တွင် 15.000 GiB ဖြစ်ပြီး checkpointing on တွင် 3.000 GiB သို့ ကျဆင်းပါသည်။ သို့သော် batch တိုးခြင်းသည် step အရေအတွက် လျော့စေသဖြင့် compute နှင့် wall-clock ကိုပါ သက်ရောက်ပါသည်။

#### Epoch

Epoch သည် သတ်မှတ်ထားသည့် training dataset ကို တစ်ကြိမ် ဖြတ်သွားခြင်း ဖြစ်ပါသည်။ ကုန်ကျစရိတ် စောင့်ကြည့်မှုတွင် epoch အရေအတွက်သည် token budget နှင့် တူညီသည့် အဓိပ္ပာယ် မရှိပါ၊ အကြောင်းမှာ dataset အရွယ်အစား မတူလျှင် တူညီသည့် epoch အရေအတွက်သည် token ပမာဏ မတူသောကြောင့် ဖြစ်ပါသည်။ run နှစ်ခုကို နှိုင်းယှဉ်ရာတွင် token budget ကို အခြေခံရမည် ဖြစ်ပါသည်။ distributed သို့မဟုတ် sampled training တွင် epoch ၏ တိကျသည့် အကောင်အထည်ဖော်မှုသည် data loader အပေါ် မူတည်ပါသည်။

### မိသားစု (ဂ) — training memory၊ precision နှင့် regularization

#### Activation Checkpointing

Activation Checkpointing သည် forward activation အားလုံးကို မသိမ်းဆည်းဘဲ ရွေးချယ်ထားသည့် အချို့ကိုသာ သိမ်းပြီး ကျန်သည့် အချို့ကို backward အတွင်း ပြန်လည် တွက်ချက်ပါသည်။ memory အရ ၎င်းသည် activation အပိုင်းကို ကျုံ့စေပါသည်၊ ဥပမာ (က) တွင် 15.000 GiB မှ 3.000 GiB သို့ ကျဆင်းပါသည်။ အစားပေးရသည့် ကုန်ကျစရိတ်မှာ compute ဖြစ်ပါသည်၊ forward တစ်ကြိမ် ပြန်တွက်သဖြင့် step FLOPs သည် 8/6 = 1.333 ဆ တင်လာပါသည်။ ဤလဲလှယ်မှု၏ ရလဒ်မှာ တစ်ကတ်ပေါ် တင်နိုင်သည့် batch သည် 26 မှ 131 သို့ တက်လာခြင်း ဖြစ်ပါသည်။

#### Mixed Precision

Mixed Precision သည် operation အမျိုးမျိုးအတွက် data type အမျိုးမျိုးကို အသုံးပြုသည့် numerical မဟာဗျူဟာ ဖြစ်ပါသည်။ memory အရ bytes per parameter ကျဆင်းသဖြင့် weight နှင့် gradient နှစ်ခုလုံး ကျုံ့ပါသည်၊ ဥပမာ (က) တွင် fp32 ၏ 4.843 GiB မှ fp16 ၏ 2.421 GiB သို့ ကျဆင်းပါသည်။ compute အရ matrix operation အများစုကို ကျဉ်းသည့် dtype ဖြင့် လုပ်သဖြင့် achieved TFLOPs တက်နိုင်ပါသည်။ သို့သော် ဤအကျိုးအမြတ်သည် hardware၊ kernel နှင့် scaling နည်းလမ်း အပေါ် မှီခိုသဖြင့် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

#### Weight

Weight သည် model transformation တစ်ခုအတွင်း ရှိသည့် train လုပ်နိုင်သည့် coefficient ဖြစ်ပါသည်။ memory အရ weight သည် parameter အရေအတွက်နှင့် bytes per parameter ၏ မြှောက်လဒ် ဖြစ်ပါသည်။ ဥပမာ (ခ) တွင် 7.0B parameter သည် fp16 ဖြင့် 13.039 GiB ဖြစ်ပါသည်။ ဤကိန်းသည် တစ်ကတ်ပေါ် တင်နိုင်မှု၏ အခြေခံ ဖြစ်သဖြင့် model အရွယ်အစား ဆုံးဖြတ်ချက်တိုင်း၏ ပထမဆုံး စစ်ဆေးချက် ဖြစ်ပါသည်။

#### Weight Decay

Weight Decay သည် training တစ်လျှောက် ရွေးချယ်ထားသည့် parameter များ၏ magnitude ကို လျှော့ချသည့် update rule ဖြစ်ပါသည်။ ၎င်းသည် memory သို့မဟုတ် step အချိန်ကို တိုက်ရိုက် မပြောင်းလဲပါ၊ scaling အပြုအမူကို ပြောင်းလဲပါသည်။ coefficient သည် model၊ optimizer၊ schedule နှင့် data အပေါ် မှီခိုသဖြင့် စမ်းသပ်ရန် run များ လိုပါသည်။ ထို့ကြောင့် ၎င်း၏ အကျိုးအမြတ်သည် generalization နှင့် tuning run ကုန်ကျစရိတ် အကြား လဲလှယ်မှု ဖြစ်ပါသည်။

#### Dropout

Dropout သည် training အတွင်း activation အချို့ကို ကျပန်း သုည သတ်မှတ်ပါသည်။ compute အရ ၎င်းသည် element-wise mask တစ်ခု ထည့်သည့် အလုပ်သာ ဖြစ်သဖြင့် step FLOPs အပေါ် သက်ရောက်မှု အနည်းငယ်သာ ရှိပါသည်။ သို့သော် training နှင့် inference အပြုအမူ ကွာခြားသဖြင့် eval configuration တွင် state ကို မှတ်တမ်းတင်ထားရပါသည်။ ဤအချက်ကို လျစ်လျူရှုလျှင် eval ရလဒ်များ၏ ပြန်လည် ရရှိနိုင်မှု ပျက်ပါသည်။

#### Normalization

Normalization သည် သတ်မှတ်ထားသည့် statistics များဖြင့် input၊ activation သို့မဟုတ် feature များကို ပြန်လည် scale လုပ်ပါသည်။ compute အရ statistics တွက်ချက်မှုနှင့် ပြောင်းပြန်လှန်မှုတို့သည် step တိုင်း၏ operation အရေအတွက်ကို တင်စေပါသည်။ batch normalization တွင် ထို statistics သည် batch အပေါ် မှီခိုသဖြင့် batch size နှင့် တွဲလျက် ရှိပါသည်။ ထို့ကြောင့် batch သေးငယ်သည့် run များတွင် normalization အမျိုးအစား ရွေးချယ်မှုသည် scaling အပြုအမူကို ပြောင်းစေပါသည်။

#### NaN (Not a Number)

NaN သည် မသတ်မှတ်နိုင်သည့် numerical ရလဒ်ကို ကိုယ်စားပြုသည့် floating-point တန်ဖိုး ဖြစ်ပါသည်။ တန်ဖိုး တစ်ခု NaN ဖြစ်လျှင် ၎င်းမှ ဆင်းသက်သည့် gradient နှင့် parameter များအားလုံး ပျက်စီးနိုင်သဖြင့် ဤဖြစ်စဉ်သည် ထုတ်လုပ်မှု အကျိုးဆက် အကြီးမားဆုံး အချက် ဖြစ်ပါသည်။ ပြန်လည် စရန် recovery checkpoint လိုသဖြင့် GPU-hours ထပ်ကုန်ပါသည်။ ထို့ကြောင့် ပထမဆုံး non-finite tensor ကို ရှာဖွေရန် anomaly detection ကို run အစောပိုင်းတွင် ထည့်ထားရပါသည်။

### မိသားစု (ဃ) — objective နှင့် သင်္ချာ အခြေခံ

#### Loss Function

Loss Function သည် prediction များနှင့် target များကို optimization လျှော့ချရန် ကြိုးစားသည့် တန်ဖိုး တစ်ခုသို့ map လုပ်ပါသည်။ ၎င်း၏ compute ကုန်ကျစရိတ်သည် output အရေအတွက်နှင့် တိုင်းတာသည့် term အရေအတွက် အပေါ် မှီခိုပါသည်။ မှားယွင်းသည့် loss ရွေးချယ်မှုသည် run ကို အလဟသ ဖြစ်စေသဖြင့် ဤရွေးချယ်မှုကို ကုန်ကျစရိတ် အပေါ် သက်ရောက်သည့် ဆုံးဖြတ်ချက် အဖြစ် သတ်မှတ်ရပါသည်။ training loss နည်းခြင်းသည် ထုတ်လုပ်မှု အပြုအမူကို အာမမခံပါ။

#### Cross-Entropy

Cross-Entropy သည် ရည်မှန်း ရလဒ်အတွက် သတ်မှတ်ထားသည့် probability ၏ negative log အပေါ် အခြေခံသည့် loss ဖြစ်ပါသည်။ next-token training တွင် ၎င်းသည် vocabulary တစ်လျှောက်လုံး log နှင့် sum ကို step တိုင်း တွက်ရသဖြင့် compute ကုန်ကျစရိတ် ရှိပါသည်။ ဤတန်ဖိုးသည် tokenization အပေါ် မှီခိုသဖြင့် tokenizer မတူသည့် run နှစ်ခုကို တိုက်ရိုက် နှိုင်းယှဉ်၍ မရပါ။ ထို့ကြောင့် loss နှိုင်းယှဉ်မှုတိုင်းတွင် tokenization ကို မှတ်တမ်းတင်ရပါသည်။

#### Softmax

Softmax သည် logit များကို အပေါင်းလက္ခဏာရှိပြီး စုစုပေါင်း တစ်နှင့် ညီသည့် distribution အဖြစ် ပြောင်းပါသည်။ compute အရ ၎င်းသည် vocabulary တစ်လျှောက် exp နှင့် normalization ကို တွက်သဖြင့် decode အဆင့်တိုင်းတွင် operation အရေအတွက် တင်စေပါသည်။ numerical stabilization မလုပ်လျှင် exp တန်ဖိုးများ ကြီးလွန်းသဖြင့် overflow ဖြစ်ပြီး non-finite တန်ဖိုးများ ထွက်နိုင်ပါသည်။ ထို့ကြောင့် ၎င်းသည် output အရည်အသွေးသာမက run တည်ငြိမ်မှုနှင့်လည်း ဆက်စပ်ပါသည်။

#### Activation Function

Activation Function သည် linear သို့မဟုတ် affine layer ပြီးနောက် nonlinearity ကို ထည့်သွင်းပါသည်။ nonlinearity မရှိလျှင် layer မည်မျှ ထပ်စေကာမူ model သည် affine transformation တစ်ခုသို့ ကျုံ့ဝင်သဖြင့် capacity သည် အလဟသ ဖြစ်ပါသည်။ compute အရ အသုံးများသည့် ရွေးချယ်မှုများသည် element-wise ဖြစ်သဖြင့် matrix operation များထက် ကုန်ကျစရိတ် နည်းပါသည်။ ရွေးချယ်မှုသည် gradient စီးဆင်းမှုကို ဆုံးဖြတ်သဖြင့် run အလုပ်ဖြစ်မှုအပေါ် တိုက်ရိုက် သက်ရောက်ပါသည်။

#### ReLU

ReLU သည် `f(x) = max(0, x)` ဟု သတ်မှတ်သည့် activation အမျိုးအစား ဖြစ်ပါသည်။ compute အရ ၎င်းသည် တွက်ချက်မှု သက်သာပြီး positive ဘက်တွင် saturation မဖြစ်သဖြင့် ကျယ်ပြန့်စွာ အသုံးပြုပါသည်။ သို့သော် negative input များတွင် gradient သုည ဖြစ်ခြင်းသည် အလုပ်မလုပ်တော့သည့် unit များကို ဖြစ်ပေါ်စေနိုင်ပါသည်။ ထို unit များ များလာလျှင် model ၏ effective capacity ကျဆင်းသဖြင့် run ပိုကြာပါသည်။

#### Eigenvalue

Eigenvalue သည် linear transformation တစ်ခုကို သက်ဆိုင်သည့် eigenvector ၏ ဦးတည်ချက် မပြောင်းဘဲ မည်မျှ ချဲ့ သို့မဟုတ် ကျုံ့ လုပ်သည်ကို ဖော်ပြသည့် scalar ဖြစ်ပါသည်။ training တွင် အမြင့်ဆုံး eigenvalue သည် objective ၏ အမြင့်ဆုံး curvature ကို ကိုယ်စားပြုသဖြင့် တည်ငြိမ်သည့် learning rate ၏ upper bound ကို သတ်မှတ်ပါသည်။ ရိုးရှင်းသည့် quadratic တွင် ထို bound သည် `2 / lambda_max` ဖြစ်ပါသည်။ ထို့ကြောင့် ဤကိန်းသည် lr ကို အစမ်းသပ် မလုပ်မီ ခန့်မှန်းရာတွင် အသုံးဝင်ပါသည်။

### မိသားစု (င) — generalization၊ data နှင့် ဖွဲ့စည်းပုံ

#### Overfitting

Overfitting သည် training data အပေါ် စွမ်းဆောင်ရည်သည် မမြင်ရသေးသည့် data အပေါ် စွမ်းဆောင်ရည်ထက် သိသိသာသာ ပိုကောင်းနေသည့် generalization gap ဖြစ်ပါသည်။ ကုန်ကျစရိတ် အရ ၎င်းသည် ထပ်လောင်း GPU-hours ကို generalization အကျိုးအမြတ် မရဘဲ ဖြုန်းတီးခြင်း ဖြစ်ပါသည်။ ထို့ကြောင့် training metric ကောင်းခြင်းကို run အောင်မြင်ခြင်း အဖြစ် မသတ်မှတ်ရပါ။ held-out metric နှင့် နှိုင်းယှဉ်ခြင်းသည် ဆက်လေ့ကျင့်ရန် သို့မဟုတ် ရပ်ရန် ဆုံးဖြတ်ချက်ကို ပေးပါသည်။

#### Underfitting

Underfitting သည် model သို့မဟုတ် training setup တွင် training data အတွင်း အသုံးဝင်သည့် ပုံစံများကို ဖမ်းယူရန် လုံလောက်သည့် capacity၊ optimization သို့မဟုတ် training signal မရှိခြင်း ဖြစ်ပါသည်။ training loss ပင် လုံလောက်စွာ မကျဆင်းလျှင် training အချိန် ထပ်တိုးခြင်းသည် ကုန်ကျစရိတ် ဖြုန်းတီးခြင်း ဖြစ်ပါသည်။ ထို့ကြောင့် data နှင့် optimization ကို အရင် စစ်ဆေးရမည် ဖြစ်ပါသည်။ ထို့နောက်မှ capacity၊ feature သို့မဟုတ် regularization ကို ချိန်ညှိရပါသည်။

#### Data Augmentation

Data Augmentation သည် ပြောင်းလဲထားသည့် နမူနာများ ဖန်တီး၍ training diversity ကို တိုးစေပါသည်။ wall-clock အရ ၎င်း၏ ကုန်ကျစရိတ်သည် host CPU တွင် ဖြစ်ပေါ်သဖြင့် host သည် accelerator ကို စောင့်စေနိုင်ပါသည်။ ထို အခြေအနေတွင် utilisation ကျဆင်းပြီး run ကုန်ကျစရိတ် တက်လာပါသည်။ ထို့ကြောင့် pipeline throughput ကို step အချိန်နှင့် တွဲဖက် တိုင်းတာရပါသည်။

#### Transfer Learning

Transfer Learning သည် data distribution သို့မဟုတ် objective တစ်ခုအပေါ် သင်ယူထားသည့် representation များမှ စတင်ပါသည်။ ကုန်ကျစရိတ် အရ ၎င်းသည် အစမှ လေ့ကျင့်ရသည့် pretraining token budget ကို ဖယ်ရှားပါသည်။ သို့သော် transfer ဖြစ်နိုင်သည့် အစိတ်အပိုင်းများနှင့် update မဟာဗျူဟာသည် architecture နှင့် task အပေါ် မှီခိုပါသည်။ source နှင့် target task များ သိသိသာသာ ကွာခြားလျှင် အောင်မြင်သည့် transfer ကို အာမမခံနိုင်ပါ။

#### Contrastive Learning

Contrastive Learning သည် embedding space အတွင်း ဆင်တူသည့် pair များကို ပိုနီးစေပြီး မတူညီသည့် pair များကို ပိုဝေးစေခြင်းဖြင့် training လုပ်ပါသည်။ compute အရ similarity matrix ၏ အရွယ်အစားသည် batch တစ်ခုလျှင် pair အရေအတွက်အပေါ် quadratic တိုးသဖြင့် ကြီးသည့် batch ကို လိုပါသည်။ ထို batch လိုအပ်ချက်သည် activation memory ကို တင်စေပါသည်။ ထို့ကြောင့် ဤနည်းလမ်းသည် VRAM ဖိအား မြင့်သည့် ကုန်ကျစရိတ်ဖြင့် လာပါသည်။

### မိသားစု (စ) — adaptation နှင့် alignment

#### Fine-tuning

Fine-tuning သည် pretrained parameter များမှ စတင်ပြီး ပိုကျဉ်းသည့် dataset သို့မဟုတ် objective အပေါ် training ကို ဆက်လုပ်ပါသည်။ ကုန်ကျစရိတ် အရ ၎င်းသည် pretraining ထက် token ပမာဏ နည်းသော်လည်း parameter အားလုံးကို update လုပ်လျှင် memory လိုအပ်ချက်သည် base model အရွယ်အစားအတိုင်း ရှိနေပါသည်။ ဥပမာ (ခ) တွင် 7.0B model ၏ weight၊ gradient နှင့် optimizer state စုစုပေါင်းသည် 78.231 GiB ဖြစ်ပါသည်။ ထို့ကြောင့် adaptation နည်းလမ်း ရွေးချယ်မှုသည် memory ဆုံးဖြတ်ချက် ဖြစ်ပါသည်။

#### LoRA (Low-Rank Adaptation)

LoRA သည် base weight များကို ရပ်တန့်ထားပြီး ရွေးချယ်ထားသည့် layer များအတွက် low-rank update matrix များကို သင်ယူပါသည်။ memory အရ trainable parameter အရေအတွက် ကျဆင်းသဖြင့် gradient နှင့် optimizer state သည် ထို adapter အပေါ်တွင်သာ တွက်ပါသည်။ သို့သော် base weight များ ကိုယ်တိုင် VRAM တွင် ရှိနေဆဲ ဖြစ်ပါသည်။ သက်သာမှု၏ ပမာဏသည် rank၊ target module၊ optimizer state၊ activation memory နှင့် အကောင်အထည်ဖော်မှု အပေါ် မှီခိုသည့်အတွက် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

#### QLoRA

QLoRA သည် pretrained base model ကို low-bit quantized ပုံစံဖြင့် ရပ်တန့်ထားပြီး LoRA adapter များကို လိုအပ်သည့်နေရာတွင် တိကျမှု မြင့်သည့် computation ဖြင့် train လုပ်ပါသည်။ memory အရ base bytes ကျဆင်းသဖြင့် ကတ်တစ်လုံးတည်းဖြင့် ကြီးသည့် model ကို adapt လုပ်နိုင်ပါသည်။ သို့သော် သက်သာမှုနှင့် အရည်အသွေးသည် model၊ rank၊ optimizer၊ sequence အရှည်၊ hardware နှင့် အကောင်အထည်ဖော်မှု အပေါ် မှီခိုပါသည်။ ထို့ကြောင့် memory ပမာဏ အတိအကျ တစ်ခုကို ကြိုတင် အာမခံ၍ မရပါ။

#### SFT (Supervised Fine-Tuning)

SFT သည် input နှင့် လိုချင်သည့် အဖြေ တွဲဖက်ထားသည့် နမူနာများအပေါ် pretrained model ကို fine-tune လုပ်ပါသည်။ ကုန်ကျစရိတ်သည် နမူနာ အရေအတွက်၊ အရှည်နှင့် epoch အရေအတွက်၏ မြှောက်လဒ် ဖြစ်ပါသည်။ ဤအဆင့်၏ ရလဒ်သည် နမူနာ အရည်အသွေးအပေါ် တိုက်ရိုက် မှီခိုသဖြင့် data cleaning သည် ကုန်ကျစရိတ် သက်သာစေသည့် ရင်းနှီးမြှုပ်နှံမှု ဖြစ်ပါသည်။ ထို့ကြောင့် SFT run ကို နမူနာ အရေအတွက်ဖြင့်သာ မတိုင်းတာရပါ။

#### DPO (Direct Preference Optimization)

DPO သည် preferred နှင့် rejected အဖြေ pair များမှ policy ကို reference policy နှင့် နှိုင်းယှဉ်၍ တိုက်ရိုက် train လုပ်ပါသည်။ cost per run အရ ၎င်းသည် reward model run နှင့် reinforcement-learning loop ကို ဖယ်ရှားသဖြင့် pipeline အဆင့် နည်းပါသည်။ ဤအချက်က ကုန်ကျစရိတ် ခန့်မှန်းမှုကို ပိုမို ရိုးရှင်းစေပါသည်။ သို့သော် ရလဒ်သည် preference data ၏ အရည်အသွေးနှင့် လွှမ်းခြုံမှုအပေါ် မှီခိုဆဲ ဖြစ်ပါသည်။

#### RLHF (Reinforcement Learning from Human Feedback)

RLHF သည် လူ၏ တုံ့ပြန်ချက်မှ reward သို့မဟုတ် preference signal ကို သင်ယူပြီး ထို signal ကို ဆန့်ကျင်သည့် အနေဖြင့် policy ကို optimize လုပ်ပါသည်။ cost per run အရ ၎င်းသည် reward model နှင့် RL အဆင့် နှစ်ခုကို ထပ်တင်သဖြင့် GPU-hours ကို အဆင့်အလိုက် တွက်ရပါသည်။ အကောင်အထည်ဖော်မှုများ ကွဲပြားသဖြင့် အားလုံး တူညီသည့် algorithm ကို အသုံးပြုရန် မလိုအပ်ပါ။ ထို့ကြောင့် capacity ခန့်မှန်းမှုတွင် အဆင့်တိုင်း၏ ကုန်ကျစရိတ်ကို ခွဲခြား မှတ်တမ်းတင်ရပါသည်။

#### Knowledge Distillation

Knowledge Distillation သည် teacher model ၏ ရွေးချယ်ထားသည့် အပြုအမူ သို့မဟုတ် output distribution များကို student model က ပုံတူပွားစေရန် train လုပ်ပါသည်။ cost per run အရ teacher run ကို ဦးစွာ လိုသဖြင့် စုစုပေါင်း GPU-hours သည် student တစ်ခုတည်း၏ run ထက် ပိုပါသည်။ အကျိုးအမြတ်မှာ ပိုသေးငယ် သို့မဟုတ် ပိုသက်သာသည့် model ကို serve နိုင်ခြင်း ဖြစ်ပါသည်။ ထို့ကြောင့် ဤရွေးချယ်မှုကို serving cost နှင့် တွဲဖက် တွက်ရပါသည်။

### မိသားစု (ဆ) — compute framework

#### JAX

JAX သည် numerical function များကို automatic differentiation၊ compilation၊ vectorization နှင့် accelerator များအကြား parallel execution ဖြင့် အသွင်ပြောင်းသည့် Python library ဖြစ်ပါသည်။ compute အရ ၎င်းသည် achieved FLOPs နှင့် peak FLOPs အကြား အချိုးကို အထောက်အကူ ပြုပါသည်၊ kernel များကို compile လုပ်၍ run သောကြောင့် ဖြစ်ပါသည်။ သို့သော် ၎င်း၏ transformation များသည် state ကို ရှင်းလင်းစွာ ဖော်ပြသည့် functional-style code နှင့် အကောင်းဆုံး အလုပ်လုပ်ပါသည်။ မကိုက်ညီသည့် အခြေအနေတွင် model code ကို ပြန်ရေးရသဖြင့် engineering အချိန် ကုန်ကျစရိတ် တက်လာပါသည်။

## ၄။ လက်တွေ့ တွက်ချက်မှု သုံးခု

ဤအပိုင်းရှိ output အားလုံးသည် အောက်တွင် ဖော်ပြသည့် command များကို တကယ် run ၍ ရရှိသည့် ရလဒ်များ ဖြစ်ပါသည်။ script များသည် standard library သာ အသုံးပြုပြီး deterministic ဖြစ်ပါသည်။

### (က) မော်ဒယ် ၁.၃B ၏ training memory — fp32၊ fp16၊ bf16 နှင့် activation checkpointing

ဖော်မြူလာ — `weights = params × bytes_per_parameter`၊ `gradients = params × bytes_per_parameter`၊ `optimizer = params × 8` (Adam fp32 moment ၂ ခု)၊ `activations = batch × seq × layers × d_model × act_factor × bytes_per_parameter`။ ယူဆချက် — params 1.3B၊ layers 24၊ d_model 2048၊ seq 2048၊ batch 8၊ act_factor 10 (checkpointing off) နှင့် 2 (on)၊ accelerator တစ်လုံးလျှင် 80 GB ဖြစ်ပြီး 16 GiB ကို သီးသန့်ထားသဖြင့် 64 GiB အသုံးပြုနိုင်သည်။

```text
$ python3 guides/01_math_and_training/scripts/ex_a_training_memory.py
================================================================================================
example (a) training memory - stated model, batch and precision
params=1.3B  layers=24  d_model=2048  seq=2048  batch=8
assumptions: gradients in the weight dtype, Adam keeps two fp32 moments,
             act_factor=10 per layer per token (2 with checkpointing)
------------------------------------------------------------------------------------------------
dtype   B/param    weights   gradients   optimizer   act(off)   act(on)  total(off)  total(on)
fp32        4.0      4.843       4.843       9.686     30.000     6.000      49.372     25.372
fp16        2.0      2.421       2.421       9.686     15.000     3.000      29.529     17.529
bf16        2.0      2.421       2.421       9.686     15.000     3.000      29.529     17.529
------------------------------------------------------------------------------------------------
all values above are GiB, fixed components are identical across dtype
largest batch that fits one 80 GB accelerator with 16 GiB reserved (64 GiB usable):
dtype         checkpointing=off         checkpointing=on
fp32                         11                       59
fp16                         26                      131
bf16                         26                      131
------------------------------------------------------------------------------------------------
activation checkpointing divides activation memory by 5x and raises the largest batch
that fits; it does not change weights, gradients or optimizer state.
================================================================================================
```

ရလဒ်က activation memory သည် weight နှင့် optimizer state ထက် ကြီးမားနိုင်သည်ကို ပြပါသည်၊ checkpointing off တွင် fp16 activation သည် 15.000 GiB ဖြစ်ပြီး checkpointing on တွင် 3.000 GiB သို့ ကျဆင်းပါသည်။ ထို့ကြောင့် အကြီးဆုံး batch သည် 26 မှ 131 သို့ တက်လာပါသည်။

### (ခ) optimizer state memory — SGD နှင့် Adam၊ တစ်ကတ်ပေါ် ဆံ့သည့် batch

ဖော်မြူလာ — `weights = params × 2`၊ `gradients = params × 2` (fp16)၊ ထို့နောက် optimizer state ကို `SGD 0 byte`၊ `SGD + momentum 4 byte`၊ `Adam / AdamW 8 byte`၊ `8-bit moment 2 byte` အဖြစ် ထည့်သည်။ တစ်လိုင်း အရေအတွက်ကို `(usable − fixed) ÷ act_per_sequence` ဖြင့် တွက်ပါသည်။ ယူဆချက် — params 7.0B၊ layers 32၊ d_model 4096၊ seq 2048၊ usable 64 GiB။

```text
$ python3 guides/01_math_and_training/scripts/ex_b_optimizer_state.py
================================================================================================
example (b) optimizer-state memory - Adam versus SGD
params=7.0B  layers=32  d_model=4096  seq=2048  weights+gradients=fp16 (2 B/param)
activations per sequence: 5.000 GiB off, 1.000 GiB on activation checkpointing
usable budget 64 GiB on one 80 GB accelerator (16 GiB reserved)
------------------------------------------------------------------------------------------------
optimizer               B/param state GiB   fixed GiB   batch off    batch on
SGD (no state)              0.0     0.000      26.077           7          37
SGD + momentum              4.0    26.077      52.154           2          11
Adam (fp32 moments)         8.0    52.154      78.231           0           0
AdamW (fp32 moments)        8.0    52.154      78.231           0           0
Adam (8-bit moments)        2.0    13.039      39.116           4          24
------------------------------------------------------------------------------------------------
Adam state is 52.154 GiB per 7.0B model, SGD without momentum keeps none.
that difference buys 10.4 extra sequences of activation memory at seq=2048.
an 8-bit moment copy halves the state to 13.039 GiB and raises the batch that fits.
weights 13.039 GiB and gradients 13.039 GiB are unchanged by the optimizer choice.
================================================================================================
```

ဤဇယားက optimizer ရွေးချယ်မှုသည် memory ဆုံးဖြတ်ချက် ဖြစ်သည်ကို ပြပါသည် — Adam ၏ fp32 moment ၂ ခုသည် 52.154 GiB ဖြစ်သဖြင့် weight နှင့် gradient နှစ်ခုစုစုပေါင်း 26.077 GiB ထက် နှစ်ဆ ပိုစားပါသည်။ SGD မှ Adam သို့ ရွှေ့လျှင် ဆံ့သည့် batch သည် ၇ မှ ၀ သို့ ကျဆင်းပြီး 8-bit moment ဖြင့် ပြန်တက်လာပါသည်။

### (ဂ) step time နှင့် run ကုန်ကျစရိတ် — token ၁၀၀B၊ GPU တစ်နာရီ USD 2.50

ဖော်မြူလာ — `step FLOPs = 6 × params × tokens_per_step`၊ `step seconds = step FLOPs ÷ (utilisation × peak)`၊ `cost = accelerator-hours × price_per_hour`၊ checkpointing အတွက် step FLOPs ကို 8/6 ဖြင့် မြှောက်သည်။ ယူဆချက် — token budget 100.0B၊ params 7.0B၊ batch 8၊ seq 2048၊ peak 1000 TFLOP/s fp16၊ accelerator ၁ လုံး။

```text
$ python3 guides/01_math_and_training/scripts/ex_c_step_cost.py
================================================================================================
example (c) step time and cost - stated token budget and GPU-hour price
budget=100.0B tokens  batch=8  seq=2048  tokens/step=16384
step FLOPs = 6 * params * tokens per step = 6.8813e+14 FLOPs
optimizer steps = 100.0B / 16384 = 6103515
peak 1000 TFLOP/s fp16 per accelerator, price USD 2.50 per accelerator-hour
------------------------------------------------------------------------------------------------
utilisation  achieved TFLOP/s   step seconds   wall-clock h    GPU-hours       cost USD
20%                     200.0          3.441         5833.3       5833.3       14583.33
40%                     400.0          1.720         2916.7       2916.7        7291.67
60%                     600.0          1.147         1944.4       1944.4        4861.11
------------------------------------------------------------------------------------------------
activation checkpointing recomputes one forward pass: step FLOPs x 1.333 (= 8/6).
utilisation  achieved TFLOP/s   step seconds   wall-clock h    GPU-hours       cost USD
20%                     200.0          4.588         7777.8       7777.8       19444.44
40%                     400.0          2.294         3888.9       3888.9        9722.22
60%                     600.0          1.529         2592.6       2592.6        6481.48
------------------------------------------------------------------------------------------------
at 40% utilisation the budget costs USD 7291.67 and 2916.7 accelerator-hours without checkpointing.
the same budget costs USD 9722.22 with checkpointing: 33.3% more accelerator time.
doubling utilisation halves wall-clock and cost; the FLOPs are unchanged.
================================================================================================
```

ရလဒ်က utilisation သည် cost ၏ အဓိက knob ဖြစ်သည်ကို ပြပါသည် — utilisation ၂၀ ရာခိုင်နှုန်းမှ ၆၀ ရာခိုင်နှုန်းသို့ တင်လျှင် GPU-hours သည် 5833.3 မှ 1944.4 သို့ ကျဆင်းပါသည်။ activation checkpointing သည် memory ကို ဝယ်ယူသည့် အစား accelerator အချိန် ၃၃.၃ ရာခိုင်နှုန်း ပိုပေးရပါသည်၊ ဤလဲလှယ်မှုသည် ဥပမာ (က) ၏ activation ကိန်းနှင့် တိုက်ရိုက် တွဲလျက် ရှိပါသည်။

## ၅။ ဤနယ်ပယ်မှ ဆင်းသက်လာသည့် လေ့ကျင့်ရေး ဆုံးဖြတ်ချက် ခြောက်ခု

**၁။ Precision နှင့် dtype သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Mixed Precision၊ Weight၊ Gradient၊ NaN (Not a Number)။ ရွေ့လျားသည့် မက်ထရစ် — bytes per parameter၊ weight GiB၊ step FLOPs။ ဥပမာ (က) အရ fp16 သည် fp32 ၏ ထက်ဝက်ကို နေရာယူပါသည်၊ weight အပိုင်းတွင် 2.421 GiB နှင့် 4.843 GiB ဖြစ်ပါသည်။

**၂။ Optimizer ရွေးချယ်ခြင်း** — မှီခိုသည့် term များ — Adam (Optimizer)၊ AdamW၊ Stochastic Gradient Descent (SGD)၊ Optimizer။ ရွေ့လျားသည့် မက်ထရစ် — optimizer state GiB နှင့် ဆံ့သည့် batch အရေအတွက်။ ဥပမာ (ခ) အရ Adam မှ SGD သို့ ရွှေ့လျှင် 52.154 GiB ပြန်ရပြီး ဆံ့သည့် batch သည် ၀ မှ ၇ သို့ တက်လာပါသည်။

**၃။ Activation checkpointing ဖြန့်ကျက်ခြင်း** — မှီခိုသည့် term များ — Activation Checkpointing၊ Batch Size၊ Gradient Accumulation။ ရွေ့လျားသည့် မက်ထရစ် — activation GiB နှင့် step FLOPs။ ဥပမာ (က) က activation ကို ၅ ဆ လျှော့ပြီး ဥပမာ (ဂ) က step FLOPs 8/6 ဆ တင်သည်ကို ပြပါသည်။

**၄။ Batch နှင့် microbatch အစီအစဉ် သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Batch Size၊ Gradient Accumulation၊ Epoch၊ Data Augmentation။ ရွေ့လျားသည့် မက်ထရစ် — tokens per step၊ step အရေအတွက်နှင့် host pipeline အချိန်။ ဥပမာ (ဂ) တွင် tokens per step 16384 ဖြစ်သဖြင့် token ၁၀၀B အတွက် step ၆,၁၀၃,၅၁၅ ခု လိုပါသည်။

**၅။ Learning rate နှင့် schedule သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Learning Rate၊ Learning Rate Schedule၊ Warmup၊ Gradient Clipping။ ရွေ့လျားသည့် မက်ထရစ် — mean lr၊ loss အစဉ်၊ critical တန်ဖိုး 2(1+momentum)/lambda_max။ ဤနယ်ပယ်၏ critical တန်ဖိုးသည် objective ၏ အမြင့်ဆုံး curvature အပေါ် မှီခိုပါသည်၊ ထို့ကြောင့် lr ကို ခန့်မှန်းရာတွင် ၎င်းကို အထက်ကန့်သတ်ချက် အဖြစ် သုံးရပါသည်။

**၆။ Run ကုန်ကျစရိတ် စောင့်ကြည့်ခြင်း** — မှီခိုသည့် term များ — Hyperparameter၊ Fine-tuning၊ LoRA (Low-Rank Adaptation)၊ QLoRA၊ Knowledge Distillation။ ရွေ့လျားသည့် မက်ထရစ် — GPU-hours၊ cost per run၊ trainable params။ ဥပမာ (ဂ) အရ utilisation နှစ်ဆ တင်လျှင် run တစ်ခုလုံး၏ ကုန်ကျစရိတ် ထက်ဝက် ကျဆင်းပါသည်၊ ထို့ကြောင့် ကုန်ကျစရိတ် လျှော့ချမှုသည် အရင် အဆင့်တွင် utilisation ကို တိုင်းတာခြင်းမှ စရပါသည်။

## လေ့ကျင့်ခန်း ဆက်စပ်မှု

ဤစာတမ်းရှိ ဖော်မြူလာများကို `guides/01_math_and_training/labs/lab_gradient_step.py`၊ `lab_schedule.py` နှင့် `lab_memory.py` တို့ဖြင့် လက်တွေ့ စမ်းသပ်နိုင်ပါသည်။ အပိုင်း ၄ ၏ script သုံးခုသည် `scripts/ex_a_training_memory.py`၊ `scripts/ex_b_optimizer_state.py` နှင့် `scripts/ex_c_step_cost.py` ဖြစ်ပါသည်။ ဤစာတမ်းရှိ ကိန်းဂဏန်းများသည် lab များ ရှိခြင်း အပေါ် မှီခိုသည် မဟုတ်ပါ။

## References

- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed၊ `rohitg00/ai-engineering-from-scratch`။
- ဤနယ်ပယ်၏ term ရှင်းလင်းချက် — `terms/01_math_and_training.md`။
- ဤနယ်ပယ်၏ term အစဉ် အခြေခံ — `glossary/by_area/01_math_and_training.json`။
- [Chain Rule and Automatic Differentiation](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/01-math-foundations/05-chain-rule-and-autodiff/)
- [Backpropagation from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/03-deep-learning-core/03-backpropagation/)
- [Activation Functions](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/03-deep-learning-core/04-activation-functions/)
- [Introduction to JAX](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/03-deep-learning-core/12-intro-to-jax/)
