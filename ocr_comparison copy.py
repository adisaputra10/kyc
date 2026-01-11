import os
import base64
import time
from openai import OpenAI
import pytesseract
from PIL import Image
from difflib import SequenceMatcher
import Levenshtein
from tabulate import tabulate

# Konfigurasi
OPENROUTER_API_KEY = "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"
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\user\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Client OpenRouter
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def encode_image_to_base64(image_path):
    """Encode gambar ke base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def ocr_qwen(image_path):
    """OCR menggunakan Qwen VL Plus"""
    try:
        start_time = time.time()
        
        base64_image = encode_image_to_base64(image_path)
        image_ext = os.path.splitext(image_path)[1].lower()
        mime_type = f"image/{image_ext[1:]}" if image_ext in ['.jpg', '.jpeg', '.png'] else "image/jpeg"
        
        response = client.chat.completions.create(
            model="qwen/qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please extract all text from this image. Provide only the text content without any additional explanation."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000
        )
        
        elapsed_time = time.time() - start_time
        ocr_text = response.choices[0].message.content
        
        return {
            "success": True,
            "text": ocr_text,
            "time": elapsed_time,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "text": None,
            "time": 0,
            "error": str(e)
        }

def ocr_tesseract(image_path):
    """OCR menggunakan Tesseract"""
    try:
        start_time = time.time()
        
        image = Image.open(image_path)
        ocr_text = pytesseract.image_to_string(image)
        
        elapsed_time = time.time() - start_time
        
        return {
            "success": True,
            "text": ocr_text,
            "time": elapsed_time,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "text": None,
            "time": 0,
            "error": str(e)
        }

def calculate_similarity(text1, text2):
    """Hitung similarity antara dua teks"""
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1, text2).ratio() * 100

def calculate_cer(reference, hypothesis):
    """
    Calculate Character Error Rate (CER)
    CER = (Substitutions + Deletions + Insertions) / Total Characters in Reference
    """
    if not reference or not hypothesis:
        return 100.0
    
    # Normalize whitespace
    ref = reference.strip()
    hyp = hypothesis.strip()
    
    if len(ref) == 0:
        return 100.0
    
    # Calculate Levenshtein distance
    distance = Levenshtein.distance(ref, hyp)
    cer = (distance / len(ref)) * 100
    
    return min(cer, 100.0)  # Cap at 100%

def calculate_wer(reference, hypothesis):
    """
    Calculate Word Error Rate (WER)
    WER = (Substitutions + Deletions + Insertions) / Total Words in Reference
    """
    if not reference or not hypothesis:
        return 100.0
    
    # Split into words
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    
    if len(ref_words) == 0:
        return 100.0
    
    # Calculate Levenshtein distance at word level
    distance = Levenshtein.distance(ref_words, hyp_words)
    wer = (distance / len(ref_words)) * 100
    
    return min(wer, 100.0)  # Cap at 100%

def main():
    # Daftar gambar yang akan diproses
    image_files = [f"{i}.jpg" for i in range(1, 7)]
    
    results = []
    
    print("="*80)
    print("PERBANDINGAN OCR: Qwen VL Plus vs Tesseract")
    print("="*80)
    
    for image_file in image_files:
        if not os.path.exists(image_file):
            print(f"\n⚠ File tidak ditemukan: {image_file}")
            continue
        
        print(f"\n{'='*80}")
        print(f"Memproses: {image_file}")
        print(f"{'='*80}")
        
        # OCR dengan Qwen VL Plus
        print("→ Qwen VL Plus...", end=" ")
        qwen_result = ocr_qwen(image_file)
        if qwen_result["success"]:
            print(f"✓ ({qwen_result['time']:.2f}s)")
        else:
            print(f"✗ Error: {qwen_result['error']}")
        
        # OCR dengan Tesseract
        print("→ Tesseract...", end=" ")
        tesseract_result = ocr_tesseract(image_file)
        if tesseract_result["success"]:
            print(f"✓ ({tesseract_result['time']:.2f}s)")
        else:
            print(f"✗ Error: {tesseract_result['error']}")
        
        # Hitung metrik perbandingan
        similarity = 0
        cer_qwen_ref = 0
        cer_tess_ref = 0
        wer_qwen_ref = 0
        wer_tess_ref = 0
        
        if qwen_result["success"] and tesseract_result["success"]:
            similarity = calculate_similarity(qwen_result["text"], tesseract_result["text"])
            
            # CER & WER dengan Qwen sebagai referensi
            cer_qwen_ref = calculate_cer(qwen_result["text"], tesseract_result["text"])
            wer_qwen_ref = calculate_wer(qwen_result["text"], tesseract_result["text"])
            
            # CER & WER dengan Tesseract sebagai referensi
            cer_tess_ref = calculate_cer(tesseract_result["text"], qwen_result["text"])
            wer_tess_ref = calculate_wer(tesseract_result["text"], qwen_result["text"])
            
            print(f"\nSimilarity: {similarity:.2f}%")
            print(f"CER (Tesseract vs Qwen ref): {cer_qwen_ref:.2f}%")
            print(f"WER (Tesseract vs Qwen ref): {wer_qwen_ref:.2f}%")
        
        results.append({
            "file": image_file,
            "qwen": qwen_result,
            "tesseract": tesseract_result,
            "similarity": similarity,
            "cer_qwen_ref": cer_qwen_ref,
            "wer_qwen_ref": wer_qwen_ref,
            "cer_tess_ref": cer_tess_ref,
            "wer_tess_ref": wer_tess_ref
        })
    
    # Simpan hasil perbandingan
    print(f"\n{'='*80}")
    print("Menyimpan hasil perbandingan...")
    
    # Simpan ke file TXT
    with open("ocr_comparison_results.txt", "w", encoding="utf-8") as f:
        # Summary
        f.write("="*80 + "\n")
        f.write("RINGKASAN PERBANDINGAN OCR\n")
        f.write("="*80 + "\n\n")
        
        total_qwen_time = sum(r["qwen"]["time"] for r in results if r["qwen"]["success"])
        total_tesseract_time = sum(r["tesseract"]["time"] for r in results if r["tesseract"]["success"])
        avg_similarity = sum(r["similarity"] for r in results) / len(results) if results else 0
        avg_cer_qwen_ref = sum(r["cer_qwen_ref"] for r in results) / len(results) if results else 0
        avg_wer_qwen_ref = sum(r["wer_qwen_ref"] for r in results) / len(results) if results else 0
        avg_cer_tess_ref = sum(r["cer_tess_ref"] for r in results) / len(results) if results else 0
        avg_wer_tess_ref = sum(r["wer_tess_ref"] for r in results) / len(results) if results else 0
        
        f.write(f"Jumlah gambar diproses: {len(results)}\n")
        f.write(f"\n{'='*80}\n")
        f.write(f"KECEPATAN\n")
        f.write(f"{'='*80}\n")
        f.write(f"Qwen VL Plus:\n")
        f.write(f"  - Total waktu: {total_qwen_time:.2f}s\n")
        f.write(f"  - Rata-rata: {total_qwen_time/len(results):.2f}s per gambar\n")
        f.write(f"\nTesseract:\n")
        f.write(f"  - Total waktu: {total_tesseract_time:.2f}s\n")
        f.write(f"  - Rata-rata: {total_tesseract_time/len(results):.2f}s per gambar\n")
        f.write(f"\nKesimpulan: Tesseract {'lebih cepat' if total_tesseract_time < total_qwen_time else 'lebih lambat'} ")
        f.write(f"{abs(total_qwen_time - total_tesseract_time):.2f}s dari Qwen VL Plus\n")
        
        f.write(f"\n{'='*80}\n")
        f.write(f"METRIK AKURASI\n")
        f.write(f"{'='*80}\n")
        f.write(f"Similarity (Text Matching): {avg_similarity:.2f}%\n")
        f.write(f"\nDengan Qwen VL Plus sebagai referensi:\n")
        f.write(f"  - Avg CER Tesseract: {avg_cer_qwen_ref:.2f}% (semakin rendah semakin baik)\n")
        f.write(f"  - Avg WER Tesseract: {avg_wer_qwen_ref:.2f}% (semakin rendah semakin baik)\n")
        f.write(f"\nDengan Tesseract sebagai referensi:\n")
        f.write(f"  - Avg CER Qwen: {avg_cer_tess_ref:.2f}% (semakin rendah semakin baik)\n")
        f.write(f"  - Avg WER Qwen: {avg_wer_tess_ref:.2f}% (semakin rendah semakin baik)\n")
        f.write(f"\nInterpretasi:\n")
        f.write(f"  - CER (Character Error Rate) = % karakter yang berbeda\n")
        f.write(f"  - WER (Word Error Rate) = % kata yang berbeda\n")
        f.write(f"  - Nilai 0% = identik, 100% = sangat berbeda\n")
        
        # Detail hasil per gambar
        f.write("\n" + "="*80 + "\n")
        f.write("HASIL DETAIL PER GAMBAR\n")
        f.write("="*80 + "\n")
        
        for result in results:
            f.write(f"\n{'='*80}\n")
            f.write(f"File: {result['file']}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Similarity: {result['similarity']:.2f}%\n")
            f.write(f"CER (Tess vs Qwen ref): {result['cer_qwen_ref']:.2f}% | WER: {result['wer_qwen_ref']:.2f}%\n")
            f.write(f"CER (Qwen vs Tess ref): {result['cer_tess_ref']:.2f}% | WER: {result['wer_tess_ref']:.2f}%\n")
            f.write(f"Waktu Qwen: {result['qwen']['time']:.2f}s | Waktu Tesseract: {result['tesseract']['time']:.2f}s\n")
            
            f.write(f"\n--- QWEN VL PLUS ---\n")
            if result["qwen"]["success"]:
                f.write(result["qwen"]["text"])
            else:
                f.write(f"Error: {result['qwen']['error']}")
            
            f.write(f"\n\n--- TESSERACT ---\n")
            if result["tesseract"]["success"]:
                f.write(result["tesseract"]["text"])
            else:
                f.write(f"Error: {result['tesseract']['error']}")
            
            f.write("\n\n")
    
    # Simpan ke file Markdown
    with open("ocr_comparison_results.md", "w", encoding="utf-8") as f:
        f.write("# Perbandingan OCR: Qwen VL Plus vs Tesseract\n\n")
        
        f.write("## 📊 Ringkasan Perbandingan\n\n")
        f.write(f"**Jumlah gambar diproses:** {len(results)}\n\n")
        
        # Tabel Ringkasan Metrik
        f.write("### ⚡ Kecepatan\n\n")
        f.write("| Metrik | Qwen VL Plus | Tesseract |\n")
        f.write("|--------|--------------|----------|\n")
        f.write(f"| Total Waktu | {total_qwen_time:.2f}s | {total_tesseract_time:.2f}s |\n")
        f.write(f"| Rata-rata/Gambar | {total_qwen_time/len(results):.2f}s | {total_tesseract_time/len(results):.2f}s |\n")
        f.write(f"| **Speedup** | - | **{total_qwen_time/total_tesseract_time:.2f}x lebih cepat** |\n\n")
        
        f.write("### 🎯 Akurasi\n\n")
        f.write("| Metrik | Qwen VL Plus | Tesseract |\n")
        f.write("|--------|--------------|----------|\n")
        f.write(f"| Similarity | {avg_similarity:.2f}% | {avg_similarity:.2f}% |\n")
        f.write(f"| Avg CER | {avg_cer_tess_ref:.2f}% | {avg_cer_qwen_ref:.2f}% |\n")
        f.write(f"| Avg WER | {avg_wer_tess_ref:.2f}% | {avg_wer_qwen_ref:.2f}% |\n\n")
        
        f.write("**Catatan:**\n")
        f.write("- CER (Character Error Rate) = % karakter yang berbeda\n")
        f.write("- WER (Word Error Rate) = % kata yang berbeda\n")
        f.write("- Semakin rendah CER/WER, semakin baik\n\n")
        
        # Tabel Detail Per Gambar
        f.write("## 📋 Detail Perbandingan Per Gambar\n\n")
        f.write("| File | Qwen Time | Tess Time | Similarity | CER (Tess vs Q) | WER (Tess vs Q) |\n")
        f.write("|------|-----------|-----------|------------|-----------------|------------------|\n")
        for result in results:
            f.write(f"| {result['file']} | {result['qwen']['time']:.2f}s | {result['tesseract']['time']:.2f}s | ")
            f.write(f"{result['similarity']:.2f}% | {result['cer_qwen_ref']:.2f}% | {result['wer_qwen_ref']:.2f}% |\n")
        f.write("\n")
        
        # Detail hasil per gambar
        f.write("## 📄 Hasil OCR Detail\n\n")
        
        for result in results:
            f.write(f"### {result['file']}\n\n")
            
            f.write("**Metrik:**\n")
            f.write(f"- Similarity: {result['similarity']:.2f}%\n")
            f.write(f"- CER (Tesseract vs Qwen): {result['cer_qwen_ref']:.2f}%\n")
            f.write(f"- WER (Tesseract vs Qwen): {result['wer_qwen_ref']:.2f}%\n")
            f.write(f"- Waktu Qwen: {result['qwen']['time']:.2f}s | Waktu Tesseract: {result['tesseract']['time']:.2f}s\n\n")
            
            f.write("#### 🤖 Qwen VL Plus\n\n")
            if result["qwen"]["success"]:
                f.write("```\n")
                f.write(result["qwen"]["text"])
                f.write("\n```\n\n")
            else:
                f.write(f"❌ Error: {result['qwen']['error']}\n\n")
            
            f.write("#### 📝 Tesseract\n\n")
            if result["tesseract"]["success"]:
                f.write("```\n")
                f.write(result["tesseract"]["text"])
                f.write("\n```\n\n")
            else:
                f.write(f"❌ Error: {result['tesseract']['error']}\n\n")
            
            f.write("---\n\n")
    
    print("✓ Selesai! Hasil disimpan di:")
    print("  - ocr_comparison_results.txt (format text)")
    print("  - ocr_comparison_results.md (format markdown)")
    
    # Buat tabel perbandingan per gambar
    print(f"\n{'='*80}")
    print("TABEL PERBANDINGAN PER GAMBAR")
    print(f"{'='*80}\n")
    
    table_data = []
    for result in results:
        table_data.append([
            result['file'],
            f"{result['qwen']['time']:.2f}s",
            f"{result['tesseract']['time']:.2f}s",
            f"{result['similarity']:.2f}%",
            f"{result['cer_qwen_ref']:.2f}%",
            f"{result['wer_qwen_ref']:.2f}%"
        ])
    
    headers = ["File", "Qwen Time", "Tess Time", "Similarity", "CER", "WER"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Buat tabel ringkasan metrik
    print(f"\n{'='*80}")
    print("TABEL RINGKASAN METRIK")
    print(f"{'='*80}\n")
    
    summary_data = [
        ["Total Waktu", f"{total_qwen_time:.2f}s", f"{total_tesseract_time:.2f}s"],
        ["Rata-rata/Gambar", f"{total_qwen_time/len(results):.2f}s", f"{total_tesseract_time/len(results):.2f}s"],
        ["Speedup", "-", f"{total_qwen_time/total_tesseract_time:.2f}x lebih cepat"],
        ["", "", ""],
        ["Avg Similarity", f"{avg_similarity:.2f}%", f"{avg_similarity:.2f}%"],
        ["Avg CER", f"{avg_cer_tess_ref:.2f}%", f"{avg_cer_qwen_ref:.2f}%"],
        ["Avg WER", f"{avg_wer_tess_ref:.2f}%", f"{avg_wer_qwen_ref:.2f}%"],
    ]
    
    summary_headers = ["Metrik", "Qwen VL Plus", "Tesseract"]
    print(tabulate(summary_data, headers=summary_headers, tablefmt="grid"))
    
    # 
    # Tampilkan summary
    print(f"\n{'='*80}")
    print("RINGKASAN")
    print(f"{'='*80}")
    print(f"Kecepatan:")
    print(f"  Qwen VL Plus : {total_qwen_time:.2f}s total ({total_qwen_time/len(results):.2f}s/gambar)")
    print(f"  Tesseract    : {total_tesseract_time:.2f}s total ({total_tesseract_time/len(results):.2f}s/gambar)")
    print(f"\nAkurasi:")
    print(f"  Similarity       : {avg_similarity:.2f}%")
    print(f"  CER (Tess vs Q)  : {avg_cer_qwen_ref:.2f}%")
    print(f"  WER (Tess vs Q)  : {avg_wer_qwen_ref:.2f}%")
    print(f"  CER (Q vs Tess)  : {avg_cer_tess_ref:.2f}%")
    print(f"  WER (Q vs Tess)  : {avg_wer_tess_ref:.2f}%")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
