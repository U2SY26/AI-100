#!/usr/bin/env python3
"""
PDF 1 이미지 OCR로 숨겨진 텍스트 찾기
"""

import fitz
from PIL import Image, ImageEnhance
import pytesseract
import io

def extract_hidden_text_from_images(pdf_path):
    """이미지 PDF에서 OCR로 숨겨진 텍스트 추출"""
    doc = fitz.open(pdf_path)
    all_text = []

    print(f"총 {len(doc)}페이지 분석 중...")

    for page_num in range(len(doc)):
        page = doc[page_num]

        # 이미지 추출
        images = page.get_images()

        for img_index, img_info in enumerate(images):
            xref = img_info[0]

            # 이미지 데이터 추출
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # PIL 이미지로 변환
            image = Image.open(io.BytesIO(image_bytes))

            # 여러 전처리 방법 시도
            print(f"\nPage {page_num + 1}, Image {img_index + 1}")

            # 1. 원본 OCR
            text1 = pytesseract.image_to_string(image, lang='eng')
            if text1.strip():
                print(f"  원본 OCR: {len(text1)} chars")

            # 2. 대비 증가 (5x)
            enhancer = ImageEnhance.Contrast(image)
            enhanced = enhancer.enhance(5.0)
            text2 = pytesseract.image_to_string(enhanced, lang='eng')
            if text2.strip():
                print(f"  대비5x OCR: {len(text2)} chars")

            # 3. 반전 (흰색 텍스트 → 검은색)
            inverted = Image.eval(image, lambda x: 255 - x)
            text3 = pytesseract.image_to_string(inverted, lang='eng')
            if text3.strip():
                print(f"  반전 OCR: {len(text3)} chars")

            # 4. 그레이스케일 + 대비
            gray = image.convert('L')
            gray_enhanced = ImageEnhance.Contrast(gray).enhance(5.0)
            text4 = pytesseract.image_to_string(gray_enhanced, lang='eng')
            if text4.strip():
                print(f"  그레이+대비 OCR: {len(text4)} chars")

            # 가장 짧은 텍스트 선택 (숨겨진 텍스트만)
            texts = [t.strip() for t in [text1, text2, text3, text4] if t.strip()]
            if texts:
                # 가장 많이 변화가 있는 것 선택
                unique_text = max(texts, key=lambda x: len(x))
                all_text.append({
                    "page": page_num + 1,
                    "text": unique_text
                })

    doc.close()
    return all_text

def main():
    pdf_path = "pdf_1.pdf"

    print(f"\n{'='*60}")
    print(f"PDF 1 OCR 분석")
    print(f"{'='*60}")

    results = extract_hidden_text_from_images(pdf_path)

    print(f"\n{'='*60}")
    print(f"발견된 텍스트:")
    print(f"{'='*60}")

    for item in results:
        print(f"\nPage {item['page']}:")
        print(item['text'][:500])  # 처음 500자

if __name__ == "__main__":
    # Tesseract 경로 설정 (Windows)
    try:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    except:
        pass

    main()
