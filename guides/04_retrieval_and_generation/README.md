# Area 04 — Retrieval & generation (terms + glossary shortcut)

<!-- guide-kind: terms-only -->

ဤဖိုင်သည် area 04 ၏ term ၁၄ ခုကို အတိုချုံး ရှင်းပြထားသည်။ term တိုင်းကို — term ဆိုတာ ဘာလဲ၊ ဥပမာ တစ်ခု၊
အတိုင်းအတာ သို့မဟုတ် အသုံးဝင်ပုံ ဆိုတဲ့ ၃ ကြောင်းဖြင့် ရေးထားသည်။ term ၁၄ ခုကို အဆင့် ၄ ခုအဖြစ် စီထားသည်။

## ၁။ chunk ခွဲခြင်းနှင့် vector index တည်ဆောက်ခြင်း

### Chunking

Chunking ဆိုတာ document တွေကို index မလုပ်ခင် ရှာဖွေနိုင်တဲ့ အပိုင်းအစ (chunk) တွေအဖြစ် ခွဲခြားတာကို ဆိုလိုပါတယ်။
ဥပမာ token 12,000 ရှိတဲ့ document တစ်ခုကို chunk 512 token၊ overlap 64 token နဲ့ ခွဲရင် chunk 27 ခု ရပြီး၊ overlap ကြောင့် token 1,824 ခု (၁၅% လောက်) ထပ်သိမ်းရပါတယ်။
Chunk အရွယ်အစားနဲ့ နယ်နိမိတ်က index ကုန်ကျစရိတ်နဲ့ retrieval အရည်အသွေး နှစ်ခုလုံးကို တိုက်ရိုက် ဆုံးဖြတ်ပါတယ် — အားလုံးအတွက် မှန်တဲ့ အရွယ်အစား မရှိပါဘူး။

### Approximate Nearest Neighbor (ANN)

Approximate Nearest Neighbor (ANN) ဆိုတာ query ကို သိမ်းထားတဲ့ vector တိုင်းနဲ့ အပြည့်အစုံ နှိုင်းယှဉ်ခြင်း မပြုဘဲ အနီးစပ်ဆုံး ဖြစ်နိုင်တဲ့ vector တွေကို ပြန်ပေးတဲ့ ရှာဖွေမှု နည်းလမ်း ဖြစ်ပါတယ်။
ဥပမာ vector 1,000,000 ခု ရှိတဲ့ index မှာ အပြည့်အစုံ နှိုင်းယှဉ်ရင် 1,000,000 ခု စစ်ရပြီး၊ ANN နဲ့ 100 ခုလောက်သာ စစ်ရတာမို့ အလုပ်ပမာဏ 10,000 ဆ လျော့သွားပါတယ်။
Approximation ဖြစ်တာမို့ true neighbor အားလုံး တွေ့မယ်လို့ ယူဆလို့ မရပါဘူး — latency နဲ့ recall@K ကို တွဲပြီး တိုင်းတာရပါတယ်။

### HNSW

HNSW ဆိုတာ vector တွေကို အလွှာလိုက် proximity graph တွေမှာ စီပြီး အထက်လွှာ ကြမ်းကြမ်းကနေ အောက်လွှာ အသေးစိတ်ဆီ ဆင်းရှာတဲ့ approximate-nearest-neighbor index ဖြစ်ပါတယ်။
ဥပမာ vector 1,000,000 ခုကို အလွှာ ၃ ခုနဲ့ စီထားရင် အထက်လွှာမှာ 1,000 ခု၊ အလယ်လွှာမှာ 10,000 ခု၊ အောက်လွှာမှာ 1,000,000 ခု ရှိပြီး၊ လွှာတစ်ခုလျှင် 100 ခုလောက် စစ်တာမို့ နှိုင်းယှဉ်မှု ၃၀၀ လောက်သာ ဖြစ်ပါတယ်။
HNSW က index algorithm တစ်ခုသာ ဖြစ်ပါတယ် — similarity metric လည်း မဟုတ်ပါဘူး၊ embedding model လည်း မဟုတ်ပါဘူး။

### Vector Database

Vector Database ဆိုတာ vector တွေအပေါ် nearest-neighbor query ကို ထောက်ပံ့တဲ့ storage နဲ့ indexing စနစ် ဖြစ်ပြီး၊ metadata filter၊ persistence နဲ့ approximate index တွေ ပါလေ့ ရှိပါတယ်။
ဥပမာ chunk 1,000,000 ခုကို dim 768 embedding၊ fp32 (vector တစ်ခုလျှင် 3,072 byte) နဲ့ သိမ်းရင် ကုန်ကျမှု 3,072,000,000 byte (3.1 GB လောက်) ဖြစ်ပါတယ်။
Chunk ၁၀ သန်း ဖြစ်လာရင် အဲဒီ ပမာဏ 30.7 GB လောက် ဖြစ်လာတာမို့ index အရွယ်အစားကို အရင် တွက်ထားရပါတယ်။

## ၂။ ရှာဖွေခြင်း — lexical နှင့် semantic

### BM25

BM25 ဆိုတာ query ထဲက စကားလုံး ကိုက်ညီမှုအပေါ် document အမှတ်ပေးတဲ့ lexical ranking function ဖြစ်ပြီး၊ စကားလုံး ရှားပါးမှု၊ ထပ်ပါဝင်မှုနဲ့ document အရှည်ကို ထည့် စဉ်းစားပါတယ်။
ဥပမာ document 1,000 ခု ရှိတဲ့ collection မှာ ရှားပါးတဲ့ "INV-2049" ပါတဲ့ document ၂ ခုကို BM25 က ထိပ်ဆုံး ရာထူး ပေးလိုက်ပါတယ်။
Semantic similarity ကို တိုက်ရိုက် နားလည်တာ မဟုတ်လို့ paraphrase မေးခွန်းတွေအတွက် dense search နဲ့ တွဲသုံးရပါတယ်။

### Dense Retrieval

Dense Retrieval ဆိုတာ query နဲ့ candidate တွေကို vector အဖြစ် embed လုပ်ပြီး similarity function နဲ့ အစဉ်သတ်မှတ်တဲ့ ပထမအဆင့် retrieval ဖြစ်ပါတယ်။
ဥပမာ "ငွေ ဘယ်လို ပြန်ရမလဲ" ဆိုတဲ့ query က "refund policy" chunk ကို စကားလုံး တူညီမှု သုည ဖြစ်လည်း embedding နီးတာမို့ ထိပ်ဆုံး 5 ခုထဲ ပါလာပါတယ်။
Dense retrieval က collection တစ်ခုလုံး ရှာတဲ့ ပထမအဆင့် ဖြစ်ပြီး၊ candidate အနည်းငယ်ကို ပြန်စီတဲ့ reranker နဲ့ တာဝန် မတူပါဘူး။

### Hybrid Retrieval

Hybrid Retrieval ဆိုတာ lexical ကိုက်ညီမှုနဲ့ dense-vector သက်ဆိုင်မှု နှစ်မျိုးလုံး ရှာပြီး ရလဒ်တွေကို ပေါင်းတာ သို့မဟုတ် ပြန်စီတာကို ဆိုလိုပါတယ်။
ဥပမာ BM25 က candidate 50 ခု၊ dense search က candidate 50 ခု ပေးလာပြီး ထပ်နေတာ 20 ခု ဖယ်ရင် ပေါင်းထားတဲ့ candidate 80 ခု ရပါတယ် (50 + 50 − 20 = 80)။
Exact identifier နဲ့ semantic paraphrase တွေ အပြုအမူ မတူတာမို့ signal တစ်ခုတည်း သုံးရင် အသုံးဝင်တဲ့ အထောက်အထား လွတ်နိုင်ပါတယ်။

### Semantic Search

Semantic Search ဆိုတာ query နဲ့ candidate ကို embedding space တစ်ခုထဲ ကိုယ်စားပြုပြီး vector similarity နဲ့ အစဉ်သတ်မှတ်တဲ့ ရှာဖွေမှု ဖြစ်ပါတယ်။
ဥပမာ query "ငွေ ဘယ်လို ပြန်ရမလဲ" နဲ့ document "refund process" မှာ စကားလုံး တူညီမှု သုည ဖြစ်လည်း embedding နီးတာမို့ ထိပ်ဆုံး 3 ခုထဲ ပါလာပါတယ်။
Paraphrase ကို ရှာနိုင်ပေမယ့် exact ID နဲ့ ရှားပါးတဲ့ string တွေအတွက် lexical search ကို ဆက်သုံးရပါတယ်။

## ၃။ ရလဒ်ကို ပြန်စီခြင်းနှင့် တိုင်းတာခြင်း

### Maximum Marginal Relevance (MMR)

Maximum Marginal Relevance (MMR) ဆိုတာ query နဲ့ သက်ဆိုင်မှုနဲ့ ရွေးပြီးသား item တွေနဲ့ မတူမှု (novelty) ကို မျှတစေတဲ့ ရွေးချယ်မှု စည်းမျဉ်း ဖြစ်ပါတယ်။
ဥပမာ candidate 20 ခုထဲမှာ အလွန် ဆင်တူတဲ့ chunk ၆ ခု ပါရင် MMR က အဲဒီ အထဲက ၁ ခုသာ ယူပြီး ကျန် ၅ ခု နေရာမှာ ကွဲပြားတဲ့ chunk တွေ ထည့်ပါတယ်။
ဒီလို လုပ်တာက ကန့်သတ်ထားတဲ့ context ဘတ်ဂျက်ထဲမှာ အထောက်အထား ပိုစုံစေပေမယ့် လွတ်နေတဲ့ အထောက်အထားကို ရှာပေးတာ မဟုတ်ပါဘူး။

### Recall@K

Recall@K ဆိုတာ query တစ်ခုအတွက် ထိပ်ဆုံး K ခုထဲ သက်ဆိုင်တဲ့ item ဘယ်နှခု ပါလာတာကို သက်ဆိုင်တဲ့ item စုစုပေါင်းနဲ့ စားတဲ့ အချိုး ဖြစ်ပါတယ်။
ဥပမာ သက်ဆိုင်တဲ့ chunk 10 ခု ရှိတဲ့ query တစ်ခုမှာ ထိပ်ဆုံး 10 ခုထဲ 8 ခု ပါလာရင် recall@10 = 8 / 10 = 0.8 ဖြစ်ပါတယ်။
0.8 ဆိုတာ သက်ဆိုင်တဲ့ ၂ ခု လွတ်နေတယ် ဆိုတာ ဖြစ်ပြီး၊ recall မြင့်ခြင်းက ထိပ်ဆုံး ရလဒ် ကောင်းတယ်လို့ မဆိုလိုပါဘူး။

### Reciprocal Rank Fusion (RRF)

Reciprocal Rank Fusion (RRF) ဆိုတာ result list အတော်များများကို rank တစ်ခုချင်းစီအပေါ် လျော့နည်းသွားတဲ့ ပါဝင်မှုတွေ ပေါင်းပြီး ပေါင်းစပ်တဲ့ rank-fusion နည်းလမ်း ဖြစ်ပါတယ်။
ဥပမာ doc တစ်ခုက list တစ်ခုမှာ rank 1၊ နောက် list မှာ rank 3 ဖြစ်ပြီး k=60 ထားရင် 1 / 61 + 1 / 63 = 0.0164 + 0.0159 = 0.0323 ရပါတယ်။
Raw score စကေး တူတယ်လို့ မယူဆဘဲ rank ချည်း ပေါင်းတာမို့ စကေး မတူတဲ့ retriever တွေကို တွဲလို့ ရပါတယ်။

### Reranker

Reranker ဆိုတာ query နဲ့ candidate တစ်ခုချင်းစီကို ပိုကြွယ်ဝတဲ့ နှိုင်းယှဉ်မှုနဲ့ ပြန်အမှတ်ပေးပြီး candidate set သေးသေးကို ပြန်စီတဲ့ ဒုတိယအဆင့် model ဖြစ်ပါတယ်။
ဥပမာ hybrid search က candidate 50 ခု ပေးလာရင် cross-encoder က အဲဒီ 50 ခုကို အမှတ်ပေးပြီး ထိပ်ဆုံး 5 ခုသာ generation ဆီ ပို့ပါတယ်။
Reranker က corpus တစ်ခုလုံး ရှာတာ မဟုတ်ပါဘူး — retrieval ရှာပြီးသား candidate တွေကိုသာ ပြန်စီပါတယ်။

## ၄။ အထောက်အထားကို model ထံ ပေးအပ်ခြင်း

### RAG (Retrieval-Augmented Generation)

RAG (Retrieval-Augmented Generation) ဆိုတာ တောင်းဆိုချက်နဲ့ သက်ဆိုင်တဲ့ အထောက်အထား ရှာပြီး ရွေးထားတဲ့ အကြောင်းအရာကို model မဖြေမီ ပေးအပ်တဲ့ စနစ် ပုံစံ ဖြစ်ပါတယ်။
ဥပမာ မေးခွန်းတစ်ခုအတွက် chunk 5 ခု ရှာပြီး prompt ထဲ ထည့်ကာ ဖြေခိုင်းရင် အဖြေက အဲဒီ chunk ၅ ခုအပေါ် အခြေခံပြီး ထွက်လာပါတယ်။
Model weight မ ပြင်ဘဲ knowledge အသစ် ထည့်လို့ ရပေမယ့် retrieval နဲ့ grounding ကို သီးခြား စစ်ရပါတယ်။

### Grounding

Grounding ဆိုတာ generate လုပ်ထားတဲ့ အဖြေ သို့မဟုတ် လုပ်ဆောင်မှုကို စနစ်က စစ်လို့ ရတဲ့ အထောက်အထား၊ state သို့မဟုတ် observation တွေနဲ့ ချိတ်ဆက်ပေးတာကို ဆိုလိုပါတယ်။
ဥပမာ policy အပိုင်း ၁ ခု ရှာပြီး အဖြေတိုင်း အဲဒါကို ကိုးကားခိုင်းရင် ကိုးကား မရှိတဲ့ စာကြောင်း 3 ခုကို ပယ်လို့ ရပါတယ်။
Prompt ထဲ document ထည့်လိုက်ရုံနဲ့ grounded ဖြစ်လာတာ မဟုတ်ပါဘူး — model က ထည့်ထားတာကို မှန်မှန် သုံး မသုံး စစ်ရပါတယ်။

## မှီခိုသည့် ဖိုင်

- term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် source အပါ) — [`../../terms/04_retrieval_and_generation.md`](../../terms/04_retrieval_and_generation.md)
