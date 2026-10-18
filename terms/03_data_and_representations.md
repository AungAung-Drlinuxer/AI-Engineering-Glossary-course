# Data & Representations (03) — အချက်အလက်နှင့် ကိုယ်စားပြုမှု

ဤဖိုင်သည် လေ့လာနယ်ပယ် **03 — Data & representations** ၏ term **၁၃** ခုကို အင်္ဂလိပ် + မြန်မာ နှစ်ဘာသာဖြင့်
စုစည်းထားသည့် ကိုးကား ဖြစ်သည်။ model တစ်ခု တည်ဆောက်ရာတွင် အချက်အလက် (data) သည် မည်သို့ ဖြစ်ပေါ်လာသည်၊
မည်သို့ ပြုပြင်သန့်စင်သည်၊ မည်သို့ ကိုယ်စားပြု (represent) လုပ်သည် ဆိုသည့် မေးခွန်းများကို ဤနယ်ပယ်က
ဖုံးလွှမ်းသည်။ training အပိုင်း၊ serving အပိုင်း မည်သည့်နေရာတွင်မဆို ဤ term များသည် နောက်ကွယ်မှ
ဆုံးဖြတ်ချက်များကို ချုပ်ကိုင်ထားသည်။

ဤ term ၁၃ ခုကို အဓိက မိသားစု သုံးစု ခွဲ၍ ဖတ်နိုင်သည်။ ပထမ မိသားစုမှာ **token နှင့် စာသား ကိုယ်စားပြုမှု**
— Tokenization၊ Token၊ Vocabulary၊ Byte Pair Encoding (BPE) — ဖြစ်ပြီး စာသားကို model လက်ခံနိုင်သည့်
ကိန်း လက္ခဏာများအဖြစ် ပြောင်းလဲသည့် အလွှာ ဖြစ်သည်။ ဒုတိယ မိသားစုမှာ **vector နှင့် ကိုယ်စားပြုမှု**
— Embedding၊ Cosine Similarity၊ Feature၊ Latent Space၊ Tensor — ဖြစ်ပြီး အဓိပ္ပာယ်ကို continuous space
အတွင်း ကိန်းဂဏန်း အစုအဝေးများဖြင့် ဖော်ပြသည့် အလွှာ ဖြစ်သည်။ တတိယ မိသားစုမှာ **data တည်ငြိမ်မှုနှင့်
ခြေရာခံမှု** — Dataset Split၊ Data Leakage၊ Data Deduplication၊ Data Provenance — ဖြစ်ပြီး အချက်အလက်
တစ်ခုကို ဘယ်အချိန်တွင် ဘယ်လိုသုံးရမည်၊ ဘယ်လို ခြေရာခံရမည် ဆိုသည့် အလွှာ ဖြစ်သည်။

ဤ term များကို အတူတကွ ထားရှုခြင်းသည် အဓိပ္ပာယ် ရှိသည်။ ဥပမာ — Dataset Split သည် Data Leakage ကို
ကာကွယ်ရန် အခြေခံ ဖြစ်ပြီး၊ Data Deduplication သည် split များ အကြား ဆက်စပ်မှုကို ရှာဖွေပေးသည်။
Tokenization သည် vocabulary နှင့် ခွဲထား၍ မရသကဲ့သို့ Embedding သည် Cosine Similarity နှင့်
ခွဲထား၍ မရပါ။ ထို့ကြောင့် ဤဖိုင်ကို term တစ်ခုချင်း အလွတ် မဖတ်ဘဲ မိသားစုအလိုက် ဆက်စပ် term များနှင့်တကွ
မှတ်သားရန် ရည်ရွယ်ထားသည်။

entry တိုင်းကို အောက်ပါအတိုင်း ဖတ်ရမည် — **မြန်မာ** တွင် term ၏ မြန်မာ အမည် သို့မဟုတ် အနီးစပ်ဆုံး
ဖော်ပြချက်၊ **ဆိုလိုသည့် အဓိပ္ပာယ်** တွင် အင်ဂျင်နီယာ အသုံးအနှုန်းအရ တကယ် ဆိုလိုသည့် အဓိပ္ပာယ်၊
**အရေးပါသည့် အကြောင်းရင်း** တွင် မည်သည့် စနစ်တွင် မည်သို့ သက်ရောက်သည်၊ **မကြာခဏ ရောထွေးမှု**
နှင့် **လက်တွေ့** တွင် အလွယ်တကူ မှားတတ်သည့် အချက်နှင့် လက်တွေ့ လုပ်ဆောင်ရမည့် အချက်၊
**ဆက်စပ် term များ** တွင် နောက်တစ်ဆင့် ဖတ်ရမည့် term များ၊ **English (source)** တွင် source ၏ မူရင်း
အင်္ဂလိပ် စာသား byte တူညီစွာ ပါဝင်သည်။ source တွင် အချက်အလက် မပါသော field (confusion၊
practice၊ learn) များကို ချန်လှပ်ထားသည်။ နည်းပညာ အသုံးအနှုန်းများ (tokenization၊ BPE၊ vocabulary၊
embedding၊ data leakage၊ dataset၊ lineage၊ annotation …) ကို မြန်မာ စာကြောင်းအတွင်း အင်္ဂလိပ်အတိုင်း
ထားရှိသည်။

### Byte Pair Encoding (BPE)

**မြန်မာ:** BPE (Byte Pair Encoding — subword tokenization နည်းလမ်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** training text အတွင်း မကြာခဏ ဆက်တွဲ ဖြစ်ပေါ်နေသည့် အနီးကပ် ယူနစ်များကို အကြိမ်ကြိမ် ပေါင်းစပ် (merge) လုပ်ခြင်းဖြင့် ပုံသေ vocabulary တစ်ခုကို တည်ဆောက်သည့် subword-tokenization နည်းလမ်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် vocabulary အရွယ်အစားနှင့် ရှားပါးသည့် သို့မဟုတ် မမြင်ဖူးသေးသည့် စကားလုံးများကို သေးငယ်သည့် ယူနစ်များအဖြစ် ကိုယ်စားပြုနိုင်စွမ်းကို ချိန်ညှိ (balance) ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** BPE သည် tokenizer မိသားစု တစ်ခုသာ ဖြစ်ပြီး model တိုင်း token ဖန်တီးသည့် ပုံစံကို ဖော်ပြသည့် အားလုံးအတွက် သက်ဆိုင်သည့် ဖော်ပြချက် မဟုတ်ပါ။
- **လက်တွေ့:** tokenizer ကို ခွင့်ပြုထားသည့် corpus split များအပေါ်တွင်သာ train လုပ်ပါ၊ ၎င်း၏ merge rule များကို model နှင့်တကွ version မှတ်ပါ၊ code၊ multilingual text နှင့် whitespace ကို မည်သို့ ခွဲခြမ်း ကိုယ်စားပြုသည်ကို စစ်ဆေးပါ။
- **ဆက်စပ် term များ:** Tokenization, Vocabulary, Token, Embedding
- **English (source):** A subword-tokenization method that repeatedly merges frequent adjacent units to construct a fixed vocabulary from training text. It balances vocabulary size with the ability to represent rare or unseen words as smaller units.

### Cosine Similarity

**မြန်မာ:** Cosine similarity (vector နှစ်ခု၏ ဦးတည်ချက် ဆင်တူမှု)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** vector နှစ်ခု၏ normalized dot product ဖြစ်သည်။ ၎င်းသည် vector များ၏ ပမာဏ (magnitude) ကို မဟုတ်ဘဲ ဦးတည်ချက် (direction) ကို နှိုင်းယှဉ်ပေးပြီး၊ real-valued vector များအတွက် -1 မှ 1 အထိ တန်ဖိုး ရှိသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် vector များ၏ ပမာဏ မဟုတ်ဘဲ ဦးတည်ချက်ကို နှိုင်းယှဉ်သဖင့် ဆင်တူမှုကို တိုင်းတာရာတွင် အသုံးဝင်သည်၊ သို့သော် ရရှိသည့် တန်ဖိုးသည် embedding model နှင့် data distribution ကို အခြေခံ၍သာ အဓိပ္ပာယ် ရှိပြီး အချက်အလက်အရ တူညီမှုကို သက်သေ မပြပါ။
- **မကြာခဏ ရောထွေးမှု:** cosine similarity မြင့်မားခြင်းသည် embedding model နှင့် data distribution ကို အခြေခံ၍သာ အဓိပ္ပာယ် ရှိသည်။ ၎င်းသည် အချက်အလက်အရ သို့မဟုတ် အဓိပ္ပာယ်အရ တူညီမှုကို သက်သေ မပြပါ။
- **ဆက်စပ် term များ:** Embedding, Semantic Search, Reranker
- **English (source):** The normalized dot product of two vectors. It compares their direction rather than their magnitude and ranges from -1 to 1 for real-valued vectors.

### Data Deduplication

**မြန်မာ:** Data deduplication (ထပ်တူ အချက်အလက်များကို ဖယ်ရှားခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** dataset တစ်ခုအတွင်း သို့မဟုတ် dataset များအကြား တိကျတူညီသည့် (exact) နှင့် အနီးစပ်ဆုံး တူညီသည့် (near-duplicate) နမူနာများကို ရှာဖွေပြီး ဖယ်ရှားခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ထပ်တလဲလဲ ဖြစ်နေခြင်းသည် training distribution ကို ပျက်စီးစေနိုင်ပြီး၊ memorization ကို တိုးစေကာ၊ test material ကို ယိုစိမ့်စေနိုင်ပြီး၊ evaluation ကို အမှန်တကယ်ထက် ပိုကောင်းသည်ဟု ထင်ရစေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Deduplication သည် သာမန် data cleaning မဟုတ်ပါ။ မတူညီသည့် record နှစ်ခုသည် စာသား တူညီစွာ ရှိနိုင်ပြီး၊ paraphrase နှစ်ခုသည် တူညီသည့် ယိုစိမ့်သည့် အချက်အလက်ကို ဆက်လက် သယ်ဆောင်ထားနိုင်သည်။
- **လက်တွေ့:** content ကို normalize လုပ်ပါ၊ exact hash များနှင့် similarity နည်းလမ်းများကို အသုံးပြုပါ၊ အလယ်အလတ် အုပ်စုများကို ပြန်လည် စစ်ဆေးပါ၊ မည်သည့် version နှင့် စည်းမျဉ်းက မည်သည့် နမူနာကို ဖယ်ရှားခဲ့သည်ကို မှတ်တမ်းတင်ပါ။
- **ဆက်စပ် term များ:** Data Provenance, Benchmark Contamination, Dataset Split, Overfitting
- **English (source):** Detecting and removing exact and near-duplicate examples within or across datasets. Repetition can distort the training distribution, increase memorization, leak test material, and make evaluation appear stronger than it is.

### Data Leakage

**မြန်မာ:** Data leakage (အချက်အလက် ယိုစိမ့်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** training အတွင်း သို့မဟုတ် feature တည်ဆောက်မှုအတွင်း တကယ့် prediction အချိန်တွင် ရရှိနိုင်မည် မဟုတ်သည့် အချက်အလက်ကို လည်းကောင်း၊ သီးခြား ဖယ်ထားသည့် evaluation နယ်နိမိတ်အတွင်း ပါဝင်သည့် အချက်အလက်ကို လည်းကောင်း မရည်ရွယ်ဘဲ အသုံးပြုခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ယိုစိမ့်မှုသည် အကောင်းဘက် လွန်ကဲသည့် metric များကို ဖြစ်ပေါ်စေပြီး၊ စနစ်သည် တကယ် မမြင်ဖူးသေးသည့် input များနှင့် ကြုံသည့်အခါ ထို metric များ ပြိုလဲသွားသည်။
- **မကြာခဏ ရောထွေးမှု:** ယိုစိမ့်မှုသည် ထပ်တူကျသည့် row များတွင်သာ ကန့်သတ်မထားပါ။ Global normalization statistic များ၊ timestamp များ၊ target မှ ဆင်းသက်သည့် feature များနှင့် test ကို အခြေခံ၍ ထပ်ခါတလဲလဲ ပြုပြင်သည့် prompt များ အားလုံး အချက်အလက် ယိုစိမ့်စေနိုင်သည်။
- **လက်တွေ့:** preprocessor များကို fit မလုပ်မီ data ကို split လုပ်ပါ၊ historical feature များမှ အနာဂတ် အချက်အလက်ကို ဖယ်ထုတ်ထားပါ၊ test label များနှင့် benchmark အဖြေများကို prompt များနှင့် tuning loop များမှ သီးခြား ခွဲထားပါ။
- **ဆက်စပ် term များ:** Dataset Split, Benchmark Contamination, Eval Set, Data Provenance
- **English (source):** Unintended use of information during training or feature construction that would not be available at the real prediction point or belongs to a held-out evaluation boundary. Leakage produces optimistic metrics that collapse when the system encounters genuinely unseen inputs.

### Data Provenance

**မြန်မာ:** Data provenance (အချက်အလက်၏ မူလနှင့် အသွင်ပြောင်းမှု ခြေရာခံချက်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အချက်အလက်သည် မည်သည့်နေရာမှ မူလ ဖြစ်ပေါ်ခဲ့သည်၊ မည်သူ သို့မဟုတ် မည်သည့် အရာက ၎င်းကို အသွင်ပြောင်းခဲ့သည်၊ မည်သည့် version များကို အသုံးပြုခဲ့သည်၊ ဆင်းသက်သည့် artifact များသည် ၎င်းတို့၏ source များနှင့် မည်သို့ ဆက်စပ်နေသည်ကို ခြေရာခံနိုင်သည့် အချက်အလက် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ရလဒ်များကို ပြန်လည် ဖန်တီးရန်၊ အသုံးပြုမှု ကန့်သတ်ချက်များကို လိုက်နာရန်၊ ညစ်ညမ်းမှုကို စုံစမ်းရန် နှင့် source ပြောင်းလဲသည့်အခါ ထိခိုက်သည့် အချက်အလက်ကို ဖယ်ရှားရန် provenance ကို လိုအပ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Source URL သည် provenance ၏ အစိတ်အပိုင်း တစ်ခုသာ ဖြစ်သည်။ ၎င်းသည် စုဆောင်းသည့် အချိန်၊ လိုင်စင် အခြေအနေ၊ filtering၊ အသွင်ပြောင်းမှု သို့မဟုတ် နောက်ဆက်တွဲ အသုံးပြုမှုကို ဖော်ပြသည်မဟုတ်ပါ။
- **လက်တွေ့:** ပြောင်းလဲ၍ မရသည့် dataset version များကို သတ်မှတ်ပါ၊ transformation job များနှင့် source identifier များကို မှတ်တမ်းတင်ပါ၊ lineage metadata ကို embedding၊ eval case နှင့် model artifact များထဲသို့ သယ်ဆောင်ပါ။
- **ဆက်စပ် term များ:** Dataset Split, Data Deduplication, Provenance Attestation, Grounding
- **English (source):** Traceable information about where data originated, who or what transformed it, which versions were used, and how derived artifacts relate to their sources. You need provenance to reproduce results, honor usage constraints, investigate contamination, and remove affected data when a source changes.

### Dataset Split

**မြန်မာ:** Dataset split (dataset ကို အပိုင်းများ ခွဲခြားခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** နမူနာများကို fitting၊ development ဆုံးဖြတ်ချက်များနှင့် နောက်ဆုံး evaluation အတွက် သီးခြား subset များအဖြစ် မှတ်တမ်းတင် ခွဲခြားထားသည့် အပိုင်းအခြား ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ခွဲခြားထားခြင်းသည် စနစ် တစ်ခုကို ရွေးချယ်ရန် အသုံးပြုသည့် အထောက်အထားက ရွေးချယ်ပြီးသား စနစ် generalization ရှိသည်ဟု သီးခြား သက်သေအဖြစ် ထပ်မံ မထမ်းဆောင်နိုင်ရန် တားဆီးပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** ကျပန်း split သည် အလိုအလျောက် လွတ်လပ်မှု ရှိသည်မဟုတ်ပါ။ အနီးစပ်ဆုံး တူညီသည့် နမူနာများ၊ အနာဂတ် လေ့လာတွေ့ရှိချက်များ သို့မဟုတ် entity တစ်ခုတည်းမှ record များသည် နယ်နိမိတ်ကို ဖြတ်ကျော်နိုင်သည်။
- **လက်တွေ့:** ဆက်စပ်နေသည့် row များကို ကျပန်း ခွဲခြင်းထက် user၊ repository၊ organization သို့မဟုတ် အချိန် ကဲ့သို့ တကယ့် deployment ယူနစ်အလိုက် ခွဲခြားပါ။
- **ဆက်စပ် term များ:** Eval Set, Overfitting, Data Leakage, Distribution Shift
- **English (source):** A documented partition of examples into separate subsets for fitting, development decisions, and final evaluation. Separation prevents the evidence used to choose a system from also serving as independent proof that the chosen system generalizes.

### Embedding

**မြန်မာ:** Embedding (အဓိပ္ပာယ်ကို ကိုယ်စားပြုသည့် vector)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သီးခြား အရာဝတ္ထုများ (စကားလုံးများ၊ ရုပ်ပုံများ၊ အသုံးပြုသူများ) ကို continuous space အတွင်းရှိ dense vector များသို့ သင်ယူထားသည့် mapping ဖြစ်ပြီး၊ ဆင်တူသည့် အရာဝတ္ထုများသည် အတူတကွ နီးကပ်စွာ ရောက်ရှိသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** သီးခြား အရာဝတ္ထုများကို vector အဖြစ် ကိုယ်စားပြုသဖင့် ၎င်းတို့ကြား ဆင်တူမှုကို အကွာအဝေးဖြင့် တိုင်းတာနိုင်သည် — သို့သော် ထို ဆင်တူမှုသည် သက်ဆိုင်သည့် model၊ training objective နှင့် metric အတွင်း၌သာ အဓိပ္ပာယ် ရှိသည်။
- **မကြာခဏ ရောထွေးမှု:** ဆင်တူမှုသည် model၊ training objective နှင့် metric အပေါ် မူတည်သည်။ embedding space တစ်ခုအတွင်း အကွာအဝေးသည် အခြား space တစ်ခုသို့ ကူးယူ အသုံးပြု၍ မရပါ။
- **ဆက်စပ် term များ:** Cosine Similarity, Semantic Search, Vector Database
- **Learn it:** [Embeddings](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/04-embeddings/)
- **English (source):** A learned mapping from discrete items (words, images, users) to dense vectors in continuous space, where similar items end up close together

### Feature

**မြန်မာ:** Feature (အချက်အလက်၏ တိုင်းတာနိုင်သည့် ပိုင်ဆိုင်မှု)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အချက်အလက်၏ တိုင်းတာနိုင်သည့် ပိုင်ဆိုင်မှု တစ်ခုချင်း ဖြစ်သည်။ classical ML တွင် feature များကို လက်ဖြင့် တည်ဆောက် (engineer) ရသည်။ deep learning တွင် network သည် raw data မှ feature များကို အလိုအလျောက် သင်ယူသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** feature သည် အချက်အလက်၏ တိုင်းတာနိုင်သည့် ပိုင်ဆိုင်မှု ဖြစ်သဖင့် classical ML တွင် လက်ဖြင့် တည်ဆောက်ရပြီး deep learning တွင် raw data မှ အလိုအလျောက် သင်ယူသည် — ထို့ကြောင့် feature ကို မည်သို့ ရရှိသည်က နည်းလမ်း နှစ်မျိုး၏ ကွာခြားချက်ကို ထင်ဟပ်သည်။
- **မကြာခဏ ရောထွေးမှု:** သိမ်းဆည်းထားသည့် column တစ်ခုတွင် အသုံးဝင်သည့် feature အများအပြား ပါဝင်နိုင်ပြီး၊ သင်ယူထားသည့် representation တစ်ခုတွင် လူက ရိုးရှင်းစွာ အမည် မတပ်နိုင်သည့် feature များလည်း ပါဝင်နိုင်သည်။
- **ဆက်စပ် term များ:** Embedding, Latent Space, Inductive Bias
- **English (source):** An individual measurable property of the data. In classical ML, you engineer features by hand. In deep learning, the network learns features automatically from raw data.

### Latent Space

**မြန်မာ:** Latent space (model ၏ ဖုံးကွယ်ထားသည့် representation space)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** coordinate များက model အတွက် အသုံးဝင်သည့် အချက်များကို encode လုပ်ထားသည့် သင်ယူထားသည့် representation space ဖြစ်သည်။ ၎င်းသည် input ထက် dimension နည်းနိုင်သည်၊ သို့သော် latent representation တိုင်းအတွက် compression လိုအပ်သည်မဟုတ်ပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** latent space အတွင်း အနီးအနား ရှိသည့် point များသည် model နှင့် training objective က သင်ယူထားသည့် အရာအရသာ အဓိပ္ပာယ် ရှိသည့် ဆင်တူမှုကို ဖော်ပြသဖင့်၊ ထို space ကို အခြေခံ၍ ဆင်တူမှု ကောက်ချက်ချသည့်အခါ သင်ယူမှု သဘောသဘာဝကို ထည့်သွင်း စဉ်းစားရမည်။
- **မကြာခဏ ရောထွေးမှု:** အနီးအနား ရှိသည့် point များသည် model နှင့် training objective က သင်ယူထားသည့် အရာအရသာ အဓိပ္ပာယ် ရှိသည့် ဆင်တူမှု ရှိသည်။
- **ဆက်စပ် term များ:** Embedding, VAE (Variational Autoencoder), Feature
- **English (source):** A learned representation space whose coordinates encode factors useful to a model. It may be lower-dimensional than the input, but compression is not required for every latent representation.

### Tensor

**မြန်မာ:** Tensor (shape၊ data type စသည့် ဂုဏ်သတ္တိပါသည့် ဘက်စုံ array)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** shape၊ data type နှင့် device placement ပါဝင်သည့် typed array ဖြစ်ပြီး၊ framework များသည် input၊ parameter၊ activation နှင့် gradient များကို ကိုယ်စားပြုရန် ၎င်းကို အသုံးပြုသည်။ automatic-differentiation metadata သည် framework နှင့် operation အပေါ် မူတည်ပြီး tensor တိုင်း၏ ပင်ကို ဂုဏ်သတ္တိ မဟုတ်ပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** framework များသည် input၊ parameter၊ activation နှင့် gradient များကို tensor ဖြင့် ကိုယ်စားပြုသဖင့် ၎င်း၏ shape၊ data type နှင့် device placement ကို သိရှိထားခြင်းသည် computation ကို နားလည်ရန် အခြေခံ ဖြစ်သည်။
- **ဆက်စပ် term များ:** Autograd, Parameter, Mixed Precision
- **English (source):** A typed array with a shape, data type, and device placement that frameworks use to represent inputs, parameters, activations, and gradients. Automatic-differentiation metadata is framework- and operation-dependent, not an inherent property of every tensor.

### Token

**မြန်မာ:** Token (model လက်ခံသည့် ကိုယ်စားပြုမှု ယူနစ် တစ်ခု)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** စာသား၊ byte၊ ရုပ်ပုံ၊ အသံ သို့မဟုတ် အခြား input representation မှ model-specific tokenizer က ထုတ်ပေးသည့် integer identifier ဖြစ်သည်။ token တစ်ခုသည် စကားလုံး တစ်လုံးလုံး၊ စကားလုံး၏ အစိတ်အပိုင်း တစ်ခု၊ punctuation၊ whitespace၊ byte sequence သို့မဟုတ် special control symbol တစ်ခု ဖြစ်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** token သည် model-specific tokenizer က ထုတ်ပေးသည့် integer identifier ဖြစ်သဖင့် ၎င်း အရေအတွက်သည် language၊ content နှင့် tokenizer အလိုက် ကွာခြားသည့် character-to-token ratio အပေါ် မူတည်ပြီး target model ၏ tokenizer သို့မဟုတ် provider tool များဖြင့် ရေတွက်ရမည်။
- **မကြာခဏ ရောထွေးမှု:** character-to-token ratio များသည် language၊ content နှင့် tokenizer အလိုက် ကွာခြားသဖင့် target model ၏ tokenizer သို့မဟုတ် provider tool များဖြင့် ရေတွက်ရမည်။
- **ဆက်စပ် term များ:** Token Budget, Context Window, Autoregressive
- **Learn it:** [Tokenizers](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/10-llms-from-scratch/01-tokenizers/)
- **English (source):** An integer identifier produced by a model-specific tokenizer from text, bytes, images, audio, or another input representation. A token can be a whole word, part of a word, punctuation, whitespace, a byte sequence, or a special control symbol.

### Tokenization

**မြန်မာ:** Tokenization (token များအဖြစ် ခွဲခြမ်းခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** input representation တစ်ခုကို သတ်မှတ်ထားသည့် model သို့မဟုတ် tokenizer လက်ခံသည့် အစဉ်လိုက် (ordered) token identifier များအဖြစ် ပြောင်းလဲခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** tokenization သည် sequence အရှည်၊ vocabulary နယ်နိမိတ်၊ ကုန်ကျစရိတ် တွက်ချက်မှု၊ truncation အပြုအမူနှင့် embedding မပြုမီ စာသား သို့မဟုတ် code ကို ကိုယ်စားပြုသည့် ပုံစံကို ဆုံးဖြတ်သည်။
- **မကြာခဏ ရောထွေးမှု:** tokenization သည် အမြဲတမ်း စကားလုံး ခွဲခြင်းမဟုတ်ပါ၊ model နှစ်ခုသည် တူညီသည့် input အတွက် မတူညီသည့် token အရေအတွက်နှင့် ID များကို သတ်မှတ်နိုင်သည်။
- **လက်တွေ့:** target model အတွက် တိကျသည့် tokenizer ကို အသုံးပြုပါ၊ ၎င်းကို artifact များနှင့်တကွ version မှတ်ပါ၊ multilingual text၊ code၊ whitespace နှင့် special token များကို စမ်းသပ်ပါ။
- **ဆက်စပ် term များ:** Token, Vocabulary, Byte Pair Encoding (BPE), Embedding
- **English (source):** Converting an input representation into the ordered token identifiers a specific model or tokenizer accepts. Tokenization determines sequence length, vocabulary boundaries, cost accounting, truncation behavior, and how text or code is represented before embedding.

### Vocabulary

**မြန်မာ:** Vocabulary (tokenizer က ထုတ်နိုင်သည့် token အစုအဝေး)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** token identifier များနှင့် tokenizer က ထုတ်နိုင်သည့် ယူနစ်များအကြား အကန့်အသတ် ရှိသည့် mapping ဖြစ်ပြီး၊ သာမန် token များ၊ byte-level token များနှင့် special control token များ ပါဝင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** vocabulary တည်ဆောက်ပုံသည် sequence အရှည်၊ multilingual coverage၊ code ကိုယ်စားပြုမှု၊ embedding အရွယ်အစားနှင့် tokenizer များနှင့် model weight များအကြား ကိုက်ညီမှုကို သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** model vocabulary သည် လူသုံး စကားလုံး အဘိဓာန် မဟုတ်ပါ။ entry အများအပြားသည် အစိတ်အပိုင်း အက်ကွဲများ၊ byte များ၊ whitespace ပုံစံများ သို့မဟုတ် control symbol များ ဖြစ်သည်။
- **လက်တွေ့:** vocabulary နှင့် special-token သတ်မှတ်ချက်များကို model နှင့်တကွ version မှတ်ပါ၊ encode-decode round trip များကို စမ်းသပ်ပါ၊ token အမည် ဆင်တူရုံမျှဖြင့် tokenizer ကို အစားထိုး၍ ဘယ်သောအခါမျှ မလုပ်ပါနှင့်။
- **ဆက်စပ် term များ:** Tokenization, Byte Pair Encoding (BPE), Token, Embedding
- **English (source):** The finite mapping between token identifiers and the units a tokenizer can emit, including ordinary, byte-level, and special control tokens. Vocabulary design affects sequence length, multilingual coverage, code representation, embedding size, and compatibility between tokenizers and model weights.

## Self-check

1. Tokenization၊ Token နှင့် Vocabulary တို့၏ တာဝန်ကို မည်သို့ ခွဲခြားသနည်း။
2. Byte Pair Encoding (BPE) သည် vocabulary အရွယ်အစားနှင့် ရှားပါး စကားလုံး ကိုယ်စားပြုမှုကို မည်သို့ ချိန်ညှိပေးသနည်း။
3. Cosine Similarity မြင့်မားခြင်းသည် အဘယ်ကြောင့် အချက်အလက်အရ တူညီမှုကို သက်သေ မပြသနည်း။
4. Dataset Split သည် Data Leakage ကို မည်သို့ ကာကွယ်ပေးသနည်း၊ ကျပန်း split သည် အဘယ်ကြောင့် လုံလောက်မှု မရှိသနည်း။
5. Data Deduplication နှင့် Data Provenance တို့သည် evaluation ၏ ယုံကြည်စိတ်ချရမှုကို မည်သို့ အထောက်အကူ ပြုသနည်း။

<details>
<summary>အဖြေများ</summary>

1. Token သည် tokenizer က ထုတ်ပေးသည့် integer identifier တစ်ခု ဖြစ်သည်။ Vocabulary သည် ထို
   identifier များနှင့် tokenizer က ထုတ်နိုင်သည့် ယူနစ်များအကြား အကန့်အသတ် ရှိသည့် mapping ဖြစ်သည်။
   Tokenization သည် input representation တစ်ခုကို ထို identifier များအဖြစ် အစဉ်လိုက် ပြောင်းလဲသည့်
   လုပ်ငန်းစဉ် ဖြစ်သည်။ သုံးခုစလုံးသည် အလွှာ တစ်ခုတည်း၏ အစိတ်အပိုင်းများ ဖြစ်သည်။
2. BPE သည် training text အတွင်း မကြာခဏ ဆက်တွဲ ဖြစ်ပေါ်နေသည့် အနီးကပ် ယူနစ်များကို အကြိမ်ကြိမ်
   ပေါင်းစပ်ခြင်းဖြင့် ပုံသေ vocabulary တစ်ခုကို တည်ဆောက်သည်။ ထို့ကြောင့် ရှားပါးသည့် သို့မဟုတ်
   မမြင်ဖူးသေးသည့် စကားလုံးများကို သေးငယ်သည့် ယူနစ်များအဖြစ် ကိုယ်စားပြုနိုင်စေပြီး vocabulary
   အရွယ်အစားကို ထိန်းချုပ်ထားနိုင်သည်။
3. Cosine Similarity သည် vector နှစ်ခု၏ ဦးတည်ချက် ဆင်တူမှုကို တိုင်းတာသည်။ ထို တန်ဖိုးသည်
   embedding model နှင့် data distribution ကို အခြေခံ၍သာ အဓိပ္ပာယ် ရှိသည်။ ထို့ကြောင့်
   similarity မြင့်မားခြင်းသည် အချက်အလက်အရ သို့မဟုတ် အဓိပ္ပာယ်အရ တူညီမှုကို သက်သေ မပြပါ။
4. Dataset Split သည် စနစ် တစ်ခုကို ရွေးချယ်ရန် အသုံးပြုသည့် အထောက်အထားက ထို စနစ်၏
   generalization သက်သေအဖြစ် ထပ်မံ မထမ်းဆောင်နိုင်ရန် သီးခြား ခွဲထားသည်။ ကျပန်း split သည်
   အနီးစပ်ဆုံး တူညီသည့် နမူနာများ၊ အနာဂတ် လေ့လာတွေ့ရှိချက်များ သို့မဟုတ် entity တစ်ခုတည်းမှ
   record များ နယ်နိမိတ်ကို ဖြတ်ကျော်နိုင်သဖင့် အလိုအလျောက် လွတ်လပ်မှု ရှိသည်မဟုတ်ပါ။
5. Data Deduplication သည် ထပ်တလဲလဲ ဖြစ်နေခြင်းကို ဖယ်ရှားခြင်းဖြင့် training distribution
   ပျက်စီးမှုကို လျှော့ချပြီး၊ test material ယိုစိမ့်မှုကို တားဆီးသဖင့် evaluation ကို အမှန်တကယ်ထက်
   ပိုကောင်းသည်ဟု ထင်ရစေခြင်းကို လျှော့ချသည်။ Data Provenance သည် ရလဒ်များကို ပြန်လည်
   ဖန်တီးနိုင်ခြင်း၊ ညစ်ညမ်းမှုကို စုံစမ်းနိုင်ခြင်းနှင့် source ပြောင်းလဲသည့်အခါ ထိခိုက်သည့်
   အချက်အလက်ကို ဖယ်ရှားနိုင်ခြင်းဖြင့် evaluation ကို ယုံကြည်စိတ်ချနိုင်စေသည်။

</details>

## References

- Source glossary — https://aiengineeringfromscratch.com/glossary
- Source repository — https://github.com/rohitg00/ai-engineering-from-scratch (MIT license)
- [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909)
- [Deduplicating Training Data Makes Language Models Better](https://arxiv.org/abs/2107.06499)
- [scikit-learn: Data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage)
- [W3C PROV Overview](https://www.w3.org/TR/prov-overview/)
- [Datasheets for Datasets](https://cacm.acm.org/research/datasheets-for-datasets/)
- [Embeddings](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/04-embeddings/)
- [Tokenizers](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/10-llms-from-scratch/01-tokenizers/)
