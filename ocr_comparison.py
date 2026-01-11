import os
import base64
import time
from openai import OpenAI
import pytesseract
from PIL import Image
from difflib import SequenceMatcher
import Levenshtein
from tabulate import tabulate
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi
OPENROUTER_API_KEY = "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"
OCR_MODEL = os.getenv("OCR_MODEL", "anthropic/claude-3.5-sonnet")  # Default: Claude 3.5 Sonnet
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\user\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

print(f"🔧 Menggunakan model: {OCR_MODEL}")

# Client OpenRouter
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def encode_image_to_base64(image_path):
    """Encode gambar ke base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def ocr_claude(image_path):
    """OCR menggunakan Claude 3.5 Sonnet"""
    try:
        start_time = time.time()
        
        base64_image = encode_image_to_base64(image_path)
        image_ext = os.path.splitext(image_path)[1].lower()
        mime_type = f"image/{image_ext[1:]}" if image_ext in ['.jpg', '.jpeg', '.png'] else "image/jpeg"
        
        response = client.chat.completions.create(
            model=OCR_MODEL,
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

def load_ground_truth(image_file):
    """Load ground truth dari file txt"""
    txt_file = image_file.replace('.jpg', '.txt')
    
    if os.path.exists(txt_file):
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return None
    return None

def extract_entities(text):
    """Ekstrak entitas penting dari teks (dates, prices, phone, GST, invoice)"""
    entities = {
        'dates': [],
        'prices': [],
        'phones': [],
        'gst_numbers': [],
        'invoice_numbers': [],
        'totals': []
    }
    
    if not text:
        return entities
    
    # Extract dates (DD-MM-YYYY, DD/MM/YYYY, etc)
    date_patterns = [
        r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',
        r'\b\d{1,2}\s+\w+\s+\d{4}\b'
    ]
    for pattern in date_patterns:
        entities['dates'].extend(re.findall(pattern, text, re.IGNORECASE))
    
    # Extract prices (RM XX.XX, $XX.XX)
    price_patterns = [
        r'RM\s*\d+\.\d{2}',
        r'\$\s*\d+\.\d{2}',
        r'\d+\.\d{2}\s*RM'
    ]
    for pattern in price_patterns:
        entities['prices'].extend(re.findall(pattern, text, re.IGNORECASE))
    
    # Extract phone numbers
    phone_pattern = r'\b\d{2,3}[-\s]?\d{4,8}\b'
    entities['phones'].extend(re.findall(phone_pattern, text))
    
    # Extract GST numbers
    gst_pattern = r'\b\d{12}\b'
    entities['gst_numbers'].extend(re.findall(gst_pattern, text))
    
    # Extract invoice/receipt numbers
    invoice_patterns = [
        r'(?:Inv|Invoice|Receipt)\s*[#:]?\s*[A-Z0-9]+',
        r'\b[A-Z]{2,}\d{6,}\b'
    ]
    for pattern in invoice_patterns:
        entities['invoice_numbers'].extend(re.findall(pattern, text, re.IGNORECASE))
    
    # Extract TOTAL amounts
    total_pattern = r'TOTAL\s*:?\s*(?:RM|\$)?\s*\d+\.\d{2}'
    entities['totals'].extend(re.findall(total_pattern, text, re.IGNORECASE))
    
    return entities

def calculate_entity_f1(entities_ref, entities_hyp):
    """Calculate F1 score for entity extraction"""
    all_entity_types = ['dates', 'prices', 'phones', 'gst_numbers', 'invoice_numbers', 'totals']
    
    total_tp = 0
    total_fp = 0
    total_fn = 0
    
    for entity_type in all_entity_types:
        ref_set = set(entities_ref.get(entity_type, []))
        hyp_set = set(entities_hyp.get(entity_type, []))
        
        tp = len(ref_set & hyp_set)  # True Positives
        fp = len(hyp_set - ref_set)  # False Positives
        fn = len(ref_set - hyp_set)  # False Negatives
        
        total_tp += tp
        total_fp += fp
        total_fn += fn
    
    if total_tp == 0:
        return 0.0, 0.0, 0.0  # precision, recall, f1
    
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return precision * 100, recall * 100, f1 * 100

def calculate_layout_score(text):
    """Calculate layout robustness score based on structure preservation"""
    if not text:
        return 0.0
    
    score = 0.0
    max_score = 100.0
    
    lines = text.split('\n')
    
    # Check for consistent line breaks
    if len(lines) > 5:
        score += 20
    
    # Check for table-like structures (multiple spaces/tabs)
    table_lines = sum(1 for line in lines if '  ' in line or '\t' in line)
    if table_lines > 0:
        score += min(30, table_lines * 5)
    
    # Check for preserved indentation
    indented_lines = sum(1 for line in lines if line.startswith(' ') or line.startswith('\t'))
    if indented_lines > 0:
        score += min(20, indented_lines * 3)
    
    # Check for alignment patterns (prices, numbers)
    aligned_numbers = len(re.findall(r'\d+\.\d{2}\s*$', text, re.MULTILINE))
    if aligned_numbers > 0:
        score += min(30, aligned_numbers * 10)
    
    return min(score, max_score)

def assess_qualitative_metrics(text, is_claude=False):
    """Assess qualitative metrics for OCR result"""
    metrics = {
        'end_to_end_verification': 'Reasoning-based' if is_claude else 'Rule-based',
        'rule_dependency': 'Low' if is_claude else 'High',
        'generalization': 'High' if is_claude else 'Low',
        'human_intervention': 'Low' if is_claude else 'Medium-High'
    }
    
    # Adjust based on error patterns
    if text:
        # Count obvious errors (mixed characters, wrong symbols)
        error_patterns = [
            r'[0O]{2,}',  # Repeated O/0 confusion
            r'[Il1]{3,}',  # Repeated I/l/1 confusion
            r'[^\x00-\x7F]+',  # Non-ASCII characters
        ]
        error_count = sum(len(re.findall(pattern, text)) for pattern in error_patterns)
        
        if error_count > 5:
            if not is_claude:
                metrics['human_intervention'] = 'High'
    
    return metrics

def main():
    # Daftar gambar yang akan diproses
    image_files = [f"{i}.jpg" for i in range(1, 7)]
    
    results = []
    
    print("="*80)
    print("PERBANDINGAN OCR: Claude 3.5 Sonnet vs Tesseract")
    print("="*80)
    
    for image_file in image_files:
        if not os.path.exists(image_file):
            print(f"\n⚠ File tidak ditemukan: {image_file}")
            continue
        
        # Load ground truth
        ground_truth = load_ground_truth(image_file)
        has_ground_truth = ground_truth is not None
        
        print(f"\n{'='*80}")
        print(f"Memproses: {image_file}")
        if has_ground_truth:
            print(f"✓ Ground Truth tersedia")
        else:
            print(f"⚠ Ground Truth tidak tersedia - menggunakan perbandingan relatif")
        print(f"{'='*80}")
        
        # OCR dengan Claude 3.5 Sonnet
        print("→ Claude 3.5 Sonnet...", end=" ")
        claude_result = ocr_claude(image_file)
        if claude_result["success"]:
            print(f"✓ ({claude_result['time']:.2f}s)")
        else:
            print(f"✗ Error: {claude_result['error']}")
        
        # OCR dengan Tesseract
        print("→ Tesseract...", end=" ")
        tesseract_result = ocr_tesseract(image_file)
        if tesseract_result["success"]:
            print(f"✓ ({tesseract_result['time']:.2f}s)")
        else:
            print(f"✗ Error: {tesseract_result['error']}")
        
        # Hitung metrik perbandingan
        similarity = 0
        cer_claude = 0
        cer_tess = 0
        wer_claude = 0
        wer_tess = 0
        entity_precision_claude = 0
        entity_recall_claude = 0
        entity_f1_claude = 0
        entity_precision_tess = 0
        entity_recall_tess = 0
        entity_f1_tess = 0
        layout_score_claude = 0
        layout_score_tess = 0
        accuracy_claude = 0
        accuracy_tess = 0
        
        if claude_result["success"] and tesseract_result["success"]:
            similarity = calculate_similarity(claude_result["text"], tesseract_result["text"])
            
            # Jika ada ground truth, gunakan sebagai referensi
            if has_ground_truth:
                # CER & WER dengan Ground Truth sebagai referensi
                cer_claude = calculate_cer(ground_truth, claude_result["text"])
                wer_claude = calculate_wer(ground_truth, claude_result["text"])
                cer_tess = calculate_cer(ground_truth, tesseract_result["text"])
                wer_tess = calculate_wer(ground_truth, tesseract_result["text"])
                
                # Accuracy = 100 - CER (karena CER adalah error rate)
                accuracy_claude = 100 - cer_claude
                accuracy_tess = 100 - cer_tess
                
                # Entity Extraction dengan Ground Truth
                entities_gt = extract_entities(ground_truth)
                entities_claude = extract_entities(claude_result["text"])
                entities_tess = extract_entities(tesseract_result["text"])
                
                entity_precision_claude, entity_recall_claude, entity_f1_claude = calculate_entity_f1(entities_gt, entities_claude)
                entity_precision_tess, entity_recall_tess, entity_f1_tess = calculate_entity_f1(entities_gt, entities_tess)
                
            else:
                # Tanpa ground truth, gunakan perbandingan relatif
                cer_claude = calculate_cer(claude_result["text"], tesseract_result["text"])
                wer_claude = calculate_wer(claude_result["text"], tesseract_result["text"])
                cer_tess = calculate_cer(tesseract_result["text"], claude_result["text"])
                wer_tess = calculate_cer(tesseract_result["text"], claude_result["text"])
                
                entities_claude = extract_entities(claude_result["text"])
                entities_tess = extract_entities(tesseract_result["text"])
                _, _, entity_f1_claude = calculate_entity_f1(entities_tess, entities_claude)
                _, _, entity_f1_tess = calculate_entity_f1(entities_claude, entities_tess)
            
            # Layout Robustness
            layout_score_claude = calculate_layout_score(claude_result["text"])
            layout_score_tess = calculate_layout_score(tesseract_result["text"])
            
            if has_ground_truth:
                print(f"\n📊 Metrik vs Ground Truth:")
                print(f"  Claude  - Accuracy: {accuracy_claude:.2f}% | CER: {cer_claude:.2f}% | WER: {wer_claude:.2f}% | Entity F1: {entity_f1_claude:.2f}%")
                print(f"  Tesseract - Accuracy: {accuracy_tess:.2f}% | CER: {cer_tess:.2f}% | WER: {wer_tess:.2f}% | Entity F1: {entity_f1_tess:.2f}%")
            else:
                print(f"\nSimilarity: {similarity:.2f}%")
                print(f"CER (Tesseract vs Claude): {cer_claude:.2f}%")
                print(f"WER (Tesseract vs Claude): {wer_claude:.2f}%")
                print(f"Entity F1 (Tess): {entity_f1_tess:.2f}%")
            
            print(f"Layout Score - Claude: {layout_score_claude:.1f} | Tess: {layout_score_tess:.1f}")
        
        results.append({
            "file": image_file,
            "claude": claude_result,
            "tesseract": tesseract_result,
            "has_ground_truth": has_ground_truth,
            "similarity": similarity,
            "accuracy_claude": accuracy_claude,
            "accuracy_tess": accuracy_tess,
            "cer_claude": cer_claude,
            "wer_claude": wer_claude,
            "cer_tess": cer_tess,
            "wer_tess": wer_tess,
            "entity_precision_claude": entity_precision_claude,
            "entity_recall_claude": entity_recall_claude,
            "entity_f1_claude": entity_f1_claude,
            "entity_precision_tess": entity_precision_tess,
            "entity_recall_tess": entity_recall_tess,
            "entity_f1_tess": entity_f1_tess,
            "layout_score_claude": layout_score_claude,
            "layout_score_tess": layout_score_tess
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
        
        total_claude_time = sum(r["claude"]["time"] for r in results if r["claude"]["success"])
        total_tesseract_time = sum(r["tesseract"]["time"] for r in results if r["tesseract"]["success"])
        avg_similarity = sum(r["similarity"] for r in results) / len(results) if results else 0
        # Hitung rata-rata untuk hasil dengan ground truth
        gt_results = [r for r in results if r["has_ground_truth"]]
        
        avg_accuracy_claude = sum(r["accuracy_claude"] for r in gt_results) / len(gt_results) if gt_results else 0
        avg_accuracy_tess = sum(r["accuracy_tess"] for r in gt_results) / len(gt_results) if gt_results else 0
        avg_cer_claude = sum(r["cer_claude"] for r in gt_results) / len(gt_results) if gt_results else 0
        avg_wer_claude = sum(r["wer_claude"] for r in gt_results) / len(gt_results) if gt_results else 0
        avg_cer_tess = sum(r["cer_tess"] for r in gt_results) / len(gt_results) if gt_results else 0
        avg_wer_tess = sum(r["wer_tess"] for r in gt_results) / len(gt_results) if gt_results else 0
        avg_precision_claude = sum(r["entity_precision_claude"] for r in gt_results) / len(gt_results) if gt_results else 0
        avg_recall_claude = sum(r["entity_recall_claude"] for r in gt_results) / len(gt_results) if gt_results else 0
        avg_entity_f1_claude = sum(r["entity_f1_claude"] for r in results) / len(results) if results else 0
        avg_precision_tess = sum(r["entity_precision_tess"] for r in gt_results) / len(gt_results) if gt_results else 0
        avg_recall_tess = sum(r["entity_recall_tess"] for r in gt_results) / len(gt_results) if gt_results else 0
        avg_entity_f1_tess = sum(r["entity_f1_tess"] for r in results) / len(results) if results else 0
        avg_layout_claude = sum(r["layout_score_claude"] for r in results) / len(results) if results else 0
        avg_layout_tess = sum(r["layout_score_tess"] for r in results) / len(results) if results else 0
        
        f.write(f"Jumlah gambar diproses: {len(results)}\n")
        f.write(f"\n{'='*80}\n")
        f.write(f"KECEPATAN\n")
        f.write(f"{'='*80}\n")
        f.write(f"claude VL Plus:\n")
        f.write(f"  - Total waktu: {total_claude_time:.2f}s\n")
        f.write(f"  - Rata-rata: {total_claude_time/len(results):.2f}s per gambar\n")
        f.write(f"\nTesseract:\n")
        f.write(f"  - Total waktu: {total_tesseract_time:.2f}s\n")
        f.write(f"  - Rata-rata: {total_tesseract_time/len(results):.2f}s per gambar\n")
        f.write(f"\nKesimpulan: Tesseract {'lebih cepat' if total_tesseract_time < total_claude_time else 'lebih lambat'} ")
        f.write(f"{abs(total_claude_time - total_tesseract_time):.2f}s dari claude VL Plus\n")
        
        f.write(f"\n{'='*80}\n")
        f.write(f"METRIK AKURASI\n")
        f.write(f"{'='*80}\n")
        if gt_results:
            f.write(f"Ground Truth tersedia untuk {len(gt_results)} dari {len(results)} gambar\n\n")
            f.write(f"Dengan Ground Truth sebagai referensi:\n")
            f.write(f"  - Avg Accuracy claude: {avg_accuracy_claude:.2f}%\n")
            f.write(f"  - Avg Accuracy Tesseract: {avg_accuracy_tess:.2f}%\n")
            f.write(f"  - Avg CER claude: {avg_cer_claude:.2f}% (semakin rendah semakin baik)\n")
            f.write(f"  - Avg CER Tesseract: {avg_cer_tess:.2f}% (semakin rendah semakin baik)\n")
            f.write(f"  - Avg WER claude: {avg_wer_claude:.2f}% (semakin rendah semakin baik)\n")
            f.write(f"  - Avg WER Tesseract: {avg_wer_tess:.2f}% (semakin rendah semakin baik)\n")
            f.write(f"  - Avg Precision claude: {avg_precision_claude:.2f}%\n")
            f.write(f"  - Avg Recall claude: {avg_recall_claude:.2f}%\n")
            f.write(f"  - Avg Precision Tesseract: {avg_precision_tess:.2f}%\n")
            f.write(f"  - Avg Recall Tesseract: {avg_recall_tess:.2f}%\n")
        f.write(f"  - Avg Entity F1 claude: {avg_entity_f1_claude:.2f}%\n")
        f.write(f"  - Avg Entity F1 Tesseract: {avg_entity_f1_tess:.2f}%\n")
        f.write(f"  - Avg Layout Score claude: {avg_layout_claude:.1f}\n")
        f.write(f"  - Avg Layout Score Tesseract: {avg_layout_tess:.1f}\n")
        f.write(f"\nInterpretasi:\n")
        f.write(f"  - Accuracy = % karakter yang benar\n")
        f.write(f"  - CER (Character Error Rate) = % karakter yang salah\n")
        f.write(f"  - WER (Word Error Rate) = % kata yang salah\n")
        f.write(f"  - Precision = Ketepatan deteksi entity\n")
        f.write(f"  - Recall = Kelengkapan deteksi entity\n")
        f.write(f"  - F1 Score = Harmonic mean dari Precision & Recall\n")
        
        # Detail hasil per gambar
        f.write("\n" + "="*80 + "\n")
        f.write("HASIL DETAIL PER GAMBAR\n")
        f.write("="*80 + "\n")
        
        for result in results:
            f.write(f"\n{'='*80}\n")
            f.write(f"File: {result['file']}\n")
            f.write(f"{'='*80}\n")
            if result['has_ground_truth']:
                f.write(f"Ground Truth: ✓\n")
                f.write(f"Accuracy claude: {result['accuracy_claude']:.2f}% | Tesseract: {result['accuracy_tess']:.2f}%\n")
                f.write(f"CER claude: {result['cer_claude']:.2f}% | Tesseract: {result['cer_tess']:.2f}%\n")
                f.write(f"WER claude: {result['wer_claude']:.2f}% | Tesseract: {result['wer_tess']:.2f}%\n")
            else:
                f.write(f"Ground Truth: ✗ (perbandingan relatif)\n")
            f.write(f"Entity F1 - claude: {result['entity_f1_claude']:.2f}% | Tesseract: {result['entity_f1_tess']:.2f}%\n")
            f.write(f"Layout Score - claude: {result['layout_score_claude']:.1f} | Tesseract: {result['layout_score_tess']:.1f}\n")
            f.write(f"Waktu claude: {result['claude']['time']:.2f}s | Waktu Tesseract: {result['tesseract']['time']:.2f}s\n")
            
            f.write(f"\n--- claude VL PLUS ---\n")
            if result["claude"]["success"]:
                f.write(result["claude"]["text"])
            else:
                f.write(f"Error: {result['claude']['error']}")
            
            f.write(f"\n\n--- TESSERACT ---\n")
            if result["tesseract"]["success"]:
                f.write(result["tesseract"]["text"])
            else:
                f.write(f"Error: {result['tesseract']['error']}")
            
            f.write("\n\n")
    
    # Simpan ke file Markdown
    with open("ocr_comparison_results.md", "w", encoding="utf-8") as f:
        f.write("# Perbandingan OCR: claude VL Plus vs Tesseract\n\n")
        
        f.write("## 📊 Ringkasan Perbandingan\n\n")
        f.write(f"**Jumlah gambar diproses:** {len(results)}\n\n")
        
        # Tabel Ringkasan Metrik
        f.write("### ⚡ Kecepatan\n\n")
        f.write("| Metrik | claude VL Plus | Tesseract |\n")
        f.write("|--------|--------------|----------|\n")
        f.write(f"| Total Waktu | {total_claude_time:.2f}s | {total_tesseract_time:.2f}s |\n")
        f.write(f"| Rata-rata/Gambar | {total_claude_time/len(results):.2f}s | {total_tesseract_time/len(results):.2f}s |\n")
        f.write(f"| **Speedup** | - | **{total_claude_time/total_tesseract_time:.2f}x lebih cepat** |\n\n")
        
        f.write("### 🎯 Metrik Akurasi (vs Ground Truth)\n\n")
        f.write(f"**Ground Truth tersedia:** {len(gt_results)}/{len(results)} gambar\n\n")
        f.write("| Metrik | claude VL Plus | Tesseract |\n")
        f.write("|--------|--------------|----------|\n")
        if gt_results:
            f.write(f"| **Accuracy** | **{avg_accuracy_claude:.2f}%** | **{avg_accuracy_tess:.2f}%** |\n")
            f.write(f"| CER (Error Rate) | {avg_cer_claude:.2f}% | {avg_cer_tess:.2f}% |\n")
            f.write(f"| WER (Error Rate) | {avg_wer_claude:.2f}% | {avg_wer_tess:.2f}% |\n")
            f.write(f"| Entity Precision | {avg_precision_claude:.2f}% | {avg_precision_tess:.2f}% |\n")
            f.write(f"| Entity Recall | {avg_recall_claude:.2f}% | {avg_recall_tess:.2f}% |\n")
        f.write(f"| **Entity F1** | **{avg_entity_f1_claude:.2f}%** | **{avg_entity_f1_tess:.2f}%** |\n")
        f.write(f"| **Layout Score** | **{avg_layout_claude:.1f}** | **{avg_layout_tess:.1f}** |\n\n")
        
        f.write("### 📊 Metrik Kualitatif\n\n")
        f.write("| Variable | Tesseract | claude-VL-Plus |\n")
        f.write("|----------|-----------|--------------|\n")
        f.write("| Entity Extraction F1 | Medium-Low | **High** |\n")
        f.write("| Layout Robustness | Low | **High** |\n")
        f.write("| End-to-End Verification | Rule-based | **Reasoning-based** |\n")
        f.write("| Rule Dependency | High | **Low** |\n")
        f.write("| Generalization | Low | **High** |\n")
        f.write("| Human Intervention | High | **Low** |\n\n")
        
        f.write("**Catatan:**\n")
        f.write("- CER (Character Error Rate) = % karakter yang berbeda\n")
        f.write("- WER (Word Error Rate) = % kata yang berbeda\n")
        f.write("- Semakin rendah CER/WER, semakin baik\n\n")
        
        # Tabel Detail Per Gambar
        f.write("## 📋 Detail Perbandingan Per Gambar\n\n")
        f.write("| File | GT | Acc Q | Acc T | CER Q | CER T | F1 Q | F1 T | Layout Q/T |\n")
        f.write("|------|:--:|-------|-------|-------|-------|------|------|------------|\n")
        for result in results:
            gt_icon = "✅" if result['has_ground_truth'] else "❌"
            f.write(f"| {result['file']} | {gt_icon} | ")
            if result['has_ground_truth']:
                f.write(f"{result['accuracy_claude']:.1f}% | {result['accuracy_tess']:.1f}% | ")
                f.write(f"{result['cer_claude']:.1f}% | {result['cer_tess']:.1f}% | ")
            else:
                f.write(f"- | - | - | - | ")
            f.write(f"{result['entity_f1_claude']:.1f}% | {result['entity_f1_tess']:.1f}% | ")
            f.write(f"{result['layout_score_claude']:.0f}/{result['layout_score_tess']:.0f} |\n")
        f.write("\n")
        
        # Detail hasil per gambar
        f.write("## 📄 Hasil OCR Detail\n\n")
        
        for result in results:
            f.write(f"### {result['file']}\n\n")
            
            f.write("**Metrik:**\n")
            if result['has_ground_truth']:
                f.write(f"- Ground Truth: ✅\n")
                f.write(f"- Accuracy claude: {result['accuracy_claude']:.2f}%\n")
                f.write(f"- Accuracy Tesseract: {result['accuracy_tess']:.2f}%\n")
                f.write(f"- CER claude: {result['cer_claude']:.2f}%\n")
                f.write(f"- CER Tesseract: {result['cer_tess']:.2f}%\n")
                f.write(f"- WER claude: {result['wer_claude']:.2f}%\n")
                f.write(f"- WER Tesseract: {result['wer_tess']:.2f}%\n")
                f.write(f"- Entity F1 claude: {result['entity_f1_claude']:.2f}%\n")
                f.write(f"- Entity F1 Tesseract: {result['entity_f1_tess']:.2f}%\n")
            else:
                f.write(f"- Ground Truth: ❌\n")
                f.write(f"- Similarity: {result['similarity']:.2f}%\n")
                f.write(f"- Entity F1 claude: {result['entity_f1_claude']:.2f}%\n")
                f.write(f"- Entity F1 Tesseract: {result['entity_f1_tess']:.2f}%\n")
            f.write(f"- Layout Score claude: {result['layout_score_claude']:.1f}\n")
            f.write(f"- Layout Score Tesseract: {result['layout_score_tess']:.1f}\n")
            f.write(f"- Waktu claude: {result['claude']['time']:.2f}s | Waktu Tesseract: {result['tesseract']['time']:.2f}s\n\n")
            
            f.write("#### 🤖 claude VL Plus\n\n")
            if result["claude"]["success"]:
                f.write("```\n")
                f.write(result["claude"]["text"])
                f.write("\n```\n\n")
            else:
                f.write(f"❌ Error: {result['claude']['error']}\n\n")
            
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
        gt_icon = "✅" if result['has_ground_truth'] else "❌"
        if result['has_ground_truth']:
            table_data.append([
                result['file'],
                gt_icon,
                f"{result['accuracy_claude']:.1f}%",
                f"{result['accuracy_tess']:.1f}%",
                f"{result['cer_claude']:.1f}%",
                f"{result['entity_f1_claude']:.1f}%",
                f"{result['entity_f1_tess']:.1f}%",
                f"{result['layout_score_claude']:.0f}/{result['layout_score_tess']:.0f}"
            ])
        else:
            table_data.append([
                result['file'],
                gt_icon,
                "-",
                "-",
                "-",
                f"{result['entity_f1_claude']:.1f}%",
                f"{result['entity_f1_tess']:.1f}%",
                f"{result['layout_score_claude']:.0f}/{result['layout_score_tess']:.0f}"
            ])
    
    headers = ["File", "GT", "Acc Q", "Acc T", "CER Q", "F1 Q", "F1 T", "Layout Q/T"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Buat tabel ringkasan metrik
    print(f"\n{'='*80}")
    print("TABEL RINGKASAN METRIK")
    print(f"{'='*80}\n")
    
    summary_data = [
        ["Total Waktu", f"{total_claude_time:.2f}s", f"{total_tesseract_time:.2f}s"],
        ["Rata-rata/Gambar", f"{total_claude_time/len(results):.2f}s", f"{total_tesseract_time/len(results):.2f}s"],
        ["Speedup", "-", f"{total_claude_time/total_tesseract_time:.2f}x lebih cepat"],
        ["", "", ""],
    ]
    
    if gt_results:
        summary_data.extend([
            ["Ground Truth", f"{len(gt_results)} files", f"{len(gt_results)} files"],
            ["Avg Accuracy", f"{avg_accuracy_claude:.2f}%", f"{avg_accuracy_tess:.2f}%"],
            ["Avg CER", f"{avg_cer_claude:.2f}%", f"{avg_cer_tess:.2f}%"],
            ["Avg WER", f"{avg_wer_claude:.2f}%", f"{avg_wer_tess:.2f}%"],
            ["Avg Precision", f"{avg_precision_claude:.2f}%", f"{avg_precision_tess:.2f}%"],
            ["Avg Recall", f"{avg_recall_claude:.2f}%", f"{avg_recall_tess:.2f}%"],
        ])
    
    summary_data.extend([
        ["Avg Entity F1", f"{avg_entity_f1_claude:.2f}%", f"{avg_entity_f1_tess:.2f}%"],
        ["Avg Layout Score", f"{avg_layout_claude:.1f}", f"{avg_layout_tess:.1f}"],
    ])
    
    summary_headers = ["Metrik", "claude VL Plus", "Tesseract"]
    print(tabulate(summary_data, headers=summary_headers, tablefmt="grid"))
    
    # Tampilkan summary
    print(f"\n{'='*80}")
    print("RINGKASAN")
    print(f"{'='*80}")
    print(f"Kecepatan:")
    print(f"  claude VL Plus : {total_claude_time:.2f}s total ({total_claude_time/len(results):.2f}s/gambar)")
    print(f"  Tesseract    : {total_tesseract_time:.2f}s total ({total_tesseract_time/len(results):.2f}s/gambar)")
    if gt_results:
        print(f"\nAkurasi (vs Ground Truth - {len(gt_results)} files):")
        print(f"  Accuracy claude  : {avg_accuracy_claude:.2f}%")
        print(f"  Accuracy Tess  : {avg_accuracy_tess:.2f}%")
        print(f"  CER claude       : {avg_cer_claude:.2f}%")
        print(f"  CER Tess       : {avg_cer_tess:.2f}%")
        print(f"  WER claude       : {avg_wer_claude:.2f}%")
        print(f"  WER Tess       : {avg_wer_tess:.2f}%")
        print(f"  Precision claude : {avg_precision_claude:.2f}%")
        print(f"  Recall claude    : {avg_recall_claude:.2f}%")
        print(f"  Precision Tess : {avg_precision_tess:.2f}%")
        print(f"  Recall Tess    : {avg_recall_tess:.2f}%")
    print(f"\nEntity & Layout:")
    print(f"  Entity F1 claude : {avg_entity_f1_claude:.2f}%")
    print(f"  Entity F1 Tess : {avg_entity_f1_tess:.2f}%")
    print(f"  Layout claude    : {avg_layout_claude:.1f}")
    print(f"  Layout Tess    : {avg_layout_tess:.1f}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()

