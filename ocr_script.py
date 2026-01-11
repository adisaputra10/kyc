import os
import base64
from openai import OpenAI

# Konfigurasi OpenRouter
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def encode_image_to_base64(image_path):
    """Encode gambar ke base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def ocr_image(image_path):
    """Melakukan OCR pada gambar menggunakan Qwen VL Plus"""
    print(f"\nMemproses: {image_path}")
    
    # Encode gambar
    base64_image = encode_image_to_base64(image_path)
    
    # Tentukan format gambar
    image_ext = os.path.splitext(image_path)[1].lower()
    mime_type = f"image/{image_ext[1:]}" if image_ext in ['.jpg', '.jpeg', '.png'] else "image/jpeg"
    
    try:
        # Panggil API dengan vision capability
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
        
        # Ekstrak hasil OCR
        ocr_text = response.choices[0].message.content
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
    print("OCR dengan Qwen VL Plus via OpenRouter")
    print("="*80)
    
    for image_file in image_files:
        if os.path.exists(image_file):
            ocr_result = ocr_image(image_file)
            results[image_file] = ocr_result
        else:
            print(f"\n⚠ File tidak ditemukan: {image_file}")
    
    # Simpan hasil ke file
    print("\nMenyimpan hasil ke ocr_results.txt...")
    with open("ocr_results.txt", "w", encoding="utf-8") as f:
        for image_file, result in results.items():
            f.write(f"{'='*80}\n")
            f.write(f"File: {image_file}\n")
            f.write(f"{'='*80}\n")
            if result:
                f.write(f"{result}\n\n")
            else:
                f.write("Error dalam pemrosesan\n\n")
    
    print("✓ Selesai! Hasil disimpan di ocr_results.txt")

if __name__ == "__main__":
    main()
