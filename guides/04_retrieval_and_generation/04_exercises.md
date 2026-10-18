# ၀၄ — လေ့ကျင့်ခန်းများနှင့် အဖြေများ (Retrieval & Generation)

ဤဖိုင်သည် နယ်ပယ် ၀၄ ၏ term ၁၄ ခုကို အသုံးပြု၍ တွက်ချက်ခြင်း၊ ပြဿနာ ရှာဖွေခြင်းနှင့် ဆုံးဖြတ်ချက် ချခြင်း
လေ့ကျင့်ခန်းများကို စုစည်းထားသည်။ အပိုင်း ၁ တွင် အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာ ၄ ခု၊ အပိုင်း ၂ တွင်
တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ အပိုင်း ၃ တွင် ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ အပိုင်း ၄ တွင်
ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း ၂ ခု ပါဝင်သည်။ အပိုင်း ၅ တွင် အဖြေ တိုင်းကို ဖော်မြူလာ၊ တွက်ချက်မှု
အဆင့်ဆင့်၊ ယူဆချက် (assumption) နှင့် အကြောင်းရင်း ရှင်းလင်းချက်နှင့်အတူ ပေးထားသည်။

အပိုင်း ၁ နှင့် အပိုင်း ၅ တွင် ပါဝင်သည့် ကိန်းဂဏန်း တိုင်းသည် Python (standard library သာ) ဖြင့်
အမှန်တကယ် လုပ်ဆောင်ခဲ့သည့် တွက်ချက်မှု၏ output ဖြစ်သည်။ ထို script များသည်
`~/.hermes/profiles/ai-engineer/cache/scratch/glossary_guide_04/` အောက်တွင် ရှိသည် —
`we_1_request_path.py`၊ `we_2_chunking.py`၊ `we_3_index_memory.py`၊ `we_4_rrf_fusion.py`၊
`ex_1_chunk_count.py`၊ `ex_2_embedding_memory.py`၊ `ex_3_recall_at_k.py`၊ `ex_4_topk_topp.py`၊
`ex_5_prompt_tokens_cost.py`၊ `ex_6_ann_parameters.py`၊ `design_1_chunk_size.py`၊ `design_2_rerank_depth.py`။
ဖော်ပြထားသည့် command အတိုင်း run လုပ်ပါက တူညီသည့် output ကို ပြန်လည် ရရှိမည်။ ကိန်းဂဏန်း တိုင်းသည်
ဖော်ပြထားသည့် ယူဆချက် အပေါ် မှီခိုသည်၊ ထို့ကြောင့် ဖော်မြူလာ တစ်ခုစီနှင့်အတူ ၎င်း၏ ယူဆချက်ကို
ဖော်ပြထားသည်။

လေ့ကျင့်ခန်းများကို လက်တွေ့ စမ်းသပ်ရန် `labs/lab_chunking.py`၊ `labs/lab_vector_index.py` နှင့်
`labs/lab_prompt_budget.py` တို့ကို အသုံးပြုနိုင်သည် (`labs/README.md` တွင် run ပုံနှင့် output များ ပါဝင်သည်)။
ဤဖိုင်၏ တွက်ချက်မှုများသည် ထို lab များအပေါ် မှီခိုမှု မရှိပါ။

## ၁။ အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာများ (Worked Examples)

### ဥပမာ ၁ — RAG တောင်းဆိုမှု တစ်ခုလုံး: token ဘတ်ဂျက်၊ latency အစိတ်အပိုင်း နှင့် ကုန်ကျစရိတ်

**ယူဆချက် —** query ၁၈ token။ BM25 မှ candidate ၄၀ ခု၊ dense retrieval မှ candidate ၄၀ ခု ရှာပြီး
document id ဖြင့် ထပ်နေမှု ဖယ်ပြီးနောက် ၆၂ ခု ကျန်သည်။ reranker သည် ၅၀ ခုကို စစ်သည်၊
pair တစ်ခုလျှင် ၃.၅ ms။ `Maximum Marginal Relevance (MMR)` သည် candidate ၁၂ ခုထဲမှ ၆ ခု ရွေးသည်။
chunk တစ်ခုလျှင် ၄၈၀ token။ system prompt ၃၅၀၊ history ၉၀၀၊ user turn ၄၀၊ output အတွက်
ချန်ထားသည့် ၁၀၂၄ token၊ context window ၈၁၉၂။ prefill အမြန်နှုန်း ၄,၅၀၀ token/s၊
decode step တစ်ခု ၁၈ ms၊ output ၇၀၀ token။ input token ခ $0.25 နှင့် output token ခ $1.00 (1M token လျှင်)။

**ဖော်မြူလာ —**
- retrieved token = chunk အရေအတွက် × chunk token
- used = system + retrieved + history + user + reserved_output
- retrieval latency = embed + BM25 + ANN + fusion + rerank + MMR
- cost = used / 10⁶ × price_in + output_tokens / 10⁶ × price_out

**တွက်ချက်မှု —**
1. retrieved = 6 × 480 = 2,880 token ဖြစ်သည်။
2. used = 350 + 2,880 + 900 + 40 + 1,024 = 5,194 token ဖြစ်သည်။
3. headroom = 8,192 − 5,194 = 2,998 token ဖြစ်သည်၊ ဆိုလိုသည်မှာ window ၏ ၃၆.၆ % ကျန်သည်။
4. retrieval latency = 8 + 22 + 6 + 1 + 175 + 4 = 216.0 ms ဖြစ်သည်။
5. prefill = 5,194 / 4,500 × 1,000 = 1,154.2 ms ဖြစ်သည်။
6. decode = 700 × 18 = 12,600 ms ဖြစ်သည်၊ စုစုပေါင်း 13.97 s ဖြစ်သည်။
7. retrieval အဆင့်သည် စုစုပေါင်း၏ ၁.၅၅ % သာ ဖြစ်သည်၊ reranking သည် ၁.၂၅ % ဖြစ်သည်။
8. cost = 5,194 / 10⁶ × 0.25 + 700 / 10⁶ × 1.00 = 0.0012985 + 0.0007 = $0.0019985 ဖြစ်သည်။
9. request ၅၀,၀၀၀ / ရက် ဆိုပါက $99.925 / ရက်၊ ၃၀ ရက်အတွက် $2,997.75 ဖြစ်သည်။
10. chunk ၆ ခုမှ ၄ ခုသို့ လျှော့ပါက $0.0017585 ဖြစ်သည်၊ ရက် တစ်လျှင် $12.00 သက်သာသည်။

**ကောက်ချက် —** ဤ geometry တွင် retrieval နှင့် reranking ကုန်ကျချိန်သည် စုစုပေါင်း latency ၏
၃ % အောက်သာ ဖြစ်သည်၊ သို့သော် retrieved token သည် input ကုန်ကျစရိတ်၏ ၅၅.၄ % ဖြစ်သည်။
ထို့ကြောင့် ဤစနစ်တွင် ကုန်ကျစရိတ် လျှော့ချရန် အကောင်းဆုံး နေရာသည် retrieval latency မဟုတ်ဘဲ
ထည့်သည့် chunk အရေအတွက် ဖြစ်သည်။

```bash
python3 - <<'PY'
query_tokens = 18
bm25_k, dense_k = 40, 40
union = 62
rerank_pool, rerank_ms_per_pair = 50, 3.5
mmr_pool, mmr_keep = 12, 6
chunk_tokens = 480
system, history, user = 350, 900, 40
reserve_output = 1024
window = 8192
retrieved = mmr_keep * chunk_tokens
used = system + retrieved + history + user + reserve_output
print("query tokens        ", query_tokens)
print("candidates bm25     ", bm25_k)
print("candidates dense    ", dense_k)
print("union after dedupe  ", union)
print("rerank pairs        ", rerank_pool, "at", rerank_ms_per_pair, "ms =", rerank_pool * rerank_ms_per_pair, "ms")
print("mmr pool / keep     ", mmr_pool, mmr_keep)
print("retrieved tokens    ", retrieved)
print("used tokens         ", used)
print("window              ", window)
print("headroom tokens     ", window - used)
print("used share pct      ", round(100 * used / window, 1))
print("retrieved share pct ", round(100 * retrieved / window, 1))
embed_ms, ann_ms, bm25_ms, fuse_ms, rerank_ms, mmr_ms = 8.0, 22.0, 6.0, 1.0, rerank_pool * rerank_ms_per_pair, 4.0
retrieval_ms = embed_ms + ann_ms + bm25_ms + fuse_ms + rerank_ms + mmr_ms
prefill_tps, decode_ms, out_tokens = 4500.0, 18.0, 700
prefill_ms = used / prefill_tps * 1000
decode_total = out_tokens * decode_ms
total_ms = retrieval_ms + prefill_ms + decode_total
print("retrieval stage ms  ", round(retrieval_ms, 1))
print("prefill ms          ", round(prefill_ms, 1))
print("decode ms           ", round(decode_total, 1))
print("total s             ", round(total_ms / 1000, 3))
print("retrieval share pct ", round(100 * retrieval_ms / total_ms, 2))
print("rerank share pct    ", round(100 * rerank_ms / total_ms, 2))
without_rerank_ms = retrieval_ms - rerank_ms
print("retrieval ms no rerank", round(without_rerank_ms, 1))
print("retrieval speedup   ", round(retrieval_ms / without_rerank_ms, 2))
price_in, price_out = 0.25, 1.00
cost_in = used / 1e6 * price_in
cost_out = out_tokens / 1e6 * price_out
per_request = cost_in + cost_out
print("cost input USD      ", round(cost_in, 7))
print("cost output USD     ", round(cost_out, 7))
print("cost per request USD", round(per_request, 7))
print("cost if retrieved 4 chunks USD", round((system + 4 * chunk_tokens + history + user + reserve_output) / 1e6 * price_in + cost_out, 7))
rpd = 50000
print("USD per day 50k req ", round(per_request * rpd, 3))
print("USD per 30 days     ", round(per_request * rpd * 30, 2))
print("saving per day 6 -> 4 chunks USD", round(((6 - 4) * chunk_tokens) / 1e6 * price_in * rpd, 3))
PY
```

```text
query tokens         18
candidates bm25      40
candidates dense     40
union after dedupe   62
rerank pairs         50 at 3.5 ms = 175.0 ms
mmr pool / keep      12 6
retrieved tokens     2880
used tokens          5194
window               8192
headroom tokens      2998
used share pct       63.4
retrieved share pct  35.2
retrieval stage ms   216.0
prefill ms           1154.2
decode ms            12600.0
total s              13.97
retrieval share pct  1.55
rerank share pct     1.25
retrieval ms no rerank 41.0
retrieval speedup    5.27
cost input USD       0.0012985
cost output USD      0.0007
cost per request USD 0.0019985
cost if retrieved 4 chunks USD 0.0017585
USD per day 50k req  99.925
USD per 30 days      2997.75
saving per day 6 -> 4 chunks USD 12.0
```

### ဥပမာ ၂ — Chunking: chunk အရေအတွက်၊ overlap ထပ်မှု နှင့် သိမ်းဆည်းမှု အချိုး

**ယူဆချက် —** document ၄၈,၀၀၀ လုံး၊ chunk size ၁,၀၀၀ လုံး။ overlap ၁၅၀ လုံး နှင့် ၃၀၀ လုံး
နှစ်မျိုးကို နှိုင်းယှဉ်သည်။ char ၄ လုံးလျှင် token ၁ ခု အဖြစ် ယူသည်။ နယ်နိမိတ်ကို လုံးအရေအတွက်ဖြင့်
ဖြတ်ပြီး၊ နောက်ဆုံး chunk သည် document ကို လွှမ်းခြုံသည်ဟု ယူသည် (ကျော်လွန်သည့် အပိုင်း ပါဝင်သည်)။

**ဖော်မြူလာ —**
- stride = size − overlap
- chunk အရေအတွက် = ⌈(N − overlap) / stride⌉
- သိမ်းဆည်းသည့် ပမာဏ = chunk အရေအတွက် × size
- duplication ratio = သိမ်းဆည်းသည့် ပမာဏ / N

**တွက်ချက်မှု —**
1. overlap ၁၅၀: stride = ၈၅၀၊ chunk အရေအတွက် = ⌈(48,000 − 150) / 850⌉ = ⌈56.29⌉ = ၅၇ ခု ဖြစ်သည်။
2. သိမ်းဆည်းသည့် ပမာဏ = 57 × 1,000 = ၅၇,၀၀၀ လုံး ဖြစ်သည်၊ ratio ၁.၁၈၇၅၊ ထပ်မှု ၉,၀၀၀ လုံး (၁၈.၇၅ %) ဖြစ်သည်။
3. overlap ၃၀၀: stride = ၇၀၀၊ chunk အရေအတွက် = ⌈(48,000 − 300) / 700⌉ = ⌈68.14⌉ = ၆၉ ခု ဖြစ်သည်။
4. သိမ်းဆည်းသည့် ပမာဏ = ၆၉,၀၀၀ လုံး၊ ratio ၁.၄၃၇၅၊ ထပ်မှု ၂၁,၀၀၀ လုံး (၄၃.၇၅ %) ဖြစ်သည်။
5. chunk အရေအတွက် အချိုး = 69 / 57 = ၁.၂၁၁ ဆ ဖြစ်သည်၊ သို့သော် ထပ်မှု ပမာဏ အချိုး = ၂.၃၃၃ ဆ ဖြစ်သည်။
6. token အလိုက် တွက်ပါက ၁၂,၀၀၀ token document တွင် ၄၀၀/၆၀ ဖြစ်ပါက ၃၆ ခု၊ ၂၀၀/၄၀ ဖြစ်ပါက ၇၅ ခု ဖြစ်သည် —
   chunk အရေအတွက် ၂.၀၈၃ ဆ ဖြစ်သည်။

**ကောက်ချက် —** overlap ကို တိုးသည့်အခါ chunk အရေအတွက်သည် အနည်းငယ်သာ တိုးသော်လည်း
ထပ်နေသည့် ပမာဏသည် အချိုးမကျ တိုးသည်။ ထို့ကြောင့် overlap ကို ဆုံးဖြတ်သည့်အခါ
"chunk ဘယ်နှစ်ခု ဖြစ်မည်" ထက် "token ဘယ်လောက် ထပ်ကုန်မည်" ကို တွက်ရမည်။

```bash
python3 - <<'PY'
import math

def chunks(n, size, overlap):
    stride = size - overlap
    return math.ceil((n - overlap) / stride)

def report(n, size, overlap, label):
    c = chunks(n, size, overlap)
    stored = c * size
    print(label, "size", size, "overlap", overlap, "stride", size - overlap)
    print("  chunks        ", c)
    print("  stored units  ", stored, "of", n, "= ratio", round(stored / n, 4))
    print("  duplicated    ", stored - n, "= pct", round(100 * (stored - n) / n, 2))
    print("  overlap links ", c - 1, "x", overlap, "=", (c - 1) * overlap)
    return c

doc_chars = 48000
c1 = report(doc_chars, 1000, 150, "characters doc")
c2 = report(doc_chars, 1000, 300, "characters doc")
print("chunk count ratio 300 vs 150 overlap", round(c2 / c1, 3))
print("ratio of duplication pct", round((100 * (c2 * 1000 - doc_chars) / doc_chars) / (100 * (c1 * 1000 - doc_chars) / doc_chars), 3))
doc_tokens = 12000
c3 = report(doc_tokens, 400, 60, "tokens doc")
c4 = report(doc_tokens, 400, 120, "tokens doc")
c5 = report(doc_tokens, 200, 40, "tokens doc")
print("embedding calls chars doc  ", c1, "tokens doc", c3)
print("tokens submitted chars doc 4 chars/token", round(c1 * 1000 / 4))
print("overlap share of submitted pct", round(100 * ((c1 - 1) * 150) / (c1 * 1000), 2))
print("smaller chunks at 200/40 tokens ->", c5, "chunks", "vs", c3, "= x", round(c5 / c3, 3))
PY
```

```text
characters doc size 1000 overlap 150 stride 850
  chunks         57
  stored units   57000 of 48000 = ratio 1.1875
  duplicated     9000 = pct 18.75
  overlap links  56 x 150 = 8400
characters doc size 1000 overlap 300 stride 700
  chunks         69
  stored units   69000 of 48000 = ratio 1.4375
  duplicated     21000 = pct 43.75
  overlap links  68 x 300 = 20400
chunk count ratio 300 vs 150 overlap 1.211
ratio of duplication pct 2.333
tokens doc size 400 overlap 60 stride 340
  chunks         36
  stored units   14400 of 12000 = ratio 1.2
  duplicated     2400 = pct 20.0
  overlap links  35 x 60 = 2100
tokens doc size 400 overlap 120 stride 280
  chunks         43
  stored units   17200 of 12000 = ratio 1.4333
  duplicated     5200 = pct 43.33
  overlap links  42 x 120 = 5040
tokens doc size 200 overlap 40 stride 160
  chunks         75
  stored units   15000 of 12000 = ratio 1.25
  duplicated     3000 = pct 25.0
  overlap links  74 x 40 = 2960
embedding calls chars doc   57 tokens doc 36
tokens submitted chars doc 4 chars/token 14250
overlap share of submitted pct 14.74
smaller chunks at 200/40 tokens -> 75 chunks vs 36 = x 2.083
```

### ဥပမာ ၃ — Embedding နှင့် HNSW index memory

**ယူဆချက် —** chunk ၃၀၀,၀၀၀ ခု၊ dimension ၇၆၈၊ fp16 (element တစ်ခုလျှင် ၂ ဘိုက်)။
`HNSW` တွင် `M` = ၁၆ (node တစ်ခုလျှင် အိမ်နီးချင်း အများဆုံး ၁၆ ခု)၊ link id တစ်ခုလျှင် ၄ ဘိုက်၊
အထက်လွှာများအတွက် link ပမာဏ ထပ်တိုးအချိုး ၁.၁၅။ metadata chunk တစ်ခုလျှင် ၂၀၀ ဘိုက်။
brute-force နှိုင်းယှဉ်မှုတွင် dimension တိုင်းအတွက် multiply-add တစ်ကြိမ် လိုသည်ဟု ယူသည်။
HNSW သည် query တစ်ခုလျှင် node ၈၀၀ ခန့် လည်ပတ်သည်ဟု ယူသည်။

**ဖော်မြူလာ —**
- vector bytes = chunk × dimension × bytes-per-element
- link bytes = chunk × M × id bytes × upper-tier factor
- စုစုပေါင်း = vector + link + metadata
- brute-force MACs = chunk × dimension

**တွက်ချက်မှု —**
1. vector = 300,000 × 768 × 2 = 460,800,000 ဘိုက် = ၄၃၉.၄၅ MiB = ၀.၄၂၉ GiB ဖြစ်သည်။
2. fp32 ဖြစ်ပါက ၈၇၈.၉၁ MiB ဖြစ်သည်၊ int8 ဖြစ်ပါက ၂၁၉.၇၃ MiB ဖြစ်သည်။
3. link = 300,000 × 16 × 4 × 1.15 = ၂၂,၀၈၀,၀၀၀ ဘိုက် = ၂၁.၀၆ MiB ဖြစ်သည်။
4. metadata = 300,000 × 200 = ၅၇.၂၂ MiB ဖြစ်သည်။
5. စုစုပေါင်း = ၅၁၇.၇၃ MiB = ၀.၅၀၆ GiB ဖြစ်သည်၊ vector သည် ၈၄.၉ % ဖြစ်သည်။
6. `M` = ၃၂ ဖြစ်ပါက စုစုပေါင်း ၅၃၈.၇၉ MiB ဖြစ်သည်။
7. brute-force = 300,000 × 768 = 230,400,000 MAC = ၀.၂၃ GFLOP ဖြစ်သည်၊ ၅၀ GFLOP/s တွင်
   query တစ်ခုလျှင် ၄.၆၁ ms ဖြစ်သည်။
8. HNSW သည် node ၈၀၀ လည်ပတ်ပါက 800 × 768 = ၆၁၄,၄၀၀ MAC ဖြစ်သည်၊ brute-force ၏ ၀.၂၆၇ % သာ ဖြစ်သည်။

**ကောက်ချက် —** ဤ အတိုင်းအတာတွင် brute-force သည် query တစ်ခုလျှင် ၄.၆ ms ဖြစ်သဖြင့်
အလွန်နှေး မဟုတ်သေးပါ။ သို့သော် chunk အရေအတွက် ဆယ်ဆ တိုးသည့်အခါ latency လည်း ဆယ်ဆ တိုးသည် —
HNSW ၏ တန်ဖိုးသည် ထို နေရာတွင် ပေါ်လာသည်။ memory အပိုင်းတွင် vector ကိုယ်တိုင်က အကြီးဆုံး
ဖြစ်သဖြင့် dimension လျှော့ခြင်း သို့မဟုတ် fp16/int8 သုံးခြင်းသည် link parameter ချိန်ညှခြင်းထက်
အကျိုးသက်ရောက်မှု ပိုကြီးသည်။

```bash
python3 - <<'PY'
n, dim = 300000, 768
fp16, fp32, int8 = 2, 4, 1
vec16 = n * dim * fp16
vec32 = n * dim * fp32
vec8 = n * dim * int8
print("vectors fp16 bytes ", vec16)
print("vectors fp16 MiB   ", round(vec16 / 2**20, 2))
print("vectors fp16 GiB   ", round(vec16 / 2**30, 3))
print("vectors fp32 MiB   ", round(vec32 / 2**20, 2))
print("vectors int8 MiB   ", round(vec8 / 2**20, 2))
print("fp32 / fp16 ratio  ", round(vec32 / vec16, 2))
M, id_bytes, upper = 16, 4, 1.15
links = int(n * M * id_bytes * upper)
print("link bytes         ", links)
print("link MiB           ", round(links / 2**20, 2))
meta = n * 200
print("metadata MiB       ", round(meta / 2**20, 2))
total16 = vec16 + links + meta
print("total fp16 MiB     ", round(total16 / 2**20, 2))
print("total fp16 GiB     ", round(total16 / 2**30, 3))
print("vectors share pct  ", round(100 * vec16 / total16, 1))
print("links share pct    ", round(100 * links / total16, 2))
print("metadata share pct ", round(100 * meta / total16, 2))
macs = n * dim
print("brute force MACs   ", macs, "=", round(macs / 1e9, 3), "GFLOP")
for gflops in (25.0, 50.0, 100.0):
    print("  at", gflops, "GFLOP/s ->", round(macs / 1e9 / gflops * 1000, 2), "ms per query")
visited = 800
print("HNSW visited nodes per query", visited)
print("HNSW distance MACs ", visited * dim, "=", round(visited * dim / macs * 100, 3), "pct of brute force")
print("HNSW MiB at M=32  ", round((n * 32 * id_bytes * upper + vec16 + meta) / 2**20, 2))
PY
```

```text
vectors fp16 bytes  460800000
vectors fp16 MiB    439.45
vectors fp16 GiB    0.429
vectors fp32 MiB    878.91
vectors int8 MiB    219.73
fp32 / fp16 ratio   2.0
link bytes          22080000
link MiB            21.06
metadata MiB        57.22
total fp16 MiB      517.73
total fp16 GiB      0.506
vectors share pct   84.9
links share pct     4.07
metadata share pct  11.05
brute force MACs    230400000 = 0.23 GFLOP
  at 25.0 GFLOP/s -> 9.22 ms per query
  at 50.0 GFLOP/s -> 4.61 ms per query
  at 100.0 GFLOP/s -> 2.3 ms per query
HNSW visited nodes per query 800
HNSW distance MACs  614400 = 0.267 pct of brute force
HNSW MiB at M=32   538.79
```

### ဥပမာ ၄ — Hybrid retrieval: RRF fusion နှင့် recall

**ယူဆချက် —** BM25 စာရင်း = `d7, d3, d1, d9, d4`၊ dense စာရင်း = `d3, d9, d5, d7, d2`။
`RRF` constant k = ၆၀။ သက်ဆိုင်သည့် item အစု = `{d1, d3, d5}`။

**ဖော်မြူလာ —**
- RRF score(d) = Σ (list တိုင်းအတွက်) 1 / (k + rank(d, list))
- Recall@K = |သက်ဆိုင်သည့် item ∩ top K| / |သက်ဆိုင်သည့် item| (source ၏ ဖော်မြူလာအတိုင်း)

**တွက်ချက်မှု —**
1. d3 သည် စာရင်း A တွင် rank ၂၊ စာရင်း B တွင် rank ၁ ဖြစ်သည်၊ ထို့ကြောင့်
   1/62 + 1/61 = 0.016129 + 0.016393 = 0.032522 ဖြစ်သည်။
2. d7 = 1/61 + 1/64 = 0.016393 + 0.015625 = 0.032018 ဖြစ်သည်။
3. d9 = 1/64 + 1/62 = 0.015625 + 0.016129 = 0.031754 ဖြစ်သည်။
4. fused အစဉ် = `d3, d7, d9, d1, d5, d2, d4` ဖြစ်သည်။
5. Recall@3: BM25 = 2/3 (0.667)၊ dense = 2/3 (0.667)၊ fused = 1/3 (0.333) ဖြစ်သည်။
6. Recall@5: BM25 = 2/3၊ dense = 2/3၊ fused = 3/3 = 1.0 ဖြစ်သည်။
7. k ကို ၁ သို့မဟုတ် ၁၀၀၀ သို့ ပြောင်းပါက top-3 အစဉ်သည် မပြောင်းလဲပါ။

**ကောက်ချက် —** fusion သည် ထိပ်ဆုံး သုံးခုတွင် recall ကျဆင်းနိုင်သည်၊ အကြောင်းမှာ
စာရင်း နှစ်ခုလုံးတွင် ပါသည့် item ကို ဆုချသောကြောင့် ဖြစ်သည်။ သို့သော် ကျယ်သည့် K တွင်
fusion သည် single retriever ထက် လွှမ်းခြုံမှု ပိုကောင်းသည် (recall@5 = ၁.၀ နှင့် ၀.၆၆၇)။
ထို့ကြောင့် fusion ကို **candidate လွှမ်းခြုံမှု** အတွက် သုံးပြီး၊ အစဉ်ကောင်းစေရန် ထို စာရင်းကို
`Reranker` ထံ ပေးအပ်ရမည်။

```bash
python3 - <<'PY'
bm25 = ["d7", "d3", "d1", "d9", "d4"]
dense = ["d3", "d9", "d5", "d7", "d2"]
K = 60

def rrf(lists, k=K):
    scores = {}
    for lst in lists:
        for rank, doc in enumerate(lst, start=1):
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda p: (-p[1], p[0]))

fused = rrf([bm25, dense])
print("bm25 list   ", bm25)
print("dense list  ", dense)
print("k constant  ", K)
for doc, s in fused:
    in_a = bm25.index(doc) + 1 if doc in bm25 else None
    in_b = dense.index(doc) + 1 if doc in dense else None
    print(f"  {doc} rank_bm25={in_a} rank_dense={in_b} rrf={s:.6f}")
union = sorted(set(bm25) | set(dense))
print("union size  ", len(union), union)
print("in both lists", sorted(set(bm25) & set(dense)))
print("fused top1  ", fused[0][0], "top3", [d for d, _ in fused[:3]])
only_a = [d for d in bm25 if d not in dense]
print("only in bm25", only_a, "-> still fused:", [d for d in only_a if d in dict(fused)])
print("rrf of single list keeps order  ", [d for d, _ in rrf([bm25])])
print("k=1 top3    ", [d for d, _ in rrf([bm25, dense], 1)[:3]])
print("k=1000 top3 ", [d for d, _ in rrf([bm25, dense], 1000)[:3]])
relevant = {"d1", "d3", "d5"}
for label, lst in (("bm25", bm25), ("dense", dense), ("fused", [d for d, _ in fused])):
    for k in (3, 5):
        hit = len(set(lst[:k]) & relevant)
        print(f"recall@{k} {label:6}", hit, "/", len(relevant), "=", round(hit / len(relevant), 3))
PY
```

```text
bm25 list    ['d7', 'd3', 'd1', 'd9', 'd4']
dense list   ['d3', 'd9', 'd5', 'd7', 'd2']
k constant   60
  d3 rank_bm25=2 rank_dense=1 rrf=0.032522
  d7 rank_bm25=1 rank_dense=4 rrf=0.032018
  d9 rank_bm25=4 rank_dense=2 rrf=0.031754
  d1 rank_bm25=3 rank_dense=None rrf=0.015873
  d5 rank_bm25=None rank_dense=3 rrf=0.015873
  d2 rank_bm25=None rank_dense=5 rrf=0.015385
  d4 rank_bm25=5 rank_dense=None rrf=0.015385
union size   7 ['d1', 'd2', 'd3', 'd4', 'd5', 'd7', 'd9']
in both lists ['d3', 'd7', 'd9']
fused top1   d3 top3 ['d3', 'd7', 'd9']
only in bm25 ['d1', 'd4'] -> still fused: ['d1', 'd4']
rrf of single list keeps order   ['d7', 'd3', 'd1', 'd9', 'd4']
k=1 top3     ['d3', 'd7', 'd9']
k=1000 top3  ['d3', 'd7', 'd9']
recall@3 bm25   2 / 3 = 0.667
recall@5 bm25   2 / 3 = 0.667
recall@3 dense  2 / 3 = 0.667
recall@5 dense  2 / 3 = 0.667
recall@3 fused  1 / 3 = 0.333
recall@5 fused  3 / 3 = 1.0
```

## ၂။ တွက်ချက်ရသည့် လေ့ကျင့်ခန်းများ (Calculation Exercises)

လေ့ကျင့်ခန်း တစ်ခုစီတွင် ကိန်းဂဏန်း အဖြေ အတိအကျ ရှိသည်။ အဖြေ၊ ဖော်မြူလာ နှင့် ယူဆချက်
ရှင်းလင်းချက်ကို အပိုင်း ၅.၁ တွင် ပေးထားသည်။

**လေ့ကျင့်ခန်း ၁ — chunk အရေအတွက်နှင့် overlap**

document ၁၂၀,၀၀၀ လုံး၊ chunk size ၁,၅၀၀ လုံး၊ overlap ၃၀၀ လုံး။ တွက်ရမည့် အချက်များ —
(က) chunk အရေအတွက်နှင့် stride၊ (ခ) သိမ်းဆည်းသည့် ပမာဏနှင့် ထပ်မှု ရာခိုင်နှုန်း၊ (ဂ) overlap ကို ၆၀၀
သို့ တိုးပါက chunk အရေအတွက်နှင့် ratio၊ (ဃ) ထပ်မှု ကုန်ကျစရိတ် အချိုး၊ (င) char ၄ လုံး = token ၁ ခု
ဖြင့် သိမ်းဆည်းသည့် token ပမာဏနှင့် 1M token လျှင် $0.02 ဖြင့် embedding ကုန်ကျစရိတ်။
→ `labs/lab_chunking.py`

**လေ့ကျင့်ခန်း ၂ — embedding storage နှင့် index memory**

chunk ၁,၂၀၀,၀၀၀ ခု၊ dimension ၁,၀၂၄။ တွက်ရမည့် အချက်များ — (က) fp16 နှင့် int8 vector memory
(GiB)၊ (ခ) `M` = ၃၂ တွင် link memory (id ၄ ဘိုက်၊ အထက်လွှာ အချိုး ၁.၁၅)၊ (ဂ) metadata ၁၅၀ ဘိုက်/chunk
နှင့် စုစုပေါင်း GiB၊ (ဃ) အစိတ်အပိုင်း အချိုး ရာခိုင်နှုန်း၊ (င) `M` = ၆၄ ဖြစ်ပါက စုစုပေါင်း၊
(စ) dimension ၃၈၄ ဖြစ်ပါက စုစုပေါင်း၊ (ဆ) brute-force MACs နှင့် ၅၀ နှင့် ၂၀၀ GFLOP/s တွင်
query တစ်ခုလျှင် ms။ → `labs/lab_vector_index.py`

**လေ့ကျင့်ခန်း ၃ — Recall@K**

query ၃ ခု အတွက် relevance judgment များ — q1 သက်ဆိုင်သည့် ၅ ခု၊ top-10 = `d1, d2, d3, d9, d10 …`။
q2 သက်ဆိုင်သည့် ၂ ခု၊ top-10 = `d2, d6, d7 …`။ q3 သက်ဆိုင်သည့် ၈ ခု၊ top-10 = `d1, d2, d9 …`။
q4 တွင် သက်ဆိုင်သည့် item မရှိပါ။ တွက်ရမည့် အချက်များ — (က) query တိုင်း၏ Recall@3၊ Recall@5၊ Recall@10၊
(ခ) q1 အတွက် k တိုးသည့်အခါ recall ပြောင်းလဲမှု၊ (ဂ) macro mean Recall@5 နှင့် Recall@10၊
(ဃ) micro (pooled) recall၊ (င) q4 ကို သုည သတ်မှတ်ပါက နှင့် ဖယ်ထုတ်ပါက mean။ → `labs/lab_vector_index.py`

**လေ့ကျင့်ခန်း ၄ — top-k နှင့် top-p ပုံစံ ဖြတ်တောက်ခြင်း (cosine similarity)**

candidate ၈ ခု၏ cosine similarity = 0.91၊ 0.86၊ 0.84၊ 0.80၊ 0.62၊ 0.58၊ 0.55၊ 0.40။
တွက်ရမည့် အချက်များ — (က) similarity ပေါင်းလဒ်နှင့် normalized အလေးချိန်၊ (ခ) top-k = ၄ ဖြင့်
ဖြတ်ပါက ကျန်သည့် အစု၊ raw ပမာဏ အချိုး နှင့် renormalize ပြီးနောက် တန်ဖိုး၊ (ဂ) normalized အလေးချိန်
အပေါ် top-p = 0.9 ဖြင့် ဖြတ်ပါက ကျန်သည့် အရေအတွက်နှင့် cumulative၊ (ဃ) ဖြတ်လိုက်သည့် mass၊
(င) absolute threshold 0.6 ဖြင့် ဖြတ်ပါက အရေအတွက်၊ (စ) နည်းလမ်း သုံးမျိုး၏ token ဘတ်ဂျက်
(chunk တစ်ခုလျှင် ၄၈၀ token)။ → `labs/lab_prompt_budget.py`

**လေ့ကျင့်ခန်း ၅ — retrieved chunk တိုင်း ထပ်တိုးသည့် token နှင့် ကုန်ကျစရိတ်**

chunk တစ်ခု၏ အကြောင်းအရာ ၅၁၂ token၊ ကိုးကားချက် ခေါင်းစီး ၄၀ token။ system ၄၀၀၊ user ၆၀၊
history ၁,၂၀၀၊ output အတွက် ချန်ထားသည့် ၈၀၀၊ window ၈,၁၉၂၊ output ၆၀၀ token။
input 1M token လျှင် $0.25၊ output 1M token လျှင် $1.00။ တွက်ရမည့် အချက်များ — (က) chunk ၂၊ ၄၊ ၆၊ ၈
ခုအတွက် used token၊ headroom နှင့် window ၏ ရာခိုင်နှုန်း၊ (ခ) window ထဲ ဝင်နိုင်သည့် chunk အများဆုံး
အရေအတွက်၊ (ဂ) request တစ်ခုလျှင် ကုန်ကျစရိတ် နှင့် ၁,၀၀၀ request အတွက်၊ (ဃ) ရက် တစ်လျှင်
၁,၀၀၀ နှင့် ၅၀,၀၀၀ request ဖြစ်ပါက USD၊ (င) chunk ၆ ခုမှ ၄ ခုသို့ လျှော့ပါက သက်သာသည့် ပမာဏ။
→ `labs/lab_prompt_budget.py`

**လေ့ကျင့်ခန်း ၆ — ANN parameter သည် latency နှင့် recall အပေါ် သက်ရောက်မှု**

ယူဆချက် — latency(e) = 0.35 + visited(e) × 0.0009 ms၊ visited(e) = 32 + 6e၊
recall(e) = 1 − exp(−e / 45)။ တွက်ရမည့် အချက်များ — (က) `ef` = ၁၆၊ ၃၂၊ ၆၄၊ ၁၂၈၊ ၂၅၆ အတွက်
latency၊ recall@10 နှင့် per-core query/s၊ (ခ) `ef` = ၁၆ တွင် လွတ်သွားသည့် true neighbor ရာခိုင်နှုန်း၊
(ဂ) `ef` ၃၂ မှ ၆၄ သို့ တိုးပါက recall အကျိုးအမြတ်နှင့် latency ထပ်တိုးမှု၊ (ဃ) `ef` ၁၂၈ မှ ၂၅၆ သို့
တိုးပါက အကျိုးအမြတ်နှင့် ကုန်ကျမှု၊ (င) recall 0.95 ရရန် လိုအပ်သည့် `ef`၊ (စ) `M` = ၁၆၊ ၃၂၊ ၆၄
အတွက် link memory (chunk ၁.၂ သန်း)။ → `labs/lab_vector_index.py`

## ၃။ ပြဿနာ ရှာဖွေခြင်း (Troubleshooting Scenarios)

ပြဿနာ တစ်ခုစီကို symptom၊ တိုင်းတာရမည့် အချက်၊ ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်)၊
ဖြေရှင်းနည်းနှင့် ရှင်းလင်းသည့် term ဟူသည့် အစဉ်အတိုင်း ဖော်ပြထားသည်။ အကြောင်းရင်း အစဉ်သည်
တိုင်းတာမှုဖြင့် ရှာဖွေနိုင်သည့် အစဉ်အတိုင်း ဖြစ်သည်။ အသေးစိတ် ရှင်းလင်းချက်ကို အပိုင်း ၅.၂ တွင်
ပေးထားသည်။

### ပြဿနာ ၁ — အဖြေများသည် ကော်ပရပ်စ်တွင် မပါသည့် အချက်များကို ကိုးကားသည်

- **Symptom —** အဖြေသည် ယုံကြည်ရသည့် ပုံစံဖြင့် ရေးထားသည်၊ သို့သော် ထိုထဲပါ အချက် တစ်ချို့ကို
  ကော်ပရပ်စ်တွင် ရှာမတွေ့နိုင်ပါ။ ကိုးကား လင့် ပါလာပါက ထို အပိုင်းသည် အဆို ကို မထောက်ခံပါ။
- **တိုင်းတာရမည့် အချက် —** အဖြေတွင် ကိုးကားချက် ပါဝင်မှု ရာခိုင်နှုန်း၊ ကိုးကားချက် တိုင်း၏ chunk id
  ကို ကော်ပရပ်စ်ထဲ ရှာတွေ့မှု၊ source မပါသည့် အဆို အရေအတွက်၊ eval set အပေါ် retrieval recall@k
  နှင့် အဖြေ တိကျမှု ကို သီးခြားစီ တိုင်းတာမှု၊ prompt ထဲ အမှန်တကယ် ရောက်သည့် chunk အရေအတွက်
  (retrieval ပြန်သည့် အရေအတွက်နှင့် ကွာခြားမှု)။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) ကိုးကား ခေါင်းစီး မပေးထားသဖြင့် model သည်
  ကိုယ်ပိုင် ခန့်မှန်းချက်ဖြင့် ဖြည့်ခြင်း၊ (၂) retrieved chunk များ ဘတ်ဂျက် ကျော်လွန်၍ context ထဲ
  မဝင်ခြင်း၊ သို့မဟုတ် အလယ်တွင် ဖြတ်ခံရခြင်း၊ (၃) `Maximum Marginal Relevance (MMR)` က
  ကွဲပြားမှုကို ဦးစားပေး၍ မေးခွန်းအတွက် တိုက်ရိုက် သက်သေဖြစ်သည့် chunk ကို ဖယ်ခြင်း၊
  (၄) query သည် ကော်ပရပ်စ် ပြင်ပ အချက်အလက်ကို တောင်းခံခြင်း (corpus coverage ပြဿနာ)။
- **ဖြေရှင်းနည်း —** အဖြေတွင် ကိုးကား chunk id ကို မဖြစ်မနေ ထည့်စေရမည်၊ ကိုးကား မရှိသည့် အဆို
  ကို ပယ်ရမည်၊ eval set အပေါ် retrieval နှင့် grounding ကို သီးခြားစီ တိုင်းရမည်၊
  window ကျော်လွန်မှုကို မှတ်တမ်းတင်ရမည်။
- **ရှင်းလင်းသည့် term —** Grounding၊ RAG (Retrieval-Augmented Generation)၊ Chunking၊ Recall@K။

### ပြဿနာ ၂ — retrieval သည် နီးပါးတူညီသည့် chunk များသာ ပြန်သည်

- **Symptom —** top-5 ရလဒ် တစ်ခုလုံးသည် စာသား တူညီသည့် chunk များ ဖြစ်သည်၊ အဖြေသည် ထို အကြောင်းအရာ
  တစ်ခုတည်းကို ထပ်ခါတလဲလဲ ပြောသည်၊ အခြား အပိုင်းများမှ အထောက်အထား လုံးဝ မပါပါ။
- **တိုင်းတာရမည့် အချက် —** top-k အတွင်း pairwise စာသား တူညီမှု (သို့မဟုတ် vector similarity)၊
  chunk overlap အချိုး၊ doc id အလိုက် ခွဲထွက်မှု (diversity)၊ အဖြေ က အသုံးပြုသည့် source အရေအတွက်၊
  `MMR` အလေးချိန် setting။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) `MMR` မသုံးဘဲ relevance အစဉ်အတိုင်း ဖြတ်ခြင်း၊
  (၂) overlap မြင့်လွန်း၍ chunk အများအပြား စာသား ထပ်နေခြင်း၊ (၃) သက်ဆိုင်သည့် အပိုင်း တစ်ခုတည်း
  score မြင့်နေပြီး အခြား အပိုင်း များသည် ထို ပမာဏ မမီခြင်း (index ပြဿနာ မဟုတ်)၊ (၄) deduplication
  မလုပ်ထားသဖြင့် document တူညီသည့် chunk များ ထပ်နေခြင်း။
- **ဖြေရှင်းနည်း —** `MMR` သုံး၍ relevance-diversity အလေးချိန်ကို မှတ်တမ်းတင်ရမည်၊ overlap ကို
  လျှော့ရမည်၊ document identity အလိုက် deduplication ထည့်ရမည်၊ source လွှမ်းခြုံမှုကို metric အဖြစ်
  တိုင်းရမည်။
- **ရှင်းလင်းသည့် term —** Maximum Marginal Relevance (MMR)၊ Chunking၊ Reranker၊ Recall@K။

### ပြဿနာ ၃ — recall မြင့်သည်၊ သို့သော် အဖြေများ မှားနေဆဲ

- **Symptom —** retrieval recall@10 သည် သတ်မှတ်ထားသည့် ရည်မှန်းချက် ကျော်သည်၊ သို့သော်
  အသုံးပြုသူ ခံစားသည့် အဖြေ တိကျမှုသည် မတက်ပါ။
- **တိုင်းတာရမည့် အချက် —** သက်ဆိုင်သည့် chunk သည် prompt ထဲ တကယ် ဝင်မဝင် (reranking နှင့်
  ဘတ်ဂျက် ဖြတ်တောက်မှု နောက်)၊ ရလဒ်၏ အစဉ် (recall မြင့်သော်လည်း အစဉ် ဆိုး)၊ အဖြေတွင်
  ကိုးကားချက် တိုင်း ထောက်ခံမှု၊ မေးခွန်း အမျိုးအစား အလိုက် ခွဲ၍ တိကျမှု၊ context ဘတ်ဂျက်
  ကျော်လွန်မှုနှင့် reserved output လုံလောက်မှု။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) reranking သို့မဟုတ် ဘတ်ဂျက် ဖြတ်သည့် အဆင့်တွင်
  သက်ဆိုင်သည့် chunk ကျန်ခဲ့ခြင်း (first-stage recall သည် နောက်ဆုံး recall မဟုတ်)၊
  (၂) သက်ဆိုင်သည့် အထောက်အထား ပါသော်လည်း prompt က ၎င်းကို အသုံးပြုရန် မတောင်းဆိုခြင်း —
  အထောက်အထား ရှိခြင်းသည် grounding အာမခံချက် မဟုတ်ပါ၊ (၃) ရလဒ် အစဉ် ဆိုး၍ အရေးကြီးသည့် chunk
  ပထမဆုံး မဟုတ်ခြင်း၊ (၄) `Recall@K` ကို ကိုယ်တိုင် သတ်မှတ်ထားသည့် relevance judgment အပေါ်
  တိုင်းထားသဖြင့် တိုင်းတာမှုနှင့် အသုံးပြုသူ အမြင် ကွာခြားခြင်း။
- **ဖြေရှင်းနည်း —** retrieval recall ကို reranking နောက် ကိန်းဂဏန်းနှင့် ပြန်တိုင်းရမည်၊
  relevance judgment အစုကို ပြန်စစ်ရမည်၊ အဖြေတွင် ကိုးကား မဖြစ်မနေ ထည့်စေရမည်၊
  မေးခွန်း အမျိုးအစား အလိုက် ခွဲ၍ တိုင်းရမည်။
- **ရှင်းလင်းသည့် term —** Recall@K၊ Reranker၊ Grounding၊ RAG (Retrieval-Augmented Generation)။

## ၄။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်းများ (Design Decisions)

### ဆုံးဖြတ်ချက် ၁ — chunk အရွယ်အစား ရွေးချယ်ခြင်း

**အခြေအနေ —** document ၁၂,၀၀၀ token စီ ရှိသည့် လမ်းညွှန် ၅၀၀ ခု ရှိသည်။ window ၈,၁၉၂၊
system ၄၀၀၊ user ၆၀၊ history ၁,၂၀၀၊ reserved output ၈၀၀၊ အဖြေတွင် chunk ၆ ခု ထည့်မည်။
ရွေးချယ်စရာ သုံးခု — (က) chunk ၂၀၀ token, overlap ၄၀၊ (ခ) chunk ၄၀၀ token, overlap ၆၀၊
(ဂ) chunk ၈၀၀ token, overlap ၁၂၀။ eval set ၂၀၀ ခုအပေါ် တိုင်းတာရရှိသည့် အဖြေ တိကျမှုမှာ
(က) ၀.၈၆၊ (ခ) ၀.၉၃၊ (ဂ) ၀.၉၄။

**trade-off —** (က) သည် အထောက်အထား တစ်ခုကို ဖုံးရန် chunk ပိုများစွာ လိုသည် (၅.၄ ခု) နှင့်
recall@10 နိမ့်သည် (၀.၇၁)။ (ဂ) သည် တိကျမှု အနည်းငယ် မြင့်သော်လည်း ထပ်နေသည့် အကြောင်းအရာ
များလာနိုင်သည်။

**ဆုံးဖြတ်ချက် —** (ခ) ကို ရွေးရမည်၊ အကြောင်းမှာ ဖြေရှင်းချက် ၂ ခုလုံးတွင် ratio ၁.၂ ဖြစ်၍
overlap ကုန်ကျစရိတ် တူညီသော်လည်း (ခ) သည် (က) ထက် တိကျမှု ၇ ရာခိုင်နှုန်းအမှတ် မြင့်ပြီး
prompt ဘတ်ဂျက် ၁၃ ခု အထိ ဝင်နိုင်သောကြောင့် ဖြစ်သည်။ (ဂ) ၏ ထပ်တိုးအမြတ် ၁ ရာခိုင်နှုန်းအမှတ်
သည် chunk ကြီးလာခြင်းကြောင့် လွှမ်းခြုံမှု ကျဆင်းမှု အန္တရာယ်နှင့် တန်ဖိုး မမျှပါ။

**တိုင်းတာမည့် metric —** eval set အပေါ် အဖြေ တိကျမှု၊ recall@10၊ prompt ထဲ ထည့်နိုင်သည့် chunk
အရေအတွက်၊ chunk တစ်ခုလျှင် token ကုန်ကျစရိတ်။

### ဆုံးဖြတ်ချက် ၂ — reranking depth ရွေးချယ်ခြင်း

**အခြေအနေ —** hybrid search သည် candidate အများအပြား ပြန်သည်။ cross-encoder reranker သည်
pair တစ်ခုလျှင် ၃.၅ ms, fixed overhead ၃၅ ms။ retrieval latency ဘတ်ဂျက် ၂၅၀ ms။
တိုင်းတာရရှိသည့် precision@5 မှာ depth ၂၀ တွင် ၀.၅၈၊ depth ၅၀ တွင် ၀.၇၄၊ depth ၁၀၀ တွင် ၀.၈၀။

**trade-off —** depth ၅၀ သည် depth ၂၀ ထက် precision@5 ၁၆ ရာခိုင်နှုန်းအမှတ် မြင့်သည်၊
latency ၁၀၅ ms ထပ်ကျသည်။ depth ၁၀၀ သည် latency ၃၈၅ ms ဖြစ်၍ ဘတ်ဂျက်ကို ကျော်လွန်သည်။

**ဆုံးဖြတ်ချက် —** depth ၅၀ ကို ရွေးရမည် (latency ၂၁၀ ms၊ ဘတ်ဂျက် ၂၅၀ ms အတွင်း)။
depth ၁၀၀ ကို မရွေးရပါ၊ ၃၈၅ ms ဖြစ်၍ ဘတ်ဂျက်ကို ၅၄ % ကျော်လွန်သကဲ့သို့ ရက် တစ်လျှင်
request ၅၀,၀၀၀ တွင် cross-encoder GPU ကုန်ကျစရိတ် ထပ်တိုး $4.07 လိုအပ်သောကြောင့် ဖြစ်သည်။

**တိုင်းမည့် metric —** precision@5 နှင့် recall@5 (reranking နောက်)၊ retrieval latency p95၊
cross-encoder GPU-hour ကုန်ကျစရိတ်။

## ၅။ အဖြေများ (Answers with Explanations)

### ၅.၁ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း အဖြေများ

#### အဖြေ ၁ — chunk အရေအတွက်နှင့် overlap

**ဖော်မြူလာ —** stride = size − overlap၊ chunk အရေအတွက် = ⌈(N − overlap) / stride⌉၊
ratio = chunk အရေအတွက် × size / N။ ယူဆချက် — နောက်ဆုံး chunk သည် document ကို လွှမ်းခြုံသည်၊
char ၄ လုံး = token ၁ ခု။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. size ၁၅၀၀၊ overlap ၃၀၀ ဖြစ်ပါက stride = ၁၂၀၀၊ chunk = ⌈(120,000 − 300) / 1,200⌉ = ⌈99.75⌉ = ၁၀၀ ခု ဖြစ်သည်။
2. သိမ်းဆည်းသည့် ပမာဏ = 150,000 လုံး၊ ထပ်မှု ၃၀,၀၀၀ လုံး (၂၅.၀ %)၊ ratio ၁.၂၅ ဖြစ်သည်။
3. overlap ၆၀၀ ဖြစ်ပါက stride = ၉၀၀၊ chunk = ⌈(120,000 − 600) / 900⌉ = ⌈132.67⌉ = ၁၃၃ ခု ဖြစ်သည်၊
   ratio ၁.၆၆၂၅၊ ထပ်မှု ကုန်ကျစရိတ် ၂.၆၅ ဆ ဖြစ်သည်။
4. token = 150,000 / 4 = ၃၇,၅၀၀ token ဖြစ်သည်၊ 1M token လျှင် $0.02 ဖြင့် $0.00075 ဖြစ်သည်။
5. overlap မသုံးဘဲ ဖြတ်ပါက ⌈120,000 / 1,500⌉ = ၈၀ ခု ဖြစ်သည်၊ ဆိုလိုသည်မှာ overlap သည် chunk ၂၀ ခု
   ထပ်တိုးစေသည်။

**အဓိပ္ပာယ် —** chunk အရေအတွက်သည် ၁၀၀ ဖြစ်သည့်အခါ embedding call ၁၀၀ ကြိမ်၊ vector ၁၀၀ ခု၊
index ထဲ node ၁၀၀ ခု ဖြစ်သည်။ overlap ၃၀၀ မှ ၆၀၀ သို့ ပြောင်းပါက chunk အရေအတွက် ၃၃ %
တိုးသော်လည်း ထပ်နေသည့် ပမာဏ ၁၆၅ % တိုးသည် — ထို့ကြောင့် overlap ကို retrieval အရည်အသွေး
တိုင်းတာပြီးမှ ချိန်ရမည်။

```bash
python3 - <<'PY'
import math
n, size, overlap = 120000, 1500, 300
stride = size - overlap
c = math.ceil((n - overlap) / stride)
print("document chars", n, "size", size, "overlap", overlap, "stride", stride)
print("chunks           ", c)
print("stored chars     ", c * size)
print("extra chars      ", c * size - n)
print("duplication ratio", round((c * size) / n, 4))
print("duplication pct  ", round(100 * (c * size - n) / n, 2))
print("overlap links    ", c - 1, "-> chars", (c - 1) * overlap)
print("last chunk start ", (c - 1) * stride, "covers to", (c - 1) * stride + size)
print("coverage ok      ", (c - 1) * stride + size >= n)
c2 = math.ceil((n - 600) / (size - 600))
print("overlap 600 -> stride", size - 600, "chunks", c2)
print("  extra chars", c2 * size - n, "ratio", round(c2 * size / n, 4))
print("  duplicate token cost x", round((c2 * size - n) / (c * size - n), 3), "vs overlap 300")
tokens_total = c * size / 4
print("tokens at 4 chars/token", round(tokens_total))
print("embedding USD at 0.02 per 1M tokens", round(tokens_total / 1e6 * 0.02, 6))
print("pure tokens duplicated", round((c - 1) * overlap / 4))
print("chunks without overlap (no dedupe)", math.ceil(n / size))
PY
```

```text
document chars 120000 size 1500 overlap 300 stride 1200
chunks            100
stored chars      150000
extra chars       30000
duplication ratio 1.25
duplication pct   25.0
overlap links     99 -> chars 29700
last chunk start  118800 covers to 120300
coverage ok       True
overlap 600 -> stride 900 chunks 133
  extra chars 79500 ratio 1.6625
  duplicate token cost x 2.65 vs overlap 300
tokens at 4 chars/token 37500
embedding USD at 0.02 per 1M tokens 0.00075
pure tokens duplicated 7425
chunks without overlap (no dedupe) 80
```

#### အဖြေ ၂ — embedding storage နှင့် index memory

**ဖော်မြူလာ —** vector bytes = chunk × dimension × bytes-per-element၊
link bytes = chunk × M × id bytes × upper-tier factor၊ စုစုပေါင်း = vector + link + metadata။
ယူဆချက် — fp16 = ၂ ဘိုက်၊ int8 = ၁ ဘိုက်၊ id ၄ ဘိုက်၊ အထက်လွှာ အချိုး ၁.၁၅၊
metadata ၁၅၀ ဘိုက်/chunk၊ brute-force တွင် dimension တိုင်းအတွက် multiply-add တစ်ကြိမ်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. fp16 vector = 1,200,000 × 1,024 × 2 = 2,457,600,000 ဘိုက် = ၂.၂၈၉ GiB ဖြစ်သည်။
2. int8 vector = 1,144,000,000 ဘိုက် = ၁.၁၄၄ GiB ဖြစ်သည်၊ သက်သာသည့် ပမာဏ ၁.၁၄၄ GiB ဖြစ်သည်။
3. link (M = ၃၂) = 1,200,000 × 32 × 4 × 1.15 = ၁၇၆,၆၄၀,၀၀၀ ဘိုက် = ၀.၁၆၅ GiB ဖြစ်သည်။
4. metadata = 1,200,000 × 150 = ၁၈၀,၀၀၀,၀၀၀ ဘိုက် = ၀.၁၆၈ GiB ဖြစ်သည်။
5. စုစုပေါင်း = ၂.၆၂၁ GiB ဖြစ်သည်၊ vector ၈၇.၃ %၊ link ၆.၂၈ %၊ metadata ၆.၄ % ဖြစ်သည်။
6. M = ၆၄ ဖြစ်ပါက ၂.၇၈၅ GiB ဖြစ်သည်။ dimension ၃၈၄ ဖြစ်ပါက ၁.၁၉ GiB ဖြစ်သည်။
7. brute-force = 1,200,000 × 1,024 = 1,228,800,000 MAC = ၁.၂၂၉ GFLOP ဖြစ်သည်၊ ၅၀ GFLOP/s တွင်
   query တစ်ခုလျှင် ၂၄.၅၈ ms၊ ၂၀၀ GFLOP/s တွင် ၆.၁၄ ms ဖြစ်သည်။
8. ကျန်သည့် အရင်းအမြစ် ၁၀၀ GFLOP/s တွင် query/s = ၈၁ ခု ဖြစ်သည်။

**အဓိပ္ပာယ် —** ဤ အတိုင်းအတာတွင် brute-force သည် query တစ်ခုလျှင် ၂၄.၅၈ ms ဖြစ်သဖြင့်
latency လိုအပ်ချက် (ဥပမာ ၅၀ ms) အတွင်း ဝင်သေးသည်၊ သို့သော် query/s သည် ၈၁ သာ ဖြစ်သဖြင့်
concurrency မြင့်သည့် စနစ်တွင် မလုံလောက်ပါ။ ထို့ကြောင့် `Approximate Nearest Neighbor (ANN)`
လိုအပ်လာသည်။ index ကို int8 သို့ ပြောင်းပါက memory ထက်ဝက် ကျသော်လည်း recall အပေါ်
သက်ရောက်မှုကို တိုင်းတာရမည်။

```bash
python3 - <<'PY'
n, dim = 1200000, 1024
vec16 = n * dim * 2
vec8 = n * dim * 1
print("chunks", n, "dim", dim)
print("fp16 vector bytes", vec16)
print("fp16 GiB", round(vec16 / 2**30, 3))
print("fp16 MiB", round(vec16 / 2**20, 2))
print("int8 GiB", round(vec8 / 2**30, 3))
print("saving GiB int8 vs fp16", round((vec16 - vec8) / 2**30, 3))
M, id_bytes, upper = 32, 4, 1.15
links = int(n * M * id_bytes * upper)
print("M", M, "link bytes", links, "GiB", round(links / 2**30, 3))
meta = n * 150
print("metadata bytes", meta, "GiB", round(meta / 2**30, 3))
total = vec16 + links + meta
print("total bytes", total)
print("total GiB  ", round(total / 2**30, 3))
print("shares pct vectors/links/meta", round(100 * vec16 / total, 1), round(100 * links / total, 2), round(100 * meta / total, 2))
print("total with M=64 GiB", round((n * 64 * id_bytes * upper + vec16 + meta) / 2**30, 3))
print("total with 384 dim fp16 GiB", round((n * 384 * 2 + links + meta) / 2**30, 3))
macs = n * dim
print("brute force MACs per query", macs, "=", round(macs / 1e9, 3), "GFLOP")
print("ms per query at 50 GFLOP/s", round(macs / 1e9 / 50.0 * 1000, 2))
print("ms per query at 200 GFLOP/s", round(macs / 1e9 / 200.0 * 1000, 2))
print("queries per second (100 GFLOP/s budget)", round(100.0 / (macs / 1e9)))
PY
```

```text
chunks 1200000 dim 1024
fp16 vector bytes 2457600000
fp16 GiB 2.289
fp16 MiB 2343.75
int8 GiB 1.144
saving GiB int8 vs fp16 1.144
M 32 link bytes 176640000 GiB 0.165
metadata bytes 180000000 GiB 0.168
total bytes 2814240000
total GiB   2.621
shares pct vectors/links/meta 87.3 6.28 6.4
total with M=64 GiB 2.785
total with 384 dim fp16 GiB 1.19
brute force MACs per query 1228800000 = 1.229 GFLOP
ms per query at 50 GFLOP/s 24.58
ms per query at 200 GFLOP/s 6.14
queries per second (100 GFLOP/s budget) 81
```

#### အဖြေ ၃ — Recall@K

**ဖော်မြူလာ —** Recall@K = |သက်ဆိုင်သည့် item ∩ top K| / |သက်ဆိုင်သည့် item|။
macro mean = per-query တန်ဖိုးများ၏ ပျမ်းမျှ၊ micro = pooled hits / pooled relevant။
ယူဆချက် — relevance judgment များ ပေးထားသည့်အတိုင်း၊ q4 တွင် သက်ဆိုင်သည့် item မရှိပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. q1: top-3၊ top-5၊ top-10 သုံးမျိုးလုံးတွင် သက်ဆိုင်သည့် ၃ ခု ပါသည်၊ ထို့ကြောင့် 3/5 = ၀.၆ ဖြစ်သည်။
2. q2: သက်ဆိုင်သည့် ၂ ခုလုံး ပါသည်၊ 2/2 = ၁.၀ ဖြစ်သည်။
3. q3: သက်ဆိုင်သည့် ၈ ခုအနက် ၂ ခု ပါသည်၊ 2/8 = ၀.၂၅ ဖြစ်သည်။
4. macro mean Recall@5 = (0.6 + 1.0 + 0.25) / 3 = ၀.၆၁၆၇ ဖြစ်သည် (၆၁.၆၇ %)။ k = ၁၀ တွင်လည်း
   တူညီသည် — ဆိုလိုသည်မှာ K တိုးခြင်းက ၃ ခုလုံးတွင် အထောက်အထား အသစ် မထည့်ပေးပါ။
5. micro recall = pooled hits (3 + 2 + 2 = 7) / pooled relevant (5 + 2 + 8 = 15) = ၀.၄၆၆၇ ဖြစ်သည်။
6. q4 ကို သုည သတ်မှတ်ပါက mean = (0.6 + 1.0 + 0.25 + 0.0) / 4 = ၀.၄၆၂၅ ဖြစ်သည်။
   ဖယ်ထုတ်ပါက ၀.၆၁၆၇ ရှိသည် — ထို့ကြောင့် မူဝါဒ ရွေးချယ်မှုသည် တန်ဖိုးကို ၁၅ ရာခိုင်နှုန်းအမှတ်
   ကွာစေသည်။

**အဓိပ္ပာယ် —** q3 ၏ နိမ့်သည့် recall သည် retrieval ပြဿနာ (သက်ဆိုင်သည့် ၈ ခုအနက် ၆ ခု မတွေ့)
ကို ပြသည်၊ q1 ၏ နိမ့်သည့် recall သည် judgment ပြဿနာ (၅ ခုအနက် ၂ ခု လွတ်) ကို ပြသည်။
macro နှင့် micro ကွာခြားခြင်းသည် သက်ဆိုင်သည့် item အရေအတွက် မညီမျှသည့် query များတွင်
အရေးပါသည်။

```bash
python3 - <<'PY'
cases = [
    ("q1", {"d1", "d2", "d3", "d4", "d5"}, ["d1", "d2", "d3", "d9", "d10", "d11", "d12", "d13", "d14", "d15"]),
    ("q2", {"d2", "d6"}, ["d2", "d6", "d7", "d8", "d9", "d10", "d11", "d12", "d13", "d14"]),
    ("q3", {"d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8"}, ["d1", "d2", "d9", "d10", "d11", "d12", "d13", "d14", "d15", "d16"]),
]
for name, rel, top in cases:
    for k in (3, 5, 10):
        hit = len(set(top[:k]) & rel)
        print(f"{name} k={k:2} hit {hit} / {len(rel)} = {hit / len(rel):.4f}")
    print(f"{name} relevant {len(rel)} top10 {top[:10]}")
r5 = [len(set(t[:5]) & r) / len(r) for _, r, t in cases]
r10 = [len(set(t[:10]) & r) / len(r) for _, r, t in cases]
print("recall@5 per query", [round(v, 4) for v in r5])
print("recall@10 per query", [round(v, 4) for v in r10])
print("mean recall@5", round(sum(r5) / len(r5), 4))
print("mean recall@10", round(sum(r10) / len(r10), 4))
print("macro mean recall@5 pct", round(100 * sum(r5) / len(r5), 2))
with_zero = r5 + [0.0]
print("mean recall@5 if zero-relevant query assigned 0", round(sum(with_zero) / len(with_zero), 4))
print("mean recall@5 if zero-relevant query excluded  ", round(sum(r5) / len(r5), 4))
print("queries with zero recalled evidence", sum(1 for _, r, t in cases if not (set(t[:10]) & r)))
print("recall@5 gap to recall@10 per query", [round(a - b, 4) for a, b in zip(r10, r5)])
print("micro recall@5 (pooled hits / pooled relevant)",
      round(sum(len(set(t[:5]) & r) for _, r, t in cases) / sum(len(r) for _, r, _ in cases), 4))
PY
```

```text
q1 k= 3 hit 3 / 5 = 0.6000
q1 k= 5 hit 3 / 5 = 0.6000
q1 k=10 hit 3 / 5 = 0.6000
q1 relevant 5 top10 ['d1', 'd2', 'd3', 'd9', 'd10', 'd11', 'd12', 'd13', 'd14', 'd15']
q2 k= 3 hit 2 / 2 = 1.0000
q2 k= 5 hit 2 / 2 = 1.0000
q2 k=10 hit 2 / 2 = 1.0000
q2 relevant 2 top10 ['d2', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13', 'd14']
q3 k= 3 hit 2 / 8 = 0.2500
q3 k= 5 hit 2 / 8 = 0.2500
q3 k=10 hit 2 / 8 = 0.2500
q3 relevant 8 top10 ['d1', 'd2', 'd9', 'd10', 'd11', 'd12', 'd13', 'd14', 'd15', 'd16']
recall@5 per query [0.6, 1.0, 0.25]
recall@10 per query [0.6, 1.0, 0.25]
mean recall@5 0.6167
mean recall@10 0.6167
macro mean recall@5 pct 61.67
mean recall@5 if zero-relevant query assigned 0 0.4625
mean recall@5 if zero-relevant query excluded   0.6167
queries with zero recalled evidence 0
recall@5 gap to recall@10 per query [0.0, 0.0, 0.0]
micro recall@5 (pooled hits / pooled relevant) 0.4667
```

#### အဖြေ ၄ — top-k နှင့် top-p ပုံစံ ဖြတ်တောက်ခြင်း

**ဖော်မြူလာ —** normalized အလေးချိန် = similarity / Σ similarity (cosine similarity သည်
ဖြစ်နိုင်ခြေ မဟုတ်သဖြင့် top-p သုံးရန် normalize လုပ်သည်ဟု ယူသည်)၊
top-p = cumulative အလေးချိန် ≥ p ဖြစ်သည့် အသေးဆုံး အစု။
ယူဆချက် — similarity စာရင်းသည် ကြီးစဉ်ငယ်လိုက် စီပြီးသား၊ chunk တစ်ခုလျှင် ၄၈၀ token။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. Σ similarity = 5.56 ဖြစ်သည်။
2. normalized = [0.1637, 0.1547, 0.1511, 0.1439, 0.1115, 0.1043, 0.0989, 0.0719] ဖြစ်သည်။
3. top-k = ၄ ဖြင့် ဖြတ်ပါက ကျန်သည့် အစု = [0.91, 0.86, 0.84, 0.80]၊ raw ပမာဏ ၃.၄၁ ဖြစ်သည်၊
   Σ ၏ ၆၁.၃၃ % ဖြစ်သည်၊ renorm ပြီးနောက် [0.2669, 0.2522, 0.2463, 0.2346] ဖြစ်သည်။
4. top-p = 0.9 ဖြင့် ဖြတ်ပါက candidate ၇ ခု ကျန်သည်၊ cumulative ၀.၉၂၈၁ ဖြစ်သည်၊
   ဖြတ်လိုက်သည့် mass ၀.၀၇၁၉ (= နောက်ဆုံး candidate ၏ အလေးချိန်) ဖြစ်သည်။
5. absolute threshold 0.6 ဖြင့် ဖြတ်ပါက ၅ ခု ကျန်သည်။
6. token ဘတ်ဂျက် = top-k ၁,၉၂၀၊ top-p ၃,၃၆၀၊ threshold ၂,၄၀၀ ဖြစ်သည်။

**အဓိပ္ပာယ် —** နည်းလမ်း သုံးမျိုးသည် အရေအတွက် ၄၊ ၇၊ ၅ ဟု ကွာခြားသဖြင့် token ဘတ်ဂျက်
၄၃ % အထိ ကွာသည်။ top-k သည် အရေအတွက်ကို အမြဲ တူညီစေသည်၊ top-p သည် score ပြန့်ကျက်မှု
အပေါ် မူတည်သည်၊ threshold သည် absolute ဖြစ်သဖြင့် score စကေး ပြောင်းသည့်အခါ မတည်ငြိမ်ပါ။
cosine similarity တွင် ဖြတ်တောက်ရန် အန္တရာယ် အနည်းဆုံး နည်းလမ်းသည် top-k ဖြစ်သည်၊
top-p သုံးလိုပါက normalize လုပ်သည့် စည်းမျဉ်းကို မှတ်တမ်းတင်ရမည်။

```bash
python3 - <<'PY'
scores = [0.91, 0.86, 0.84, 0.80, 0.62, 0.58, 0.55, 0.40]
labels = [f"c{i}" for i in range(1, len(scores) + 1)]
total = sum(scores)
print("cosine scores", list(zip(labels, scores)))
print("sum of scores", round(total, 4))
norm = [s / total for s in scores]
print("normalised   ", [round(v, 6) for v in norm])
K = 4
kept_k = scores[:K]
sk = sum(kept_k)
print("top-k", K, "kept", list(zip(labels[:K], kept_k)))
print("  raw mass", round(sk, 4), "share of total", round(sk / total, 4), "dropped", round(1 - sk / total, 4))
print("  renormalised", [round(v / sk, 6) for v in kept_k])
cut = 0.90
acc, kept_p = 0.0, []
for v in norm:
    acc += v
    kept_p.append(v)
    if acc >= cut:
        break
print("top-p", cut, "keeps", len(kept_p), "candidates", labels[:len(kept_p)])
print("  cumulative normalised", round(acc, 6))
print("  renormalised", [round(v / acc, 6) for v in kept_p])
print("  dropped mass", round(1 - acc, 6))
thr = 0.60
kept_t = [s for s in scores if s >= thr]
print("absolute threshold", thr, "keeps", len(kept_t), "candidates", kept_t, "sum", round(sum(kept_t), 4))
print("relative share of kept set", round(sum(kept_t) / total, 4))
print("k=4 shares pct", round(100 * sum(kept_k) / total, 2))
print("tokens kept by each rule: top-k", K, "top-p", len(kept_p), "threshold", len(kept_t))
print("token budget at 480 tokens per candidate", 480 * K, 480 * len(kept_p), 480 * len(kept_t))
print("normalised score of the first dropped candidate under top-p", round(norm[len(kept_p)], 6))
print("score gap c4 -> c5", round(scores[3] - scores[4], 4))
PY
```

```text
cosine scores [('c1', 0.91), ('c2', 0.86), ('c3', 0.84), ('c4', 0.8), ('c5', 0.62), ('c6', 0.58), ('c7', 0.55), ('c8', 0.4)]
sum of scores 5.56
normalised    [0.163669, 0.154676, 0.151079, 0.143885, 0.111511, 0.104317, 0.098921, 0.071942]
top-k 4 kept [('c1', 0.91), ('c2', 0.86), ('c3', 0.84), ('c4', 0.8)]
  raw mass 3.41 share of total 0.6133 dropped 0.3867
  renormalised [0.266862, 0.252199, 0.246334, 0.234604]
top-p 0.9 keeps 7 candidates ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7']
  cumulative normalised 0.928058
  renormalised [0.176357, 0.166667, 0.162791, 0.155039, 0.120155, 0.112403, 0.106589]
  dropped mass 0.071942
absolute threshold 0.6 keeps 5 candidates [0.91, 0.86, 0.84, 0.8, 0.62] sum 4.03
relative share of kept set 0.7248
k=4 shares pct 61.33
tokens kept by each rule: top-k 4 top-p 7 threshold 5
token budget at 480 tokens per candidate 1920 3360 2400
normalised score of the first dropped candidate under top-p 0.071942
score gap c4 -> c5 0.18
```

#### အဖြေ ၅ — retrieved chunk တိုင်း ထပ်တိုးသည့် token နှင့် ကုန်ကျစရိတ်

**ဖော်မြူလာ —** retrieved = chunk အရေအတွက် × (chunk token + header token)၊
used = system + user + history + reserved_output + retrieved၊
cost = used / 10⁶ × price_in + output / 10⁶ × price_out။
ယူဆချက် — header ၄၀ token သည် chunk တိုင်းတွင် ပါသည်၊ output ၆၀၀ token ဖြစ်သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. chunk ၂ ခု: retrieved ၁,၁၀၄၊ used ၃,၅၆၄ (၄၃.၅ %)၊ headroom ၄,၆၂၈ ဖြစ်သည်။
2. chunk ၆ ခု: retrieved ၃,၃၁၂၊ used ၅,၇၇၂ (၇၀.၅ %)၊ headroom ၂,၄၂၀ ဖြစ်သည်။
3. chunk ၈ ခု: used ၆,၈၇၆ (၈၃.၉ %) ဖြစ်သည်။
4. window ထဲ ဝင်နိုင်သည့် chunk = (8,192 − 2,460) / 552 = ၁၀ ခု ဖြစ်သည်။
5. cost = 5,772 / 10⁶ × 0.25 + 600 / 10⁶ × 1.00 = 0.001443 + 0.0006 = $0.002043 ဖြစ်သည်။
6. ၁,၀၀၀ request = $2.043၊ ရက် ၅၀,၀၀၀ = $102.15 / ရက်၊ ၃၀ ရက် = $3,064.50 ဖြစ်သည်။
7. chunk ၆ မှ ၄ ခုသို့ လျှော့ပါက request တစ်ခုလျှင် $0.000276၊ ရက် ၅၀,၀၀၀ တွင် $13.80 သက်သာသည်။
8. retrieval မပါသည့် baseline used = ၂,၄၆၀ ဖြစ်သည်၊ ထို့ကြောင့် retrieve လုပ်ခြင်းသည် input
   ကုန်ကျစရိတ်ကို ၂.၃၄၆ ဆ ဖြစ်စေသည်။

**အဓိပ္ပာယ် —** chunk တိုင်းသည် header နှင့်အတူ token ၅၅၂ ယူသည်၊ ထို့ကြောင့် chunk ၈ ခု
တင်ပါက window ၏ ၈၄ % ပြည့်ပြီး output အတွက် နေရာ ၁,၃၁၆ token သာ ကျန်သည်။
header token သည် ကိုးကားချက် အတွက် မဖြစ်မနေ လိုသော်လည်း ကုန်ကျစရိတ် အပိုင်း၌
၇.၈ % ယူသည် — ထို့ကြောင့် header ကို ကျစ်လျစ်အောင် ရေးခြင်းသည် တိုက်ရိုက် အကျိုးရှိသည်။

```bash
python3 - <<'PY'
chunk_tokens, header = 512, 40
system, user, history, reserve = 400, 60, 1200, 800
window = 8192
price_in, price_out = 0.25, 1.00
out_tokens = 600
for kept in (2, 4, 6, 8):
    retrieved = kept * (chunk_tokens + header)
    used = system + user + history + reserve + retrieved
    print(f"chunks {kept}: retrieved {retrieved} used {used} window {window} "
          f"headroom {window - used} share {100 * used / window:.1f} pct")
kept = 6
retrieved = kept * (chunk_tokens + header)
used = system + user + history + reserve + retrieved
cost_in = used / 1e6 * price_in
cost_out = out_tokens / 1e6 * price_out
per_request = cost_in + cost_out
print("per chunk cost USD          ", round((chunk_tokens + header) / 1e6 * price_in, 7))
print("chunks that fit in window   ", (window - (system + user + history + reserve)) // (chunk_tokens + header))
print("max token budget for chunks ", window - (system + user + history + reserve))
print("cost input USD              ", round(cost_in, 7))
print("cost output USD             ", round(cost_out, 7))
print("cost per request USD        ", round(per_request, 7))
print("cost per 1000 requests USD  ", round(per_request * 1000, 4))
for rpd in (1000, 50000):
    print(f"requests/day {rpd}: USD/day {per_request * rpd:.3f} USD/30d {per_request * rpd * 30:.2f}")
print("retrieved share of input pct", round(100 * retrieved / used, 1))
print("saving 6 -> 4 chunks per request USD", round(2 * (chunk_tokens + header) / 1e6 * price_in, 7))
print("saving 6 -> 4 chunks per 50k requests/day USD", round(2 * (chunk_tokens + header) / 1e6 * price_in * 50000, 3))
print("no retrieval baseline used  ", system + user + history + reserve)
print("retrieval multiplier on input cost", round((used) / (system + user + history + reserve), 3))
PY
```

```text
chunks 2: retrieved 1104 used 3564 window 8192 headroom 4628 share 43.5 pct
chunks 4: retrieved 2208 used 4668 window 8192 headroom 3524 share 57.0 pct
chunks 6: retrieved 3312 used 5772 window 8192 headroom 2420 share 70.5 pct
chunks 8: retrieved 4416 used 6876 window 8192 headroom 1316 share 83.9 pct
per chunk cost USD           0.000138
chunks that fit in window    10
max token budget for chunks  5732
cost input USD               0.001443
cost output USD              0.0006
cost per request USD         0.002043
cost per 1000 requests USD   2.043
requests/day 1000: USD/day 2.043 USD/30d 61.29
requests/day 50000: USD/day 102.150 USD/30d 3064.50
retrieved share of input pct 57.4
saving 6 -> 4 chunks per request USD 0.000276
saving 6 -> 4 chunks per 50k requests/day USD 13.8
no retrieval baseline used   2460
retrieval multiplier on input cost 2.346
```

#### အဖြေ ၆ — ANN parameter သည် latency နှင့် recall အပေါ် သက်ရောက်မှု

**ဖော်မြူလာ —** latency(e) = 0.35 + (32 + 6e) × 0.0009 ms၊ recall(e) = 1 − exp(−e / 45)၊
per-core query/s = 1,000 / latency။ ယူဆချက် — node တစ်ခု လည်ပတ်သည့် အချိန် ၀.၉ µs၊
fixed overhead ၀.၃၅ ms၊ recall curve သည် ပေးထားသည့် ယူဆချက်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. `ef` = ၁၆: visited ၁၂၈၊ latency ၀.၄၆၅ ms၊ recall@10 ၀.၂၉၉၂ ဖြစ်သည်။
2. `ef` = ၆၄: visited ၄၁၆၊ latency ၀.၇၂၄ ms၊ recall@10 ၀.၇၅၈၈ ဖြစ်သည်။
3. `ef` = ၂၅၆: visited ၁,၅၆၈၊ latency ၁.၇၆၁ ms၊ recall@10 ၀.၉၉၆၆ ဖြစ်သည်။
4. `ef` ၁၆ တွင် true neighbor ၏ ၇၀.၀၈ % လွတ်သည်၊ ဆိုလိုသည်မှာ recall ၀.၂၉၉၂ ဖြစ်သည်။
5. `ef` ၃၂ → ၆၄: recall ၂၄.၉၉ ရာခိုင်နှုန်းအမှတ် တိုးသည်၊ latency ၀.၁၇၃ ms သာ ထပ်တိုးသည် —
   ဤနေရာသည် အကျိုးအမြတ် အများဆုံး နေရာ ဖြစ်သည်။
6. `ef` ၁၂၈ → ၂၅၆: recall ၅.၄၈ ရာခိုင်နှုန်းအမှတ် တိုးသည်၊ latency ၀.၆၉၁ ms ထပ်တိုးသည် —
   ကုန်ကျမှု အချိုးသည် ပိုဆိုးသည်။
7. recall 0.95 ရရန် `ef` = −45 × ln(0.05) = ၁၃၄.၈ လိုသည်၊ 0.99 ရရန် ၂၀၇.၂ လိုသည်။
8. `M` = ၁၆၊ ၃၂၊ ၆၄ အတွက် link memory = ၈၄.၂၊ ၁၆၈.၅၊ ၃၃၆.၉ MiB ဖြစ်သည် (chunk ၁.၂ သန်း)။
9. per-core query/s သည် `ef` ၁၆ တွင် ၂,၁၄၉.၆ မှ `ef` ၂၅၆ တွင် ၅၆၇.၈ သို့ ကျဆင်းသည်၊
   ဆိုလိုသည်မှာ `ef` ၁၆ မှ ၆၄ သို့ တိုးပါက ၃၅.၈ % ကျဆင်းသည်။

**ကောက်ချက် —** recall ကို latency နှင့် **တွဲဖက်** တင်ပြရမည်။ `ef` ကို ၁၆ မှ ၆၄ သို့ တိုးခြင်းသည်
ကုန်ကျမှု အနည်းငယ်ဖြင့် အကျိုးအမြတ် အကြီးဆုံး ဖြစ်သည်၊ ၁၂၈ မှ ၂၅၆ သို့ တိုးခြင်းသည်
အကျိုးအမြတ် နည်း၍ ကုန်ကျမှု ကြီးသည်။ `M` တိုးခြင်းသည် memory ကို linear တိုးစေသော်လည်း
recall အပေါ် သက်ရောက်မှုကို သီးခြား တိုင်းတာရမည်။

```bash
python3 - <<'PY'
import math
fixed_ms, us_per_node, cores = 0.35, 0.9, 8
for e in (16, 32, 64, 128, 256):
    visited = 32 + 6 * e
    lat = fixed_ms + visited * us_per_node / 1000
    rec = 1 - math.exp(-e / 45)
    qps = 1000 / lat
    print(f"ef {e:3} visited {visited:5} latency_ms {lat:.3f} recall@10 {rec:.4f} per-core qps {qps:.1f} 8-core qps {qps * cores:.0f}")
print("recall floor ef=16", round(1 - math.exp(-16 / 45), 4), "misses pct", round(100 * math.exp(-16 / 45), 2))
print("recall floor ef=64", round(1 - math.exp(-64 / 45), 4), "misses pct", round(100 * math.exp(-64 / 45), 2))
print("latency ratio 256 vs 16", round((fixed_ms + (32 + 6 * 256) * us_per_node / 1000) / (fixed_ms + (32 + 6 * 16) * us_per_node / 1000), 3))
print("recall gain 32 -> 64 pt", round(100 * ((1 - math.exp(-64 / 45)) - (1 - math.exp(-32 / 45))), 2))
print("latency added 32 -> 64 ms", round((32 + 6 * 64) * us_per_node / 1000 - (32 + 6 * 32) * us_per_node / 1000, 3))
print("recall gain 128 -> 256 pt", round(100 * ((1 - math.exp(-256 / 45)) - (1 - math.exp(-128 / 45))), 2))
print("latency added 128 -> 256 ms", round((32 + 6 * 256) * us_per_node / 1000 - (32 + 6 * 128) * us_per_node / 1000, 3))
print("per-core qps ef16/64/256", round(1000 / (fixed_ms + 128 * us_per_node / 1000), 1),
      round(1000 / (fixed_ms + 416 * us_per_node / 1000), 1),
      round(1000 / (fixed_ms + 1568 * us_per_node / 1000), 1))
print("8-core aggregate qps ef64", round(8 * 1000 / (fixed_ms + 416 * us_per_node / 1000)))
print("8-core qps loss ef64 vs ef16 pct",
      round(100 * (1000 / (fixed_ms + 128 * us_per_node / 1000) - 1000 / (fixed_ms + 416 * us_per_node / 1000)) / (1000 / (fixed_ms + 128 * us_per_node / 1000)), 1))
n, dim, id_bytes, upper = 1200000, 1024, 4, 1.15
for M in (16, 32, 64):
    link_mib = n * M * id_bytes * upper / 2**20
    print(f"M={M:2} link MiB {link_mib:8.1f}")
print("memory cost of M 16 -> 64 pct", round(100 * (64 - 16) / 16, 1))
print("index build link bytes M=32", int(n * 32 * id_bytes * upper))
print("ef needed for 0.95 recall", round(-45 * math.log(0.05), 1))
print("ef needed for 0.99 recall", round(-45 * math.log(0.01), 1))
PY
```

```text
ef  16 visited   128 latency_ms 0.465 recall@10 0.2992 per-core qps 2149.6 8-core qps 17197
ef  32 visited   224 latency_ms 0.552 recall@10 0.5089 per-core qps 1812.9 8-core qps 14503
ef  64 visited   416 latency_ms 0.724 recall@10 0.7588 per-core qps 1380.5 8-core qps 11044
ef 128 visited   800 latency_ms 1.070 recall@10 0.9418 per-core qps 934.6 8-core qps 7477
ef 256 visited  1568 latency_ms 1.761 recall@10 0.9966 per-core qps 567.8 8-core qps 4542
recall floor ef=16 0.2992 misses pct 70.08
recall floor ef=64 0.7588 misses pct 24.12
latency ratio 256 vs 16 3.786
recall gain 32 -> 64 pt 24.99
latency added 32 -> 64 ms 0.173
recall gain 128 -> 256 pt 5.48
latency added 128 -> 256 ms 0.691
per-core qps ef16/64/256 2149.6 1380.5 567.8
8-core aggregate qps ef64 11044
8-core qps loss ef64 vs ef16 pct 35.8
M=16 link MiB     84.2
M=32 link MiB    168.5
M=64 link MiB    336.9
memory cost of M 16 -> 64 pct 300.0
index build link bytes M=32 176640000
ef needed for 0.95 recall 134.8
ef needed for 0.99 recall 207.2
```

### ၅.၂ ပြဿနာ ရှာဖွေခြင်း အဖြေများ

#### အဖြေ ၁ — ကော်ပရပ်စ်တွင် မပါသည့် အချက်များ ကိုးကားခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** prompt ထဲသို့ document များ ထည့်ခြင်းသည် `Grounding` အတွက်
အခွင့်အလမ်း တစ်ခု ဖန်တီးပေးသည်၊ သို့သော် model က ၎င်းတို့ကို မှန်ကန်စွာ အသုံးပြုမည်ဟု
အာမမခံပါ။ ကိုးကား ခေါင်းစီး မပါပါက မည်သည့် အဆိုက မည်သည့် chunk မှ လာသည်ကို စစ်ဆေးရန်
မဖြစ်နိုင်သဖြင့် အထောက်အထား မရှိသည့် အဆိုသည် အဖြေထဲ ဝင်လာသည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** ကိုးကားချက် ပါဝင်မှု ရာခိုင်နှုန်းကို ဦးစွာ တိုင်းပါ၊ သုည ဖြစ်ပါက
အကြောင်းရင်း (၁) ဖြစ်သည်။ ကိုးကားချက် ပါသော်လည်း ထို chunk သည် ခေါင်းစီး အဆို ကို
မထောက်ခံပါက grounding အဆင့် ပြဿနာ ဖြစ်သည်။ window ကျော်လွန်မှု မှတ်တမ်း ရှိပါက
အကြောင်းရင်း (၂) ဖြစ်သည်။ `MMR` သုံးထားပြီး သက်ဆိုင်သည့် chunk မပါဝင်ပါက အကြောင်းရင်း (၃) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** ကိုးကား မဖြစ်မနေ ထည့်စေပြီးနောက် မထောက်ခံသည့် အဆို
အရေအတွက် ကျဆင်းမှ အတည်ပြုနိုင်သည်။ `Recall@K` မြင့်ခြင်းသည် နောက်ဆုံး အဖြေ grounded ဖြစ်ခြင်းကို
အာမမခံသဖြင့် retrieval metric နှင့် grounding metric နှစ်ခုကို သီးခြားစီ တင်ပြရမည်။

#### အဖြေ ၂ — နီးပါးတူညီသည့် chunk များ ပြန်ခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** relevance အစဉ်အတိုင်း ဖြတ်ပါက စာသား တူညီသည့် chunk များသည်
score နီးပါး ရသဖြင့် အစဉ်လိုက် ပါလာသည်။ ကန့်သတ်ထားသည့် ဘတ်ဂျက်တွင် ထို chunk များသည်
အခြား အပိုင်းများကို နေရာ မကျန်စေပါ — ဆိုလိုသည်မှာ လွှမ်းခြုံမှုသည် ကျဆင်းသည်။

**အစဉ်လိုက် ဆုံးရှာရန် —** top-k အတွင်း pairwise တူညီမှု မြင့်ပါက ဤ ပြဿနာ ဖြစ်သည်။ chunk overlap
အချိုး မြင့်ပါက အကြောင်းရင်း (၂) ဖြစ်သည်။ chunk id ထပ်နေပါက အကြောင်းရင်း (၄) ဖြစ်သည်။
`MMR` သုံးထားပြီးသော်လည်း ဤ အခြေအနေ ဖြစ်ပါက အလေးချိန် setting ပြဿနာ ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** `MMR` ဖွင့်ပြီးနောက် source အရေအတွက် တိုးမှ အတည်ပြုနိုင်သည်။
`MMR` သည် ရှိပြီးသား candidate set ကို ကွဲပြားစေရုံသာ ဖြစ်သည်၊ လွတ်နေသည့် အထောက်အထားကို
ရှာဖွေပေးခြင်း မပြုပါ — ထို့ကြောင့် candidate pool ကိုပါ တွဲဖက် ပြင်ရမည်။

#### အဖြေ ၃ — recall မြင့်သော်လည်း အဖြေ မှားနေဆဲ

**အကြောင်းရင်း ရှင်းလင်းချက် —** `Recall@K` သည် retrieval အဆင့်တစ်ခုက downstream အတွက်
သက်ဆိုင်သည့် candidate များ လုံလောက်စွာ ပေးနိုင်ခြင်း ရှိ/မရှိ ကိုသာ ပြောပြသည်။ ၎င်းသည်
ထိပ်ဆုံး ရလဒ် ကောင်းခြင်း၊ ranking ကောင်းစွာ အစဉ်သတ်မှတ်ထားခြင်း သို့မဟုတ် နောက်ဆုံး အဖြေ
grounded ဖြစ်ခြင်းကို အာမမခံပါ။ ထို့ကြောင့် recall@10 မြင့်သော်လည်း reranking နှင့် ဘတ်ဂျက်
ဖြတ်သည့် အဆင့်တွင် သက်ဆိုင်သည့် chunk ကျန်ခဲ့နိုင်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** retrieval ပြန်သည့် စာရင်းနှင့် prompt ထဲ တကယ် ဝင်သည့် စာရင်း
နှစ်ခုကို နှိုင်းပါ။ သက်ဆိုင်သည့် chunk သည် ဒုတိယ စာရင်းတွင် မပါပါက အကြောင်းရင်း (၁) ဖြစ်သည်။
ပါသော်လည်း အဖြေ မှားပါက grounding ပြဿနာ ဖြစ်သည် (အကြောင်းရင်း ၂)။ တိုင်းတာသည့် judgment
အစုကို ပြန်စစ်ပါ — အကြောင်းရင်း (၄) ဖြစ်နိုင်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** reranking နောက် recall ကို ပြန်တိုင်း၍ ကျဆင်းမှုကို ဖော်ထုတ်ရမည်။
recall metric နှင့် အဖြေ တိကျမှု metric နှစ်ခုလုံး မြင့်မှသာ စနစ်သည် အမှန် တိုးတက်သည်ဟု
ဆုံးဖြတ်နိုင်သည်။

### ၅.၃ ဆုံးဖြတ်ချက် အဖြေများ

#### အဖြေ ၁ — chunk အရွယ်အစား

**ရှင်းလင်းချက် —** chunk ၂၀၀ token, overlap ၄၀ ဖြစ်ပါက stride ၁၆၀၊ chunk ၇၅ ခု၊ ratio ၁.၂၅
ဖြစ်သည်။ chunk ၄၀၀/၆၀ ဖြစ်ပါက stride ၃၄၀၊ chunk ၃၆ ခု၊ ratio ၁.၂ ဖြစ်သည်။
chunk ၈၀၀/၁၂၀ ဖြစ်ပါက stride ၆၈၀၊ chunk ၁၈ ခု၊ ratio ၁.၂ ဖြစ်သည်။ window ၈,၁၉၂ တွင်
အထောက်အထား အတွက် နေရာ ၅,၇၃၂ token ကျန်သဖြင့် (ခ) အတွက် chunk ၁၄ ခု အထိ ထည့်နိုင်သည်၊
၆ ခု ထည့်သည့် အစီအစဉ်နှင့် ကိုက်ညီသည်။

**ဆုံးဖြတ်ချက် —** chunk ၄၀၀ token, overlap ၆၀ ကို ရွေးရမည်၊ အကြောင်းမှာ ထပ်မှု ratio သည်
chunk ၂၀၀ နှင့် တူညီသော်လည်း အဖြေ တိကျမှု ၇ ရာခိုင်နှုန်းအမှတ် မြင့်ပြီး chunk အရေအတွက်လည်း
ထက်ဝက် လျော့သဖြင့် index နှင့် store ကုန်ကျစရိတ် လျော့သည်။ chunk ၈၀၀ သည် တိကျမှု ၁
ရာခိုင်နှုန်းအမှတ် သာ ပိုပေးသဖြင့် လွှမ်းခြုံမှု ကျဆင်းနိုင်ခြေ နှင့် မမျှပါ။

**တိုင်းတာမည့် metric —** eval set အပေါ် တိကျမှု၊ recall@10၊ window ၏ အသုံးပြုမှု ရာခိုင်နှုန်း၊
chunk တစ်ခုလျှင် token ကုန်ကျစရိတ်။ ဤဆုံးဖြတ်ချက်တွင် အန္တရာယ်မှာ recall ကျဆင်းမှု ဖြစ်သဖြင့်
eval သည် အဓိက အတည်ပြုချက် ဖြစ်သည်။

#### အဖြေ ၂ — reranking depth

**ရှင်းလင်းချက် —** depth ၂၀ တွင် latency = 35 + 20 × 3.5 = ၁၀၅ ms၊ depth ၅၀ တွင် ၂၁၀ ms၊
depth ၁၀၀ တွင် ၃၈၅ ms ဖြစ်သည်။ ဘတ်ဂျက် ၂၅၀ ms အတွင်း အကြီးဆုံး depth = (250 − 35) / 3.5 = ၆၁ ဖြစ်သည်။
precision@5 သည် depth ၂၀ တွင် ၀.၅၈၊ depth ၅၀ တွင် ၀.၇၄ ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** depth ၅၀ (latency ၂၁၀ ms) ကို ရွေးရမည်၊ အကြောင်းမှာ ဘတ်ဂျက် ၂၅၀ ms အတွင်း
ဝင်ပြီး precision@5 ကို ၁၆ ရာခိုင်နှုန်းအမှတ် တိုးပေးသောကြောင့် ဖြစ်သည်။ depth ၁၀၀ သည်
၃၈၅ ms ဖြစ်၍ ဘတ်ဂျက်ကို ၅၄ % ကျော်လွန်သကဲ့သို့ ရက် ၅၀,၀၀၀ request တွင် cross-encoder
GPU-second သည် ၁,၆၆၇ မှ ၈,၃၃၃ သို့ တိုးသည် — ထပ်တိုး ၁.၈၅ GPU-hour/ရက် ($4.07/ရက်) ဖြစ်သည်။

**တိုင်းမည့် metric —** precision@5 နှင့် recall@5 (reranking နောက်)၊ retrieval latency p95 နှင့်
ရက် တစ်လျှင် cross-encoder GPU-hour။

```bash
python3 - <<'PY'
per_pair_ms, fixed_ms = 3.5, 35.0
for depth in (10, 20, 50, 100):
    lat = fixed_ms + depth * per_pair_ms
    print(f"depth {depth:3}: latency {lat:7.1f} ms  qps cap {1000 / lat:6.1f}")
print("latency 20 vs 100 ms", round((fixed_ms + 100 * per_pair_ms) - (fixed_ms + 20 * per_pair_ms), 1))
print("latency ratio 100/20", round((fixed_ms + 100 * per_pair_ms) / (fixed_ms + 20 * per_pair_ms), 2))
first_stage_recall = {"10": 0.41, "20": 0.62, "50": 0.81, "100": 0.88}
precision_at_5 = {"10": 0.34, "20": 0.58, "50": 0.74, "100": 0.80}
for d in ("10", "20", "50", "100"):
    print(f"  depth {d:3}: candidates recall {first_stage_recall[d]:.2f} -> precision@5 after rerank {precision_at_5[d]:.2f}")
print("precision@5 gain 20 -> 50 pct points", round(100 * (precision_at_5["50"] - precision_at_5["20"]), 1))
print("latency added 20 -> 50 ms", round((50 - 20) * per_pair_ms, 1))
budget_ms = 250.0
print("max depth within 250 ms retrieval budget", int((budget_ms - fixed_ms) / per_pair_ms))
print("requests/day 50000 at depth 20 -> cross-encoder GPU-seconds", round(50000 * 20 / 600))
print("requests/day 50000 at depth 100 -> cross-encoder GPU-seconds", round(50000 * 100 / 600))
print("extra GPU-hours per day at depth 100", round((50000 * 100 / 600 - 50000 * 20 / 600) / 3600, 2))
print("extra USD per day at 2.20 per GPU-hour", round((50000 * 100 / 600 - 50000 * 20 / 600) / 3600 * 2.20, 2))
PY
```

```text
depth  10: latency    70.0 ms  qps cap   14.3
depth  20: latency   105.0 ms  qps cap    9.5
depth  50: latency   210.0 ms  qps cap    4.8
depth 100: latency   385.0 ms  qps cap    2.6
latency 20 vs 100 ms 280.0
latency ratio 100/20 3.67
  depth  10: candidates recall 0.41 -> precision@5 after rerank 0.34
  depth  20: candidates recall 0.62 -> precision@5 after rerank 0.58
  depth  50: candidates recall 0.81 -> precision@5 after rerank 0.74
  depth 100: candidates recall 0.88 -> precision@5 after rerank 0.80
precision@5 gain 20 -> 50 pct points 16.0
latency added 20 -> 50 ms 105.0
max depth within 250 ms retrieval budget 61
requests/day 50000 at depth 20 -> cross-encoder GPU-seconds 1667
requests/day 50000 at depth 100 -> cross-encoder GPU-seconds 8333
extra GPU-hours per day at depth 100 1.85
extra USD per day at 2.20 per GPU-hour 4.07
```

## Self-check

၁။ အပိုင်း ၅.၁ အဖြေ ၁ တွင် chunk အရေအတွက် ဖော်မြူလာကို မည်သို့ ရေးသည်၊ overlap တိုးပါက
ဘာသောကြောင့် ထပ်မှု ပမာဏသည် အချိုးမကျ တိုးသနည်း။

၂။ အပိုင်း ၅.၁ အဖြေ ၂ တွင် memory အကြီးဆုံး အစိတ်အပိုင်းသည် ဘာလဲ၊ dimension လျှော့ခြင်းနှင့်
`M` လျှော့ခြင်း အနက် မည်သည့်အရာက memory ကို ပိုသက်သာစေသနည်း။

၃။ အပိုင်း ၅.၁ အဖြေ ၃ တွင် q4 ကို သုည သတ်မှတ်ခြင်းနှင့် ဖယ်ထုတ်ခြင်း ကွာခြားချက်က မည်မျှသနည်း။

၄။ ဥပမာ ၄ တွင် fusion သည် recall@3 ကျဆင်းသော်လည်း recall@5 တွင် အကျိုးရှိသည့် အကြောင်းရင်းက ဘာလဲ။

၅။ အပိုင်း ၅.၂ အဖြေ ၃ တွင် recall မြင့်သော်လည်း အဖြေ မှားသည့် အဓိက ယန္တရားကို ရှင်းလင်းပါ။

<details>
<summary>အဖြေများ</summary>

၁။ chunk အရေအတွက် = ⌈(N − overlap) / (size − overlap)⌉ ဖြစ်သည်။ overlap တိုးပါက denominator
သေးလာသဖြင့် chunk အရေအတွက် တိုးသည်၊ ထို့အပြင် ထပ်နေသည့် လုံးအရေအတွက်သည် (chunk − 1) × overlap
ဖြစ်သဖြင့် chunk အရေအတွက်နှင့် overlap နှစ်ခုလုံး တိုးသည့်အခါ ထပ်မှုသည် အနှစ်ချုပ် (multiplicative)
ဖြင့် တိုးသည် — အဖြေ ၁ တွင် chunk ၁.၃၃ ဆ၊ ထပ်မှု ၂.၆၅ ဆ ဖြစ်သည်။

၂။ vector ကိုယ်တိုင် ဖြစ်သည် (၈၇.၃ %)။ dimension ၁,၀၂၄ မှ ၃၈၄ သို့ လျှော့ပါက စုစုပေါင်း
၂.၆၂၁ GiB မှ ၁.၁၉ GiB သို့ ကျသည်၊ `M` ၃၂ မှ ၆၄ သို့ တိုးပါက ၂.၆၂၁ မှ ၂.၇၈၅ GiB သို့
တိုးသည် — ထို့ကြောင့် dimension လျှော့ခြင်းသည် ပိုသက်သာစေသည်။

၃။ ဖယ်ထုတ်ပါက mean recall@5 = ၀.၆၁၆၇၊ သုည သတ်မှတ်ပါက ၀.၄၆၂၅ ဖြစ်သည်၊
ကွာခြားချက် ၁၅.၄၂ ရာခိုင်နှုန်းအမှတ် ဖြစ်သည်။ ထို့ကြောင့် မူဝါဒကို ကြိုတင် သတ်မှတ်ရမည်။

၄။ `RRF` သည် စာရင်း နှစ်ခုလုံးတွင် ပါသည့် item ကို ဆုချသဖြင့် ထိပ်ဆုံး သုံးခုတွင်
single retriever က သာ ပါသည့် သက်ဆိုင်သည့် item (d1၊ d5) ကို ဖယ်လိုက်သည်။ K ကျယ်လာသည့်အခါ
ထို item များ ပြန်ပါလာသဖြင့် လွှမ်းခြုံမှု ပြည့်သည် (recall@5 = ၁.၀)။

၅။ `Recall@K` သည် retrieval အဆင့်တစ်ခု သက်ဆိုင်သည့် candidate များ လုံလောက်စွာ ပေးနိုင်မှုကိုသာ
တိုင်းသည်။ ranking အစဉ်၊ reranking နောက် ကျန်သည့် စာရင်း နှင့် အဖြေ grounded ဖြစ်မှုကို
မတိုင်းပါ — ထို့ကြောင့် recall မြင့်သော်လည်း သက်ဆိုင်သည့် chunk သည် prompt ထဲ မဝင်နိုင်ဘဲ
အဖြေ မှားနိုင်သည်။

</details>

## References

- နယ်ပယ် အခြေခံ အချက်အလက် — `terms/04_retrieval_and_generation.md` နှင့် `glossary/by_area/04_retrieval_and_generation.json`။
- Source glossary — [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed, from `rohitg00/ai-engineering-from-scratch`။
- [Dense Passage Retrieval](https://aclanthology.org/2020.emnlp-main.550/)၊ [Efficient and Robust Approximate Nearest Neighbor Search Using HNSW](https://dl.acm.org/doi/10.1109/TPAMI.2018.2889473)၊ [BEIR](https://openreview.net/forum?id=wCu6T5xFjeJ)။
- [The Probabilistic Relevance Framework: BM25 and Beyond](https://doi.org/10.1561/1500000019)၊ [Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods](https://dl.acm.org/doi/10.1145/1571941.1572114)၊ [The Use of MMR](https://www.cs.cmu.edu/~jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf)။
- [Retrieval-Augmented Generation paper](https://arxiv.org/abs/2005.11401)။
- ကိန်းဂဏန်း script များ — `~/.hermes/profiles/ai-engineer/cache/scratch/glossary_guide_04/` (Python standard library သာ)။
