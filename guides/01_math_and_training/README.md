# Area 01 — Math & training (terms + glossary shortcut)

<!-- guide-kind: terms-only -->

ဤဖိုင်သည် area 01 ၏ term ၄၂ ခုကို အတိုချုံး ရှင်းပြထားသည်။ term တိုင်းကို — term ဆိုတာ ဘာလဲ၊ ဥပမာ တစ်ခု၊
အသုံးဝင်ပုံ ဆိုတဲ့ ၃ ကြောင်းဖြင့် ရေးထားသည်။ term ၄၂ ခုကို အဆင့် ၆ ခုအဖြစ် စီထားသည်။

## ၁။ training တစ်ကြိမ် အတွင်း အလုပ်လုပ်သည့် အစိတ်အပိုင်းများ

### Activation Checkpointing

Activation Checkpointing ဆိုတာ forward pass မှာ activation အားလုံးကို မသိမ်းဘဲ ရွေးထားတဲ့ အချို့ကိုသာ သိမ်းထားပြီး backpropagation မှာ ကျန်တာကို ပြန်တွက်တဲ့ training memory နည်းပညာကို ဆိုလိုပါတယ်။
ဥပမာ layer 24 ခုရှိတဲ့ model မှာ layer ၄ ခုတစ်ခါ checkpoint လုပ်ရင် activation အစု ၆ ခုသာ သိမ်းထားပြီး ကျန် ၁၈ ခုကို backward မှာ ပြန်တွက်ရပါတယ်။
Activation သိမ်းတာ လျှော့ပေမယ့် step အချိန် ပိုကြာလာတဲ့အတွက် memory နဲ့ compute လဲလှယ်တဲ့ နည်းလမ်း ဖြစ်ပါတယ်။

### Activation Function

Activation Function ဆိုတာ linear layer ပြီးနောက်မှာ ထည့်ပြီး nonlinearity ပေးတဲ့ function ကို ဆိုလိုပါတယ်။
ဥပမာ ReLU ကို input ၂ ခု -2 နဲ့ 3 အပေါ် သုံးရင် max(0, -2) = 0 နဲ့ max(0, 3) = 3 ရပါတယ်။
Nonlinearity မပါရင် layer ဘယ်လောက် ထပ်ထပ် affine transformation တစ်ခုတည်း ဖြစ်သွားပါတယ်။

### Adam (Optimizer)

Adam (Optimizer) ဆိုတာ gradient ရဲ့ ပျမ်းမျှ (first moment) နဲ့ squared gradient ရဲ့ ပျမ်းမျှ (second moment) ကို ပေါင်းပြီး parameter တစ်ခုချင်းစီအတွက် update ကို ချိန်ညှိပေးတဲ့ optimizer ကို ဆိုလိုပါတယ်။
ဥပမာ parameter 1,000,000 ခုရှိတဲ့ model မှာ Adam က moment ၂ ခုစီ သိမ်းတဲ့အတွက် fp32 နဲ့ဆိုရင် အပို 2,000,000 float (8 MB) လိုပါတယ်။
အားကောင်းတဲ့ baseline ဖြစ်ပေမယ့် သင့်တော်တဲ့ learning rate နဲ့ schedule မရှိရင် အလုပ်မဖြစ်ပါဘူး။

### AdamW

AdamW ဆိုတာ weight decay ကို gradient update နဲ့ ခွဲထုတ် (decouple) ထားတဲ့ Adam မျိုးကွဲကို ဆိုလိုပါတယ်။
ဥပမာ weight decay 0.01 သတ်မှတ်ရင် step တစ်ခုစီမှာ weight က 0.99 ဆ ဖြစ်သွားပြီး step 100 ပြီးရင် မူလ weight ရဲ့ 0.366 ဆ လောက် ကျန်ပါတယ်။
Decouple လုပ်ထားတာကြောင့် weight ကျုံ့ဝင်တဲ့ အပြုအမူကို ခန့်မှန်းရ လွယ်ပါတယ်။

### Autograd

Autograd ဆိုတာ tensor operation များကို မှတ်တမ်းတင်ထားပြီး forward computation ကနေ derivative ကို အလိုအလျောက် ဆင်းသက်ပေးတဲ့ စနစ်ကို ဆိုလိုပါတယ်။
ဥပမာ y = x² မှာ x = 3 ထားရင် dy/dx = 2x = 6 ကို autograd က လက်ဖြင့် မတွက်ရဘဲ ထုတ်ပေးပါတယ်။
Layer များစွာ ပါတဲ့ model မှာ gradient ကို လူက လက်ဖြင့် ဆင်းသက်တွက်တာ မဖြစ်နိုင်တဲ့အတွက် မရှိမဖြစ် လိုပါတယ်။

### Backpropagation

Backpropagation ဆိုတာ scalar loss ကနေ computation graph အတွင်း နောက်သို့ chain rule နဲ့ derivative ဖြန့်ပြီး gradient တွက်ပေးတဲ့ နည်းလမ်းကို ဆိုလိုပါတယ်။
ဥပမာ prediction 5၊ target 3 နဲ့ loss = (pred - target)² ဆိုရင် loss = 4 ဖြစ်ပြီး dloss/dpred = 2 × (5 - 3) = 4 ရပါတယ်။
Backpropagation က gradient တွက်တာသာ ဖြစ်ပြီး learning rate ရွေးတာ မဟုတ်ပါဘူး — update လုပ်တာ optimizer ပါ။

### Batch Size

Batch Size ဆိုတာ optimizer update တစ်ကြိမ် မတိုင်မီ gradient ခန့်မှန်းချက်အတွက် ပါဝင်တဲ့ နမူနာ အရေအတွက်ကို ဆိုလိုပါတယ်။
ဥပမာ dataset 1,000 ခုကို batch 100 နဲ့ train ရင် epoch တစ်ခုစာ step 10 ခု ဖြစ်ပြီး epoch ၅ ခုဆိုရင် step 50 ရပါတယ်။
Batch ကြီးလာရင် memory ပိုလိုပြီး learning rate ကို ပြန်ချိန်ရတာကြောင့် batch တိုင်း တူညီစွာ တိုးလို့ မရပါဘူး။

## ၂။ loss၊ data နှင့် သင်ယူသည့် နည်းလမ်းများ

### Contrastive Learning

Contrastive Learning ဆိုတာ embedding space မှာ ဆင်တူတဲ့ pair ကို ပိုနီးစေပြီး မတူတဲ့ pair ကို ပိုဝေးစေအောင် train လုပ်တာကို ဆိုလိုပါတယ်။
ဥပမာ image-text pair 8 ခုပါတဲ့ batch မှာ ကိုက်တဲ့ pair 8 ခု ဆွဲကပ်ပြီး မကိုက်တဲ့ 8 × 7 = 56 ခုကို တွန်းဖယ်ပါတယ်။
Target label မလိုဘဲ ဆင်တူမှု ဖွဲ့စည်းပုံကို သင်ယူတဲ့အတွက် retrieval နဲ့ CLIP မျိုးမှာ အသုံးများပါတယ်။

### Cross-Entropy

Cross-Entropy ဆိုတာ မှန်ကန်တဲ့ target အတွက် model ပေးတဲ့ probability ရဲ့ negative log အပေါ် အခြေခံတဲ့ loss ကို ဆိုလိုပါတယ်။
ဥပမာ မှန်တဲ့ next token ကို model က probability 0.5 ပေးရင် loss = -ln(0.5) ≈ 0.693 ရပါတယ်။
Language model pretraining အပါအဝင် classification လုပ်ငန်းစဉ် အများစုမှာ ဒီ loss ကို သုံးပါတယ်။

### Data Augmentation

Data Augmentation ဆိုတာ source data အသစ် မစုဆောင်းဘဲ ပြောင်းလဲထားတဲ့ နမူနာများ ဖန်တီးပြီး training diversity တိုးတာကို ဆိုလိုပါတယ်။
ဥပမာ ရုပ်ပုံ 2,000 ခုကို transform ၃ မျိုးစီ လုပ်ရင် နမူနာ 2,000 × 3 = 6,000 ခု ရပါတယ်။
Transform က task signal ကို မပျက်စီးစေရင် overfitting ကို လျှော့ပေးပါတယ်။

### DPO (Direct Preference Optimization)

DPO (Direct Preference Optimization) ဆိုတာ နှစ်သက်တဲ့ အဖြေနဲ့ ပယ်ချတဲ့ အဖြေ pair များကနေ reward model မလိုဘဲ policy ကို တိုက်ရိုက် train လုပ်တဲ့ objective ကို ဆိုလိုပါတယ်။
ဥပမာ preference pair 1,000 ခုရှိရင် reference policy နဲ့ နှိုင်းယှဉ်ပြီး တိုက်ရိုက် optimize လုပ်တဲ့အတွက် reinforcement-learning loop တစ်ခု လျော့သွားပါတယ်။
Reward model အဆင့် မလိုတာက pipeline ကို ရိုးရှင်းစေပေမယ့် preference data အရည်အသွေးအပေါ် မှီခိုဆဲ ဖြစ်ပါတယ်။

### Dropout

Dropout ဆိုတာ training အတွင်း activation အချို့ကို ကျပန်း သုည သတ်မှတ်ပြီး path တစ်ခုတည်းအပေါ် မှီခိုမှုကို လျှော့တာကို ဆိုလိုပါတယ်။
ဥပမာ dropout 0.1 ကို activation 1,000 ခုအပေါ် သုံးရင် activation 100 ခု သုည ဖြစ်ပြီး 900 ခု ကျန်ပါတယ်။
Inference အချိန်မှာ ပုံမှန်အားဖြင့် ပိတ်ထားတဲ့အတွက် training နဲ့ inference အပြုအမူ ကွာပါတယ်။

### Eigenvalue

Eigenvalue ဆိုတာ linear transformation တစ်ခုက သက်ဆိုင်တဲ့ eigenvector ရဲ့ ဦးတည်ချက် မပြောင်းဘဲ ဘယ်လောက် ချဲ့ သို့မဟုတ် ကျုံ့လဲ ဖော်ပြတဲ့ scalar ကို ဆိုလိုပါတယ်။
ဥပမာ covariance matrix [[4, 0], [0, 1]] မှာ eigenvalue 4 နဲ့ 1 ရပြီး ပထမ ဦးတည်ချက်ရဲ့ variance က ဒုတိယထက် ၄ ဆ ရှိပါတယ်။
Eigenvalue ကို ကြည့်ပြီး variance များတဲ့ ဦးတည်ချက်ကို ခွဲထုတ်တဲ့အတွက် PCA နဲ့ dimension လျှော့ချမှုမှာ အခြေခံ ဖြစ်ပါတယ်။

### Epoch

Epoch ဆိုတာ သတ်မှတ်ထားတဲ့ training dataset ကို တစ်ကြိမ် ဖြတ်သွားတာကို ဆိုလိုပါတယ်။
ဥပမာ နမူနာ 10,000 နဲ့ batch 500 ဆိုရင် step 20 ခုနဲ့ epoch ၁ ခု ပြည့်ပြီး epoch ၃ ခုဆိုရင် step 60 ရပါတယ်။
Epoch ပိုများလို့ generalization ပိုကောင်းမယ်လို့ အာမမခံနိုင်ဘဲ held-out data နဲ့ စစ်ရပါတယ်။

## ၃။ gradient စီးဆင်းမှုနှင့် fine-tuning အခြေခံ

### Fine-tuning

Fine-tuning ဆိုတာ pretrained parameter များကနေ စပြီး ပိုကျဉ်းတဲ့ dataset သို့မဟုတ် objective အပေါ် training ကို ဆက်လုပ်တာကို ဆိုလိုပါတယ်။
ဥပမာ နမူနာ 500 ခုကို batch 50 နဲ့ epoch ၃ ခု train ရင် step 30 ခု ရပါတယ်။
Fine-tuning က style နဲ့ format ကို ချိန်ညှိနိုင်ပေမယ့် အချက်အလက် လက်ရှိ ဖြစ်နေရမယ့်နေရာမှာ retrieval ကို အစားမထိုးနိုင်ပါဘူး။

### Gradient

Gradient ဆိုတာ အမြန်ဆုံး တိုးပွားတဲ့ ဦးတည်ချက်သို့ ညွှန်တဲ့ partial derivative များရဲ့ vector ကို ဆိုလိုပါတယ်။
ဥပမာ f(w) = w² မှာ w = 3 ဆိုရင် gradient = 2 × 3 = 6 ဖြစ်ပြီး lr 0.1 နဲ့ ဆင်းရင် w အသစ်က 3 - 0.1 × 6 = 2.4 ဖြစ်ပါတယ်။
ML မှာ gradient ရဲ့ ဆန့်ကျင်ဘက် ဦးတည်ချက်သို့ သွားပြီး loss ကို လျှော့ချပါတယ်။

### Gradient Accumulation

Gradient Accumulation ဆိုတာ optimizer update တစ်ကြိမ် မလုပ်မီ microbatch အများအပြားရဲ့ gradient ကို ပေါင်းတာ သို့မဟုတ် ပျမ်းမျှယူတာကို ဆိုလိုပါတယ်။
ဥပမာ device တစ်လုံးက micro-batch 8 သာဆံ့ရင် accumulate step 4 ခုနဲ့ effective batch 8 × 4 = 32 ရပါတယ်။
Step တစ်ကြိမ်စာ activation memory လျော့ပေမယ့် batch အပြည့်ကို တစ်ပြိုင်နက် စီမံတာရဲ့ အရည်အချင်း အားလုံးကို မပြန်ဖော်ပြနိုင်ပါဘူး။

### Gradient Clipping

Gradient Clipping ဆိုတာ gradient တန်ဖိုးများ သို့မဟုတ် ၎င်းတို့ရဲ့ စုစုပေါင်း norm ကို သတ်မှတ် threshold အောက် ကန့်သတ်တာကို ဆိုလိုပါတယ်။
ဥပမာ gradient norm 10 ရှိပြီး threshold 1 ထားရင် 1/10 ဆ scale လုပ်ပြီး norm 1 ဖြစ်သွားပါတယ်။
ကြီးမားတဲ့ gradient တစ်ခုက step ကို မတည်ငြိမ်စေတာကို တားပေမယ့် မမှန်တဲ့ data သို့မဟုတ် ပျက်နေတဲ့ loss ကို ပြုပြင်ပေးတာ မဟုတ်ပါဘူး။

### Gradient Descent

Gradient Descent ဆိုတာ objective ရဲ့ negative gradient ကို သုံးပြီး parameter များကို ရွှေ့တဲ့ optimization update အုပ်စုကို ဆိုလိုပါတယ်။
ဥပမာ gradient 4 နဲ့ lr 0.25 ဆိုရင် step တစ်ခုမှာ parameter က 0.25 × 4 = 1 ရွေ့သွားပါတယ်။
များသောအားဖြင့် dataset တစ်ခုလုံး အစား batch များကနေ gradient ကို ခန့်မှန်းပါတယ်။

### Hyperparameter

Hyperparameter ဆိုတာ model parameter အဖြစ် သင်ယူခြင်း မရှိဘဲ training ကို ပုံဖော်တဲ့ configuration ရွေးချယ်မှုကို ဆိုလိုပါတယ်။
ဥပမာ learning rate၊ batch size နဲ့ layer အရေအတွက် သုံးခုကို တစ်ခုစီ တန်ဖိုး ၃ မျိုးစီ စမ်းရင် ပေါင်းစပ်မှု 3 × 3 × 3 = 27 မျိုး ဖြစ်ပါတယ်။
ရွေးချယ်မှုတိုင်းက training အပြုအမူကို ကန့်သတ်သတ်မှတ်ပေးတဲ့အတွက် ရလဒ်ကို တိုက်ရိုက် သက်ရောက်ပါတယ်။

### JAX

JAX ဆိုတာ numerical function များကို automatic differentiation၊ compilation၊ vectorization နဲ့ parallel execution ဖြင့် အသွင်ပြောင်းပေးတဲ့ Python library ကို ဆိုလိုပါတယ်။
ဥပမာ နမူနာ 32 ခုကို Python loop နဲ့ 32 ကြိမ် ခေါ်တာအစား vmap က 32 ခုကို ခေါ်စရာ တစ်ကြိမ်အဖြစ် ပြောင်းပေးပါတယ်။
Transformation များက state ကို ရှင်းလင်းစွာ ဖော်ပြတဲ့ functional-style code နဲ့ အကောင်းဆုံး အလုပ်လုပ်ပါတယ်။

## ၄။ learning rate၊ adaptation နှင့် loss တိကျမှု

### Knowledge Distillation

Knowledge Distillation ဆိုတာ teacher model ရဲ့ အပြုအမူ သို့မဟုတ် output distribution ကို student model က ပုံတူပွားအောင် train လုပ်တာကို ဆိုလိုပါတယ်။
ဥပမာ layer 12 ခုရှိတဲ့ teacher ကနေ layer 4 ခုရှိတဲ့ student ကို လွှဲရင် student က 12 / 4 = 3 ဆ သေးပါတယ်။
Distillation က training distribution အပေါ်ရှိ အပြုအမူကို လွှဲပေးပေမယ့် teacher ရဲ့ စွမ်းရည်နဲ့ အချက်အလက် အားလုံးကို ကူးပေးတာ မဟုတ်ပါဘူး။

### Learning Rate

Learning Rate ဆိုတာ optimizer က parameter update အရွယ်အစားကို ထိန်းချုပ်တဲ့ scale factor ကို ဆိုလိုပါတယ်။
ဥပမာ lr 0.001 နဲ့ gradient 0.5 ဆိုရင် step တစ်ခုမှာ update က 0.001 × 0.5 = 0.0005 ဖြစ်ပါတယ်။
တန်ဖိုး ကြီးလွန်းရင် training မတည်ငြိမ်ဘဲ၊ သေးလွန်းရင် တိုးတက်မှု နှေးလွန်းတဲ့အတွက် ချိန်ညှိရတဲ့ အဓိက hyperparameter ဖြစ်ပါတယ်။

### Learning Rate Schedule

Learning Rate Schedule ဆိုတာ training တိုးတက်လာတာနဲ့အမျှ step၊ epoch သို့မဟုတ် curve တစ်ခုအပေါ် မူတည်ပြီး learning rate ကို ပြောင်းစေတဲ့ မူဝါဒကို ဆိုလိုပါတယ်။
ဥပမာ step 50 တိုင်း lr ကို တစ်ဝက်ချပြီး စတင် lr 0.001 ထားရင် step 200 မှာ lr က 0.001 / 16 = 0.0000625 ဖြစ်ပါတယ်။
အစောပိုင်းနဲ့ နောက်ပိုင်း အဆင့်များက update scale မတူတာကို လိုချင်တဲ့အတွက် ကိန်းသေ rate တစ်ခုတည်း မလုံလောက်ပါဘူး။

### LoRA (Low-Rank Adaptation)

LoRA (Low-Rank Adaptation) ဆိုတာ base weight ကို freeze ထားပြီး ရွေးထားတဲ့ layer များအတွက် low-rank update matrix များကိုသာ သင်ယူတဲ့ နည်းလမ်းကို ဆိုလိုပါတယ်။
ဥပမာ matrix 1000 × 1000 (parameter 1,000,000) အတွက် rank 8 နဲ့ LoRA ဆိုရင် A 1000 × 8 နဲ့ B 8 × 1000 ပေါင်း parameter 16,000 သာ ရပါတယ်။
Train လုပ်ရတဲ့ parameter လျော့တာက full-parameter fine-tuning ထက် training memory သက်သာစေပါတယ်။

### Loss Function

Loss Function ဆိုတာ prediction နဲ့ target ကို optimization က လျှော့ချရန် ကြိုးစားတဲ့ တန်ဖိုး တစ်ခုသို့ map လုပ်တဲ့ objective ကို ဆိုလိုပါတယ်။
ဥပမာ error ၂ ခုက 1 နဲ့ 3 ဖြစ်ပြီး MSE သုံးရင် (1² + 3²) / 2 = 5 ရပါတယ်။
Loss က training က မည်သည့် အမှားကို အရင့်အရောက် ခံစေတာကို ဆုံးဖြတ်တဲ့အတွက် ရွေးချယ်မှု အလွန် အရေးပါပါတယ်။

### Mixed Precision

Mixed Precision ဆိုတာ operation အမျိုးမျိုးအတွက် data type အမျိုးမျိုးကို သုံးတဲ့ numerical မဟာဗျူဟာကို ဆိုလိုပါတယ်။
ဥပမာ parameter 1 ဘီလီယံကို fp32 နဲ့ သိမ်းရင် 4 GB လိုပြီး fp16 နဲ့ဆိုရင် 2 GB သာ လိုပါတယ်။
အမြန်နှုန်းနဲ့ memory သက်သာမှုက hardware၊ dtype၊ kernel နဲ့ model အပေါ် မူတည်တဲ့အတွက် ကိန်းသေ multiplier တစ်ခု မဟုတ်ပါဘူး။

### NaN (Not a Number)

NaN (Not a Number) ဆိုတာ မသတ်မှတ်နိုင်တဲ့ numerical ရလဒ်ကို ကိုယ်စားပြုတဲ့ floating-point တန်ဖိုးကို ဆိုလိုပါတယ်။
ဥပမာ exp(1000) က overflow ဖြစ်ပြီး inf ဖြစ်သွားရင် inf - inf က NaN ဖြစ်လာပါတယ်။
တန်ဖိုး တစ်ခု NaN ဖြစ်ရင် ၎င်းကနေ ဆင်းသက်တဲ့ gradient နဲ့ parameter အားလုံး ပျက်နိုင်တဲ့အတွက် run တစ်ခုလုံး အသုံးမဝင်တော့ပါဘူး။

## ၅။ optimizer အခြေခံများ၊ activation နှင့် preference training

### Normalization

Normalization ဆိုတာ သတ်မှတ်ထားတဲ့ statistics များနဲ့ input၊ activation သို့မဟုတ် feature များကို ပြန် scale လုပ် သို့မဟုတ် ဗဟိုပြန်ချိန်တဲ့ transformation အုပ်စုကို ဆိုလိုပါတယ်။
ဥပမာ mean 10 နဲ့ std 2 ရှိရင် x = 14 က (14 - 10) / 2 = 2 ဖြစ်သွားပါတယ်။
Activation ရဲ့ scale ကို ထိန်ညှိပေးတာက optimization တည်ငြိမ်မှုကို ကူပေမယ့် architecture တိုင်းကို တိုးတက်စေတာ မဟုတ်ပါဘူး။

### Optimizer

Optimizer ဆိုတာ gradient များကို parameter update များအဖြစ် အသွင်ပြောင်းတဲ့ algorithm ကို ဆိုလိုပါတယ်။
ဥပမာ parameter 1 ဘီလီယံရှိတဲ့ model မှာ SGD က အပို state မလိုပေမယ့် Adam က moment ၂ ခုစီ fp32 နဲ့ သိမ်းတဲ့အတွက် အပို 8 GB လိုပါတယ်။
Backpropagation က gradient တွက်ပေးပြီး optimizer က ၎င်းကို စားသုံးပြီး parameter ကို ရွှေ့ပါတယ်။

### Overfitting

Overfitting ဆိုတာ training data အပေါ် စွမ်းဆောင်ရည်က မမြင်ရသေးတဲ့ data အပေါ် စွမ်းဆောင်ရည်ထက် သိသိသာသာ ပိုကောင်းနေတဲ့ generalization gap ကို ဆိုလိုပါတယ်။
ဥပမာ train accuracy 99% ဖြစ်ပြီး validation accuracy 70% ဆိုရင် ကွာဟမှု 29 အမှတ် ရှိပါတယ်။
Training metric တစ်ခုတည်း ကောင်းနေတာက unseen data အပေါ် အလုပ်လုပ်မယ်လို့ အာမမခံနိုင်ပါဘူး။

### QLoRA

QLoRA ဆိုတာ pretrained base model ကို low-bit quantized ပုံစံနဲ့ freeze ထားပြီး LoRA adapter များကို ချိန်ညှိတဲ့ parameter-efficient fine-tuning နည်းလမ်းကို ဆိုလိုပါတယ်။
ဥပမာ parameter 7 ဘီလီယံရှိတဲ့ model ကို fp16 နဲ့ဆိုရင် 14 GB လိုပြီး 4-bit နဲ့ဆိုရင် 3.5 GB သာ လိုပါတယ်။
Memory သက်သာပေမယ့် သက်သာမှုနဲ့ အရည်အသွေးက rank၊ optimizer၊ sequence အရှည်နဲ့ hardware အပေါ် မူတည်ပါတယ်။

### ReLU

ReLU ဆိုတာ f(x) = max(0, x) လို့ သတ်မှတ်တဲ့ Rectified Linear Unit ကို ဆိုလိုပါတယ်။
ဥပမာ input ၄ ခု (-1, 2, -3, 4) ကို ReLU ဖြတ်ရင် (0, 2, 0, 4) ရပြီး ၄ ခုထဲက ၂ ခု သုည ဖြစ်သွားပါတယ်။
တွက်ချက်မှု သက်သာပေမယ့် negative input မှာ gradient သုည ဖြစ်တာက အလုပ်မလုပ်တော့တဲ့ unit များကို ဖြစ်စေနိုင်ပါတယ်။

### RLHF (Reinforcement Learning from Human Feedback)

RLHF (Reinforcement Learning from Human Feedback) ဆိုတာ လူ၏ တုံ့ပြန်ချက်ကနေ reward သို့မဟုတ် preference signal ကို သင်ယူပြီး ထို signal အတွက် policy ကို optimize လုပ်တဲ့ pipeline အုပ်စုကို ဆိုလိုပါတယ်။
ဥပမာ လူ နှိုင်းယှဉ်ချက် 10,000 ကနေ reward model တစ်ခု ဆောက်ပြီး ထို reward အပေါ် policy ကို optimize လုပ်ပါတယ်။
RLHF က သင်ယူထားတဲ့ proxy တစ်ခုကို optimize လုပ်တာ ဖြစ်တဲ့အတွက် အခြေအနေ တိုင်းအတွက် alignment ကို အာမမခံပါဘူး။

### SFT (Supervised Fine-Tuning)

SFT (Supervised Fine-Tuning) ဆိုတာ input နဲ့ လိုချင်တဲ့ အဖြေ တွဲဖက်ထားတဲ့ နမူနာများအပေါ် pretrained model ကို ဆက်လက် train လုပ်တာကို ဆိုလိုပါတယ်။
ဥပမာ pair 1,000 ခုကို batch 50 နဲ့ epoch ၂ ခု train ရင် step 40 ရပါတယ်။
ပြသထားတဲ့ နမူနာ အရည်အသွေးက မည်သည့် အပြုအမူကို အရင့်အရောက် ခံစေတာကို ဆုံးဖြတ်ပါတယ်။

### Softmax

Softmax ဆိုတာ logit များကို အပေါင်းလက္ခဏာ ဖြစ်ပြီး စုစုပေါင်း တစ်နဲ့ ညီတဲ့ တန်ဖိုးများအဖြစ် ပြောင်းတဲ့ function ကို ဆိုလိုပါတယ်။
ဥပမာ logit (1, 1, 1) ဆိုရင် class ၃ ခုစီအတွက် e¹ ညီတဲ့အတွက် probability 1/3 ≈ 0.333 စီ ရပါတယ်။
Output များက စုစုပေါင်း တစ်နဲ့ ညီတာကြောင့် categorical distribution အဖြစ် သုံးလို့ ရပါတယ်။

### Stochastic Gradient Descent (SGD)

Stochastic Gradient Descent (SGD) ဆိုတာ dataset တစ်ခုလုံး အစား နမူနာ တစ်ခု သို့မဟုတ် minibatch တစ်ခုကနေ ခန့်မှန်းတဲ့ gradient နဲ့ parameter ကို update လုပ်တဲ့ optimizer အုပ်စုကို ဆိုလိုပါတယ်။
ဥပမာ dataset 1,000 ကို batch 100 နဲ့ ဆိုရင် update တစ်ကြိမ်အတွက် နမူနာ 100 ခုသာ ကြည့်ပြီး 1,000 ခုလုံး မကြည့်ရပါဘူး။
Gradient noise၊ momentum နဲ့ batch scaling ကို နားလည်ရန် SGD က အခြေခံ baseline ဖြစ်ပါတယ်။

## ၆။ generalization နှင့် parameter ထိန်းချုပ်မှု

### Transfer Learning

Transfer Learning ဆိုတာ distribution သို့မဟုတ် objective တစ်ခုအပေါ် သင်ယူထားတဲ့ representation များကနေ စပြီး အခြား task တစ်ခုအတွက် ချိန်ညှိတာကို ဆိုလိုပါတယ်။
ဥပမာ နမူနာ 1,000,000 နဲ့ pretrain လုပ်ထားတဲ့ model ကို နမူနာ 5,000 နဲ့ fine-tune ရင် data 5,000 / 1,000,000 = 0.5% သာ လိုပါတယ်။
Source နဲ့ target task ကွာလွန်းရင် transfer အောင်မြင်မယ်လို့ အာမမခံနိုင်ပါဘူး။

### Underfitting

Underfitting ဆိုတာ model သို့မဟုတ် training setup တစ်ခုမှာ training data အတွင်း အသုံးဝင်တဲ့ ပုံစံများကို ဖမ်းယူရန် effective capacity၊ optimization သို့မဟုတ် training signal မလုံလောက်တာကို ဆိုလိုပါတယ်။
ဥပမာ train loss 1.2 နဲ့ validation loss 1.25 ဆိုရင် နှစ်ခုလုံး မြင့်ပြီး ကွာဟမှုက 0.05 သာ ရှိပါတယ်။
Training loss ပင် လုံလောက်စွာ မကျရင် data နဲ့ optimization ကို အရင် စစ်ရပါတယ်။

### Warmup

Warmup ဆိုတာ learning rate ကို သေးငယ်တဲ့ တန်ဖိုးကနေ စပြီး အဓိက schedule ရဲ့ တန်ဖိုးသို့ တဖြည်းဖြည်း တင်တဲ့ အစပိုင်း training အဆင့်ကို ဆိုလိုပါတယ်။
ဥပမာ warmup step 10 နဲ့ lr ကို 0.00001 ကနေ 0.001 အထိ တင်ရင် step တစ်ခုစီမှာ 0.000099 စီ တိုးပါတယ်။
အစောပိုင်း gradient များ မတည်ငြိမ်တဲ့အတွက် warmup က optimization ကို ထိခိုက်မှုကို ကာကွယ်ပေးပါတယ်။

### Weight

Weight ဆိုတာ model transformation တစ်ခုအတွင်း ရှိတဲ့ train လုပ်နိုင်တဲ့ coefficient ကို ဆိုလိုပါတယ်။
ဥပမာ layer တစ်ခုရဲ့ matrix 512 × 512 ဆိုရင် weight 512² = 262,144 ခု ရှိပါတယ်။
Weight များကို tensor အဖြစ် စီစဉ်ထားပြီး optimization က training objective ကို လျှော့ချရန် ၎င်းတို့ကို ချိန်ညှိပါတယ်။

### Weight Decay

Weight Decay ဆိုတာ training တစ်လျှောက် ရွေးထားတဲ့ parameter များရဲ့ အရွယ်အစားကို လျှော့ချတဲ့ update rule ကို ဆိုလိုပါတယ်။
ဥပမာ decay 0.001 ဆိုရင် step တစ်ခုစီမှာ weight က 0.999 ဆ ဖြစ်ပြီး step 50 ပြီးရင် မူလ weight ရဲ့ 0.951 ဆ လောက် ကျန်ပါတယ်။
Generalization ကို ကူပေမယ့် သင့်တော်တဲ့ coefficient က model၊ optimizer နဲ့ data အပေါ် မူတည်ပါတယ်။

## မှီခိုသည့် ဖိုင်

- term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် source အပါ) — [`../../terms/01_math_and_training.md`](../../terms/01_math_and_training.md)
