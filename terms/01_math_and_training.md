# Math & Training (01) — သင်္ချာနှင့် training

ဤဖိုင်သည် လေ့လာနယ်ပယ် **01 — Math & training** ၏ term **၄၂** ခုကို အင်္ဂလိပ် + မြန်မာ နှစ်ဘာသာဖြင့်
စုစည်းထားသည့် ကိုးကား ဖြစ်သည်။ ဤနယ်ပယ်သည် model တစ်ခုကို training လုပ်သည့်အခါ အခြေခံ အကျဆုံး
ဖြစ်သည့် အသုံးအနှုန်းများ — loss၊ gradient၊ optimizer၊ learning rate၊ regularization၊ training memory
နှင့် ကိန်းဂဏန်း တိကျမှု — ကို ဖုံးလွှမ်းသည်။

ဤ term များသည် တစ်ခုချင်း သီးခြား မဟုတ်ဘဲ ကွင်းဆက် တစ်ခုအဖြစ် အလုပ်လုပ်သည်။ forward pass က loss ကို
ထုတ်ပေးပြီး၊ backpropagation နှင့် autograd က gradient ကို တွက်ချက်ကာ၊ optimizer သည် ထို gradient ကို
parameter update အဖြစ် အသွင်ပြောင်းသည်။ learning rate နှင့် schedule၊ batch size၊ weight decay ကဲ့သို့
hyperparameter များက ထို update ၏ တည်ငြိမ်မှုနှင့် generalization ကို ဆုံးဖြတ်သည်။ ထို့ကြောင့်
မည်သည့် အစိတ်အပိုင်း ပျက်ကွက်နေသည်ကို ခွဲခြား သိရှိရန် term တိုင်းကို ဆက်စပ် term များနှင့်တကွ
မှတ်သားရန် လိုအပ်သည်။

entry တိုင်းကို အောက်ပါအတိုင်း ဖတ်ရမည် — **မြန်မာ** တွင် term ၏ မြန်မာ အမည် သို့မဟုတ် အနီးစပ်ဆုံး
ဖော်ပြချက်၊ **ဆိုလိုသည့် အဓိပ္ပာယ်** တွင် အင်ဂျင်နီယာ အသုံးအနှုန်းအရ တကယ် ဆိုလိုသည့် အဓိပ္ပာယ်၊
**အရေးပါသည့် အကြောင်းရင်း** တွင် မည်သည့် စနစ်တွင် မည်သို့ သက်ရောက်သည်၊ **မကြာခဏ ရောထွေးမှု**
နှင့် **လက်တွေ့** တွင် အလွယ်တကူ မှားတတ်သည့် အချက်နှင့် လက်တွေ့ လုပ်ဆောင်ရမည့် အချက်၊
**ဆက်စပ် term များ** တွင် နောက်တစ်ဆင့် ဖတ်ရမည့် term များ၊ **English (source)** တွင် source ၏ မူရင်း
အင်္ဂလိပ် စာသား byte တူညီစွာ ပါဝင်သည်။ source တွင် အချက်အလက် မပါသော field (confusion၊
practice၊ learn) များကို ချန်လှပ်ထားသည်။ နည်းပညာ အသုံးအနှုန်းများ (gradient၊ optimizer၊ loss၊
tensor၊ dtype၊ checkpoint၊ quantization …) ကို မြန်မာ စာကြောင်းအတွင်း အင်္ဂလိပ်အတိုင်း ထားရှိသည်။

### Activation Checkpointing

**မြန်မာ:** Activation ပြန်လည် တွက်ချက်ခြင်း (activation checkpointing)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** training memory ကို လျှော့ချသည့် နည်းပညာ တစ်ခု ဖြစ်သည်။ forward pass အတွင်း activation အားလုံးကို မသိမ်းဆည်းဘဲ ရွေးချယ်ထားသည့် အချို့ကိုသာ သိမ်းဆည်းထားပြီး၊ backpropagation လုပ်ငန်းစဉ်အတွင်း ချန်ထားခဲ့သည့် activation များကို ပြန်လည် တွက်ချက် (recompute) ရသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** memory သတ်မှတ်ချက် တစ်ခုအတွင်း ပိုကြီးသည့် model သို့မဟုတ် ပိုရှည်သည့် sequence များကို train လုပ်နိုင်ရန် အထောက်အကူ ဖြစ်သည်။ activation သိမ်းဆည်းမှုကို လျှော့ချသည့် အစား computation ပိုလုပ်ရသဖြင့် memory နှင့် အချိန် လဲလှယ်သည့် နည်းလမ်း ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Activation checkpointing သည် အမြဲတည်ရှိသည့် training checkpoint မဟုတ်ပါ။ forward နှင့် backward တစ်ကြိမ်စာ memory ထဲ ဆံ့စေရန် ကူညီသည်၊ သို့သော် ပြိုလဲသွားသည့် run ကို ပြန်လည် စတင်နိုင်ရန် (resume) မပြုလုပ်ပေးပါ။
- **လက်တွေ့:** memory အများဆုံး စားသည့် transformer block များကို checkpoint လုပ်ပါ၊ အပိုကျသည့် step အချိန်ကို တိုင်းတာပါ၊ recovery checkpoint များနှင့် activation ပြန်တွက်ချက်မှု setting များကို သီးခြား ထားရှိပါ။
- **ဆက်စပ် term များ:** Autograd, Backpropagation, Checkpoint, Mixed Precision
- **English (source):** A training-memory technique that saves only selected forward-pass activations and recomputes the omitted ones during backpropagation. It lets you train larger models or sequences within a fixed memory budget by trading additional computation for lower activation storage.

### Activation Function

**မြန်မာ:** Activation function (အပိုဒ်များကြား nonlinear လုပ်ဆောင်ချက်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** linear သို့မဟုတ် affine layer တစ်ခုပြီးနောက် အသုံးပြုသည့် function ဖြစ်ပြီး nonlinearity ကို ထည့်သွင်းပေးသည်။ မထည့်သွင်းပါက weights နှင့် biases ဖြင့် စုစည်းထားသည့် layer များသည် affine transformation တစ်ခုတည်းအဖြစ် ကျုံ့ဝင်သွားသည်။ ReLU၊ GELU နှင့် SiLU တို့သည် အသုံးများသည့် ရွေးချယ်မှုများ ဖြစ်သည်။ ရွေးချယ်မှုသည် training အတွင်း gradient စီးဆင်းမှုကို တိုက်ရိုက် သက်ရောက်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** nonlinearity မရှိပါက layer မည်မျှ ထပ်စေကာမူ model သည် affine transformation တစ်ခုထက် မပိုနိုင်သဖြင့်၊ activation function သည် network ကို ပိုရှုပ်ထွေးသည့် function များ ဖော်ပြနိုင်စေသည်။ ထို့အပြင် gradient စီးဆင်းမှုကို ဆုံးဖြတ်သဖြင့် training အလုပ်ဖြစ်မှုကိုပါ သက်ရောက်သည်။
- **ဆက်စပ် term များ:** ReLU, Gradient, Backpropagation
- **Learn it:** [Activation Functions](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/03-deep-learning-core/04-activation-functions/)
- **English (source):** A function applied after a linear or affine layer that introduces nonlinearity. Without it, composing layers with weights and biases collapses to one affine transformation. ReLU, GELU, and SiLU are common choices. The choice directly affects whether gradients flow during training.

### Adam (Optimizer)

**မြန်မာ:** Adam (optimizer တစ်မျိုး)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** Adaptive Moment Estimation ဖြစ်သည်။ gradient ၏ exponential average နှင့် squared gradient ၏ exponential average ကို ပေါင်းစပ်ပြီး bias correction ကို အသုံးပြုကာ parameter တစ်ခုချင်းစီအတွက် update scale ကို ချိန်ညှိပေးသည်။ အသုံးဝင်သည့် baseline တစ်ခု ဖြစ်သော်လည်း သင့်တော်သည့် learning rate နှင့် schedule ကို လိုအပ်ဆဲ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Adam သည် gradient ကို parameter တစ်ခုချင်းစီအလိုက် ချိန်ညှိ (adapt) ပေးသဖြင့် လက်တွေ့ training တွင် အလွန်အသုံးများသည့် baseline optimizer ဖြစ်လာသည်။ update အရွယ်အစား အတိအကျကို learning rate နှင့် schedule က ဆုံးဖြတ်ဆဲ ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Adam သည် အားကောင်းသည့် baseline ဖြစ်သည်၊ အားလုံးအတွက် အကောင်းဆုံး optimizer မဟုတ်ပါ။
- **ဆက်စပ် term များ:** AdamW, Optimizer, Learning Rate
- **English (source):** Adaptive Moment Estimation. It combines an exponential average of gradients with an exponential average of squared gradients, applies bias correction, and adapts the update scale per parameter. It is a useful baseline, but it still needs a suitable learning rate and schedule.

### AdamW

**မြန်မာ:** AdamW (weight decay ကို ခွဲထုတ်ထားသည့် Adam)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** weight decay ကို gradient အပေါ် အခြေခံသည့် parameter update မှ ခွဲထုတ် (decouple) ထားသည့် Adam မျိုးကွဲ ဖြစ်သည်။ ထို့ကြောင့် Adam ၏ adaptive scale ခံထားသည့် gradient အတွင်း L2 penalty ထည့်သည့် နည်းလမ်းထက် ကျုံ့ဝင်သည့် အပြုအမူကို ပိုမို နားလည်လွယ်စေသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** weight decay နှင့် gradient update ကို ခွဲထုတ်ထားသဖြင့် parameter ကျုံ့ဝင်သည့် အပြုအမူကို ခန့်မှန်းရ လွယ်ကူပြီး regularization ၏ အာနိသင်ကို ပိုမို ထိန်းချုပ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Decoupled weight decay သည် AdamW ကို အားလုံးအတွက် အကောင်းဆုံး ဖြစ်စေသည်မဟုတ်ပါ။ model၊ data နှင့် training scale က အကောင်းဆုံး optimizer နှင့် schedule ကို ဆုံးဖြတ်ဆဲ ဖြစ်သည်။
- **ဆက်စပ် term များ:** Adam (Optimizer), Weight Decay, Optimizer
- **English (source):** An Adam variant that decouples weight decay from the gradient-based parameter update. That makes the shrinkage behavior easier to reason about than adding an L2 penalty inside Adam's adaptively scaled gradient.

### Autograd

**မြန်မာ:** Autograd (အလိုအလျောက် gradient တွက်ချက်သည့် စနစ်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** tensor operation များကို မှတ်တမ်းတင်ခြင်း သို့မဟုတ် အသွင်ပြောင်းခြင်း ပြုလုပ်ပြီး derivative များကို တွက်ချက်နိုင်သည့် စနစ် ဖြစ်သည်။ များသောအားဖြင့် reverse-mode automatic differentiation ကို အသုံးပြုသည်။ အသုံးပြုသူက forward computation ကိုသာ ရေးသားရပြီး backpropagation အတွက် လိုအပ်သည့် gradient များကို framework က ဆင်းသက် ထုတ်ပေးသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** gradient များကို လက်ဖြင့် ဆင်းသက် တွက်ချက်ရန် မလိုတော့သဖြင့် layer များစွာ ပါဝင်သည့် model ကြီးများကို လက်တွေ့ train လုပ်နိုင်သည်။ ၎င်းသည် backpropagation ကို အလိုအလျောက် လုပ်ဆောင်ပေးသည့် အခြေခံ ယန္တရား ဖြစ်သည်။
- **ဆက်စပ် term များ:** Backpropagation, Gradient, Tensor
- **Learn it:** [Chain Rule and Automatic Differentiation](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/01-math-foundations/05-chain-rule-and-autodiff/)
- **English (source):** A system that records or transforms tensor operations so it can compute derivatives, usually with reverse-mode automatic differentiation. You write the forward computation and the framework derives the gradients needed for backpropagation.

### Backpropagation

**မြန်မာ:** Backpropagation (နောက်သို့ ဆင်းသက် ဖြန့်တွက်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** scalar loss တစ်ခုမှ computation graph အတွင်း နောက်သို့ derivative များကို ဖြန့်ပေးသည့် chain rule ၏ ထိရောက်သည့် အသုံးချမှု ဖြစ်သည်။ ၎င်းသည် gradient များကို တွက်ချက်ပေးသည်၊ optimizer က ထို gradient များဖြင့် parameter များကို update လုပ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** parameter update တိုင်း၏ အခရာ ဖြစ်သည့် gradient များကို ထုတ်ပေးသဖြင့် neural network သင်ယူမှု တစ်ခုလုံး၏ အခြေခံ ယန္တရား ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Backpropagation သည် gradient များကို တွက်ချက်သည်။ update rule သို့မဟုတ် learning rate ကို ရွေးချယ်ခြင်း မဟုတ်ပါ။
- **ဆက်စပ် term များ:** Autograd, Gradient, Optimizer
- **Learn it:** [Backpropagation from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/03-deep-learning-core/03-backpropagation/)
- **English (source):** An efficient application of the chain rule that propagates derivatives from a scalar loss backward through a computation graph. It computes gradients; an optimizer uses those gradients to update parameters.

### Batch Size

**မြန်မာ:** Batch size (တစ်ကြိမ် တွဲဖက် တွက်ချက်သည့် နမူနာ အရေအတွက်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** optimizer update တစ်ကြိမ် မတိုင်မီ gradient ခန့်မှန်းချက် တစ်ခုအတွက် loss များ ပါဝင်သည့် နမူနာ (example) အရေအတွက် ဖြစ်သည်။ batch ကြီးပါက hardware အသုံးချမှု တိုးတက်နိုင်ပြီး gradient noise လျော့နိုင်သည်၊ သို့သော် memory ပိုလိုအပ်ကာ learning rate သို့မဟုတ် scheduling ရွေးချယ်မှုများ ကွဲပြားရနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** batch size သည် update တစ်ကြိမ်၏ gradient ခန့်မှန်းချက် ယုံကြည်စိတ်ချရမှု၊ memory အသုံးပြုမှုနှင့် learning rate ရွေးချယ်မှုကို တစ်ပြိုင်နက် သက်ရောက်သဖြင့် training တစ်ခုလုံး၏ အပြုအမူကို ဆုံးဖြတ်သည့် အဓိက အချက် ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** batch size ၏ အတိုင်းအတာ (range) သို့မဟုတ် batch တိုင်း တိုးလာသည့်အလိုက် learning rate ကို တူညီစွာ တိုးရမည်ဟု ဆိုသည့် စည်းမျဉ်း အားလုံးအတွက် သက်ဆိုင်သည့် တစ်ခု မရှိပါ။
- **ဆက်စပ် term များ:** Learning Rate, Gradient, Optimizer
- **English (source):** The number of examples whose losses contribute to one gradient estimate before an optimizer update. Larger batches can improve hardware utilization and reduce gradient noise, but they require more memory and may need different learning-rate or scheduling choices.

### Contrastive Learning

**မြန်မာ:** Contrastive learning (နှိုင်းယှဉ်၍ သင်ယူခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** embedding space အတွင်း ဆင်တူသည့် pair များကို ပိုနီးစေပြီး မတူညီသည့် pair များကို ပိုဝေးစေခြင်းဖြင့် training လုပ်သည့် နည်းလမ်း ဖြစ်သည်။ CLIP သည် ဤနည်းလမ်းကို အသုံးပြုသည် — ကိုက်ညီသည့် image-text pair နှင့် မကိုက်ညီသည့် pair များကို ခွဲခြားစေသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** target label ကို တိုက်ရိုက် မသတ်မှတ်ဘဲ pair ၏ တူညီမှု သို့မဟုတ် မတူညီမှု အခြေအနေမှ ဆင်တူမှု ဖွဲ့စည်းပုံကို သင်ယူသဖြင့်၊ ဆင်တူမှု တိုင်းတာနိုင်သည့် representation များ လိုအပ်သည့် စနစ်များအတွက် အသုံးဝင်သည်။
- **ဆက်စပ် term များ:** Embedding, Cosine Similarity, Loss Function
- **English (source):** Training by pulling similar pairs closer and pushing dissimilar pairs apart in embedding space. CLIP uses this: matching image-text pairs vs non-matching ones.

### Cross-Entropy

**မြန်မာ:** Cross-entropy (classification loss)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ရည်မှန်း ရလဒ် (target outcome) အတွက် သတ်မှတ်ထားသည့် probability ၏ negative log အပေါ် အခြေခံသည့် loss ဖြစ်သည်။ next-token training တွင် တွေ့ရှိသည့် နောက် token အတွက် model က probability နည်းစွာ သတ်မှတ်ပါက ထို model ကို အရင့်အရောက် ခံစေသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** language model pretraining အပါအဝင် classification လုပ်ငန်းစဉ် အများစုတွင် အသုံးပြုသည့် loss ဖြစ်သဖြင့် training က မည်သည့် အမှားကို တိုက်ရိုက် အရင့်အရောက် ခံစေသည်ကို ဆုံးဖြတ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Perplexity သည် ပျမ်းမျှ cross-entropy ကို exponent တင်ထားသည့် တန်ဖိုး ဖြစ်သည်မှာ ပျမ်းမျှ တွက်သည့် နည်းလမ်းနှင့် logarithm ၏ base ကို တစ်သမတ်တည်း သတ်မှတ်ထားသည့်အခါတွင်သာ ဖြစ်သည်။
- **ဆက်စပ် term များ:** Loss Function, Softmax, Perplexity
- **English (source):** A loss based on the negative log probability assigned to the target outcome. In next-token training, it penalizes the model when it assigns low probability to the observed next token.

### Data Augmentation

**မြန်မာ:** Data augmentation (training data တိုးချဲ့ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ပြောင်းလဲထားသည့် နမူနာများ — ရုပ်ပုံ အသွင်ပြောင်းခြင်း၊ အသံ နှောင့်ယှက်ခြင်း၊ စာသား ပြန်လည် ရေးသားခြင်း ကဲ့သို့ — ကို ဖန်တီးပြီး source data အသစ် လုံးလုံး စုဆောင်းခြင်း မလိုဘဲ training diversity ကို တိုးစေသည်။ transformation သည် task signal ကို မပျက်စီးစေပါက overfitting ကို လျှော့ချနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** training data ကို မြင်ရသည့် ပုံစံ အမျိုးမျိုးအဖြစ် တိုးပွားစေသဖြင့် model သည် အဓိပ္ပာယ် မပြောင်းသည့် ကွဲပြားမှုများအပေါ် ပိုမို ခံနိုင်ရည် ရှိလာစေသည်။
- **မကြာခဏ ရောထွေးမှု:** Augmentation တစ်ခုသည် model သင်ယူစေလိုသည့် target label သို့မဟုတ် အပြုအမူကို မပျက်စီးစေရပါ။
- **ဆက်စပ် term များ:** Overfitting, Epoch, Eval Set
- **English (source):** Creating modified examples, such as transformed images, perturbed audio, or paraphrased text, to increase training diversity without collecting entirely new source data. It can reduce overfitting when the transformation preserves the task signal.

### DPO (Direct Preference Optimization)

**မြန်မာ:** DPO (Direct Preference Optimization — နှစ်သက်မှုကို တိုက်ရိုက် ချိန်ညှိခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** နှစ်သက်သည့် (preferred) နှင့် ပယ်ချသည့် (rejected) အဖြေ pair များမှ policy ကို reference policy နှင့် နှိုင်းယှဉ်၍ တိုက်ရိုက် train လုပ်သည့် preference-optimization objective ဖြစ်သည်။ ဤအဆင့်တွင် သီးခြား reward model တစ်ခု လည်းကောင်း၊ reinforcement-learning loop တစ်ခု လည်းကောင်း run လုပ်ရန် မလိုအပ်ပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** reward model နှင့် reinforcement learning အဆင့် မလိုဘဲ preference data ကို တိုက်ရိုက် အသုံးပြုသဖြင့် pipeline ပိုရိုးရှင်းပြီး ထိန်းချုပ်ရ လွယ်ကူသည်။
- **မကြာခဏ ရောထွေးမှု:** DPO သည် preference data ၏ အရည်အသွေးနှင့် လွှမ်းခြုံမှုအပေါ် မှီခိုဆဲ ဖြစ်ပြီး evaluation သို့မဟုတ် alignment အန္တရာယ်ကို ဖယ်ရှားပေးသည်မဟုတ်ပါ။
- **ဆက်စပ် term များ:** RLHF (Reinforcement Learning from Human Feedback), SFT (Supervised Fine-Tuning), Alignment
- **Learn it:** [Direct Preference Optimization](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/10-llms-from-scratch/08-dpo/)
- **English (source):** A preference-optimization objective that trains a policy directly from preferred and rejected response pairs relative to a reference policy. It avoids running an explicit reward model and reinforcement-learning loop during this stage.

### Dropout

**မြန်မာ:** Dropout (activation များကို ကျပန်း ပိတ်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** training အတွင်း activation အချို့ကို ကျပန်း သုည သတ်မှတ်ခြင်းဖြင့် network သည် activation လမ်းကြောင်း တစ်ခုတည်းအပေါ် မှီခိုခြင်း မဖြစ်စေရန် အားပေးသည်။ ပုံမှန် inference တွင် ပိတ်ထားလေ့ ရှိသည်၊ သို့သော် Monte Carlo dropout သည် uncertainty ကို ခန့်မှန်းရန် တမင် ဖွင့်ထားသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** activation လမ်းကြောင်း တစ်ခုတည်းအပေါ် မှီခိုမှုကို လျှော့ချသဖြင့် overfitting ကို တိုက်ဖျက်ရန် အသုံးပြုသည့် regularization နည်းလမ်း ဖြစ်သည်။ inference နှင့် training အပြုအမူ ကွာခြားမှုကို နားလည်ထားရန် လိုအပ်သည်။
- **ဆက်စပ် term များ:** Overfitting, Weight Decay, Activation Function
- **English (source):** During training, randomly setting a fraction of activations to zero encourages the network not to rely on one activation path. It is normally disabled for standard inference, although Monte Carlo dropout deliberately keeps it active to estimate uncertainty.

### Eigenvalue

**မြန်မာ:** Eigenvalue (linear transformation ၏ ကိုယ်ပိုင်တန်ဖိုး)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** linear transformation တစ်ခုသည် သက်ဆိုင်သည့် nonzero eigenvector ၏ ဦးတည်ချက်ကို မပြောင်းလဲဘဲ ၎င်းကို မည်မျှ ချဲ့ သို့မဟုတ် ကျုံ့ လုပ်သည်ကို ဖော်ပြသည့် scalar ဖြစ်သည်။ covariance matrix ကို အသုံးပြုသည့် PCA တွင် eigenvalue ကြီးသည့် ဦးတည်ချက်များသည် variance ပိုများသည့် ဦးတည်ချက်များ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အရေးကြီးသည့် ဦးတည်ချက် (variance များသည့် ဦးတည်ချက်) များကို ခွဲထုတ်ရန် အသုံးပြုသဖြင့် dimension လျှော့ချခြင်း (dimensionality reduction) နှင့် feature တည်ဆောက်မှုတွင် အခြေခံ အချက် ဖြစ်သည်။
- **ဆက်စပ် term များ:** Tensor, Feature, Latent Space
- **English (source):** A scalar that describes how a linear transformation scales a corresponding nonzero eigenvector without changing its direction. In covariance-matrix PCA, larger eigenvalues correspond to directions with more variance.

### Epoch

**မြန်မာ:** Epoch (training data တစ်ကြိမ် ဖြတ်သွားခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် training dataset ကို တစ်ကြိမ် ဖြတ်သွားခြင်း (traversal) ဖြစ်သည်။ distributed သို့မဟုတ် sampling ပါဝင်သည့် training တွင် epoch ၏ တိကျသည့် အကောင်အထည်ဖော်မှုသည် data loader နှင့် sampling policy အပေါ် မူတည်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** training လုပ်သည့် ပမာဏကို တိုင်းတာသည့် အခြေခံ ယူနစ် ဖြစ်သဖြင့် training အရှည်နှင့် dataset အရွယ်အစားကို နှိုင်းယှဉ်သတ်မှတ်ရာတွင် အသုံးပြုသည်။
- **မကြာခဏ ရောထွေးမှု:** Epoch ပိုများလာခြင်းသည် generalization ပိုကောင်းလာမည်ဟု အာမမခံပါ၊ held-out data အပေါ် အကဲဖြတ်ရမည်။
- **ဆက်စပ် term များ:** Batch Size, Overfitting, Eval Set
- **English (source):** One traversal of the defined training dataset. In distributed or sampled training, the exact implementation of an epoch depends on the data loader and sampling policy.

### Fine-tuning

**မြန်မာ:** Fine-tuning (ဆက်လက်၍ ချိန်ညှိ training လုပ်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** pretrained parameter များမှ စတင်ပြီး ပိုကျဉ်းသည့် dataset သို့မဟုတ် objective အပေါ် training ကို ဆက်လက် လုပ်ခြင်း ဖြစ်သည်။ နည်းလမ်းအပေါ် မူတည်၍ parameter အားလုံး၊ ရွေးချယ်ထားသည့် parameter များ၊ သို့မဟုတ် ထည့်သွင်းထားသည့် adapter parameter များကို update လုပ်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Fine-tuning သည် အပြုအမူ၊ style၊ format သို့မဟုတ် task စွမ်းဆောင်ရည်ကို ပြုပြင်နိုင်သည်၊ သို့သော် အချက်အလက်များ (facts) လက်ရှိ ဖြစ်နေရန် သို့မဟုတ် ခြေရာခံနိုင်ရန် လိုအပ်သည့်အခါ retrieval ကို ယုံကြည်စိတ်ချစွာ အစားထိုးနိုင်သည့် နည်းလမ်း မဟုတ်ပါ။
- **မကြာခဏ ရောထွေးမှု:** Fine-tuning သည် သင်ယူထားသည့် အသိပညာကို သက်ရောက်နိုင်သည်၊ သို့သော် model အတွင်းရှိ ရှာဖွေနိုင်သည့် database တစ်ခုသို့ မှတ်တမ်းများ ရိုးရှင်းစွာ ထပ်ဖြည့်သည့် သဘောမျိုး မဟုတ်ပါ။
- **ဆက်စပ် term များ:** SFT (Supervised Fine-Tuning), LoRA (Low-Rank Adaptation), QLoRA, RAG (Retrieval-Augmented Generation)
- **Learn it:** [Fine-Tuning and LoRA](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/08-fine-tuning-lora/)
- **English (source):** Continuing training from pretrained parameters on a narrower dataset or objective. Depending on the method, you may update all parameters, selected parameters, or added adapter parameters. Fine-tuning can adapt behavior, style, format, or task performance, but it is not a dependable replacement for retrieval when facts must stay current or traceable.

### Gradient

**မြန်မာ:** Gradient (တိမ်းစောင်းမှု vector)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အမြန်ဆုံး တိုးပွားသည့် (steepest increase) ဦးတည်ချက်သို့ ညွှန်းသည့် partial derivative များ၏ vector ဖြစ်သည်။ ML တွင် loss ကို အနည်းဆုံး ဖြစ်စေရန် gradient ၏ ဆန့်ကျင်ဘက် ဦးတည်ချက်သို့ သွားသည် (gradient descent)။
- **အရေးပါသည့် အကြောင်းရင်း:** loss ကို လျှော့ချရန် parameter များကို မည်သည့် ဦးတည်ချက်သို့ မည်မျှ ရွှေ့ရမည်ကို ဖော်ပြသဖြင့် optimizer အားလုံး၏ input ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Optimizer များသည် ရိုးရိုး negative-gradient step ကို မလုပ်ဘဲ gradient များကို အသွင်ပြောင်းခြင်း၊ ပျမ်းမျှခြင်း၊ clip လုပ်ခြင်း သို့မဟုတ် ချိန်ညှိခြင်း ပြုလုပ်နိုင်သည်။
- **ဆက်စပ် term များ:** Backpropagation, Gradient Descent, Optimizer
- **English (source):** A vector of partial derivatives pointing in the direction of steepest increase. In ML, you go opposite to the gradient (gradient descent) to minimize the loss.

### Gradient Accumulation

**မြန်မာ:** Gradient accumulation (gradient များကို စုဆောင်းခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** optimizer update တစ်ကြိမ် မလုပ်မီ microbatch အများအပြားမှ gradient များကို ပေါင်း သို့မဟုတ် ပျမ်းမျှ ယူခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** စက် (device) တစ်လုံးတည်းတွင် နမူနာနှင့် activation အားလုံးကို တစ်ပြိုင်နက် မထည့်နိုင်သည့်အခါ ပိုကြီးသည့် effective batch ကို အနီးစပ်ဆုံး ရရှိစေသည်။
- **မကြာခဏ ရောထွေးမှု:** Gradient accumulation သည် step တစ်ကြိမ်စာ activation memory ကို လျှော့ချပေးသည်၊ သို့သော် batch အပြည့်ကို တစ်ပြိုင်နက် စီမံခြင်း၏ အရည်အချင်း အားလုံးကို ပြန်လည် ဖော်ပြပေးသည်မဟုတ်ပါ။
- **လက်တွေ့:** loss ကို တစ်သမတ်တည်း scale လုပ်ပါ၊ ရွေးချယ်ထားသည့် microbatch အရေအတွက် ပြည့်မှသာ optimizer ကို ခေါ်ပါ၊ normalization သို့မဟုတ် distributed synchronization က အပြုအမူကို ပြောင်းလဲစေသလား တိုင်းတာပါ။
- **ဆက်စပ် term များ:** Batch Size, Mixed Precision, Optimizer, Backpropagation
- **English (source):** Summing or averaging gradients from several microbatches before performing one optimizer update. It lets you approximate a larger effective batch when one device cannot hold all examples and activations at once.

### Gradient Clipping

**မြန်မာ:** Gradient clipping (gradient ကို ကန့်သတ်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** gradient တန်ဖိုးများ သို့မဟုတ် ၎င်းတို့၏ စုစုပေါင်း norm သည် ရွေးချယ်ထားသည့် threshold ကို ကျော်လွန်သည့်အခါ optimizer update မတိုင်မီ ကန့်သတ်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ပုံမှန်မဟုတ်စွာ ကြီးမားသည့် gradient တစ်ခုသည် training step တစ်ခုကို မတည်ငြိမ်စေဘဲ non-finite တန်ဖိုးများ ဖြစ်ပေါ်စေခြင်းကို တားဆီးနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Clipping သည် update အရွယ်အစားကို ထိန်းချုပ်သည်၊ မမှန်ကန်သည့် data၊ ပျက်နေသည့် loss သို့မဟုတ် အမြဲတမ်း မသင့်တော်သည့် learning rate ကို ပြုပြင်ပေးသည့် နည်းလမ်း မဟုတ်ပါ။
- **လက်တွေ့:** clip မလုပ်ရသေးသည့် norm များကို log မှတ်ပါ၊ mixed-precision gradient များကို unscale လုပ်ပြီးမှ clip လုပ်ပါ၊ ထပ်ခါတလဲလဲ clip ဖြစ်ခြင်းကို မတည်ငြိမ်မှု ရှာဖွေခြင်း၏ အစားထိုးအဖြစ် မသဘောထားဘဲ စုံစမ်းစစ်ဆေးပါ။
- **ဆက်စပ် term များ:** Gradient, NaN (Not a Number), Mixed Precision, Learning Rate
- **English (source):** Limiting gradient values or their combined norm before an optimizer update when they exceed a chosen threshold. It can prevent an unusually large gradient from destabilizing a training step and producing non-finite values.

### Gradient Descent

**မြန်မာ:** Gradient descent (gradient အသုံးပြု၍ အနည်းဆုံးသို့ ဆင်းခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** objective ၏ negative gradient ကို အသုံးပြု၍ parameter များကို ရွှေ့သည့် optimization update အုပ်စု တစ်ခု ဖြစ်သည်။ များသောအားဖြင့် dataset တစ်ခုလုံး အစား batch များမှ ခန့်မှန်းထားသည့် gradient ကို အသုံးပြုသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** optimizer အားလုံးနီးပါးသည် ဤအခြေခံ နည်းလမ်းပေါ်မှ တည်ဆောက်ထားသဖြင့် update များ အလုပ်လုပ်သည့် ပုံစံကို နားလည်ရန် အခြေခံ ဖြစ်သည်။
- **ဆက်စပ် term များ:** Gradient, Learning Rate, Optimizer
- **English (source):** A family of optimization updates that move parameters using the negative gradient of an objective, usually estimated from batches rather than the entire dataset.

### Hyperparameter

**မြန်မာ:** Hyperparameter (ကြိုတင် သတ်မှတ်သည့် configuration တန်ဖိုး)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ပုံမှန် model parameter အဖြစ် သင်ယူခြင်း မရှိဘဲ model တည်ဆောက်ပုံ၊ optimization၊ data ပြုပြင်ခြင်း သို့မဟုတ် inference ကို ပုံဖော်သည့် configuration ရွေးချယ်မှု ဖြစ်သည်။ ဥပမာ — learning rate၊ batch size၊ layer အရေအတွက်နှင့် decoding setting များ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** hyperparameter ရွေးချယ်မှုသည် parameter များ မသင်ယူမီ ကတည်းက model ၏ တည်ဆောက်ပုံနှင့် training အပြုအမူကို ကန့်သတ် သတ်မှတ်ပေးသဖြင့် ရလဒ်ကို တိုက်ရိုက် သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** hyperparameter အချို့ကို training မစမီ ရွေးချယ်ရပြီး၊ အချို့ကို schedule အတွင်း သို့မဟုတ် inference အချိန်တွင် ပြောင်းလဲနိုင်သည်။
- **ဆက်စပ် term များ:** Parameter, Learning Rate, Batch Size, Temperature
- **English (source):** A configuration choice that shapes model structure, optimization, data processing, or inference rather than being learned as an ordinary model parameter. Examples include learning rate, batch size, layer count, and decoding settings.

### JAX

**မြန်မာ:** JAX (numerical function များကို အသွင်ပြောင်းသည့် Python library)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** numerical function များကို automatic differentiation၊ compilation၊ vectorization နှင့် accelerator များအကြား parallel execution ဖြင့် အသွင်ပြောင်းနိုင်သည့် Python library ဖြစ်သည်။ ၎င်း၏ transformation များသည် state ကို ရှင်းလင်းစွာ ဖော်ပြသည့် functional-style code နှင့် အကောင်းဆုံး အလုပ်လုပ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** accelerator အပေါ် numerical computation ကို compile လုပ်၍ run နိုင်ရန် ခွင့်ပြုပြီး autograd၊ vectorization နှင့် parallel execution ကို function transformation အဖြစ် ပူးတွဲ ရရှိစေသည်။
- **မကြာခဏ ရောထွေးမှု:** JAX သည် state ပါဝင်သည့် programming ကို လုံးဝ တားမြစ်သည်မဟုတ်ပါ၊ သို့သော် transformation ခံထားသည့် function အတွင်း ဖုံးကွယ်ထားသည့် mutation သည် မှားယွင်းသည့် သို့မဟုတ် မပံ့ပိုးသည့် အပြုအမူကို ဖြစ်ပေါ်စေနိုင်သည်။
- **ဆက်စပ် term များ:** Autograd, Tensor, CUDA
- **Learn it:** [Introduction to JAX](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/03-deep-learning-core/12-intro-to-jax/)
- **English (source):** A Python library for transforming numerical functions with automatic differentiation, compilation, vectorization, and parallel execution across accelerators. Its transformations work best with explicit state and functional-style code.

### Knowledge Distillation

**မြန်မာ:** Knowledge distillation (သင်ယူထားသည့် အပြုအမူ လွှဲပြောင်းခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ပိုစွမ်းဆောင်ရည် မြင့်သည့် teacher model မှ ရွေးချယ်ထားသည့် အပြုအမူ သို့မဟုတ် output distribution များကို ပုံတူပွားစေရန် student model တစ်ခုကို train လုပ်ခြင်း ဖြစ်ပြီး၊ များသောအားဖြင့် ပုံမှန် target label များနှင့် တွဲဖက် အသုံးပြုသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** teacher ကို တိုက်ရိုက် serve လုပ်ခြင်း လက်တွေ့ မဖြစ်နိုင်သည့်အခါ အသုံးဝင်သည့် အပြုအမူများကို ပိုသေးငယ် သို့မဟုတ် ပိုသက်သာသည့် model ထဲသို့ လွှဲပြောင်းနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Distillation သည် training distribution အပေါ်ရှိ အပြုအမူကို လွှဲပြောင်းပေးသည်၊ teacher ၏ စွမ်းရည်၊ အချက်အလက်နှင့် လုံခြုံရေး ဂုဏ်သတ္တိ အားလုံးကို ကူးယူပေးသည်မဟုတ်ပါ။
- **လက်တွေ့:** teacher output များ၊ temperature၊ student loss နှင့် held-out eval set ကို သတ်မှတ်ပါ၊ ထို့နောက် student ကို teacher နှင့်လည်းကောင်း၊ label သာ အသုံးပြုသည့် baseline နှင့်လည်းကောင်း နှိုင်းယှဉ်ပါ။
- **ဆက်စပ် term များ:** Fine-tuning, Loss Function, Logits, Quantization
- **English (source):** Training a student model to reproduce selected behavior or output distributions from a more capable teacher, often alongside ordinary target labels. It can transfer useful behavior into a smaller or cheaper model when serving the teacher directly is impractical.

### Learning Rate

**မြန်မာ:** Learning rate (သင်ယူမှု နှုန်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** optimizer က parameter update အရွယ်အစားကို ထိန်းချုပ်ရန် အသုံးပြုသည့် scale factor ဖြစ်သည်။ အလွန်ကြီးသည့် တန်ဖိုးများသည် training ကို မတည်ငြိမ်စေနိုင်ပြီး၊ အလွန်သေးငယ်သည့် တန်ဖိုးများသည် အသုံးဝင်သည့် တိုးတက်မှုကို လက်တွေ့ မဖြစ်နိုင်လောက်အောင် နှေးစေနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** update တစ်ကြိမ်စီ၏ အရွယ်အစားကို တိုက်ရိုက် သတ်မှတ်သဖြင့် training တည်ငြိမ်မှုနှင့် အလျင်နှုန်းကို ဆုံးဖြတ်သည့် အဓိက hyperparameter ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** အမှန်တကယ် ကျသင့်သည့် update သည် optimizer၊ schedule၊ gradient scale၊ batch နှင့် parameter များ၏ မှတ်တမ်း (history) အပေါ် မူတည်ဆဲ ဖြစ်သည်။
- **ဆက်စပ် term များ:** Optimizer, Gradient Descent, Batch Size
- **English (source):** A scale factor used by an optimizer to control parameter-update magnitude. Values that are too large can destabilize training; values that are too small can make useful progress impractically slow.

### Learning Rate Schedule

**မြန်မာ:** Learning rate schedule (learning rate ပြောင်းလဲသည့် အစီအစဉ်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** training တိုးတက်လာသည့်အလိုက် step၊ epoch၊ metric သို့မဟုတ် ကြိုတင် သတ်မှတ်ထားသည့် curve အပေါ် မူတည်၍ optimizer ၏ learning rate ကို ပြောင်းလဲစေသည့် မူဝါဒ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** training အဆင့် အမျိုးမျိုးသည် update scale အမျိုးမျိုးမှ အကျိုးရနိုင် ဖြစ်သဖင့် တန်ဖိုး တစ်ခုတည်း ကိန်းသေ ထားပါက အစပိုင်းတွင် မတည်ငြိမ်နိုင်ပြီး နောက်ပိုင်းတွင် အလဟသ ဖြစ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Scheduler သည် အချိန်နှင့်အမျှ learning rate ကို ထိန်းချုပ်သည်၊ optimizer step မည်သည့်အချိန်တွင် ဖြစ်မည်ကို ဆုံးဖြတ်ခြင်း သို့မဟုတ် convergence ကို အာမခံခြင်း မဟုတ်ပါ။
- **လက်တွေ့:** schedule ကို optimizer configuration နှင့်တကွ version မှတ်ပါ၊ step တိုင်းတွင် အမှန်တကယ် ရရှိသည့် rate ကို log မှတ်ပါ၊ token သို့မဟုတ် update budget တူညီသည့် အခြေအနေတွင် schedule များကို နှိုင်းယှဉ်ပါ။
- **ဆက်စပ် term များ:** Learning Rate, Warmup, Optimizer, Epoch
- **English (source):** A policy that changes the optimizer's learning rate as training progresses according to steps, epochs, metrics, or a predefined curve. Different training stages can benefit from different update scales, so one constant rate may be unstable early or wasteful late.

### LoRA (Low-Rank Adaptation)

**မြန်မာ:** LoRA (Low-Rank Adaptation — အနည်းငယ်သော parameter ဖြင့် ချိန်ညှိခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** base weight များကို ရပ်တန့် (freeze) ထားပြီး ရွေးချယ်ထားသည့် layer များအတွက် low-rank update matrix များကို သင်ယူသည့် နည်းလမ်း ဖြစ်သည်။ train လုပ်ရမည့် parameter အရေအတွက်ကို လျှော့ချပေးပြီး full-parameter fine-tuning နှင့် နှိုင်းယှဉ်ပါက training memory လျော့နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** parameter အားလုံးကို update လုပ်ရန် မလိုဘဲ ချိန်ညှိမှုကို ရရှိစေသဖြင့် model ကြီးများကို သက်သာသည့် အရင်းအမြစ်ဖြင့် adapt လုပ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** အမှန်တကယ် memory နှင့် အမြန်နှုန်း သက်သာမှုသည် rank၊ target module၊ optimizer state၊ activation memory၊ quantization နှင့် အကောင်အထည်ဖော်မှုအပေါ် မူတည်သည်။
- **ဆက်စပ် term များ:** Fine-tuning, QLoRA, Parameter
- **Learn it:** [Fine-Tuning and LoRA](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/08-fine-tuning-lora/)
- **English (source):** A method that keeps base weights frozen and learns low-rank update matrices for selected layers. It reduces the number of trainable parameters and can lower training memory relative to full-parameter fine-tuning.

### Loss Function

**မြန်မာ:** Loss function (ဆုံးရှုံးမှု တိုင်းတာသည့် function)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** prediction များနှင့် target များကို — တစ်ခါတစ်ရံ regularization term များနှင့်တကွ — optimization က လျှော့ချရန် ကြိုးစားသည့် တန်ဖိုး တစ်ခုသို့ map လုပ်သည့် objective ဖြစ်သည်။ loss သည် training က မည်သည့် အမှားကို တိုက်ရိုက် ဆုချ သို့မဟုတ် အရင့်အရောက် ခံစေသည်ကို ဆုံးဖြတ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** training တစ်ခုလုံး၏ ရည်မှန်းချက်ကို loss က သတ်မှတ်သဖင့် မှားယွင်းသည့် loss ရွေးချယ်မှုသည် model ကို လိုချင်သည့် အပြုအမူမဟုတ်သည့် အရာကို ဦးတည်စေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** training loss နည်းခြင်းသည် production task များအပေါ် အသုံးဝင်သည့်၊ လုံခြုံသည့် သို့မဟုတ် generalization ရှိသည့် အပြုအမူကို အာမမခံပါ။
- **ဆက်စပ် term များ:** Cross-Entropy, Gradient, Evaluation (Eval)
- **English (source):** An objective that maps predictions and targets, sometimes with regularization terms, to a value optimization tries to reduce. The loss determines which errors training directly rewards or penalizes.

### Mixed Precision

**မြန်မာ:** Mixed precision (တိကျမှု ရောစပ်၍ တွက်ချက်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** operation အမျိုးမျိုးအတွက် data type အမျိုးမျိုးကို အသုံးပြုသည့် numerical မဟာဗျူဟာ ဖြစ်သည်။ များသောအားဖြင့် matrix operation အများစုအတွက် တိကျမှု နည်းသည့် type ကို သုံးပြီး၊ range သို့မဟုတ် တည်ငြိမ်မှု ပိုလိုအပ်သည့် တန်ဖိုးများအတွက် တိကျမှု မြင့်သည့် type ကို သုံးသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** dtype ရွေးချယ်မှုသည် memory အသုံးပြုမှုနှင့် throughput ကို တိုက်ရိုက် သက်ရောက်သဖင့် ကြီးမားသည့် model များကို train လုပ်နိုင်မှုကို ဆုံးဖြတ်သည်။
- **မကြာခဏ ရောထွေးမှု:** အမြန်နှုန်း၊ memory နှင့် တိကျမှု သက်ရောက်မှုများသည် hardware၊ data type၊ scaling နည်းလမ်း၊ kernel နှင့် model အပေါ် မူတည်သည်။ ကိန်းသေ multiplier တစ်ခု မဟုတ်ပါ။
- **ဆက်စပ် term များ:** Tensor, CUDA, NaN (Not a Number), Quantization
- **English (source):** A numerical strategy that uses different data types for different operations, often lower precision for many matrix operations and higher precision for values that need more range or stability.

### NaN (Not a Number)

**မြန်မာ:** NaN (Not a Number — ကိန်းဂဏန်း မဟုတ်သည့် တန်ဖိုး)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မသတ်မှတ်နိုင်သည့် သို့မဟုတ် ဖော်ပြနိုင်မှု မရှိသည့် numerical ရလဒ်ကို ကိုယ်စားပြုသည့် floating-point တန်ဖိုး ဖြစ်သည်။ training တွင် NaN များသည် မမှန်ကန်သည့် operation၊ overflow၊ မတည်ငြိမ်သည့် normalization၊ အလွန်အကျွံ ကြီးသည့် update များ သို့မဟုတ် ယခင်ကတည်းက ပျက်စီးနေသည့် တန်ဖိုးများမှ ဖြစ်ပေါ်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** တန်ဖိုး တစ်ခု NaN ဖြစ်ပါက ၎င်းမှ ဆင်းသက်သည့် gradient နှင့် parameter များအားလုံး ပျက်စီးနိုင်သဖင့် training run တစ်ခုလုံး အသုံးမဝင်တော့ဘဲ ဖြစ်နိုင်သည်။
- **လက်တွေ့:** ပထမဆုံး non-finite tensor ကို ရှာပါ၊ ၎င်း၏ input များကို စစ်ဆေးပါ၊ ထို operation အနီးတွင် assertion သို့မဟုတ် anomaly detection ထည့်ပါ။
- **ဆက်စပ် term များ:** Mixed Precision, Learning Rate, Gradient
- **English (source):** A floating-point value representing an undefined or unrepresentable numerical result. In training, NaNs can come from invalid operations, overflow, unstable normalization, excessive updates, or earlier corrupted values.

### Normalization

**မြန်မာ:** Normalization (စံတန်ဖိုးအဖြစ် ချိန်ညှိခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် statistics များကို အသုံးပြု၍ input၊ activation သို့မဟုတ် feature များကို ပြန်လည် scale လုပ်ခြင်း သို့မဟုတ် ဗဟိုပြန် ချိန်ခြင်း ပြုလုပ်သည့် transformation အုပ်စု ဖြစ်သည်။ Batch normalization နှင့် layer normalization တို့သည် မတူညီသည့် axis များကို အသုံးပြုပြီး training နှင့် inference တွင် ကွဲပြားစွာ အပြုအမူ ရှိသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** activation များ၏ scale ကို ထိန်းညှိပေးသဖင့် optimization တည်ငြိမ်မှုကို တိုးတက်စေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Normalization သည် optimization တည်ငြိမ်မှုကို တိုးတက်စေနိုင်သည်၊ သို့သော် အမြဲတမ်း ပိုကြီးသည့် learning rate ကို ခွင့်ပြုပေးခြင်း သို့မဟုတ် architecture တိုင်းကို တိုးတက်စေခြင်း မဟုတ်ပါ။
- **ဆက်စပ် term များ:** Tensor, Activation Function, Mixed Precision
- **English (source):** A family of transformations that rescale or recenter inputs, activations, or features using defined statistics. Batch normalization and layer normalization use different axes and behave differently across training and inference.

### Optimizer

**မြန်မာ:** Optimizer (parameter များကို update လုပ်သည့် algorithm)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** gradient များကို parameter update များအဖြစ် အသွင်ပြောင်းသည့် algorithm ဖြစ်သည်။ ရိုးရှင်းသည့် stochastic gradient descent သည် အခြေခံ baseline ဖြစ်ပြီး၊ momentum၊ Adam နှင့် အခြား optimizer များသည် history သို့မဟုတ် adaptive scaling ကို အသုံးပြု၍ update ကို ပြောင်းလဲသည်။ ရွေးချယ်မှုတိုင်းတွင် memory၊ တည်ငြိမ်မှုနှင့် tuning အပြုအမူ ကွဲပြားသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** gradient ကို အသုံးချ၍ parameter များကို မည်သို့ ရွှေ့မည်ကို optimizer က ဆုံးဖြတ်သဖင့် training အမြန်နှုန်းနှင့် တည်ငြိမ်မှုကို တိုက်ရိုက် သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** Optimizer သည် gradient များကို စားသုံးသည်၊ backpropagation က ၎င်းတို့ကို တွက်ချက်ပေးသည်။
- **ဆက်စပ် term များ:** Adam (Optimizer), AdamW, Gradient, Learning Rate
- **English (source):** An algorithm that transforms gradients into parameter updates. Plain stochastic gradient descent is a simple baseline; momentum, Adam, and other optimizers change the update using history or adaptive scaling. Each choice has different memory, stability, and tuning behavior.

### Overfitting

**မြန်မာ:** Overfitting (training data အပေါ် အလွန်အကျွံ ကိုက်ညီခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** training data အပေါ် စွမ်းဆောင်ရည်သည် ကိုယ်စားပြုနိုင်သည့် မမြင်ရသေးသည့် (unseen) data အပေါ် စွမ်းဆောင်ရည်ထက် သိသိသာသာ ပိုကောင်းနေသည့် generalization gap ဖြစ်သည်။ memorization သည် အထောက်အကူ ဖြစ်နိုင်သော်လည်း လုပ်ငန်းသုံး လက္ခဏာမှာ generalization အားနည်းမှု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** training metric တစ်ခုတည်း ကောင်းနေခြင်းဖြင့် unseen data အပေါ် အလုပ်လုပ်နိုင်မည်ဟု မဆိုနိုင်သဖင့် held-out data အပေါ် အကဲဖြတ်ရမည် ဖြစ်သည်။
- **လက်တွေ့:** training metric နှင့် held-out metric များကို နှိုင်းယှဉ်ပါ၊ subgroup များတွင် ကျရှုံးမှုကို စစ်ဆေးပါ၊ data အရည်အသွေး၊ regularization၊ early stopping သို့မဟုတ် model capacity ကဲ့သို့ ပြောင်းလဲမှုများကို စမ်းသပ်ပါ။
- **ဆက်စပ် term များ:** Underfitting, Dropout, Weight Decay, Eval Set
- **English (source):** A generalization gap in which performance on training data is substantially better than performance on representative unseen data. Memorization can contribute, but the operational symptom is poor generalization.

### QLoRA

**မြန်မာ:** QLoRA (quantized base model နှင့် LoRA)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** pretrained base model ကို low-bit quantized ပုံစံဖြင့် ရပ်တန့် (freeze) ထားပြီး၊ LoRA adapter များကို လိုအပ်သည့်နေရာတွင် တိကျမှု မြင့်သည့် computation ဖြင့် train လုပ်သည့် parameter-efficient fine-tuning နည်းလမ်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ကြီးမားသည့် model များကို ချိန်ညှိရန် လိုအပ်သည့် memory ကို လျှော့ချနိုင်သည်၊ သို့သော် သက်သာမှုနှင့် အရည်အသွေးသည် model၊ rank၊ optimizer၊ sequence အရှည်၊ hardware နှင့် အကောင်အထည်ဖော်မှုအပေါ် မူတည်သည်။
- **မကြာခဏ ရောထွေးမှု:** QLoRA သည် memory အသုံးပြုမှု အတိအကျ တစ်ခုကို လည်းကောင်း၊ full fine-tuning နှင့် ကွာခြားသည့် အရည်အသွေး ကွာဟမှု ကိန်းသေ တစ်ခုကို လည်းကောင်း အာမမခံပါ။
- **ဆက်စပ် term များ:** LoRA (Low-Rank Adaptation), Quantization, Fine-tuning
- **Learn it:** [Fine-Tuning and LoRA](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/08-fine-tuning-lora/)
- **English (source):** A parameter-efficient fine-tuning method that keeps a pretrained base model frozen in a low-bit quantized representation while training LoRA adapters with higher-precision computation where needed. It can reduce the memory needed to adapt large models, but savings and quality depend on model, rank, optimizer, sequence length, hardware, and implementation.

### ReLU

**မြန်မာ:** ReLU (Rectified Linear Unit)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** `f(x) = max(0, x)` ဟု သတ်မှတ်သည့် Rectified Linear Unit ဖြစ်သည်။ တွက်ချက်မှု သက်သာပြီး positive ဘက်တွင် saturation မဖြစ်သည့် အကိုင်း ရှိသည်၊ သို့သော် negative input များတွင် gradient သုည ဖြစ်ခြင်းသည် အလုပ်မလုပ်တော့သည့် unit များကို ဖြစ်ပေါ်စေနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** activation function အဖြစ် ကျယ်ပြန့်စွာ အသုံးပြုသဖင့် gradient စီးဆင်းမှုနှင့် အလုပ်မလုပ်တော့သည့် unit ပြဿနာကို နားလည်ရန် အခြေခံ ဖြစ်သည်။
- **ဆက်စပ် term များ:** Activation Function, Gradient, CNN (Convolutional Neural Network)
- **English (source):** Rectified Linear Unit, defined as `f(x) = max(0, x)`. It is inexpensive and has a non-saturating positive branch, though zero gradients on negative inputs can create inactive units.

### RLHF (Reinforcement Learning from Human Feedback)

**မြန်မာ:** RLHF (လူ၏ တုံ့ပြန်ချက်မှ reinforcement learning)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** လူ၏ တုံ့ပြန်ချက် (human feedback) ကို အသုံးပြု၍ reward သို့မဟုတ် preference signal တစ်ခုကို သင်ယူပြီး၊ ထို signal ကို ဆန့်ကျင်သည့် အနေဖြင့် model policy ကို optimize လုပ်သည့် pipeline အုပ်စု ဖြစ်သည်။ အကောင်အထည်ဖော်မှုများ ကွဲပြားပြီး အားလုံး တူညီသည့် reinforcement-learning algorithm ကို အသုံးပြုရန် မလိုအပ်ပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** တိုက်ရိုက် တိုင်းတာ၍ မရသည့် အပြုအမူများကို လူ၏ ရွေးချယ်မှုမှ သင်ယူထားသည့် signal အဖြစ် ပြောင်းလဲပြီး policy ကို optimize လုပ်နိုင်သဖင့် လူ အကြိုက် အပြုအမူများကို training အဖြစ် ပြောင်းလဲစေသည်။
- **မကြာခဏ ရောထွေးမှု:** RLHF သည် စုဆောင်းထားသည့် တုံ့ပြန်ချက်မှ သင်ယူထားသည့် proxy တစ်ခုကို optimize လုပ်သည်။ အသုံးပြုသူနှင့် အခြေအနေ တိုင်းအတွက် ကျယ်ပြန့်သည့် alignment ကို အာမမခံပါ။
- **ဆက်စပ် term များ:** DPO (Direct Preference Optimization), SFT (Supervised Fine-Tuning), Alignment
- **Learn it:** [Reinforcement Learning from Human Feedback](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/10-llms-from-scratch/07-rlhf/)
- **English (source):** A family of pipelines that uses human feedback to learn a reward or preference signal and then optimizes a model policy against that signal. Implementations vary and need not all use the same reinforcement-learning algorithm.

### SFT (Supervised Fine-Tuning)

**မြန်မာ:** SFT (Supervised Fine-Tuning — နမူနာများဖြင့် ကြီးကြပ်၍ ချိန်ညှိခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** input နှင့် လိုချင်သည့် အဖြေ တွဲဖက်ထားသည့် နမူနာများအပေါ် pretrained model ကို fine-tune လုပ်ခြင်းဖြင့် training distribution အတွင်း ပြသထားသည့် အပြုအမူကို သင်ယူစေသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ပြသထားသည့် နမူနာ အရည်အသွေးက မည်သည့် အပြုအမူကို အရင့်အရောက် ခံစေသည်ကို ဆုံးဖြတ်သဖင့် data အရည်အသွေးသည် တိုက်ရိုက် အရေးပါသည်။
- **မကြာခဏ ရောထွေးမှု:** SFT သည် chat အပြုအမူထက် ကျော်လွန်၍ အပြုအမူ အများအပြားကို ချိန်ညှိနိုင်ပြီး၊ နမူနာ အရည်အသွေးက မည်သည့် အပြုအမူကို အရင့်အရောက် ခံစေသည်ကို ဆုံးဖြတ်သည်။
- **ဆက်စပ် term များ:** Fine-tuning, DPO (Direct Preference Optimization), RLHF (Reinforcement Learning from Human Feedback)
- **English (source):** Fine-tuning a pretrained model on paired inputs and desired responses so it learns the demonstrated behavior under the training distribution.

### Softmax

**မြန်မာ:** Softmax (logit များကို normalization လုပ်သည့် function)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** `softmax(x_i) = exp(x_i) / sum(exp(x_j))` ဟု သတ်မှတ်ပြီး numerical stabilization နှင့်တကွ အကောင်အထည်ဖော်လေ့ ရှိသည့် function ဖြစ်သည်။ output များသည် အပေါင်းလက္ခဏာ ဖြစ်ပြီး စုစုပေါင်း တစ်နှင့် ညီသဖင့် categorical distribution တစ်ခုအဖြစ် parameter သတ်မှတ်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** logit များကို အနက်ပြန်နိုင်သည့် distribution အဖြစ် ပြောင်းပေးသဖင့် sampling၊ cross-entropy loss တွက်ချက်မှုနှင့် attention weight များတွင် တိုက်ရိုက် အသုံးပြုသည်။
- **မကြာခဏ ရောထွေးမှု:** Softmax တန်ဖိုးများသည် လက်တွေ့ ကမ္ဘာ၏ မှန်ကန်မှုနှင့် ပတ်သက်၍ အလိုအလျောက် calibration ဖြစ်ပြီးသား probability များ မဟုတ်ပါ။
- **ဆက်စပ် term များ:** Temperature, Cross-Entropy, Attention
- **English (source):** A function defined by `softmax(x_i) = exp(x_i) / sum(exp(x_j))`, implemented with numerical stabilization. Its outputs are positive and sum to one, so they can parameterize a categorical distribution.

### Stochastic Gradient Descent (SGD)

**မြန်မာ:** Stochastic Gradient Descent (SGD — ကျပန်း gradient ဆင်းနည်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** dataset တစ်ခုလုံး အစား နမူနာ တစ်ခု သို့မဟုတ် minibatch တစ်ခုမှ ခန့်မှန်းထားသည့် gradient ဖြင့် parameter များကို update လုပ်သည့် optimizer အုပ်စု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** gradient noise၊ momentum၊ batch scaling နှင့် ခေတ်သစ် training တွင် အသုံးပြုသည့် adaptive optimizer များကို နားလည်ရန် အခြေခံ baseline ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** လက်ရှိ လက်တွေ့တွင် SGD ဆိုသည်မှာ များသောအားဖြင့် minibatch SGD ကို ဆိုလိုပြီး၊ ၎င်း၏ အသုံးဝင်သည့် learning rate သည် ကျင့်သုံးနိုင်သည့် batch-scaling စည်းမျဉ်း တစ်ခုတည်းကို မလိုက်နာပါ။
- **လက်တွေ့:** batch sampling၊ learning rate၊ အသုံးပြုပါက momentum နှင့် schedule ကို မှတ်တမ်းတင်ပါ၊ ထို့နောက် update သို့မဟုတ် token budget တူညီသည့် အခြေအနေတွင် validation အပြုအမူကို နှိုင်းယှဉ်ပါ။
- **ဆက်စပ် term များ:** Gradient Descent, Batch Size, Learning Rate, Optimizer
- **English (source):** An optimizer family that updates parameters from a gradient estimated on a sampled example or minibatch rather than the complete training dataset. It is the baseline for understanding gradient noise, momentum, batch scaling, and the adaptive optimizers used in modern training.

### Transfer Learning

**မြန်မာ:** Transfer learning (သင်ယူမှု လွှဲပြောင်းခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** data distribution သို့မဟုတ် objective တစ်ခုအပေါ် သင်ယူထားသည့် representation သို့မဟုတ် parameter များမှ စတင်ပြီး အခြား တစ်ခုအတွက် ချိန်ညှိခြင်း ဖြစ်သည်။ လွှဲပြောင်းနိုင်သည့် အစိတ်အပိုင်းများနှင့် update မဟာဗျူဟာသည် architecture နှင့် task အပေါ် မူတည်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ရှိပြီးသား representation များမှ စတင်သဖင့် task အသစ်အတွက် အခြေခံ အချက်အလက်ကို ပြန်လည် အသုံးချနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Transfer သည် နောက်ပိုင်း layer များတွင်သာ ကန့်သတ်ထားသည်မဟုတ်ပါ၊ source နှင့် target task များ သိသိသာသာ ကွာခြားသည့်အခါ အောင်မြင်သည့် transfer ကို အာမမခံပါ။
- **ဆက်စပ် term များ:** Fine-tuning, Feature, SFT (Supervised Fine-Tuning)
- **English (source):** Starting from representations or parameters learned on one data distribution or objective and adapting them for another. The transferable components and update strategy depend on architecture and task.

### Underfitting

**မြန်မာ:** Underfitting (လုံလောက်စွာ မလိုက်ညီနိုင်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** model သို့မဟုတ် training setup တစ်ခုတွင် training data အတွင်း အသုံးဝင်သည့် ပုံစံများကို ဖမ်းယူရန် လုံလောက်သည့် effective capacity၊ optimization၊ feature သို့မဟုတ် training signal မရှိခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** training loss ပင် လုံလောက်စွာ မကျဆင်းပါက model သည် task ကို သင်ယူနိုင်ခြင်း မရှိသေးသည်ကို ညွှန်းသဖင့် data နှင့် optimization ကို အရင် စစ်ဆေးရမည် ဖြစ်သည်။
- **လက်တွေ့:** data နှင့် optimization ကို အရင် စစ်ဆေးစမ်းသပ်ပါ၊ ထို့နောက်မှ training အချိန် ပိုရှည်စွာ လုပ်ခြင်း၊ feature ပြောင်းခြင်း၊ အလွန်အကျွံ regularization လျှော့ခြင်း သို့မဟုတ် သင့်လျော်သည့် capacity တိုးခြင်းကို စဉ်းစားပါ။
- **ဆက်စပ် term များ:** Overfitting, Loss Function, Hyperparameter
- **English (source):** A model or training setup has insufficient effective capacity, optimization, features, or training signal to capture useful patterns in the training data.

### Warmup

**မြန်မာ:** Warmup (learning rate ကို အစပိုင်းတွင် တဖြည်းဖြည်း တင်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** learning rate ကို သေးငယ်သည့် တန်ဖိုးမှ စတင်၍ အဓိက schedule ၏ ရည်မှန်း တန်ဖိုးသို့ တိုးတက်စေသည့် အစပိုင်း training အဆင့် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အစောပိုင်း gradient များနှင့် optimizer statistics များသည် — အထူးသဖြင့် large-batch သို့မဟုတ် transformer training တွင် — မတည်ငြိမ်နိုင်သဖင့် ချက်ချင်း အရွယ်အစား ပြည့် update လုပ်ခြင်းသည် optimization ကို ထိခိုက်စေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Warmup သည် model တိုင်းအတွက် မလိုအပ်ပါ၊ အခြားနည်းဖြင့် မသင့်တော်သည့် learning rate ကို လုံခြုံအောင်လည်း လုပ်ပေးသည်မဟုတ်ပါ။
- **လက်တွေ့:** warmup ကို step သို့မဟုတ် processed token အနေဖြင့် သတ်မှတ်ပါ၊ အမှန်တကယ် ရရှိသည့် curve ကို log မှတ်ပါ၊ batch၊ optimizer နှင့် စုစုပေါင်း training budget များကို မြင်သာစွာ ထားရှိပြီး tune လုပ်ပါ။
- **ဆက်စပ် term များ:** Learning Rate Schedule, Learning Rate, Batch Size, AdamW
- **English (source):** An initial training phase in which the learning rate rises from a smaller value toward the main schedule's target value. Early gradients and optimizer statistics can be unstable, especially in large-batch or transformer training, so abrupt full-size updates may damage optimization.

### Weight

**မြန်မာ:** Weight (သင်ယူထားသည့် ကိန်းရင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** model transformation တစ်ခုအတွင်း ရှိသည့် train လုပ်နိုင်သည့် coefficient ဖြစ်သည်။ weight များကို များသောအားဖြင့် tensor များအဖြစ် စီစဉ်ထားပြီး၊ optimization က training objective ကို လျှော့ချရန် ၎င်းတို့ကို ချိန်ညှိသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** weight များသည် model သင်ယူထားသည့် အချက်အလက် အဓိက သိုလှောင်ရာ ဖြစ်သဖင့် training က ၎င်းတို့ကို မည်သို့ ပြောင်းလဲသည်ကို နားလည်ရန် အခြေခံ ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** parameter တိုင်းကို weight ဟု ခေါ်သည်မဟုတ်ပါ — bias၊ embedding နှင့် normalization scale များလည်း parameter များ ဖြစ်သည်။
- **ဆက်စပ် term များ:** Parameter, Tensor, Optimizer
- **English (source):** A trainable coefficient in a model transformation. Weights are usually organized into tensors, and optimization adjusts them to reduce the training objective.

### Weight Decay

**မြန်မာ:** Weight decay (weight များကို ကျုံ့ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** training တစ်လျှောက် ရွေးချယ်ထားသည့် parameter များ၏ အရွယ်အစား (magnitude) ကို လျှော့ချသည့် update rule ဖြစ်ပြီး၊ များသောအားဖြင့် gradient update နှင့် သီးခြားစွာ weight များကို shrinkage factor တစ်ခုဖြင့် မြှောက်ခြင်းဖြင့် လုပ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** generalization ကို တိုးတက်စေနိုင်သည်၊ သို့သော် အသုံးဝင်သည့် coefficient နှင့် ဖယ်ထုတ်ရမည့် parameter အုပ်စုများသည် model၊ optimizer၊ schedule နှင့် data အပေါ် မူတည်သည်။
- **မကြာခဏ ရောထွေးမှု:** Decoupled weight decay သည် ရိုးရှင်းသည့် optimizer အချို့အတွက် L2 loss penalty နှင့် တူညီသည်၊ သို့သော် Adam ကဲ့သို့ adaptive optimizer များအတွက် ယေဘုယျအားဖြင့် တူညီသည်မဟုတ်ပါ။
- **ဆက်စပ် term များ:** AdamW, Overfitting, Optimizer
- **English (source):** An update rule that reduces selected parameter magnitudes over training, often by multiplying weights by a shrinkage factor separate from the gradient update. It can improve generalization, but the useful coefficient and excluded parameter groups depend on model, optimizer, schedule, and data.

## Self-check

1. Activation checkpointing နှင့် recovery အတွက် training checkpoint တို့၏ ကွာခြားချက်ကား အဘယ်နည်း။
2. Backpropagation နှင့် optimizer တို့၏ တာဝန်ကို မည်သို့ ခွဲခြားသနည်း။
3. Adam နှင့် AdamW တို့၏ ကွာခြားချက်ကား အဘယ်နည်း။
4. Gradient accumulation သည် မည်သည့် ပြဿနာကို ဖြေရှင်းပေးသနည်း၊ မည်သည့် အရည်အချင်းကို မပြန်လည် ဖော်ပြနိုင်သနည်း။
5. Overfitting နှင့် underfitting ကို လက်တွေ့တွင် မည်သည့် metric များဖြင့် ခွဲခြားစစ်ဆေးသနည်း။

<details>
<summary>အဖြေများ</summary>

1. Activation checkpointing သည် forward နှင့် backward တစ်ကြိမ်စာ memory ထဲ ဆံ့စေရန် forward activation
   အချို့ကို သိမ်းဆည်းပြီး ကျန်သည့် အချို့ကို ပြန်လည် တွက်ချက်သည်။ ၎င်းသည် ပြိုလဲသွားသည့် run ကို
   ပြန်လည် စတင်နိုင်ရန် (resume) မပြုလုပ်ပေးပါ — ထိုအတွက် recovery training checkpoint ကို သီးခြား
   သိမ်းဆည်းရမည်။
2. Backpropagation သည် scalar loss မှ computation graph အတွင်း နောက်သို့ chain rule ဖြင့် derivative
   များကို ဖြန့်၍ gradient များကို တွက်ချက်ပေးသည်။ optimizer သည် ထို gradient များကို စားသုံးပြီး
   parameter update အဖြစ် အသွင်ပြောင်းသည် — update rule နှင့် learning rate ကို ဆုံးဖြတ်သည်မှာ
   optimizer ဖြစ်သည်။
3. Adam သည် weight decay ကို (L2 penalty အဖြစ်) gradient အတွင်းသို့ ထည့်သွင်းသည်၊ AdamW သည်
   weight decay ကို gradient အပေါ် အခြေခံသည့် update မှ ခွဲထုတ် (decouple) ထားသဖြင့် ကျုံ့ဝင်သည့်
   အပြုအမူကို ပိုမို နားလည်လွယ်သည်။
4. Gradient accumulation သည် စက်တစ်လုံးတည်းတွင် နမူနာနှင့် activation အားလုံးကို တစ်ပြိုင်နက်
   မထည့်နိုင်သည့်အခါ microbatch များမှ gradient များကို ပေါင်း သို့မဟုတ် ပျမ်းမျှယူ၍ ပိုကြီးသည့်
   effective batch ကို အနီးစပ်ဆုံး ရရှိစေသည်။ သို့သော် batch အပြည့်ကို တစ်ပြိုင်နက် စီမံခြင်း၏
   အရည်အချင်း အားလုံးကို ပြန်လည် ဖော်ပြပေးသည်မဟုတ်ပါ။
5. training metric နှင့် held-out metric ကို နှိုင်းယှဉ်သည် — training ကောင်းပြီး held-out အားနည်းပါက
   overfitting၊ training ပင် လုံလောက်စွာ မကောင်းပါက underfitting ဖြစ်သည်။ overfitting တွင် subgroup
   ကျရှုံးမှုများကို စစ်ဆေးပြီး data အရည်အသွေး၊ regularization၊ early stopping၊ model capacity ကို
   စမ်းသပ်သည်။ underfitting တွင် data နှင့် optimization ကို အရင် စစ်ဆေးပြီး ထို့နောက်မှ training
   အချိန်၊ feature၊ regularization နှင့် capacity ကို ချိန်ညှိသည်။

</details>

## References

- Source glossary — https://aiengineeringfromscratch.com/glossary
- Source repository — https://github.com/rohitg00/ai-engineering-from-scratch (MIT license)
- [Activation Functions](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/03-deep-learning-core/04-activation-functions/)
- [Chain Rule and Automatic Differentiation](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/01-math-foundations/05-chain-rule-and-autodiff/)
- [Backpropagation from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/03-deep-learning-core/03-backpropagation/)
- [Direct Preference Optimization](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/10-llms-from-scratch/08-dpo/)
- [Fine-Tuning and LoRA](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/08-fine-tuning-lora/)
- [Introduction to JAX](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/03-deep-learning-core/12-intro-to-jax/)
- [Reinforcement Learning from Human Feedback](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/10-llms-from-scratch/07-rlhf/)

