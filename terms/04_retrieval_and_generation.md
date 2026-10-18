# Retrieval & Generation (04) — ရှာဖွေခြင်းနှင့် ဖန်တီးခြင်း

ဤဖိုင်သည် လေ့လာနယ်ပယ် **04 — Retrieval & generation** ၏ term **၁၄** ခုကို အင်္ဂလိပ် + မြန်မာ နှစ်ဘာသာဖြင့်
စုစည်းထားသည့် ကိုးကား ဖြစ်သည်။ ဤနယ်ပယ်သည် model တစ်ခုကို ပြင်ပမှ သိရှိထားသည့် အချက်အလက်ဖြင့်
ဖြည့်စွက် အဖြေထုတ်စေသည့် လုပ်ငန်းစဉ် တစ်ခုလုံးကို ဖုံးလွှမ်းသည် — document များကို ရှာဖွေနိုင်သည့် ယူနစ်
များအဖြစ် ခွဲခြားခြင်း၊ ထို ယူနစ်များကို vector အဖြစ် ကိုယ်စားပြု၍ index တည်ဆောက်ခြင်း၊ query နှင့်
သက်ဆိုင်သည့် အထောက်အထားကို ရှာဖွေခြင်း၊ ထို အထောက်အထားကို ပြန်စီ၍ ရွေးချယ်ခြင်း၊ နောက်ဆုံးတွင်
ရွေးချယ်ထားသည့် အကြောင်းအရာကို generative model ထံ ပေးအပ်ခြင်း ဖြစ်သည်။

ဤ term များကို လေးအုပ်စု အဖြစ် ဖတ်နိုင်သည်။ ပထမ အုပ်စုသည် ရှာဖွေမှု အခြေခံ နည်းလမ်းများ —
Semantic Search၊ Dense Retrieval၊ BM25 နှင့် Hybrid Retrieval — ဖြစ်ပြီး၊ ရှာဖွေမှုသည် စကားလုံး တိုက်ရိုက်
ကိုက်ညီမှုအပေါ် အခြေခံသည် သို့မဟုတ် အဓိပ္ပာယ် (semantic) အပေါ် အခြေခံသည် ကို ခွဲခြား ဖော်ပြသည်။
ဒုတိယ အုပ်စုသည် index နှင့် သိုလှောင်မှု — Vector Database၊ HNSW နှင့် Approximate Nearest Neighbor (ANN) —
ဖြစ်ပြီး၊ vector များကို မည်သို့ သိမ်းဆည်း၍ လျင်မြန်စွာ ရှာဖွေမည်ကို ဖော်ပြသည်။ တတိယ အုပ်စုသည်
အစဉ်သတ်မှတ်မှုနှင့် အကဲဖြတ်မှု — Reranker၊ Reciprocal Rank Fusion (RRF)၊ Maximum Marginal Relevance (MMR)
နှင့် Recall@K — ဖြစ်ပြီး၊ ရှာဖွေမှု ရလဒ်များကို ပေါင်းစပ်၍ ပြန်စီခြင်းနှင့် ထို ရလဒ် အရည်အသွေးကို
တိုင်းတာခြင်း ဖြစ်သည်။ စတုတ္ထ အုပ်စုသည် စနစ် ပုံစံ — Chunking၊ RAG နှင့် Grounding — ဖြစ်ပြီး၊
အစိတ်အပိုင်း အားလုံးကို အဖြေ ထုတ်လုပ်သည့် လုပ်ငန်းစဉ် တစ်ခုအဖြစ် စုစည်းသည်။

entry တိုင်းကို အောက်ပါအတိုင်း ဖတ်ရမည် — **မြန်မာ** တွင် term ၏ မြန်မာ အမည် သို့မဟုတ် အနီးစပ်ဆုံး
ဖော်ပြချက်၊ **ဆိုလိုသည့် အဓိပ္ပာယ်** တွင် အင်ဂျင်နီယာ အသုံးအနှုန်းအရ တကယ် ဆိုလိုသည့် အဓိပ္ပာယ်၊
**အရေးပါသည့် အကြောင်းရင်း** တွင် မည်သည့် စနစ်တွင် မည်သို့ သက်ရောက်သည်၊ **မကြာခဏ ရောထွေးမှု**
နှင့် **လက်တွေ့** တွင် အလွယ်တကူ မှားတတ်သည့် အချက်နှင့် လက်တွေ့ လုပ်ဆောင်ရမည့် အချက်၊
**ဆက်စပ် term များ** တွင် နောက်တစ်ဆင့် ဖတ်ရမည့် term များ၊ **English (source)** တွင် source ၏ မူရင်း
အင်္ဂလိပ် စာသား byte တူညီစွာ ပါဝင်သည်။ source တွင် အချက်အလက် မပါသော field (confusion၊
practice၊ learn) များကို ချန်လှပ်ထားသည်။ နည်းပညာ အသုံးအနှုန်းများ (embedding၊ vector search၊ ANN၊
chunking၊ reranking၊ RAG၊ recall@k၊ hybrid search …) ကို မြန်မာ စာကြောင်းအတွင်း အင်္ဂလိပ်အတိုင်း
ထားရှိသည်။

### Approximate Nearest Neighbor (ANN)

**မြန်မာ:** Approximate Nearest Neighbor (ANN — အနီးစပ်ဆုံး အိမ်နီးချင်း ခန့်မှန်း ရှာဖွေခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** query ကို သိမ်းဆည်းထားသည့် vector တိုင်းနှင့် အပြည့်အစုံ နှိုင်းယှဉ်ခြင်း မပြုဘဲ၊ query နှင့် အနီးစပ်ဆုံး ဖြစ်နိုင်သည့် vector များထဲတွင် ပါဝင်နိုင်ခြေ မြင့်သည့် vector များကို ပြန်လည် ပေးအပ်သည့် ရှာဖွေမှု နည်းလမ်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** approximation သည် vector index ကြီးများကို လက်တွေ့ အသုံးပြုနိုင်စေသည်၊ သို့သော် ရှာဖွေမှု အမြန်နှုန်း၊ memory နှင့် retrieval recall အကြား တိုင်းတာနိုင်သည့် လဲလှယ်မှု (tradeoff) ကို ဖြစ်ပေါ်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** ANN သည် ရှာဖွေမှု ရည်မှန်းချက်နှင့် လဲလှယ်မှုကို ဖော်ပြသည်၊ သို့သော် HNSW သည် ၎င်းကို အကောင်အထည်ဖော်နိုင်သည့် index algorithm တစ်ခု ဖြစ်သည်။
- **လက်တွေ့:** သီးသန့်ဖယ်ထားသည့် (held-out) query set တစ်ခုအပေါ် index နှင့် search parameter များကို tune လုပ်ပါ၊ ထို့နောက် true neighbor တိုင်း တွေ့ရှိသည်ဟု ယူဆခြင်းအစား latency ကို Recall@K နှင့်တကွ တင်ပြပါ။
- **ဆက်စပ် term များ:** Vector Database, HNSW, Cosine Similarity, Recall@K
- **English (source):** A search method that returns vectors likely to be among the nearest to a query without exhaustively comparing the query with every stored vector. Approximation makes large vector indexes practical, but it introduces a measurable tradeoff between search speed, memory, and retrieval recall.

### BM25

**မြန်မာ:** BM25 (lexical ranking function)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** query term များ ကိုက်ညီမှုမှ document တစ်ခုကို အမှတ်ပေးသည့် lexical ranking function ဖြစ်ပြီး၊ term ၏ ရှားပါးမှု၊ ထပ်ခါတလဲလဲ ပါဝင်မှုနှင့် document အရှည်တို့ကို ထည့်သွင်း စဉ်းစားသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် ခိုင်မာသည့် exact-term retrieval baseline ဖြစ်ပြီး၊ identifier၊ ရှားပါးသည့် စကားလုံးနှင့် domain-specific phrase များအတွက် dense retrieval ကို ဖြည့်စွက်ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** BM25 သည် semantic similarity ကို တိုက်ရိုက် နားလည်သည်မဟုတ်ဘဲ၊ ၎င်း၏ အမှတ်သည် query အမျိုးမျိုး သို့မဟုတ် index configuration အမျိုးမျိုးအကြား တစ်သမတ်တည်း အဓိပ္ပာယ် မရှိပါ။
- **လက်တွေ့:** BM25 နှင့် dense search ဖြင့် candidate များ ရှာဖွေပါ၊ ၎င်းတို့၏ rank များကို ပေါင်းစပ်ပါ၊ ထို့နောက် ပိုကုန်ကျသည့် reranker တစ်ခု မထည့်မီ ပေါင်းစပ်ထားသည့် ရလဒ်များကို အကဲဖြတ်ပါ။
- **ဆက်စပ် term များ:** Hybrid Retrieval, Dense Retrieval, Reranker, RAG (Retrieval-Augmented Generation)
- **English (source):** A lexical ranking function that scores a document from query-term matches while accounting for term rarity, repeated occurrences, and document length. It is a strong exact-term retrieval baseline and complements dense retrieval for identifiers, rare words, and domain-specific phrases.

### Chunking

**မြန်မာ:** Chunking (document များကို အပိုင်းအစများ ခွဲခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** index မပြုမီ source material ကို ရှာဖွေနိုင်သည့် ယူနစ်များအဖြစ် ခွဲခြားခြင်း ဖြစ်သည်။ chunk နယ်နိမိတ်၊ overlap၊ metadata နှင့် document တည်ဆောက်ပုံတို့က retrieval သည် prompt ကို အလွန်အကျွံ ဖြည့်တင်းခြင်း မရှိဘဲ လုံလောက်သည့် context ကို ပြန်ပေးနိုင်ခြင်း ရှိ/မရှိကို ဆုံးဖြတ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** မှန်ကန်သည့် chunking strategy သည် document ပုံစံ၊ query အမျိုးအစား၊ embedding model နှင့် evaluation ရလဒ်များအပေါ် မူတည်သည်။ အားလုံးအတွက် သက်ဆိုင်သည့် token အရွယ်အစား သို့မဟုတ် overlap ရာခိုင်နှုန်း မရှိပါ။
- **လက်တွေ့:** heading နှင့် code block များကို မပျက်စီးစေဘဲ ထိန်းသိမ်းပါ၊ source metadata ကို ပူးတွဲထည့်ပါ၊ ထို့နောက် အရွယ်အစား tune မလုပ်မီ တကယ့် မေးခွန်းများအပေါ် retrieval အရည်အသွေးကို တိုင်းတာပါ။
- **ဆက်စပ် term များ:** RAG (Retrieval-Augmented Generation), Reranker, Grounding
- **English (source):** Dividing source material into retrievable units before indexing. Chunk boundaries, overlap, metadata, and document structure determine whether retrieval returns enough context without flooding the prompt. The right chunking strategy depends on document shape, query type, embedding model, and evaluation results. There is no universal token size or overlap percentage.

### Dense Retrieval

**မြန်မာ:** Dense Retrieval (vector အခြေခံ ရှာဖွေခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** query များနှင့် candidate များကို vector representation များအဖြစ် embed လုပ်ပြီး၊ candidate များကို similarity function တစ်ခုဖြင့် အစဉ်သတ်မှတ်သည့် ပထမအဆင့် retrieval ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် တူညီသည့် စကားလုံး အနည်းငယ်သာ မျှဝေသည့် paraphrase များနှင့် semantic ကိုက်ညီမှုများကို ရှာဖွေနိုင်သဖြင့် BM25 ကဲ့သို့ lexical နည်းလမ်းများကို ဖြည့်စွက်ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** Dense retrieval သည် reranker မဟုတ်ပါ။ ၎င်းသည် collection တစ်ခုလုံးကို ရှာဖွေသည်၊ reranker သည် ပိုသေးငယ်သည့် candidate set တစ်ခုကို ပြန်စီပေးသည်။
- **လက်တွေ့:** domain အတွက် embedding model ကို train လုပ်ပါ သို့မဟုတ် ရွေးချယ်ပါ၊ candidate vector များကို index လုပ်ပါ၊ ရလဒ်များကို generation နှင့် ချိတ်ဆက်မီ retrieval recall ကို အကဲဖြတ်ပါ။
- **ဆက်စပ် term များ:** Embedding, Semantic Search, BM25, Hybrid Retrieval
- **English (source):** First-stage retrieval that embeds queries and candidates into vector representations and ranks candidates by a similarity function. It can retrieve paraphrases and semantic matches that share few exact words, complementing lexical methods such as BM25.

### Grounding

**မြန်မာ:** Grounding (အထောက်အထားအပေါ် အခြေခံစေခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** generate လုပ်ထားသည့် အဖြေ သို့မဟုတ် လုပ်ဆောင်မှုကို စနစ်က ဖော်ထုတ်၍ စစ်ဆေးနိုင်သည့် အထောက်အထား၊ state သို့မဟုတ် observation များနှင့် ချိတ်ဆက်ပေးခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** grounding သည် စနစ်အား ကန့်သတ်မှု မရှိသည့် generation ထက် လွန်သည့် အခြေခံ တစ်ခုကို ပေးပြီး၊ အထောက်အထား မရှိသည့် အဆိုများကို ဖော်ထုတ်ရ ပိုလွယ်ကူစေသည်။
- **မကြာခဏ ရောထွေးမှု:** prompt ထဲသို့ document များ ထည့်ခြင်းသည် grounding အတွက် အခွင့်အလမ်း တစ်ခု ဖန်တီးပေးသည်။ သို့သော် model က ၎င်းတို့ကို မှန်ကန်စွာ အသုံးပြုမည်ဟု အာမမခံပါ။
- **လက်တွေ့:** policy အပိုင်း တစ်ခုကို ရှာဖွေပါ၊ အဖြေက ၎င်းကို ကိုးကားရန် တောင်းဆိုပါ၊ ကိုးကားထားသည့် အပိုင်းက မထောက်ခံသည့် အဆိုများကို ပယ်ချပါ။
- **ဆက်စပ် term များ:** RAG (Retrieval-Augmented Generation), Hallucination, Verification Gate, Reranker
- **Learn it:** [Retrieval-Augmented Generation](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/06-rag/)
- **English (source):** Connecting a generated answer or action to evidence, state, or observations that the system can identify and check. Grounding gives the system a basis beyond unconstrained generation and makes unsupported claims easier to detect.

### HNSW

**မြန်မာ:** HNSW (Hierarchical Navigable Small World — အလွှာလိုက် proximity graph index)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** vector များကို အလွှာလိုက် proximity graph များတွင် စီစဉ်ပြီး၊ ကြမ်းတမ်းသည့် အထက်လွှာများမှ အသေးစိတ် အောက်လွှာများဆီသို့ ရှာဖွေသည့် approximate-nearest-neighbor index တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အပြည့်အစုံ နှိုင်းယှဉ်ခြင်း အလွန်နှေးသည့် အတိုင်းအတာများတွင် recall မြင့်သည့် vector search ကို လက်တွေ့ အသုံးပြုနိုင်စေသည့် အသုံးများသည့် နည်းလမ်း ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** HNSW သည် index algorithm တစ်ခု ဖြစ်သည်၊ similarity metric၊ embedding model သို့မဟုတ် အပြည့်အစုံ vector database မဟုတ်ပါ။
- **လက်တွေ့:** latency၊ memory နှင့် Recall@K ရည်မှန်းချက်များအပေါ် construction နှင့် query parameter များကို tune လုပ်ပါ၊ ထို့နောက် embedding version များ ပြောင်းလဲသည့်အခါ index ကို ပြန်လည် တည်ဆောက်ပါ။
- **ဆက်စပ် term များ:** Approximate Nearest Neighbor (ANN), Vector Database, Embedding, Recall@K
- **English (source):** An approximate-nearest-neighbor index that organizes vectors in layered proximity graphs and searches from coarse upper layers toward detailed lower layers. It is a common way to make high-recall vector search practical at scales where exhaustive comparison is too slow.

### Hybrid Retrieval

**မြန်မာ:** Hybrid Retrieval (နည်းလမ်း ရောစပ် ရှာဖွေခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** နည်းလမ်း အမျိုးမျိုးမှ signal များကို — အများအားဖြင့် lexical matching နှင့် dense-vector similarity — ရလဒ်များကို ပေါင်းစပ်ခြင်း သို့မဟုတ် ပြန်စီခြင်း မပြုမီ ပေါင်းစပ်အသုံးပြုသည့် retrieval ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** exact identifier၊ ရှားပါးသည့် term နှင့် semantic paraphrase များသည် မတူညီစွာ အပြုအမူ ရှိသဖြင့် retrieval signal တစ်ခုတည်းဖြင့် အသုံးဝင်သည့် အထောက်အထားကို လွတ်သွားနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Hybrid retrieval သည် candidate signal များကို ပေါင်းစပ်သည်။ reranker သည် ရှာဖွေပြီးသား candidate များအပေါ် ဒုတိယ relevance model တစ်ခုကို အသုံးချသည်။
- **လက်တွေ့:** BM25 ပုံစံ keyword search နှင့် embedding နှစ်မျိုးလုံးဖြင့် candidate များ ရှာဖွေပါ၊ ၎င်းတို့၏ rank များကို ပေါင်းစပ်ပါ၊ ထို့နောက် အသုံးပြုသူ၏ query အတွက် ပေါင်းစပ်ထားသည့် set ကို ပြန်စီပါ။
- **ဆက်စပ် term များ:** Semantic Search, Reranker, RAG (Retrieval-Augmented Generation), Embedding
- **Learn it:** [Advanced RAG](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/07-advanced-rag/)
- **English (source):** Retrieval that combines signals from different methods, commonly lexical matching and dense-vector similarity, before merging or reranking results. Exact identifiers, rare terms, and semantic paraphrases behave differently, so one retrieval signal can miss useful evidence.

### Maximum Marginal Relevance (MMR)

**မြန်မာ:** Maximum Marginal Relevance (MMR — သက်ဆိုင်မှုနှင့် အသစ်အဆန်းမှု မျှတစေသည့် ရွေးချယ်မှု)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** query နှင့် သက်ဆိုင်မှုနှင့် ရွေးချယ်ပြီးသား item များနှင့် နှိုင်းယှဉ်သည့် အသစ်အဆန်းမှု (novelty) ကို မျှတစေသည့် ရွေးချယ်မှု စည်းမျဉ်း တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ထပ်နေသည့် chunk များကို လျှော့ချနိုင်သဖြင့် ကန့်သတ်ထားသည့် context ဘတ်ဂျက်တစ်ခုသည် ပိုမို ကွဲပြားသည့် အထောက်အထားများကို လွှမ်းခြုံနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** MMR သည် ရှိပြီးသား candidate set တစ်ခုကို ကွဲပြားစေသည်၊ လွတ်နေသည့် အထောက်အထားကို ရှာဖွေပေးခြင်း သို့မဟုတ် ရွေးချယ်ထားသည့် အပိုင်းများ မှန်ကန်သည်ကို သက်သေပြခြင်း မပြုပါ။
- **လက်တွေ့:** candidate pool တစ်ခု ရှာဖွေပါ၊ မှတ်တမ်းတင်ထားသည့် relevance-diversity အလေးချိန်တစ်ခုဖြင့် နောက် item ကို ရွေးချယ်ပါ၊ ထို့နောက် အဖြေ အရည်အသွေးနှင့် source လွှမ်းခြုံမှု နှစ်မျိုးလုံးကို အကဲဖြတ်ပါ။
- **ဆက်စပ် term များ:** Reranker, Chunking, RAG (Retrieval-Augmented Generation), Grounding
- **English (source):** A selection rule that balances relevance to the query with novelty relative to items already selected. It can reduce redundant chunks so a limited context budget covers more distinct evidence.

### RAG (Retrieval-Augmented Generation)

**မြန်မာ:** RAG (Retrieval-Augmented Generation — ရှာဖွေမှုဖြင့် ဖြည့်စွက် ဖန်တီးခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** တောင်းဆိုချက်တစ်ခုနှင့် သက်ဆိုင်သည့် အထောက်အထားကို ရှာဖွေပြီး၊ ရွေးချယ်ထားသည့် အကြောင်းအရာကို generative model သို့ ၎င်းက ဖြေကြားခြင်း သို့မဟုတ် လုပ်ဆောင်ခြင်း မပြုမီ ပေးအပ်သည့် စနစ် ပုံစံ (system pattern) ဖြစ်သည်။ retrieval သည် lexical၊ vector၊ structured သို့မဟုတ် hybrid နည်းလမ်းများကို အသုံးပြုနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** RAG သည် လက်ရှိ သို့မဟုတ် သီးသန့် အထောက်အထားကို model weight များထဲ ထည့်သွင်းခြင်း မရှိဘဲ အသုံးပြုနိုင်စေသည်၊ သို့သော် retrieval နှင့် grounding ကို သီးခြားစီ အကဲဖြတ်ရမည် ဖြစ်သည်။
- **ဆက်စပ် term များ:** Grounding, Hybrid Retrieval, Reranker, Hallucination
- **Learn it:** [Retrieval-Augmented Generation](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/06-rag/)
- **English (source):** A system pattern that retrieves evidence relevant to a request and supplies selected content to a generative model before it answers or acts. Retrieval can use lexical, vector, structured, or hybrid methods. RAG can make current or private evidence available without encoding it into model weights, but retrieval and grounding must be evaluated separately.

### Recall@K

**မြန်မာ:** Recall@K (ထိပ်ဆုံး K အတွင်း ပြန်လည် ရရှိမှု အချိုး)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** query တစ်ခုအတွက် Recall@K သည် `|relevant items intersecting the top k| / |relevant items|` ဖြစ်သည်။ dataset အမှတ် တစ်ခုသည် ဖော်ပြထားသည့် စည်းမျဉ်း တစ်ခုအောက်တွင် ထို per-query တန်ဖိုးများကို စုစည်းပေးသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် retrieval အဆင့်တစ်ခုက downstream generation သို့မဟုတ် reranking အတွက် သက်ဆိုင်သည့် candidate များ လုံလောက်စွာ ပေးနိုင်ခြင်း ရှိ/မရှိကို ပြောပြသည်။
- **မကြာခဏ ရောထွေးမှု:** Recall@K မြင့်ခြင်းသည် ထိပ်ဆုံး ရလဒ် ကောင်းသည်ဟု လည်းကောင်း၊ ranking ကောင်းစွာ အစဉ်သတ်မှတ်ထားသည်ဟု လည်းကောင်း၊ နောက်ဆုံး အဖြေ grounded ဖြစ်သည်ဟု လည်းကောင်း မဆိုလိုပါ။ သက်ဆိုင်သည့် item မရှိသည့် query များအတွက် denominator သုည ဖြစ်သဖြင့် ရှင်းလင်းသည့် ဖယ်ထုတ်မှု သို့မဟုတ် တန်ဖိုး သတ်မှတ်မှု မူဝါဒ တစ်ခု လိုအပ်သည်။
- **လက်တွေ့:** relevance judgment များ၊ k၊ aggregation နည်းလမ်းနှင့် သက်ဆိုင်သည့် item မသတ်မှတ်ထားသည့် query များအတွက် မူဝါဒ တစ်ခုကို သတ်မှတ်ပါ၊ ထို့နောက် အထောက်အထား တစ်ခုမျှ ပြန်မရသည့် query များကို စစ်ဆေးပါ။
- **ဆက်စပ် term များ:** Precision & Recall, Eval Set, Reranker, Approximate Nearest Neighbor (ANN)
- **English (source):** For one query, Recall@K is `|relevant items intersecting the top k| / |relevant items|`. A dataset score aggregates those per-query values under a stated rule. It tells you whether a retrieval stage supplies downstream generation or reranking with enough relevant candidates.

### Reciprocal Rank Fusion (RRF)

**မြန်မာ:** Reciprocal Rank Fusion (RRF — rank အပြန်အလှန် ပေါင်းစပ်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** result list အများအပြားကို ပေါင်းစပ်သည့် rank-fusion နည်းလမ်း တစ်ခု ဖြစ်ပြီး၊ list တစ်ခုချင်းစီတွင် item တစ်ခု၏ rank နှင့်အမျှ လျော့နည်းသွားသည့် ပါဝင်မှုများကို ပေါင်းခြင်းဖြင့် ပေါင်းစပ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် lexical၊ dense သို့မဟုတ် multi-query ranking များကို ၎င်းတို့၏ raw score များသည် တူညီသည့် စကေး (scale) ရှိသည်ဟု ယူဆခြင်း မရှိဘဲ ပေါင်းစပ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** RRF သည် rank များကို ပေါင်းစပ်သည်၊ embedding များ သို့မဟုတ် relevance score များကို မဟုတ်ပါ၊ ၎င်းသည် input list အားလုံးတွင် မပါဝင်သည့် item တစ်ခုကို ပြန်လည် ရယူနိုင်ခြင်း မရှိပါ။
- **လက်တွေ့:** သီးခြားလွတ်လပ်သည့် candidate list များ ရှာဖွေပါ၊ တည်ငြိမ်သည့် document identity ဖြင့် ထပ်နေမှုကို ဖယ်ရှားပါ၊ version သတ်မှတ်ထားသည့် fusion constant တစ်ခုကို အသုံးချပါ၊ ထို့နောက် retriever တစ်ခုချင်းစီနှင့် နှိုင်းယှဉ် အကဲဖြတ်ပါ။
- **ဆက်စပ် term များ:** Hybrid Retrieval, BM25, Dense Retrieval, Reranker
- **English (source):** A rank-fusion method that combines several result lists by summing contributions that decrease with each item's rank in each list. It can merge lexical, dense, or multi-query rankings without assuming their raw scores share the same scale.

### Reranker

**မြန်မာ:** Reranker (ရလဒ်များကို ပြန်စီသည့် ဒုတိယအဆင့် model)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** query နှင့် candidate တစ်ခုချင်းစီအကြား ပိုကြွယ်ဝသည့် နှိုင်းယှဉ်မှုကို အသုံးပြု၍ candidate set သေးငယ်တစ်ခုကို ပြန်စီပေးသည့် ဒုတိယအဆင့် model သို့မဟုတ် scoring function ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** လျင်မြန်သည့် ပထမအဆင့် retrieval သည် candidate လွှမ်းခြုံမှုကို အမြင့်ဆုံး ဖြစ်စေပြီး၊ reranking သည် ကန့်သတ်ထားသည့် context window သို့ မည်သည့် အထောက်အထား ရောက်ရှိမည်ကို တိုးတက်စေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** reranker သည် corpus တစ်ခုလုံးကို ရှာဖွေသည်မဟုတ်ပါ။ retrieval က ရှာဖွေပြီးသား candidate များကိုသာ ပြန်စီပေးသည်။
- **လက်တွေ့:** hybrid search ဖြင့် candidate ၅၀ ရှာဖွေပါ၊ query-document pair တိုင်းကို cross-encoder ဖြင့် အမှတ်ပေးပါ၊ ထို့နောက် ထောက်ခံထားသည့် chunk ထိပ်ဆုံး ၅ ခုကို generation သို့ ပေးအပ်ပါ။
- **ဆက်စပ် term များ:** Hybrid Retrieval, Semantic Search, RAG (Retrieval-Augmented Generation)
- **English (source):** A second-stage model or scoring function that reorders a small candidate set using a richer comparison between the query and each candidate. Fast first-stage retrieval maximizes candidate coverage, while reranking can improve which evidence reaches the limited context window.

### Semantic Search

**မြန်မာ:** Semantic Search (အဓိပ္ပာယ်အလိုက် ရှာဖွေခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** query နှင့် candidate များကို embedding space တစ်ခုအတွင်း ကိုယ်စားပြုပြီး၊ vector-similarity function တစ်ခုကို အသုံးပြု၍ candidate များကို အစဉ်သတ်မှတ်သည့် retrieval ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် paraphrase များနှင့် အယူအဆအရ ဆက်စပ်သည့် စာသားများကို ရှာဖွေနိုင်သည်၊ သို့သော် exact identifier နှင့် ရှားပါးသည့် string များအတွက် lexical search ကို အသုံးပြုရန် လိုအပ်ဆဲ ဖြစ်နိုင်သည်။
- **ဆက်စပ် term များ:** Embedding, Hybrid Retrieval, Vector Database, Reranker
- **English (source):** Retrieval that represents a query and candidates in an embedding space and ranks candidates using a vector-similarity function. It can retrieve paraphrases and conceptually related text, but exact identifiers and rare strings may still need lexical search.

### Vector Database

**မြန်မာ:** Vector Database (vector များအတွက် သိုလှောင်မှုနှင့် ရှာဖွေမှု စနစ်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** vector representation များအပေါ် nearest-neighbor query များကို ပံ့ပိုးသည့် storage နှင့် indexing စနစ် ဖြစ်ပြီး၊ များသောအားဖြင့် metadata filtering၊ persistence နှင့် approximate index များ ပါဝင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် vector များကို သိမ်းဆည်းပြီး ရှာဖွေပေးသည့် အခန်းကဏ္ဍကို ထမ်းဆောင်သဖြင့် dense retrieval လုပ်ငန်းစဉ်တွင် index အလွှာအဖြစ် တည်ရှိသည်။
- **မကြာခဏ ရောထွေးမှု:** vector database သည် vector များကို သိမ်းဆည်းပြီး ရှာဖွေသည်။ ၎င်းသည် အရည်အသွေးမြင့် embedding များကို ဖန်တီးပေးခြင်း သို့မဟုတ် သက်ဆိုင်သည့် retrieval ကို အာမခံခြင်း မပြုပါ။
- **ဆက်စပ် term များ:** Embedding, Semantic Search, Hybrid Retrieval
- **English (source):** A storage and indexing system that supports nearest-neighbor queries over vector representations, often with metadata filtering, persistence, and approximate indexes.

## Self-check

1. ANN နှင့် HNSW တို့၏ ကွာခြားချက်ကား အဘယ်နည်း။
2. Dense retrieval နှင့် reranker တို့၏ တာဝန် ကွာခြားချက်ကား အဘယ်နည်း။
3. BM25 ကဲ့သို့ lexical retrieval ကို dense retrieval နှင့် ပေါင်းစပ်ခြင်းက အဘယ်ကြောင့် အသုံးဝင်သနည်း။
4. Recall@K မြင့်ခြင်းက မည်သည့် အချက်များကို အာမမခံသနည်း။
5. Chunking မဟာဗျူဟာကို မည်သို့ ရွေးချယ် အကဲဖြတ်သနည်း။

<details>
<summary>အဖြေများ</summary>

1. ANN သည် ရှာဖွေမှု ရည်မှန်းချက်နှင့် လဲလှယ်မှုကို ဖော်ပြသည့် ယေဘုယျ အယူအဆ ဖြစ်သည် —
   vector တိုင်းနှင့် အပြည့်အစုံ နှိုင်းယှဉ်ခြင်း မပြုဘဲ အနီးစပ်ဆုံး vector များကို ပြန်ပေးသည်။ HNSW သည် ထို
   ရည်မှန်းချက်ကို အလွှာလိုက် proximity graph ဖြင့် အကောင်အထည်ဖော်သည့် index algorithm တစ်ခု ဖြစ်သည်။
   HNSW သည် ANN ၏ နမူနာ တစ်ခုသာ ဖြစ်ပြီး၊ ANN သည် HNSW တစ်ခုတည်း မဟုတ်ပါ။
2. Dense retrieval သည် collection တစ်ခုလုံးကို ရှာဖွေပြီး candidate များကို ပေးအပ်သည့် ပထမအဆင့်
   retrieval ဖြစ်သည်။ reranker သည် corpus တစ်ခုလုံးကို ရှာဖွေခြင်း မပြုဘဲ retrieval က ရှာဖွေပြီးသား
   candidate set သေးငယ်တစ်ခုကို query နှင့် ပိုကြွယ်ဝသည့် နှိုင်းယှဉ်မှုဖြင့် ပြန်စီပေးသည့် ဒုတိယအဆင့်
   ဖြစ်သည်။
3. exact identifier၊ ရှားပါးသည့် စကားလုံးနှင့် semantic paraphrase များသည် မတူညီစွာ အပြုအမူ ရှိသဖြင့်
   signal တစ်ခုတည်းဖြင့် အသုံးဝင်သည့် အထောက်အထားကို လွတ်သွားနိုင်သည်။ နှစ်မျိုးလုံးမှ candidate များ
   ရှာဖွေပြီး rank များကို ပေါင်းစပ်ခြင်းဖြင့် လွှမ်းခြုံမှုကို တိုးစေသည်။
4. Recall@K မြင့်ခြင်းသည် ထိပ်ဆုံး ရလဒ် ကောင်းခြင်း၊ ranking ကောင်းစွာ အစဉ်သတ်မှတ်ထားခြင်း သို့မဟုတ်
   နောက်ဆုံး အဖြေ grounded ဖြစ်ခြင်းကို အာမမခံပါ။ ထို့အပြင် သက်ဆိုင်သည့် item မရှိသည့် query များတွင်
   denominator သုည ဖြစ်သဖြင့် မူဝါဒ တစ်ခု သတ်မှတ်ရန် လိုအပ်သည်။
5. chunking strategy သည် document ပုံစံ၊ query အမျိုးအစား၊ embedding model နှင့် evaluation ရလဒ်များအပေါ်
   မူတည်သဖြင့်၊ heading နှင့် code block များကို ထိန်းသိမ်း၍ source metadata ပူးတွဲထည့်ပြီး၊ တကယ့်
   မေးခွန်းများအပေါ် retrieval အရည်အသွေးကို တိုင်းတာကာ အရွယ်အစားကို tune လုပ်ရသည်။ အားလုံးအတွက်
   သက်ဆိုင်သည့် token အရွယ်အစား သို့မဟုတ် overlap ရာခိုင်နှုန်း မရှိပါ။

</details>

## References

- Source glossary — https://aiengineeringfromscratch.com/glossary
- Source repository — https://github.com/rohitg00/ai-engineering-from-scratch (MIT license)
- [Efficient and Robust Approximate Nearest Neighbor Search Using HNSW](https://dl.acm.org/doi/10.1109/TPAMI.2018.2889473)
- [The Probabilistic Relevance Framework: BM25 and Beyond](https://doi.org/10.1561/1500000019)
- [Dense Passage Retrieval](https://aclanthology.org/2020.emnlp-main.550/)
- [The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries](https://www.cs.cmu.edu/~jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf)
- [Retrieval-Augmented Generation paper](https://arxiv.org/abs/2005.11401)
- [BEIR](https://openreview.net/forum?id=wCu6T5xFjeJ)
- [Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods](https://dl.acm.org/doi/10.1145/1571941.1572114)
- [Retrieval-Augmented Generation](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/06-rag/)
- [Advanced RAG](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/07-advanced-rag/)
