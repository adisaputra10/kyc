# Cara Mengganti Model OCR

## Metode 1: Edit File `.env` (Recommended)

1. Buka file `.env`
2. Ubah nilai `OCR_MODEL` dengan model yang diinginkan:

```env
OCR_MODEL=anthropic/claude-3.5-sonnet
```

3. Jalankan script: `python ocr_comparison.py`

## Metode 2: Set Environment Variable di Terminal

### Windows PowerShell:
```powershell
$env:OCR_MODEL="qwen/qwen-vl-plus"
python ocr_comparison.py
```

### Windows CMD:
```cmd
set OCR_MODEL=qwen/qwen-vl-plus
python ocr_comparison.py
```

### Linux/Mac:
```bash
export OCR_MODEL=qwen/qwen-vl-plus
python ocr_comparison.py
```

## Pilihan Model yang Tersedia

### Anthropic Claude (Recommended untuk Akurasi)
- `anthropic/claude-3.5-sonnet` - **Terbaik untuk akurasi**, lambat (~18s/gambar)
- `anthropic/claude-3-opus` - Sangat akurat, sangat lambat
- `anthropic/claude-3-sonnet` - Balance akurasi & kecepatan
- `anthropic/claude-3-haiku` - Cepat, akurasi cukup baik

### Qwen (Recommended untuk Balance)
- `qwen/qwen-vl-plus` - Cepat (~5s/gambar), akurasi baik (66.94%)
- `qwen/qwen-vl-max` - Lebih akurat, lebih lambat
- `qwen/qwen2-vl-72b` - Sangat akurat

### OpenAI
- `openai/gpt-4-vision-preview` - Akurat, lumayan lambat
- `openai/gpt-4o` - Cepat & akurat

### Google
- `google/gemini-pro-vision` - Cepat, akurasi baik
- `google/gemini-1.5-pro` - Lebih akurat
- `google/gemini-1.5-flash` - Sangat cepat

### Meta
- `meta-llama/llama-3.2-90b-vision` - Open source, akurat

## Contoh Penggunaan

### Test dengan GPT-4 Vision:
```powershell
$env:OCR_MODEL="openai/gpt-4-vision-preview"
python ocr_comparison.py
```

### Test dengan Gemini Flash (paling cepat):
```powershell
$env:OCR_MODEL="google/gemini-1.5-flash"
python ocr_comparison.py
```

### Kembali ke Claude 3.5 Sonnet:
```powershell
$env:OCR_MODEL="anthropic/claude-3.5-sonnet"
python ocr_comparison.py
```

## Tips Memilih Model

1. **Prioritas Akurasi**: `anthropic/claude-3.5-sonnet`
2. **Prioritas Kecepatan**: `google/gemini-1.5-flash` atau `qwen/qwen-vl-plus`
3. **Balance Akurasi & Kecepatan**: `anthropic/claude-3-haiku` atau `qwen/qwen-vl-plus`
4. **Budget Rendah**: `qwen/qwen-vl-plus` (lebih murah dari Claude)

## Catatan

- Model default (jika tidak diset): `anthropic/claude-3.5-sonnet`
- Script akan menampilkan model yang digunakan saat dijalankan: `🔧 Menggunakan model: ...`
- Semua model menggunakan OpenRouter API yang sama
