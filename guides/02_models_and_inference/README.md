# Area 02 — Models & inference (terms + glossary shortcut)

<!-- guide-kind: terms-only -->

ဤဖိုင်သည် area 02 ၏ term ၂၉ ခုကို အတိုချုံး ရှင်းပြထားသည်။ term တိုင်းကို — term ဆိုတာ ဘာလဲ၊ ဥပမာ တစ်ခု၊
အတိုင်းအတာ သို့မဟုတ် အသုံးဝင်ပုံ ဆိုတဲ့ ၃ ကြောင်းဖြင့် ရေးထားသည်။ term ၂၉ ခုကို အဆင့် ၆ ခုအဖြစ်
ဖွဲ့စည်းပုံ အခြေခံမှ စ၍ output ရွေးချယ်ခြင်း၊ အရှိန်၊ တိကျမှုနှင့် ဝန်ဆောင်မှု တိုင်းတာမှု အထိ အစဉ်လိုက် စီထားသည်။

## ၁။ မော်ဒယ်၏ အခြေခံ ဖွဲ့စည်းပုံနှင့် တွက်ချက်ရေး

### Attention

Attention ဆိုတာ sequence ထဲက token များအချင်းချင်း ဘယ်ဟာ ဘယ်လောက် အရေးပါတာကို score တွက်ပြီး value များကို ပေါင်းစပ်ပေးတဲ့ ယန္တရားကို ဆိုလိုပါတယ်။
ဥပမာ token 1,024 လုံးရှိတဲ့ sequence မှာ token တိုင်း token တိုင်းကို ကြည့်ရင် score 1,024 × 1,024 = 1,048,576 ခု ရလာပါတယ်။
ထို score သည် calculation coefficient သာ ဖြစ်ပါတယ် — model ဘာကို နားလည်ခဲ့တာကို သက်သေပြခြင်း မဟုတ်ပါဘူး။

### Autoregressive

Autoregressive ဆိုတာ output token တစ်လုံးစီကို အရှေ့က token များမှ ခန့်မှန်းပြီး ထို token ကို ပြန်ထည့်ကာ နောက် token ကို ဆက်ခန့်မှန်းတဲ့ ပုံစံကို ဆိုလိုပါတယ်။
ဥပမာ token 512 လုံး ထုတ်ရင် forward pass 512 ကြိမ် အစဉ်လိုက် run ရပါတယ်။
ခန့်မှန်းသည့် အလုံးအစုက word မဟုတ်ဘဲ token ဖြစ်ပါတယ် — အစဉ်လိုက် ဖြစ်တာကြောင့် KV Cache နှင့် Temperature တို့က ဒီအပေါ် မှီခိုပါတယ်။

### CNN (Convolutional Neural Network)

CNN ဆိုတာ input အပေါ် လျှောကျသွားတဲ့ filter ဖြင့် ဒေသဆိုင်ရာ pattern (edge၊ texture၊ object) ကို ရှာဖွေတဲ့ neural network ကို ဆိုလိုပါတယ်။
ဥပမာ 3×3 filter၊ input channel 3 ခု၊ output channel 64 ခု ဆိုရင် weight = 3 × 3 × 3 × 64 = 1,728 ခု ဖြစ်ပါတယ်။
filter ကို position တိုင်းမှာ မျှဝေသုံးတာကြောင့် 224 × 224 = 50,176 position အတွက် weight 1,728 ခုတည်းနဲ့ လုံလောက်ပါတယ်။

### CUDA

CUDA ဆိုတာ NVIDIA GPU များပေါ်တွင် tensor တွက်ချက်မှု အများအပြားကို တစ်ပြိုင်နက် လုပ်ဆောင်နိုင်စေတဲ့ platform နှင့် programming model ကို ဆိုလိုပါတယ်။
ဥပမာ 4,096 × 4,096 matrix တစ်ခု မြှောက်ရင် multiply-add 68,719,476,736 ခု (≈ 68.7 billion) ရှိပြီး GPU က ဒါကို တစ်ပြိုင်နက် ခွဲလုပ်ပါတယ်။
ကိန်းဂဏန်း ပမာဏ ကြီးတာကြောင့် kernel နှင့် driver မကိုက်ညီရင် tokens/s ချက်ချင်း ကျဆင်းပါတယ်။

## ၂။ ဖွဲ့စည်းပုံ အစိတ်အပိုင်းနှင့် ဖန်တီးသည့် မော်ဒယ်များ

### Decoder

Decoder ဆိုတာ representation တစ်ခုကို output အဖြစ် ပြောင်းလဲပေးတဲ့ အစိတ်အပိုင်းကို ဆိုလိုပါတယ်။
ဥပမာ encoder-decoder translation တစ်ခုမှာ source token 100 ခု ဖတ်ပြီး target token 200 ခု ထုတ်ရင် decoder အဆင့် 200 ကြိမ် run ရပါတယ်။
decoder-only model များမှာမူ causal stack တစ်ခုတည်းမှ ထုတ်လုပ်တာကြောင့် masking က token တိုင်း မြင်နိုင်သည့် position ကို သတ်မှတ်ပါတယ်။

### Decoding Strategy

Decoding Strategy ဆိုတာ model ရဲ့ next-token score အစဉ်ကို ရွေးချယ်ပြီးသား token များနှင့် ပြီးစီးသည့် output အဖြစ် ပြောင်းလဲပေးတဲ့ algorithm ကို ဆိုလိုပါတယ်။
ဥပမာ logits တူတူပဲ ဖြစ်နေလည်း greedy (temperature 0) နှင့် top-p 0.9 sampling တို့က output ကို မတူညီစွာ ထုတ်ပေးပါတယ်။
decoding က output ရွေးချယ်ပုံကို ပြောင်းတာသာ ဖြစ်ပါတယ် — လေ့ကျင့်ပြီး weight ကို မပြောင်းလဲသလို အသိပညာလည်း မထပ်တိုးပါဘူး။

### Diffusion Model

Diffusion Model ဆိုတာ noise တစ်ဆင့်ချင်း ထည့်သည့် ဖြစ်စဉ်ကို ပြောင်းပြန်လှန်ကာ အဆင့်ဆင့် ပြန်ရှင်းလင်းပေးတဲ့ generative model ကို ဆိုလိုပါတယ်။
ဥပမာ 512 × 512 ပုံတစ်ပုံအတွက် denoise အဆင့် 50 ခု run ရင် forward pass 50 ခု လိုပါတယ်။
အဆင့် အရေအတွက်နှင့် အချိုးကျ အချိန် ကုန်တာကြောင့် step count၊ resolution နှင့် batch size သုံးခုကို ချိန်ညှိရပါတယ်။

### Encoder

Encoder ဆိုတာ input ကို representation အဖြစ် ပြောင်းလဲပေးတဲ့ အစိတ်အပိုင်းကို ဆိုလိုပါတယ်။
ဥပမာ token 512 လုံး ထည့်ရင် encoder က position 512 ခုကို non-causal အနေနဲ့ တစ်ပြိုင်နက် တွက်တာကြောင့် pass တစ်ခုတည်းနဲ့ representation 512 ခု ရပါတယ်။
ထို prefill compute ပမာဏက TTFT ကို ဆုံးဖြတ်တာကြောင့် embedding နှင့် rerank service များတွင် အဓိက ဖြစ်ပါတယ်။

### GAN (Generative Adversarial Network)

GAN ဆိုတာ generator က အစစ်နှင့်တူသည့် data ဖန်တီးဖို့ ကြိုးစားပြီး discriminator က အစစ်/အတု ခွဲဖို့ ကြိုးစားတဲ့ ကွန်ရက် ၂ ခု အတူတကွ လေ့ကျင့်တဲ့ ဖွဲ့စည်းပုံကို ဆိုလိုပါတယ်။
ဥပမာ လေ့ကျင့်မှု အဆင့်တိုင်းမှာ forward pass 2 ခု (generator 1 ခု၊ discriminator 1 ခု) နှင့် backward pass 2 ခု လိုပါတယ်။
နှစ်ခု တစ်ပြိုင်နက် တိုးတက်လာတာကြောင့် လေ့ကျင့်မှုသည် မတည်ငြိမ်နိုင်ပြီး ဟန်ချက် ထိန်းရပါတယ်။

## ၃။ မော်ဒယ် မိသားစု၊ inference နှင့် cache

### GPT

GPT ဆိုတာ Generative Pre-trained Transformer ဖြစ်ပြီး sequence-prediction objective ဖြင့် ကြိုတင်လေ့ကျင့်ထားတဲ့ generative transformer model မိသားစု အမည်ကို ဆိုလိုပါတယ်။
ဥပမာ အမည်ထဲက generative က output ထုတ်ခြင်း၊ pre-trained က အစောပိုင်း ကျယ်ပြန့်သည့် လေ့ကျင့်မှု၊ transformer က ဖွဲ့စည်းပုံ မိသားစုကို ရည်ညွှန်းပါတယ်။
အမည်တစ်ခုတည်းနဲ့ parameter အရေအတွက် သို့မဟုတ် serving cost ကို မဆုံးဖြတ်နိုင်ပါဘူး။

### Inductive Bias

Inductive Bias ဆိုတာ function သို့မဟုတ် representation အချို့ကို အခြားအရာများထက် ဦးစားပေးတဲ့ ဖွဲ့စည်းပုံဆိုင်ရာ သို့မဟုတ် စာရင်းအင်းဆိုင်ရာ ကြိုတင်ယူဆချက်များကို ဆိုလိုပါတယ်။
ဥပမာ convolution က filter 1,728 ခုကို position 50,176 ခုမှာ မျှဝေသုံးတာကြောင့် locality နှင့် filter မျှဝေခြင်းကို ဦးစားပေးပါတယ်။
causal masking က ရှေ့ position များမှ ခန့်မှန်းခြင်းကို ဦးစားပေးပြီး transformer များတွင်လည်း bias များ ရှိပါတယ်။

### Inference

Inference ဆိုတာ လေ့ကျင့်ပြီး model ကို execute လုပ်ပြီး prediction၊ score၊ embedding သို့မဟုတ် token များ ထုတ်ယူခြင်းကို ဆိုလိုပါတယ်။
ဥပမာ prompt token 1,000 လုံးနှင့် output token 200 လုံး ရှိတဲ့ request တစ်ခုအတွက် token စုစုပေါင်း 1,200 လုံး တွက်ရပါတယ်။
inference လုပ်နေစဉ် cache နှင့် conversation state ပြောင်းနိုင်ပေမယ့် model weight များ မပြောင်းလဲပါဘူး။

### KV Cache

KV Cache ဆိုတာ autoregressive generation မှာ ရှေးဦး position များ၏ key နှင့် value tensor များကို သိမ်းထားပြီး ပြန်လည် အသုံးပြုတဲ့ cache ကို ဆိုလိုပါတယ်။
ဥပမာ layer 32၊ head 32၊ head_dim 128၊ fp16 ဆိုရင် token တစ်လုံး 2 × 32 × 32 × 128 × 2 bytes = 0.5 MiB ဖြစ်ပြီး context 8,192 ဆိုရင် 8,192 × 0.5 MiB = 4 GiB ဖြစ်ပါတယ်။
cache က ထပ်တလဲလဲ တွက်ချက်မှုကို လျှော့ပေးပေမယ့် context ရှည်လာသည်နှင့်အမျှ memory က တိုးလာတာကြောင့် paged attention ဖြင့် စီမံရပါတယ်။

### LLM (Large Language Model)

LLM ဆိုတာ capacity နှင့် ကျယ်ပြန့်သည့် လေ့ကျင့်မှု လုံလောက်စွာ ရှိသည့်အတွက် prompting သို့မဟုတ် adaptation ဖြင့် ဘာသာစကား task အများအပြား လုပ်နိုင်တဲ့ language model ကို ဆိုလိုပါတယ်။
ဥပမာ parameter 7 billion ရှိတဲ့ model ကို fp16 ဖြင့် သိမ်းရင် 7,000,000,000 × 2 bytes = 14 GB လိုပါတယ်။
LLM သည် system တစ်ခုရဲ့ model အစိတ်အပိုင်းသာ ဖြစ်ပါတယ် — tool၊ retrieval၊ state နှင့် product logic တို့က အပြင်မှာ ရှိပါတယ်။

## ၄။ logits၊ ရွေးချယ်ခြင်း၊ အရွယ်အစားနှင့် အကဲဖြတ်ခြင်း

### Logits

Logits ဆိုတာ normalization မလုပ်ရသေးတဲ့ ကိန်းဂဏန်း score များကို ဆိုလိုပါတယ်။
ဥပမာ vocabulary 50,000 ရှိရင် position တိုင်းအတွက် logits 50,000 ခု ထွက်လာပြီး softmax ပြီးရင် အားလုံး ပေါင်းလျှင် 1 ဖြစ်ပါတယ်။
Temperature၊ top-k နှင့် top-p တို့သည် logits အပေါ် လုပ်ဆောင်တာကြောင့် logits က model တွက်ချက်မှုနှင့် ထွက်လာသည့် token ကို ဆက်သွယ်ပေးပါတယ်။

### MoE (Mixture of Experts)

MoE ဆိုတာ expert subnetwork များထဲက အခွဲတစ်စုကို router က input တိုင်း (များသောအားဖြင့် token တိုင်း) အတွက် ရွေးချယ်ပေးတဲ့ ဖွဲ့စည်းပုံကို ဆိုလိုပါတယ်။
ဥပမာ layer တိုင်းမှာ expert 8 ခု ရှိပြီး top-2 ရွေးရင် token တိုင်းအတွက် expert weight ရဲ့ 2 ÷ 8 = 25% သာ activate ဖြစ်ပါတယ်။
sparse activation က total parameter စွမ်းရည်ကို တိုးပေးပေမယ့် expert အားလုံးကို memory ထဲ ထားရတာကြောင့် VRAM က အလိုအလျောက် မလျော့ပါဘူး။

### Nucleus Sampling (Top-p)

Nucleus Sampling (Top-p) ဆိုတာ cumulative probability က သတ်မှတ်ချက် ပြည့်သည့် အသေးဆုံး candidate အစုမှ sampling လုပ်တဲ့ decode နည်းလမ်းကို ဆိုလိုပါတယ်။
ဥပမာ vocabulary 50,000 မှာ top-p 0.9 သုံးရင် cumulative 0.9 ပြည့်ဖို့ candidate 40 ခုလောက်သာ လိုပြီး ကျန် 49,960 ခု (99.92%) ဖယ်ထုတ်ခံရပါတယ်။
candidate အစု အရွယ်အစားက distribution အလိုက် ပြောင်းတာကြောင့် ပုံသေ k သုံးသည့် top-k နှင့် မတူပါဘူး။

### Parameter

Parameter ဆိုတာ လေ့ကျင့်မှုအတွင်း သင်ယူသည့် တန်ဖိုး (weight၊ bias၊ embedding element) ကို ဆိုလိုပါတယ်။
ဥပမာ parameter 7 billion ကို fp16 (2 bytes) ဖြင့် သိမ်းရင် 7,000,000,000 × 2 = 14 GB ဖြစ်ပြီး 4-bit (0.5 byte) ဖြင့် ဆိုရင် 3.5 GB သာ ဖြစ်ပါတယ်။
parameter အရေအတွက်သည် capacity ကို တိုင်းတာတာ ဖြစ်ပြီး အရည်အသွေး သို့မဟုတ် serving cost ကို တိုက်ရိုက် မဆုံးဖြတ်ပါဘူး။

### Perplexity

Perplexity ဆိုတာ ပျမ်းမျှ negative log-likelihood ကို exponent ပြန်တင်ထားတဲ့ တန်ဖိုးကို ဆိုလိုပါတယ်။
ဥပမာ ပျမ်းမျှ negative log-likelihood 2.0 ဆိုရင် perplexity = e^2 ≈ 7.39 ဖြစ်ပြီး တန်ဖိုး နည်းလျှင် sequence အတွက် model က probability ပိုမြင့်စွာ ပေးခဲ့တာ ဖြစ်ပါတယ်။
tokenizer သို့မဟုတ် eval setup မတူညီပါက perplexity ကို နှိုင်းယှဉ်လို့ မရပါဘူး — factuality ကိုလည်း တိုက်ရိုက် မတိုင်းတာပါဘူး။

## ၅။ တိကျမှု၊ အရှိန်မြှင့်ခြင်းနှင့် ထုတ်လွှင့်မှု

### Quantization

Quantization ဆိုတာ weight၊ activation သို့မဟုတ် cache များကို ပိုနည်းတဲ့ bit format ဖြင့် ဖော်ပြခြင်းကို ဆိုလိုပါတယ်။
ဥပမာ parameter 70 billion ရှိတဲ့ model သည် fp16 ဖြင့် 70,000,000,000 × 2 = 140 GB လိုပြီး 4-bit ဖြင့် 70,000,000,000 × 0.5 = 35 GB သာ လိုပါတယ်။
bit width လျှော့လိုက်တာ metadata၊ kernel နှင့် hardware အထောက်အပံ့ အပေါ် မှီခိုတာကြောင့် memory အချိုး အတိအကျ ရမည်ဟု အာမမခံနိုင်ပါဘူး။

### Self-Attention

Self-Attention ဆိုတာ query၊ key နှင့် value အားလုံးကို sequence တစ်ခုတည်းမှ ရယူပြီး လုပ်တဲ့ attention ကို ဆိုလိုပါတယ်။
ဥပမာ token 10 လုံးရှိရင် score 10 × 10 = 100 ခု ဖြစ်ပြီး causal mask သုံးရင် ရှေ့ကိုသာ ကြည့်သည့် score 10 × 11 ÷ 2 = 55 ခု ဖြစ်ပါတယ်။
token တိုင်းသည် token တိုင်းကို အမြဲ attend လုပ်နိုင်တာ မဟုတ်ပါ — causal နှင့် sparse model များက ရည်ရွယ်ချက်ရှိရှိ ကန့်သတ်ပါတယ်။

### Speculative Decoding

Speculative Decoding ဆိုတာ draft ဖြစ်စဉ်က token များ အဆိုပြုပြီး target model က ထို position များကို တစ်ပြိုင်နက် score ပေးတဲ့ inference နည်းလမ်းကို ဆိုလိုပါတယ်။
ဥပမာ draft က token 5 ခု အဆိုပြုပြီး target pass တစ်ကြိမ်နဲ့ 4 ခု လက်ခံခံရရင် pass တစ်ခုလျှင် ပုံမှန် 1 ခုအစား 4 ခု ရသဖြင့် 4 ဆ အထိ ပိုမြန်နိုင်ပါတယ်။
acceptance rate နိမ့်ရင် draft overhead က အကျိုးအမြတ်ကို လွန်နိုင်တာကြောင့် acceptance rate ကို တိုင်းတာရပါတယ်။

### Stop Sequence

Stop Sequence ဆိုတာ decoding စနစ် ကြုံတွေ့တဲ့အခါ generation ရပ်သွားစေတဲ့ application မှ သတ်မှတ်ထားသည့် token သို့မဟုတ် pattern ကို ဆိုလိုပါတယ်။
ဥပမာ max_tokens 1,024 ထားပြီး stop sequence က token 200 မှာ ကိုက်ရင် ကျန် 1,024 - 200 = 824 decode အဆင့် လျော့သွားပါတယ်။
stop sequence သည် စက်ပိုင်း အခြေအနေသာ ဖြစ်ပါတယ် — အဖြေ ပြည့်စုံကြောင်း သို့မဟုတ် agent ရည်မှန်းချက် ပြည့်ကြောင်း သက်သေ မဟုတ်ပါဘူး။

### Streaming

Streaming ဆိုတာ ရလဒ် မပြည့်စုံမီ အစိတ်အပိုင်း အလိုက် response event များ ပို့ပေးခြင်းကို ဆိုလိုပါတယ်။
ဥပမာ TTFT 300 ms နှင့် 40 tokens/s ရှိပြီး အဖြေ 500 token ဆိုရင် စုစုပေါင်း 0.3 + 500 ÷ 40 = 0.3 + 12.5 = 12.8 s ကြာပါတယ်။
Streaming က ပထမ token ကို စောစော မြင်ရစေတာသာ ဖြစ်ပြီး အဖြေ အပြည့်အစုံ ထုတ်ရန် အချိန်ကို မလျှော့ပါဘူး။

## ၆။ sampling ဆက်တင်၊ တိုင်းတာမှုနှင့် အခြေခံ ဖွဲ့စည်းပုံ

### Temperature

Temperature ဆိုတာ probability distribution မဖြစ်ပေါ်မီ logits များကို ပြန်လည် scale ချိန်ညှိသည့် decoding parameter ကို ဆိုလိုပါတယ်။
ဥပမာ logits 4၊ 2၊ 1 အတွက် temperature 1.0 မှာ top token probability 0.844 ဖြစ်ပြီး temperature 0.5 မှာ 0.980 အထိ မြင့်လာပါတယ်။
temperature က sampling အပြုအမူကို ပြောင်းတာသာ — model ရဲ့ အသိပညာ သို့မဟုတ် factuality ကို မပြောင်းလဲပါဘူး။

### Time to First Token (TTFT)

Time to First Token (TTFT) ဆိုတာ request တင်သွင်းသည့် အချိန်မှ client က ပထမဆုံး output token ရရှိသည့် အချိန်အထိ ကြာချိန်ကို ဆိုလိုပါတယ်။
ဥပမာ TTFT 400 ms နှင့် decode 50 tokens/s ရှိပြီး output 300 token ဆိုရင် စုစုပေါင်း 0.4 + 300 ÷ 50 = 0.4 + 6 = 6.4 s ဖြစ်ပါတယ်။
TTFT သည် tokens per second မဟုတ်ပါ — တစ်ခုက စတင်သည့် latency၊ အခြားတစ်ခုက output စတင်ပြီးနောက် throughput ကို တိုင်းတာပါတယ်။

### Top-k Sampling

Top-k Sampling ဆိုတာ next-token distribution ကို အမြင့်ဆုံး score ရှိတဲ့ candidate k ခုအထိ ကန့်သတ်ပြီး ထို အစုမှ sampling လုပ်တဲ့ နည်းလမ်းကို ဆိုလိုပါတယ်။
ဥပမာ vocabulary 50,000 မှာ k = 50 သုံးရင် ဖြစ်နိုင်ခြေ နည်းသည့် tail 49,950 ခု (99.9%) ဖယ်ထုတ်ခံရပါတယ်။
k သည် ပုံသေ အရေအတွက် ဖြစ်ပြီး top-p ကတော့ step တိုင်း candidate အရေအတွက် ပြောင်းတာကြောင့် နှစ်ခု မတူပါဘူး။

### Transformer

Transformer ဆိုတာ attention၊ position အချက်အလက်၊ feed-forward အလွှာ၊ residual connection နှင့် normalization တို့ဖြင့် တည်ဆောက်ထားတဲ့ neural network ဖွဲ့စည်းပုံကို ဆိုလိုပါတယ်။
ဥပမာ layer 32 ခုရှိတဲ့ transformer တစ်ခုမှာ layer တိုင်းတွင် attention အလွှာတစ်ခုနှင့် FFN အလွှာတစ်ခု ရှိပါတယ်။
လေ့ကျင့်မှုတွင် position အများအပြားကို တစ်ပြိုင်နက် တွက်နိုင်သော်လည်း autoregressive generation က အဆင့်ဆင့် အစဉ်လိုက် ထုတ်လုပ်ပါတယ်။

### VAE (Variational Autoencoder)

VAE (Variational Autoencoder) ဆိုတာ reconstruction objective နှင့် approximate posterior ကို prior နှင့် နီးစေတဲ့ regularization term ဖြင့် လေ့ကျင့်တဲ့ latent-variable model ကို ဆိုလိုပါတယ်။
ဥပမာ 28 × 28 pixel ပုံတစ်ပုံ (dimension 784) ကို latent dimension 32 ဆီ ချုံ့ရင် 784 ÷ 32 = 24.5 ဆ ချုံ့သွားပါတယ်။
latent dimension က representation byte ပမာဏကို ဆုံးဖြတ်တာကြောင့် latent resolution ကို ချိန်ညှိရပါတယ်။

## မှီခိုသည့် ဖိုင်

- term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် source အပါ) — [`../../terms/02_models_and_inference.md`](../../terms/02_models_and_inference.md)
