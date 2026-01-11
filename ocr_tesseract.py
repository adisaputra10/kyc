import os
import pytesseract
from PIL import Image

# Konfigurasi path Tesseract (sesuaikan jika berbeda)
# Untuk Windows, biasanya di: C:\Program Files\Tesseract-OCR\tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\user\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def ocr_image_tesseract(image_path):
    """Melakukan OCR pada gambar menggunakan Tesseract"""
    print(f"\nMemproses: {image_path}")
    
    try:
        # Baca gambar
        image = Image.open(image_path)
        
        # Lakukan OCR
        ocr_text = pytesseract.image_to_string(image)
        
        print(f"✓ Berhasil")
        print(f"Hasil OCR:\n{ocr_text}\n")
        print("-" * 80)
        
        return ocr_text
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

def main():
    # Daftar gambar yang akan diproses
    image_files = [f"{i}.jpg" for i in range(1, 7)]
    
    results = {}
    
    print("="*80)
    print("OCR dengan Tesseract")
    print("="*80)
    
    for image_file in image_files:
        if os.path.exists(image_file):
            ocr_result = ocr_image_tesseract(image_file)
            results[image_file] = ocr_result
        else:
            print(f"\n⚠ File tidak ditemukan: {image_file}")
    
    # Simpan hasil ke file
    print("\nMenyimpan hasil ke ocr_results_tesseract.txt...")
    with open("ocr_results_tesseract.txt", "w", encoding="utf-8") as f:
        for image_file, result in results.items():
            f.write(f"{'='*80}\n")
            f.write(f"File: {image_file}\n")
            f.write(f"{'='*80}\n")
            if result:
                f.write(f"{result}\n\n")
            else:
                f.write("Error dalam pemrosesan\n\n")
    
    print("✓ Selesai! Hasil disimpan di ocr_results_tesseract.txt")

if __name__ == "__main__":
    main()
