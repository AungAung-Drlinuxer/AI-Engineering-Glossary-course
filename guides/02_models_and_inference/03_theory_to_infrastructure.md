# 03 — သီအိုရီမှ ထုတ်လုပ်မှု အခြေခံအဆောက်အအုံသို့ (Theory to Infrastructure)

ဤစာတမ်းသည် နယ်ပယ် ၀၂ ၏ term ၂၉ ခုလုံးကို အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ပြန်လည် ဖတ်သည်။ မော်ဒယ်တစ်ခု၏ ဖွဲ့စည်းပုံ term တစ်ခုသည် စာတမ်းအတွင်း သီအိုရီ အဖြစ်သာ မကျန်ရပါ။ ၎င်းသည် GPU memory (VRAM) ပမာဏ၊ compute အသုံးပြုမှု အချိုး၊ latency၊ throughput သို့မဟုတ် serving cost အနက် တစ်ခုခုကို ရွေ့လျားစေသည်။ ရွေ့လျားသည့် ကိန်းဂဏန်း တစ်ခုစီသည် ထုတ်လုပ်မှု အခြေအနေတွင် တုံ့ပြန်ရမည့် ဆုံးဖြတ်ချက် တစ်ခုစီနှင့် တွဲလျက် ရှိသည်။

ဤစာတမ်းရှိ ကိန်းဂဏန်း အားလုံးသည် `guides/02_models_and_inference/scripts/` အောက်ရှိ Python script များမှ ရရှိသည့် တန်ဖိုးများ ဖြစ်သည်။ library version၊ GPU model သို့မဟုတ် vendor စျေးနှုန်း အပေါ် မှီခိုသည့် တန်ဖိုးတိုင်းကို `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်` ဟု မှတ်သားထားသည်။ ဤစာတမ်းသည် benchmark ရလဒ် များကို ဖော်ပြခြင်း မပြုပါ။ ဖော်ပြသည့် တန်ဖိုး အားလုံးသည် ဖော်မြူလာ နှင့် ယူဆချက် (assumption) မှ တွက်ချက်ထားသည့် တန်ဖိုးများ ဖြစ်သည်။

## ၁။ ဝင်ရိုး ခြောက်ခု၏ ဝေါဟာရ သတ်မှတ်ချက်

နောက်ပိုင်း အပိုင်းများတွင် ဤဝေါဟာရ ခြောက်ခုကို တူညီသည့် အဓိပ္ပာယ်ဖြင့်သာ အသုံးပြုမည် ဖြစ်သည်။

**GPU memory (VRAM)** — accelerator တစ်လုံး၏ memory ပေါ်တွင် တစ်ပြိုင်နက် နေရာယူသည့် byte ပမာဏ ဖြစ်သည်။ weight၊ KV cache၊ activation နှင့် runtime buffer အားလုံး ပါဝင်သည်။ VRAM ပြည့်လျှင် deployment သည် throughput ကျခြင်းဖြင့် မဟုတ်ဘဲ အလုပ်လုပ်နိုင်ခြင်း ရပ်တန့်ခြင်းဖြင့် ကျိုးပျက်သည်၊ ထို့ကြောင့် ဤဝင်ရိုးသည် အမာခံ ကန့်သတ်ချက် ဖြစ်သည်။

**compute (FLOPs utilisation)** — တောင်းဆိုမှု တစ်ခုအတွက် လိုအပ်သည့် floating-point operation ပမာဏနှင့် accelerator ၏ peak စွမ်းရည်ကို နှိုင်းယှဉ်သည့် အချိုး ဖြစ်သည်။ utilisation နည်းခြင်းသည် hardware ရှိပြီး အလုပ်မဖြစ်ခြင်း ဖြစ်သည်၊ ဆိုလိုသည်မှာ ပိုသည့် စရိတ် ဖြစ်သည်။

**latency** — အစိတ်အပိုင်း နှစ်ခုဖြင့် တိုင်းတာသည်။ **TTFT (Time to First Token)** သည် generation တောင်းဆိုမှု တင်သည့် အချိန်မှ ပထမဆုံး output token ရရှိသည့် အချိန်အထိ ကာလ ဖြစ်သည်။ **inter-token latency** သည် output token တစ်လုံးနှင့် နောက် တစ်လုံးအကြား ကာလ ဖြစ်သည်။ ပထမတစ်ခုသည် prompt processing နှင့် queueing ကို ဖော်ပြပြီး ဒုတိယတစ်ခုသည် decode အရှိန်ကို ဖော်ပြသည်။

**throughput (tokens/s)** — တစ်စက္ကန့်လျှင် ထုတ်လုပ်သည့် output token အရေအတွက် ဖြစ်သည်။ throughput ကို တောင်းဆိုမှု တစ်ခုတည်း အတွက် တိုင်းတာလျှင် inter-token latency ၏ ပြောင်းပြန် တန်ဖိုးနှင့် နီးစပ်ပြီး တောင်းဆိုမှု အစုအဝေး (batch) အတွက် တိုင်းတာလျှင် စုစုပေါင်း ထုတ်လုပ်မှုကို ရည်ညွှန်းသည်။ ဤနှစ်တန်ဖိုးသည် တူညီသည့် အရာ မဟုတ်ပါ။

**serving cost (cost per million tokens)** — accelerator အချိန်၏ ကုန်ကျစရိတ်ကို ထုတ်လုပ်သည့် token အရေအတွက်ဖြင့် စားခြင်း ဖြစ်သည်။ အဓိကအချက် နှစ်ခုက ၎င်းကို ဆုံးဖြတ်သည် — accelerator တစ်နာရီ စျေးနှုန်း နှင့် ထိုစျေးနှုန်းအောက်တွင် ရရှိသည့် tokens/s။ စျေးနှုန်းသည် vendor နှင့် region အလိုက် ကွာခြားသည့်အတွက် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

**production consequence** — ထို concept ကို လျစ်လျူရှုလျှင် deployment တွင် မည်သည့် အရာ ကျိုးပျက်မည်ကို ဆိုလိုသည်။ ဥပမာ context window ကို တိုးလျှင် quality မြင့်သည် မဟုတ်ဘဲ KV cache ကြီးထွားမှုကြောင့် batch အရေအတွက် ကျဆင်းခြင်းသည် ထုတ်လုပ်မှု အကျိုးဆက် ဖြစ်သည်။

## ၂။ Master table — term ၂၉ ခုလုံး

| Term | primary axis | ကုန်ကျခြင်း / ချွေတာခြင်း | ရွေ့လျားသည့် ကိန်း | ထုတ်လုပ်မှု အကျိုးဆက် |
|---|---|---|---|---|
| Attention | compute | attention core FLOPs သည် sequence length ၏ နှစ်ထပ်ဖြင့် ကြီးထွားသည် | attn core ÷ FFN (0.186 → 2.977) | context အရှည် တိုးလျှင် compute ceiling ကို ထိသည် |
| Autoregressive | latency | KV cache မရှိလျှင် token တိုင်း prefix ကို ပြန်တွက်ရသည် | inter-token latency | decode သည် serial ဖြစ်သည့်အတွက် throughput ကန့်သတ်ခံရသည် |
| CNN (Convolutional Neural Network) | GPU memory | filter မျှဝေအသုံးပြုခြင်းဖြင့် weight နှင့် FLOPs လျော့သည် | weight bytes, FLOPs per input | vision encoder ကို accelerator တစ်လုံးပေါ် တင်နိုင်သည် |
| CUDA | compute | kernel library များဖြင့် achieved FLOPs ကို မြှင့်သည် | achieved ÷ peak FLOPs | stack မကိုက်ညီလျှင် tokens/s ကျဆင်းသည် |
| Decoder | compute | causal stack တစ်ခုတည်းဖြင့် output ထုတ်သည် | per-token FLOPs ≈ 2 × parameter | decode path သည် serving အဓိက လမ်းကြောင်း ဖြစ်သည် |
| Decoding Strategy | latency | sampling အရေအတွက်ထက် output အရှည်ကို ဆုံးဖြတ်သည် | output token အရေအတွက် | output အရှည် ကွာခြားလျှင် ကုန်ကျစရိတ် ကျဆင်းသည် |
| Diffusion Model | compute | denoise step အရေအတွက် × network FLOPs | sampling steps | ရုပ်ပုံ serving ကုန်ကျစရိတ်ကို step အရေအတွက်က ဆုံးဖြတ်သည် |
| Encoder | compute | prompt တစ်ခုလုံးကို တစ်ပြိုင်နက် တွက်သည် | prefill FLOPs | embedding နှင့် rerank service ၏ TTFT ကို ဆုံးဖြတ်သည် |
| GAN (Generative Adversarial Network) | compute | forward pass တစ်ခုတည်းဖြင့် sample ထုတ်သည် | sampling latency | realtime ထုတ်လုပ်မှု စနစ်များတွင် အသုံးပြုသည် |
| GPT | serving cost | မိသားစု အမည် ဖြစ်သည်၊ model ကိုယ်တိုင် မဟုတ်ပါ | parameter အရေအတွက် | model နှင့် product ကို ခွဲခြားမှတ်တမ်းတင်ရမည် |
| Inductive Bias | compute | structure သည် သင်ယူမှု ထိရောက်မှုကို ဆုံးဖြတ်သည် | training compute | ဖွဲ့စည်းပုံ ရွေးချယ်မှုသည် serving cost ကို ရေရှည် သက်ရောက်သည် |
| Inference | serving cost | weight မပြောင်းလဲဘဲ ရလဒ် ထုတ်သည် | cost per million tokens | capacity planning ၏ တစ်ခုတည်းသော အခြေခံ ဖြစ်သည် |
| KV Cache | GPU memory | compute ကို ချွေတာပြီး VRAM ကို စားသည် | token တစ်လုံး 0.5 MiB; 32K batch 32 တွင် 512 GiB | batch အရေအတွက်၏ အမာခံ ကန့်သတ်ချက် ဖြစ်သည် |
| LLM (Large Language Model) | serving cost | စွမ်းရည်ကြီးမားသည့် model အစိတ်အပိုင်း ဖြစ်သည် | parameter အရေအတွက် | system နှင့် model ကို ခွဲခြင်း မပြုလျှင် အမှား ရှာရခက်သည် |
| Logits | compute | vocabulary အပေါ် နောက်ဆုံး projection ကို တွက်သည် | vocabulary × d_model; logits bytes | ကြီးမားသည့် vocabulary သည် decode အရှိန်ကို လျှော့သည် |
| MoE (Mixture of Experts) | GPU memory | sparse activation ဖြင့် active parameter ကို လျှော့သည် | active ÷ total parameter | expert parallelism လိုအပ်မှုကို ဖြစ်ပေါ်စေသည် |
| Nucleus Sampling (Top-p) | latency | candidate အစုကို distribution အလိုက် ကန့်သတ်သည် | top-p candidate အရေအတွက် | latency သည် ပြောင်းလဲနိုင်သည့် တန်ဖိုး ဖြစ်လာသည် |
| Parameter | GPU memory | fp16 တွင် parameter တစ်ခုလျှင် 2 byte လိုသည် | 7B အတွက် 14 GB | accelerator တစ်လုံးပေါ် တင်နိုင်မှုကို ဆုံးဖြတ်သည် |
| Perplexity | compute | evaluation အဆင့်တွင်သာ တွက်သည် | exp(average negative log-likelihood) | model အစားထိုးမှုကို တားဆီးသည့် quality gate ဖြစ်သည် |
| Quantization | GPU memory | fp16 မှ int8 သို့ ရွေ့လျှင် ထက်ဝက်၊ 4-bit တွင် ၄ ဆ ချွေတာသည် | bits per parameter | accelerator တစ်လုံးပေါ် copy အရေအတွက် တိုးသည် |
| Self-Attention | compute | score တွက်ချက်မှုသည် sequence length ၏ နှစ်ထပ်ဖြင့် ကြီးထွားသည် | attention core FLOPs | long-context request များသည် compute ကို ဖိသည် |
| Speculative Decoding | latency | draft လက်ခံပါက target model ၏ serial step လျော့သည် | acceptance rate | draft overhead မထည့်သွင်းလျှင် အကျိုးအမြတ် ပျောက်သည် |
| Stop Sequence | latency | ဆုံးဖြတ်ချက်အရ ထုတ်လုပ်မှုကို ရပ်တန့်စေသည် | output token အရေအတွက် | output အရှည်အတွက် ကုန်ကျစရိတ် ကန့်သတ်ချက် ဖြစ်သည် |
| Streaming | latency | ခံစားရသည့် နှောင့်နှေးမှုကို သာ လျှော့ချသည် | TTFT | စုစုပေါင်း အချိန်ကို လျှော့ချသည် မဟုတ်ပါ |
| Temperature | production consequence | sampling အပြုအမူကို ပြောင်းသည်၊ ကုန်ကျစရိတ်ကို တိုက်ရိုက် မပြောင်းပါ | output အရှည်နှင့် ကွဲပြားမှု | ပြန်လည် ရရှိနိုင်မှု (repeatability) ကို သက်ရောက်သည် |
| Time to First Token (TTFT) | latency | prefill၊ queueing နှင့် cache အခြေအနေ ပါဝင်သည် | မီလီစက္ကန့် | SLO ချိုးဖောက်မှုကို ဖော်ထုတ်သည့် ပထမဆုံး လက္ခဏာ ဖြစ်သည် |
| Top-k Sampling | latency | candidate အရေအတွက်ကို ပုံသေ ကန့်သတ်သည် | k တန်ဖိုး | sampler ကုန်ကျစရိတ် ကို ခန့်မှန်းနိုင်သည် |
| Transformer | compute | လေ့ကျင့်ရာတွင် position များကို တစ်ပြိုင်နက် တွက်သည် | per-position FLOPs | scaling ဆုံးဖြတ်ချက်သည် memory နှင့် ချိတ်ဆက်သည် |
| VAE (Variational Autoencoder) | GPU memory | input ကို latent အရေအတွက် နည်းသည့် representation အဖြစ် ချုံ့သည် | latent dimension | encoder နှင့် decoder နှစ်ခုလုံး VRAM ယူသည် |

## ၃။ term အလိုက် ရှင်းလင်းချက်

term များကို မိသားစု ငါးခုဖြင့် စုစည်းထားသည် — (က) ဖွဲ့စည်းပုံ၊ (ခ) ထုတ်လုပ်မှု အပြုအမူ၊ (ဂ) ခန့်မှန်းချက် ယန္တရား၊ (ဃ) စွမ်းဆောင်ရည်၊ (င) တိုင်းတာမှု။ ဤအုပ်စုခွဲမှုသည် အပိုင်း ၂ ၏ ဇယားနှင့် တိုက်ရိုက် ကိုက်ညီသည်။

### မိသားစု (က) — ဖွဲ့စည်းပုံ (architecture)

#### Attention

Attention သည် query နှင့် key ၏ နှိုင်းယှဉ်မှုမှ score များ ဖြစ်ပေါ်စေပြီး ထို score များဖြင့် value များကို ပေါင်းစပ်သည်။ ဤတွက်ချက်မှု၏ FLOPs သည် sequence length ၏ နှစ်ထပ်ဖြင့် ကြီးထွားသည်၊ ထို့ကြောင့် ၎င်းသည် compute ဝင်ရိုး၏ အဓိက ကိန်း ဖြစ်သည်။ ဥပမာ (ဂ) တွင် attention core နှင့် FFN ၏ အချိုးသည် context 2K တွင် 0.186 ဖြစ်ပြီး context 32K တွင် 2.977 သို့ ရောက်သည်၊ ဆိုလိုသည်မှာ 32K တွင် attention core သည် FFN ကို သုံးဆ ကျော် လွန်သည်။ serving engineer သည် ဤအချိုးကို ကြည့်၍ context limit ကို ရွေးရမည်၊ context ကို တိုးလျှင် KV cache နှင့် compute နှစ်ခုလုံး တစ်ပြိုင်နက် ကြီးထွားသည်။ mask များနှင့် sparse pattern များသည် ဤကိန်းကို လျှော့ရန် အသုံးပြုသည့် knob များ ဖြစ်သည်။

#### Self-Attention

Self-Attention သည် query၊ key၊ value အားလုံးကို တူညီသည့် sequence representation တစ်ခုတည်းမှ ရယူသည်။ ဤအချက်က ၎င်းကို attention ၏ အထူးအခြေအနေ တစ်ခု ဖြစ်စေပြီး အခြေခံအဆောက်အအုံ အရ အရေးအကြီးဆုံး FLOPs အရင်းအမြစ် ဖြစ်သည်။ context အရှည် 2K တွင် attention စုစုပေါင်း (core နှင့် projection) သည် layer FLOPs ၏ 48.2 ရာခိုင်နှုန်း ဖြစ်ပြီး context 32K တွင် 78.8 ရာခိုင်နှုန်း သို့ ရောက်သည်။ ဆိုလိုသည်မှာ long-context အသုံးပြုမှုတွင် attention သည် layer ၏ အဓိက ကုန်ကျစရိတ် ဖြစ်လာသည်။ serving engineer သည် causal mask ကို မည်သို့ ချုံ့မည်၊ local window ကို မည်သို့ သတ်မှတ်မည် ဆိုသည့် ရွေးချယ်မှုကို ဤကိန်းဖြင့် အခြေခံရမည်။

#### Transformer

Transformer သည် attention၊ position အချက်အလက်၊ feed-forward အလွှာခွဲ၊ residual connection နှင့် normalization တို့ဖြင့် တည်ဆောက်ထားသည့် ဖွဲ့စည်းပုံ ဖြစ်သည်။ လေ့ကျင့်မှုတွင် position များကို တစ်ပြိုင်နက် တွက်နိုင်သော်လည်း autoregressive generation သည် token တစ်လုံးချင်း အစဉ်လိုက် ထုတ်လုပ်နေဆဲ ဖြစ်သည်၊ ဤမချိန်တွင် parallel training နှင့် serial serving ကွာခြားချက်သည် compute နှင့် latency ဝင်ရိုး နှစ်ခုအကြား အဓိက ကန့်သတ်ချက် ဖြစ်သည်။ serving engineer သည် prefill (parallel) နှင့် decode (serial) ကို တစ်ခြား အဆင့်များအဖြစ် စီမံရမည်၊ အကြောင်းမှာ နှစ်ခု၏ ကုန်ကျစရိတ် သဘောသဘာဝ မတူပါ။

#### Encoder

Encoder သည် input ကို representation အဖြစ် ပြောင်းလဲပေးပြီး non-causal self-attention ဖြင့် input တစ်လျှောက်လုံးကို တစ်ပြိုင်နက် ကြည့်နိုင်သည်။ ဤအချက်က encoder-based service များ (embedding၊ rerank) တွင် TTFT သည် prefill FLOPs အပေါ် တိုက်ရိုက် မှီခိုသည်ဟု ဆိုလိုသည်။ decoder-only model တွင် KV cache လိုအပ်သော encoding step သည် encoder-only အသုံးပြုမှုတွင် အပြည့်အဝ cache လုပ်ရန် မလိုအပ်ခြင်းသည် VRAM အကျိုးရှိမှု ဖြစ်သည်။ serving engineer သည် batch size ကို prefill compute နှင့် ညှိ၍ သတ်မှတ်ရမည်။

#### Decoder

Decoder သည် representation កို output အဖြစ် ပြောင်းလဲပေးပြီး decoder-only model များတွင် causal stack တစ်ခုတည်းမှ ထုတ်လုပ်သည်။ causal masking ကြောင့် ၎င်းသည် autoregressive ဖြစ်လာပြီး token တိုင်း၏ per-token FLOPs သည် parameter အရေအတွက်၏ နှစ်ဆ နီးပါး ဖြစ်သည်။ decoder-only ဖွဲ့စည်းပုံတွင် context တစ်ခုလုံးသည် တောင်းဆိုမှု တစ်ခုစီ၏ KV cache အဖြစ် တည်ရှိနေသည်၊ ထို့ကြောင့် VRAM စီမံမှုသည် decode အရှိန်နှင့် တိုက်ရိုက် ချိတ်ဆက်သည်။ serving engineer သည် decode batch (continuous batching) ကို ဤဖွဲ့စည်းပုံ အပေါ် အခြေခံ၍ စီမံရမည်။

#### CNN (Convolutional Neural Network)

CNN သည် filter များကို input အပေါ် လျှောကျစေ၍ local pattern များကို ရှာဖွေပြီး filter မျှဝေအသုံးပြုခြင်းဖြင့် parameter အရေအတွက်ကို ချုံ့သည်။ ၎င်း၏ inductive bias သည် locality ကို ဦးစားပေးသည့်အတွက် vision အပိုင်း တွင် ကုန်ကျစရိတ် သက်သာသည့် ရွေးချယ်မှု ဖြစ်သည်။ မျှဝေအသုံးပြုသည့် filter များကြောင့် weight bytes သည် နည်းပြီး VRAM လိုအပ်ချက် ကျဆင်းသည်။ serving engineer သည် ရုပ်ပိုင်းဆိုင်ရာ လုပ်ငန်းတာဝန်များတွင် CNN encoder ကို VRAM နည်းသည့် accelerator ပေါ် တင်နိုင်သည်။

#### Inductive Bias

Inductive Bias သည် model တစ်ခု လွယ်ကူစွာ သင်ယူနိုင်သည့် function အမျိုးအစားကို ဆုံးဖြတ်သည့် ဖွဲ့စည်းပုံဆိုင်ရာ သို့မဟုတ် စာရင်းအင်းဆိုင်ရာ ကြိုတင်ယူဆချက်များ ဖြစ်သည်။ convolution သည် locality ကို၊ causal masking သည် ရှေ့ position များမှ ခန့်မှန်းခြင်းကို ဦးစားပေးသည်။ ဤရွေးချယ်မှုသည် model တစ်ခုလိုအပ်သည့် training compute နှင့် inference compute ကို ရေရှည်တွင် သတ်မှတ်သည်။ ထို bias များသည် deployment အပေါ် လက်တွေ့ သက်ရောက်သည် — ဥပမာ all-to-all attention မဟုတ်သည့် sparse pattern ရှိသည့် ဖွဲ့စည်းပုံသည် VRAM ကို ပို၍ ချွေတာသည်။ serving engineer သည် ဖွဲ့စည်းပုံ ရွေးချယ်မှုကို နောက်မှ ပြန်ပြင်နိုင်သည့် ဆုံးဖြတ်ချက် အဖြစ် မယူဆရ၊ အကြောင်းမှာ ၎င်းသည် ကုန်ကျစရိတ် ကို ဖွဲ့စည်းပုံ အဆင့်တွင် ချုပ်ထားသည်။

#### VAE (Variational Autoencoder)

VAE သည် reconstruction objective နှင့် prior နှင့် နီးကပ်စွာ ထားရှိသည့် regularization term ဖြင့် လေ့ကျင့်သည့် latent-variable model ဖြစ်သည်။ ခန့်မှန်း posterior နှင့် prior ကို မည်သို့ ရွေးချယ်သည် ဆိုသည်က latent space ၏ ဖွဲ့စည်းပုံကို သတ်မှတ်သည်။ latent dimension သည် ချုံ့ထားသည့် representation ၏ byte ပမာဏကို ဆုံးဖြတ်သောကြောင့် ၎င်းသည် GPU memory ဝင်ရိုး အပေါ် သက်ရောက်သည်။ diffusion model ကဲ့သို့ စနစ်များတွင် latent space အတွင်း၌ လုပ်ဆောင်ခြင်းသည် sampling step တိုင်း၏ VRAM နှင့် compute ကို လျှော့ချရန် အသုံးပြုသည့် knob ဖြစ်သည်။ serving engineer သည် latent resolution ကို အရည်အသွေး နှင့် ကုန်ကျစရိတ် အကြား ချိန်ညှိရမည်။

#### GAN (Generative Adversarial Network)

GAN သည် generator နှင့် discriminator နှစ်ခုကို ပြိုင်ဆိုင်စွာ လေ့ကျင့်သည်၊ generator သည် data ဖန်တီးရန်၊ discriminator သည် အစစ်နှင့် အတု ခွဲခြားရန် ကြိုးစားသည်။ serving အခြေအနေတွင် discriminator မလိုအပ်ဘဲ generator ၏ forward pass တစ်ခုတည်းဖြင့် sample ထုတ်နိုင်သည်၊ ထို့ကြောင့် sampling latency သည် diffusion ၏ denoise step အရေအတွက်ကဲ့သို့ အလွှာများစွာ မလိုအပ်ပါ။ ဤအချက်က GAN ကို realtime ထုတ်လုပ်မှု စနစ်များတွင် compute သက်သာသည့် ရွေးချယ်မှု ဖြစ်စေသည်။ လေ့ကျင့်မှု မတည်ငြိမ်မှုသည် ကုန်ကျစရိတ် အပေါ် လွှမ်းမိုးသည်၊ အကြောင်းမှာ ပြန်လည် လေ့ကျင့်ရမှု များလာသည်။

### မိသားစု (ခ) — ထုတ်လုပ်မှု အပြုအမူ (generative behaviour)

#### Autoregressive

Autoregressive သည် output token တစ်ခုစီကို ၎င်း၏ အရင် token များမှ ခန့်မှန်းသည့် factorization ဖြစ်ပြီး ရွေးချယ်လိုက်သည့် token ကို sequence အဆုံးတွင် ထည့်သည်။ ဤအစဉ်လိုက် သဘောသဘာဝကြောင့် decode အဆင့်တစ်ခုစီသည် serial ဖြစ်ပြီး parallel လုပ်နိုင်သည့် အပိုင်း မရှိပါ။ ထို့ကြောင့် inter-token latency သည် compute မဟုတ်ဘဲ memory bandwidth နှင့် weight byte ပမာဏ အပေါ် မှီခိုလာသည်။ KV cache နှင့် batching သည် ဤ အစဉ်လိုက် ဇာတ်ကြောင်း အပေါ် တည်ဆောက်ထားသည့် အဓိက ဖြေရှင်းနည်း နှစ်ခု ဖြစ်သည်။ serving engineer သည် decode step တိုင်း ဖတ်ရမည့် byte ပမာဏကို ဤအချက်မှ တိုက်ရိုက် တွက်နိုင်သည်။

#### Diffusion Model

Diffusion Model သည် noise ထည့်သည့် ဖြစ်စဉ်နှင့် ၎င်းကို ပြောင်းပြန်လှန်သည့် သင်ယူထားသည့် ဖြစ်စဉ် အပေါ် အခြေခံသည်၊ sampling သည် noise မှ စတင်၍ denoise အဆင့်များကို အကြိမ်ကြိမ် လုပ်ဆောင်သည်။ ထို့ကြောင့် ၎င်း၏ compute ကုန်ကျစရိတ်သည် sampling step အရေအတွက်နှင့် တိုက်ရိုက် အချိုးကျသည်၊ ဆိုလိုသည်မှာ step အရေအတွက် လျှော့ချခြင်းသည် အရည်အသွေး နှင့် ကုန်ကျစရိတ် ကို လဲလှယ်သည့် knob ဖြစ်သည်။ latent space အတွင်း၌ လုပ်ဆောင်လျှင် step တိုင်း၏ VRAM နှင့် FLOPs နှစ်ခုလုံး ကျဆင်းသည်။ serving engineer သည် step count၊ resolution နှင့် batch size သုံးခုကို တစ်ပြိုင်နက် ချိန်ညှိရမည်။

#### GPT

GPT သည် Generative Pre-trained Transformer ဖြစ်ပြီး generative transformer model များအတွက် မိသားစု အမည် ဖြစ်သည်။ ၎င်းသည် model ဖွဲ့စည်းပုံ အမည် ဖြစ်သည့်အတွက် serving budget ကို တိုက်ရိုက် မဆုံးဖြတ်ပါ၊ parameter အရေအတွက်၊ context limit နှင့် precision တို့ကသာ ဆုံးဖြတ်သည်။ ထုတ်လုပ်မှု စနစ်တွင် အမည်တစ်ခုတည်းကို အသုံးပြု၍ version မကွဲပြားစွာ မှတ်တမ်းတင်ခြင်းသည် ကုန်ကျစရိတ် တွက်ချက်မှုကို မှားယွင်းစေသည်။ serving engineer သည် model card ၏ parameter၊ context နှင့် precision အချက်များကို အမည်အစား အခြေခံ တန်ဖိုးများ အဖြစ် သတ်မှတ်ရမည်။

#### LLM (Large Language Model)

LLM သည် စွမ်းရည်နှင့် ကျယ်ပြန့်သည့် လေ့ကျင့်မှု ရှိသည့်အတွက် prompting သို့မဟုတ် adaptation မှတစ်ဆင့် task အများအပြား လုပ်ဆောင်နိုင်သည့် language model ဖြစ်သည်။ ထုတ်လုပ်မှု အမြင်ဖြင့် ၎င်းသည် system တစ်ခု၏ အစိတ်အပိုင်း တစ်ခုသာ ဖြစ်သည်၊ ထို့ကြောင့် cost per million tokens ကို တိုင်းတာရာတွင် model ဆိုင်ရာ ကိန်းနှင့် system ဆိုင်ရာ ကိန်း (retrieval၊ tool call၊ orchestration) ကို ခွဲခြားရမည်။ လက်ရှိ LLM အများစုသည် transformer ဖွဲ့စည်းပုံကို အသုံးပြုသော်လည်း အရွယ်အစား သတ်မှတ်ချက်နှင့် လေ့ကျင့်သည့် နည်းလမ်းများ ကွာခြားသည်။ serving engineer သည် ဤ ကွာခြားချက်ကို hardware ရွေးချယ်မှု အဆင့်အထိ ဆက်လက် သယ်ဆောင်ရမည်။

#### Decoding Strategy

Decoding Strategy သည် model ၏ next-token score အစဉ်ကို ရွေးချယ်ပြီးသား token အဖြစ် ပြောင်းလဲသည့် algorithm ဖြစ်သည်။ logits တူညီသည့် အခြေအနေတွင်ပင် greedy၊ sampling၊ truncation နှင့် search နည်းလမ်းများသည် ထုတ်လုပ်သည့် output အရှည်ကို မတူညီစွာ ဖြစ်စေနိုင်သည်၊ output အရှည်သည် serving cost ၏ အကြီးမားဆုံး ပြောင်းလဲနိုင်သည့် အချက် ဖြစ်သည်။ ထို့ကြောင့် decoding setting များကို eval configuration တွင် မှတ်တမ်းတင်ထားခြင်းသည် ကုန်ကျစရိတ် နှိုင်းယှဉ်မှုအတွက် မရှိမဖြစ် ဖြစ်သည်။ serving engineer သည် decode strategy ကို latency၊ diversity နှင့် cost သုံးခုအကြား ချိန်ညှိသည့် policy အဖြစ် သတ်မှတ်ရမည်။

#### Temperature

Temperature သည် distribution မဖြစ်ပေါ်မီ logits များကို ပြန်လည် အတိုင်းအတာ ချိန်ညှိသည့် decode parameter ဖြစ်သည်၊ မြင့်သည့် တန်ဖိုးသည် distribution ကို ပြန့်ပြူးစေပြီး နိမ့်သည့် တန်ဖိုးသည် စူးရှစေသည်။ ၎င်းသည် sampling အပြုအမူကို ပြောင်းလဲသော်လည်း model ၏ ကိုယ်အလေးချိန် (weight)၊ VRAM သို့မဟုတ် per-token FLOPs ကို မပြောင်းလဲပါ။ သို့သော် မြင့်သည့် temperature သည် output ရှည်ခြင်း သို့မဟုတ် ရပ်တန့်ခြင်း မဖြစ်ဘဲ ဆက်လက် ထုတ်လုပ်ခြင်းကို ဖြစ်စေနိုင်သည့်အတွက် ကုန်ကျစရိတ် အပေါ် သွယ်ဝိုက်၍ သက်ရောက်သည်။ ထို့အပြင် determinism သည် provider၊ sampler နှင့် seed အထောက်အပံ့ အပေါ် မှီခိုသည်ဟု မှတ်သားရမည်၊ ဤအချက်သည် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်` အမျိုးအစား ဖြစ်သည်။ serving engineer သည် temperature ကို ပြန်လည် ရရှိနိုင်မှု လိုအပ်သည့် task များတွင် ပုံသေ သတ်မှတ်ထားရမည်။

#### Top-k Sampling

Top-k Sampling သည် next-token distribution ကို အမြင့်ဆုံး score ရှိသည့် candidate k လုံးအထိ ကန့်သတ်ပြီး ပြန်လည် normalize လုပ်ကာ ထို အစုမှ sampling လုပ်သည်။ candidate အရေအတွက်သည် ပုံသေ ဖြစ်သည့်အတွက် sampler ၏ ကုန်ကျစရိတ်သည် ခန့်မှန်းနိုင်သည့် အခြေအနေ တွင် ရှိသည်။ k ကို သေးငယ်စွာ သတ်မှတ်ခြင်းသည် low-probability အမြီးရှည်ကို ဖယ်ရှားပြီး output ကို ပို၍ တည်ငြိမ်စေသည်။ serving engineer သည် top-k ကို temperature၊ top-p နှင့် stop setting များနှင့်အတူ အကဲဖြတ်ရမည်၊ ရလဒ်တိုင်းနှင့်အတူ sampler configuration အပြည့်အစုံကို မှတ်တမ်းတင်ရမည်။

#### Nucleus Sampling (Top-p)

Nucleus Sampling သည် cumulative probability သတ်မှတ်ချက် ပြည့်သည့် အသေးဆုံး candidate အစုမှ sampling လုပ်သည်။ candidate အစု၏ အရွယ်အစားသည် distribution အပေါ် မှီခို၍ ပြောင်းလဲသည့်အတွက် sampler ၏ per-token ကုန်ကျစရိတ်သည် အခြေအနေ အလိုက် ကွာခြားသည်။ မသေချာမှု ကျယ်ပြန့်သည့်အခါ candidate များပြီး probability စုစည်းနေသည့်အခါ candidate နည်းသည်၊ ဤအချက်သည် latency တွင် သေးငယ်သည့် ပြောင်းလဲမှုကို ဖြစ်စေသည်။ top-p သည် probability mass အဆင့သတ်မှတ်ချက် ဖြစ်ပြီး top-k သည် အများဆုံး candidate အရေအတွက် ဖြစ်သည်၊ ဤကွာခြားချက်သည် capacity ခန့်မှန်းမှုတွင် အရေးပါသည်။ serving engineer သည် temperature နှင့် stop setting များကို မပြောင်းလဲဘဲ သတ်မှတ်ချက်ကို အကဲဖြတ်ရမည်။

#### Stop Sequence

Stop Sequence သည် decoding စနစ် ကြုံတွေ့သည့်အခါ generation ကို ရပ်တန့်စေသည့် application မှ သတ်မှတ်ထားသည့် token သို့မဟုတ် စာသား pattern ဖြစ်သည်။ ၎င်းသည် output protocol များကို ကန့်သတ်ပြီး model ක မိမိ ပြီးဆုံးပြီဟု ဆုံးဖြတ်သည့်အထိ စောင့်ရန် မလိုအပ်ပါ၊ ဆိုလိုသည်မှာ ၎င်းသည် ထုတ်လုပ်သည့် token အရေအတွက်၏ အထက်ကန့်သတ်ချက် ဖြစ်သည်။ ထို့ကြောင့် stop sequence သည် cost per million tokens အပေါ် တိုက်ရိုက် သက်ရောက်သည့် ကုန်ကျစရိတ် ထိန်းချုပ်မှု ဖြစ်သည်။ သို့သော် ၎င်းသည် စက်ပိုင်းဆိုင်ရာ decoding အခြေအနေ တစ်ခုသာ ဖြစ်သည်၊ အဖြေ ပြည့်စုံသည် ဟု သက်သေပြခြင်း မဟုတ်ပါ။ serving engineer သည် မရောထွေးနိုင်သည့် delimiter များကို ရွေးရမည်၊ tokenization နှင့် streaming တွင် တစ်စိတ်တစ်ပိုင်း ကိုက်ညီမှုများကို စမ်းသပ်ရမည်။

### မိသားစု (ဂ) — ခန့်မှန်းချက် ယန္တရား (inference mechanics)

#### Inference

Inference သည် လေ့ကျင့်ပြီးသား model ကို execute လုပ်၍ prediction သို့မဟုတ် token များကို ရရှိစေခြင်း ဖြစ်ပြီး parameter များအတွက် training update ကို မပြုလုပ်ပါ။ weight မပြောင်းလဲသည့်အတွက် ကုန်ကျစရိတ် အားလုံးသည် accelerator အချိန် အပေါ် ရောက်လာသည်၊ ထို့ကြောင့် cost per million tokens သည် inference အဆင့်၏ သီးသန့် တိုင်းတာမှု ဖြစ်သည်။ application သည် inference လုပ်နေစဉ် cache များ၊ conversation state သို့မဟုတ် ပြင်ပ memory ကို update လုပ်နိုင်သော်လည်း model weight မပြောင်းလဲပါ။ serving engineer သည် inference အဆင့်တွင် ပြောင်းနိုင်သည့် knob များ — batch size၊ precision၊ cache policy နှင့် context limit — ကိုသာ အသုံးပြု၍ ကုန်ကျစရိတ်ကို ထိန်းရမည်။

#### KV Cache

KV Cache သည် ရှေးဦး position များမှ key နှင့် value tensor များကို သိမ်းဆည်းထားပြီး မပြောင်းလဲသည့် prefix အတွက် attention projection များကို decode အဆင့်တိုင်း ပြန်လည် တွက်ချက်ခြင်းကို ရှောင်ရှားသည်။ ဤအချက်က compute ကို ချွေတာပြီး VRAM ကို စားသည့် တိုက်ရိုက် လဲလှယ်မှု ဖြစ်သည်။ ဥပမာ (က) တွင် reference model ၏ KV cache သည် token တစ်လုံးလျှင် 0.5 MiB ဖြစ်ပြီး context 32768၊ fp16၊ batch 32 တွင် 512 GiB သို့ ရောက်သည်၊ ဤတန်ဖိုးသည် 64 GiB ခန့် သီးသန့်ထားသည့် accelerator တစ်လုံးပေါ် တွင် လုံးဝ မဆံ့ပါ။ int8 သိမ်းဆည်းမှုဖြင့် ထက်ဝက် ချုံ့နိုင်သည်ဟု ဥပမာ (က) က ပြသည် (32768 တွင် 256 GiB)၊ သို့သော် ထိုတန်ဖိုးသည်ပင် ကြီးမားနေဆဲ ဖြစ်သည်။ serving engineer သည် paged attention၊ prefix caching နှင့် KV precision သုံးခုကို အသုံးပြု၍ ဤ VRAM ကို စီမံရမည်။

#### Logits

Logits သည် normalization မလုပ်ရသေးသည့် ကိန်းဂဏန်း score များဖြစ်ပြီး temperature၊ softmax၊ top-k နှင့် top-p တို့သည် logits အပေါ် လုပ်ဆောင်သည် သို့မဟုတ် မှ ဆင်းသက်လာသည်။ ထုတ်လုပ်မှု အခြင်း ဖြင့် logits ကို တွက်ရာတွင် vocabulary အပေါ် နောက်ဆုံး projection တစ်ခု လိုအပ်သည်၊ ဤ projection ၏ FLOPs သည် vocabulary နှင့် d_model ၏ မြှောက်လဒ် အပေါ် မှီခိုသည်။ vocabulary ကြီးမားသည့် model များတွင် logits tensor ၏ byte ပမာဏသည်လည်း decode အဆင့်တိုင်း VRAM နှင့် bandwidth ကို အနည်းငယ် စားသည်၊ ထို့ကြောင့် logits သည် compute ဝင်ရိုးနှင့် memory ဝင်ရိုး နှစ်ခုလုံးအပေါ် သက်ရောက်သည်။ logits သည် probability များ မဟုတ်သည့်အတွက် တူညီသည့် transformation မရှိဘဲ model နှစ်ခုအကြား နှိုင်းယှဉ်နိုင်သည် မဟုတ်ပါ။ serving engineer သည် mask များကို sampling မလုပ်မီ အသုံးပြုရမည်။

#### Speculative Decoding

Speculative Decoding သည် ကုန်ကျစရိတ် ပိုနည်းသည့် draft ဖြစ်စဉ်တစ်ခုက token အများအပြားကို အဆိုပြုပြီး target model က ထို draft position များကို တစ်ပြိုင်နက် score ပေးသည်။ ဤနည်းလမ်းသည် target model ၏ serial decoding အလုပ်ပမာဏကို လျှော့ချပြီး weight များကို ပြောင်းလဲရန် မလိုအပ်ပါ။ အကျိုးအမြတ်၏ အဓိက ကိန်းသည် acceptance rate ဖြစ်သည်၊ acceptance rate နိမ့်လျှင် draft ၏ အပိုအလွှာ (overhead) သည် ရရှိသည့် အကျိုးအမြတ်ကို လွန်ကာ ပို၍ နှေးစေနိုင်သည်။ ထို့ကြောင့် လက်တွေ့ prompt များအပေါ် acceptance rate နှင့် end-to-end latency ကို တိုင်းတာရမည်၊ ဤတန်ဖိုးသည် model နှင့် data အလိုက် ကွာခြားသည့်အတွက် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။ VRAM အပိုင်းတွင်လည်း draft model သည် နေရာ ထပ်ယူသည်။

#### Streaming

Streaming သည် ပြီးစီးသည့် ရလဒ် အသင့်မဖြစ်မီ အဆင့်ဆင့် ဖြစ်ပေါ်သည့် response event များကို ပေးပို့သည်။ ၎င်းသည် ခံစားရသည့် တုံ့ပြန်မှု လျင်မြန်မှုကို ကောင်းမွန်စေသော်လည်း model ၏ အဖြေ အပြည့်အစုံ ထုတ်လုပ်ရန် အမှန်တကယ် အချိန်ကို လျှော့ချပေးသည် မဟုတ်ပါ။ ထို့ကြောင့် streaming သည် TTFT ၏ အတိုင်းအတာကို မြှင့်တင်ပြီး စုစုပေါင်း latency ကို မပြောင်းလဲပါ၊ ဤခွဲခြားမှုသည် capacity planning တွင် အရေးပါသည်။ network transport၊ event ပုံစံနှင့် chunk နယ်နိမိတ်များသည် provider အလိုက် ကွာခြားပြီး word သို့မဟုတ် token များနှင့် တိုက်ဆိုင်မည်ဟု အာမမခံနိုင်ပါ။ serving engineer သည် client-side TTFT ကို streaming state နှင့်အတူ မှတ်တမ်းတင်ရမည်။

#### Time to First Token (TTFT)

TTFT သည် generation တောင်းဆိုမှု တင်သည့် အချိန်မှ client က ပထမဆုံး output token သို့မဟုတ် content event ကို လက်ခံရရှိသည့် အချိန်အထိ ကာလ ဖြစ်သည်။ ၎င်းသည် queueing၊ prompt processing (prefill)၊ cache နှင့် network ဆိုင်ရာ နှောင့်နှေးမှုများကို ဖော်ထုတ်ပေးနိုင်သည့်အတွက် SLO ၏ အဓိက ကိန်း ဖြစ်သည်။ TTFT သည် tokens per second မဟုတ်ပါ၊ တစ်ခုသည် စတင်သည့် latency ကို တိုင်းတာပြီး အခြားတစ်ခုသည် output စတင်ပြီးနောက် generation throughput ကို တိုင်းတာသည်။ prefill compute သည် context အရှည်နှင့် အတူ တိုးသည့်အတွက် context limit နှင့် batching policy သည် TTFT အပေါ် တိုက်ရိုက် သက်ရောက်သည်။ serving engineer သည် client-side TTFT ကို model၊ prompt အရှည်၊ region နှင့် cache အခြေအနေ အလိုက် မှတ်တမ်းတင်ရမည်။

### မိသားစု (ဃ) — စွမ်းဆောင်ရည် (efficiency)

#### Parameter

Parameter သည် လေ့ကျင့်မှုအတွင်း သင်ယူသည့် တန်ဖိုး ဖြစ်ပြီး အများအားဖြင့် weight၊ bias၊ embedding element သို့မဟုတ် normalization parameter ဖြစ်သည်။ parameter အရေအတွက်သည် model စွမ်းရည်ကို တိုင်းတာသည့် အတိုင်းအတာ တစ်ခု ဖြစ်သော်လည်း memory သို့မဟုတ် serving cost ကို တိုက်ရိုက် မသတ်မှတ်ပါ။ ဥပမာ (ခ) တွင် 7B parameter သည် fp16 ဖြင့် 13.039 GiB (14.000 GB) ဖြစ်ပြီး 70B သည် fp16 ဖြင့် 130.385 GiB ဖြစ်သည်၊ ဤတန်ဖိုးများသည် numerical format ပေါ် မှီခိုသည်။ Parameter တစ်ခုစီအတွက် memory သည် numerical format၊ quantization metadata၊ sharding၊ optimizer state၊ activation နှင့် runtime အပိုအလွှာများအပေါ် မှီခိုသည်ဟု မှတ်သားရမည်။ serving engineer သည် parameter အရေအတွက်ကို model ရွေးချယ်မှု၏ အစအချက်အဖြစ် အသုံးပြု၍ VRAM ခန့်မှန်းမှုကို byte အဆင့်တွင် ပြန်တွက်ရမည်။

#### Quantization

Quantization သည် memory၊ bandwidth သို့မဟုတ် တွက်ချက်မှု ကုန်ကျစရိတ် လျှော့ချရန် weight များ၊ activation များ သို့မဟုတ် cache များကို lower-precision format များဖြင့် ဖော်ပြခြင်း ဖြစ်သည်။ ဥပမာ (ခ) တွင် 70B သည် fp16 မှ 4-bit သို့ ရွေ့လျှင် 130.385 GiB မှ 32.596 GiB သို့ ကျဆင်းသည်၊ ဆိုလိုသည်မှာ 64 GiB ခန့် သီးသန့်ထားသည့် accelerator တစ်လုံးပေါ် တွင် copy တစ်ခု တင်နိုင်လာသည် (fp16 တွင် မဆံ့ပါ)။ 7B တွင် 4-bit ဖြင့် copy ၁၉ ခုအထိ တင်နိုင်သည်ဟု တွက်ချက်မှုက ပြသည်၊ fp16 တွင် ၄ ခုသာ ဖြစ်သည်။ ဤအချက်သည် throughput (တစ်ပြိုင်နက် ဝန်ဆောင်နိုင်သည့် request အရေအတွက်) ကို မြှင့်စေပြီး serving cost ကို လျှော့ချသည်။ သို့သော် bit အလုံးအစု တစ်ခုမှ အခြား တစ်ခုသို့ ရွေ့ခြင်းသည် တူညီသည့် end-to-end memory သို့မဟုတ် အရှိန် အချိုးကို အာမမခံနိုင်ပါ၊ metadata၊ kernel၊ cache နှင့် hardware အထောက်အပံ့တို့သည် အရေးပါသည်၊ ဤအချက်သည် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်` အမျိုးအစား ဖြစ်သည်။

#### CUDA

CUDA သည် NVIDIA ၏ platform နှင့် programming model ဖြစ်ပြီး deep-learning framework များသည် ၎င်း၏ library များနှင့် kernel များကို အသုံးပြု၍ tensor operation အများအပြားကို တစ်ပြိုင်နက် execute လုပ်သည်။ ဤအလွှာသည် achieved FLOPs နှင့် peak FLOPs အကြား အချိုး (compute utilisation) ကို ဆုံးဖြတ်ပေးသည့်အတွက် tokens/s အပေါ် တိုက်ရိုက် သက်ရောက်သည်။ kernel version၊ driver နှင့် quantization အထောက်အပံ့တို့ မကိုက်ညီလျှင် ဖော်မြူလာအရ ရနိုင်သည့် ကိန်းဂဏန်းကို လက်တွေ့တွင် မရရှိနိုင်ပါ၊ ထို့ကြောင့် ဤအပိုင်းရှိ တန်ဖိုးများသည် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။ GPU acceleration သည် CUDA နှင့် ထပ်တူကျသည့် အဓိပ္ပာယ် မဟုတ်ပါ၊ အခြား hardware နှင့် software stack များလည်း တည်ရှိသည်။ serving engineer သည် image version နှင့် kernel ရွေးချယ်မှုကို capacity ခန့်မှန်းမှုနှင့် တွဲဖက် မှတ်တမ်းတင်ရမည်။

#### MoE (Mixture of Experts)

MoE သည် expert subnetwork အများအပြား ပါဝင်ပြီး သင်ယူထားသည့် router တစ်ခုက token တစ်စီ အတွက် အခွဲ တစ်စုကို ရွေးချယ်ပေးသည်။ sparse activation သည် forward pass တိုင်းတွင် expert အားလုံးကို အသုံးမပြုဘဲ စုစုပေါင်း parameter စွမ်းရည်ကို တိုးမြှင့်နိုင်သည်၊ ထို့ကြောင့် active parameter (compute ကို ဆုံးဖြတ်သည့် ကိန်း) နှင့် total parameter (VRAM ကို ဆုံးဖြတ်သည့် ကိန်း) သည် ကွဲပြားသွားသည်။ ဤကွဲပြားမှုသည် accelerator တစ်လုံးပေါ် တွင် ချုံ့၍ မရနိုင်သည့် အခြေအနေ ဖြစ်စေပြီး expert parallelism လိုအပ်မှုကို ဖြစ်ပေါ်စေသည်။ compute၊ memory၊ communication၊ routing balance နှင့် quality တို့သည် သက်ဆိုင်ရာ ဖွဲ့စည်းပုံနှင့် serving စနစ်အပေါ် မှီခိုသည်ဟု မှတ်သားရမည်။ serving engineer သည် total parameter အတွက် VRAM ကို ကြိုတင်စစ်ဆေးရမည်၊ အကြောင်းမှာ active parameter နည်းခြင်းသည် memory လျော့ခြင်း မဟုတ်ပါ။

### မိသားစု (င) — တိုင်းတာမှု (measurement)

#### Perplexity

Perplexity သည် သတ်မှတ်ထားသည့် tokenization နှင့် logarithm သဘောတူညီချက် အောက်တွင် တွက်ချက်သည့် ပျမ်းမျှ negative log-likelihood ကို exponent ပြန်တင်ထားသည့် တန်ဖိုး ဖြစ်သည်၊ တန်ဖိုး နည်းလျှင် model က probability ပိုမြင့်စွာ ပေးသည်။ ၎င်းသည် compute အရင်းအမြစ် သုံးစွဲသည့် evaluation အဆင့်တွင် တွက်ရသည့် ကိန်း ဖြစ်သောကြောင့် capacity budget တွင် evaluation အချိန်ကို သီးသန့် ထားရမည်။ model အစားထိုးလျှင် perplexity ကို tokenizer တူညီသည့် အခြေအနေတွင်သာ နှိုင်းယှဉ်နိုင်သည့်အတွက် ၎င်းသည် မှားယွင်းသည့် အစားထိုးမှုကို တားဆီးသည့် quality gate အဖြစ် အသုံးပြုရမည်။ ၎င်းသည် အချက်အလက် တိကျမှု (factuality) သို့မဟုတ် အသုံးဝင်မှုကို တိုက်ရိုက် တိုင်းတာသည် မဟုတ်ပါ။ serving engineer သည် perplexity ကို precision သို့မဟုတ် quantization အဆင့်တိုင်း၏ အရည်အသွေး ပြောင်းလဲမှုကို တိုင်းတာရန် အသုံးပြုသည်။

## ၄။ လက်တွေ့ တွက်ချက်မှု လေးခု

ဤအပိုင်းရှိ output အားလုံးသည် အောက်တွင် ဖော်ပြသည့် command များကို တကယ် run ၍ ရရှိသည့် ရလဒ်များ ဖြစ်သည်။ script များသည် standard library သာ အသုံးပြုပြီး deterministic ဖြစ်သည်။

### (က) KV cache — context 8K၊ 32K၊ 128K ၊ fp16 နှင့် int8၊ batch 1 နှင့် 32

ဖော်မြူလာ — `bytes = 2 (K နှင့် V) × layers × heads × head_dim × sequence_length × bytes_per_element × batch`။ ယူဆချက် — layers 32၊ heads 32၊ head_dim 128 (d_model 4096)၊ fp16 သည် 2 byte/element၊ int8 သည် 1 byte/element။

```text
$ python3 guides/02_models_and_inference/scripts/ex_a_kv_cache.py
reference model: layers=32 heads=32 head_dim=128 d_model=4096
KV bytes per token (fp16, batch 1) = 2*32*32*128*2 = 524288 B = 0.500 MiB

context   prec   batch  KV caches (GiB)          bytes
8192      fp16   1               4.000     4294967296
8192      fp16   32            128.000   137438953472
8192      int8   1               2.000     2147483648
8192      int8   32             64.000    68719476736
32768     fp16   1              16.000    17179869184
32768     fp16   32            512.000   549755813888
32768     int8   1               8.000     8589934592
32768     int8   32            256.000   274877906944
131072    fp16   1              64.000    68719476736
131072    fp16   32           2048.000  2199023255552
131072    int8   1              32.000    34359738368
131072    int8   32           1024.000  1099511627776

headroom check against one 80 GB accelerator with 16 GiB reserved (64 GiB usable):
  context 8192    fp16  per sequence    4.00 GiB -> largest batch that fits = 16
  context 8192    int8  per sequence    2.00 GiB -> largest batch that fits = 32
  context 32768   fp16  per sequence   16.00 GiB -> largest batch that fits = 4
  context 32768   int8  per sequence    8.00 GiB -> largest batch that fits = 8
  context 131072  fp16  per sequence   64.00 GiB -> largest batch that fits = 1
  context 131072  int8  per sequence   32.00 GiB -> largest batch that fits = 2
```

ဤတန်ဖိုးများသည် architecture ဖော်မြူလာ အရသာ တွက်ချက်ထားခြင်း ဖြစ်ပြီး serving library ၏ memory pool စီမံမှု အလိုက် အနည်းငယ် ကွာခြားနိုင်သည့်အတွက် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

### (ခ) ဝန်ဆောင်မှု ပေးသည့် weight memory — 7B၊ 70B၊ 405B ၊ fp16 နှင့် 4-bit

ဖော်မြူလာ — `weight_bytes = parameter_count × bytes_per_parameter`၊ ဤနေရာတွင် runtime အပိုအလွှာ (sharding၊ metadata၊ activation) မပါဝင်ပါ။ ယူဆချက် — fp16 သည် 2 byte/parameter၊ 4-bit သည် 0.5 byte/parameter၊ accelerator တစ်လုံးလျှင် 80 GB ဖြစ်ပြီး 16 GiB ကို KV cache အတွက် သီးသန့်ထားသည့်အတွက် weight အတွက် 64 GiB အသုံးပြုနိုင်သည်။

```text
$ python3 guides/02_models_and_inference/scripts/ex_b_weights.py
usable weight budget = 64 GiB (80 GB accelerator - 16 GiB reserved)

params prec            GiB           GB copies @64GiB
7B     fp16         13.039       14.000            4
7B     4-bit         3.260        3.500           19
70B    fp16        130.385      140.000            0
70B    4-bit        32.596       35.000            1
405B   fp16        754.371      810.000            0
405B   4-bit       188.593      202.500            0

ratio fp16/4-bit per model family = 97.79 GiB saved for 70B
```

ဤဇယားက 4-bit ၏ အကျိုးအမြတ်ကို တိုက်ရိုက် ပြသည် — 70B သည် fp16 တွင် accelerator တစ်လုံးပေါ် မဆံ့သော်လည်း 4-bit တွင် တစ်ခု ဆံ့သည်။

### (ဂ) attention နှင့် feed-forward FLOPs — context 2K၊ 8K၊ 32K

ဖော်မြူလာ (multiply-accumulate ကို 2 FLOPs အဖြစ် ရေတွက်သည်၊ forward pass၊ batch 1) —
attention core တစ်လွှာလျှင် `4 × seq² × d_model`၊ attention projection တစ်လွှာလျှင် `8 × seq × d_model²`၊ feed-forward တစ်လွှာလျှင် `4 × seq × d_model × d_ff`။ ယူဆချက် — layers 32၊ d_model 4096၊ d_ff 11008။ attention core သည် FFN ကို `seq = d_ff = 11008` တွင် ကျော်လွန်သည်။

```text
$ python3 guides/02_models_and_inference/scripts/ex_c_attention_ffn.py
reference: layers=32 d_model=4096 d_ff=11008 ; attention core = FFN when seq = d_ff = 11008

seq      attn core TFLOP  attn proj TFLOP        ffn TFLOP   core/ffn
2048                2.20             8.80            11.82      0.186
8192               35.18            35.18            47.28      0.744
32768             562.95           140.74           189.12      2.977

seq 2048   attention total (core+proj) is 48.2% of the layer FLOPs; core alone 9.6%
seq 8192   attention total (core+proj) is 59.8% of the layer FLOPs; core alone 29.9%
seq 32768  attention total (core+proj) is 78.8% of the layer FLOPs; core alone 63.1%
```

### (ဃ) cost per million output tokens — batch 1 နှင့် batch 32

ဤတွက်ချက်မှုသည် roofline ဖော်မြူလာမှ ရရှိသည့် တန်ဖိုး ဖြစ်ပြီး benchmark တိုင်းတာမှု မဟုတ်ပါ။ ဖော်မြူလာ — `tokens/s = batch × bandwidth ÷ (weight_bytes + batch × kv_bytes_per_token)`၊ ထို့နောက် `cost_per_million = price_per_hour ÷ (tokens_per_second × 3600) × 10⁶`။ ယူဆချက် — model 7B fp16 (14.0 GB weight)၊ KV token တစ်လုံးလျှင် 512 KiB (ဥပမာ (က) ၏ reference model)၊ bandwidth 3350 GB/s၊ accelerator တစ်နာရီ စျေးနှုန်း USD 2.50၊ batch 32 အတွက် compute ကန့်သတ်ချက် 990 TFLOPS ကို ထပ်ဆောင်း စစ်ဆေးသည်။ throughput၊ bandwidth နှင့် စျေးနှုန်း အားလုံးသည် GPU model၊ library version နှင့် vendor အလိုက် ကွာခြားသည့်အတွက် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

```text
$ python3 guides/02_models_and_inference/scripts/ex_d_cost.py
weights = 14.00 GB fp16 ; KV per token per sequence = 512.0 KiB ; price = USD 2.50/h

batch       bytes/step          tok/s tok/s compute-cap    USD / 1e6 tok
1            1.400e+10          239.3        70714.3           2.9023
32           1.402e+10         7648.0      2262857.1           0.0908

cost ratio batch 1 / batch 32 = 31.96x
```

ရလဒ်က ပြသည့် အဓိက အချက်မှာ batch 32 တွင် weight byte သည် step အရေအတွက် အနည်းငယ်ဖြင့် အကြိမ်များစွာ ပြန်လည် အသုံးပြုခံရခြင်းကြောင့် cost per million tokens သည် ခန့်မှန်းခြေ ၃၂ ဆ ကျဆင်းခြင်း ဖြစ်သည်။ ဤအကျိုးအမြတ်သည် VRAM (KV cache) ဖြင့် ဝယ်ယူရသည်၊ ဥပမာ (က) တွင် ထို လဲလှယ်မှုကို ကိန်းဂဏန်းဖြင့် ပြထားသည်။

## ၅။ ဤနယ်ပယ်မှ ဆင်းသက်လာသည့် ထုတ်လုပ်မှု ဆုံးဖြတ်ချက် ခြောက်ခု

**၁။ Context window သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Attention၊ Self-Attention၊ KV Cache၊ Time to First Token (TTFT)။ သက်သေပြသည့် မက်ထရစ် — context length အလိုက် KV cache byte နှင့် prefill latency။ ဥပမာ (က) က context 131072 တွင် fp16 batch 32 သည် 2048 GiB လိုသည်ဟု ပြသည်၊ ထို့ကြောင့် context ကို ကြော်ငြာ အရေအတွက်ဖြင့် မသတ်မှတ်ရ၊ accelerator အရေအတွက်နှင့် တွဲဖက် သတ်မှတ်ရမည်။

**၂။ Precision ရွေးချယ်ခြင်း** — မှီခိုသည့် term များ — Quantization၊ Parameter၊ KV Cache။ သက်သေပြသည့် မက်ထရစ် — bits per parameter၊ weight GiB၊ accelerator တစ်လုံးပေါ် တင်နိုင်သည့် copy အရေအတွက်။ ဥပမာ (ခ) အရ 70B သည် 4-bit တွင်သာ ဆံ့သည်၊ ထို့ကြောင့် precision ဆုံးဖြတ်ချက်သည် capacity ဆုံးဖြတ်ချက် ဖြစ်သည်။

**၃။ Batching policy သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Autoregressive၊ KV Cache၊ Attention၊ Inference။ သက်သေပြသည့် မက်ထရစ် — tokens/s နှင့် inter-token latency။ ဥပမာ (ဃ) က batch 1 မှ batch 32 သို့ ရွေ့လျှင် cost per million tokens သည် 2.9023 USD မှ 0.0908 USD သို့ ကျဆင်းသည်ဟု ပြသည်၊ သို့သော် batch ကြီးလျှင် KV cache VRAM လိုအပ်ချက် တိုးသည်။

**၄။ Cache strategy သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — KV Cache၊ Streaming၊ Time to First Token (TTFT)။ သက်သေပြသည့် မက်ထရစ် — prefix cache hit rate နှင့် client-side TTFT။ ရှည်သည့် system prompt ကို ပြန်လည် အသုံးပြုသည့် prefix caching သည် prefill compute ကို ချွေတာသော်လည်း cache ကိုယ်တိုင် VRAM ယူသည်ကို ဥပမာ (က) ၏ token တစ်လုံးလျှင် 0.5 MiB ကိန်းဖြင့် တွက်ရမည်။

**၅။ Capacity headroom သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Parameter၊ Quantization၊ MoE (Mixture of Experts)၊ Attention။ သက်သေပြသည့် မက်ထရစ် — VRAM အသုံးပြုမှု ရာခိုင်နှုန်း (weight + KV + activation)။ MoE တွင် total parameter က VRAM ကို ဆုံးဖြတ်ပြီး active parameter က compute ကို ဆုံးဖြတ်သည့်အတွက် ဤနှစ်ကိန်းကို ခွဲခြား မှတ်တမ်းတင်ရမည်။

**၆။ Cost monitoring သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Inference၊ Streaming၊ Stop Sequence၊ Decoding Strategy၊ Top-k Sampling၊ Nucleus Sampling (Top-p)။ သက်သေပြသည့် မက်ထရစ် — cost per million output tokens (input နှင့် output ခွဲခြား၍)။ output token အရေအတွက်သည် decoding setting အလိုက် ကွာခြားသည့်အတွက် ဤမက်ထရစ်ကို model version၊ prompt အရှည် နှင့် decoding configuration နှင့် တွဲဖက် တိုင်းတာရမည်။

## လေ့ကျင့်ခန်း ဆက်စပ်မှု

ဤစာတမ်းရှိ ဖော်မြူလာများကို `guides/02_models_and_inference/labs/lab_kv_cache.py`၊ `lab_quantization.py`၊ `lab_attention_cost.py`၊ `lab_batching.py`၊ `lab_context_budget.py`၊ `lab_sampling.py` တို့ဖြင့် လက်တွေ့ စမ်းသပ်နိုင်သည်။ ဤစာတမ်းရှိ ကိန်းဂဏန်းများသည် ထို lab များ ရှိခြင်း အပေါ် မှီခိုသည် မဟုတ်ပါ။

## References

- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed၊ `rohitg00/ai-engineering-from-scratch`။
- ဤနယ်ပယ်၏ term ရှင်းလင်းချက် — `terms/02_models_and_inference.md`။
- ဤနယ်ပယ်၏ term အစဉ် အခြေခံ — `glossary/by_area/02_models_and_inference.json`။
