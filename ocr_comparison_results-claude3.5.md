# Perbandingan OCR: claude-3.5  vs Tesseract

## 📊 Ringkasan Perbandingan

**Jumlah gambar diproses:** 6

### ⚡ Kecepatan

| Metrik | claude-3.5  | Tesseract |
|--------|--------------|----------|
| Total Waktu | 109.12s | 3.05s |
| Rata-rata/Gambar | 18.19s | 0.51s |
| **Speedup** | - | **35.80x lebih cepat** |

### 🎯 Metrik Akurasi (vs Ground Truth)

**Ground Truth tersedia:** 6/6 gambar

| Metrik | claude-3.5  | Tesseract |
|--------|--------------|----------|
| **Accuracy** | **72.61%** | **56.46%** |
| CER (Error Rate) | 27.39% | 43.54% |
| WER (Error Rate) | 16.16% | 38.34% |
| Entity Precision | 61.49% | 62.52% |
| Entity Recall | 62.87% | 48.10% |
| **Entity F1** | **62.15%** | **53.86%** |
| **Layout Score** | **75.0** | **45.8** |

### 📊 Metrik Kualitatif

| Variable | Tesseract | claude-3.5-VL-Plus |
|----------|-----------|--------------|
| Entity Extraction F1 | Medium-Low | **High** |
| Layout Robustness | Low | **High** |
| End-to-End Verification | Rule-based | **Reasoning-based** |
| Rule Dependency | High | **Low** |
| Generalization | Low | **High** |
| Human Intervention | High | **Low** |

**Catatan:**
- CER (Character Error Rate) = % karakter yang berbeda
- WER (Word Error Rate) = % kata yang berbeda
- Semakin rendah CER/WER, semakin baik

## 📋 Detail Perbandingan Per Gambar

| File | GT | Acc Q | Acc T | CER Q | CER T | F1 Q | F1 T | Layout Q/T |
|------|:--:|-------|-------|-------|-------|------|------|------------|
| 1.jpg | ✅ | 78.0% | 57.6% | 22.0% | 42.4% | 83.9% | 64.3% | 80/50 |
| 2.jpg | ✅ | 78.7% | 57.6% | 21.3% | 42.4% | 77.4% | 64.3% | 80/50 |
| 3.jpg | ✅ | 55.8% | 39.4% | 44.2% | 60.6% | 55.6% | 13.3% | 50/50 |
| 4.jpg | ✅ | 75.0% | 65.1% | 25.0% | 34.9% | 41.0% | 46.7% | 80/45 |
| 5.jpg | ✅ | 62.0% | 44.0% | 38.0% | 56.0% | 40.0% | 63.2% | 80/50 |
| 6.jpg | ✅ | 86.1% | 75.0% | 13.9% | 25.0% | 75.0% | 71.4% | 80/30 |

## 📄 Hasil OCR Detail

### 1.jpg

**Metrik:**
- Ground Truth: ✅
- Accuracy claude-3.5: 78.03%
- Accuracy Tesseract: 57.64%
- CER claude-3.5: 21.97%
- CER Tesseract: 42.36%
- WER claude-3.5: 9.84%
- WER Tesseract: 31.15%
- Entity F1 claude-3.5: 83.87%
- Entity F1 Tesseract: 64.29%
- Layout Score claude-3.5: 80.0
- Layout Score Tesseract: 50.0
- Waktu claude-3.5: 19.33s | Waktu Tesseract: 0.51s

#### 🤖 claude-3.5 

```
SAM SAM TRADING CO
(742016-M)
67,JLN MEWAH 25/63 TMN SRI MUDA,
40400 SHAH ALAM.
TEL/FAX : 03-51213881
GST NO: 001006288896

TAX INVOICE

HE E06 UNICORN TWIN SUPER GLUE USG-99-
955736803013    1 X   5.20    5.20 S
SS EZL A4 CYBER MIX COLOR PAPER 100'S8
2970008         1 X   8.90    8.90 S

No. Qtys:        2 No. Items:    2

TAX AMT (S) 6%             RM 13.30
GST 6%                     RM 0.80
TAX AMT (Z) 0%             RM 0.00
GST 0%                     RM 0.00
TAX AMT (E) 6%             RM 0.00
EXC GST 6%                 RM 0.00

TOTAL               RM 14.10
CASH                RM 20.00
CHANGE              RM 5.90

THANK YOU FOR SHOPPING
GOODS SOLD ARE NOT RETURNABLE.

Friday, 29-12-2017  Time : 20:17
Cas. : SAM SAM
WCS  SWH  01  Inv:R000721136
```

#### 📝 Tesseract

```
SAM SAM TRADING CO
(742016-W)
67,JLN MEWAH 25/63 THN SRI MUDA,
40400 SHAH ALAM.
TEL/FAX : 03-51213881
BST NO: 001006288896

TAX INVOICE

HE EOG UNICORN TWIN SUPER GLUE USG-99-
9997368063013 1X $.20 5.20 §

$5 EZL A4 CYBER MIX COLOR PAPER 100758

2979008 1X 8.90 8.90 5
No. Qtyss 2 No. Items: 2
TAX AMT (S) 6% Rit 13.30
GST 62 RM 0.80
TAX AMT (Z) 0% RM 0.00
GST 02 RM 0.00
TAX ANT (E) 62 RH 0.00
EXC GST 62% RM 0.00
TOTAL RM 14.10
CASH RH 20.00
CHANGE RN 3.969

— Saat

THANK YOU FOR SHOPPING
GOODS SOLD ARE NOT RETURNABLE, ~

Frid-v, 29-12-2017 Time : 20:17
Cas, c : SAN SAM
Wc5 SWH 01 InvsR000721134

```

---

### 2.jpg

**Metrik:**
- Ground Truth: ✅
- Accuracy claude-3.5: 78.66%
- Accuracy Tesseract: 57.64%
- CER claude-3.5: 21.34%
- CER Tesseract: 42.36%
- WER claude-3.5: 10.66%
- WER Tesseract: 31.15%
- Entity F1 claude-3.5: 77.42%
- Entity F1 Tesseract: 64.29%
- Layout Score claude-3.5: 80.0
- Layout Score Tesseract: 50.0
- Waktu claude-3.5: 17.84s | Waktu Tesseract: 0.49s

#### 🤖 claude-3.5 

```
SAM SAM TRADING CO
(742016-W)
69,JLN MEWAH 25/63 TMN SRI MUDA,
40400 SHAH ALAM.
TEL/FAX : 03-51213881
GST NO: 001006288896

TAX INVOICE

HE E06 UNICORN TWIN SUPER GLUE USG-99-
9557368063013    1 X    5.20    5.20 $
SS EZL A4 CYBER MIX COLOR PAPER 100'S8
2325008         1 X    8.90    8.90 $

No. Qtys:         2 No. Items:    2

TAX AMT (S) 6%               RM 13.30
GST 6%                       RM 0.80
TAX AMT (Z) 0%               RM 0.00
GST 0%                       RM 0.00
TAX AMT (E) 6%               RM 0.00
EXC GST 6%                   RM 0.00

TOTAL                   RM 14.10
CASH                    RM 20.00

CHANGE                  RM 5.90

THANK YOU FOR SHOPPING
GOODS SOLD ARE NOT RETURNABLE.

Friday, 29-12-2017 Time : 20:17
Cas. r : SAM SAM
Wc5 SWH 01 Inv:ROO0721136
```

#### 📝 Tesseract

```
SAM SAM TRADING CO
(742016-W)
67,JLN MEWAH 25/63 THN SRI MUDA,
40400 SHAH ALAM.
TEL/FAX : 03-51213881
BST NO: 001006288896

TAX INVOICE

HE EOG UNICORN TWIN SUPER GLUE USG-99-
9997368063013 1X $.20 5.20 §

$5 EZL A4 CYBER MIX COLOR PAPER 100758

2979008 1X 8.90 8.90 5
No. Qtyss 2 No. Items: 2
TAX AMT (S) 6% Rit 13.30
GST 62 RM 0.80
TAX AMT (Z) 0% RM 0.00
GST 02 RM 0.00
TAX ANT (E) 62 RH 0.00
EXC GST 62% RM 0.00
TOTAL RM 14.10
CASH RH 20.00
CHANGE RN 3.969

— Saat

THANK YOU FOR SHOPPING
GOODS SOLD ARE NOT RETURNABLE, ~

Frid-v, 29-12-2017 Time : 20:17
Cas, c : SAN SAM
Wc5 SWH 01 InvsR000721134

```

---

### 3.jpg

**Metrik:**
- Ground Truth: ✅
- Accuracy claude-3.5: 55.76%
- Accuracy Tesseract: 39.42%
- CER claude-3.5: 44.24%
- CER Tesseract: 60.58%
- WER claude-3.5: 16.08%
- WER Tesseract: 63.64%
- Entity F1 claude-3.5: 55.56%
- Entity F1 Tesseract: 13.33%
- Layout Score claude-3.5: 50.0
- Layout Score Tesseract: 50.0
- Waktu claude-3.5: 17.17s | Waktu Tesseract: 0.53s

#### 🤖 claude-3.5 

```
AIK HUAT HARDWARE ENTERPRISE (SETIA ALAM) SDN BHD
822787-X
NO. 17-6, JALAN SETIA INDAH
(A) U13/X, SETIA ALAM,
SEKSYEN U13, 40170 SHAH ALAM,
TEL: 012 - 6651783 FAX: 03 - 33623688
GST NO: 000394528768

SIMPLIFIED TAX INVOICE

CASH
RECEIPT #: CSP0393921 DATE: 15/06/2017
SALESPERSON : AH002 TIME: 15:28:00

ITEM QTY U/P AMOUNT(RM)
2000160000024 1 15.00 15.00 S
20 1.8KG X 300MM BIG STRETCH FILM ???

TOTAL QUANTITY 1

SUB-TOTAL(GST) 15.00
DISC 0.00
ROUNDING 0.00
TOTAL 15.00
CASH 15.00
CHANGE 0.00

*GST @ 6% INCLUDED IN TOTAL

GST SUMMARY
CODE AMOUNT % TAX/AMT
SR 14.15 6 0.85

TAX TOTAL: 0.85

GOODS SOLD ARE NOT REFUNDABLE.
THANK YOU FOR CHOOSING US.
*PROVIDE ORIGINAL BILL FOR GOODS
EXCHANGE WITHIN 1 WEEK FROM TRANSACTION
GOODS MUST BE IN ORIGINAL STATE TO BE
ENTITLED FOR EXCHANGE.
```

#### 📝 Tesseract

```
HARDWARE
Se ETIA

“x
NO. 17-6, aA SETIA INDAH
X) U13/X, SETIA ALAH
SEKSYEN 13 “itt SHAH ALAN
TEL: O12 ~ 6651793 FAX: Us - 33633608
GST NO: GuOs94528769

SUAPLIFTED TAX THVODCE

RECEIPT #2 CSPO394921 OATES 15/06/2017
SALESPERSON ; AHOO2 TIME: 15:29:00

ITEH Oty U/P — ANOUNT
bl

Rit}
2000160000024 1 3.0 1S
20" 1.6KG X SOGHH BIG sinEICH FIL a

TAL QUANTITY 1

SUB-TOTAL (6ST) 5.00
UISC 0.00

ROUNDING 0.00
TOTAL 1i5.u0
CASH iS.ug
CHANGE G.00

TAX TOTALS 0.85

GOODS SOLD ARE NOY RERUNDABLE,
“THANE YOU FOR CHOUSING US.

3 PROVIDE ORLGINAL BILL KOR
BICHANGE WITHIN 1 SBEK PRO IRANSA/TION
GOODS HUSS BE IN ORIGINAL STATE 70 bE
ENTITLED FOR BXCHANGS.

```

---

### 4.jpg

**Metrik:**
- Ground Truth: ✅
- Accuracy claude-3.5: 75.00%
- Accuracy Tesseract: 65.09%
- CER claude-3.5: 25.00%
- CER Tesseract: 34.91%
- WER claude-3.5: 22.71%
- WER Tesseract: 25.60%
- Entity F1 claude-3.5: 41.03%
- Entity F1 Tesseract: 46.67%
- Layout Score claude-3.5: 80.0
- Layout Score Tesseract: 45.0
- Waktu claude-3.5: 23.37s | Waktu Tesseract: 0.77s

#### 🤖 claude-3.5 

```
LIGHTROOM GALLERY SDN BHD
G-54, JALAN ASTANA 1C,
BANDAR BUKIT RAJA, 41050
KLANG SELANGOR D.E, MALAYSIA
ROC No.: (1072825-A)
GST No.: 000584089600
Tel:03-3362 4395 Fax:03-3362 4395

CREDIT NOTE
Station: CASHIER    C/N No: LCN00212
Cashier: ANGELA     Cover: 1
Bill Date: 20/11/2017
Bill Start: 20/11/2017 03:57:01 PM

Code: 300-E0009
Name: ESWARAN 012-6369400
Address:
GST No.:

YT51129                                SR
VE36 BK 12W WW LED TRACK LIGHT
2 * RM 45.29 UNI ( 5.43)=RM 90.57
YT52683                               SR
YE44 35W WW BK TRACK HOLDER
1 * RM 155.66 UNI ( 9.34)=RM 155.66
CH50688                               SR
1METER TRACK-BK
1 * RM 16.99 UNI ( 1.01)=RM 16.79
RM39.80 CONTRA W LCN00211
0 * UNIT

Sub Total: RM 263.02
Item Discount: RM 0.20
Service Charge: RM 0.00
GST/TAX 6%: RM 15.78
TOT: RM 278.80
CASH: RM 278.80
CHANGE: 0.00

Item Count: 4
Qty Count: 4.0
Closed Bill: 20/11/2017 04:01:23 PM

Thank You, Please come again.
Goods Sold are not refundable, returnable
BANK ACC MBB 5123 4651 2118
BANK ACC MBB 5626 4732 1744
BANK ACC AMBANK 888 100 123 3706

GST Summary    Amount(RM)    Tax(RM)
SR @ 6%        263.02        15.78
ZR/OS/EZ       0.00          0.00
```

#### 📝 Tesseract

```
LIGHTROOM GALLERY SDN BHD
No: 28, TALAN ASTANA 1C
BANDAR LUKIT RAJA, 41050

KLANG SELANGOR D.E, MALAYSIA
ROC No. : (1072825-A)
GST No. : 000584089600
Tel:03-3362 4395 Fax:03-3362 4395

CREDIT NOTE
Station: CASHIER C/N No: LCNO0212
Cashier: ANGELA Cover : 1
Bill Date : 20/11/2017
Bill Start: 20/11/2017 03:57:01 PM

Code : 300-E0009

Name : ESWARAN 012-6369400

Address

GST No.

YT51129 SR

YE36 BK 12W WW LED TRACK LIGHT
-2  * RM 45.29 UNI ( 5.43)=RM 90. 57

YT52683 SR

YE44 35W WW BK TRACK HOLDER

1 * RM 155.66 UNI ( 9,34)=RM 155. 66

CH50688 SR

IMETER TRACK-BK

1 * RM 16.99 UNI ( 1.01)=RM 16. 7%

= SR
RM39. 80 CONTRA W LCNOO211

0 * UNIT

Sub Total : RM 263. 02
Item Discount 5 RM 0/20
Service Charge : RM 0), 00
GST/TAX 6% : RM 15. 78
TOT’ : RM 278.80

CAS1, : RM 278.80
CHANGE: RM 0. 00

Ttem Count: 4
Qty Count : 4.0

Closed Bill: 20/11/2017 04:01:23 PM

You, Please come again.
Tene Sold are not refundable, returnable
BANK ACC MBB 5128 4851 2118
BANK ACC MBB 5626 4732 1744
BANK ACC AMBANK 888 100 123 3706

GST Summary Amount (RM) Tax (RMD

‘ 5. 78
SR @ 6% 263, 02 15
ZR/0S/EZ 0. 00 0. 00

```

---

### 5.jpg

**Metrik:**
- Ground Truth: ✅
- Accuracy claude-3.5: 62.05%
- Accuracy Tesseract: 43.98%
- CER claude-3.5: 37.95%
- CER Tesseract: 56.02%
- WER claude-3.5: 27.78%
- WER Tesseract: 45.56%
- Entity F1 claude-3.5: 40.00%
- Entity F1 Tesseract: 63.16%
- Layout Score claude-3.5: 80.0
- Layout Score Tesseract: 50.0
- Waktu claude-3.5: 13.48s | Waktu Tesseract: 0.30s

#### 🤖 claude-3.5 

```
UNIHAKKA INTERNATIONAL SDN BHD
29 Mar 2016 18:19
(867386-U)
12 Jalan Tampoi 7/4,Kawasan Perindustrian
Tampoi,81200 Johor Bahru,Johor
TAX INVOICE
Invoice # : OR16032902170347

Item                                    Qty        Total
SR f00100000036- 1 Meat + 3 Vege       1         $7.10

Total Amount: $7.10
GST @6%: $0.40
Nett Total: $7.10

Payment Mode                            Amount
CASH                                    $7.10
Change                                  $0.00

GST Summary                            Amount($)    Tax($)
SR + GST@6%                            6.70         0.40

GST REG #000856195584
BAR WANG RICE@PERMAS JAYA
(Price Inclusive Of GST)
Thank You & Come Again!
Like and Follow Us on Facebook!
Facebook.com/BarWangRice
```

#### 📝 Tesseract

```
UNIHAKKA INTERNATIGNAL SDN BHD
29 Mar 2018 48:19
(867388-U)
42, Jalan Tampoi 74,Kawasan Perindustrian
Tampoi,81200 Johor Bahru,lohor
TAXINVOICE
Invoice # : OR 1802602170347

tem aty

SR ODTGOOG003S- 1 Meat +3 Vege
$7.10 1 $7.10
Total Amount: $7.40
GST @B%: $0.40
Nett Totai: $7.10
Payment Mode Amount
CASH 5710
Change $0.00
mous) Texts)
em a0

GST REG #0008581 50584

BAR WANG RICE@PERMAS JAYA
(Price Inctusive Of GST)
Thank You & Come Again!

Like and Follow Us on Facebook!
Facebook.com'BarWangRice

```

---

### 6.jpg

**Metrik:**
- Ground Truth: ✅
- Accuracy claude-3.5: 86.15%
- Accuracy Tesseract: 75.00%
- CER claude-3.5: 13.85%
- CER Tesseract: 25.00%
- WER claude-3.5: 9.89%
- WER Tesseract: 32.97%
- Entity F1 claude-3.5: 75.00%
- Entity F1 Tesseract: 71.43%
- Layout Score claude-3.5: 80.0
- Layout Score Tesseract: 30.0
- Waktu claude-3.5: 17.92s | Waktu Tesseract: 0.43s

#### 🤖 claude-3.5 

```
SUN WONG KUI SDN BHD
Company No: 20965-W
Site: 1046
176 JLN SUNGEI BESI,
57100 KUALA LUMPUR.
Telephone: 03-9221345
GST No: 001580630016

Invoice number 600000483942

39.54 litre Pump # 07
FuelSave 95    RM   88.17 C
2.230 RM / litre
Total          RM   88.17
Visa           RM   88.17
Relief GST   C RM    0.00
Total Gross  C RM   88.17

Shell Loyalty Card
601884005914776
Points Awarded: 39

Date      Time   Num   OPT
21/02/18  11:19  40278  07

Diesel & Petrol RON95
given Relief under Section
56 (3) (b) GST Act 2014

Thank you
Please come again
```

#### 📝 Tesseract

```
SUN WONG KUT SON BHD
Company No 20965-¥
Site: 1046

176 JLN SUNGEI BESI
57100 KUALA LUMPUR
Telephone: 03-9221345
GST No: 001580630016"

Invoice number 60000483942

39.54 litre Punp # 07
FuelSave 95 RN 88 17 C
2.230 RN / litre
Total RN = =88. 17
Visa RN = 88.17

0

1
1
Relief GST C RN 0.0
Total Gross C RM 88.1
Shell Loyalty Card
6018840059147765

Points Awarded: 39

Date Tine Nun OPT
21/02/18 11.19 40278 07

Diesel & Petrol RON95
geen Relief under Section
6 (3) (b) GST Act 2014

Thank you
Please come again


```

---

