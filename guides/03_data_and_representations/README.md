# Area 03 — Data & representations (terms + glossary shortcut)

<!-- guide-kind: terms-only -->

ဤဖိုင်သည် area 03 ၏ term ၁၃ ခုကို အတိုချုံး ရှင်းပြထားသည်။ စာသားမှ token သို့၊ အဓိပ္ပာယ်ကို vector အဖြစ်၊
dataset ပြင်ဆင်ခြင်း၊ ယိုစိမ့်မှုနှင့် ခြေရာခံမှု ဆိုတဲ့ အဆင့် ၄ ခုအဖြစ် အစဉ်လိုက် စီထားသည်။ term တိုင်းကို —
term ဆိုတာ ဘာလဲ၊ ဥပမာ တစ်ခု၊ အတိုင်းအတာ သို့မဟုတ် အသုံးဝင်ပုံ ဆိုတဲ့ ၃ ကြောင်းဖြင့် ရေးထားသည်။

## ၁။ စာသားမှ token သို့

### Tokenization

Tokenization ဆိုတာ စာသား သို့မဟုတ် code ကို model လက်ခံတဲ့ အစဉ်လိုက် token identifier များအဖြစ် ပြောင်းလဲတာကို ဆိုလိုပါတယ်။
ဥပမာ document ၁,၀၀၀ ခု၊ တစ်ခုလျှင် token ၅၀၀ ခု ဆိုရင် စုစုပေါင်း token ၅၀၀,၀၀၀ ခု (၁,၀၀၀ × ၅၀၀) ရပါတယ်။
token အရေအတွက်က sequence အရှည်နဲ့ ကုန်ကျစရိတ် နှစ်ခုလုံးကို ဆုံးဖြတ်ပါတယ် — ကုန်ကျစရိတ် တွက်ချက်မှုရဲ့ အခြေခံ ဖြစ်ပါတယ်။

### Token

Token ဆိုတာ model ဖတ်တဲ့ အသေးဆုံး ယူနစ် ဖြစ်ပြီး tokenizer က ထုတ်ပေးတဲ့ integer identifier တစ်ခု ဖြစ်တာကို ဆိုလိုပါတယ်။
ဥပမာ စာသား တစ်ကြောင်းတည်းကို tokenizer A နဲ့ ရေတွက်ရင် token ၁၂ ခု၊ tokenizer B နဲ့ ရေတွက်ရင် token ၁၅ ခု ရနိုင်ပါတယ်။
ဒါကြောင့် token အရေအတွက်ကို target model ရဲ့ tokenizer နဲ့သာ ရေတွက်ရပါတယ် — ခန့်မှန်း ရေတွက်ရင် ၃ ခု လောက် လွဲနိုင်ပါတယ်။

### Vocabulary

Vocabulary ဆိုတာ tokenizer က ထုတ်နိုင်တဲ့ ယူနစ်များနဲ့ token identifier များကြား အကန့်အသတ် ရှိတဲ့ mapping ကို ဆိုလိုပါတယ်။
ဥပမာ vocab size ၅၀,၀၀၀ နဲ့ d_model 768 ဆိုရင် embedding matrix မှာ parameter ၅၀,၀၀၀ × 768 = ၃၈,၄၀၀,၀၀၀ ခု ရှိပါတယ်။
float32 ဆိုရင် အဲဒီ matrix တစ်ခုတည်း ၅၀,၀၀၀ × 768 × 4 = 153,600,000 byte (၁၄၆ MiB လောက်) နေရာ ယူပါတယ်။

### Byte Pair Encoding (BPE)

Byte Pair Encoding (BPE) ဆိုတာ training text ထဲ မကြာခဏ ဆက်တွဲ ဖြစ်နေတဲ့ ယူနစ် ၂ ခုကို ထပ်ခါတလဲလဲ ပေါင်းပြီး ပုံသေ vocabulary တည်ဆောက်တဲ့ နည်းလမ်းကို ဆိုလိုပါတယ်။
ဥပမာ merge rule ၁,၀၀၀ ကြိမ် လုပ်ရင် vocabulary entry ၁,၀၀၀ ခု တိုးလာပြီး ရှားပါးတဲ့ စကားလုံးကို အက်ကွဲ အပိုင်းများအဖြစ် ကိုယ်စားပြုပါတယ်။
BPE က tokenizer မိသားစု တစ်ခုသာ ဖြစ်ပါတယ် — merge rule ကို model နဲ့တကွ version မှတ်ထားမှ ပြန်လည် ဖန်တီးလို့ ရပါတယ်။

## ၂။ အဓိပ္ပာယ်ကို vector အဖြစ်

### Embedding

Embedding ဆိုတာ စကားလုံး၊ ရုပ်ပုံ သို့မဟုတ် user လို သီးခြား အရာတစ်ခုကို continuous space ထဲက dense vector အဖြစ် mapping လုပ်ထားတာကို ဆိုလိုပါတယ်။
ဥပမာ 768-dim float32 vector တစ်ခုက 768 × 4 = 3,072 byte (၃ KB လောက်) ဖြစ်ပါတယ်။
Chunk ၁၀,၀၀၀ ခုကို embed လုပ်ရင် ၁၀,၀၀၀ × 3,072 = 30,720,000 byte (၂၉ MiB လောက်) ဖြစ်ပါတယ်။

### Cosine Similarity

Cosine Similarity ဆိုတာ vector ၂ ခုရဲ့ normalized dot product ဖြစ်ပြီး ပမာဏ မဟုတ်ဘဲ ဦးတည်ချက် ဆင်တူမှုကို တိုင်းတာတာကို ဆိုလိုပါတယ်။
ဥပမာ vector ၂ ခုရဲ့ cosine similarity က 0.92 ဆိုရင် -1 မှ 1 အတွင်းရှိ အလွန် နီးစပ်တဲ့ တန်ဖိုး တစ်ခု ဖြစ်ပါတယ်။
ဒါပေမယ့် 0.92 ဆိုတာ embedding model နဲ့ data distribution အတွင်းမှာသာ အဓိပ္ပာယ် ရှိပါတယ် — အချက်အလက် တူညီကြောင်း သက်သေ မဖြစ်ပါဘူး။

### Feature

Feature ဆိုတာ data ရဲ့ တိုင်းတာနိုင်တဲ့ ပိုင်ဆိုင်မှု တစ်ခုချင်း ဖြစ်ပြီး classical ML မှာ လက်နဲ့ တည်ဆောက်ရတာကို ဆိုလိုပါတယ်။
ဥပမာ အခန်း ၃ ခု၊ ဧရိယာ 1,200 စတုရန်းပေ ဆိုတဲ့ record တစ်ခုကနေ feature ၂ ခု (room count၊ area) ထုတ်နိုင်ပါတယ်။
deep learning မှာတော့ network က raw data ကနေ feature ကို အလိုအလျောက် သင်ယူပါတယ် — လက်နဲ့ ရေးရတာ မရှိပါဘူး။

### Latent Space

Latent Space ဆိုတာ model အတွက် အသုံးဝင်တဲ့ အချက်များကို coordinate အနေနဲ့ encode လုပ်ထားတဲ့ သင်ယူထားသည့် representation space ကို ဆိုလိုပါတယ်။
ဥပမာ input dimension 1,024 ကို latent 64 dimension နဲ့ ကိုယ်စားပြုရင် coordinate ၆၄ ခုသာ ကျန်ပါတယ်။
coordinate နည်းခြင်းက compression မဟုတ်ပါဘူး — အနီးအနား point ဆင်တူမှုက model နဲ့ training objective သင်ယူထားတာ အတိုင်းသာ ဖြစ်ပါတယ်။

### Tensor

Tensor ဆိုတာ shape၊ data type နဲ့ device placement ပါတဲ့ typed array ဖြစ်ပြီး framework က input၊ parameter၊ activation နဲ့ gradient ကို ကိုယ်စားပြုတာကို ဆိုလိုပါတယ်။
ဥပမာ batch 32၊ sequence 512၊ hidden 768 ရှိတဲ့ activation တစ်ခုရဲ့ shape က (32, 512, 768) ဖြစ်ပြီး element ၃၂ × ၅၁၂ × ၇၆၈ = ၁၂,၅၈၂,၉၁၂ ခု ရှိပါတယ်။
float32 ဆိုရင် အဲဒီ tensor တစ်ခု ၁၂,၅၈၂,၉၁၂ × 4 = 50,331,648 byte (၄၈ MiB) နေရာ ယူပါတယ်။

## ၃။ dataset ပြင်ဆင်ခြင်း

### Data Deduplication

Data Deduplication ဆိုတာ dataset တစ်ခုအတွင်း သို့မဟုတ် dataset များအကြား တိကျတူညီတဲ့ နဲ့ အနီးစပ်ဆုံး တူညီတဲ့ နမူနာများကို ရှာပြီး ဖယ်ရှားတာကို ဆိုလိုပါတယ်။
ဥပမာ document ၁,၀၀၀ ခုထဲမှာ ထပ်တူ ၁၀၀ ခု ရှိရင် ၁၀ ရာခိုင်နှုန်း (၁၀၀/၁,၀၀၀) ဖယ်ရှားရပါတယ်။
မဖယ်ရှားရင် training distribution လွဲပြီး test material ယိုစိမ့်နိုင်တာကြောင့် evaluation က အမှန်တကယ်ထက် ပိုကောင်းဟန် ထင်လာပါတယ်။

### Dataset Split

Dataset Split ဆိုတာ နမူနာများကို fitting၊ development ဆုံးဖြတ်ချက်နဲ့ နောက်ဆုံး evaluation အတွက် သီးခြား subset များအဖြစ် ခွဲထားတာကို ဆိုလိုပါတယ်။
ဥပမာ record ၁,၀၀၀ ခုကို ၈၀/၁၀/၁၀ ခွဲရင် train ၈၀၀ ခု၊ validation ၁၀၀ ခု၊ test ၁၀၀ ခု ရပါတယ်။
ကျပန်း ခွဲရုံနဲ့ မလုံလောက်ပါဘူး — user၊ repository သို့မဟုတ် အချိန် လို တကယ့် deployment ယူနစ်အလိုက် ခွဲရပါတယ်။

## ၄။ ယိုစိမ့်မှုနှင့် ခြေရာခံမှု

### Data Leakage

Data Leakage ဆိုတာ တကယ့် prediction အချိန်မှာ ရနိုင်မည် မဟုတ်တဲ့ သို့မဟုတ် ဖယ်ထားတဲ့ evaluation နယ်နိမိတ်ထဲ ပါတဲ့ အချက်အလက်ကို training အတွင်း မရည်ရွယ်ဘဲ သုံးမိတာကို ဆိုလိုပါတယ်။
ဥပမာ test record ၁,၀၀၀ ခုထဲက ၅၀ ခု train ထဲ ရောက်နေရင် ၅ ရာခိုင်နှုန်း (၅၀/၁,၀၀၀) ယိုစိမ့်မှု ဖြစ်ပါတယ်။
ယိုစိမ့်မှု ရှိရင် metric က အကောင်းဘက် လွန်ကဲပြီး တကယ် မမြင်ဖူးတဲ့ input ရောက်တဲ့အခါ ပြိုလဲသွားပါတယ်။

### Data Provenance

Data Provenance ဆိုတာ data ဘယ်ကနေ လာပြီး ဘယ်သူ ဘယ်လို အသွင်ပြောင်းခဲ့တာ၊ ဘယ် version သုံးခဲ့တာကို ခြေရာခံနိုင်တဲ့ အချက်အလက်ကို ဆိုလိုပါတယ်။
ဥပမာ source file ၁ ခု ပြင်လိုက်ရင် ဆင်းသက်တဲ့ dataset ၃ ခု၊ embedding ၂ ခု၊ model ၁ ခု အနက် ဘယ်ဟာ ပြန်လုပ်ရမည် ဆိုတာ provenance ကြည့်ပြီး သိပါတယ်။
Provenance မရှိရင် ရလဒ် ပြန်လည် ဖန်တီးလို့ မရပါဘူး — source ပြောင်းတဲ့အခါ ထိခိုက်တဲ့ data ကိုလည်း ရှာလို့ မရပါဘူး။

## မှီခိုသည့် ဖိုင်

- term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် source အပါ) — [`../../terms/03_data_and_representations.md`](../../terms/03_data_and_representations.md)
