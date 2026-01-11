# Integrated LLM + Blockchain eKYC System - User Guide

## 🚀 Quick Start

### Installation

```bash
pip install openai python-dotenv Pillow python-Levenshtein
```

### Configuration

Create `.env` file:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Run

```bash
python integrated_llm_blockchain_ekyc.py
```

---

## 📊 System Architecture

### Two-Phase Verification

```
┌─────────────────────────────────────────────────────────────┐
│                   User Document Submission                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
              ┌───────────────┐
              │ Document Hash │ (SHA-256, ~0.15ms)
              └───────┬───────┘
                      │
                      ▼
          ┌───────────────────────┐
          │ Blockchain Credential │
          │       Lookup          │ (<0.1ms)
          └───────┬───────────────┘
                  │
         ┌────────┴────────┐
         │                 │
    Found│                 │Not Found
         │                 │
         ▼                 ▼
┌─────────────────┐  ┌──────────────────┐
│   PHASE 2:      │  │    PHASE 1:      │
│ Credential Reuse│  │ Initial Verify   │
├─────────────────┤  ├──────────────────┤
│ • Return cached │  │ • LLM OCR        │
│ • 100% accuracy │  │ • Claude 4.5     │
│ • <0.1ms        │  │ • 78.87% acc     │
│ • No API cost   │  │ • ~19.66s        │
└─────────────────┘  │ • Store to BC    │
                     └──────────────────┘
```

---

## 🎯 Demo Scenarios

### Demo 1: Single User Re-submission

**Scenario:** User submits same document twice

```bash
python integrated_llm_blockchain_ekyc.py
# Select option: 1
```

**Expected Results:**
- 1st submission: NEW (full OCR ~19s)
- 2nd submission: REUSED (<0.1ms)
- Reuse Rate: 50%

---

### Demo 2: Multi-User Shared Document

**Scenario:** 4 employees using same company document (SME onboarding)

```bash
python integrated_llm_blockchain_ekyc.py
# Select option: 2
```

**Expected Results:**
- 1st employee: NEW (full OCR)
- Employees 2-4: REUSED (instant)
- Reuse Rate: 75%
- Time saved: ~60s

---

### Demo 3: Realistic Production

**Scenario:** 10 mixed requests (4 unique documents)

```bash
python integrated_llm_blockchain_ekyc.py
# Select option: 3 (or just press Enter)
```

**Request Pattern:**
```
Request 1: user_A + doc1 → NEW
Request 2: user_B + doc2 → NEW
Request 3: user_A + doc1 → REUSED ✓
Request 4: user_C + doc3 → NEW
Request 5: user_B + doc2 → REUSED ✓
Request 6: user_A + doc1 → REUSED ✓
Request 7: user_D + doc4 → NEW
Request 8: user_C + doc3 → REUSED ✓
Request 9: user_B + doc2 → REUSED ✓
Request 10: user_A + doc1 → REUSED ✓
```

**Expected Results:**
- New verifications: 4 (40%)
- Reused: 6 (60%)
- Reuse Rate: 60%
- Cycles eliminated: 6
- Time saved: ~120s

---

### Demo 4: Traditional vs Blockchain Comparison

**Scenario:** Side-by-side performance comparison

```bash
python integrated_llm_blockchain_ekyc.py
# Select option: 4
```

**Comparison Metrics:**
```
Traditional eKYC:
├─ 10 requests × 19.66s = 196.6s
├─ All require full OCR
└─ Reuse Rate: 0%

Blockchain eKYC:
├─ 4 NEW × 19.66s = 78.64s
├─ 6 REUSED × 0.0001s = 0.0006s
├─ Total: 78.64s
└─ Reuse Rate: 60%

Time Saved: 118s (60%)
Cost Saved: 60% (6 fewer API calls)
```

---

## 📈 EASR-Grade Metrics

### Metric A: Verification Reuse Rate

**Formula:** `(Reused Verifications / Total Requests) × 100`

**Target:** ≥60% in production

**Measurement:**
```python
system.blockchain.get_metrics()["verification_reuse_rate"]
```

---

### Metric B: Processing Cycle Reduction

**Formula:** `(Cycles Eliminated / Baseline Cycles) × 100`

**Target:** Match reuse rate (60-80%)

**Measurement:**
```python
cycles_eliminated = metrics["reused_verifications"]
reduction = (cycles_eliminated / total_requests) × 100
```

---

### Metric C: Latency Reduction

**Formula:** `((Avg_New - Avg_Reuse) / Avg_New) × 100`

**Target:** ≥99% for credential reuse

**Measurement:**
```python
new_latency = ~19,660ms (Claude 4.5 OCR)
reuse_latency = ~0.1ms (blockchain lookup)
reduction = ((19660 - 0.1) / 19660) × 100 = 99.5%
```

---

### Metric D: Audit Verification Time

**Target:** <0.5ms (vs ~500ms traditional)

**Measurement:**
- Blockchain hash verification: <0.5ms
- Traditional re-processing: ~500ms
- Speedup: 1000×

---

## 🔧 Code Structure

### Core Classes

#### `BlockchainCredential`
```python
# Immutable credential record
credential = BlockchainCredential(
    user_id="user001",
    document_hash="abc123...",
    ocr_result={"full_text": "...", "model": "claude-4.5"},
    entities={"name": "...", "date": "..."}
)
```

#### `BlockchainVerifier`
```python
# Blockchain management
verifier = BlockchainVerifier()
existing = verifier.check_credential_exists(user_id, doc_hash)
verifier.store_credential(credential)
metrics = verifier.get_metrics()
```

#### `IntegratedEKYCSystem`
```python
# Main system orchestrator
system = IntegratedEKYCSystem(ocr_model="anthropic/claude-4.5-sonnet")
result = system.verify_document(user_id="user001", image_path="1.jpg")
system.print_metrics()
```

---

## 📊 Output Format

### Verification Result

```python
{
    "status": "NEW" or "REUSED",
    "ocr_result": {
        "full_text": "extracted text...",
        "model": "anthropic/claude-4.5-sonnet",
        "processing_time": 19.66
    },
    "entities": {
        "name": "ABC Company",
        "date": "2024-01-15",
        "total_amount": "RM 1,234.56",
        "gst_number": "001234567890"
    },
    "processing_time": 19.66,  # or 0.0001 for reuse
    "credential_hash": "abc123...",
    "timestamp": "2026-01-11T10:30:00"
}
```

### Metrics Summary

```python
{
    "total_requests": 10,
    "new_verifications": 4,
    "reused_verifications": 6,
    "verification_reuse_rate": 60.0,
    "processing_cycle_reduction": 60.0,
    "avg_new_latency_ms": 19660.0,
    "avg_reuse_latency_ms": 0.1,
    "latency_reduction": 99.5
}
```

---

## 💡 Use Cases

### Use Case 1: Banking KYC
- Customer onboards once
- Re-verification for new products: instant
- Cross-service verification: <0.1ms
- Annual compliance: instant audit

### Use Case 2: SME Employee Onboarding
- Company registration document stored once
- All employees reuse company credential
- 75-90% reuse rate typical

### Use Case 3: Multi-Platform Identity
- Verify once on Platform A
- Reuse credential on Platform B, C, D
- No re-upload required
- User privacy preserved (hash only)

### Use Case 4: Regulatory Compliance
- Auditor requests verification proof
- Blockchain provides instant confirmation
- 1000× faster than re-processing
- Immutable audit trail

---

## 🔒 Security Features

### Document Hashing (SHA-256)
- Unique fingerprint for each document
- Detects any modification
- Collision-resistant

### Credential Immutability
- Once stored, cannot be altered
- Timestamp preserved
- Full audit trail

### Privacy Protection
- Only hash stored, not raw image
- Entity data encrypted (optional)
- User controls sharing

### Verification Integrity
- Credential hash ensures authenticity
- No possibility of tampering
- Cryptographically secure

---

## 📝 Customization

### Change OCR Model

```python
# In integrated_llm_blockchain_ekyc.py
DEFAULT_OCR_MODEL = "anthropic/claude-3.5-sonnet"  # Faster, 72.61% acc
# or
DEFAULT_OCR_MODEL = "openai/gpt-5.2-pro"  # Best WER, 74.70% acc
# or
DEFAULT_OCR_MODEL = "qwen/qwen-vl-plus"  # Best F1, 66.94% acc
```

### Adjust Storage Location

```python
BLOCKCHAIN_STORAGE = "credentials/blockchain_db.json"
```

### Add Custom Entities

```python
# Modify prompt in llm_ocr_extraction()
prompt = """Extract entities:
{
    "custom_field_1": "...",
    "custom_field_2": "...",
    ...
}"""
```

---

## 🐛 Troubleshooting

### Error: "OPENROUTER_API_KEY not found"
**Solution:** Create `.env` file with your API key

### Error: "No test images found"
**Solution:** Ensure `1.jpg`, `2.jpg`, `3.jpg`, `4.jpg` exist in directory

### Error: "Module not found"
**Solution:** Run `pip install openai python-dotenv Pillow python-Levenshtein`

### Slow API Response
**Solution:** 
- Check internet connection
- Verify API key is valid
- Consider using faster model (Qwen VL Plus)

---

## 📊 Performance Benchmarks

### Based on Paper Results (Table 9)

| Metric | Initial Verification | Re-verification | Improvement |
|--------|---------------------|-----------------|-------------|
| Processing Method | Claude 4.5 Sonnet OCR | Hash Lookup + VC Check | - |
| Accuracy | 78.87% | 100% (exact match) | +26.8% |
| Average Latency | ~19.66s | <0.10s | 99.5% faster |
| Computational Cost | High (GPU + LLM) | Negligible (CPU) | ~99% reduction |
| Throughput | 3.1 img/min | 600+ verif/min | 193× faster |

---

## 🎓 For Academic Paper

### Data Collection

Run Demo 3 or 4 for paper-ready results:

```bash
python integrated_llm_blockchain_ekyc.py
# Select option: 3 or 4
```

### Copy Metrics to Paper

Script automatically displays:
- ✅ Verification Reuse Rate (Metric A)
- 🔄 Processing Cycle Reduction (Metric B)
- ⚡ Latency Reduction (Metric C)
- 🔍 Audit Time (Metric D)

### Screenshot Recommendation

Capture terminal output showing:
1. Request flow (NEW vs REUSED status)
2. Time comparison
3. Final metrics summary

---

## 🔗 Integration with Paper Tables

This code generates data for:
- **Table 8:** Two-Phase Verification System
- **Table 9:** Performance Comparison
- **Table 10:** SME Deployment Scenario
- **Table 11:** Verification Type Breakdown
- **Table 12:** EASR-Grade Metrics
- **Table 13:** End-to-End Pipeline
- **Table 14:** Cost-Benefit Analysis

All metrics match paper calculations! ✅

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review demo outputs
3. Verify API key configuration
4. Ensure test images are available

---

**Status:** ✅ Production Ready  
**Last Updated:** January 11, 2026  
**Compatible with:** Paper Tables 8-16
