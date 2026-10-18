# ၀၄ — လေ့ကျင့်ခန်းများနှင့် အဖြေများ (Security & Governance)

ဤဖိုင်သည် နယ်ပယ် ၁၁ ၏ term ၂၀ ခုကို အသုံးပြု၍ တွက်ချက်ခြင်း၊ ပြဿနာ ရှာဖွေခြင်းနှင့် ဆုံးဖြတ်ချက် ချခြင်း
လေ့ကျင့်ခန်းများကို စုစည်းထားသည်။ အပိုင်း ၁ တွင် အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာ ၄ ခု၊ အပိုင်း ၂ တွင်
တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ အပိုင်း ၃ တွင် ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ အပိုင်း ၄ တွင်
ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း ၂ ခု ပါဝင်သည်။ အပိုင်း ၅ တွင် အဖြေတိုင်းကို ဖော်မြူလာ၊ တွက်ချက်မှု
အဆင့်ဆင့်နှင့် အကြောင်းရင်း ရှင်းလင်းချက်နှင့်အတူ ပေးထားသည်။

အပိုင်း ၁၊ အပိုင်း ၅.၁ နှင့် အပိုင်း ၅.၃ တွင် ပါဝင်သည့် ကိန်းဂဏန်း တိုင်းသည် Python (standard library သာ)
ဖြင့် အမှန်တကယ် လုပ်ဆောင်ခဲ့သည့် တွက်ချက်မှု၏ output ဖြစ်သည်။ ဖော်ပြထားသည့် command အတိုင်း run
လုပ်ပါက တူညီသည့် output ကို ပြန်လည် ရရှိမည်။ ကိန်းဂဏန်း တိုင်းသည် သတ်မှတ်ထားသည့် ယူဆချက်
(assumption) အပေါ် မှီခိုသည်၊ ထို့ကြောင့် ဖော်မြူလာ တစ်ခုစီနှင့်အတူ ၎င်း၏ ယူဆချက်ကို ဖော်ပြထားသည်။

**မှတ်ချက်** — ဤဖိုင်တွင် credential၊ key၊ token သို့မဟုတ် card အမှန်တကယ် တန်ဖိုး တစ်ခုမျှ
ရေးထားခြင်း မရှိပါ။ key နှင့် secret နှင့် သက်ဆိုင်သည့် လေ့ကျင့်ခန်းများသည် **ကာလ (window)၊
အရေအတွက်နှင့် ကုန်ကျစရိတ်** ကိုသာ တွက်ချက်သည်။

လေ့ကျင့်ခန်းများကို လက်တွေ့ စမ်းသပ်ရန် [`labs/`](labs/) ရှိ `lab_blast_radius.py` (scope နှင့် risk)၊
`lab_redaction_path.py` (redaction ၏ latency နှင့် false positive ကုန်ကျစရိတ်) နှင့်
`lab_audit_volume.py` (audit log ပမာဏနှင့် ကုန်ကျစရိတ်) တို့ကို အသုံးပြုနိုင်သည်။
ထို့အပြင် [`scripts/`](scripts/) ရှိ `ex_a_guardrail_cost.py`၊ `ex_b_audit_volume.py` နှင့်
`ex_c_control_roi.py` တို့သည် guardrail ကုန်ကျစရိတ်၊ audit log ပမာဏနှင့် control ၏ ROI ကို
တွက်ပေးသည်။ ဤဖိုင်၏ တွက်ချက်မှုများသည် ထို lab နှင့် script များအပေါ် မှီခိုမှု မရှိပါ။

## ၁။ အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာများ (Worked Examples)

### ဥပမာ ၁ — AI Risk Assessment: hazard register တစ်ခုမှ risk score နှင့် residual risk

**ယူဆချက် —** likelihood နှင့် impact ကို ၁ မှ ၅ အထိ အဆင့်သတ်မှတ်သည်။ risk score = likelihood × impact
ဖြစ်သည်၊ ထို့ကြောင့် အကြီးဆုံး score သည် ၅ × ၅ = ၂၅ ဖြစ်သည်။ control သည် ဖြစ်နိုင်ခြေနှင့်
သက်ရောက်မှုကို ပေါင်းစပ်၍ ၇၀ ရာခိုင်နှုန်း လျော့စေသည်ဟု ယူဆသည် (residual = score × (1 − 0.70))။

**ဖော်မြူလာ —**
- risk score = likelihood × impact
- residual score = score × (1 − control effectiveness)
- risk reduction % = (score sum − residual sum) / score sum

**တွက်ချက်မှု —** hazard ငါးခုကို စာရင်းချသည် — injection to exfiltration (4, 5) = 20၊
jailbreak to unsafe output (3, 3) = 9၊ membership inference (2, 4) = 8၊ over-permissioned tool (3, 5) = 15၊
stale key exposure (2, 4) = 8။ ပေါင်းလဒ်သည် 60 ဖြစ်ပြီး၊ weighted mean သည် 12.0 ဖြစ်သည်။
control ပြီးနောက် residual သည် [6, 3, 2, 5, 2] ဖြစ်၍ ပေါင်းလဒ် 18 ဖြစ်သည်၊ ဆိုလိုသည်မှာ
70.0 % လျော့သည်။ ၂၀ နှင့် အထက် ရှိသည့် hazard သည် ၁ ခု ရှိသည်။

**ကောက်ချက် —** control effectiveness သည် တူညီသည့်တိုင်း score ကြီးသည့် hazard သည်
residual တွင်လည်း ကြီးနေသည် — ထို့ကြောင့် ဦးစားပေး စီစဉ်မှု (prioritisation) သည် hazard တိုင်းကို
တူညီစွာ ကာကွယ်ခြင်းထက် ပို၍ အကျိုးရှိသည်။ residual score ကို မှတ်တမ်းတင်ခြင်းသည်
AI Risk Assessment ၏ လိုအပ်ချက် ဖြစ်သည်။

```bash
python3 - <<'PY'
hazards = [("injection to exfiltration", 4, 5),
           ("jailbreak to unsafe output", 3, 3),
           ("membership inference", 2, 4),
           ("over-permissioned tool", 3, 5),
           ("stale key exposure", 2, 4)]
for name, likelihood, impact in hazards:
    print(name.ljust(28), "L", likelihood, "I", impact, "score", likelihood * impact)
total = sum(l * i for _, l, i in hazards)
print("score sum".ljust(28), total, "of", 5 * 25)
print("weighted mean".ljust(28), round(total / len(hazards), 2))
eff = 0.70
residual = [round(l * i * (1 - eff)) for _, l, i in hazards]
print("residual at 70 pct".ljust(28), residual, "sum", sum(residual))
print("risk reduction pct".ljust(28), round(100 * (total - sum(residual)) / total, 1))
print("hazards at 20 or above".ljust(28), sum(1 for _, l, i in hazards if l * i >= 20))
PY
```

```text
injection to exfiltration    L 4 I 5 score 20
jailbreak to unsafe output   L 3 I 3 score 9
membership inference         L 2 I 4 score 8
over-permissioned tool       L 3 I 5 score 15
stale key exposure           L 2 I 4 score 8
score sum                    60 of 125
weighted mean                12.0
residual at 70 pct           [6, 3, 2, 5, 2] sum 18
risk reduction pct           70.0
hazards at 20 or above       1
```

### ဥပမာ ၂ — expected annual loss နှင့် control ၏ အကျိုးအမြတ်

**ယူဆချက် —** asset value 2,000,000 USD၊ exposure factor 0.15၊ ဖြစ်ပွားနှုန်း (ARO) 0.4 ကြိမ်/နှစ်။
control တစ်ခု (redaction၊ destination allowlist နှင့် DLP) သည် exposure factor ကို 0.04 သို့ လျှော့ပေးသည်၊
ကုန်ကျစရိတ်သည် 48,000 USD/နှစ် ဖြစ်သည်။

**ဖော်မြူလာ —**
- SLE (single loss expectancy) = asset value × exposure factor
- ALE (annualized loss expectancy) = SLE × ARO
- gross savings = ALE before − ALE after
- net savings = gross savings − control cost
- ROI % = net savings / control cost

**တွက်ချက်မှု —** SLE before = 300,000 USD၊ ALE before = 120,000 USD။ SLE after = 80,000 USD၊
ALE after = 32,000 USD။ gross savings = 88,000 USD၊ control cost = 48,000 USD၊
net savings = 40,000 USD၊ ROI = 83.3 %။ break-even ARO သည် 0.218 ဖြစ်သည်၊ ဆိုလိုသည်မှာ
ARO သည် 0.218 အောက် ကျဆင်းပါက ထို control သည် ကုန်ကျစရိတ်ကို ပြန်မရနိုင်တော့ပါ။

**ကောက်ချက် —** control ၏ တန်ဖိုးသည် ALE လျော့မှုအပေါ် မူတည်သည်၊ control ၏ ကုန်ကျစရိတ်အပေါ်
တစ်ခုတည်း မဟုတ်ပါ။ ARO သည် အလွန်နည်းသည့် အန္တရာယ်အတွက် ဤ control သည် အကျိုးမရှိနိုင်ပါ —
ထို့ကြောင့် AI Risk Assessment တွင် likelihood ကို မှတ်တမ်းတင်ရခြင်း ဖြစ်သည်။

```bash
python3 - <<'PY'
value, exposure, aro = 2_000_000, 0.15, 0.4
sle = value * exposure
ale = sle * aro
print("asset value".ljust(26), value)
print("SLE before".ljust(26), round(sle))
print("ALE before".ljust(26), round(ale))
exposure2 = 0.04
sle2 = value * exposure2
ale2 = sle2 * aro
print("SLE after".ljust(26), round(sle2))
print("ALE after".ljust(26), round(ale2))
control = 48_000
print("gross savings".ljust(26), round(ale - ale2))
print("control cost".ljust(26), control)
print("net savings".ljust(26), round(ale - ale2 - control))
print("ROI pct".ljust(26), round(100 * (ale - ale2 - control) / control, 1))
print("break-even ARO".ljust(26), round(control / (sle - sle2), 3))
PY
```

```text
asset value                2000000
SLE before                 300000
ALE before                 120000
SLE after                  80000
ALE after                  32000
gross savings              88000
control cost               48000
net savings                40000
ROI pct                    83.3
break-even ARO             0.218
```

### ဥပမာ ၃ — key rotation window နှင့် exposure time

**ယူဆချက် —** key တစ်ခုကို ၉၀ ရက်တိုင်း rotate လုပ်သည်။ ဖောက်ထွင်းခံရမှု တစ်ခု ဖြစ်ပွားပါက
ရှာတွေ့ရန် ၁၂ ရက် ကြာသည်၊ ထို့နောက် ၃ ရက်အတွင်း ရပ်စဲနိုင်သည်။ ရှာတွေ့နိုင်သည့် ဖြစ်နိုင်ခြေသည်
0.8 ဖြစ်သည်။ ရှာမတွေ့ပါက exposure သည် rotation အထိ ဆက်ရှိသည်။ တစ်နှစ်လျှင် ဖြစ်ပွားမှု ၂ ကြိမ်
ရှိသည်ဟု ယူဆသည်။

**ဖော်မြူလာ —**
- exposure per incident = p × min(detect + contain, rotation) + (1 − p) × rotation
- annual exposure = exposure per incident × incidents per year
- rotations per year = 365 / rotation days

**တွက်ချက်မှု —** rotation ၉၀ ရက်တွင် exposure per incident = 30.0 ရက်၊ annual = 60.0 ရက်၊
worst case = 90 ရက်၊ rotation အရေအတွက် = 4.06။ rotation ၃၀ ရက်သို့ လျှော့ပါက
exposure per incident = 18.0 ရက်၊ annual = 36.0 ရက်၊ worst case = 30 ရက်၊ rotation = 12.17။
ထို့ကြောင့် လျော့မှုသည် 40.0 % ဖြစ်သည်။ လက်ရှိ အနေအထားတွင် တစ်နှစ်၏ 16.4 % တွင်
key သည် ဖော်ထုတ်ခံရနိုင်သည့် အနေအထား၌ ရှိသည်။

**ကောက်ချက် —** exposure ကို အဓိက ဆုံးဖြတ်သည့်အရာသည် **ရှာတွေ့ရန် ကြာသည့် အချိန်** ဖြစ်သည်။
rotation interval သည် detection မအောင်မြင်သည့် အခြေအနေတွင် upper bound ကို သတ်မှတ်ပေးသည် —
ထို့ကြောင့် rotation သည် detection ကို အစားထိုးခြင်း မဟုတ်ဘဲ သတ်မှတ်ချက် တစ်ခု ဖြစ်သည်။
rotation လုပ်သည့် အရေအတွက် တိုးလာခြင်းသည် လုပ်ငန်းလည်ပတ်မှု ကုန်ကျစရိတ် တိုးစေသည်။

```bash
python3 - <<'PY'
interval, detect, contain, p = 90, 12, 3, 0.8
incidents = 2
def expected(rotation):
    return p * min(detect + contain, rotation) + (1 - p) * rotation
for rotation in (90, 30):
    e = expected(rotation)
    print("rotation days".ljust(26), rotation)
    print("exposure per incident days".ljust(26), round(e, 1))
    print("annual exposure days".ljust(26), round(e * incidents, 1))
    print("worst case days".ljust(26), rotation)
    print("rotations per year".ljust(26), round(365 / rotation, 2))
print("reduction pct".ljust(26), round(100 * (expected(90) - expected(30)) / expected(90), 1))
print("days of year exposed now".ljust(26), round(100 * expected(90) * incidents / 365, 1))
PY
```

```text
rotation days              90
exposure per incident days 30.0
annual exposure days       60.0
worst case days            90
rotations per year         4.06
rotation days              30
exposure per incident days 18.0
annual exposure days       36.0
worst case days            30
rotations per year         12.17
reduction pct              40.0
days of year exposed now   16.4
```

### ဥပမာ ၄ — audit log ပမာဏနှင့် retention ကုန်ကျစရိတ်

**ယူဆချက် —** တစ်နေ့လျှင် ဖြစ်ရပ် 1,200,000 ခု မှတ်တမ်းတင်သည်။ record တစ်ခုလျှင် ပျမ်းမျှ
900 byte ဖြစ်သည်။ retention ကာလသည် ၃၆၅ ရက် ဖြစ်သည်။ သိုလှောင်မှု ခ = 0.023 USD/GB-လ။

**ဖော်မြူလာ —**
- GB per day = events per day × bytes per record / 10⁹
- GB retained = GB per day × retention days
- USD per month = GB retained × price per GB-month
- USD per year = USD per month × 12

**တွက်ချက်မှု —** GB per day = 1.08 GB၊ GB retained = 394.2 GB၊ USD per month = 9.07၊
USD per year = 108.8။ record သည် သုံးဆ ကြီးလာပါက USD per year = 326.4၊
compression ၈:၁ ဖြင့် သိမ်းပါက USD per year = 13.6 ဖြစ်သည်။ retention ကို ၉၀ ရက်သို့
လျှော့ပါက သိမ်းထားသည့် ပမာဏသည် 97.2 GB ဖြစ်သည်။

**ကောက်ချက် —** audit log ၏ ကုန်ကျစရိတ်သည် **record တစ်ခုလျှင် ပမာဏ** နှင့် **retention ကာလ**
နှစ်ခုလုံးအပေါ် တိုက်ရိုက် အချိုးကျ ကြီးထွားသည်။ ထို့ကြောင့် မှတ်တမ်းတင်သည့် field များကို
Data Minimization ၏ ဘောင်အတွင်း ရွေးချယ်ခြင်းသည် လုံခြုံရေး ကုန်ကျစရိတ်ကို တိုက်ရိုက် လျှော့ပေးသည်။
ဤဖိုင်ရှိ မည်သည့် နေရာတွင်မျှ secret ၏ တန်ဖိုးကို မှတ်တမ်းတင်ခြင်း မပြုရ — log တွင် ကျန်သင့်သည့်အရာ
သည် ဖြစ်ရပ်၏ **ရလဒ်နှင့် ဆုံးဖြတ်ချက်** ဖြစ်သည်။

```bash
python3 - <<'PY'
events, record_bytes, days, price = 1_200_000, 900, 365, 0.023
day_gb = events * record_bytes / 1e9
print("events per day".ljust(28), events)
print("bytes per record".ljust(28), record_bytes)
print("GB per day".ljust(28), round(day_gb, 3))
print("GB retained".ljust(28), round(day_gb * days, 1))
print("USD per month".ljust(28), round(day_gb * days * price, 2))
print("USD per year".ljust(28), round(day_gb * days * price * 12, 2))
print("USD per year 3x record".ljust(28), round(day_gb * 3 * days * price * 12, 2))
print("USD per year compressed 8 to 1".ljust(28), round(day_gb * days * price * 12 / 8, 2))
print("GB retained at 90 days".ljust(28), round(day_gb * 90, 1))
PY
```

```text
events per day               1200000
bytes per record             900
GB per day                   1.08
GB retained                  394.2
USD per month                9.07
USD per year                 108.8
USD per year 3x record       326.4
USD per year compressed 8 to 1 13.6
GB retained at 90 days       97.2
```

## ၂။ တွက်ချက်ရသည့် လေ့ကျင့်ခန်းများ (Calculation Exercises)

လေ့ကျင့်ခန်း တစ်ခုစီတွင် ကိန်းဂဏန်း အဖြေ အတိအကျ ရှိသည်။ အဖြေနှင့် ဖော်မြူလာ ရှင်းလင်းချက်ကို
အပိုင်း ၅.၁ တွင် ပေးထားသည်။

**လေ့ကျင့်ခန်း ၁ — risk score နှင့် residual risk**

hazard လေးခုကို likelihood နှင့် impact ဖြင့် ပေးထားသည် — A (5, 5)၊ B (3, 5)၊ C (4, 2)၊ D (2, 3)။
control တစ်ခုသည် ဖြစ်နိုင်ခြေနှင့် သက်ရောက်မှုကို ၆၀ ရာခိုင်နှုန်း လျော့စေသည်။ တွက်ရမည့် အချက်များ —
(က) hazard တိုင်း၏ score၊ (ခ) score ပေါင်းလဒ်နှင့် ပျမ်းမျှ၊ (ဂ) control ပြီးနောက် residual score များ
နှင့် ပေါင်းလဒ်၊ (ဃ) လျော့သွားသည့် ရာခိုင်နှုန်း၊ (င) ၁၀ ထက် ကျော်သည့် hazard အရေအတွက်။
→ `labs/lab_blast_radius.py` နှင့် `scripts/ex_c_control_roi.py`

**လေ့ကျင့်ခန်း ၂ — expected annual loss**

asset value 5,000,000 USD၊ exposure factor 0.10၊ ARO 0.25။ control တစ်ခုသည် exposure factor ကို
0.03 သို့ လျှော့ပေးသည်။ တွက်ရမည့် အချက်များ — (က) SLE and ALE before၊ (ခ) SLE and ALE after၊
(ဂ) loss avoided၊ (ဃ) ALE သည် asset value ၏ မည်မျှ အချိုး ဖြစ်သည်။
→ `scripts/ex_c_control_roi.py`

**လေ့ကျင့်ခန်း ၃ — control ၏ ကုန်ကျစရိတ်နှင့် expected savings**

လေ့ကျင့်ခန်း ၂ ၏ ကိန်းဂဏန်းများကို ဆက်သုံးသည်။ control ၏ ကုန်ကျစရိတ်သည် 60,000 USD/နှစ် ဖြစ်သည်။
တွက်ရမည့် အချက်များ — (က) gross avoided loss၊ (ခ) net benefit၊ (ဂ) ROI %၊ (ဃ) payback လ မည်မျှ၊
(င) break-even exposure factor၊ (စ) avoided loss ၁ USD လျှင် control ကုန်ကျစရိတ်။
→ `scripts/ex_c_control_roi.py`

**လေ့ကျင့်ခန်း ၄ — key rotation window နှင့် exposure time**

rotation interval ၄၅ ရက်၊ ရှာတွေ့ရန် ကြာသည့် အချိန် ၂၀ ရက်၊ ရပ်စဲရန် ၄ ရက်၊
ရှာတွေ့နိုင်သည့် ဖြစ်နိုင်ခြေ 0.75၊ တစ်နှစ်လျှင် ဖြစ်ပွားမှု ၃ ကြိမ်။
တွက်ရမည့် အချက်များ — (က) exposure per incident၊ (ခ) annual exposure ရက်၊ (ဂ) တစ်နှစ်၏ မည်မျှ ရာခိုင်နှုန်း၊
(ဃ) worst case ရက်၊ (င) rotations per year၊ (စ) ရှာတွေ့မှု အမြဲရှိသည့် အခြေအနေနှင့် လုံးဝ မရှိသည့် အခြေအနေ၏
exposure၊ (ဆ) rotation ကို ၁၅ ရက်သို့ လျှော့ပါက exposure နှင့် လျော့မှု ရာခိုင်နှုန်း။
→ rotation window အတွက် သီးသန့် lab မရှိပါ — ဤဖိုင်ရှိ ကိန်းဂဏန်း ကုဒ်ဖြင့် တွက်ပါ။

**လေ့ကျင့်ခန်း ၅ — audit log ပမာဏနှင့် retention ကုန်ကျစရိတ်**

တစ်နေ့လျှင် ဖြစ်ရပ် 400,000 ခု၊ record တစ်ခုလျှင် 1,500 byte၊ retention ၁၈၀ ရက်၊
သိုလှောင်မှု 0.025 USD/GB-လ။ တွက်ရမည့် အချက်များ — (က) GB per day၊ (ခ) GB retained၊
(ဂ) USD per month နှင့် USD per year၊ (ဃ) ဖြစ်ရပ် အရေအတွက် per second၊ (င) 1 GB လျှင် record အရေအတွက်၊
(စ) record သည် 4 KB ဖြစ်ပါက နှစ်စဉ် ကုန်ကျစရိတ်၊ (ဆ) compression ၁၀:၁ ဖြစ်ပါက နှစ်စဉ် ကုန်ကျစရိတ်။
→ `labs/lab_audit_volume.py` နှင့် `scripts/ex_b_audit_volume.py`

**လေ့ကျင့်ခန်း ၆ — over-permissioned tool တစ်ခု၏ blast radius**

tool တစ်ခုသည် object 4,800 ခု ရှိသည့် သိုလှောင်ရာ တစ်ခုလုံးကို ဖတ်နိုင်သည်၊ ထို object များ၏
၁၂ ရာခိုင်နှုန်းသည် sensitive ဖြစ်သည်၊ sensitive object တစ်ခုလျှင် record ၂၅၀ ပါဝင်သည်၊
alert မထွက်မီ တစ်မိနစ်လျှင် object ၆၀ ခု ဆွဲယူနိုင်သည်။ ပြန်လည် သတ်မှတ်ပြီးနောက် tool သည်
object ၃၀၀ ရှိသည့် folder တစ်ခုသာ ဖတ်နိုင်သည်၊ ထို folder တွင် sensitive ၅ ရာခိုင်နှုန်း ရှိသည်။
တွက်ရမည့် အချက်များ — (က) sensitive object စုစုပေါင်း၊ (ခ) တစ်မိနစ်လျှင် sensitive object နှင့် record၊
(ဂ) တစ်နာရီလျှင် sensitive object၊ (ဃ) ပြန်လည် သတ်မှတ်ပြီးနောက် တစ်မိနစ်လျှင် record အရေအတွက်၊
(င) blast radius လျော့မှု ရာခိုင်နှုန်းနှင့် object လျော့မှု ရာခိုင်နှုန်း။
→ `labs/lab_blast_radius.py`

## ၃။ ပြဿနာ ရှာဖွေခြင်း (Troubleshooting Scenarios)

ပြဿနာ တစ်ခုစီကို symptom၊ တိုင်းတာရမည့် အချက်၊ ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်)၊
ဖြေရှင်းနည်းနှင့် ရှင်းလင်းသည့် term ဟူသည့် အစဉ်အတိုင်း ဖော်ပြထားသည်။ အကြောင်းရင်း အစဉ်သည်
တိုင်းတာမှုဖြင့် ရှာဖွေနိုင်သည့် အစဉ်အတိုင်း ဖြစ်သည်။ အသေးစိတ် ရှင်းလင်းချက်ကို အပိုင်း ၅.၂ တွင် ပေးထားသည်။

### ပြဿနာ ၁ — API key တစ်ခု၏ တန်ဖိုးသည် log တွင် ပေါ်လာသည်

- **Symptom —** log aggregator တွင် ပြင်ပ service ၏ key ပုံစံနှင့် တူသည့် စာသားတစ်ခု ပေါ်လာသည်။
  မူလ data store မပျက်စီးဘဲ ရှိနေသော်လည်း ထို log ကို ဖတ်နိုင်သူ တိုင်း ထို key ကို အသုံးပြုနိုင်သည်။
- **တိုင်းတာရမည့် အချက် —** log တွင် ထို ပုံစံ ပေါ်လာသည့် အရေအတွက် (တစ်နေ့လျှင်)၊ log ကို ဖတ်နိုင်သည့်
  principal အရေအတွက်၊ ထို key ၏ သက်တမ်း (နောက်ဆုံး rotate လုပ်ခဲ့သည့် အချိန်)၊ key ကို ရပ်စဲပြီးပြီလား၊
  ထုတ်လုပ်သည့် request များကို ပို့သည့် destination အရေအတွက်၊ redaction စည်းမျဉ်း အလုပ်လုပ်သည့် အရေအတွက်။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) key ကို error message တွင် ထည့်၍ log ရေးခြင်း၊
  (၂) redaction စည်းမျဉ်း မရှိခြင်း သို့မဟုတ် မကိုက်ညီခြင်း၊ (၃) log access ကို လိုသည်ထက် ကျယ်စွာ
  ခွင့်ပြုထားခြင်း၊ (၄) log ကို ပြင်ပ service သို့ တိုက်ရိုက် ပို့ထားခြင်း။
- **ဖြေရှင်းနည်း —** ထို key ကို ချက်ချင်း ရပ်စဲ၍ rotate လုပ်ရမည်၊ log writer တွင် redaction စည်းမျဉ်း
  ကို secret ဖြစ်နိုင်သည့် field အားလုံးအပေါ် ချထားရမည်၊ log access ကို role အလိုက် ကန့်သတ်ရမည်၊
  ထို ဖြစ်ရပ်ကို audit log တွင် မှတ်တမ်းတင်ရမည်။
- **ရှင်းလင်းသည့် term —** Data Exfiltration၊ Audit Log၊ Zero Trust၊ Trust Boundary။

### ပြဿနာ ၂ — agent သည် ၎င်း၏ scope အပြင်ဘက် data ကို ဖတ်သည်

- **Symptom —** audit log တွင် agent သည် အသုံးပြုသူ တစ်ဦးနှင့်သာ သက်ဆိုင်သည့် task တစ်ခုအတွင်း
  အခြား အသုံးပြုသူများ၏ record များကို ရယူခဲ့ကြောင်း ပြသည်။
- **တိုင်းတာရမည့် အချက် —** tool တစ်ခုလျှင် ရောက်နိုင်သည့် object အရေအတွက်၊ ထို object များ၏
  sensitive အချိုး၊ တစ်မိနစ်လျှင် ဆွဲယူနိုင်သည့် အရေအတွက်၊ scope စစ်ဆေးမှု ရှိမရှိ၊
  request တစ်ခုလျှင် ပြန်လည်ရရှိသည့် record အရေအတွက်၊ outbound destination စာရင်း။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) tool ၏ permission သည် task အပေါ် အခြေခံခြင်း မရှိဘဲ
  ကျယ်လွန်းခြင်း၊ (၂) filter ကို model က ဖော်ပြသည့် argument အပေါ်သာ မှီခိုခြင်း၊
  (၃) boundary ဖြတ်ကူးသည့် နေရာတွင် authorization စစ်ဆေးမှု မရှိခြင်း၊
  (၄) ရလဒ်ကို prompt ထဲ ထည့်ပြီးနောက် ထို data ကို ဖြတ်တောက်ခြင်း မရှိခြင်း။
- **ဖြေရှင်းနည်း —** tool တိုင်း၏ permission ကို task နှင့် လုပ်ဆောင်သူ အလိုက် ကျဉ်းစေရမည်၊
  filter ကို server ဘက်တွင် ချထားရမည်၊ boundary ဖြတ်ကူးမှု တိုင်းအတွက် authorization ကို
  သတ်မှတ်ရမည်၊ ရလဒ်ပမာဏကို ကန့်သတ်၍ alert ထုတ်ရမည်။
- **ရှင်းလင်းသည့် term —** Zero Trust၊ Defense in Depth၊ Data Exfiltration၊ Trust Boundary။

### ပြဿနာ ၃ — policy သည် တရားဝင် workflow တစ်ခုကို ပိတ်ဆို့သည်

- **Symptom —** policy version အသစ် ချပြီးနောက် ပုံမှန် အလုပ်လုပ်ခဲ့သည့် workflow တစ်ခုသည်
  ဆက်လက် မလုပ်နိုင်တော့ဘဲ အားလုံး ငြင်းပယ်ခံရသည်။
- **တိုင်းတာရမည့် အချက် —** ငြင်းပယ်ခံရသည့် အရေအတွက် (policy version အလိုက်)၊ ငြင်းပယ်ရသည့်
  အကြောင်းရင်း ကုဒ်၊ ထို workflow ၏ data class နှင့် destination၊ ကြိုတင် သတ်မှတ်ထားသည့်
  allowlist၊ approval gate သို့ ရောက်ခဲ့သည့် အရေအတွက်၊ escalation လမ်းကြောင်း အလုပ်လုပ်မှု။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) policy သည် data class တစ်ခုကို ကျယ်လွန်းစွာ
  သတ်မှတ်ခြင်း၊ (၂) destination ကို allowlist တွင် မထည့်ခြင်း၊ (၃) approval gate လိုသည့်
  အခြေအနေကို အကျိုးဆက် အပေါ် အခြေခံခြင်း မရှိဘဲ လုပ်ဆောင်ချက် အမည်အပေါ် အခြေခံခြင်း၊
  (၄) escalation သို့မဟုတ် emergency access လမ်းကြောင်း မရှိခြင်း။
- **ဖြေရှင်းနည်း —** policy ကို ချမီ dry-run ဖြင့် အလုပ်လုပ်နေသည့် workflow များအပေါ် စမ်းသပ်ရမည်၊
  allowlist ကို အမည်ဖြင့် မဟုတ်ဘဲ လုပ်ဆောင်ချက်နှင့် destination အတွဲဖြင့် သတ်မှတ်ရမည်၊
  emergency access ကို သတ်မှတ်ပြီး နောက်ပိုင်းတွင် ပြန်လည် သုံးသပ်ရမည်၊ ငြင်းပယ်မှု တိုင်းကို
  audit log တွင် ထိန်းသိမ်းရမည်။
- **ရှင်းလင်းသည့် term —** Zero Trust၊ Separation of Duties၊ Defense in Depth၊ Audit Log။

## ၄။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်းများ (Design Decisions)

### ဆုံးဖြတ်ချက် ၁ — redaction ကို မည်သည့် အလွှာတွင် ထားမည်

**အခြေအနေ —** တစ်နေ့လျှင် ဖြစ်ရပ် 400,000 ခု မှတ်တမ်းတင်သည်၊ ထို အရေအတွက်၏ ၂၀,၀၀၀ ခုလျှင်
၁ ခုတွင် credential ပုံစံနှင့် တူသည့် စာသား ပါနိုင်သည်။ ရွေးချယ်စရာ နှစ်ခု ရှိသည် —
ရွေးချယ်မှု A သည် redaction ကို **အရင်းအမြစ် (service တွင်)** လုပ်သည်၊ ရွေးချယ်မှု B သည်
**log writer တွင်** လုပ်သည်။ တိုင်းတာရရှိသည့် လွတ်သွားသည့် နှုန်းသည် A တွင် ၂ ရာခိုင်နှုန်း၊
B တွင် ၉ ရာခိုင်နှုန်း ဖြစ်သည်။ detector ၏ ကုန်ကျစရိတ်သည် ဖြစ်ရပ် ၁ ခုလျှင် 0.000004 USD ဖြစ်သည်။
ဖော်ထုတ်ခံရသည့် credential တစ်ခုမှ ဖြစ်ပေါ်နိုင်သည့် incident သည် ၀.၅ ရာခိုင်နှုန်း ဖြစ်နိုင်ပြီး
incident တစ်ခုလျှင် ကုန်ကျစရိတ်သည် 25,000 USD ဖြစ်သည်။

**trade-off —** ရွေးချယ်မှု A သည် producer တိုင်းတွင် စည်းမျဉ်း ထည့်ရသဖြင့် လွတ်သွားသည့် နှုန်း နည်းသည်၊
သို့သော် အလွှာ အသစ် တစ်ခု ထပ်လာသည်။ ရွေးချယ်မှု B သည် စုစည်း၍ စစ်ဆေးနိုင်သဖြင့် ထည့်ရ လွယ်သည်၊
သို့သော် လွတ်သွားသည့် နှုန်း မြင့်သည်။

**ဆုံးဖြတ်ချက် —** A ကို ရွေးရမည်၊ အကြောင်းမှာ လွတ်သွားသည့် credential အရေအတွက်သည်
657 မှ 146 သို့ ကျဆင်းသည် (77.8 % လျော့သည်)၊ နှစ်စဉ် မျှော်မှန်းဆုံးရှုံးမှုသည် 82,125 USD မှ
18,250 USD သို့ ကျဆင်းသည်၊ detector ၏ ကုန်ကျစရိတ်သည် နှစ်စဉ် 584 USD သာ ဖြစ်သဖြင့်
net benefit သည် 63,291 USD ဖြစ်သည်။

**တိုင်းတာမည့် metric —** တစ်နေ့လျှင် လွတ်သွားသည့် credential အရေအတွက်၊
နှစ်စဉ် မျှော်မှန်းဆုံးရှုံးမှု USD၊ detector ၏ ကုန်ကျစရိတ် USD။ ဤဆုံးဖြတ်ချက်ကို
`labs/lab_redaction_path.py` နှင့် `scripts/ex_a_guardrail_cost.py` ဖြင့် လက်တွေ့ စမ်းသပ်နိုင်သည်။

### ဆုံးဖြတ်ချက် ၂ — key rotation interval ကို မည်မျှ သတ်မှတ်မည်

**အခြေအနေ —** လက်ရှိတွင် key ကို ၉၀ ရက်တိုင်း rotate လုပ်သည်။ rotation တစ်ကြိမ်လျှင်
လုပ်ငန်းလည်ပတ်မှု ၆ ခု လိုအပ်ပြီး တစ်ခုလျှင် 250 USD ကုန်ကျသည်။ ရှာတွေ့ရန် ကြာသည့် အချိန်သည်
၁၂ ရက်၊ ရပ်စဲရန် ၃ ရက်၊ ရှာတွေ့နိုင်သည့် ဖြစ်နိုင်ခြေ 0.8 ဖြစ်သည်။ ဖော်ထုတ်ခံရသည့် key တစ်ခုမှ
တစ်နေ့လျှင် 4,500 USD ဆုံးရှုံးနိုင်သည်၊ တစ်နှစ်လျှင် ဖြစ်ပွားမှု ၂ ကြိမ် ရှိသည်။
ရွေးချယ်စရာမှာ ၉၀ ရက် ထားခြင်းနှင့် ၃၀ ရက်သို့ လျှော့ခြင်း ဖြစ်သည်။

**trade-off —** ၃၀ ရက်သို့ လျှော့ပါက worst case exposure သည် ၉၀ ရက်မှ ၃၀ ရက်သို့ ကျဆင်းသည်၊
သို့သော် rotation အရေအတွက်သည် 4.06 မှ 12.17 သို့ တိုးသဖြင့် ကုန်ကျစရိတ်လည်း တိုးသည်။

**ဆုံးဖြတ်ချက် —** ၃၀ ရက်ကို ရွေးရမည်၊ အကြောင်းမှာ exposure သည် incident တစ်ခုလျှင်
30.0 ရက်မှ 18.0 ရက်သို့ ကျဆင်းသည်၊ နှစ်စဉ် လျော့သွားသည့် ဆုံးရှုံးမှုသည် 108,000 USD ဖြစ်ပြီး
rotation ကုန်ကျစရိတ် တိုးလာမှုသည် 12,166.67 USD သာ ဖြစ်သဖြင့် net benefit သည်
95,833.33 USD ဖြစ်သည်။ break-even ဖြစ်သည့် တစ်နေ့လျှင် ဆုံးရှုံးမှုသည် 506.94 USD ဖြစ်သည်၊
ဆိုလိုသည်မှာ ထို တန်ဖိုးအောက် ကျဆင်းပါက ၉၀ ရက် ထားခြင်းသည် ပို၍ သင့်လျော်မည်။

**တိုင်းမ်တာမည့် metric —** incident တစ်ခုလျှင် exposure ရက်၊ နှစ်စဉ် exposure ရက်၊
နှစ်စဉ် rotation ကုန်ကျစရိတ် USD၊ နှစ်စဉ် မျှော်မှန်းဆုံးရှုံးမှု USD။

## ၅။ အဖြေများ (Answers with Explanations)

### ၅.၁ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း အဖြေများ

#### အဖြေ ၁ — risk score နှင့် residual risk

**ဖော်မြူလာ —** risk score = likelihood × impact၊ residual = score × (1 − effectiveness)။
ယူဆချက် — likelihood နှင့် impact သည် ၁ မှ ၅ အထိ၊ effectiveness = 0.60။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. score များ = A 25၊ B 15၊ C 8၊ D 6 ဖြစ်သည်။
2. ပေါင်းလဒ် = 54 ဖြစ်သည်၊ ပျမ်းမျှ = 13.5 ဖြစ်သည်။
3. residual = [10, 6, 3, 2] ဖြစ်သည်၊ ပေါင်းလဒ် = 21 ဖြစ်သည်။
4. လျော့မှု = (54 − 21) / 54 = 61.1 % ဖြစ်သည်။
5. ၁၀ ထက် ကျော်သည့် hazard = A နှင့် B ဟူ၍ ၂ ခု ဖြစ်သည်။

**အဓိပ္ပာယ် —** A သည် ကျန်နေသည့် အန္တရာယ် အကြီးဆုံး ဖြစ်သည်၊ ထို့ကြောင့် control များကို
A အပေါ် ဦးစွာ ချထားရမည်။ effectiveness သည် ပေါင်းလဒ်ကို လျော့စေသော်လည်း hazard အစဉ်
(ranking) ကို မပြောင်းလဲပါ။

```bash
python3 - <<'PY'
hazards = [("A", 5, 5), ("B", 3, 5), ("C", 4, 2), ("D", 2, 3)]
for name, likelihood, impact in hazards:
    print("hazard", name, "L", likelihood, "I", impact, "score", likelihood * impact)
total = sum(l * i for _, l, i in hazards)
print("score sum".ljust(24), total)
print("mean score".ljust(24), round(total / len(hazards), 2))
eff = 0.6
residual = [round(l * i * (1 - eff)) for _, l, i in hazards]
print("residual at 60 pct".ljust(24), residual, "sum", sum(residual))
print("reduction pct".ljust(24), round(100 * (total - sum(residual)) / total, 1))
print("hazards above 10".ljust(24), sum(1 for _, l, i in hazards if l * i > 10))
PY
```

```text
hazard A L 5 I 5 score 25
hazard B L 3 I 5 score 15
hazard C L 4 I 2 score 8
hazard D L 2 I 3 score 6
score sum                54
mean score               13.5
residual at 60 pct       [10, 6, 3, 2] sum 21
reduction pct            61.1
hazards above 10         2
```

#### အဖြေ ၂ — expected annual loss

**ဖော်မြူလာ —** SLE = asset value × exposure factor၊ ALE = SLE × ARO။
ယူဆချက် — asset value 5,000,000 USD၊ ARO 0.25၊ exposure factor သည် 0.10 မှ 0.03 သို့ ကျဆင်းသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. SLE = 5,000,000 × 0.10 = 500,000 USD ဖြစ်သည်။
2. ALE = 500,000 × 0.25 = 125,000 USD ဖြစ်သည်။
3. control ပြီးနောက် SLE = 5,000,000 × 0.03 = 150,000 USD ဖြစ်သည်။
4. control ပြီးနောက် ALE = 150,000 × 0.25 = 37,500 USD ဖြစ်သည်။
5. loss avoided = 125,000 − 37,500 = 87,500 USD ဖြစ်သည်။
6. ALE သည် asset value ၏ 0.025 (2.5 %) ဖြစ်သည်။

**အဓိပ္ပာယ် —** ALE သည် ဖြစ်နိုင်ခြေ နည်းသော်လည်း (ARO 0.25) သက်ရောက်မှု ကြီးသည့် (SLE 500,000)
ဖြစ်ရပ်များ၏ နှစ်စဉ် ခံနိုင်ရည် ကို ဖော်ပြသည်။ ထို တန်ဖိုးသည် control ၏ ကုန်ကျစရိတ်ကို
ဆုံးဖြတ်သည့် အခြေခံ ဖြစ်သည်။

```bash
python3 - <<'PY'
value, exposure, aro = 5_000_000, 0.10, 0.25
sle = value * exposure
ale = sle * aro
print("asset value".ljust(22), value)
print("SLE".ljust(22), round(sle))
print("ALE".ljust(22), round(ale))
exposure2 = 0.03
print("SLE after control".ljust(22), round(value * exposure2))
print("ALE after control".ljust(22), round(value * exposure2 * aro))
print("loss avoided".ljust(22), round(ale - value * exposure2 * aro))
print("ALE as share of value".ljust(22), round(ale / value, 4))
PY
```

```text
asset value            5000000
SLE                    500000
ALE                    125000
SLE after control      150000
ALE after control      37500
loss avoided           87500
ALE as share of value  0.025
```

#### အဖြေ ၃ — control ၏ ကုန်ကျစရိတ်နှင့် expected savings

**ဖော်မြူလာ —** net benefit = loss avoided − control cost၊ ROI % = net benefit / control cost × 100၊
payback months = 12 × control cost / loss avoided၊
break-even exposure factor = exposure factor − control cost / (value × ARO)။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. loss avoided = 87,500 USD ဖြစ်သည်။
2. control cost = 60,000 USD ဖြစ်သဖြင့် net benefit = 27,500 USD ဖြစ်သည်။
3. ROI = 27,500 / 60,000 = 45.8 % ဖြစ်သည်။
4. payback = 12 × 60,000 / 87,500 = 8.23 လ ဖြစ်သည်။
5. break-even exposure factor = 0.10 − 60,000 / (5,000,000 × 0.25) = 0.052 ဖြစ်သည်။
6. avoided loss ၁ USD လျှင် control ကုန်ကျစရိတ် = 60,000 / 87,500 = 0.686 USD ဖြစ်သည်။

**အဓိပ္ပာယ် —** control သည် exposure factor ကို 0.052 အောက်သို့ လျှော့နိုင်မှသာ အကျိုးရှိသည် —
လက်ရှိတွင် 0.03 သို့ လျှော့သဖြင့် ထို သတ်မှတ်ချက်ကို ဖြေသည်။ exposure factor သည် 0.052 နှင့်
နီးကပ်လာပါက ထို control ကို ရွေးချယ်ရန် အကြောင်းရင်း မရှိတော့ပါ။

```bash
python3 - <<'PY'
value, exposure, aro = 5_000_000, 0.10, 0.25
ale_before = value * exposure * aro
exposure2 = 0.03
ale_after = value * exposure2 * aro
control = 60_000
avoided = ale_before - ale_after
print("ALE before".ljust(30), round(ale_before))
print("ALE after".ljust(30), round(ale_after))
print("loss avoided".ljust(30), round(avoided))
print("control cost".ljust(30), control)
print("net benefit".ljust(30), round(avoided - control))
print("ROI pct".ljust(30), round(100 * (avoided - control) / control, 1))
print("payback months".ljust(30), round(control / avoided * 12, 2))
print("break-even exposure factor".ljust(30), round(exposure - control / (value * aro), 5))
print("cost per USD avoided".ljust(30), round(control / avoided, 3))
PY
```

```text
ALE before                     125000
ALE after                      37500
loss avoided                   87500
control cost                   60000
net benefit                    27500
ROI pct                        45.8
payback months                 8.23
break-even exposure factor     0.052
cost per USD avoided           0.686
```

#### အဖြေ ၄ — key rotation window နှင့် exposure time

**ဖော်မြူလာ —** exposure per incident = p × min(detect + contain, rotation) + (1 − p) × rotation။
ယူဆချက် — rotation 45 ရက်၊ detect 20 ရက်၊ contain 4 ရက်၊ p 0.75၊ ဖြစ်ပွားမှု 3 ကြိမ်/နှစ်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. min(20 + 4, 45) = 24 ဖြစ်သည်၊ ထို့ကြောင့် exposure = 0.75 × 24 + 0.25 × 45 = 29.2 ရက် ဖြစ်သည်။
2. annual exposure = 29.2 × 3 = 87.8 ရက် ဖြစ်သည်၊ ဆိုလိုသည်မှာ တစ်နှစ်၏ 24.0 % ဖြစ်သည်။
3. worst case = 45 ရက် ဖြစ်သည်၊ rotations per year = 365 / 45 = 8.11 ဖြစ်သည်။
4. ရှာတွေ့မှု လုံးဝ မရှိပါက exposure = 45 ရက်၊ အမြဲ ရှိပါက = 24 ရက် ဖြစ်သည်။
5. rotation ကို 15 ရက်သို့ လျှော့ပါက exposure = 0.75 × 24 + 0.25 × 15 = 21.75 ဖြစ်သည်၊
   သို့သော် output တွင် 15.0 ဟု ပြသည်၊ အကြောင်းမှာ 15 < 24 ဖြစ်သဖြင့် min(24, 15) = 15 ဖြစ်သည်။
   ထို့ကြောင့် exposure = 0.75 × 15 + 0.25 × 15 = 15.0 ရက် ဖြစ်သည်၊ annual = 45.0 ရက် ဖြစ်သည်။
6. လျော့မှု = (29.2 − 15.0) / 29.2 = 48.7 % ဖြစ်သည်၊ rotations per year = 24.33 ဖြစ်သည်။

**အဓိပ္ပာယ် —** rotation interval သည် detect + contain အချိန်ထက် ကျဆင်းသည့်အခါ exposure သည်
detection ဖြင့် မဟုတ်ဘဲ rotation ဖြင့် သတ်မှတ်ခံရသည် — ထို့ကြောင့် rotation သည် exposure ၏ upper bound
ဖြစ်လာသည်။ ထို အခြေအနေတွင် rotation ကို ထပ်လျှော့ခြင်း၏ အကျိုးအမြတ်သည် အလွန်ကြီးသည်။

```bash
python3 - <<'PY'
interval, detect, contain, p, incidents = 45, 20, 4, 0.75, 3
def expected(rotation):
    return p * min(detect + contain, rotation) + (1 - p) * rotation
print("rotation days".ljust(30), interval)
print("exposure per incident".ljust(30), round(expected(interval), 1))
print("annual exposure days".ljust(30), round(expected(interval) * incidents, 1))
print("days of year exposed pct".ljust(30), round(100 * expected(interval) * incidents / 365, 1))
print("worst case days".ljust(30), interval)
print("rotations per year".ljust(30), round(365 / interval, 2))
print("exposure if never detected".ljust(30), interval)
print("exposure if always detected".ljust(30), detect + contain)
shorter = 15
print("exposure at 15 days".ljust(30), round(expected(shorter), 1))
print("annual at 15 days".ljust(30), round(expected(shorter) * incidents, 1))
print("reduction pct".ljust(30), round(100 * (expected(interval) - expected(shorter)) / expected(interval), 1))
print("rotations per year at 15".ljust(30), round(365 / shorter, 2))
PY
```

```text
rotation days                  45
exposure per incident          29.2
annual exposure days           87.8
days of year exposed pct       24.0
worst case days                45
rotations per year             8.11
exposure if never detected     45
exposure if always detected    24
exposure at 15 days            15.0
annual at 15 days              45.0
reduction pct                  48.7
rotations per year at 15       24.33
```

#### အဖြေ ၅ — audit log ပမာဏနှင့် retention ကုန်ကျစရိတ်

**ဖော်မြူလာ —** GB per day = events × bytes / 10⁹၊ GB retained = GB per day × days၊
USD per month = GB retained × price။ ယူဆချက် — 400,000 ဖြစ်ရပ်/နေ့၊ 1,500 byte၊ 180 ရက်၊
0.025 USD/GB-လ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. GB per day = 400,000 × 1,500 / 10⁹ = 0.6 GB ဖြစ်သည်။
2. GB retained = 0.6 × 180 = 108.0 GB ဖြစ်သည်။
3. USD per month = 108.0 × 0.025 = 2.7 USD ဖြစ်သည်၊ USD per year = 32.4 USD ဖြစ်သည်။
4. ဖြစ်ရပ် per second = 400,000 / 86,400 = 4.6 ဖြစ်သည်။
5. 1 GB လျှင် record = 10⁹ / 1,500 ≈ 666,667 ခု ဖြစ်သည်။
6. record သည် 4 KB ဖြစ်ပါက GB per day = 1.6 ဖြစ်သည်၊ USD per year = 86.4 ဖြစ်သည်။
7. compression 10:1 ဖြစ်ပါက USD per year = 3.24 ဖြစ်သည်။

**အဓိပ္ပာယ် —** retention ကာလ နှင့် record အရွယ်အစား နှစ်ခုလုံးသည် ကုန်ကျစရိတ်အပေါ် တိုက်ရိုက်
အချိုးကျ သက်ရောက်သည်။ ထို့ကြောင့် audit log သည် မည်သည့် field များကို မှတ်တမ်းတင်သည် ကို
Data Minimization ၏ ဘောင်အတွင်း ဆုံးဖြတ်ရမည်။

```bash
python3 - <<'PY'
events, record_bytes, days, price = 400_000, 1_500, 180, 0.025
day_gb = events * record_bytes / 1e9
print("GB per day".ljust(30), round(day_gb, 3))
print("GB retained".ljust(30), round(day_gb * days, 1))
print("USD per month".ljust(30), round(day_gb * days * price, 2))
print("USD per year".ljust(30), round(day_gb * days * price * 12, 2))
print("events per second".ljust(30), round(events / 86400, 1))
print("records per GB".ljust(30), round(1e9 / record_bytes))
print("GB per day with 4 KB record".ljust(30), round(events * 4000 / 1e9, 3))
print("USD per year with 4 KB record".ljust(30), round(events * 4000 / 1e9 * days * price * 12, 2))
print("USD per year compressed 10 to 1".ljust(30), round(day_gb * days * price * 12 / 10, 2))
PY
```

```text
GB per day                     0.6
GB retained                    108.0
USD per month                  2.7
USD per year                   32.4
events per second              4.6
records per GB                 666667
GB per day with 4 KB record    1.6
USD per year with 4 KB record  86.4
USD per year compressed 10 to 1 3.24
```

#### အဖြေ ၆ — over-permissioned tool တစ်ခု၏ blast radius

**ဖော်မြူလာ —** ထိတွေ့နိုင်သည့် sensitive object = ဆွဲယူနိုင်သည့် object × sensitive အချိုး၊
record = object × record per object။ ယူဆချက် — 4,800 object၊ 12 % sensitive၊ 250 record/object၊
တစ်မိနစ်လျှင် 60 object။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. sensitive object စုစုပေါင်း = 4,800 × 0.12 = 576.0 ဖြစ်သည်။
2. တစ်မိနစ်လျှင် sensitive object = 60 × 0.12 = 7.2 ဖြစ်သည်၊ record = 7.2 × 250 = 1,800.0 ဖြစ်သည်။
3. တစ်နာရီလျှင် sensitive object = 60 × 60 × 0.12 = 432.0 ဖြစ်သည်။
4. scope ပြန်လည် သတ်မှတ်ပြီးနောက် တစ်မိနစ်လျှင် sensitive object = 60 × 0.05 = 3.0 ဖြစ်သည်၊
   record = 3.0 × 250 = 750.0 ဖြစ်သည်။
5. blast radius လျော့မှု = (0.12 − 0.05) / 0.12 = 58.3 % ဖြစ်သည်။
6. object လျော့မှု = (4,800 − 300) / 4,800 = 93.8 % ဖြစ်သည်။

**အဓိပ္ပာယ် —** object အရေအတွက်ကို ၉၃.၈ % လျှော့သော်လည်း blast radius သည် ၅၈.၃ % သာ
လျော့သည်၊ အကြောင်းမှာ scope အသစ်တွင် sensitive အချိုး ကျန်နေသည့်အတွက် ဖြစ်သည်။ ထို့ကြောင့်
permission ကို ကျဉ်းစေခြင်းနှင့် sensitive data ကို ထို scope ထဲမှ ဖယ်ထုတ်ခြင်းသည်
မတူညီသည့် အလုပ်နှစ်ခု ဖြစ်သည်။

```bash
python3 - <<'PY'
objects, sensitive, records, per_minute = 4_800, 0.12, 250, 60
print("reachable objects".ljust(32), objects)
print("sensitive objects".ljust(32), round(objects * sensitive, 1))
print("objects reachable per minute".ljust(32), per_minute)
print("sensitive objects per minute".ljust(32), round(per_minute * sensitive, 1))
print("records per minute".ljust(32), round(per_minute * sensitive * records, 1))
print("sensitive objects per hour".ljust(32), round(60 * per_minute * sensitive, 1))
scoped, sensitive2 = 300, 0.05
print("scoped objects".ljust(32), scoped)
print("scoped sensitive per minute".ljust(32), round(per_minute * sensitive2, 1))
print("scoped records per minute".ljust(32), round(per_minute * sensitive2 * records, 1))
print("blast radius reduction pct".ljust(32), round(100 * (sensitive - sensitive2) / sensitive, 1))
print("objects reduction pct".ljust(32), round(100 * (objects - scoped) / objects, 1))
PY
```

```text
reachable objects                4800
sensitive objects                576.0
objects reachable per minute     60
sensitive objects per minute     7.2
records per minute               1800.0
sensitive objects per hour       432.0
scoped objects                   300
scoped sensitive per minute      3.0
scoped records per minute        750.0
blast radius reduction pct       58.3
objects reduction pct            93.8
```

### ၅.၂ ပြဿနာ ရှာဖွေခြင်း အဖြေများ

#### အဖြေ ၁ — log တွင် credential ပေါ်လာခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** data exfiltration သည် မူလ data store ပျက်စီးမှုကို မလိုအပ်ပါ —
agent သို့မဟုတ် service သည် generate လုပ်ထားသည့် စာသား၊ tool argument၊ URL သို့မဟုတ် log မှတစ်ဆင့်
secret ကို ဖော်ထုတ်နိုင်သည်။ log သည် access control ဖြင့် ကာကွယ်ထားသည့် သက်သေ မှတ်တမ်း ဖြစ်သော်လည်း
ထို access control ပျက်ကွက်ပါက log ကိုယ်တိုင် ဖော်ထုတ်သည့် လမ်းကြောင်း ဖြစ်လာသည်။
ထို့ကြောင့် log ကို အလွှာ တစ်ခု အနေဖြင့် ကာကွယ်ရမည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** error message ထဲတွင် key ပါမပါ စစ်ပါ၊ ပါပါက အကြောင်းရင်း (၁) ဖြစ်သည်။
redaction စည်းမျဉ်း အတိအကျ ရှိမရှိ စစ်ပါ၊ မရှိပါက အကြောင်းရင်း (၂) ဖြစ်သည်။ log ကို ဖတ်နိုင်သည့်
principal စာရင်းကို ကြည့်ပါ၊ လိုသည်ထက် ကျယ်ပါက အကြောင်းရင်း (၃) ဖြစ်သည်။ log သည် ပြင်ပ
service သို့ တိုက်ရိုက် ရောက်နေပါက အကြောင်းရင်း (၄) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** key ကို ရပ်စဲ၍ rotate လုပ်ပြီးနောက် ထို key ဖြင့် ထုတ်လုပ်သည့်
request အရေအတွက် သုည ဖြစ်ရမည် (audit log တွင် စစ်ရမည်)။ redaction စည်းမျဉ်း ချပြီးနောက်
log အတွင်း ထို ပုံစံ ပေါ်လာသည့် အရေအတွက် သုည ဖြစ်မှ အတည်ပြုနိုင်သည်။

#### အဖြေ ၂ — agent သည် scope အပြင်ဘက် data ဖတ်ခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** zero trust တွင် access တောင်းခံမှု တိုင်းကို identity၊ resource၊
policy နှင့် လက်ရှိ context အလိုက် အကဲဖြတ်သည်။ tool ၏ permission သည် task အပေါ် အခြေခံခြင်း
မရှိဘဲ ကျယ်လွန်းပါက agent သည် ခွင့်ပြုထားသည့် task တစ်ခုကို ဆောင်ရွက်စဉ် လိုသည်ထက်
များစွာသော data ကို ဖတ်နိုင်သည်။ ထို အခြေအနေတွင် authorization ဆုံးဖြတ်ချက်သည်
model ဖော်ပြသည့် argument အပေါ် မှီခိုနေပါက scope စစ်ဆေးမှု တကယ် မရှိသည့် အတူတူ ဖြစ်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** tool တိုင်း၏ permission scope ကို စာရင်းချပါ၊ ကျယ်သည့် scope
တစ်ခု တွေ့ပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ filter သည် client ဘက်တွင်သာ ရှိပါက
အကြောင်းရင်း (၂) ဖြစ်သည်။ boundary ဖြတ်ကူးသည့် နေရာတွင် authorization log မရှိပါက
အကြောင်းရင်း (၃) ဖြစ်သည်။ ရလဒ် ပမာဏကို ကန့်သတ်ချက် မရှိပါက အကြောင်းရင်း (၄) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** permission ကျဉ်းပြီးနောက် တူညီသည့် task တစ်ခုအတွက်
ပြန်လည်ရရှိသည့် record အရေအတွက်ကို တိုင်းပါ။ blast radius လျော့မှုကို အပိုင်း ၅.၁ အဖြေ ၆ ၏
ပုံစံအတိုင်း တွက်ပြီး မျှော်မှန်းထားသည့် အတိုင်း ကျဆင်းမှ အတည်ပြုနိုင်သည်။

#### အဖြေ ၃ — policy သည် တရားဝင် workflow ကို ပိတ်ဆို့ခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** policy သည် အကျိုးဆက် (consequence) အပေါ် အခြေခံရမည်။
လုပ်ဆောင်ချက် အမည်အပေါ် အခြေခံပါက တူညီသည့် အမည် ရှိသည့် ဘေးကင်းသည့် လုပ်ဆောင်ချက် နှင့်
အန္တရာယ်ရှိသည့် လုပ်ဆောင်ချက် နှစ်ခုလုံးကို တူညီစွာ ပိတ်ဆို့သည်။ defense in depth တွင်
control တိုင်းသည် မတူညီသည့် failure mode ကို ကိုင်တွယ်ရမည် — ထို့ကြောင့် policy ကို
ချမီ workflow အပေါ် dry-run လုပ်ခြင်းသည် control တစ်ခု အလွန်ကျဉ်းလွန်းခြင်းကို ဖော်ထုတ်ပေးသည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** ငြင်းပယ်ခံရသည့် ဖြစ်ရပ်များ၏ data class ကို ကြည့်ပါ၊
အန္တရာယ်နည်းသည့် class ဖြစ်ပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ destination သည် ခွင့်ပြုသင့်သည့်
အမျိုးအစား ဖြစ်ပါက အကြောင်းရင်း (၂) ဖြစ်သည်။ approval gate သို့ လုံးဝ မရောက်ပါက
အကြောင်းရင်း (၃) ဖြစ်သည်။ emergency access လမ်းကြောင်း မရှိပါက အကြောင်းရင်း (၄) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** allowlist ကို လုပ်ဆောင်ချက်နှင့် destination အတွဲဖြင့်
ပြန်သတ်မှတ်ပြီးနောက် ငြင်းပယ်မှု အရေအတွက် ကျဆင်းပြီး အန္တရာယ်ရှိသည့် လုပ်ဆောင်ချက်များ
ဆက်လက် ပိတ်ဆို့ခံရလျှင် ဆုံးဖြတ်ချက် မှန်ကန်သည်။ emergency access ကို သတ်မှတ်ပြီးနောက်
ထို ဖြစ်ရပ် တိုင်းကို audit log တွင် မှတ်တမ်းတင်ရမည်။

### ၅.၃ ဆုံးဖြတ်ချက် အဖြေများ

#### အဖြေ ၁ — redaction ကို မည်သည့် အလွှာတွင် ထားမည်

**ရှင်းလင်းချက် —** credential ပုံစံပါသည့် ဖြစ်ရပ်သည် တစ်နေ့လျှင် 20.0 ခု ဖြစ်သည်။
အရင်းအမြစ်တွင် redact လုပ်ပါက လွတ်သွားသည့် နှုန်းသည် ၂ ရာခိုင်နှုန်း (0.4 ခု/နေ့၊ 146 ခု/နှစ်)၊
log writer တွင် လုပ်ပါက ၉ ရာခိုင်နှုန်း (1.8 ခု/နေ့၊ 657 ခု/နှစ်) ဖြစ်သည်။
incident အဖြစ် ပြောင်းလဲသည့် ဖြစ်နိုင်ခြေ 0.5 ရာခိုင်နှုန်း နှင့် incident တစ်ခုလျှင် 25,000 USD
ဖြင့် တွက်ပါက နှစ်စဉ် မျှော်မှန်းဆုံးရှုံးမှုသည် 18,250 USD နှင့် 82,125 USD ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** အရင်းအမြစ်တွင် redact လုပ်ရမည်။ ထိုသို့ လုပ်ခြင်းဖြင့် လွတ်သွားသည့်
credential အရေအတွက်သည် 77.8 % လျော့သည်၊ နှစ်စဉ် မျှော်မှန်းဆုံးရှုံးမှုသည် 63,875 USD လျော့သည်၊
detector ၏ နှစ်စဉ် ကုန်ကျစရိတ်သည် 584 USD ဖြစ်သဖြင့် net benefit သည် 63,291 USD ဖြစ်သည်။

**တိုင်းတာမည့် metric —** တစ်နေ့လျှင် လွတ်သွားသည့် credential အရေအတွက်၊
နှစ်စဉ် မျှော်မှန်းဆုံးရှုံးမှု USD၊ detector ကုန်ကျစရိတ် USD။ ဤဆုံးဖြတ်ချက်တွင်
ကုန်ကျစရိတ် နှစ်ခုလုံး (leak နှင့် detector) ကို ထည့်သွင်း စဉ်းစားထားသည်။

```bash
python3 - <<'PY'
events = 400_000
credential_rate = 1 / 20_000
credentials = events * credential_rate
print("events per day".ljust(34), events)
print("events holding a credential".ljust(34), round(credentials, 1))
escalation, incident_cost = 0.005, 25_000
for name, miss in (("redact at source", 0.02), ("redact at the writer", 0.09)):
    leaks = credentials * miss
    loss = leaks * 365 * escalation * incident_cost
    print(name.ljust(34), "miss pct", round(miss * 100, 1),
          "leaks per day", round(leaks, 2), "USD per year", round(loss))
print("loss difference USD".ljust(34), round(credentials * (0.09 - 0.02) * 365 * escalation * incident_cost))
print("detector cost USD per year".ljust(34), round(events * 0.000004 * 365, 2))
print("net benefit USD".ljust(34), round(credentials * (0.09 - 0.02) * 365 * escalation * incident_cost
                                             - events * 0.000004 * 365, 2))
print("leak reduction pct".ljust(34), round(100 * (0.09 - 0.02) / 0.09, 1))
PY
```

```text
events per day                     400000
events holding a credential        20.0
redact at source                   miss pct 2.0 leaks per day 0.4 USD per year 18250
redact at the writer               miss pct 9.0 leaks per day 1.8 USD per year 82125
loss difference USD                63875
detector cost USD per year         584.0
net benefit USD                    63291.0
leak reduction pct                 77.8
```

#### အဖြေ ၂ — key rotation interval ကို မည်မျှ သတ်မှတ်မည်

**ရှင်းလင်းချက် —** rotation ၉၀ ရက်တွင် နှစ်စဉ် rotation အရေအတွက်သည် 4.06 ဖြစ်ပြီး
ကုန်ကျစရိတ်သည် 6,083.33 USD ဖြစ်သည်။ ၃၀ ရက်တွင် 12.17 ဖြစ်ပြီး 18,250.00 USD ဖြစ်သည်၊
ဆိုလိုသည်မှာ 12,166.67 USD ပိုကုန်သည်။ exposure သည် 30.0 ရက်မှ 18.0 ရက်သို့ ကျဆင်းသည်၊
တစ်နေ့လျှင် 4,500 USD နှင့် ဖြစ်ပွားမှု ၂ ကြိမ်ဖြင့် နှစ်စဉ် 108,000 USD သက်သာသည်။

**ဆုံးဖြတ်ချက် —** ၃၀ ရက်ကို ရွေးရမည်၊ net benefit သည် 95,833.33 USD ဖြစ်သည်။
break-even ဖြစ်သည့် တစ်နေ့လျှင် ဆုံးရှုံးမှုသည် 506.94 USD ဖြစ်သည် — တကယ့် တစ်နေ့လျှင်
ဆုံးရှုံးနိုင်သည့် တန်ဖိုးသည် ထို တန်ဖိုးအောက် ကျဆင်းပါက ၉၀ ရက်ကို ဆက်ထားရမည်။

**တိုင်းတာမည့် metric —** incident တစ်ခုလျှင် exposure ရက်၊ နှစ်စဉ် exposure ရက်၊
နှစ်စဉ် rotation ကုန်ကျစရိတ် USD၊ နှစ်စဉ် မျှော်မှန်းဆုံးရှုံးမှု USD။ ဤဆုံးဖြတ်ချက်တွင်
security အကျိုးအမြတ်နှင့် လုပ်ငန်းလည်ပတ်မှု ကုန်ကျစရိတ် နှစ်ခုလုံးကို ထည့်သွင်း စဉ်းစားထားသည်။

```bash
python3 - <<'PY'
for interval in (90, 30):
    print("rotation days".ljust(34), interval,
          "rotations per year", round(365 / interval, 2),
          "USD per year", round(365 / interval * 6 * 250, 2))
p, detect, contain, incidents, loss_per_day = 0.8, 12, 3, 2, 4_500
def expected(rotation):
    return p * min(detect + contain, rotation) + (1 - p) * rotation
print("exposure 90 days".ljust(34), round(expected(90), 1), "days")
print("exposure 30 days".ljust(34), round(expected(30), 1), "days")
extra = (365 / 30 - 365 / 90) * 6 * 250
avoided = (expected(90) - expected(30)) * incidents * loss_per_day
print("extra rotation cost USD".ljust(34), round(extra, 2))
print("loss avoided USD per year".ljust(34), round(avoided, 2))
print("net benefit USD".ljust(34), round(avoided - extra, 2))
print("break-even loss per day USD".ljust(34), round(extra / ((expected(90) - expected(30)) * incidents), 2))
PY
```

```text
rotation days                      90 rotations per year 4.06 USD per year 6083.33
rotation days                      30 rotations per year 12.17 USD per year 18250.0
exposure 90 days                   30.0 days
exposure 30 days                   18.0 days
extra rotation cost USD            12166.67
loss avoided USD per year          108000.0
net benefit USD                    95833.33
break-even loss per day USD        506.94
```

## Self-check

၁။ အပိုင်း ၅.၁ အဖြေ ၁ တွင် control effectiveness မြင့်လာသည့်အခါ hazard အစဉ် (ranking) ပြောင်းလဲပါသလော၊
အကြောင်းရင်းကို ရှင်းလင်းပါ။

၂။ အပိုင်း ၅.၁ အဖြေ ၃ တွင် break-even exposure factor ကို မည်သို့ တွက်သည်၊ ထို တန်ဖိုးသည်
ဆုံးဖြတ်ချက်အပေါ် မည်သို့ သက်ရောက်သည်။

၃။ အပိုင်း ၅.၁ အဖြေ ၄ တွင် rotation interval သည် detect နှင့် contain အချိန်ထက် ကျဆင်းသည့်အခါ
exposure ကို မည်သည့်အရာက ဆုံးဖြတ်သည်။

၄။ အပိုင်း ၅.၁ အဖြေ ၆ တွင် object လျော့မှု ရာခိုင်နှုန်းသည် blast radius လျော့မှု ရာခိုင်နှုန်းထက်
မည်သောကြောင့် ကြီးသည်။

၅။ အပိုင်း ၅.၃ အဖြေ ၂ တွင် ၃၀ ရက် ရွေးချယ်မှုကို ပြောင်းလဲစေနိုင်သည့် အခြေအနေ တစ်ခုကို
ကိန်းဂဏန်းဖြင့် ဖော်ပြပါ။

<details>
<summary>အဖြေများ</summary>

၁။ မပြောင်းလဲပါ။ control effectiveness သည် score တိုင်းကို တူညီသည့် အချိုးဖြင့် မြှောက်သည်၊
ထို့ကြောင့် hazard များအကြား အစဉ်သည် တူညီနေသည်။ residual ပေါင်းလဒ်သာ လျော့သည်။

၂။ break-even exposure factor = exposure factor − control cost / (value × ARO) ဖြစ်သည်။
လေ့ကျင့်ခန်း ၃ တွင် ထို တန်ဖိုးသည် 0.052 ဖြစ်သည်၊ control သည် exposure factor ကို 0.052 အောက်သို့
လျှော့နိုင်မှသာ အကျိုးရှိသည်ဟု ဆုံးဖြတ်သည်။

၃။ rotation က ဆုံးဖြတ်သည်။ rotation ឞည် detect + contain ထက် ကျဆင်းပါက
min(detect + contain, rotation) = rotation ဖြစ်သဖြင့် exposure သည် rotation interval ဖြင့်
သတ်မှတ်ခံရသည်။ လေ့ကျင့်ခန်း ၄ တွင် rotation ၁၅ ရက်ဖြင့် exposure သည် 15.0 ရက် ဖြစ်သည်။

၄။ အကြောင်းမှာ scope အသစ်တွင် sensitive အချိုး ကျန်နေသည့်အတွက် ဖြစ်သည်။ object ကို 93.8 %
လျှော့သော်လည်း sensitive အချိုးသည် 12 % မှ 5 % သို့သာ ကျဆင်းသဖြင့် blast radius သည် 58.3 % သာ
လျော့သည်။

၅။ တစ်နေ့လျှင် ဆုံးရှုံးနိုင်သည့် တန်ဖိုးသည် 506.94 USD အောက် ကျဆင်းပါက (ဥပမာ 300 USD)
rotation ကို ၉၀ ရက် ဆက်ထားခြင်းသည် ပို၍ အကျိုးရှိသည်၊ အကြောင်းမှာ သက်သာသည့် ဆုံးရှုံးမှုသည်
12,166.67 USD ၏ rotation ကုန်ကျစရိတ် တိုးလာမှုကို မဖုံးနိုင်သောကြောင့် ဖြစ်သည်။

</details>

## References

- နယ်ပယ် အခြေခံ အချက်အလက် — `terms/11_security_and_governance.md` နှင့် `glossary/by_area/11_security_and_governance.json`။
- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed, from `rohitg00/ai-engineering-from-scratch`။
- လက်တွေ့ lab များ — `labs/lab_blast_radius.py`၊ `labs/lab_redaction_path.py`၊ `labs/lab_audit_volume.py`။
- ကိန်းဂဏန်း script များ — `scripts/ex_a_guardrail_cost.py`၊ `scripts/ex_b_audit_volume.py`၊ `scripts/ex_c_control_roi.py`။
- Documentation: [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)၊
  [NIST SP 800-92](https://csrc.nist.gov/pubs/sp/800/92/final)၊ [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final)၊
  [SLSA Software Attestations](https://slsa.dev/spec/v1.2/attestation-model)။
