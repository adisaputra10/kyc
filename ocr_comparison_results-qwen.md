# Perbandingan OCR: Qwen VL Plus vs Tesseract

## 📊 Ringkasan Perbandingan

**Jumlah gambar diproses:** 6

### ⚡ Kecepatan

| Metrik | Qwen VL Plus | Tesseract |
|--------|--------------|----------|
| Total Waktu | 29.48s | 3.01s |
| Rata-rata/Gambar | 4.91s | 0.50s |
| **Speedup** | - | **9.81x lebih cepat** |

### 🎯 Metrik Akurasi (vs Ground Truth)

**Ground Truth tersedia:** 6/6 gambar

| Metrik | Qwen VL Plus | Tesseract |
|--------|--------------|----------|
| **Accuracy** | **66.94%** | **56.46%** |
| CER (Error Rate) | 33.06% | 43.54% |
| WER (Error Rate) | 16.38% | 38.34% |
| Entity Precision | 69.16% | 62.52% |
| Entity Recall | 70.05% | 48.10% |
| **Entity F1** | **69.50%** | **53.86%** |
| **Layout Score** | **65.5** | **45.8** |

### 📊 Metrik Kualitatif

| Variable | Tesseract | Qwen-VL-Plus |
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
| 1.jpg | ✅ | 63.3% | 57.6% | 36.7% | 42.4% | 86.7% | 64.3% | 50/50 |
| 2.jpg | ✅ | 68.7% | 57.6% | 31.3% | 42.4% | 93.3% | 64.3% | 80/50 |
| 3.jpg | ✅ | 66.4% | 39.4% | 33.6% | 60.6% | 77.8% | 13.3% | 83/50 |
| 4.jpg | ✅ | 63.0% | 65.1% | 37.0% | 34.9% | 43.2% | 46.7% | 50/45 |
| 5.jpg | ✅ | 61.6% | 44.0% | 38.4% | 56.0% | 57.1% | 63.2% | 80/50 |
| 6.jpg | ✅ | 78.7% | 75.0% | 21.3% | 25.0% | 58.8% | 71.4% | 50/30 |

## 📄 Hasil OCR Detail

### 1.jpg

**Metrik:**
- Ground Truth: ✅
- Accuracy Qwen: 63.27%
- Accuracy Tesseract: 57.64%
- CER Qwen: 36.73%
- CER Tesseract: 42.36%
- WER Qwen: 7.38%
- WER Tesseract: 31.15%
- Entity F1 Qwen: 86.67%
- Entity F1 Tesseract: 64.29%
- Layout Score Qwen: 50.0
- Layout Score Tesseract: 50.0
- Waktu Qwen: 4.54s | Waktu Tesseract: 0.50s

#### 🤖 Qwen VL Plus

```
SAM SAM TRADING CO
(742016-W)
67,JLN MEWAH 25/63 TMN SRI MUDA,
40400 SHAH ALAM.
TEL/FAX : 03-51213881
GST NO: 001006288896

TAX INVOICE
==============
HE EOG UNICORN TWIN SUPER GLUE USG-99-
9557368063013 1 X 5.20 5.20 S
SS EZL A4 CYBER MIX COLOR PAPER 100'S8
2321008 1 X 8.90 8.90 S

No. Qtys: 2 No. Items: 2

TAX AMT (S) 6% RM 13.30
GST 6% RM 0.80
TAX AMT (Z) 0% RM 0.00
GST 0% RM 0.00
TAX AMT (E) 6% RM 0.00
EXC GST 6% RM 0.00

TOTAL RM 14.10
CASH RM 20.00

CHANGE RM 5.90

THANK YOU FOR SHOPPING
GOODS SOLD ARE NOT RETURNABLE.

Fri-v, 29-12-2017 Time : 20:17
Csr : SAM SAM
Wc5 SWH 01 Inv:R000721136
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
- Accuracy Qwen: 68.68%
- Accuracy Tesseract: 57.64%
- CER Qwen: 31.32%
- CER Tesseract: 42.36%
- WER Qwen: 9.02%
- WER Tesseract: 31.15%
- Entity F1 Qwen: 93.33%
- Entity F1 Tesseract: 64.29%
- Layout Score Qwen: 80.0
- Layout Score Tesseract: 50.0
- Waktu Qwen: 4.65s | Waktu Tesseract: 0.47s

#### 🤖 Qwen VL Plus

```
SAM SAM TRADING CO  
(742016-W)  
67, JLN MEWAH 25/63 TMN SRI MUDA,  
40400 SHAH ALAM.  
TEL/FAX : 03-51213881  
GST NO: 001006288896  

TAX INVOICE  
==============================  
HE EOG UNICORN TWIN SUPER GLUE USG-99-9557368063013 1 X 5.20 5.20 S  
SS EZL A4 CYBER MIX COLOR PAPER 100'SB 220008 1 X 8.90 8.90 S  

No. Qtys: 2 No. Items: 2  
-------------------------  
TAX AMT (S) 6% RM 13.30  
GST 6% RM 0.80  
TAX AMT (Z) 0% RM 0.00  
GST 0% RM 0.00  
TAX AMT (E) 6% RM 0.00  
EXC GST 6% RM 0.00  
-------------------------  
TOTAL RM 14.10  
CASH RM 20.00  

CHANGE RM 5.90  
-------------------------  
THANK YOU FOR SHOPPING  
GOODS SOLD ARE NOT RETURNABLE.  

Fri-v, 29-12-2017 Time : 20:17  
Cas r : SAM SAM  
WC5 SWH 01 Inv:R000721136  
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
- Accuracy Qwen: 66.40%
- Accuracy Tesseract: 39.42%
- CER Qwen: 33.60%
- CER Tesseract: 60.58%
- WER Qwen: 9.09%
- WER Tesseract: 63.64%
- Entity F1 Qwen: 77.78%
- Entity F1 Tesseract: 13.33%
- Layout Score Qwen: 83.0
- Layout Score Tesseract: 50.0
- Waktu Qwen: 6.38s | Waktu Tesseract: 0.54s

#### 🤖 Qwen VL Plus

```
AIK HUAT HARDWARE
ENTERPRISE (SETIA
ALAM) SDN BHD
822737-X
NO. 17-G, JALAN SETIA INDAH
(X) U13/X, SETIA ALAM,
SEKSYEN U13, 40170 SHAH ALAM,
TEL: 012 - 6651783 FAX: 03 - 33623608
GST NO: 000394528768

SIMPLIFIED TAX INVOICE

CASH

RECEIPT #: CSP0393921 DATE: 15/06/2017
SALESPERSON: AH002 TIME: 15:28:00

ITEM                      QTY    U/P    AMOUNT
                          (RM)   (RM)
2000160000024              1    15.00   15.00 S
20"  1.6KG X 500MM BIG STRETCH FILM ???

TOTAL QUANTITY             1

SUB-TOTAL (GST)           15.00
DISC                       0.00
ROUNDING                   0.00
---------------------------------
TOTAL                     15.00
CASH                      15.00
CHANGE                     0.00

*GST @ 6% INCLUDED IN TOTAL

GST SUMMARY
CODE  AMOUNT   %  TAX/AMT
SR     14.15   6      0.85
---------------------------------
TAX TOTAL:                 0.85

GOODS SOLD ARE NOT REFUNDABLE,
THANK YOU FOR CHOOSING US.
WE PROVIDE ORIGINAL BILL FOR GOODS
EXCHANGE WITHIN 1 WEEK FROM TRANSACTION.
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
- Accuracy Qwen: 63.04%
- Accuracy Tesseract: 65.09%
- CER Qwen: 36.96%
- CER Tesseract: 34.91%
- WER Qwen: 36.23%
- WER Tesseract: 25.60%
- Entity F1 Qwen: 43.24%
- Entity F1 Tesseract: 46.67%
- Layout Score Qwen: 50.0
- Layout Score Tesseract: 45.0
- Waktu Qwen: 7.00s | Waktu Tesseract: 0.77s

#### 🤖 Qwen VL Plus

```
LIGHTROOM GALLERY SDN BHD
No: 28, JALAN ASTANA 1C,
BANDAR ENOKIT RAJA, 41050
KLANG SELANGOR D.E, MALAYSIA
ROC No.: (1072825-A)
GST No.: 000584089600
Tel:03-3362 4395 Fax:03-3362 4395

CREDIT NOTE
Station: CASHIER
Cashier: ANGELA
Bill Date : 20/11/2017
Bill Start: 20/11/2017 03:57:01 PM
Code: 300-E0009
Name: ESWARAN 012-6369400
Address:
GST No.:

YT51129 YM36 BK 12W WW LED TRACK LIGHT 2* RM 45.29 UNL (5.43)=RM 90.57 SR
YT52683 YM44 35W WW BK TRACK HOLDER 1* RM 155.66 UNL (9.34)=RM 155.66 SR
CH50688 1METER TRACK-BK 1* RM 16.99 UNL (1.01)=RM 16.79 SR
RM39.80 CONTRA W LCNOO211 0* UNIT

Sub Total: RM 263.02
Item Discount: 0.20
Service Charge: 0.00
GSTI/TAX 6%: 15.78

TOTAL: RM 278.80
CASH: RM 278.80
CHANGE: RM 0.00

Item Count: 4
Qty Count: 4.0
Closed Bill: 20/11/2017 04:01:23 PM

Thank You, Please come again.
Goods Sold are not refundable,returnable
BANK ACC MBB 5128 4851 2118
BANK ACC MBB 5628 4732 1744
BANK ACC AMBANK 888 100 123 3706

GST Summary Amount(RM) Tax(RM)
SR @ 6% 263.02 15.78
ZR/OS/EZ 0.00 0.00
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
- Accuracy Qwen: 61.57%
- Accuracy Tesseract: 43.98%
- CER Qwen: 38.43%
- CER Tesseract: 56.02%
- WER Qwen: 28.89%
- WER Tesseract: 45.56%
- Entity F1 Qwen: 57.14%
- Entity F1 Tesseract: 63.16%
- Layout Score Qwen: 80.0
- Layout Score Tesseract: 50.0
- Waktu Qwen: 3.69s | Waktu Tesseract: 0.31s

#### 🤖 Qwen VL Plus

```
UNIHAKKA INTERNATIONAL SDN BHD
29 Mar 2018 18:13
(867388-U)
12 Jalan Tempol 7/4,Kawasan Perindustrian
Tampoi,81200 Johor Bahru,Johor
TAX INVOICE

Invoice #: OR18032602170347

Item                                      Qty       Total
SR 10010000035-1 Meat + 3 Vege          1         $7.10

Total Amount: $7.10
GST @8%: $0.40
Net Total: $7.10

Payment Mode                            Amount
CASH                                    $7.10
Change                                  $0.00

GST Summary                              Amount($)  Tax($)
SR = GST @8%                             6.70       0.40

GST REG #000858118534
BAR WANG RICE @ PERMAS JAYA
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
- Accuracy Qwen: 78.66%
- Accuracy Tesseract: 75.00%
- CER Qwen: 21.34%
- CER Tesseract: 25.00%
- WER Qwen: 7.69%
- WER Tesseract: 32.97%
- Entity F1 Qwen: 58.82%
- Entity F1 Tesseract: 71.43%
- Layout Score Qwen: 50.0
- Layout Score Tesseract: 30.0
- Waktu Qwen: 3.21s | Waktu Tesseract: 0.42s

#### 🤖 Qwen VL Plus

```
SUN WONG KUT SDN BHD
Company No: 20965-W
Site: 1046
176 JLN SUNGEI BESI
57100 KUALA LUMPUR.
Telephone: 03-9221345
GST No: 001580630016*

Invoice number: 60000483942
39.54 litre Pump # 07
FuelSave 95 RM 88.17 C
2.230 RM/ litre
Total RM 88.17
Visa RM 88.17
Relief GST C RM 0.00
Total Gross C RM 88.17
Shell Loyalty Card
6018840059147765
Points Awarded: 39

Date Time Num OPT
21/02/18 11:19 40278 07

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

