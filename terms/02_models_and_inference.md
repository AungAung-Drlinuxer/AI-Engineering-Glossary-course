# 02 — မော်ဒယ်များနှင့် ခန့်မှန်းချက် ထုတ်လုပ်ခြင်း (Models & Inference)

ဤနယ်ပယ်သည် ဘာသာစကားနှင့် ဖန်တီးမှုဆိုင်ရာ မော်ဒယ်များ၏ တွက်ချက်မှု ဖွဲ့စည်းပုံများနှင့် လေ့ကျင့်ပြီး မော်ဒယ်တစ်ခုမှ ရလဒ် ထုတ်လုပ်သည့် အဆင့်ကို ဖော်ပြသည်။ Attention နှင့် Transformer ကဲ့သို့သော အခြေခံ ဖွဲ့စည်းပုံများ၊ CNN၊ GAN၊ VAE နှင့် diffusion model ကဲ့သို့သော မော်ဒယ် မိသားစုများ၊ ထို့အပြင် decoding၊ KV cache၊ speculative decoding၊ streaming နှင့် TTFT ကဲ့သို့သော ခန့်မှန်းချက် ထုတ်လုပ်သည့် လုပ်ငန်းစဉ်များကို ဤနယ်ပယ်တွင် စုစည်းထားသည်။ ခေါင်းစဉ် ၂၉ ခု ပါဝင်သည်။

ဤ term များသည် အတူတကွ အရေးပါသည်၊ အကြောင်းမှာ မော်ဒယ်တစ်ခု၏ တွက်ချက်မှု ဖွဲ့စည်းပုံနှင့် output ဖြစ်ပေါ်လာသည့် လုပ်ငန်းစဉ်တို့သည် တစ်ခုနှင့် တစ်ခု ခွဲခြား၍ မရသောကြောင့် ဖြစ်သည်။ လေ့ကျင့်ပြီးသား weight များသည် မည်သည့် အချက်အလက်ကို ဖော်ပြသည်ကို သိရုံဖြင့် မလုံလောက်ပါ။ မည်သည့် decoding နည်းလမ်းကို ရွေးချယ်သည်၊ cache ကို မည်သို့ အသုံးပြုသည်၊ မည်သည့် တိကျမှုဖြင့် တန်ဖိုးများကို သိမ်းဆည်းသည် စသည့် အချက်များက လက်တွေ့ အရည်အသွေး၊ အရှိန်၊ memory အသုံးပြုမှုနှင့် ကုန်ကျစရိတ်ကို ဆုံးဖြတ်သည်။ ထို့ကြောင့် ဖွဲ့စည်းပုံ ဆိုင်ရာ term များနှင့် inference ဆိုင်ရာ term များကို တွဲဖက်၍ နားလည်ရမည်။

Term တစ်ခုစီတွင် အောက်ပါ field များ ပါဝင်သည်။ **မြန်မာ** တွင် term ၏ မြန်မာ အမည် သို့မဟုတ် အနီးစပ်ဆုံး ဖော်ပြချက်ကို ပေးထားသည်။ **ဆိုလိုသည့် အဓိပ္ပာယ်** သည် source glossary ၏ အင်ဂျင်နီယာ အဓိပ္ပာယ်ကို မြန်မာလို တိုက်ရိုက် ရှင်းလင်းထားခြင်း ဖြစ်ပြီး အနှစ်ချုပ် မဟုတ်ပါ။ **အရေးပါသည့် အကြောင်းရင်း** သည် မည်သည့် စနစ်တွင် မည်သို့ သက်ရောက်သည်ကို ဖော်ပြသည်။ **မကြာခဏ ရောထွေးမှု** နှင့် **လက်တွေ့** ကို source တွင် ပါဝင်ပါက သာ ထည့်သွင်းထားသည်။ technical term များ (tokenizer, quantization, attention, KV cache, temperature, logits စသည်) ကို မြန်မာ စာကြောင်းအတွင်း အင်္ဂလိပ်အတိုင်း ထားရှိသည်။

**English (source)** field သည် source glossary ၏ မူရင်း အင်္ဂလိပ် စာသား ဖြစ်ပြီး စကားလုံး တစ်လုံးမျှ မပြင်ဆင်ရ၊ ဖြတ်တောက်၍ လည်း မရပါ။ ထို အင်္ဂလိပ် စာသားသည် အတည်ပြုရန် အခြေခံ စာသား ဖြစ်သည်၊ မြန်မာ ရှင်းလင်းချက်သည် ၎င်း၏ အဓိပ္ပာယ်နှင့် တိုက်ရိုက် ကိုက်ညီရမည်။ Entry များ၏ အစဉ်သည် source ၏ JSON slice အစဉ်အတိုင်း ဖြစ်သည်။ ဖိုင် အဆုံးတွင် Self-check နှင့် References ပါဝင်သည်။

### Attention

**မြန်မာ:** အာရုံစိုက်မှု ယန္တရား (Attention)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** query vector များကို key vector များနှင့် နှိုင်းယှဉ်ခြင်းဖြင့် ရရှိလာသည့် score များကို normalize လုပ်ပြီးနောက် ထို score များကို အသုံးပြု၍ value vector များကို ပေါင်းစပ်ခြင်းဖြင့် context ပါဝင်သည့် representation များကို တည်ဆောက်ပေးသည့် ယန္တရား ဖြစ်သည်။ mask များ၊ position စည်းမျဉ်းများ သို့မဟုတ် sparse pattern များဖြင့် မည်သည့် position များ ပါဝင်မည်ကို ကန့်သတ်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Attention သည် sequence အတွင်းရှိ position များအကြား အချက်အလက် စီးဆင်းမှုကို လမ်းကြောင်းချပေးနိုင်သည်၊ သို့သော် ၎င်းကိုယ်တိုင်က model နားလည်ခဲ့သည့် အကြောင်းအရာကို ရှင်းလင်းပြသည် သို့မဟုတ် သက်သေပြသည် မဟုတ်ပါ။
- **မကြာခဏ ရောထွေးမှု:** Attention weight များသည် computation coefficient များ ဖြစ်သည်၊ model ၏ ကျိုးကြောင်းဆင်ခြင်မှုကို သစ္စာရှိစွာ ဖော်ပြသည့် ရှင်းလင်းချက် မဟုတ်ပါ။
- **ဆက်စပ် term များ:** Self-Attention, Transformer, KV Cache
- **Learn it:** [Self-Attention from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/07-transformers-deep-dive/02-self-attention-from-scratch/)
- **English (source):** A mechanism that forms contextual representations by comparing query vectors with key vectors, normalizing the resulting scores, and using them to combine value vectors. Masks, position rules, or sparse patterns can restrict which positions participate. Attention lets a model route information between sequence positions, but it does not by itself explain or prove what the model understood.

### Autoregressive

**မြန်မာ:** ရှေးရှိပြီးသား token များမှ နောက် token ကို အစဉ်လိုက် ခန့်မှန်းသည့် နည်းလမ်း (Autoregressive)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** output token တစ်ခုစီကို ၎င်း၏ အရင် position ရှိ token များမှ ခန့်မှန်းသည့် factorization ဖြစ်သည်။ Generation လုပ်ဆောင်စဉ် ရွေးချယ်လိုက်သည့် token ကို sequence ၏ အဆုံးတွင် ထည့်သွင်းပြီး ထို token သည် နောက် ခန့်မှန်းမှု၏ context တွင် ပါဝင်လာသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** စာသား ထုတ်လုပ်မှုသည် token တစ်လုံးချင်း အစဉ်လိုက် ဖြစ်ပေါ်သောကြောင့် ထပ်တလဲလဲ တွက်ချက်မှုကို လျှော့ချသည့် KV cache နှင့် ရွေးချယ်မှုကို ထိန်းညှိသည့် Temperature စသည့် လုပ်ငန်းစဉ်များသည် ဤအစဉ်လိုက် သဘောသဘာဝအပေါ် မှီခိုသည်။
- **မကြာခဏ ရောထွေးမှု:** ခန့်မှန်းသည့် အလုံးအစုသည် token ဖြစ်သည်၊ word ဖြစ်ရန် မလိုအပ်ပါ။ ထို့အပြင် generation တွင် အမြင့်ဆုံး probability ရှိသည့် token ကို အမြဲ ရွေးချယ်သည့် နည်းလမ်းသာ မဟုတ်ဘဲ အခြား decoding နည်းလမ်းများကိုလည်း အသုံးပြုနိုင်သည်။
- **ဆက်စပ် term များ:** Token, Temperature, KV Cache
- **English (source):** A factorization in which each output token is predicted from the tokens that precede it. During generation, the selected token is appended to the sequence and becomes part of the next prediction's context.

### CNN (Convolutional Neural Network)

**မြန်မာ:** convolution လုပ်ဆောင်ချက်ကို အသုံးပြုသည့် နျူရယ်ကွန်ရက် (CNN)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** convolution operation များ (input အပေါ် လျှောကျလားသည့် filter များ) ကို အသုံးပြု၍ ဒေသဆိုင်ရာ (local) pattern များကို ရှာဖွေသည့် neural network ဖြစ်သည်။ convolution များကို အထပ်ထပ် စုပုံခြင်းဖြင့် ပိုမို ရှုပ်ထွေးသည့် feature များ ဖြစ်သည့် edge၊ texture၊ object များကို ရှာဖွေနိုင်လာသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** filter မျှဝေအသုံးပြုခြင်းဖြင့် local pattern ကို ရှာဖွေသည့် ဤဖွဲ့စည်းပုံသည် ရုပ်ပုံ များအတွက် အသုံးများပြီး ၎င်း၏ inductive bias သည် စနစ်တစ်ခု မည်သည့် feature များကို လွယ်ကူစွာ သင်ယူနိုင်သည်ကို သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** convolution များသည် အသံ (audio)၊ အချိန်စဉ် အချက်အလက် (time series) နှင့် အခြား grid ပုံစံ data များတွင်လည်း အလုပ်လုပ်သည်။
- **ဆက်စပ် term များ:** Feature, Inductive Bias, Activation Function
- **English (source):** A neural network that uses convolution operations (sliding filters over the input) to detect local patterns. Stacking convolutions detects increasingly complex features: edges, textures, objects.

### CUDA

**မြန်မာ:** မြန်မာလို တိုက်ရိုက် ခေါ်ဝေါ်မှု မရှိ — NVIDIA ၏ GPU များပေါ်တွင် အထွေထွေ တွက်ချက်မှု ပြုလုပ်နိုင်သည့် platform နှင့် programming model

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** NVIDIA ၏ platform နှင့် programming model ဖြစ်ပြီး ၎င်းနှင့် ကိုက်ညီသည့် GPU များပေါ်တွင် general-purpose computation ကို လုပ်ဆောင်နိုင်သည်။ deep-learning framework များသည် CUDA library များနှင့် kernel များကို အသုံးပြု၍ tensor operation အများအပြားကို တစ်ပြိုင်နက် execute လုပ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** deep-learning framework များတွင် tensor တွက်ချက်မှု အများအပြားကို တစ်ပြိုင်နက် လုပ်ဆောင်နိုင်စေသည့် အလွှာမှာ ဤ platform ဖြစ်သောကြောင့် လေ့ကျင့်ခြင်းနှင့် inference အရှိန်သည် CUDA အထောက်အပံ့အပေါ် မှီခိုသည်။
- **မကြာခဏ ရောထွေးမှု:** GPU acceleration သည် CUDA နှင့် ထပ်တူကျသည့် အဓိပ္ပာယ် မဟုတ်ပါ၊ အခြား hardware နှင့် software stack များလည်း တည်ရှိသည်။
- **ဆက်စပ် term များ:** Tensor, Mixed Precision, JAX
- **English (source):** NVIDIA's platform and programming model for general-purpose computation on compatible GPUs. Deep-learning frameworks use CUDA libraries and kernels to execute many tensor operations in parallel.

### Decoder

**မြန်မာ:** representation တစ်ခုမှ output အဖြစ် ပြောင်းလဲပေးသည့် အစိတ်အပိုင်း (Decoder)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** representation တစ်ခုကို output အဖြစ် ပြောင်းလဲပေးသည့် အစိတ်အပိုင်း ဖြစ်သည်။ encoder-decoder transformer တွင် decoder သည် masked self-attention နှင့် cross-attention ကို အသုံးပြု၍ output များကို ထုတ်လုပ်သည်။ decoder-only language model များမှာမူ causal stack တစ်ခုတည်းမှ ထုတ်လုပ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** decoder-only အမျိုးအစား model များတွင် causal stack တစ်ခုတည်းမှ ထုတ်လုပ်သောကြောင့် masking စည်းမျဉ်းသည် token တစ်လုံးစီ မည်သည့် position များကို တွေ့မြင်နိုင်သည်ကို သတ်မှတ်သည်။
- **ဆက်စပ် term များ:** Encoder, Transformer, Autoregressive
- **English (source):** A component that maps a representation into an output. In an encoder-decoder transformer, the decoder uses masked self-attention and cross-attention to generate outputs. Decoder-only language models instead generate from a single causal stack.

### Decoding Strategy

**မြန်မာ:** ခန့်မှန်းချက် score များမှ token များ ရွေးချယ်သည့် algorithm (Decoding Strategy)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** model ၏ next-token score အစဉ်ကို ရွေးချယ်ပြီးသား token များနှင့် ပြီးစီးသည့် output အဖြစ် ပြောင်းလဲပေးသည့် algorithm ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** logits တူညီသည့် အခြေအနေတွင်ပင် greedy ရွေးချယ်ခြင်း၊ sampling၊ truncation နှင့် search နည်းလမ်းများက အရည်အသွေး၊ ကွဲပြားမှု (diversity)၊ latency နှင့် ထပ်တူ ပြန်လည်ရရှိနိုင်မှု (repeatability) တို့ကို ကွဲပြားစွာ ဖြစ်ပေါ်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** decoding သည် output များ မည်သို့ ရွေးချယ်ခံရသည်ကို ပြောင်းလဲသည်၊ model ၏ လေ့ကျင့်ပြီး parameter များကို မပြောင်းလဲပါ၊ အသိပညာ ထပ်တိုး မပေးပါ။
- **လက်တွေ့:** task ၏ decoding setting များ၊ ရပ်တန့်သည့် စည်းမျဉ်းများနှင့် seed အပြုအမူကို eval configuration တွင် သတ်မှတ်ထားရမည်၊ ထိုအခါ ရလဒ်များကို တရားမျှတစွာ နှိုင်းယှဉ်နိုင်သည်။
- **ဆက်စပ် term များ:** Autoregressive, Temperature, Top-k Sampling, Nucleus Sampling (Top-p)
- **English (source):** The algorithm that converts a model's sequence of next-token scores into selected tokens and a completed output. Greedy selection, sampling, truncation, and search can produce different quality, diversity, latency, and repeatability from the same logits.

### Diffusion Model

**မြန်မာ:** မြန်မာလို တိုက်ရိုက် ခေါ်ဝေါ်မှု မရှိ — noise မှ စတင်၍ အဆင့်ဆင့် ပြန်လည် ရှင်းလင်းပေးသည့် ဖန်တီးနိုင်သည့် model (Diffusion Model)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အဆင့်ဆင့် ဆူညံသံ (noise) ထည့်သွင်းသည့် ဖြစ်စဉ်နှင့် ၎င်းကို ပြောင်းပြန်လှန်ပေးသည့် သင်ယူထားသော ဖြစ်စဉ်တို့ကို အခြေခံ၍ လေ့ကျင့်ထားသည့် generative model ဖြစ်သည်။ Sampling ပြုလုပ်သည့်အခါ အများအားဖြင့် noise မှ စတင်ပြီး denoise လုပ်သည့် အဆင့်များကို အကြိမ်ကြိမ် လုပ်ဆောင်သည်၊ အချို့ အခြေအနေများတွင် သင်ယူထားသည့် latent space အတွင်း၌ လုပ်ဆောင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် ရုပ်ပုံသီးသန့် နည်းစနစ် မဟုတ်ဘဲ ယေဘုယျ generative framework တစ်ခု ဖြစ်သောကြောင့် ဖန်တီးမှုဆိုင်ရာ စနစ်များတွင် ရွေးချယ်နိုင်သည့် ဖွဲ့စည်းပုံ တစ်ခု အဖြစ် သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** diffusion သည် ယေဘုယျ generative framework တစ်ခု ဖြစ်သည်၊ ရုပ်ပုံ (image) သီးသန့် နည်းစနစ် မဟုတ်ပါ။
- **ဆက်စပ် term များ:** Latent Space, VAE (Variational Autoencoder), Inference
- **English (source):** A generative model trained around a progressive noising process and a learned reverse process. Sampling usually begins from noise and applies repeated denoising steps, sometimes in a learned latent space.

### Encoder

**မြန်မာ:** input ကို representation အဖြစ် ပြောင်းလဲပေးသည့် အစိတ်အပိုင်း (Encoder)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** input ကို representation တစ်ခုအဖြစ် ပြောင်းလဲပေးသည့် အစိတ်အပိုင်း ဖြစ်သည်။ transformer encoder သည် အများအားဖြင့် non-causal self-attention ကို အသုံးပြုပြီး mask များ ရှိပါက ထို mask များ၏ ကန့်သတ်ချက်အောက်တွင် position တစ်ခုစီသည် input တစ်လျှောက်လုံးရှိ context ကို ထည့်သွင်းစဉ်းစားနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** encoder ၏ output representation သည် နောက်ဆက်တွဲ task များအတွက် အသုံးပြုခံရသောကြောင့် မည်သည့် mask များဖြင့် context ကို ကန့်သတ်သည် ဆိုသည်က စနစ်တစ်ခု တွေ့မြင်နိုင်သည့် အချက်အလက် ပမာဏကို သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** encoder-only model များသည် autoregressive စာသား ထုတ်လုပ်ခြင်းအတွက် ပုံမှန်အားဖြင့် အသုံးပြုခြင်း မခံရသော်လည်း task head များမှတစ်ဆင့် output များ ထုတ်လုပ်နိုင်သည်။
- **ဆက်စပ် term များ:** Decoder, Transformer, Embedding
- **English (source):** A component that transforms input into a representation. A transformer encoder commonly uses non-causal self-attention, subject to any masks, so each position can incorporate context from across the input.

### GAN (Generative Adversarial Network)

**မြန်မာ:** ပြိုင်ဆိုင်လျက် လေ့ကျင့်သည့် ကွန်ရက် နှစ်ခု (GAN)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** generator network သည် လက်တွေ့နှင့် တူညီသည့် data ဖန်တီးရန် ကြိုးစားပြီး discriminator network သည် အစစ်နှင့် အတုကို ခွဲခြားရန် ကြိုးစားသည်။ ၎င်းတို့နှစ်ခုသည် အတူတကွ လေ့ကျင့်သည် — generator သည် discriminator ကို လှည့်ဖျားနိုင်မှု ပိုကောင်းလာသည်၊ discriminator သည် အတုကို ဖော်ထုတ်နိုင်မှု ပိုကောင်းလာသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** generator နှင့် discriminator နှစ်ခုလုံး တစ်ပြိုင်နက် တိုးတက်လာသည့် ဤပြိုင်ဆိုင်မှု ဖွဲ့စည်းပုံသည် data ဖန်တီးသည့် စနစ်များတွင် လေ့ကျင့်မှု လုပ်ငန်းစဉ်ကို သက်ရောက်သည်။
- **ဆက်စပ် term များ:** Loss Function, Latent Space, Diffusion Model
- **English (source):** A generator network tries to create realistic data while a discriminator network tries to tell real from fake. They train together: the generator gets better at fooling the discriminator, and the discriminator gets better at detecting fakes.

### GPT

**မြန်မာ:** GPT — Generative Pre-trained Transformer (generative transformer model မိသားစု၏ အမည်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** Generative Pre-trained Transformer ဖြစ်ပြီး sequence-prediction objective များဖြင့် ကြိုတင် လေ့ကျင့်ထားကာ နောက်ဆက်တွဲ အသုံးပြုမှုများအတွက် ပြင်ဆင်ထားသည့် generative transformer model များအတွက် မိသားစု အမည် ဖြစ်သည်။ Product အမည်များနှင့် model ဖွဲ့စည်းပုံများကို အပြန်အလှန် အစားထိုး အသုံးပြုနိုင်သည့် အရာများ အဖြစ် မယူဆရ။ အမည်တွင် generative သည် output ထုတ်လုပ်ခြင်းကို ရည်ညွှန်းပြီး pre-trained သည် အစောပိုင်း ကျယ်ပြန့်သည့် လေ့ကျင့်မှု အဆင့်ကို ရည်ညွှန်းသည်၊ transformer သည် ဖွဲ့စည်းပုံ မိသားစုကို ရည်ညွှန်းသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** GPT သည် ဖွဲ့စည်းပုံ မိသားစုကို ရည်ညွှန်းသည့် အမည် ဖြစ်သောကြောင့် စနစ်တစ်ခုတွင် အသုံးပြုသည့် model နှင့် ၎င်းအပေါ် တည်ဆောက်ထားသည့် product တို့ကို မတူညီသည့် အရာများ အဖြစ် ခွဲခြား သတ်မှတ်ရမည်။
- **ဆက်စပ် term များ:** Transformer, Autoregressive, LLM (Large Language Model)
- **English (source):** Generative Pre-trained Transformer, a family label for generative transformer models pretrained on sequence-prediction objectives and adapted for downstream use. Product names and model architectures should not be treated as interchangeable.

### Inductive Bias

**မြန်မာ:** လေ့ကျင့်သည့် စနစ်တွင် ပါဝင်နေသည့် ကြိုတင်ယူဆချက်များ (Inductive Bias)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** function သို့မဟုတ် representation အချို့ကို အခြားအရာများထက် ဦးစားပေးသည့် ဖွဲ့စည်းပုံဆိုင်ရာ သို့မဟုတ် စာရင်းအင်းဆိုင်ရာ ကြိုတင်ယူဆချက်များ ဖြစ်သည်။ convolution သည် locality နှင့် filter မျှဝေအသုံးပြုခြင်းကို ဦးစားပေးသည်၊ causal masking သည် ရှေ့ position များမှ ခန့်မှန်းခြင်းကို ဦးစားပေးသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ဤကြိုတင်ယူဆချက်များသည် model တစ်ခု လွယ်ကူစွာ သင်ယူနိုင်သည့် function အမျိုးအစားကို ကွာခြားစေသောကြောင့် ဖွဲ့စည်းပုံ ရွေးချယ်မှုသည် စနစ်တစ်ခု၏ အပြုအမူကို သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** transformer များတွင်လည်း tokenization၊ position ကိုင်တွယ်မှု၊ masking၊ architecture၊ data နှင့် objective များမှတစ်ဆင့် inductive bias များ ရှိသည်။
- **ဆက်စပ် term များ:** CNN (Convolutional Neural Network), Transformer, Feature
- **English (source):** Structural or statistical assumptions that favor some functions or representations over others. Convolution favors locality and shared filters; causal masking favors prediction from preceding positions.

### Inference

**မြန်မာ:** လေ့ကျင့်ပြီး model ကို အလုပ်လုပ်စေခြင်း (Inference)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** လေ့ကျင့်ပြီးသား model ကို execute လုပ်၍ prediction၊ score၊ embedding သို့မဟုတ် ထုတ်လုပ်သည့် token များကို ရရှိစေခြင်း ဖြစ်ပြီး ၎င်း၏ parameter များအတွက် ပုံမှန် training update တစ်ခုကို မပြုလုပ်ပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** model weight များ မပြောင်းလဲဘဲ prediction နှင့် token ထုတ်လုပ်ခြင်း အားလုံး ဤအဆင့်တွင် ဖြစ်ပေါ်သောကြောင့် စနစ်တစ်ခု၏ ဖြေကြားမှု လျင်မြန်မှုနှင့် တွက်ချက်မှု ကုန်ကျစရိတ်ကို ဤအဆင့်က သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** application တစ်ခုသည် inference လုပ်နေစဉ်အတွင်း cache များ၊ စကားပြောမှု အခြေအနေ (conversation state) သို့မဟုတ် ပြင်ပ memory ကို update လုပ်နိုင်သည်၊ သို့သော် model weight များ မပြောင်းလဲပါ။
- **ဆက်စပ် term များ:** Autoregressive, Streaming, KV Cache
- **English (source):** Executing a trained model to produce predictions, scores, embeddings, or generated tokens without performing an ordinary training update to its parameters.

### KV Cache

**မြန်မာ:** မြန်မာလို တိုက်ရိုက် ခေါ်ဝေါ်မှု မရှိ — key နှင့် value tensor များကို ပြန်လည် အသုံးပြုရန် သိမ်းဆည်းထားသည့် cache

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** autoregressive generation တွင် ရှေးဦး position များမှ key နှင့် value tensor များကို သိမ်းဆည်းထားခြင်း ဖြစ်သည်။ ၎င်းတို့ကို ပြန်လည် အသုံးပြုခြင်းဖြင့် မပြောင်းလဲသည့် prefix အတွက် attention projection များကို decode လုပ်သည့် အဆင့်တိုင်း ပြန်လည် တွက်ချက်ခြင်းကို ရှောင်ရှားနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် ထပ်တလဲလဲ တွက်ချက်မှုကို လျှော့ချပေးသော်လည်း sequence အရှည်၊ layer အရေအတွက်၊ batch နှင့် model configuration အပေါ် မှီခို၍ ကြီးထွားလာသည့် memory ကို အသုံးပြုသည်။
- **မကြာခဏ ရောထွေးမှု:** KV cache သည် sequence တစ်ခုအတွက် runtime attention state ဖြစ်သည်။ Prefix caching သည် အသုံးပြုနိုင်သည့် KV state ကို request များအကြား ပြန်လည် အသုံးပြုခြင်း ဖြစ်ပြီး prompt caching သည် ပိုမို ကျယ်ပြန့်သည့် provider သို့မဟုတ် application အဆင့် ပြန်လည် အသုံးပြုမှု သဘောတူညီချက် ဖြစ်သည်။
- **ဆက်စပ် term များ:** Attention, Autoregressive, Prefix Caching, Prompt Cache
- **Learn it:** [KV Cache and Flash Attention](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/07-transformers-deep-dive/12-kv-cache-flash-attention/)
- **English (source):** Stored key and value tensors from earlier positions in autoregressive generation. Reusing them avoids recomputing attention projections for the unchanged prefix at every decoding step. It reduces repeated computation but consumes memory that grows with sequence length, layers, batch, and model configuration.

### LLM (Large Language Model)

**မြန်မာ:** စွမ်းရည်ကြီးမားသည့် ဘာသာစကား မော်ဒယ် (LLM)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** စွမ်းရည် (capacity) နှင့် ကျယ်ပြန့်သည့် လေ့ကျင့်မှု လုံလောက်စွာ ရှိသည့်အတွက် prompting သို့မဟုတ် adaptation မှတစ်ဆင့် ဘာသာစကား task အများအပြားကို လုပ်ဆောင်နိုင်သည့် language model ဖြစ်သည်။ လက်ရှိ LLM အများစုသည် transformer ဖွဲ့စည်းပုံနှင့် sequence-prediction objective များကို အသုံးပြုကြသော်လည်း အရွယ်အစား သတ်မှတ်ချက်၊ data အရင်းအမြစ်နှင့် လေ့ကျင့်သည့် နည်းလမ်းများ ကွာခြားသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** LLM သည် system တစ်ခုအတွင်းရှိ model အစိတ်အပိုင်း တစ်ခု ဖြစ်သောကြောင့် application တစ်ခု၏ အပြုအမူကို ခွဲခြမ်းရာတွင် model နှင့် ၎င်းကို ဝန်းရံထားသည့် စနစ် အစိတ်အပိုင်းများကို ခွဲခြားရမည်။
- **မကြာခဏ ရောထွေးမှု:** LLM သည် model အစိတ်အပိုင်း တစ်ခု ဖြစ်သည်။ tool များ၊ retrieval၊ state၊ policy များနှင့် product logic တို့သည် ၎င်းကို ဝန်းရံထားသည့် စနစ်တွင် တည်ရှိသည်။
- **ဆက်စပ် term များ:** Transformer, Autoregressive, Agent Harness
- **English (source):** A language model with enough capacity and broad training to perform many language tasks through prompting or adaptation. Most current LLMs use transformer architectures and sequence-prediction objectives, but size thresholds, data sources, and training recipes vary.

### Logits

**မြန်မာ:** normalize မလုပ်ရသေးသည့် ကိန်းဂဏန်း score များ (Logits)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** normalization function သို့မဟုတ် decoding rule တစ်ခုက ၎င်းတို့ကို ရွေးချယ်မှုများ အဖြစ် မပြောင်းလဲမီ ဖြစ်နိုင်သည့် ရလဒ်များအတွက် model ၏ normalize မလုပ်ရသေးသည့် ကိန်းဂဏန်း score များ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Temperature၊ softmax၊ top-k နှင့် top-p တို့သည် logits အပေါ် လုပ်ဆောင်သည် သို့မဟုတ် logits မှ ဆင်းသက်လာသောကြောင့် logits သည် model ၏ တွက်ချက်မှုနှင့် ထုတ်လုပ်လိုက်သည့် token များကို ဆက်သွယ်ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** logits သည် probability များ မဟုတ်ပါ၊ သတ်မှတ်ထားသည့် transformation တစ်ခု မရှိဘဲ ဆက်စပ်မှု မရှိသည့် position များ၊ model များ သို့မဟုတ် task များအကြား နှိုင်းယှဉ်နိုင်သည် မဟုတ်ပါ။
- **လက်တွေ့:** API က ဖော်ပြသည့် အခြေအနေတွင် logits သို့မဟုတ် log probability များကို စစ်ဆေးရမည်၊ sampling မလုပ်မီ mask များကို အသုံးပြုရမည်၊ ကိန်းဂဏန်း ပမာဏ အကြီးအငယ်ကို calibration ရှိသည့် ယုံကြည်စိတ်ချမှု အဖြစ် အဓိပ္ပာယ် ကောက်ခြင်းကို ရှောင်ရမည်။
- **ဆက်စပ် term များ:** Softmax, Temperature, Token, Cross-Entropy
- **English (source):** The model's unnormalized numeric scores for candidate outcomes before a normalization function or decoding rule converts them into selections. Temperature, softmax, top-k, and top-p operate on or derive from logits, so logits connect model computation to generated tokens.

### MoE (Mixture of Experts)

**မြန်မာ:** ကျွမ်းကျင်သူ ကွန်ရက်အခွဲများ ပေါင်းစပ်ထားသည့် ဖွဲ့စည်းပုံ (MoE)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** expert subnetwork အများအပြား ပါဝင်ပြီး သင်ယူထားသည့် router တစ်ခုက input အလုံးအစု တစ်ခုစီ (များသောအားဖြင့် token တစ်လုံးစီ) အတွက် အခွဲ တစ်စုကို ရွေးချယ်ပေးသည့် ဖွဲ့စည်းပုံ ဖြစ်သည်။ sparse activation သည် forward pass တိုင်းတွင် expert အားလုံးကို အသုံးမပြုဘဲ စုစုပေါင်း parameter စွမ်းရည် (capacity) ကို တိုးမြှင့်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** compute၊ memory၊ communication၊ routing balance နှင့် quality တို့သည် သက်ဆိုင်ရာ ဖွဲ့စည်းပုံနှင့် serving စနစ်အပေါ် မှီခိုသည်။
- **မကြာခဏ ရောထွေးမှု:** product အမည်များသည် model developer က ထုတ်ဖော်မပြဘဲ MoE ဖွဲ့စည်းပုံ ဖြစ်သည်ဟု သက်သေပြသည် မဟုတ်ပါ။
- **ဆက်စပ် term များ:** Transformer, Model Router, Parameter
- **Learn it:** [Mixture of Experts](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/07-transformers-deep-dive/11-mixture-of-experts/)
- **English (source):** An architecture with multiple expert subnetworks and a learned router that selects a subset for each input unit, often each token. Sparse activation can increase total parameter capacity without using every expert on every forward pass. Compute, memory, communication, routing balance, and quality depend on the specific architecture and serving system.

### Nucleus Sampling (Top-p)

**မြန်မာ:** မြန်မာလို တိုက်ရိုက် ခေါ်ဝေါ်မှု မရှိ — cumulative probability သတ်မှတ်ချက် ပြည့်သည့် အသေးဆုံး အစုမှ ရွေးချယ်သည့် decode နည်းလမ်း (Top-p)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ရွေးချယ်ထားသည့် သတ်မှတ်ချက်အထိ cumulative probability ရောက်ရှိသည့် next-token candidate များ၏ အသေးဆုံး အစုမှ sampling လုပ်သည့် decoding နည်းလမ်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** candidate အစု၏ အရွယ်အစားသည် distribution အပေါ် မှီခို၍ ပြောင်းလဲသည်၊ မသေချာမှု ကျယ်ပြန့်သည့်အခါ ရွေးချယ်စရာ ပိုများစွာ ထားရှိပြီး probability စုစည်းနေသည့်အခါ ပိုနည်းစွာ ထားရှိသည်။
- **မကြာခဏ ရောထွေးမှု:** top-p သည် probability mass အဆင့်သတ်မှတ်ချက် ဖြစ်ပြီး top-k သည် အမြဲတမ်း သတ်မှတ်ထားသည့် အများဆုံး candidate အရေအတွက်ကို ထိန်းသိမ်းသည်။
- **လက်တွေ့:** temperature နှင့် stop setting များကို မပြောင်းလဲဘဲ ထားရှိပြီး သတ်မှတ်ချက်ကို အကဲဖြတ်ရမည်၊ ရလဒ်တိုင်းနှင့်အတူ decoding configuration အပြည့်အစုံကို မှတ်တမ်းတင်ရမည်။
- **ဆက်စပ် term များ:** Top-k Sampling, Temperature, Decoding Strategy, Softmax
- **English (source):** A decoding method that samples from the smallest set of next-token candidates whose cumulative probability reaches a chosen threshold. The candidate-set size adapts to the distribution, retaining more options when uncertainty is broad and fewer when probability is concentrated.

### Parameter

**မြန်မာ:** လေ့ကျင့်မှုအတွင်း သင်ယူသည့် တန်ဖိုး (Parameter)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** လေ့ကျင့်မှုအတွင်း သင်ယူသည့် တန်ဖိုး ဖြစ်ပြီး အများအားဖြင့် weight၊ bias၊ embedding element သို့မဟုတ် normalization parameter ဖြစ်သည်။ parameter အရေအတွက်သည် model စွမ်းရည် (capacity) ကို တိုင်းတာသည့် အတိုင်းအတာ တစ်ခု ဖြစ်သော်လည်း အရည်အသွေး၊ memory သို့မဟုတ် serving ကုန်ကျစရိတ်ကို တိုက်ရိုက် သတ်မှတ်သည် မဟုတ်ပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** model အရွယ်အစားကို ဖော်ပြရာတွင် parameter အရေအတွက်ကို အသုံးပြုသော်လည်း လက်တွေ့ memory နှင့် ကုန်ကျစရိတ် ခန့်မှန်းရာတွင် ၎င်းတို့ သိမ်းဆည်းသည့် numerical format နှင့် runtime အခြေအနေများကို ထည့်သွင်းစဉ်းစားရမည်။
- **မကြာခဏ ရောထွေးမှု:** parameter တစ်ခုစီအတွက် memory သည် numerical format၊ quantization metadata၊ sharding၊ optimizer state၊ activation များနှင့် runtime အပိုအလွှာ (overhead) များအပေါ် မှီခိုသည်။
- **ဆက်စပ် term များ:** Weight, MoE (Mixture of Experts), Quantization
- **English (source):** A value learned during training, commonly a weight, bias, embedding element, or normalization parameter. Parameter count is one measure of model capacity, but it does not directly determine quality, memory, or serving cost.

### Perplexity

**မြန်မာ:** ဘာသာစကား model တစ်ခု အံ့အားသင့်မှု အတိုင်းအတာ (Perplexity)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် tokenization နှင့် logarithm သဘောတူညီချက် အောက်တွင် တွက်ချက်သည့် ပျမ်းမျှ negative log-likelihood ကို exponent ပြန်တင်ထားသည့် တန်ဖိုး ဖြစ်သည်။ တန်ဖိုး နည်းသည်ဆိုလျှင် အကဲဖြတ်ခံရသည့် sequence အတွက် model က probability ပိုမြင့်စွာ ပေးခဲ့သည်ဟု အဓိပ္ပာယ်ရသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** model တစ်ခု၏ token များအတွက် probability ခန့်မှန်းမှု အတိုင်းအတာကို ကိန်းဂဏန်း တစ်ခုတည်းဖြင့် ဖော်ပြသည့်အတွက် အကဲဖြတ်မှု (evaluation) လုပ်ငန်းစဉ်များတွင် ဤတန်ဖိုးကို အသုံးပြုသည်၊ သို့သော် tokenizer သို့မဟုတ် အကဲဖြတ်မှု အခြေအနေ မတူညီပါက ၎င်းကို နှိုင်းယှဉ်နိုင်သည် မဟုတ်ပါ။
- **မကြာခဏ ရောထွေးမှု:** perplexity သည် tokenizer မတူညီသည့် အခြေအနေများ သို့မဟုတ် အကဲဖြတ်မှု စနစ် မတူညီသည့် အခြေအနေများအကြား နှိုင်းယှဉ်နိုင်သည် မဟုတ်ပါ၊ အချက်အလက် တိကျမှု (factuality) သို့မဟုတ် အသုံးဝင်မှုကို တိုက်ရိုက် တိုင်းတာသည် လည်း မဟုတ်ပါ။
- **ဆက်စပ် term များ:** Cross-Entropy, Token, Evaluation (Eval)
- **English (source):** The exponentiated average negative log-likelihood under a stated tokenization and logarithm convention. Lower values mean the model assigned higher probability to the evaluated sequence.

### Quantization

**မြန်မာ:** တန်ဖိုးများကို bit အနည်းငယ်ဖြင့် သိမ်းဆည်းခြင်း သို့မဟုတ် တွက်ချက်ခြင်း (Quantization)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** memory၊ bandwidth သို့မဟုတ် တွက်ချက်မှု ကုန်ကျစရိတ် လျှော့ချရန် weight များ၊ activation များ သို့မဟုတ် cache များကို ပိုနည်းသည့် တိကျမှု (lower-precision) format များဖြင့် ဖော်ပြခြင်း ဖြစ်သည်။ နည်းလမ်းများသည် calibration၊ granularity၊ data type နှင့် ပြောင်းလဲခြင်းကို လေ့ကျင့်မှု မတိုင်မီ၊ အလယ်တွင် သို့မဟုတ် အပြီးတွင် ပြုလုပ်ခြင်း တို့တွင် ကွာခြားသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** model တစ်ခုကို ပိုနည်းသည့် memory ဖြင့် serving လုပ်နိုင်ရန် ဤဖော်ပြမှု format ကို ရွေးချယ်သည့်အတွက် လက်တွေ့ deployment တွင် memory အပေါ် မှီခိုမှုနှင့် အရှိန်အပေါ် သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** သတ်မှတ် bit အလုံးအစု တစ်ခုမှ အခြား တစ်ခုသို့ ရွေ့ခြင်းသည် တူညီသည့် end-to-end memory သို့မဟုတ် အရှိန် အချိုးကို အာမမခံနိုင်ပါ၊ အကြောင်းမှာ metadata၊ kernel များ၊ cache များနှင့် hardware အထောက်အပံ့တို့သည်လည်း အရေးပါသည်။
- **ဆက်စပ် term များ:** QLoRA, Mixed Precision, Parameter
- **English (source):** Representing weights, activations, or caches with lower-precision formats to reduce memory, bandwidth, or compute cost. Methods differ in calibration, granularity, data type, and whether conversion happens before, during, or after training.

### Self-Attention

**မြန်မာ:** sequence တစ်ခုတည်းမှ ရရှိသည့် query၊ key၊ value ဖြင့် ပြုလုပ်သည့် attention (Self-Attention)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** query၊ key နှင့် value များကို တူညီသည့် sequence representation တစ်ခုတည်းမှ ရယူသည့် attention ဖြစ်သည်။ scale ပြုလုပ်ထားသည့် similarity score များကို normalize လုပ်ပြီး value များကို ပေါင်းစပ်ရာတွင် အသုံးပြုသည်၊ ထိုသို့ လုပ်ဆောင်ရာတွင် causal၊ padding၊ local သို့မဟုတ် အခြား mask များ၏ ကန့်သတ်ချက်အောက်တွင် ရှိသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် context အပေါ် မှီခိုသည့် token representation များကို တည်ဆောက်ပေးသော်လည်း ခွင့်ပြုထားသည့် attention pattern သည် ဖွဲ့စည်းပုံအပေါ် မှီခိုသည်။
- **မကြာခဏ ရောထွေးမှု:** token တိုင်းသည် အခြား token တိုင်းကို အမြဲတမ်း attend လုပ်နိုင်သည် မဟုတ်ပါ။ causal နှင့် sparse model များသည် ဆက်သွယ်မှုများကို ရည်ရွယ်ချက်ရှိရှိ ကန့်သတ်သည်။
- **ဆက်စပ် term များ:** Attention, Transformer, Context Window
- **Learn it:** [Self-Attention from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/07-transformers-deep-dive/02-self-attention-from-scratch/)
- **English (source):** Attention in which queries, keys, and values are derived from the same sequence representation. Scaled similarity scores are normalized and used to combine values, subject to causal, padding, local, or other masks. It builds context-sensitive token representations, but the permitted attention pattern depends on the architecture.

### Speculative Decoding

**မြန်မာ:** ကြိုတင် ခန့်မှန်းချက်များကို အသုံးပြု၍ လျင်မြန်စေသည့် decode နည်းလမ်း (Speculative Decoding)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ကုန်ကျစရိတ် ပိုနည်းသည့် draft ဖြစ်စဉ်တစ်ခုက token အများအပြားကို အဆိုပြုပြီး target model က ထို draft position များကို တစ်ပြိုင်နက် score ပေးသည့် inference နည်းလမ်း ဖြစ်သည်။ တိကျသည့် (exact) sampling မျိုးကွဲများတွင် လက်ခံခြင်း (acceptance) နှင့် ပြန်လည် ပြင်ဆင်ခြင်း (correction) စည်းမျဉ်းက target model ၏ output distribution ကို ထိန်းသိမ်းပေးသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** draft များ လက်ခံခံရသည့်အခါ target model ၏ အစဉ်လိုက် decoding အလုပ်ပမာဏကို လျှော့ချနိုင်ပြီး target model ၏ လေ့ကျင့်ပြီး weight များကို ပြောင်းလဲရန် မလိုအပ်ပါ။
- **မကြာခဏ ရောထွေးမှု:** speculative decoding သည် သာမန် model routing သို့မဟုတ် အတည်မပြုရသေးသည့် autocomplete မဟုတ်ပါ။ တိကျသည့် မျိုးကွဲများသည် လက်ခံခြင်းနှင့် ပြင်ဆင်ခြင်းဖြင့် target distribution ကို ထိန်းသိမ်းပြီး အနီးစပ်ဆုံး (approximate) မျိုးကွဲများသည် ထို အာမခံချက်ကို အရှိန်နှင့် လဲလှယ်နိုင်သည်။
- **လက်တွေ့:** လက်တွေ့ prompt များအပေါ် acceptance rate နှင့် end-to-end latency ကို တိုင်းတာရမည်၊ draft model ၏ အပိုအလွှာ (overhead) ကို ထည့်သွင်းစဉ်းစားရမည်၊ implementation သည် ရည်ရွယ်သည့် decoding distribution ကို ထိန်းသိမ်းကြောင်း စစ်ဆေးရမည်။
- **ဆက်စပ် term များ:** Autoregressive, KV Cache, Decoding Strategy, Tokens per Second (TPS)
- **English (source):** An inference method in which a cheaper draft process proposes several tokens and the target model scores those draft positions in parallel. In exact sampling variants, an acceptance and correction rule preserves the target model's output distribution. It can reduce serial target-model decoding work when drafts are accepted, without requiring a change to the target model's trained weights.

### Stop Sequence

**မြန်မာ:** generation ကို ရပ်တန့်စေသည့် စာသား အစဉ် (Stop Sequence)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** decoding စနစ် ကြုံတွေ့သည့်အခါ generation ကို ရပ်တန့်စေသည့် application မှ သတ်မှတ်ထားသည့် token သို့မဟုတ် စာသား pattern ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** stop sequence များသည် output protocol များနှင့် အပိုင်းအစ များစွာ ပါဝင်သည့် generation ကို ကန့်သတ်ပေးပြီး model က မိမိ ပြီးဆုံးပြီဟု အဓိပ္ပာယ်ဖြင့် ဆုံးဖြတ်သည့်အထိ စောင့်ရန် မလိုအပ်ပါ။
- **မကြာခဏ ရောထွေးမှု:** stop sequence သည် စက်ပိုင်းဆိုင်ရာ decoding အခြေအနေ တစ်ခု ဖြစ်သည်၊ အဖြေ ပြည့်စုံသည် သို့မဟုတ် agent ရည်မှန်းချက် ပြည့်မီသည်ဟု သက်သေပြခြင်း မဟုတ်ပါ။
- **လက်တွေ့:** မရောထွေးနိုင်သည့် delimiter များကို ရွေးချယ်ရမည်၊ tokenization နှင့် streaming တွင် တစ်စိတ်တစ်ပိုင်း ကိုက်ညီမှုများကို စမ်းသပ်ရမည်၊ output အရှည်နှင့် schema validation ကို ဆက်လက် ကျင့်သုံးရမည်။
- **ဆက်စပ် term များ:** Decoding Strategy, Structured Output, Token, Termination Condition
- **English (source):** An application-specified token or text pattern that causes generation to stop when the decoding system encounters it. Stop sequences bound output protocols and multi-part generation without waiting for the model to decide semantically that it is finished.

### Streaming

**မြန်မာ:** ရလဒ် မပြည့်စုံမီ အစိတ်အပိုင်း အလိုက် ပေးပို့ခြင်း (Streaming)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ပြီးစီးသည့် ရလဒ် အသင့်ဖြစ်မီ အဆင့်ဆင့် ဖြစ်ပေါ်သည့် response event များကို ပေးပို့ခြင်း ဖြစ်သည်။ API အပေါ် မှီခို၍ stream တွင် token စာသား၊ structured delta များ၊ tool-call argument များ၊ usage metadata သို့မဟုတ် status event များ ပါဝင်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် ခံစားရသည့် တုံ့ပြန်မှု လျင်မြန်မှုကို ကောင်းမွန်စေသည်၊ သို့သော် model ၏ အဖြေ အပြည့်အစုံ ထုတ်လုပ်ရန် အမှန်တကယ် အချိန်ကို လျှော့ချပေးသည် မဟုတ်ပါ။
- **မကြာခဏ ရောထွေးမှု:** network transport၊ event ပုံစံနှင့် chunk နယ်နိမိတ်များသည် provider အလိုက် ကွာခြားပြီး word သို့မဟုတ် token များနှင့် တိုက်ဆိုင်မည်ဟု အာမမခံနိုင်ပါ။
- **ဆက်စပ် term များ:** Time to First Token (TTFT), Autoregressive, Observability
- **Learn it:** [Production LLM Application](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/13-production-app/)
- **English (source):** Delivering incremental response events before the complete result is ready. A stream may contain token text, structured deltas, tool-call arguments, usage metadata, or status events depending on the API. It improves perceived responsiveness, but it does not reduce the model's actual time to produce a complete answer.

### Temperature

**မြန်မာ:** logits ကို ပြန်လည် အတိုင်းအတာ ချိန်ညှိသည့် decode parameter (Temperature)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** probability distribution တစ်ခု မဖြစ်ပေါ်မီ logits များကို ပြန်လည် အတိုင်းအတာ ချိန်ညှိသည့် decoding parameter ဖြစ်သည်။ အပြုကိန်း တန်ဖိုး မြင့်လျှင် distribution ကို ပြန့်ပြူးစေလေ့ ရှိပြီး အပြုကိန်း တန်ဖိုး နိမ့်လျှင် ပို၍ စူးရှစေသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** temperature သည် sampling အပြုအမူကို ပြောင်းလဲသည်၊ model ၏ အသိပညာ သို့မဟုတ် အချက်အလက် တိကျမှုကို မပြောင်းလဲပါ။
- **မကြာခဏ ရောထွေးမှု:** တန်ဖိုး သုည သတ်မှတ်ခြင်းကို greedy decoding အဖြစ် အကောင်အထည်ဖော်လေ့ ရှိသော်လည်း အတိအကျ အပြုအမူနှင့် အဆုံးအဖြတ်ဖြစ်မှု (determinism) သည် provider၊ sampler၊ seed အထောက်အပံ့နှင့် serving စနစ်အပေါ် မှီခိုသည်။
- **ဆက်စပ် term များ:** Softmax, Autoregressive, Token
- **English (source):** A decoding parameter that rescales logits before a probability distribution is formed. Higher positive values usually flatten the distribution; lower positive values sharpen it. Temperature changes sampling behavior, not the model's knowledge or factuality.

### Time to First Token (TTFT)

**မြန်မာ:** ပထမဆုံး output token ရရှိသည်အထိ ကြာချိန် (Time to First Token — TTFT)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** generation တောင်းဆိုမှု တင်သွင်းသည့် အချိန်မှ သတ်မှတ်ထားသည့် တိုင်းတာမှု နယ်နိမိတ်အောက်တွင် client က ပထမဆုံး output token သို့မဟုတ် content event ကို လက်ခံရရှိသည့် အချိန်အထိ ကုန်ဆုံးသည့် အချိန် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** TTFT သည် ခံစားရသည့် တုံ့ပြန်မှု လျင်မြန်မှုကို ပြင်းထန်စွာ သက်ရောက်ပြီး queueing၊ prompt processing၊ cache သို့မဟုတ် network ဆိုင်ရာ နှောင့်နှေးမှုများကို ဖော်ထုတ်ပေးနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** TTFT သည် tokens per second မဟုတ်ပါ။ တစ်ခုသည် စတင်သည့် latency ကို တိုင်းတာပြီး အခြားတစ်ခုသည် output စတင်ပြီးနောက် generation throughput ကို တိုင်းတာသည်။
- **လက်တွေ့:** model၊ prompt အရှည်၊ region နှင့် cache အခြေအနေ အလိုက် client-side TTFT ကို မှတ်တမ်းတင်ပြီး စုစုပေါင်း ပြီးစီးချိန်နှင့် ခွဲခြားရမည်။
- **ဆက်စပ် term များ:** Streaming, Prompt Cache, Observability, Token Budget
- **English (source):** The elapsed time from submitting a generation request until the client receives the first output token or content event under a defined measurement boundary. TTFT strongly affects perceived responsiveness and can reveal queueing, prompt processing, cache, or network delays.

### Top-k Sampling

**မြန်မာ:** အမြင့်ဆုံး score ရှိသည့် k လုံးမှ ရွေးချယ်သည့် decode နည်းလမ်း (Top-k Sampling)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** next-token distribution ကို အမြင့်ဆုံး score ရှိသည့် candidate k လုံးအထိ ကန့်သတ်ပြီး ၎င်းတို့၏ probability များကို ပြန်လည် normalize လုပ်ကာ ထို အစုမှ sampling လုပ်သည့် decoding နည်းလမ်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** sampling မှ probability နည်းသည့် အမြီးရှည် (long tail) ကို ဖယ်ရှားပေးပြီး သတ်မှတ်ထားသည့် အများဆုံး candidate အရေအတွက်ကို ထိန်းသိမ်းသည်။
- **မကြာခဏ ရောထွေးမှု:** top-k သည် သတ်မှတ်ထားသည့် candidate အရေအတွက်ကို အသုံးပြုပြီး top-p သည် candidate အရေအတွက် အဆင့်တိုင်း ပြောင်းလဲသည့် probability mass အဆင့်သတ်မှတ်ချက်ကို အသုံးပြုသည်။
- **လက်တွေ့:** k ကို temperature၊ top-p နှင့် stop setting များနှင့်အတူ အကဲဖြတ်ရမည်၊ ထုတ်လုပ်လိုက်သည့် ရလဒ်များနှင့်အတူ sampler configuration အပြည့်အစုံကို မှတ်တမ်းတင်ရမည်။
- **ဆက်စပ် term များ:** Nucleus Sampling (Top-p), Temperature, Decoding Strategy, Logits
- **English (source):** A decoding method that restricts the next-token distribution to the k highest-scoring candidates, renormalizes their probabilities, and samples from that set. It removes the long low-probability tail from sampling while keeping a fixed maximum candidate count.

### Transformer

**မြန်မာ:** attention အပေါ် အခြေခံသည့် နျူရယ်ကွန်ရက် ဖွဲ့စည်းပုံ (Transformer)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** attention၊ position အချက်အလက်၊ feed-forward အလွှာခွဲများ၊ residual connection များနှင့် normalization တို့ဖြင့် တည်ဆောက်ထားသည့် နျူရယ်ကွန်ရက် ဖွဲ့စည်းပုံ ဖြစ်သည်။ encoder၊ decoder နှင့် encoder-decoder မျိုးကွဲများသည် mask များနှင့် အချက်အလက် စီးဆင်းမှု လမ်းကြောင်း မတူညီကြပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** လေ့ကျင့်မှုတွင် sequence position အများအပြားကို တစ်ပြိုင်နက် လုပ်ဆောင်နိုင်ပြီး autoregressive generation သည် အဆင့်ဆင့် အစဉ်လိုက် output ထုတ်လုပ်နေဆဲ ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** self-attention ရှိခြင်းသည် transformer တိုင်းတွင် ကန့်သတ်ချက် မရှိ all-to-all attention ရှိသည်ဟု အဓိပ္ပာယ် မဆောင်ပါ။
- **ဆက်စပ် term များ:** Attention, Self-Attention, Encoder, Decoder
- **Learn it:** [Build a Full Transformer](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/07-transformers-deep-dive/05-full-transformer/)
- **English (source):** A neural-network architecture built from attention, position information, feed-forward sublayers, residual connections, and normalization. Encoder, decoder, and encoder-decoder variants use different masks and information flows. Training can process many sequence positions in parallel, while autoregressive generation still produces outputs step by step.

### VAE (Variational Autoencoder)

**မြန်မာ:** ဖြစ်နိုင်ခြေဆိုင်ရာ latent-variable autoencoder (VAE)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** reconstruction objective နှင့် ခန့်မှန်း posterior ကို ရွေးချယ်ထားသည့် prior နှင့် နီးကပ်စွာ ထားရှိသည့် regularization term တစ်ခုတို့ဖြင့် လေ့ကျင့်သည့် latent-variable model ဖြစ်သည်။ reparameterization estimator သည် ကျပန်း latent sampling မှတစ်ဆင့် gradient များ စီးဆင်းနိုင်စေသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ခန့်မှန်း posterior နှင့် prior ကို ရွေးချယ်ခြင်းသည် model ၏ latent space ဖွဲ့စည်းပုံကို သတ်မှတ်သောကြောင့် sampling လုပ်သည့် စနစ်များတွင် ဤရွေးချယ်မှုများ သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** VAE သည် latent distribution တိုင်းကို တစ်ခုတည်းသော Gaussian တစ်ခုသို့ အတင်းအကြပ် ရောက်ရှိစေသည် မဟုတ်ပါ၊ prior နှင့် ခန့်မှန်း posterior အတိအကျကို model ရေးဆွဲသည့် ရွေးချယ်မှုများ အဖြစ် သတ်မှတ်သည်။
- **ဆက်စပ် term များ:** Latent Space, Encoder, Decoder, Diffusion Model
- **English (source):** A latent-variable model trained with a reconstruction objective and a regularization term that keeps an approximate posterior close to a chosen prior. The reparameterization estimator allows gradients through stochastic latent sampling.

## Self-check

၁။ Attention weight များကို model ၏ ကျိုးကြောင်းဆင်ခြင်မှုကို သစ္စာရှိစွာ ရှင်းလင်းပြသည့် အဖြေအဖြစ် တိုက်ရိုက် အသုံးပြုနိုင်ပါသလော။

၂။ Autoregressive နည်းလမ်းတွင် ခန့်မှန်းသည့် အလုံးအစုသည် word ဖြစ်ပါသလော။

၃။ KV cache နှင့် prompt caching သည် မည်သို့ ကွာခြားပါသလော။

၄။ Temperature တန်ဖိုးကို မြှင့်ခြင်းသည် model ၏ အသိပညာ သို့မဟုတ် အချက်အလက် တိကျမှုကို တိုးစေပါသလော။

၅။ TTFT နှင့် tokens per second သည် မည်သို့ ကွာခြားပါသလော။

<details>
<summary>အဖြေများ</summary>

၁။ မရပါ။ Attention weight များသည် computation coefficient များသာ ဖြစ်သည်၊ model နားလည်ခဲ့သည့် အကြောင်းအရာကို ရှင်းလင်းပြသည် သို့မဟုတ် သက်သေပြသည် မဟုတ်ပါ။ Attention သည် position များအကြား အချက်အလက် စီးဆင်းမှုကို လမ်းကြောင်းချပေးသည် သာ ဖြစ်သည်။

၂။ မဟုတ်ပါ။ အလုံးအစုသည် token ဖြစ်သည်၊ word ဖြစ်ရန် မလိုအပ်ပါ။ ထို့အပြင် အမြင့်ဆုံး probability ရှိသည့် token ကို အမြဲ ရွေးချယ်သည့် နည်းလမ်းသာ မဟုတ်ဘဲ အခြား decoding နည်းလမ်းများကိုလည်း အသုံးပြုနိုင်သည်။

၃။ KV cache သည် sequence တစ်ခုအတွက် runtime attention state ဖြစ်ပြီး ရှေးဦး position များ၏ key နှင့် value tensor များကို ထပ်မံ တွက်ချက်ခြင်း မပြုရန် သိမ်းဆည်းသည်။ Prefix caching သည် အသုံးပြုနိုင်သည့် KV state ကို request များအကြား ပြန်လည် အသုံးပြုခြင်း ဖြစ်ပြီး prompt caching သည် ပိုမို ကျယ်ပြန့်သည့် provider သို့မဟုတ် application အဆင့် ပြန်လည် အသုံးပြုမှု သဘောတူညီချက် ဖြစ်သည်။

၄။ မတိုးစေပါ။ Temperature သည် probability distribution မဖြစ်ပေါ်မီ logits များကို ပြန်လည် အတိုင်းအတာ ချိန်ညှိသည့် decoding parameter ဖြစ်သည်၊ sampling အပြုအမူကို ပြောင်းလဲသည်၊ model ၏ အသိပညာ သို့မဟုတ် အချက်အလက် တိကျမှုကို မပြောင်းလဲပါ။

၅။ TTFT သည် generation တောင်းဆိုမှု တင်သွင်းသည့် အချိန်မှ ပထမဆုံး output token သို့မဟုတ် content event ရရှိသည့် အချိန်အထိ စတင်သည့် latency ကို တိုင်းတာသည်။ tokens per second သည် output စတင်ပြီးနောက် generation throughput ကို တိုင်းတာသည်။

</details>

## References

- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed, from `rohitg00/ai-engineering-from-scratch`။
- Lessons: [Self-Attention from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/07-transformers-deep-dive/02-self-attention-from-scratch/)၊ [Build a Full Transformer](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/07-transformers-deep-dive/05-full-transformer/)၊ [Mixture of Experts](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/07-transformers-deep-dive/11-mixture-of-experts/)၊ [KV Cache and Flash Attention](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/07-transformers-deep-dive/12-kv-cache-flash-attention/)၊ [Production LLM Application](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/13-production-app/)။
- Papers and documentation: [Attention Is All You Need](https://arxiv.org/abs/1706.03762)၊ [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)၊ [Fast Inference from Transformers via Speculative Decoding](https://proceedings.mlr.press/v202/leviathan23a.html)၊ [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)၊ [Transformers text-generation documentation](https://huggingface.co/docs/transformers/main/en/main_classes/text_generation)။
