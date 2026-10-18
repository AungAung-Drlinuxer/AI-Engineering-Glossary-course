# 12 — Multimodal systems

ဤနယ်ပယ်သည် စနစ် တစ်ခုတည်းအတွင်း modality တစ်ခုထက်ပိုသည့် အချက်အလက်များ — text၊ ရုပ်ပုံ၊ အသံ၊ video၊ depth၊ sensor တိုင်းတာချက်များ — ကို စီမံသည့် အင်ဂျင်နီယာ အခြေခံသဘောတရားများကို ဖုံးလွှမ်းသည်။ **Modality** သည် ထို အလွှာ၏ အခြေခံ အယူအဆ ဖြစ်ပြီး၊ ကျန် term များသည် အချက်အလက်တစ်ခုစီကို model နားလည်နိုင်သည့် ပုံစံသို့ ပြောင်းခြင်း၊ ၎င်းတို့အကြား ဆက်စပ်မှု တည်ထောင်ခြင်း၊ ပေါင်းစည်းခြင်းနှင့် အဖြေ ထုတ်ခြင်း အဆင့်များတွင် ရှိသည်။ ဤ term များကို မသိဘဲ ရုပ်ပုံနှင့် စာသား၊ အသံနှင့် စာသား ပေါင်းစပ်သည့် စနစ် တစ်ခုကို တည်ဆောက်ပါက အဆင့်တစ်ခုစီရှိ representation နယ်နိမိတ်တွင် ချို့ယွင်းမှုများ ဖုံးကွယ်နေနိုင်သည်။

Term ၁၅ ခုကို အဓိက မိသားစု သုံးခုအဖြစ် စုစည်းနိုင်သည်။ ပထမ — representation မိသားစု: **Modality**၊ ၎င်းမှ ဆင်းသက်သည့် **Audio Token** နှင့် **Image Token**၊ ထို token များ ဖြစ်ပေါ်ရာ အဆင့်ဖြစ်သည့် **Patch Embedding** နှင့် **Vision Transformer (ViT)**၊ ထို့နောက် modality အားလုံးကို နှိုင်းယှဉ်နိုင်သည့် **Shared Embedding Space** တို့ ဖြစ်သည်။ ဒုတိယ — ချိတ်ဆက်မှုနှင့် ပေါင်းစည်းမှု မိသားစု: **Modality Alignment**၊ **Cross-Attention**၊ **Multimodal Fusion** နှင့် ၎င်း၏ နေရာ နှစ်မျိုးဖြစ်သည့် **Early Fusion** နှင့် **Late Fusion** တို့ ဖြစ်သည်။ တတိယ — စနစ်နှင့် task မိသားစု: **Multimodal Model**၊ **Vision-Language Model (VLM)**၊ **Automatic Speech Recognition (ASR)** နှင့် အထောက်အထား တည်နေရာ ချိတ်ဆက်သည့် **Visual Grounding** တို့ ဖြစ်သည်။

Entry တစ်ခုကို ဖတ်သည့်အခါ **ဆိုလိုသည့် အဓိပ္ပာယ်** ဖြင့် စတင်ပါ — ၎င်းသည် source ၏ အင်ဂျင်နီယာ အဓိပ္ပာယ် ဖြစ်သည်။ ထို့နောက် **အရေးပါသည့် အကြောင်းရင်း** တွင် မည်သည့် စနစ်အပေါ် မည်သို့ သက်ရောက်သည်ကို ကြည့်ပါ။ **မကြာခဏ ရောထွေးမှု** နှင့် **လက်တွေ့** စာကြောင်းများသည် source တွင် ပါသည့်အခါသာ ပေါ်လာသည်။ Technical term များ (vision encoder၊ modality၊ cross-attention၊ image token၊ OCR၊ video sampling၊ speech၊ embedding၊ fusion) ကို မြန်မာ စာကြောင်းအတွင်း အင်္ဂလိပ်အတိုင်း ထားရှိထားသည်။

### Audio Token

**မြန်မာ:** အသံ token (audio token)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** audio codec သို့မဟုတ် tokenizer တစ်ခုက audio signal ၏ အပိုင်းအစ တိုတစ်ခု သို့မဟုတ် feature တစ်ခုအတွက် — တစ်ခါတစ်ရံ codebook အတော်များများအပေါ် ဖြန့်၍ — ထုတ်လုပ်ပေးသည့် သီးခြားဖြစ်သည့် (discrete) အမှတ်အသား ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** discrete audio representation များသည် sequence model များအား token အခြေခံ ဗိသုကာများဖြင့် အသံကို စီမံခြင်း၊ ခန့်မှန်းခြင်း၊ သိမ်းဆည်းခြင်း သို့မဟုတ် ထုတ်လုပ်ခြင်း ပြုလုပ်နိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** audio token သည် သတ်မှတ်ထားသည့် ကြာချိန်၊ phoneme သို့မဟုတ် စကားလုံး တစ်လုံး မဟုတ်ပါ။ ၎င်း၏ အဓိပ္ပာယ်နှင့် အချိန် အတိုင်းအတာသည် tokenizer နှင့် codebook design အပေါ် မူတည်သည်။
- **လက်တွေ့:** codec ကို model နှင့်အတူ version ထိန်းရမည်၊ sample-rate နှင့် codebook metadata ကို ထိန်းသိမ်းရမည်၊ ပြန်လည် တည်ဆောက်မှု အရည်အသွေး (reconstruction quality) ကို တိုင်းတာရမည်၊ semantic audio token များနှင့် waveform-compression token များကို ခွဲခြားရမည်။
- **ဆက်စပ် term များ:** Token, Embedding, Automatic Speech Recognition (ASR), Multimodal Model
- **Learn it:** [Neural Audio Codecs](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/06-speech-and-audio/13-neural-audio-codecs/)
- **English (source):** A discrete identifier produced by an audio codec or tokenizer for a short segment or feature of an audio signal, sometimes across several codebooks. Discrete audio representations let sequence models process, predict, store, or generate sound using token-oriented architectures.

### Automatic Speech Recognition (ASR)

**မြန်မာ:** အလိုအလျောက် စကားပြော အသံ အသိအမှတ်ပြုခြင်း (ASR)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** speech signal တစ်ခုကို transcription တစ်ခုအဖြစ် ပြောင်းလဲပေးသည့် task နှင့် စနစ် pipeline ဖြစ်ပြီး၊ များသောအားဖြင့် token သို့မဟုတ် segment အချိန်မှတ် (timing) နှင့် confidence အချက်အလက်များ ရွေးချယ်၍ ပါဝင်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** speech interface များသည် language modeling တစ်ခုတည်းအပေါ် မှီခိုသည် မဟုတ်ပါ။ acoustic ကွဲပြားမှု (variation)၊ segmentation၊ decoding၊ vocabulary နှင့် domain အခြေအနေများသည် နောက်ဆုံး transcript အပေါ် သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** ASR သည် ပြောခဲ့သည့် အကြောင်းအရာကို transcript ရေးသည်။ မည်သူ ပြောသည်ကို ဆုံးဖြတ်ရန် diarization သို့မဟုတ် speaker recognition လိုအပ်ပြီး၊ translation နှင့် intent understanding တို့သည် သီးခြား task များ ဖြစ်သည်။
- **လက်တွေ့:** ဘာသာစကား၊ ပြောသူ၊ noise နှင့် domain အလိုက် word သို့မဟုတ် character error များကို တိုင်းတာရမည်၊ downstream grounding အတွက် လိုအပ်သည့်အခါ timestamp များကို ထိန်းသိမ်းရမည်၊ production တွင် အသုံးပြုသည့် audio preprocessing အတိအကျကို စမ်းသပ်ရမည်။
- **ဆက်စပ် term များ:** Audio Token, Encoder, Tokenization, Multimodal Model
- **Learn it:** [Speech Recognition and ASR](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/06-speech-and-audio/04-speech-recognition-asr/)
- **English (source):** The task and system pipeline that maps a speech signal to a transcription, often with optional token or segment timing and confidence information. Speech interfaces depend on more than language modeling. Acoustic variation, segmentation, decoding, vocabulary, and domain conditions all affect the final transcript.

### Cross-Attention

**မြန်မာ:** ငြိချိတ် attention (cross-attention)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** query representation သည် sequence သို့မဟုတ် representation တစ်ခုမှ လာပြီး key နှင့် value များသည် အခြား တစ်ခုမှ လာသည့် attention ပုံစံ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် stream တစ်ခုအား အခြား stream တစ်ခုမှ အချက်အလက် ရယူနိုင်သည့် သင်ယူနိုင်သည့် နည်းလမ်းကို ပေးသည် — ဥပမာ language token များသည် visual feature များသို့ attend လုပ်ခြင်း ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** cross-attention သည် ပင်ကိုအားဖြင့် multimodal ဖြစ်သည် မဟုတ်ပါ။ text sequence နှစ်ခု သို့မဟုတ် အခြား representation များကိုလည်း ချိတ်ဆက်နိုင်သည်။ self-attention ကမူ query၊ key နှင့် value အားလုံးကို တူညီသည့် sequence representation မှ ဆင်းသက်စေသည်။
- **လက်တွေ့:** query၊ key နှင့် value များကို မည်သည့် stream မှ ပေးသည်ကို ဖော်ပြရမည်၊ ပျောက်ဆုံးနေသည့် သို့မဟုတ် မမှန်ကန်သည့် နေရာများအတွက် mask များ ထည့်သွင်းရမည်၊ modality တစ်ခုကို ဖယ်ရှားလိုက်သည့်အခါ (ablation) model သည် အလုပ်လုပ်နေဆဲ ဖြစ်မဖြစ် စစ်ဆေးရမည်။
- **ဆက်စပ် term များ:** Attention, Self-Attention, Vision-Language Model (VLM), Multimodal Fusion
- **English (source):** Attention in which the query representation comes from one sequence or representation while keys and values come from another. It gives one stream a learnable way to retrieve information from another, such as language tokens attending to visual features.

### Early Fusion

**မြန်မာ:** အစောပိုင်း ပေါင်းစည်းခြင်း (early fusion)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** task သီးသန့် modeling အများစု မဖြစ်ပေါ်မီ modality အတော်များများမှ raw သို့မဟုတ် low-level representation များကို ပေါင်းစည်းခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အစောပိုင်း အပြန်အလှန် သက်ရောက်မှုသည် သေးငယ်သည့် cross-modal ဆက်စပ်မှုများကို ဖော်ထုတ်နိုင်သည်။ သို့သော် ကိုက်ညီသည့် representation များ လိုအပ်ပြီး၊ alignment နှင့် ပျောက်ဆုံးနေသည့် input များကို ဂရုတစိုက် စီမံရမည်။
- **မကြာခဏ ရောထွေးမှု:** early fusion သည် ဗိသုကာအတွင်း stream များကို မည်သည့်နေရာတွင် ပေါင်းစည်းသည်ကို ဖော်ပြသည်။ ၎င်းတို့အကြား အသုံးဝင်သည့် alignment ကို model သင်ယူသည်ဟု အာမခံသည် မဟုတ်ပါ။
- **လက်တွေ့:** modality တစ်ခုစီကို ကြေညာထားသည့် token သို့မဟုတ် feature representation အဖြစ် ပြောင်းရမည်၊ ရင်းမြစ် (source) နှင့် နေရာ (position) အမှတ်အသားများကို ထိန်းသိမ်းရမည်၊ မျှဝေသည့် backbone မတိုင်မီ ပေါင်းစည်းရမည်၊ single-modality နှင့် late-fusion baseline များနှင့် နှိုင်းယှဉ်ရမည်။
- **ဆက်စပ် term များ:** Late Fusion, Multimodal Fusion, Modality Alignment, Token
- **Learn it:** [Chameleon Early-Fusion Tokens](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/12-multimodal-ai/11-chameleon-early-fusion-tokens/)
- **English (source):** Combining raw or low-level representations from several modalities before most task-specific modeling occurs. Early interaction can expose fine-grained cross-modal relationships, but it also requires compatible representations and careful handling of alignment and missing inputs.

### Image Token

**မြန်မာ:** ရုပ်ပုံ token (image token)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** model သီးသန့် visual ယူနစ်တစ်ခုကို vector သို့မဟုတ် discrete code အဖြစ် ဖော်ပြထားခြင်း ဖြစ်ပြီး၊ များသောအားဖြင့် image patch၊ region သို့မဟုတ် သင်ယူထားသည့် visual-codebook entry တစ်ခုမှ ဆင်းသက်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** visual input ကို sequence အဖြစ် ပြောင်းလဲခြင်းသည် transformer ပုံစံ အစိတ်အပိုင်းများအား ရုပ်ပုံများကို text သို့မဟုတ် အခြား tokenize လုပ်ထားသည့် modality များနှင့်အတူ စီမံနိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** image token သည် pixel တစ်ခု၊ object တစ်ခု သို့မဟုတ် သတ်မှတ်ထားသည့် ရုပ်ပိုင်း ဧရိယာ တစ်ခု အမြဲ ဖြစ်ရမည် မဟုတ်ပါ။ ၎င်း၏ အတိုင်းအတာသည် visual encoder သို့မဟုတ် tokenizer ကို လိုက်နာသည်။
- **လက်တွေ့:** token များသည် continuous patch များ သို့မဟုတ် discrete code များ ဖြစ်သည်ကို မှတ်တမ်းတင်ရမည်၊ spatial position ကို ထိန်းသိမ်းရမည်၊ resolution နှင့် aspect-ratio အပြောင်းအလဲများကို စမ်းသပ်ရမည်၊ model ၏ input budget တွင် visual token အရေအတွက်ကို ရေတွက်ရမည်။
- **ဆက်စပ် term များ:** Patch Embedding, Token, VAE (Variational Autoencoder), Vision Transformer (ViT)
- **Learn it:** [Vision-Language Models](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/04-computer-vision/25-vision-language-models/)
- **English (source):** A model-specific visual unit represented as a vector or discrete code, commonly derived from an image patch, region, or learned visual-codebook entry. Turning visual input into a sequence lets transformer-style components process images together with text or other tokenized modalities.

### Late Fusion

**မြန်မာ:** နောက်ကျ ပေါင်းစည်းခြင်း (late fusion)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** modality များကို သီးခြား encoder သို့မဟုတ် predictor များမှတစ်ဆင့် စီမံပြီး၊ ၎င်းတို့၏ အဆင့်မြင့် representation၊ score သို့မဟုတ် ဆုံးဖြတ်ချက်များကို task output အနီးတွင် ပေါင်းစည်းခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** သီးခြား branch များသည် modality သီးသန့် ဗိသုကာများကို အသုံးပြုနိုင်ပြီး ပျောက်ဆုံးနေသည့် input များကို ခံနိုင်သည်။ သို့သော် အစောပိုင်း fusion တွင် ရနိုင်သည့် သေးငယ်သည့် အပြန်အလှန် သက်ရောက်မှုများကို လွတ်သွားနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** late fusion သည် ပေါင်းစည်းသည့် နေရာကို ဖော်ပြသည်။ ရိုးရှင်းစွာ ပျှမ်းမျှခြင်း (averaging) ဟု မဆိုလိုသလို၊ modality များ တူညီစွာ အထောက်အကူ ပြုသည်ဟုလည်း အာမခံသည် မဟုတ်ပါ။
- **လက်တွေ့:** branch တစ်ခုစီကို calibrate လုပ်ရမည်၊ ပျောက်ဆုံးနေသည့် modality များသည် ပေါင်းစည်းမှု (merge) ကို မည်သို့ သက်ရောက်သည်ကို သတ်မှတ်ရမည်၊ score-level နှင့် feature-level ပေါင်းစည်းမှုများကို နှိုင်းယှဉ်ရမည်၊ branch တစ်ခုစီကို တစ်ခုတည်း ablation အဖြစ် တိုင်းတာရမည်။
- **ဆက်စပ် term များ:** Early Fusion, Multimodal Fusion, Modality, Evaluation (Eval)
- **Learn it:** [Cross-Attention Fusion](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/19-capstone-projects/61-cross-attention-fusion/)
- **English (source):** Processing modalities through separate encoders or predictors and combining their high-level representations, scores, or decisions near the task output. Separate branches can use modality-specific architectures and tolerate missing inputs, though they may miss fine-grained interactions available to earlier fusion.

### Modality

**မြန်မာ:** modality (အချက်အလက် ပုံစံ)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ကိုယ်ပိုင် တည်ဆောက်ပုံနှင့် ရယူသည့် လုပ်ငန်းစဉ် ရှိသည့် အချက်အလက် ပုံစံတစ်ခု — ဥပမာ text၊ image၊ audio၊ video၊ depth သို့မဟုတ် sensor တိုင်းတာချက်များ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** modality မတူညီသည့်အရာများတွင် sampling rate၊ noise၊ spatial သို့မဟုတ် temporal တည်ဆောက်ပုံနှင့် ပျောက်ဆုံးနေသည့် အချက်အလက် အပြုအမူ မတူညီကြသည်။ ထို့ကြောင့် preprocessing ယူဆချက် တစ်ခုတည်းသည် အားလုံးအတွက် သင့်လျော်လိမ့်မည်ဟု မဆိုနိုင်ပါ။
- **မကြာခဏ ရောထွေးမှု:** modality သည် file extension သို့မဟုတ် feature column တစ်ခု သက်သက် မဟုတ်ပါ။ encoding အတော်များများသည် modality တစ်ခုတည်းကို ဖော်ပြနိုင်ပြီး၊ sample တစ်ခုတွင် modality အတော်များများ ပါဝင်နိုင်သည်။
- **လက်တွေ့:** alignment သို့မဟုတ် fusion ကို မတည်ဆောက်မီ modality တစ်ခုစီ၏ ရင်းမြစ်၊ ယူနစ်၊ resolution၊ အချိန်၊ preprocessing နှင့် ပျောက်ဆုံးတန်ဖိုး မူဝါဒ (missing-value policy) တို့ကို မှတ်တမ်းတင်ရမည်။
- **ဆက်စပ် term များ:** Multimodal Model, Token, Tensor, Embedding
- **Learn it:** [MIO Any-to-Any Streaming](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/12-multimodal-ai/16-mio-any-to-any-streaming/)
- **English (source):** A form of information with its own structure and acquisition process, such as text, image, audio, video, depth, or sensor measurements. Different modalities have different sampling rates, noise, spatial or temporal structure, and missing-data behavior, so one preprocessing assumption rarely fits all of them.

### Modality Alignment

**မြန်မာ:** modality များ ကိုက်ညီစေခြင်း (modality alignment)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အဓိပ္ပာယ် သို့မဟုတ် အချိန်အားဖြင့် ဆက်စပ်နေသည့် အရာများကို တွဲဖက် (match) နိုင်ရန် modality မတူညီသည့်အရာများမှ representation များအကြား ဆက်စပ်မှုများကို သင်ယူခြင်း သို့မဟုတ် တည်ထောင်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** စနစ်တစ်ခုသည် တူညီသည့် ဖြစ်ရပ်၊ အရာဝတ္ထု သို့မဟုတ် အယူအဆကို ဖွဲ့စည်းပုံ မတူညီသည့် input များအကြား ချိတ်ဆက်နိုင်ခြင်း မရှိပါက fusion နှင့် cross-modal retrieval များ မအောင်မြင်ပါ။
- **မကြာခဏ ရောထွေးမှု:** alignment သည် representation များကို နှိုင်းယှဉ်နိုင်စေသည် သို့မဟုတ် ကိုက်ညီစေသည်။ ၎င်းတို့ တူညီလာရမည်ဟု မလိုအပ်သလို၊ modality သီးသန့် အချက်အလက်များကို ဖျောက်ဖျက်ရမည်လည်း မဟုတ်ပါ။
- **လက်တွေ့:** positive နှင့် negative pair များကို သတ်မှတ်ရမည်၊ အချိန် သို့မဟုတ် နေရာ metadata ကို ထိန်းသိမ်းရမည်၊ မကိုက်ညီသည့် နမူနာများကို တိုင်းတာရမည်၊ နောက်ဆက်တွဲ task တိကျမှုနှင့် သီးခြားစီ alignment ကို တိုင်းတာရမည်။
- **ဆက်စပ် term များ:** Shared Embedding Space, Contrastive Learning, Grounding, Multimodal Fusion
- **Learn it:** [Projection Layer Modality Alignment](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/19-capstone-projects/60-projection-layer-modality-align/)
- **English (source):** Learning or establishing correspondences between representations from different modalities so semantically or temporally related items can be matched. Fusion and cross-modal retrieval fail when the system cannot connect the same event, object, or concept across differently structured inputs.

### Multimodal Fusion

**မြန်မာ:** multimodal ပေါင်းစည်းခြင်း (multimodal fusion)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** modality တစ်ခုထက်ပိုသည့်အရာမှ အထောက်အထား သို့မဟုတ် သင်ယူထားသည့် representation များကို ပေါင်းစည်း၍ ပူးတွဲ representation၊ ခန့်မှန်းချက် သို့မဟုတ် ထုတ်လုပ်သည့် output တစ်ခု ဖန်တီးခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** modality များသည် ဖြည့်စွက်သည့် အထောက်အထားများ ပေးနိုင်သည်။ သို့သော် နက်နဲမှုမရှိသည့် ပေါင်းစည်းမှုသည် noise၊ အချိန်မှားယွင်းမှု သို့မဟုတ် လွှမ်းမိုးနေသည့် stream တစ်ခုကို ချဲ့ထွင်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** fusion သည် ပေါင်းစည်းသည့် လုပ်ဆောင်ချက် ဖြစ်သည်။ alignment သည် ဆက်စပ်မှုကို တည်ထောင်သည်။ modality နှစ်ခုကို request တစ်ခုတည်းတွင် ထည့်ထားခြင်းသည် ထို နှစ်ခုလုံး အောင်မြင်စွာ ဖြစ်ပေါ်သည်ဟု မသက်သေပြပါ။
- **လက်တွေ့:** single-modality baseline များ တည်ဆောက်ရမည်၊ fusion ပြုလုပ်သည့် နေရာနှင့် mask များကို သတ်မှတ်ရမည်၊ ပျောက်ဆုံးနေသည့် နှင့် ဆန့်ကျင်နေသည့် input များကို စမ်းသပ်ရမည်၊ တိုင်းတာသည့် အပိုင်းတစ်ခုစီတွင် မည်သည့် modality များက မောင်းနှင်သည်ကို ဖော်ပြရမည်။
- **ဆက်စပ် term များ:** Early Fusion, Late Fusion, Cross-Attention, Modality Alignment
- **Learn it:** [Cross-Attention Fusion](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/19-capstone-projects/61-cross-attention-fusion/)
- **English (source):** Combining evidence or learned representations from more than one modality to produce a joint representation, prediction, or generated output. Modalities can supply complementary evidence, but naïve combination can amplify noise, timing errors, or one dominant stream.

### Multimodal Model

**မြန်မာ:** modality များစွာ စီမံသည့် model (multimodal model)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** representation၊ alignment၊ fusion၊ translation သို့မဟုတ် ညှိနှိုင်း ခန့်မှန်းချက် (coordinated prediction) များမှတစ်ဆင့် modality တစ်ခုထက်ပိုသည့်အရာမှ သင်ယူခြင်း၊ ဆက်စပ်ခြင်း သို့မဟုတ် ထုတ်လုပ်ခြင်း ပြုလုပ်သည့် model ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** multimodal စွမ်းရည်သည် input အမျိုးအစား အတော်များများကို လက်ခံခြင်းအပေါ် တည်သည်မဟုတ်ဘဲ modality များ မည်သို့ အပြန်အလှန် သက်ရောက်သည်အပေါ် မူတည်ပြီး၊ ချို့ယွင်းမှုများသည် representation နယ်နိမိတ် တစ်ခုစီတွင် ဖြစ်ပေါ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** image နှင့် text model သီးခြားရှိသည့် pipeline သည် စနစ်အဆင့်တွင် multimodal ဖြစ်သည်။ သို့သော် ၎င်းသည် ပေါင်းတွဲ သင်တန်းပေးထားသည့် multimodal model တစ်ခု ဖြစ်ရမည်ဟု မဆိုလိုပါ။
- **လက်တွေ့:** ထောက်ပံ့သည့် input နှင့် output ပေါင်းစပ်မှုများကို မှတ်တမ်းတင်ရမည်၊ modality တစ်ခုစီကို တစ်ခုတည်းနှင့် အတူတကွ တိုင်းတာရမည်၊ ပျောက်ဆုံးနေသည့် သို့မဟုတ် ဆန့်ကျင်နေသည့် input များကို စမ်းသပ်ရမည်၊ preprocessing version များကို model နှင့်အတူ ခြေရာခံရမည်။
- **ဆက်စပ် term များ:** Modality, Vision-Language Model (VLM), Multimodal Fusion, Transformer
- **Learn it:** [MIO Any-to-Any Streaming](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/12-multimodal-ai/16-mio-any-to-any-streaming/)
- **English (source):** A model that learns from, relates, or generates more than one modality through representation, alignment, fusion, translation, or coordinated prediction. Multimodal capability depends on how modalities interact, not simply on accepting several input types, and failures can occur at each representation boundary.

### Patch Embedding

**မြန်မာ:** patch embedding (ရုပ်ပုံ patch ကို vector အဖြစ် ပြောင်းလဲခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** image patch တစ်ခုကို transformer input sequence ၏ အစိတ်အပိုင်း တစ်ခုအဖြစ် အသုံးပြုသည့် ပုံသေ အကျယ် (fixed-width) vector အဖြစ် ပြောင်းလဲပေးသည့် သင်ယူထားသည့် projection ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် spatial image grid နှင့် sequence model အကြား ချိတ်ဆက်မှု (interface) ကို ဖန်တီးပေးပြီး၊ patch အရွယ်အစားသည် token အရေအတွက်နှင့် ထိန်းသိမ်းထားသည့် local အသေးစိတ်ကို ထိန်းချုပ်သည်။
- **မကြာခဏ ရောထွေးမှု:** patch embedding သည် patch တစ်ခု၏ vector representation ဖြစ်ပြီး၊ semantic object detector မဟုတ်သလို၊ patch နယ်နိမိတ်များသည် visual အရာဝတ္ထုများနှင့် ကိုက်ညီမည်ဟု အာမခံသည် လည်း မဟုတ်ပါ။
- **လက်တွေ့:** patch နှင့် image အရွယ်အစားများကို မှတ်တမ်းတင်ရမည်၊ padding သို့မဟုတ် resizing ကို ရှင်းလင်းစွာ စီမံရမည်၊ position အချက်အလက် ထည့်ရမည်၊ resolution အပြောင်းအလဲများသည် တိကျမှုနှင့် token ကုန်ကျစရိတ် နှစ်ခုလုံးကို မည်သို့ သက်ရောက်သည်ကို တိုင်းတာရမည်။
- **ဆက်စပ် term များ:** Vision Transformer (ViT), Image Token, Embedding, Token
- **Learn it:** [Vision Transformer Patch Tokens](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/12-multimodal-ai/01-vision-transformer-patch-tokens/)
- **English (source):** A learned projection that converts an image patch into a fixed-width vector used as one element of a transformer input sequence. It creates the interface between a spatial image grid and a sequence model, with patch size controlling token count and retained local detail.

### Shared Embedding Space

**မြန်မာ:** မျှဝေသည့် embedding space (shared embedding space)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** modality မတူညီသည့်အရာများမှ representation များကို တူညီသည့် similarity function ဖြင့် နှိုင်းယှဉ်နိုင်သည့် ဘုံ vector space တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် အရာနှစ်ခုလုံး raw representation ကို မျှဝေရန် မလိုအပ်ဘဲ cross-modal retrieval နှင့် matching — ဥပမာ text မှ image ရှာဖွေခြင်း — ကို ဖြစ်နိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** vector dimension မျှဝေခြင်းသည် မျှဝေသည့် semantic space ကို ဖန်တီးသည်မဟုတ်ပါ။ cross-modal နှိုင်းယှဉ်နိုင်မှုကို သင်တန်း ရည်မှန်းချက် (training objective) နှင့် data က တည်ထောင်ရမည်။
- **လက်တွေ့:** paired နှင့် unpaired negative များကို တမင်တကာ သင်တန်းပေးရမည်၊ objective လိုအပ်သည့်အခါ vector များကို normalize လုပ်ရမည်၊ retrieval လမ်းကြောင်း နှစ်ခုလုံးကို တိုင်းတာရမည်၊ subgroup နှင့် ဘာသာစကား စွမ်းဆောင်ရည်ကို စစ်ဆေးရမည်။
- **ဆက်စပ် term များ:** Embedding, Cosine Similarity, Modality Alignment, Semantic Search
- **Learn it:** [CLIP Contrastive Pretraining](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/12-multimodal-ai/02-clip-contrastive-pretraining/)
- **English (source):** A common vector space in which representations from different modalities can be compared with the same similarity function. It enables cross-modal retrieval and matching, such as finding images from text, without requiring both items to share a raw representation.

### Vision-Language Model (VLM)

**မြန်မာ:** ရုပ်ပုံ–ဘာသာစကား model (VLM)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ရုပ်ပုံ နှင့် ဘာသာစကား representation များအကြား ဆက်စပ်မှုများကို သင်ယူသည့် သို့မဟုတ် ပူးတွဲ စီမံသည့် model ဖြစ်ပြီး၊ retrieval၊ ဖော်ပြချက် ရေးသားခြင်း၊ မေးခွန်း ဖြေဆိုခြင်း သို့မဟုတ် grounding ဖြင့် ထုတ်လုပ်ခြင်း ကဲ့သို့သော task များအတွက် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** VLM စွမ်းဆောင်ရည်သည် ယေဘုယျ စွမ်းရည် အမည်တစ်ခုအပေါ် မဟုတ်ဘဲ၊ visual encoder၊ language အစိတ်အပိုင်း၊ ချိတ်ဆက်သည့် ယန္တရား၊ သင်တန်း data နှင့် resolution မူဝါဒ တို့အပေါ် မူတည်သည်။
- **မကြာခဏ ရောထွေးမှု:** ရုပ်ပုံကို လက်ခံခြင်းသည် model က ၎င်းကို မှန်ကန်စွာ အသုံးပြုသည်ဟု မသက်သေပြပါ။ ထို့အပြင် VLM တစ်ခုသည် ရုပ်ပုံ ထုတ်လုပ်နိုင်စွမ်း အမြဲ ရှိသည် မဟုတ်ပါ။
- **လက်တွေ့:** text-only နှင့် vision-only control များကို တိုင်းတာရမည်၊ image resolution နှင့် layout ကို ပြောင်းလဲရမည်၊ ဖြစ်နိုင်သည့်အခါ အထောက်အထား တည်နေရာ ဖော်ထုတ်မှု (evidence localization) ကို တောင်းခံရမည်၊ visual ကျွမ်းကျင်မှုနှင့် ဘာသာစကား အလိုက် ချို့ယွင်းမှုများကို ဖော်ပြရမည်။
- **ဆက်စပ် term များ:** Multimodal Model, Vision Transformer (ViT), Cross-Attention, Visual Grounding
- **Learn it:** [Vision-Language Models](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/04-computer-vision/25-vision-language-models/)
- **English (source):** A model that learns relationships between, or jointly processes, visual and language representations for tasks such as retrieval, description, question answering, or grounded generation. VLM performance depends on the visual encoder, language component, connection mechanism, training data, and resolution policy rather than one generic capability label.

### Vision Transformer (ViT)

**မြန်မာ:** Vision Transformer (ViT)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ရုပ်ပုံကို position အချက်အလက်နှင့်အတူ patch embedding များ၏ sequence အဖြစ် ဖော်ပြပြီး၊ ထို sequence ကို transformer encoder block များဖြင့် စီမံသည့် vision ဗိသုကာ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် visual data အတွက် sequence-model ချိတ်ဆက်မှုကို ပေးသည်။ သို့သော် စွမ်းဆောင်ရည်နှင့် compute သည် patch အရွယ်အစား၊ resolution၊ pretraining နှင့် inductive bias များအပေါ် မူတည်သည်။
- **မကြာခဏ ရောထွေးမှု:** ViT သည် ဗိသုကာ မိသားစုတစ်ခု ဖြစ်ပြီး၊ ရုပ်ပုံကို လက်ခံသည့် transformer အားလုံး မဟုတ်ပါ။ ၎င်း၏ patch များသည် ပင်ကိုအားဖြင့် semantic object များ မဟုတ်ပါ။
- **လက်တွေ့:** patching နှင့် normalization ကို သင်တန်းနှင့် တူညီစွာ ထားရမည်၊ resolution အသစ်များတွင် position-embedding အပြုအမူကို ထည့်သွင်းစဉ်းစားရမည်၊ ပစ်မှတ် dataset ပေါ်တွင် သင့်လျော်သည့် visual baseline တစ်ခုနှင့် နှိုင်းယှဉ်ရမည်။
- **ဆက်စပ် term များ:** Transformer, Patch Embedding, Self-Attention, Encoder
- **Learn it:** [Vision Transformers](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/04-computer-vision/14-vision-transformers/)
- **English (source):** A vision architecture that represents an image as a sequence of patch embeddings with position information and processes that sequence with transformer encoder blocks. It provides a sequence-model interface for visual data, but performance and compute depend on patch size, resolution, pretraining, and inductive biases.

### Visual Grounding

**မြန်မာ:** visual grounding (ရုပ်ပုံအတွင်း အထောက်အထား ချိတ်ဆက်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ဘာသာစကား ဖော်ပြချက်တစ်ခုကို ရုပ်ပုံ သို့မဟုတ် video အတွင်းရှိ spatial အထောက်အထား — region၊ object၊ mask သို့မဟုတ် ခြေရာခံထားသည့် entity — နှင့် ချိတ်ဆက်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ချောမွေ့သည့် visual အဖြေတစ်ခုသည် အထောက်အထား မရှိနိုင်သည်။ grounding သည် ဆိုလိုသည့် ရည်ညွှန်းချက် (referent) ကို စစ်ဆေးနိုင်စေပြီး region အဆင့် တိုင်းတာမှုကို ဖြစ်နိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** visual grounding သည် ရည်ညွှန်းထားသည့် အထောက်အထား မည်သည့်နေရာတွင် ရှိသည်ကို ဖော်ထုတ်သည်။ ယေဘုယျ image captioning သည် ဖော်ပြချက် တစ်ခုစီကို တည်နေရာ ဖော်ထုတ်ခြင်း မရှိဘဲ မြင်ကွင်းတစ်ခုကို ဖော်ပြနိုင်သည်။
- **လက်တွေ့:** အဖြေနှင့်အတူ box၊ mask သို့မဟုတ် temporal segment တစ်ခု တောင်းခံရမည်၊ မရှင်းလင်းသည့် နှင့် မရှိသည့် referent များကို စမ်းသပ်ရမည်၊ localization ကို ဘာသာစကား မှန်ကန်မှုနှင့် သီးခြားစီ တိုင်းတာရမည်။
- **ဆက်စပ် term များ:** Grounding, Vision-Language Model (VLM), Attention, Evaluation (Eval)
- **Learn it:** [Cross-Attention Fusion](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/19-capstone-projects/61-cross-attention-fusion/)
- **English (source):** Connecting a language expression to spatial evidence in an image or video, such as a region, object, mask, or tracked entity. A fluent visual answer can be unsupported, while grounding makes the claimed referent inspectable and enables region-level evaluation.

## Self-check

1. Audio Token ၏ အဓိပ္ပာယ်နှင့် အချိန် အတိုင်းအတာကို မည်သည့် အရာက ဆုံးဖြတ်သနည်း။
2. ASR နှင့် diarization ကွာခြားချက်သည် အဘယ်နည်း။
3. Early Fusion နှင့် Late Fusion ကွာခြားချက်ကား အဘယ်နည်း။
4. Cross-Attention သည် အမြဲ multimodal ဖြစ်သလား။
5. Visual Grounding သည် ယေဘုယျ image captioning နှင့် မည်သို့ ကွာခြားသနည်း။

<details>
<summary>အဖြေများ</summary>

1. audio token သည် သတ်မှတ်ထားသည့် ကြာချိန်၊ phoneme သို့မဟုတ် စကားလုံး တစ်လုံး မဟုတ်ပါ။ ၎င်း၏ အဓိပ္ပာယ်နှင့် အချိန် အတိုင်းအတာသည် tokenizer နှင့် codebook design အပေါ် မူတည်သည်။
2. ASR သည် ပြောခဲ့သည့် အကြောင်းအရာကို transcript ရေးသည်။ မည်သူ ပြောသည်ကို ဆုံးဖြတ်ရန် diarization သို့မဟုတ် speaker recognition လိုအပ်သည်။
3. Early Fusion သည် task သီးသန့် modeling အများစု မဖြစ်ပေါ်မီ raw သို့မဟုတ် low-level representation များကို ပေါင်းစည်းသည်။ Late Fusion သည် modality တစ်ခုစီကို သီးခြား encoder သို့မဟုတ် predictor များဖြင့် စီမံပြီး အဆင့်မြင့် representation၊ score သို့မဟုတ် ဆုံးဖြတ်ချက်များကို task output အနီးတွင် ပေါင်းစည်းသည်။
4. မဖြစ်ပါ။ cross-attention သည် query ကို sequence တစ်ခုမှ၊ key နှင့် value ကို အခြား တစ်ခုမှ ယူသည့် ပုံစံ ဖြစ်သည်။ text sequence နှစ်ခု သို့မဟုတ် အခြား representation များကိုလည်း ချိတ်ဆက်နိုင်သည်။
5. Visual Grounding သည် ရည်ညွှန်းထားသည့် အထောက်အထား မည်သည့်နေရာတွင် ရှိသည်ကို region၊ object၊ mask သို့မဟုတ် temporal segment အဖြစ် ဖော်ထုတ်သည်။ ယေဘုယျ image captioning သည် ဖော်ပြချက် တစ်ခုစီကို တည်နေရာ ဖော်ထုတ်ခြင်း မရှိဘဲ မြင်ကွင်းတစ်ခုကို ဖော်ပြနိုင်သည်။

</details>

## References

- Source glossary — https://aiengineeringfromscratch.com/glossary
- Source repository — https://github.com/rohitg00/ai-engineering-from-scratch (MIT)
- Lessons — [Neural Audio Codecs](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/06-speech-and-audio/13-neural-audio-codecs/), [Speech Recognition and ASR](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/06-speech-and-audio/04-speech-recognition-asr/), [Chameleon Early-Fusion Tokens](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/12-multimodal-ai/11-chameleon-early-fusion-tokens/), [Vision-Language Models](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/04-computer-vision/25-vision-language-models/), [Cross-Attention Fusion](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/19-capstone-projects/61-cross-attention-fusion/), [MIO Any-to-Any Streaming](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/12-multimodal-ai/16-mio-any-to-any-streaming/), [Projection Layer Modality Alignment](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/19-capstone-projects/60-projection-layer-modality-align/), [Vision Transformer Patch Tokens](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/12-multimodal-ai/01-vision-transformer-patch-tokens/), [CLIP Contrastive Pretraining](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/12-multimodal-ai/02-clip-contrastive-pretraining/), [Vision Transformers](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/04-computer-vision/14-vision-transformers/)
- Papers — [SoundStream](https://arxiv.org/abs/2107.03312), [Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf), [Attention Is All You Need](https://arxiv.org/abs/1706.03762), [Chameleon: Mixed-Modal Early-Fusion Foundation Models](https://arxiv.org/abs/2405.09818), [Multimodal Machine Learning: A Survey and Taxonomy](https://arxiv.org/abs/1705.09406), [Vision Transformer](https://arxiv.org/abs/2010.11929), [VQ-VAE](https://arxiv.org/abs/1711.00937), [Multimodal Deep Learning](https://ai.stanford.edu/~ang/papers/icml11-MultimodalDeepLearning.pdf), [ImageBind](https://arxiv.org/abs/2305.05665), [Learning Transferable Visual Models From Natural Language Supervision](https://proceedings.mlr.press/v139/radford21a.html), [CLIP](https://arxiv.org/abs/2103.00020), [Flamingo](https://arxiv.org/abs/2204.14198), [MDETR](https://arxiv.org/abs/2104.12763)
