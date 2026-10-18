# ၀၄ — လေ့ကျင့်ခန်းများနှင့် အဖြေများ (Evaluation & Safety)

ဤဖိုင်သည် နယ်ပယ် ၀၇ ၏ term ၁၇ ခုကို အသုံးပြု၍ တွက်ချက်ခြင်း၊ ပြဿနာ ရှာဖွေခြင်းနှင့် ဆုံးဖြတ်ချက်
ချခြင်း လေ့ကျင့်ခန်းများကို စုစည်းထားသည်။ အပိုင်း ၁ တွင် အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာ လေးခု၊
အပိုင်း ၂ တွင် တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ခြောက်ခု၊ အပိုင်း ၃ တွင် ပြဿနာ ရှာဖွေခြင်း သုံးခု၊
အပိုင်း ၄ တွင် ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း နှစ်ခု ပါဝင်သည်။ အပိုင်း ၅ တွင် အဖြေတိုင်းကို
ဖော်မြူလာ၊ တွက်ချက်မှု အဆင့်ဆင့်နှင့် အကြောင်းရင်း ရှင်းလင်းချက်နှင့်အတူ ပေးထားသည်။

အပိုင်း ၁ နှင့် အပိုင်း ၅ တွင် ပါဝင်သည့် ကိန်းဂဏန်း တိုင်းသည် Python (standard library သာ) ဖြင့်
အမှန်တကယ် လုပ်ဆောင်ခဲ့သည့် တွက်ချက်မှု၏ output ဖြစ်သည်။ ဖော်ပြထားသည့် command အတိုင်း
run လုပ်ပါက တူညီသည့် output ကို ပြန်လည် ရရှိမည်။ ကိန်းဂဏန်း တိုင်းသည် သတ်မှတ်ထားသည့်
sample size၊ price နှင့် distribution အပေါ် မှီခိုသည်၊ ထို့ကြောင့် ဖော်မြူလာ တစ်ခုစီနှင့်အတူ
၎င်း၏ ယူဆချက် (assumption) ကို ဖော်ပြထားသည်။

## ၁။ အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာများ (Worked Examples)

### ဥပမာ ၁ — Contamination rate နှင့် benchmark score အပေါ် ၎င်း၏ လွှမ်းမိုးမှု

**ယူဆချက် —** Eval set တွင် item ၄၀၀ ပါသည်။ ထို item အနက် ၅၂ ခုသည် training corpus ထဲတွင်
အတိအကျ သို့မဟုတ် အနီးစပ်ဆုံး ထပ်နေသည် (contamination rate 13.0 % ဖြစ်သည်)။ Model သည်
item အားလုံးအပေါ် ၃၃၈ ခုကို မှန်သည်၊ ၎င်း အနက် contaminated item ၅၂ ခုအပေါ် ၅၀ ခု မှန်သည်။

**ဖော်မြူလာ —**

- reported score = cr × accuracy_on_contaminated + (1 − cr) × accuracy_on_clean
- inflation = reported score − accuracy_on_clean
- item တစ်ခုလျှင် လွှမ်းမိုးမှု = (accuracy_on_contaminated − accuracy_on_clean) / item စုစုပေါင်း

**တွက်ချက်မှု —**

1. Contamination rate = 52 / 400 = 13.0 % ဖြစ်သည်။ Clean item = 400 − 52 = 348 ဖြစ်သည်။
2. Reported score = 338 / 400 = 84.5 % ဖြစ်သည်။
3. Contaminated item အပေါ် တိကျမှု = 50 / 52 = 96.15 % ဖြစ်သည်။
4. Clean item အပေါ် တိကျမှု = (338 − 50) / 348 = 288 / 348 = 82.76 % ဖြစ်သည်။
5. Mix ဖော်မြူလာဖြင့် ပြန်စစ်ပါက 0.13 × 96.15 + 0.87 × 82.76 = 84.50 % ဖြစ်သည်။
6. Inflation = 84.50 − 82.76 = 1.74 ရာခိုင်နှုန်းအမှတ် ဖြစ်သည်။
7. Item တစ်ခုလျှင် လွှမ်းမိုးမှု = (96.15 − 82.76) / 400 = 0.0335 ရာခိုင်နှုန်းအမှတ် ဖြစ်သည်ဟု
   တွက်ပါက inflation ၁ ရာခိုင်နှုန်းအမှတ်ကို ဖယ်ရှားရန် contaminated item ၂၉.၉ ခု လိုအပ်သည်။
8. Contamination rate ၂၆ % ဖြစ်လာပါက reported score = 86.24 % (inflation 3.48 ရာခိုင်နှုန်းအမှတ်)၊
   ၅၀ % ဖြစ်လာပါက 89.46 % (inflation 6.70 ရာခိုင်နှုန်းအမှတ်) ဖြစ်သည်။

**ကောက်ချက် —** Contamination သည် score ကို တိုက်ရိုက် ဖောင်းပွစေသည်၊ ၎င်း၏ လွှမ်းမိုးမှုသည်
contaminated item များ၏ တိကျမှုနှင့် clean item များ၏ တိကျမှု ကွာခြားချက်အပေါ် အချိုးကျသည်။
ထို့ကြောင့် score တစ်ခုကို ဖတ်သည့်အခါ "မည်သည့် data အပေါ် တိုင်းတာသည်နှင့် contamination
ရှိမရှိ" ကို ဦးစွာ စစ်ရမည်။ Clean subset အပေါ် တိကျမှု (82.76 %) သည် generalize လုပ်နိုင်စွမ်းကို
ပိုမို ဖော်ပြသည်။

```bash
python3 - <<'PY'
items = 400
contaminated = 52
clean = items - contaminated
overall = 338
on_cont = 50
on_clean = overall - on_cont

print("--- contamination rate and its effect on the score ---")
print("contaminated", contaminated, "clean", clean)
print("overall correct", overall, "pct", round(100 * overall / items, 2))
print("contamination rate pct", round(100 * contaminated / items, 2))
print("accuracy on contaminated pct", round(100 * on_cont / contaminated, 2))
print("accuracy on clean pct       ", round(100 * on_clean / clean, 2))
print("inflation pt", round(100 * overall / items - 100 * on_clean / clean, 2))
for cr in (0.0, 0.13, 0.26, 0.50):
    mix = cr * on_cont / contaminated + (1 - cr) * on_clean / clean
    print(f"contamination {100*cr:4.0f} pct -> reported {100*mix:5.2f} pct"
          f"  inflation {100*mix - 100*on_clean/clean:5.2f} pt")
print("adjusted score if contaminated items scored at clean rate",
      round(100 * (on_clean + contaminated * on_clean / clean) / items, 2))
print("items to fix to remove 1 pt of inflation",
      round(1.0 / (100 * (on_cont / contaminated - on_clean / clean) / items), 1))
PY
```

```text
--- contamination rate and its effect on the score ---
contaminated 52 clean 348
overall correct 338 pct 84.5
contamination rate pct 13.0
accuracy on contaminated pct 96.15
accuracy on clean pct        82.76
inflation pt 1.74
contamination    0 pct -> reported 82.76 pct  inflation  0.00 pt
contamination   13 pct -> reported 84.50 pct  inflation  1.74 pt
contamination   26 pct -> reported 86.24 pct  inflation  3.48 pt
contamination   50 pct -> reported 89.46 pct  inflation  6.70 pt
adjusted score if contaminated items scored at clean rate 82.76
items to fix to remove 1 pt of inflation 29.9
```

### ဥပမာ ၂ — Pass@k ကို သတ်မှတ်ထားသည့် အစုမှ တွက်ချက်ခြင်း

**ယူဆချက် —** အလုပ်တစ်ခုကို သတ်မှတ်ထားသည့် configuration အောက်တွင် သီးခြားစီ ၁၀ ကြိမ်
နမူနာယူသည် (n = 10)။ ထို candidate ၁၀ ခုအနက် ၂ ခုသည် သီးသန့် test ကို အောင်သည် (c = 2)။
Task set ကြီးတစ်ခုတွင် အလုပ် ၃၀ ခု ရှိသည်၊ လျာထားချက် ၃၀၀ အနက် ၆၀ ခု အောင်သည်၊
အနည်းဆုံး တစ်ခု အောင်သည့် အလုပ် ၁၈ ခု ရှိသည်ဟု ယူသည်။

**ဖော်မြူလာ —**

- pass@k (unbiased estimator၊ အလုပ် တစ်ခုအတွက်) = 1 − C(n − c, k) / C(n, k)
- empirical pass@k (task set အတွက်) = အနည်းဆုံး တစ်ခု အောင်သည့် အလုပ် / အလုပ် စုစုပေါင်း
- candidate တိုင်း သီးခြားစီ p ဖြင့် အောင်ပါက မျှော်မှန်းချက် = 1 − (1 − p)^k

**တွက်ချက်မှု —**

1. pass@1 = 1 − C(8, 1) / C(10, 1) = 1 − 8 / 10 = 0.2000 ဖြစ်သည်။
2. pass@3 = 1 − C(8, 3) / C(10, 3) = 1 − 56 / 120 = 0.5333 ဖြစ်သည်။
3. pass@5 = 1 − C(8, 5) / C(10, 5) = 1 − 56 / 252 = 0.7778 ဖြစ်သည်။
4. pass@10 = 1 − C(8, 10) / C(10, 10) = 1 − 0 / 1 = 1.0000 ဖြစ်သည်။
5. Candidate အဆင့် အောင်နှုန်း = 60 / 300 = 20.0 % ဖြစ်သည်။ ဤတန်ဖိုးသည် pass@k မဟုတ်ပါ။
6. Empirical pass@10 = 18 / 30 = 60.0 % ဖြစ်သည်။
7. Candidate တိုင်း ၂၀ % ဖြင့် သီးခြားစီ အောင်သည်ဟု ယူပါက မျှော်မှန်းချက်သည်
   k = 1 တွင် 20.00 %၊ k = 2 တွင် 36.00 %၊ k = 4 တွင် 59.04 %၊ k = 6 တွင် 73.79 %၊
   k = 8 တွင် 83.22 %၊ k = 10 တွင် 89.26 % ဖြစ်သည်။

**ကောက်ချက် —** Pass@k သည် model ပြောင်းလဲခြင်း မရှိဘဲ k တိုးရုံဖြင့် တက်သည်။ ထို့ကြောင့်
score တစ်ခုကို ကြားသည့်အခါ k နှင့် sampling အသေးစိတ်ကို တောင်းရမည်။ မြင့်မားသည့် pass@k သည်
"ပိုကောင်းသည့် ပထမဆုံး အဖြေ" ကို မဆိုလိုဘဲ ပိုကြီးမားသည့် attempt budget ကို ထင်ဟပ်နိုင်သည်။

```bash
python3 - <<'PY'
from math import comb

print("--- pass@k for one task, from n samples with c passing ---")
n, c = 10, 2
for k in (1, 3, 5, 10):
    num = comb(n - c, k) if n - c >= k else 0
    est = 1 - num / comb(n, k)
    print(f"n={n} c={c} k={k:<2} C(n-c,k)={num:5d} C(n,k)={comb(n,k):6d} pass@{k} = {est:.4f}")

print()
print("--- across a task set ---")
tasks, samples = 30, 10
candidates = tasks * samples
passing = 60
with_pass = 18
print("candidates", candidates, "passing", passing,
      "candidate pass rate pct", round(100 * passing / candidates, 2))
print("tasks with at least one pass", with_pass, "pass@10 pct",
      round(100 * with_pass / tasks, 2))
print("candidate level pass rate", round(100 * passing / candidates, 2),
      "pct is not pass@k")
for kk in (1, 2, 4, 6, 8, 10):
    print(f"k={kk:<2} expected pass@k at 0.20 per candidate = {100*(1-(1-0.2)**kk):5.2f} pct")
PY
```

```text
--- pass@k for one task, from n samples with c passing ---
n=10 c=2 k=1  C(n-c,k)=    8 C(n,k)=    10 pass@1 = 0.2000
n=10 c=2 k=3  C(n-c,k)=   56 C(n,k)=   120 pass@3 = 0.5333
n=10 c=2 k=5  C(n-c,k)=   56 C(n,k)=   252 pass@5 = 0.7778
n=10 c=2 k=10 C(n-c,k)=    0 C(n,k)=     1 pass@10 = 1.0000

--- across a task set ---
candidates 300 passing 60 candidate pass rate pct 20.0
tasks with at least one pass 18 pass@10 pct 60.0
candidate level pass rate 20.0 pct is not pass@k
k=1  expected pass@k at 0.20 per candidate = 20.00 pct
k=2  expected pass@k at 0.20 per candidate = 36.00 pct
k=4  expected pass@k at 0.20 per candidate = 59.04 pct
k=6  expected pass@k at 0.20 per candidate = 73.79 pct
k=8  expected pass@k at 0.20 per candidate = 83.22 pct
k=10 expected pass@k at 0.20 per candidate = 89.26 pct
```

### ဥပမာ ၃ — သတ်မှတ်ထားသည့် confusion matrix အတွက် precision, recall နှင့် F1

**ယူဆချက် —** Guardrail classifier တစ်ခုကို request ၅၀၀ အပေါ် စမ်းသပ်သည်။ သက်ဆိုင်သည့်
request အရေအတွက်သည် ၅၀ ဖြစ်သည် (prevalence 10.0 % ဖြစ်သည်)။ Threshold နှစ်ခုကို
နှိုင်းယှဉ်သည် — threshold 0.50 တွင် TP = 42၊ FP = 18၊ FN = 8၊ TN = 432 ဖြစ်သည်၊
threshold 0.30 တွင် TP = 48၊ FP = 52၊ FN = 2၊ TN = 398 ဖြစ်သည်။

**ဖော်မြူလာ —**

- precision = TP / (TP + FP)
- recall = TP / (TP + FN)
- F1 = 2 × precision × recall / (precision + recall)
- false-positive rate = FP / (FP + TN)

**တွက်ချက်မှု —**

1. Threshold 0.50: precision = 42 / 60 = 0.7000 ဖြစ်သည်။ Recall = 42 / 50 = 0.8400 ဖြစ်သည်။
2. F1 = 2 × 0.70 × 0.84 / (0.70 + 0.84) = 1.176 / 1.54 = 0.7636 ဖြစ်သည်။
3. Threshold 0.50: accuracy = (42 + 432) / 500 = 0.9480 ဖြစ်သည်။
4. Threshold 0.30: precision = 48 / 100 = 0.4800 ဖြစ်သည်။ Recall = 48 / 50 = 0.9600 ဖြစ်သည်။
5. F1 = 2 × 0.48 × 0.96 / (0.48 + 0.96) = 0.9216 / 1.44 = 0.6400 ဖြစ်သည်။
6. Threshold 0.30 ၏ false-positive rate = 52 / (52 + 398) = 0.1156 ဖြစ်သည်။
7. Request ၁၀,၀၀၀ သို့ တိုးပါက threshold 0.30 သည် request ၂,၀၀၀ ကို အမှတ်အသားပြုသည်၊
   ၎င်းအနက် ၁,၀၄၀ ခုသည် မှားသည် (false block)၊ လွတ်သွားသည့် violation သည် ၄၀ ခု ဖြစ်သည်။

**ကောက်ချက် —** Threshold လျှော့ချခြင်းသည် recall ကို 0.84 မှ 0.96 သို့ တင်ပေးသော်လည်း
precision ကို 0.70 မှ 0.48 သို့ ချသည်။ F1 သည် 0.7636 မှ 0.6400 သို့ ကျသည်။ Accuracy သည်
0.9480 မှ 0.8920 သို့ ကျသော်လည်း accuracy ကို ဤအခြေအနေတွင် မကြည့်သင့်ပါ — အမှား နှစ်မျိုး၏
ကုန်ကျစရိတ်သည် တူညီခြင်း မရှိသည့်အတွက် မှန်ကန်သည့် metric သည် အမှား တစ်ခုစီ၏ ကုန်ကျစရိတ်နှင့်
ပစ်မှတ် class ၏ အဖြစ်အများအပြားအပေါ် မူတည်သည်။

```bash
python3 - <<'PY'
def report(name, tp, fp, fn, tn):
    p = tp / (tp + fp)
    r = tp / (tp + fn)
    f = 2 * p * r / (p + r)
    acc = (tp + tn) / (tp + fp + fn + tn)
    print(f"{name}: TP={tp} FP={fp} FN={fn} TN={tn}")
    print(f"  flagged {tp+fp} relevant {tp+fn} precision {p:.4f} recall {r:.4f}"
          f" F1 {f:.4f} accuracy {acc:.4f}")
    print(f"  prevalence {(tp+fn)/(tp+fp+fn+tn):.4f}  false-positive rate {fp/(fp+tn):.4f}")

print("--- precision and recall at two thresholds ---")
report("threshold 0.50", 42, 18, 8, 432)
report("threshold 0.30", 48, 52, 2, 398)
print()
print("F1 cross-check", round(2*0.70*0.84/(0.70+0.84), 4), round(2*0.48*0.96/(0.48+0.96), 4))
print("per 10000 requests at threshold 0.30: flagged", 10000*(48+52)/500,
      "missed", 10000*2/500, "false blocks", 10000*52/500)
PY
```

```text
--- precision and recall at two thresholds ---
threshold 0.50: TP=42 FP=18 FN=8 TN=432
  flagged 60 relevant 50 precision 0.7000 recall 0.8400 F1 0.7636 accuracy 0.9480
  prevalence 0.1000  false-positive rate 0.0400
threshold 0.30: TP=48 FP=52 FN=2 TN=398
  flagged 100 relevant 50 precision 0.4800 recall 0.9600 F1 0.6400 accuracy 0.8920
  prevalence 0.1000  false-positive rate 0.1156

F1 cross-check 0.7636 0.64
per 10000 requests at threshold 0.30: flagged 2000.0 missed 40.0 false blocks 1040.0
```

### ဥပမာ ၄ — Eval run တစ်ကြိမ်၏ ကုန်ကျစရိတ်

**ယူဆချက် —** Eval set တွင် item ၄၀၀ ပါသည်။ Generator သည် item တစ်ခုလျှင် input token ၈၅၀
နှင့် output token ၂၂၀ ကို သုံးသည်၊ input သည် ၁ သန်း token လျှင် USD 3.00 နှင့် output သည်
USD 15.00 ဖြစ်သည်။ Judge model ကို item ၁၂၀ အပေါ် သုံးသည်၊ ၎င်း၏ input သည် item တစ်ခုလျှင်
token ၁၆၀၀ နှင့် output သည် ၆၀ token ဖြစ်သည်။

**ဖော်မြူလာ —**

- cost = input token / 10⁶ × price_input + output token / 10⁶ × price_output
- per item cost = run တစ်ကြိမ်၏ cost / item အရေအတွက်
- run အရေအတွက် = development iteration + final run

**တွက်ချက်မှု —**

1. Generator input = 400 × 850 = 340,000 token၊ output = 400 × 220 = 88,000 token ဖြစ်သည်။
2. Generator cost = 0.34 × 3.00 + 0.088 × 15.00 = 1.02 + 1.32 = USD 2.34 ဖြစ်သည်။
3. Judge input = 120 × 1600 = 192,000 token၊ output = 120 × 60 = 7,200 token ဖြစ်သည်။
4. Judge cost = 0.192 × 3.00 + 0.0072 × 15.00 = 0.576 + 0.108 = USD 0.684 ဖြစ်သည်။
5. Run တစ်ကြိမ် = USD 3.024 ဖြစ်သည်၊ item တစ်ခုလျှင် USD 0.00756 ဖြစ်သည်။
6. Dev iteration ၆ ကြိမ် + final ကြိမ် တစ်ခု = ၇ ကြိမ် = USD 21.168 ဖြစ်သည်၊
   ပြန်လည် run ရန် ၂၀ % ချန်ထားပါက USD 25.4016 ဖြစ်သည်။
7. Item တစ်ခုလျှင် ၉ စက္ကန့်၊ concurrency ၃ ဖြင့် run တစ်ကြိမ်သည် ၂၀.၀ မိနစ် ကြသည်၊
   ၇ ကြိမ်အတွက် ၁၄၀.၀ မိနစ် (၂.၃၃ နာရီ) ဖြစ်သည်။

**ကောက်ချက် —** Eval ကုန်ကျစရိတ်သည် item အရေအတွက်နှင့် run အရေအတွက် နှစ်ခုလုံးအပေါ်
အချိုးကျသည်။ Judge သည် item အနည်းငယ်အပေါ်သာ run သော်လည်း input token ကြီးသည့်အတွက်
ကုန်ကျစရိတ်၏ ၂၂.၆ % ကို ယူသည်။ ထို့ကြောင့် dev iteration ကို စျေးပေါသော scorer ဖြင့်
လုပ်ပြီး ကြီးသည့် scorer ကို ရွေးချယ်မှု အနည်းငယ်အတွက်သာ သုံးခြင်းသည် တန်ဖိုးရှိသည့် မူဝါဒ ဖြစ်သည်။

```bash
python3 - <<'PY'
items, in_tok, out_tok = 400, 850, 220
price_in, price_out = 3.00, 15.00
gen_in, gen_out = items * in_tok, items * out_tok
gen_cost = gen_in / 1e6 * price_in + gen_out / 1e6 * price_out

print("--- cost of one eval run ---")
print("generator input tokens ", gen_in, "output tokens", gen_out)
print("generator cost USD     ", round(gen_cost, 4))
judge_items, j_in, j_out = 120, 1600, 60
j_in_t, j_out_t = judge_items * j_in, judge_items * j_out
j_cost = j_in_t / 1e6 * price_in + j_out_t / 1e6 * price_out
print("judge items", judge_items, "input", j_in_t, "output", j_out_t,
      "cost USD", round(j_cost, 4))
per_run = gen_cost + j_cost
print("per run USD", round(per_run, 4), "per item USD", round(per_run / items, 6))
runs = 6 + 1
print("7 runs USD", round(runs * per_run, 4), "with 20 pct retry",
      round(runs * per_run * 1.2, 4))
conc, sec = 3, 9.0
mins = items / conc * sec / 60
print("wall clock one run min", round(mins, 2), "for 7 runs min",
      round(7 * mins, 2), "h", round(7 * mins / 60, 2))
print("cost of 10 dev configs on 700 items USD", round(10 * 700 * (per_run / items), 4))
print("cost of one held-out run on 500 items USD", round(500 * (per_run / items), 4))
PY
```

```text
--- cost of one eval run ---
generator input tokens  340000 output tokens 88000
generator cost USD      2.34
judge items 120 input 192000 output 7200 cost USD 0.684
per run USD 3.024 per item USD 0.00756
7 runs USD 21.168 with 20 pct retry 25.4016
wall clock one run min 20.0 for 7 runs min 140.0 h 2.33
cost of 10 dev configs on 700 items USD 52.92
cost of one held-out run on 500 items USD 3.78
```

## ၂။ တွက်ချက်ရသည့် လေ့ကျင့်ခန်းများ (Calculation Exercises)

လေ့ကျင့်ခန်း တစ်ခုစီတွင် ကိန်းဂဏန်း အဖြေ အတိအကျ ရှိသည်။ အဖြေနှင့် ဖော်မြူလာ ရှင်းလင်းချက်ကို
အပိုင်း ၅.၁ တွင် ပေးထားသည်။

**လေ့ကျင့်ခန်း ၁ — သတ်မှတ်ထားသည့် confidence အတွက် လိုအပ်သည့် eval size**

(က) p = 0.5၊ 0.85 နှင့် 0.9 အတွက် half-width ±5၊ ±3 နှင့် ±2 ရာခိုင်နှုန်းအမှတ် (95 % confidence)
လိုအပ်သည့် item အရေအတွက် (ခ) လူဦးရေ N = 5,000 အတွက် finite population correction ဖြင့်
p = 0.5၊ half-width ±3 အတွက် n (ဂ) n = 100၊ 200၊ 400၊ 500၊ 1,000 နှင့် 1,068 တွင် p = 0.90
အတွက် margin နှင့် item တစ်ခုလျှင် ရာခိုင်နှုန်းအမှတ် (ဃ) တစ်ဘက် 95 % (one-sided) အတွက်
p = 0.9၊ half-width ±3 တွင် n။

**လေ့ကျင့်ခန်း ၂ — သတ်မှတ်ထားသည့် အစုမှ pass@k**

n = 10၊ c = 2 ရှိသည့် အလုပ်တစ်ခုအတွက် (က) pass@1၊ pass@3၊ pass@5 နှင့် pass@10 (ခ) အလုပ် ၃၀ ခု၊
လျာထားချက် ၃၀၀၊ အောင်သည့် လျာထားချက် ၆၀၊ အနည်းဆုံး တစ်ခု အောင်သည့် အလုပ် ၁၈ ခု အတွက်
candidate အဆင့် အောင်နှုန်းနှင့် empirical pass@10 (ဂ) candidate တိုင်း ၀.၂၀ ဖြင့် သီးခြားစီ အောင်ပါက
k = 1၊ 2၊ 4၊ 6၊ 8 နှင့် 10 အတွက် မျှော်မှန်းချက် (ဃ) k = 1 နှင့် k = 10 ၏ ကွာခြားမှုသည်
model တိုးတက်မှုကို ဖော်ပြသလား။

**လေ့ကျင့်ခန်း ၃ — contamination rate နှင့် score အပေါ် ၎င်း၏ လွှမ်းမိုးမှု**

(က) item ၄၀၀၊ contaminated ၅၂၊ overall မှန်သည့် item ၃၃၈၊ contaminated item အပေါ် မှန်သည့်
item ၅၀ အတွက် contamination rate၊ reported score၊ contaminated item အပေါ် တိကျမှုနှင့် clean item
အပေါ် တိကျမှု (ခ) inflation (ဂ) contamination rate ၂၆ % နှင့် ၅၀ % ဖြစ်ပါက reported score
(ဃ) inflation ၁ ရာခိုင်နှုန်းအမှတ်ကို ဖယ်ရှားရန် ပြုပြင်ရမည့် contaminated item အရေအတွက်
(င) clean subset အပေါ် score သည် အဘယ်ကြောင့် ပိုမို ယုံထိုက်သည်။

**လေ့ကျင့်ခန်း ၄ — eval run တစ်ကြိမ်၏ ကုန်ကျစရိတ်**

Item ၄၀၀၊ generator input ၈၅၀ token နှင့် output ၂၂၀ token၊ input USD 3.00 / 1M နှင့်
output USD 15.00 / 1M၊ judge item ၁၂၀၊ judge input ၁,၆၀၀ token နှင့် output ၆၀ token။
(က) generator ၏ input နှင့် output token (ခ) generator cost (ဂ) judge cost (ဃ) run တစ်ကြိမ်၏
cost နှင့် item တစ်ခုလျှင် cost (င) run ၇ ကြိမ်အတွက် cost နှင့် ၂၀ % retry အနားသတ် ထည့်ပါက
cost (စ) item တစ်ခုလျှင် ၉ စက္ကန့်၊ concurrency ၃ ဖြင့် run တစ်ကြိမ်နှင့် run ၇ ကြိမ်၏
အချိန် (ဆ) judge cost သည် run တစ်ကြိမ်၏ မည်မျှ ရာခိုင်နှုန်း ဖြစ်သည်။

**လေ့ကျင့်ခန်း ၅ — သတ်မှတ်ထားသည့် confusion matrix အတွက် precision နှင့် recall**

Threshold နှစ်ခု — 0.50 တွင် TP = 42၊ FP = 18၊ FN = 8၊ TN = 432၊ 0.30 တွင် TP = 48၊ FP = 52၊
FN = 2၊ TN = 398။ (က) threshold တစ်ခုစီ၏ precision၊ recall နှင့် accuracy (ခ) F1 နှစ်ခု
(ဂ) recall ကို သုညမှ တစ်သို့ တင်ရန် precision ကို မည်သည့် အတိုင်းအတာအထိ လျှော့ရသည်
(ဃ) request ၁၀,၀၀၀ တွင် threshold 0.30 ၏ အမှတ်အသားပြုမှု၊ false block နှင့် လွတ်သွားသည့်
violation အရေအတွက် (င) prevalence ၁၀ % မှ ၁ % သို့ ကျပါက threshold 0.50 ၏ precision မည်သို့
ပြောင်းသည်။

**လေ့ကျင့်ခန်း ၆ — window နှစ်ခုမှ drift threshold**

Baseline window တွင် n = 1,200၊ accuracy 0.912၊ လက်ရှိ window တွင် n = 800၊ accuracy 0.871။
(က) ကွာခြားမှု ရာခိုင်နှုန်းအမှတ် (ခ) ကွာခြားမှု၏ standard error နှင့် z တန်ဖိုး (ဂ) 2 se နှင့်
3 se သတိပေးချက် threshold (ဃ) 95 % ယုံကြည်မှု ကြားကာလ (င) slice n = 200/140 နှင့် n = 150/100
အတွက် se နှင့် z (slice ငယ်လျှင် အဘယ်ကြောင့် သတိပေးချက် မထွက်သည်)။

## ၃။ ပြဿနာ ရှာဖွေခြင်း (Troubleshooting Scenarios)

ပြဿနာ တစ်ခုစီကို symptom၊ တိုင်းတာရမည့် အချက်၊ ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်)၊
ဖြေရှင်းနည်းနှင့် ရှင်းလင်းသည့် term ဟူသည့် အစဉ်အတိုင်း ဖော်ပြထားသည်။ အကြောင်းရင်း အစဉ်သည်
တိုင်းတာမှုဖြင့် ရှာဖွေနိုင်သည့် အစဉ်အတိုင်း ဖြစ်သည်။ အသေးစိတ် ရှင်းလင်းချက်ကို အပိုင်း ၅.၂
တွင် ပေးထားသည်။

### ပြဿနာ ၁ — score သည် run တစ်ကြိမ်နှင့် တစ်ကြိမ် မတူညီခြင်း

- **Symptom —** တူညီသည့် eval set ကို ပြန် run သည့်အခါ စုစုပေါင်း score သည် ရာခိုင်နှုန်းအမှတ်
  အနည်းငယ် လှုပ်ရှားသည်၊ မည်သည့် ပြောင်းလဲမှုက ထို လှုပ်ရှားမှုကို ဖြစ်စေသည်ကို မခွဲခြားနိုင်။
- **တိုင်းတာရမည့် အချက် —** run ၃–၅ ကြိမ်၏ score ပျမ်းမျှနှင့် လှုပ်ရှားမှု အတိုင်းအတာ၊ failure item
  များသည် run တိုင်းတွင် တူညီသလား၊ generator ၏ temperature နှင့် seed တန်ဖိုး၊ judge model ၏
  version နှင့် score များ၏ လှုပ်ရှားမှု၊ eval set ၏ version နှင့် checksum၊ retrieval index ၏
  snapshot။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) sampling parameter (temperature၊ seed)
  သတ်မှတ်မထားသဖြင့် output တိုင်း မတူညီခြင်း၊ (၂) judge model ကို version မချိတ်ထားသဖြင့်
  scorer ကိုယ်တိုင် ပြောင်းလဲခြင်း၊ (၃) eval set သို့မဟုတ် retrieval index ကို run အကြား
  ပြင်ဆင်မိခြင်း၊ (၄) parallelism နှင့် timeout ကြောင့် item အချို့ မပါဝင်ခြင်း၊ (၅) output ကို
  normalize လုပ်သည့် စည်းမျဉ်း မတည်ငြိမ်ခြင်း။
- **ဖြေရှင်းနည်း —** Eval set၊ judge version နှင့် retrieval snapshot ကို version ချိတ်ပြီး
  ဖွင့်ထားရမည်၊ sampling parameter ကို သတ်မှတ်ရမည်၊ judge score ကို လူသား ပြန်လည်စစ်ဆေးထားသည့်
  နမူနာများနှင့် ချိန်ညှိရမည်၊ run တစ်ကြိမ်တည်း၏ score ကို ကိုးကားမည့်အစား ကြိမ်များစွာ၏
  ပျမ်းမျှနှင့် အတိုင်းအတာကို အစီရင်ခံရမည်။
- **ရှင်းလင်းသည့် term —** Evaluation (Eval)၊ Eval Set၊ LLM-as-a-Judge၊ Exact Match (EM)၊ Calibration။

### ပြဿနာ ၂ — Benchmark score မြင့်သည်၊ သို့သော် ထုတ်လုပ်မှုတွင် ဆိုးသည်

- **Symptom —** public benchmark အပေါ် score သည် ပြိုင်ဘက်များထက် မြင့်သည်၊ သို့သော် deploy
  လုပ်ပြီးနောက် အသုံးပြုသူ အစီရင်ခံချက်များနှင့် လက်တွေ့ တိုင်းတာမှုများသည် ကျဆင်းသည်။
- **တိုင်းတာရမည့် အချက် —** deploy လုပ်မည့် slice အလိုက် စွမ်းဆောင်ရည်၊ ထုတ်လုပ်မှု input ၏
  လက္ခဏာများ (အရှည်၊ ဘာသာစကား၊ task အမျိုးအစား)၊ training corpus နှင့် benchmark ထပ်နေမှု၊
  held-out set ကို မည်မျှကြာ ချိန်ညှိခဲ့သည်၊ confidence အဆင့်အလိုက် လက်တွေ့ တိကျမှု၊ metric နှင့်
  လက်တွေ့ အသုံးဝင်မှု ကွာခြားချက်။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) benchmark contamination ကြောင့် score သည်
  ယခင် ကြုံဖူးမှုကို ထင်ဟပ်ခြင်း၊ (၂) distribution shift ကြောင့် အသုံးပြုသူ၊ အလုပ်၊ ဘာသာစကား
  သို့မဟုတ် tool ပြောင်းလဲခြင်း၊ (၃) held-out set ကို ထပ်ခါတလဲလဲ ချိန်ညှိခြင်းကြောင့် test
  အချက်အလက် ယိုစိမ့်ခြင်း၊ (၄) metric သည် canonical အဖြေ တစ်ခုတည်းကို တိုင်းသော်လည်း
  လက်တွေ့ အလုပ်တွင် အဖြေ များစွာ မှန်ကန်နိုင်ခြင်း၊ (၅) confidence လွန်ကဲသဖြင့် ယုံထိုက်မှု
  မရှိသည့် အခြေအနေတွင် ဆုံးဖြတ်ချက် ချခြင်း။
- **ဖြေရှင်းနည်း —** ထုတ်လုပ်မှုမှ နမူနာယူထားသည့် case များဖြင့် version စီမံထားသည့် eval set
  အသစ် ဖွဲ့ရမည်၊ slice အလိုက် တိုင်းတာရမည်၊ training source တွင် အတိအကျနှင့် အနီးစပ်ဆုံး
  ထပ်နေသည့် အရာများကို ရှာဖွေရမည်၊ ကျရှုံးမှု အသစ်များကို eval set ထဲသို့ ထည့်ရမည်၊
  calibration ကို တိုင်း၍ ကွာဟမှု လက်မခံနိုင်လောက်ပါက recalibrate လုပ်ခြင်း သို့မဟုတ်
  အဖြေပေးခြင်းမှ ရှောင်ကြဉ်ခြင်း ပြုလုပ်ရမည်။
- **ရှင်းလင်းသည့် term —** Benchmark Contamination၊ Distribution Shift၊ Eval Set၊ Calibration၊
  Model Card၊ Exact Match (EM)။

### ပြဿနာ ၃ — Guardrail သည် တရားဝင်သည့် request များကို ပိတ်ဆို့ခြင်း

- **Symptom —** ဘေးကင်းရေး ထိန်းချုပ်မှု ထည့်ပြီးနောက် တရားဝင်သည့် အသုံးပြုသူ request များ
  ပိတ်ဆို့ခံရသည်၊ အသုံးပြုသူ အစီရင်ခံချက် တိုးလာသည်၊ ဆိုးသည့် request များ လွတ်သွားသည်ကို
  မသိရသေးပါ။
- **တိုင်းတာရမည့် အချက် —** false-block rate (တရားဝင် request များထဲမှ ပိတ်ဆို့ခံရသည့် အချိုး)၊
  violation recall (ဆိုးသည့် request များထဲမှ ဖမ်းမိသည့် အချိုး)၊ threshold အလိုက် metric နှစ်ခု၏
  လဲလှယ်မှု၊ traffic ထဲရှိ violation ၏ prevalence၊ ပိတ်ဆို့ခံရသည့် request များ၏ slice ဖြန့်ကျက်မှု။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) threshold ကို recall ဘက်သို့ အလွန်အကျွံ
  လျှော့ချမိခြင်း၊ (၂) classifier ကို မတူညီသည့် domain သို့မဟုတ် မတူညီသည့် prevalence အပေါ်
  train လုပ်ခဲ့သဖြင့် လက်ရှိ traffic တွင် precision ကျဆင်းခြင်း၊ (၃) ပြင်ပ အကြောင်းအရာ အားလုံးကို
  တူညီစွာ သံသယဖြင့် ဆက်ဆံသဖြင့် တရားဝင်သည့် retrieved content ပါ ပိတ်ဆို့ခံရခြင်း၊
  (၄) ထိန်းချုပ်မှု အလွှာများ ထပ်နေသဖြင့် အလွှာတစ်ခုချင်း၏ false block များ စုပေါင်းခြင်း။
- **ဖြေရှင်းနည်း —** လိုအပ်သည့် စံနှုန်း နှစ်ခုလုံး (false-block rate အနည်းဆုံး၊ violation recall
  အနည်းဆုံး) ကို ကြိုတင် သတ်မှတ်ပြီး threshold ကို ထို စံနှုန်းများ ပြည့်သည့် အမှတ်တွင်
  သတ်မှတ်ရမည်၊ slice အလိုက် threshold ခွဲထားရမည်၊ ပိတ်ဆို့ခံရသည့် request များကို လူသား
  ပြန်လည်စစ်ဆေးသည့် အလွှာနှင့် တွဲရမည်၊ ပိတ်ဆို့မိသည့် တရားဝင် case များကို eval set ထဲသို့
  regression case အဖြစ် ထည့်ရမည်။
- **ရှင်းလင်းသည့် term —** Guardrails၊ Precision & Recall၊ Prompt Injection၊ Eval Set၊ Verification Gate။

## ၄။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်းများ (Design Decisions)

### ဆုံးဖြတ်ချက် ၁ — Eval set ကို မည်သို့ ခွဲမည်၊ dev run မည်မျှ လုပ်မည်

**အခြေအနေ —** ရေးသားပြီး၊ စစ်ဆေးပြီးသည့် item ၁,၂၀၀ ရှိသည်။ ရွေးချယ်စရာ configuration ၁၀ ခုကို
နှိုင်းယှဉ်ရမည်။ Report လုပ်မည့် ကိန်းဂဏန်းသည် လက်ရှိ pilot တွင် p ≈ 0.87 ရှိသည့် စွမ်းဆောင်ရည်
ဖြစ်ပြီး half-width ±3 ရာခိုင်နှုန်းအမှတ် (95 % confidence) ကို ကာကွယ်ရမည်။ Item တစ်ခုလျှင်
ကုန်ကျစရိတ်သည် ဥပမာ ၄ မှ USD 0.00756 ဖြစ်သည်။

**ရွေးချယ်စရာ —** (က) item အားလုံးကို development အတွက် သုံး၍ နောက်ဆုံး report အတွက်လည်း
ထိုအစုကိုသာ ပြန် run ခြင်း၊ (ခ) dev ၇၀၀ နှင့် held-out ၅၀၀ အဖြစ် ခွဲခြင်း၊ dev ကို
config များအတွက် လွတ်လပ်စွာ သုံး၍ held-out ကို ရွေးချယ်မှု သတ်မှတ်ပြီးနောက် တစ်ကြိမ်သာ run
ခြင်း။

**ဆုံးဖြတ်ချက် —** (ခ) ကို ရွေးရမည်။

**တိုင်းတာမည့် metric —** held-out အပေါ် အဖြေ တိကျမှုနှင့် ၎င်း၏ margin၊ dev အဆင့်တွင်
အကောင်းဆုံး config နှင့် held-out အဆင့်တွင် အကောင်းဆုံး config တူညီမှု၊ စုစုပေါင်း cost။

### ဆုံးဖြတ်ချက် ၂ — Guardrail threshold ကို မည်သည့်နေရာတွင် သတ်မှတ်မည်

**အခြေအနေ —** Request ၁၀,၀၀၀ / ရက် ရှိသည်၊ ၎င်းအနက် ၃၀၀ (၃ %) သည် policy ချိုးဖောက်မှု ဖြစ်သည်။
Classifier တစ်ခုအတွက် threshold လေးခု၏ တိုင်းတာမှုများမှာ —

| Threshold | violation recall | false-block rate |
|---|---|---|
| T1 | 0.990 | 0.061 |
| T2 | 0.960 | 0.038 |
| T3 | 0.920 | 0.019 |
| T4 | 0.840 | 0.008 |

စံနှုန်းမှာ false-block rate ≤ 2.0 % နှင့် violation recall ≥ 0.90 ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** T3 ကို ရွေးရမည်၊ အကြောင်းမှာ ၎င်းသည် စံနှုန်း နှစ်ခုလုံးကို ပြည့်သည့်
တစ်ခုတည်းသော threshold ဖြစ်သည်။

**တိုင်းတာမည့် metric —** False-block rate၊ violation recall၊ blocked request စုစုပေါင်း နှင့် ၎င်းအနက်
မှန်သည့် အချိုး (precision)၊ လူသား ပြန်လည်စစ်ဆေးရမည့် ဝန်။

## ၅။ အဖြေများ (Answers with Explanations)

### ၅.၁ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း အဖြေများ

#### အဖြေ ၁ — သတ်မှတ်ထားသည့် confidence အတွက် လိုအပ်သည့် eval size

**ဖော်မြူလာ —** n = z² × p × (1 − p) / e²။ ယူဆချက် — 95 % confidence အတွက် z = 1.959964၊
e သည် half-width ဖြစ်သည်၊ အကြီးဆုံး variance ကို p = 0.5 တွင် ရသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**

1. p = 0.5 တွင် half-width ±5 အတွက် n = 384.1၊ ထို့ကြောင့် 385 လိုသည်။
2. p = 0.5 တွင် ±3 အတွက် n = 1,067.1၊ ထို့ကြောင့် 1,068 လိုသည်။ ±2 အတွက် 2,401 လိုသည်။
3. p = 0.85 တွင် ±5၊ ±3 နှင့် ±2 အတွက် 196၊ 545 နှင့် 1,225 လိုသည်။
4. p = 0.9 တွင် ±5၊ ±3 နှင့် ±2 အတွက် 139၊ 385 နှင့် 865 လိုသည်။
5. N = 5,000 အတွက် finite population correction ဖြင့် 1,067.1 → 879.5၊ ထို့ကြောင့် 880 လိုသည်။
6. n = 100 တွင် margin 5.88 ရာခိုင်နှုန်းအမှတ်၊ n = 400 တွင် 2.94၊ n = 500 တွင် 2.63၊
   n = 1,000 တွင် 1.86 ဖြစ်သည်။ Item တစ်ခုလျှင် တန်ဖိုးသည် n = 400 တွင် 0.25 ရာခိုင်နှုန်းအမှတ်
   ဖြစ်သည်။
7. တစ်ဘက် 95 % အတွက် z = 1.6449 ဖြစ်သဖြင့် p = 0.9၊ ±3 အတွက် n = 271 သာ လိုသည်။

**အဓိပ္ပာယ် —** လိုအပ်သည့် item အရေအတွက်သည် half-width ၏ နှစ်ထပ်ကိန်းနှင့် တစ်ပြန်တစ်လှည့်
အချိုးကျသည် — ±3 မှ ±2 သို့ တိုးလိုက်ပါက item အရေအတွက် ၂.၂၅ ဆ တိုးသည်။ p ကို ကြိုတင်
သိပါက (pilot မှ) လိုအပ်သည့် အရေအတွက်သည် သိသိသာသာ လျော့သည်။ 1,068 နှင့် 385 ကွာခြားမှုသည်
"ဘယ်လောက် သေချာမှု လိုသည်" ဟူသည့် စံနှုန်းမှ လာသည်၊ ဖော်မြူလာမှ မဟုတ်ပါ။

```bash
python3 - <<'PY'
import math

z = 1.959963985

def n_for(p, e):
    return z * z * p * (1 - p) / (e * e)

def margin(p, n):
    return z * math.sqrt(p * (1 - p) / n)

print("--- items needed for a stated half-width ---")
for p in (0.5, 0.85, 0.9):
    for e in (0.05, 0.03, 0.02):
        raw = n_for(p, e)
        print(f"p={p:<4} half-width={e}  raw n={raw:9.1f}  ceil={math.ceil(raw):5d}")

N = 5000
raw = n_for(0.5, 0.03)
adj = raw / (1 + (raw - 1) / N)
print("finite population correction N=5000 raw", round(raw, 1),
      "adjusted", round(adj, 1), "ceil", math.ceil(adj))

for n in (100, 200, 400, 500, 1000, 1068):
    print(f"n={n:<5} margin at p=0.90 = {100*margin(0.9, n):5.2f} pt   one item = {100/n:5.2f} pt")

z95 = 1.6448536270
print("one-sided 95 percent z", z95, "n at p=0.9 e=0.03",
      math.ceil(z95 * z95 * 0.9 * 0.1 / (0.03 * 0.03)))
PY
```

```text
--- items needed for a stated half-width ---
p=0.5  half-width=0.05  raw n=    384.1  ceil=  385
p=0.5  half-width=0.03  raw n=   1067.1  ceil= 1068
p=0.5  half-width=0.02  raw n=   2400.9  ceil= 2401
p=0.85 half-width=0.05  raw n=    195.9  ceil=  196
p=0.85 half-width=0.03  raw n=    544.2  ceil=  545
p=0.85 half-width=0.02  raw n=   1224.5  ceil= 1225
p=0.9  half-width=0.05  raw n=    138.3  ceil=  139
p=0.9  half-width=0.03  raw n=    384.1  ceil=  385
p=0.9  half-width=0.02  raw n=    864.3  ceil=  865
finite population correction N=5000 raw 1067.1 adjusted 879.5 ceil 880
n=100   margin at p=0.90 =  5.88 pt   one item =  1.00 pt
n=200   margin at p=0.90 =  4.16 pt   one item =  0.50 pt
n=400   margin at p=0.90 =  2.94 pt   one item =  0.25 pt
n=500   margin at p=0.90 =  2.63 pt   one item =  0.20 pt
n=1000  margin at p=0.90 =  1.86 pt   one item =  0.10 pt
n=1068  margin at p=0.90 =  1.80 pt   one item =  0.09 pt
one-sided 95 percent z 1.644853627 n at p=0.9 e=0.03 271
```

#### အဖြေ ၂ — သတ်မှတ်ထားသည့် အစုမှ pass@k

**ဖော်မြူလာ —** pass@k = 1 − C(n − c, k) / C(n, k)၊ C(a, b) = 0 ဖြစ်သည့်အခါ (b > a) pass@k = 1
ဖြစ်သည်။ ယူဆချက် — candidate များသည် သီးခြားစီ နမူနာယူထားသည်၊ verifier သည် candidate တိုင်းအတွက်
တူညီသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**

1. pass@1 = 1 − 8 / 10 = 0.2000 ဖြစ်သည်။
2. pass@3 = 1 − 56 / 120 = 0.5333 ဖြစ်သည်။
3. pass@5 = 1 − 56 / 252 = 0.7778 ဖြစ်သည်။
4. pass@10 = 1 − 0 / 1 = 1.0000 ဖြစ်သည်။
5. Candidate အဆင့် အောင်နှုန်း = 60 / 300 = 20.0 %၊ empirical pass@10 = 18 / 30 = 60.0 % ဖြစ်သည်။
6. Binomial ခန့်မှန်းချက်ဖြင့် k = 1 တွင် 20.00 %၊ k = 2 တွင် 36.00 %၊ k = 4 တွင် 59.04 %၊
   k = 6 တွင် 73.79 %၊ k = 8 တွင် 83.22 %၊ k = 10 တွင် 89.26 % ဖြစ်သည်။
7. k = 1 နှင့် k = 10 ၏ ကွာခြားမှုသည် model တိုးတက်မှုကို မဖော်ပြပါ — ထို အလုပ်အတွက်
   candidate တိုင်း တူညီသည့် ဖြစ်နိုင်ခြေ ရှိပါက attempt budget ကွာခြားမှုသာ ဖော်ပြသည်။

**အဓိပ္ပာယ် —** Pass@k ကို အစီရင်ခံသည့်အခါ k၊ sampling parameter နှင့် estimator အသေးစိတ်ကို
တွဲဖက် အစီရင်ခံရမည်။ Candidate အဆင့် အောင်နှုန်းနှင့် pass@k ကို ရောထွေးပါက တစ်ခုတည်းသော
အလုပ်အတွက် "၂၀ %" နှင့် "၆၀ %" ဟူသည့် ကိန်းဂဏန်း နှစ်ခု တစ်ပြိုင်နက် ပေါ်လာသည့် အခြေအနေ
ဖြစ်သည်။

```bash
python3 - <<'PY'
from math import comb

print("--- pass@k for one task, from n samples with c passing ---")
n, c = 10, 2
for k in (1, 3, 5, 10):
    num = comb(n - c, k) if n - c >= k else 0
    est = 1 - num / comb(n, k)
    print(f"n={n} c={c} k={k:<2} C(n-c,k)={num:5d} C(n,k)={comb(n,k):6d} pass@{k} = {est:.4f}")

print()
print("--- across a task set ---")
tasks, samples = 30, 10
candidates = tasks * samples
passing = 60
with_pass = 18
print("candidates", candidates, "passing", passing,
      "candidate pass rate pct", round(100 * passing / candidates, 2))
print("tasks with at least one pass", with_pass, "pass@10 pct",
      round(100 * with_pass / tasks, 2))
print("candidate level pass rate", round(100 * passing / candidates, 2),
      "pct is not pass@k")
for kk in (1, 2, 4, 6, 8, 10):
    print(f"k={kk:<2} expected pass@k at 0.20 per candidate = {100*(1-(1-0.2)**kk):5.2f} pct")
PY
```

```text
--- pass@k for one task, from n samples with c passing ---
n=10 c=2 k=1  C(n-c,k)=    8 C(n,k)=    10 pass@1 = 0.2000
n=10 c=2 k=3  C(n-c,k)=   56 C(n,k)=   120 pass@3 = 0.5333
n=10 c=2 k=5  C(n-c,k)=   56 C(n,k)=   252 pass@5 = 0.7778
n=10 c=2 k=10 C(n-c,k)=    0 C(n,k)=     1 pass@10 = 1.0000

--- across a task set ---
candidates 300 passing 60 candidate pass rate pct 20.0
tasks with at least one pass 18 pass@10 pct 60.0
candidate level pass rate 20.0 pct is not pass@k
k=1  expected pass@k at 0.20 per candidate = 20.00 pct
k=2  expected pass@k at 0.20 per candidate = 36.00 pct
k=4  expected pass@k at 0.20 per candidate = 59.04 pct
k=6  expected pass@k at 0.20 per candidate = 73.79 pct
k=8  expected pass@k at 0.20 per candidate = 83.22 pct
k=10 expected pass@k at 0.20 per candidate = 89.26 pct
```

#### အဖြေ ၃ — contamination rate နှင့် score အပေါ် ၎င်း၏ လွှမ်းမိုးမှု

**ဖော်မြူလာ —** reported = cr × acc_contaminated + (1 − cr) × acc_clean။ ယူဆချက် — contaminated
item များသည် clean item များထက် ပိုမို လွယ်ကူသည်၊ ထိုကွာခြားမှုသည် တည်ငြိမ်သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**

1. cr = 52 / 400 = 13.0 %၊ reported = 338 / 400 = 84.5 % ဖြစ်သည်။
2. acc_on_contaminated = 50 / 52 = 96.15 %၊ acc_on_clean = 288 / 348 = 82.76 % ဖြစ်သည်။
3. Inflation = 84.50 − 82.76 = 1.74 ရာခိုင်နှုန်းအမှတ် ဖြစ်သည်။
4. cr = 26 % တွင် reported = 86.24 % (inflation 3.48 ရာခိုင်နှုန်းအမှတ်)၊ cr = 50 % တွင်
   89.46 % (inflation 6.70 ရာခိုင်နှုန်းအမှတ်) ဖြစ်သည်။
5. Item တစ်ခုလျှင် လွှမ်းမိုးမှု = 0.0335 ရာခိုင်နှုန်းအမှတ် ဖြစ်သဖြင့် inflation ၁ ရာခိုင်နှုန်းအမှတ်ကို
   ဖယ်ရှားရန် contaminated item ၂၉.၉ ခုကို ပြုပြင်ရမည်။
6. Clean subset အပေါ် score သည် 82.76 % ဖြစ်သည်၊ ၎င်းသည် contaminated item များ၏
   လွယ်ကူမှုကို မပါဝင်သဖြင့် generalize လုပ်နိုင်စွမ်းကို ပိုမို ဖော်ပြသည်။

**အဓိပ္ပာယ် —** Contamination ကို "ဖယ်ရှားရမည့် အရာ" အနေဖြင့်သာ မမြင်ရ — ၎င်းသည် score ၏
အစိတ်အပိုင်း ဖြစ်လာသည့်အခါ model နှစ်ခုကို နှိုင်းယှဉ်ခြင်းကိုပါ ပျက်စီးစေသည်၊
အကြောင်းမှာ model တစ်ခုသည် benchmark ကို ပိုမို ကြုံဖူးသည်သာ ဖြစ်နိုင်သည်။

```bash
python3 - <<'PY'
items = 400
contaminated = 52
clean = items - contaminated
overall = 338
on_cont = 50
on_clean = overall - on_cont

print("--- contamination rate and its effect on the score ---")
print("contaminated", contaminated, "clean", clean)
print("overall correct", overall, "pct", round(100 * overall / items, 2))
print("contamination rate pct", round(100 * contaminated / items, 2))
print("accuracy on contaminated pct", round(100 * on_cont / contaminated, 2))
print("accuracy on clean pct       ", round(100 * on_clean / clean, 2))
print("inflation pt", round(100 * overall / items - 100 * on_clean / clean, 2))
for cr in (0.0, 0.13, 0.26, 0.50):
    mix = cr * on_cont / contaminated + (1 - cr) * on_clean / clean
    print(f"contamination {100*cr:4.0f} pct -> reported {100*mix:5.2f} pct"
          f"  inflation {100*mix - 100*on_clean/clean:5.2f} pt")
print("adjusted score if contaminated items scored at clean rate",
      round(100 * (on_clean + contaminated * on_clean / clean) / items, 2))
print("items to fix to remove 1 pt of inflation",
      round(1.0 / (100 * (on_cont / contaminated - on_clean / clean) / items), 1))
PY
```

```text
--- contamination rate and its effect on the score ---
contaminated 52 clean 348
overall correct 338 pct 84.5
contamination rate pct 13.0
accuracy on contaminated pct 96.15
accuracy on clean pct        82.76
inflation pt 1.74
contamination    0 pct -> reported 82.76 pct  inflation  0.00 pt
contamination   13 pct -> reported 84.50 pct  inflation  1.74 pt
contamination   26 pct -> reported 86.24 pct  inflation  3.48 pt
contamination   50 pct -> reported 89.46 pct  inflation  6.70 pt
adjusted score if contaminated items scored at clean rate 82.76
items to fix to remove 1 pt of inflation 29.9
```

#### အဖြေ ၄ — eval run တစ်ကြိမ်၏ ကုန်ကျစရိတ်

**ဖော်မြူလာ —** cost = input token / 10⁶ × price_input + output token / 10⁶ × price_output။
ယူဆချက် — token အရေအတွက်သည် item တိုင်းတွင် တူညီသည်၊ cache မှ လျှော့ချမှု မရှိပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**

1. Generator input = 340,000 token၊ output = 88,000 token ဖြစ်သည်။
2. Generator cost = 1.020 + 1.320 = USD 2.340 ဖြစ်သည်။
3. Judge input = 192,000 token၊ output = 7,200 token ဖြစ်သည်။
4. Judge cost = 0.576 + 0.108 = USD 0.684 ဖြစ်သည်။
5. Run တစ်ကြိမ် = USD 3.024၊ item တစ်ခုလျှင် USD 0.00756 ဖြစ်သည်။
6. Run ၇ ကြိမ် = USD 21.168၊ ၂၀ % retry အနားသတ် ထည့်ပါက USD 25.4016 ဖြစ်သည်။
7. Run တစ်ကြိမ် = 400 / 3 × 9 s = 1,200 s = 20.0 မိနစ်၊ run ၇ ကြိမ် = 140.0 မိနစ် = 2.33 နာရီဖြစ်သည်။
8. Judge cost share = 0.684 / 3.024 = 22.6 % ဖြစ်သည်။
9. Dev config ၁၀ ခုကို item ၇၀၀ အပေါ် run ပါက USD 52.92၊ held-out ၅၀၀ အပေါ် တစ်ကြိမ် run ပါက
   USD 3.78 ဖြစ်သည်။

**အဓိပ္ပာယ် —** ကုန်ကျစရိတ်၏ အဓိက အစိတ်အပိုင်းသည် run အရေအတွက် ဖြစ်သည်၊ item အရေအတွက်
မဟုတ်ပါ။ ထို့ကြောင့် dev iteration ကို item နည်းသည့် subset အပေါ် လုပ်ပြီး ကြီးသည့်၊
စျေးကြီးသည့် run ကို ရွေးချယ်မှု သတ်မှတ်ပြီးနောက် တစ်ကြိမ်သာ ပြုလုပ်ခြင်းသည်
ကုန်ကျစရိတ်ကို ထိရောက်စွာ လျှော့သည်။

```bash
python3 - <<'PY'
items, in_tok, out_tok = 400, 850, 220
price_in, price_out = 3.00, 15.00
gen_in, gen_out = items * in_tok, items * out_tok
gen_cost = gen_in / 1e6 * price_in + gen_out / 1e6 * price_out

print("--- cost of one eval run ---")
print("generator input tokens ", gen_in, "output tokens", gen_out)
print("generator cost USD     ", round(gen_cost, 4))
judge_items, j_in, j_out = 120, 1600, 60
j_in_t, j_out_t = judge_items * j_in, judge_items * j_out
j_cost = j_in_t / 1e6 * price_in + j_out_t / 1e6 * price_out
print("judge items", judge_items, "input", j_in_t, "output", j_out_t,
      "cost USD", round(j_cost, 4))
per_run = gen_cost + j_cost
print("per run USD", round(per_run, 4), "per item USD", round(per_run / items, 6))
runs = 6 + 1
print("7 runs USD", round(runs * per_run, 4), "with 20 pct retry",
      round(runs * per_run * 1.2, 4))
conc, sec = 3, 9.0
mins = items / conc * sec / 60
print("wall clock one run min", round(mins, 2), "for 7 runs min",
      round(7 * mins, 2), "h", round(7 * mins / 60, 2))
print("cost of 10 dev configs on 700 items USD", round(10 * 700 * (per_run / items), 4))
print("cost of one held-out run on 500 items USD", round(500 * (per_run / items), 4))
PY
```

```text
--- cost of one eval run ---
generator input tokens  340000 output tokens 88000
generator cost USD      2.34
judge items 120 input 192000 output 7200 cost USD 0.684
per run USD 3.024 per item USD 0.00756
7 runs USD 21.168 with 20 pct retry 25.4016
wall clock one run min 20.0 for 7 runs min 140.0 h 2.33
cost of 10 dev configs on 700 items USD 52.92
cost of one held-out run on 500 items USD 3.78
```

#### အဖြေ ၅ — သတ်မှတ်ထားသည့် confusion matrix အတွက် precision နှင့် recall

**ဖော်မြူလာ —** precision = TP / (TP + FP)၊ recall = TP / (TP + FN)၊ F1 = 2PR / (P + R)။
ယူဆချက် — scoring model တစ်ခုတည်းဖြစ်ပြီး threshold သာ ပြောင်းသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**

1. Threshold 0.50: precision 0.7000၊ recall 0.8400၊ accuracy 0.9480 ဖြစ်သည်။
2. Threshold 0.50: F1 = 0.7636 ဖြစ်သည်။
3. Threshold 0.30: precision 0.4800၊ recall 0.9600၊ accuracy 0.8920 ဖြစ်သည်။
4. Threshold 0.30: F1 = 0.6400 ဖြစ်သည်။
5. Recall ကို 0.84 မှ 0.96 သို့ တင်ရန် precision ကို 0.70 မှ 0.48 (−0.22) သို့ လျှော့ရသည်၊
   ဆိုလိုသည်မှာ အမှတ်အသားပြုသည့် အရာ တစ်ခုလျှင် မှန်နိုင်ခြေ ၂၂ ရာခိုင်နှုန်းအမှတ် လျော့သည်။
6. Request ၁၀,၀၀၀ တွင် threshold 0.30 သည် ၂,၀၀၀ ကို အမှတ်အသားပြုသည်၊ ၁,၀၄၀ ခု မှားသည်၊
   ၄၀ ခု လွတ်သွားသည်။
7. Prevalence ၁၀ % မှ ၁ % သို့ ကျပါက threshold 0.50 ၏ precision သည် TP = 4.2၊ FP = 18 ခန့်
   ဖြစ်သဖြင့် 0.19 ခန့်သို့ ကျသည် — ထို့ကြောင့် prevalence ပြောင်းသည့်အခါ threshold ကို
   ပြန်ချိန်ရမည်။

**အဓိပ္ပာယ် —** threshold သည် "စနစ် ဘယ်လောက် ကောင်းသည်" ၏ တိုင်းတာမှု မဟုတ်ဘဲ
"မည်သည့် အမှားကို ပိုမို ခံနိုင်သည်" ၏ ရွေးချယ်မှု ဖြစ်သည်။ Prevalence ပြောင်းလဲခြင်းသည်
precision ကို တိုက်ရိုက် သက်ရောက်သဖြင့် held-out evaluation ၏ prevalence နှင့် ထုတ်လုပ်မှု
prevalence တူညီမှုကို စစ်ရမည်။

```bash
python3 - <<'PY'
def report(name, tp, fp, fn, tn):
    p = tp / (tp + fp)
    r = tp / (tp + fn)
    f = 2 * p * r / (p + r)
    acc = (tp + tn) / (tp + fp + fn + tn)
    print(f"{name}: TP={tp} FP={fp} FN={fn} TN={tn}")
    print(f"  flagged {tp+fp} relevant {tp+fn} precision {p:.4f} recall {r:.4f}"
          f" F1 {f:.4f} accuracy {acc:.4f}")
    print(f"  prevalence {(tp+fn)/(tp+fp+fn+tn):.4f}  false-positive rate {fp/(fp+tn):.4f}")

print("--- precision and recall at two thresholds ---")
report("threshold 0.50", 42, 18, 8, 432)
report("threshold 0.30", 48, 52, 2, 398)
print()
print("F1 cross-check", round(2*0.70*0.84/(0.70+0.84), 4), round(2*0.48*0.96/(0.48+0.96), 4))
print("per 10000 requests at threshold 0.30: flagged", 10000*(48+52)/500,
      "missed", 10000*2/500, "false blocks", 10000*52/500)
PY
```

```text
--- precision and recall at two thresholds ---
threshold 0.50: TP=42 FP=18 FN=8 TN=432
  flagged 60 relevant 50 precision 0.7000 recall 0.8400 F1 0.7636 accuracy 0.9480
  prevalence 0.1000  false-positive rate 0.0400
threshold 0.30: TP=48 FP=52 FN=2 TN=398
  flagged 100 relevant 50 precision 0.4800 recall 0.9600 F1 0.6400 accuracy 0.8920
  prevalence 0.1000  false-positive rate 0.1156

F1 cross-check 0.7636 0.64
per 10000 requests at threshold 0.30: flagged 2000.0 missed 40.0 false blocks 1040.0
```

#### အဖြေ ၆ — window နှစ်ခုမှ drift threshold

**ဖော်မြူလာ —** se = √[p₁(1 − p₁)/n₁ + p₂(1 − p₂)/n₂]၊ z = (p₁ − p₂) / se။ ယူဆချက် —
window နှစ်ခုသည် သီးခြားစီ နမူနာယူထားသည်၊ ကွာခြားမှုသည် ပြောင်းလဲမှုမှ လာသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**

1. ကွာခြားမှု = 0.912 − 0.871 = 0.041 = 4.1 ရာခိုင်နှုန်းအမှတ် ဖြစ်သည်။
2. se = 0.0144 = 1.44 ရာခိုင်နှုန်းအမှတ် ဖြစ်သည်။ z = 0.041 / 0.0144 = 2.847 ဖြစ်သည်။
3. 2 se threshold = 2.88 ရာခိုင်နှုန်းအမှတ်၊ 3 se threshold = 4.32 ရာခိုင်နှုန်းအမှတ် ဖြစ်သည်။
4. 95 % ကြားကာလ = 1.278 မှ 6.922 ရာခိုင်နှုန်းအမှတ် ဖြစ်သည် (သုည မပါဝင်သဖြင့်
   ကွာခြားမှုသည် စစ်မှန်သည်)။
5. Slice n = 200/140 တွင် se = 3.470၊ z = 1.18 ဖြစ်သဖြင့် 2 se ကို မကျော်ပါ။ Slice n = 150/100
   တွင် se = 4.073၊ z = 1.01 ဖြစ်သည်။ Window ကြီး n = 5,000/3,000 တွင် se = 0.731၊
   z = 5.61 ဖြစ်သည်။
6. Slice ငယ်တွင် se ကြီးသဖြင့် တူညီသည့် 4.1 ရာခိုင်နှုန်းအမှတ် ကွာခြားမှုသည် noise အတွင်း
   ရောက်နေသည် — ထို့ကြောင့် သတိပေးချက် မထွက်ပါ။

**အဓိပ္ပာယ် —** Drift threshold သည် သတ်မှတ်သည့် ကိန်းဂဏန်း တစ်ခု မဟုတ်ဘဲ window အရွယ်အစားနှင့်
တူညီစွာ ပြောင်းလဲသည့် တန်ဖိုး ဖြစ်သည်။ Slice အလိုက် စောင့်ကြည့်သည့်အခါ window ငယ်လျှင်
se ကြီးသည့်အတွက် သတိပေးချက် မည်မျှ ထွက်မည်ကို ကြိုတင် တွက်ရမည်။

```bash
python3 - <<'PY'
import math

z = 1.959963985

print("--- drift between two windows ---")
p1, n1 = 0.912, 1200
p2, n2 = 0.871, 800
se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
diff = p1 - p2
print(f"baseline n={n1} p={p1}  current n={n2} p={p2}")
print("difference pt", round(100 * diff, 2))
print("standard error pt", round(100 * se, 3))
print("z", round(diff / se, 3))
print("2 sigma threshold pt", round(100 * 2 * se, 3))
print("3 sigma threshold pt", round(100 * 3 * se, 3))
print("95 pct interval pt", round(100 * (diff - z * se), 3),
      round(100 * (diff + z * se), 3))
print()
for sn1, sn2 in ((200, 140), (150, 100), (5000, 3000)):
    s = math.sqrt(p1 * (1 - p1) / sn1 + p2 * (1 - p2) / sn2)
    print(f"slice n={sn1}/{sn2} se pt {100*s:5.3f}  z {diff/s:5.2f}"
          f"  2 sigma {100*2*s:5.3f} pt")
PY
```

```text
--- drift between two windows ---
baseline n=1200 p=0.912  current n=800 p=0.871
difference pt 4.1
standard error pt 1.44
z 2.847
2 sigma threshold pt 2.88
3 sigma threshold pt 4.32
95 pct interval pt 1.278 6.922

slice n=200/140 se pt 3.470  z  1.18  2 sigma 6.939 pt
slice n=150/100 se pt 4.073  z  1.01  2 sigma 8.145 pt
slice n=5000/3000 se pt 0.731  z  5.61  2 sigma 1.463 pt
```

### ၅.၂ ပြဿနာ ရှာဖွေခြင်း အဖြေများ

#### အဖြေ ၁ — score မတူညီခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** Evaluation ၏ ရလဒ်တွင် မတူညီသည့် အရင်းအမြစ် နှစ်မျိုး
ရောနေသည် — စနစ်ကိုယ်တိုင်၏ အပြုအမူပြောင်းလဲမှု နှင့် တိုင်းတာမှု လုပ်ငန်းစဉ်၏ ကျပန်းသဘာဝ။
Generative စနစ်တွင် sampling parameter ကို သတ်မှတ်မထားပါက output တိုင်း မတူညီသဖြင့်
score သည် run တိုင်း လှုပ်ရှားသည်။ Judge model ကို version မချိတ်ထားပါက scorer ကိုယ်တိုင်
ပြောင်းလဲနိုင်သည်။

**ဖော်မြူလာဖြင့် တိုင်းတာခြင်း —** run ၃–၅ ကြိမ်၏ score ကို အသုံးပြု၍ ပျမ်းမျှနှင့် လှုပ်ရှားမှု
အတိုင်းအတာကို တွက်ရမည်။ လှုပ်ရှားမှုသည် item တစ်ခုလျှင် တန်ဖိုးနှင့် နှိုင်းယှဉ်ပါက
(အပိုင်း ၅.၁ အဖြေ ၁ ရှိ n = 400 အတွက် 0.25 ရာခိုင်နှုန်းအမှတ်) မည်သည့် ပြောင်းလဲမှုသည်
စစ်မှန်သည်ကို ခွဲခြားနိုင်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** eval set နှင့် retrieval snapshot ၏ checksum ကို run တိုင်း
မှတ်တမ်းတင်ပါ။ ၎င်းတို့ မတူပါက အကြောင်းရင်း (၃) ဖြစ်သည်။ Checksum တူညီပါက
judge version ကို စစ်ပါ (အကြောင်းရင်း ၂)၊ ထို့နောက် temperature နှင့် seed ကို စစ်ပါ
(အကြောင်းရင်း ၁)။ Failure item အရေအတွက် သည် run အကြား လျော့များပါက အကြောင်းရင်း (၄)
ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** sampling parameter သတ်မှတ်ပြီးနောက် လှုပ်ရှားမှု လုံးဝ ပျောက်ပါက
အကြောင်းရင်းသည် generator ဖြစ်သည်။ မပျောက်ပါက judge ၏ လှုပ်ရှားမှု ဖြစ်နိုင်သဖြင့်
judge score များကို လူသား ပြန်လည်စစ်ဆေးထားသည့် နမူနာများနှင့် ချိန်ညှိရမည်။

#### အဖြေ ၂ — benchmark score မြင့်သော်လည်း ထုတ်လုပ်မှုတွင် ဆိုးခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** Benchmark score သည် သတ်မှတ်ထားသည့် အစုတစ်ခုအပေါ်
တိုင်းတာမှုသာ ဖြစ်သည်၊ ထုတ်လုပ်မှု အရည်အသွေး၏ ပြည့်စုံသည့် ဖော်ပြချက် မဟုတ်ပါ။
Contamination ရှိပါက score သည် မမြင်ဖူးသေးသည့် အလုပ်များသို့ generalize လုပ်နိုင်စွမ်းကို
မဖော်ပြဘဲ ယခင် ကြုံဖူးမှုကို ထင်ဟပ်သည် (အပိုင်း ၅.၁ အဖြေ ၃ တွင် inflation 1.74
ရာခိုင်နှုန်းအမှတ် ဖြစ်သည်)။ Distribution shift ရှိပါက model သည် held-out test ကို အောင်သော်လည်း
အသုံးပြုသူ၊ အလုပ်၊ ဘာသာစကား၊ tool သို့မဟုတ် လည်ပတ်မှု အခြေအနေများ ပြောင်းသည့်အခါ
ကျရှုံးသည်။

**ဖော်မြူလာဖြင့် တိုင်းတာခြင်း —** slice အလိုက် စွမ်းဆောင်ရည်ကို တွက်ပါ၊ စုစုပေါင်း metric နှင့်
slice metric ကွာခြားပါက ပြဿနာသည် slice တစ်ခုတွင် စုစည်းနေသည်။ ထို့နောက် input လက္ခဏာ
ဖြန့်ကျက်မှုကို baseline နှင့် နှိုင်းယှဉ်ပါ (အပိုင်း ၅.၁ အဖြေ ၆ ၏ 2 se နည်းလမ်းအတိုင်း)။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** training source တွင် အတိအကျနှင့် အနီးစပ်ဆုံး ထပ်နေသည့် အရာများကို
ရှာဖွေပါ။ ထပ်နေမှု မြင့်မားပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ Slice အလိုက် ကျဆင်းမှု ရှိပါက
အကြောင်းရင်း (၂) ဖြစ်သည်။ Clean subset အပေါ် score သည် ထုတ်လုပ်မှု တိုင်းတာမှုနှင့်
နီးပါက အကြောင်းရင်းသည် benchmark ၏ data ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** ထုတ်လုပ်မှုမှ နမူနာယူထားသည့် case များဖြင့် eval set
အသစ် ဖွဲ့ပြီးနောက် benchmark နှင့် ထို eval set ၏ ကွာခြားမှုသည် ထို eval set အပေါ်
ကျဆင်းဖြစ်ပါက အကြောင်းရင်းသည် eval set ၏ ကိုယ်စားပြုမှု ဖြစ်သည်။

#### အဖြေ ၃ — guardrail သည် တရားဝင်သည့် request များကို ပိတ်ဆို့ခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** Guardrail ၏ threshold သည် မှန်သည့် အမှတ်အသားပြုမှု (recall) နှင့်
မှားသည့် အမှတ်အသားပြုမှု (false block) အကြား လဲလှယ်မှု ဖြစ်သည် (အပိုင်း ၅.၁ အဖြေ ၅ တွင်
recall 0.84 → 0.96 အတွက် precision 0.70 → 0.48 ဖြစ်သည်)။ Threshold ကို recall ဘက်သို့
လျှော့ချသည့်အခါ တရားဝင်သည့် request များ ပိတ်ဆို့ခံရသည်။ Classifier ကို မတူညီသည့်
prevalence အောက် train လုပ်ခဲ့ပါက ထိုလဲလှယ်မှုသည် ပို၍ ဆိုးသည်၊ အကြောင်းမှာ prevalence
ပြောင်းလဲခြင်းသည် precision ကို တိုက်ရိုက် သက်ရောက်သည်။

**ဖော်မြူလာဖြင့် တိုင်းတာခြင်း —** false-block rate = FP / (FP + TN)၊ violation recall = TP / (TP + FN)။
ထို နှစ်ခုကို threshold တိုင်းအတွက် တွက်ပြီး စံနှုန်း နှစ်ခုလုံး ပြည့်သည့် အနိမ့်ဆုံး threshold ကို
ရွေးရမည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** Threshold ကို sweep လုပ်ပြီး false-block rate နှင့် violation recall ကို
အတွဲလိုက် တိုင်းပါ။ စံနှုန်း ပြည့်သည့် threshold တစ်ခုတည်း ရှိပါက အကြောင်းရင်းသည်
threshold ဖြစ်သည် (အကြောင်းရင်း ၁)။ Threshold အားလုံးတွင် false-block rate မြင့်ပါက
classifier ၏ domain သို့မဟုတ် prevalence ကို စစ်ပါ (အကြောင်းရင်း ၂)။ Slice အလိုက်
false-block rate ကွာခြားပါက အကြောင်းရင်း (၃) ဖြစ်သည်။ Layer တစ်ခုချင်း၏ false block များ
စုပေါင်းသည့် ပမာဏသည် ခန့်မှန်းချက်ထက် ကြီးပါက အကြောင်းရင်း (၄) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** Threshold အသစ်ဖြင့် ရက်အနည်းငယ် စောင့်ကြည့်ပြီး false-block rate သည်
စံနှုန်းအောက် ရောက်သော်လည်း violation recall မကျဆင်းကြောင်း တိုင်းတာဖြင့် အတည်ပြုရမည်။
ပိတ်ဆို့မိသည့် တရားဝင် case များကို eval set ထဲသို့ ထည့်ထားခြင်းသည် ဤပြဿနာကို
ပြန်မပေါ်စေသည့် အထောက်အထား ဖြစ်သည်။

### ၅.၃ ဆုံးဖြတ်ချက် အဖြေများ

#### အဖြေ ၁ — eval set ခွဲခြင်းနှင့် dev run

**ရှင်းလင်းချက် —** လိုအပ်သည့် held-out အရွယ်အစားကို အပိုင်း ၅.၁ အဖြေ ၁ ၏ ဖော်မြူလာဖြင့်
တွက်သည် — n = 1.959964² × 0.87 × 0.13 / 0.03² = 482.7၊ ထို့ကြောင့် 483 item လိုသည်။ ရရှိနိုင်သည့်
1,200 အနက် held-out ၅၀၀ ကို ခွဲထားပါက margin သည် 2.948 ရာခိုင်နှုန်းအမှတ် ဖြစ်သည်၊
ဆိုလိုသည်မှာ ±3 ရာခိုင်နှုန်းအမှတ် စံနှုန်းကို ပြည့်သည်။ Dev အပိုင်းသည် ၇၀၀ ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** dev ၇၀၀ နှင့် held-out ၅၀၀ အဖြစ် ခွဲရမည်။ Configuration ၁၀ ခုကို dev ၇၀၀
အပေါ် run ပါက USD 52.92၊ held-out ကို တစ်ကြိမ်သာ run ပါက USD 3.78၊ စုစုပေါင်း USD 56.70
ဖြစ်သည်။ ၂၀ % retry အနားသတ် ထည့်ပါက USD 68.04 ဖြစ်သည်။ အချိန်မှာ dev run များအတွက်
350.0 မိနစ်၊ held-out အတွက် 25.0 မိနစ် ဖြစ်သည်။

**အဘယ်ကြောင့် (က) မဟုတ်သည်ကို ရှင်းလင်းချက် —** item အားလုံးကို development အတွက်
သုံးပါက configuration ၁၀ ခုကို ထို အစုအပေါ် ချိန်ညှိခြင်းဖြင့် test အချက်အလက် ယိုစိမ့်သည်။
ထို့နောက် report လုပ်သည့် score သည် မမြင်ဖူးသေးသည့် item များအပေါ် စွမ်းဆောင်ရည်ကို
ခန့်မှန်းနိုင်တော့မည် မဟုတ်ပါ။

**တိုင်းတာမည့် metric —** held-out အပေါ် အဖြေ တိကျမှု (margin 2.948 ရာခိုင်နှုန်းအမှတ် အပါအဝင်)၊
dev အကောင်းဆုံး config နှင့် held-out အကောင်းဆုံး config တူညီမှု၊ စုစုပေါင်း USD။

```bash
python3 - <<'PY'
import math

z = 1.959963985
p, e = 0.87, 0.03
n_need = z * z * p * (1 - p) / (e * e)
print("--- design decision 1: held-out size and dev runs ---")
print("items needed for +-3 pt at 95 pct with p=0.87:", round(n_need, 1),
      "->", math.ceil(n_need))
held, dev = 500, 700
print("held-out", held, "dev", dev)
m = z * math.sqrt(p * (1 - p) / held)
print("held-out margin pt", round(100 * m, 3))
per_item = 0.00756
print("cost 10 dev configs on 700 items USD", round(10 * dev * per_item, 2))
print("cost 1 held-out run USD", round(held * per_item, 2))
print("total USD", round(10 * dev * per_item + held * per_item, 2))
print("with 20 pct retry USD", round(1.2 * (10 * dev * per_item + held * per_item), 2))
print("wall clock: 10 dev runs min", round(10 * dev / 3 * 9 / 60, 1),
      " held-out min", round(held / 3 * 9 / 60, 1))
PY
```

```text
--- design decision 1: held-out size and dev runs ---
items needed for +-3 pt at 95 pct with p=0.87: 482.7 -> 483
held-out 500 dev 700
held-out margin pt 2.948
cost 10 dev configs on 700 items USD 52.92
cost 1 held-out run USD 3.78
total USD 56.7
with 20 pct retry USD 68.04
wall clock: 10 dev runs min 350.0  held-out min 25.0
```

#### အဖြေ ၂ — guardrail threshold ရွေးချယ်ခြင်း

**ရှင်းလင်းချက် —** Threshold တစ်ခုစီအတွက် ဖမ်းမိသည့် violation = recall × 300၊ false block =
false-block rate × 9,700၊ စုစုပေါင်း အမှတ်အသားပြုမှု = နှစ်ခု၏ ပေါင်းလဒ်၊ precision =
ဖမ်းမိသည့် violation / စုစုပေါင်း တန်ဖိုး ဖြစ်သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**

1. T1: ဖမ်းမိ 297.0၊ false block 591.7၊ စုစုပေါင်း 888.7၊ precision 0.334 — false-block rate
   6.1 % ဖြစ်သဖြင့် စံနှုန်းကို မပြည့်ပါ။
2. T2: ဖမ်းမိ 288.0၊ false block 368.6၊ စုစုပေါင်း 656.6၊ precision 0.439 — false-block rate
   3.8 % ဖြစ်သဖြင့် မပြည့်ပါ (စံနှုန်းထက် false block 174.6 ခု ပိုသည်)။
3. T3: ဖမ်းမိ 276.0၊ false block 184.3၊ စုစုပေါင်း 460.3၊ precision 0.600 — false-block rate
   1.9 % နှင့် recall 0.92 ဖြစ်သဖြင့် စံနှုန်း နှစ်ခုလုံး ပြည့်သည်။
4. T4: ဖမ်းမိ 252.0၊ false block 77.6၊ စုစုပေါင်း 329.6၊ precision 0.765 — false-block rate
   0.8 % ဖြစ်သော်လည်း recall 0.84 ဖြစ်သဖြင့် စံနှုန်းကို မပြည့်ပါ (violation 18.0 ခု လွတ်သည်)။
5. T3 တွင် request ၁,၀၀၀ လျှင် အမှတ်အသားပြုမှု 46.0 ခု၊ ၎င်းအနက် 18.4 ခု မှားသည်။
   Request ၁၀,၀၀၀ ၏ 4.6 % ကို လူသား ပြန်လည်စစ်ဆေးသည့် အလွှာသို့ ပို့ပါက
   ထို ဝန်ကို စီမံနိုင်သည်။

**ဆုံးဖြတ်ချက် —** T3 ကို ရွေးရမည်။ အကြောင်းမှာ ၎င်းသည် စံနှုန်း နှစ်ခုလုံး ပြည့်သည့်
တစ်ခုတည်းသော threshold ဖြစ်သည်။ T2 ကို ရွေးပါက တရားဝင် request ၁၀,၀၀၀ လျှင် 174.6 ခု
ပိုမို ပိတ်ဆို့ခံရသည်၊ T4 ကို ရွေးပါက violation 18.0 ခု လွတ်သွားသည်။

**သတိထားရန် —** ဤ ကိန်းဂဏန်းများသည် prevalence 3 % ဟု ယူဆထားသည်။ Prevalence ပြောင်းလဲပါက
precision ပြောင်းလဲသဖြင့် threshold ကို ပြန်ချိန်ရမည်၊ ထို့ကြောင့် false-block rate နှင့်
violation recall ကို အပတ်စဉ် ပြန်တိုင်းရမည်။

**တိုင်းတာမည့် metric —** false-block rate၊ violation recall၊ blocked request အရေအတွက်နှင့်
၎င်း၏ precision၊ လူသား ပြန်လည်စစ်ဆေးရမည့် ဝန်။

```bash
python3 - <<'PY'
print("--- design decision 2: guardrail threshold ---")
total = 10000
viol = 300
legit = total - viol
rows = [("T1", 0.99, 0.061), ("T2", 0.96, 0.038), ("T3", 0.92, 0.019), ("T4", 0.84, 0.008)]
for name, rec, fbr in rows:
    caught = rec * viol
    fb = fbr * legit
    blocks = caught + fb
    prec = caught / blocks
    ok = (fbr <= 0.02) and (rec >= 0.90)
    print(f"{name}: recall {rec:.3f} false-block {fbr:.3f} caught {caught:7.1f}"
          f" false blocks {fb:7.1f} total blocks {blocks:7.1f}"
          f" precision {prec:.3f} meets bar {ok}")
print()
print("chosen T3 per 1000 requests: blocks", round(460 / 10, 1),
      "of which false", round(184 / 10, 1))
print("review load if every block is reviewed by a human:",
      round(460 / 10000 * 100, 2), "pct of traffic")
print("T2 fails the 2 pct false-block bar by",
      round((0.038 - 0.02) * legit, 1), "extra false blocks per 10000")
print("T4 misses", round((0.90 - 0.84) * viol, 1), "violations per 10000 to save",
      round(184 - 78, 1), "false blocks")
PY
```

```text
--- design decision 2: guardrail threshold ---
T1: recall 0.990 false-block 0.061 caught   297.0 false blocks   591.7 total blocks   888.7 precision 0.334 meets bar False
T2: recall 0.960 false-block 0.038 caught   288.0 false blocks   368.6 total blocks   656.6 precision 0.439 meets bar False
T3: recall 0.920 false-block 0.019 caught   276.0 false blocks   184.3 total blocks   460.3 precision 0.600 meets bar True
T4: recall 0.840 false-block 0.008 caught   252.0 false blocks    77.6 total blocks   329.6 precision 0.765 meets bar False

chosen T3 per 1000 requests: blocks 46.0 of which false 18.4
review load if every block is reviewed by a human: 4.6 pct of traffic
T2 fails the 2 pct false-block bar by 174.6 extra false blocks per 10000
T4 misses 18.0 violations per 10000 to save 106 false blocks
```

## Self-check

၁။ အပိုင်း ၅.၁ အဖြေ ၃ တွင် contamination rate တိုးသည့်အခါ reported score အဘယ်ကြောင့် တက်သနည်း၊
inflation သည် မည်သည့် အချက်နှစ်ချက်အပေါ် မှီခိုသည်။

၂။ အပိုင်း ၅.၁ အဖြေ ၂ တွင် pass@1 နှင့် pass@10 ၏ ကွာခြားမှုသည် မည်သည့် အရာကို တိုင်းတာသနည်း။

၃။ အပိုင်း ၅.၁ အဖြေ ၅ တွင် threshold ကို 0.50 မှ 0.30 သို့ လျှော့သည့်အခါ metric လေးခု
(precision၊ recall၊ F1၊ accuracy) မည်သို့ ပြောင်းသနည်း။

၄။ အပိုင်း ၅.၁ အဖြေ ၆ တွင် slice ငယ်တွင် drift သတိပေးချက် အဘယ်ကြောင့် မထွက်သနည်း။

၅။ အပိုင်း ၅.၃ အဖြေ ၂ တွင် T2 နှင့် T4 ကို မရွေးရသည့် အကြောင်းရင်း ကွာခြားချက်ကို
ဖော်ပြပါ။

<details>
<summary>အဖြေများ</summary>

၁။ Contaminated item များအပေါ် တိကျမှု (96.15 %) သည် clean item များအပေါ် တိကျမှု (82.76 %)
ထက် မြင့်သည့်အတွက် contaminated item များ၏ အချိုးအစား တိုးလာသည့်အခါ ရောစပ်ပြီး score
တက်လာသည်။ Inflation သည် contaminated item များနှင့် clean item များ၏ တိကျမှု ကွာခြားချက်
(13.39 ရာခိုင်နှုန်းအမှတ်) နှင့် contamination rate (13.0 %) နှစ်ခုအပေါ် မှီခိုသည်။

၂။ ၎င်းသည် attempt budget ၏ တန်ဖိုးကို တိုင်းတာသည်၊ model ၏ စွမ်းရည် တိုးတက်မှုကို
မတိုင်းတာပါ။ Candidate တိုင်း၏ ဖြစ်နိုင်ခြေ မပြောင်းလဲဘဲ k တိုးရုံဖြင့် 20.00 % မှ 89.26 % သို့
တက်သည်။

၃။ Precision သည် 0.7000 မှ 0.4800 သို့ ကျသည်၊ recall သည် 0.8400 မှ 0.9600 သို့ တက်သည်၊
F1 သည် 0.7636 မှ 0.6400 သို့ ကျသည်၊ accuracy သည် 0.9480 မှ 0.8920 သို့ ကျသည်။

၄။ Slice ငယ်တွင် n နည်းသဖြင့် se ကြီးသည် (n = 150/100 တွင် 4.073 ရာခိုင်နှုန်းအမှတ်)၊
ထို့ကြောင့် 4.1 ရာခိုင်နှုန်းအမှတ် ကွာခြားမှုသည် 2 se အတွင်း ရောက်နေသည်။

၅။ T2 သည် false-block rate 3.8 % ဖြစ်သဖြင့် 2.0 % စံနှုန်းကို မပြည့်ပါ (request ၁၀,၀၀၀ လျှင်
false block 174.6 ခု ပိုသည်)၊ T4 သည် false-block rate 0.8 % ဖြစ်၍ စံနှုန်းကို လွန်သည့်အပြင်
violation 18.0 ခု လွတ်သွားသည်၊ ဆိုလိုသည်မှာ ၎င်း၏ recall 0.84 သည် 0.90 စံနှုန်းကို မပြည့်ပါ။

</details>

## References

- နယ်ပယ် အခြေခံ အချက်အလက် — `terms/07_evaluation_and_safety.md` နှင့်
  `glossary/by_area/07_evaluation_and_safety.json`။
- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary)
  — MIT licensed, from `rohitg00/ai-engineering-from-scratch`။
- [Investigating Data Contamination in Modern Benchmarks for Large Language Models](https://arxiv.org/abs/2311.09783)
- [On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html)
- [Model Cards for Model Reporting](https://dl.acm.org/doi/10.1145/3287560.3287596)
- [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)
- [OWASP prompt injection guidance](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
