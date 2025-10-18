#!/usr/bin/env python3
"""
PDF 숨겨진 텍스트 추출기
AI_TOP_100 Textfinder Challenge

숨겨진 텍스트 유형:
1. 이미지에 배경색과 비슷한 색상의 텍스트
2. 흰색 또는 극소 폰트 크기의 텍스트
3. 보이지 않는 레이어의 텍스트
"""

import fitz  # PyMuPDF
import re
from pathlib import Path

def extract_all_text_with_properties(pdf_path):
    """PDF에서 모든 텍스트와 속성 추출"""
    doc = fitz.open(pdf_path)
    results = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        # 텍스트와 속성 추출
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text:
                            results.append({
                                "page": page_num + 1,
                                "text": text,
                                "size": span["size"],
                                "color": span["color"],
                                "font": span["font"],
                                "bbox": span["bbox"]
                            })

    doc.close()
    return results

def find_hidden_text_pdf1(pdf_path):
    """
    PDF 1: 이미지 기반 PDF에 배경과 비슷한 색상으로 숨겨진 텍스트
    14단어
    """
    print(f"\n{'='*60}")
    print(f"PDF 1: {pdf_path.name}")
    print(f"{'='*60}")

    doc = fitz.open(pdf_path)
    hidden_texts = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        # 모든 텍스트 추출
        text_instances = page.get_text("dict")["blocks"]

        for block in text_instances:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        color = span["color"]
                        size = span["size"]

                        # 색상이 밝거나 회색인 경우 (배경과 비슷)
                        # RGB 값이 높으면 밝은 색 (흰색에 가까움)
                        if text:
                            # 16진수 색상을 RGB로 변환
                            r = (color >> 16) & 0xFF
                            g = (color >> 8) & 0xFF
                            b = color & 0xFF

                            # 밝은 색상 체크 (RGB > 200)
                            if r > 200 and g > 200 and b > 200:
                                hidden_texts.append({
                                    "page": page_num + 1,
                                    "text": text,
                                    "color_hex": f"#{color:06x}",
                                    "rgb": (r, g, b),
                                    "size": size
                                })

    doc.close()

    # 결과 출력
    if hidden_texts:
        print(f"\n발견된 숨겨진 텍스트 ({len(hidden_texts)}개):")
        full_text = []
        for item in hidden_texts:
            print(f"  Page {item['page']}: '{item['text']}' (Color: {item['color_hex']}, RGB: {item['rgb']}, Size: {item['size']:.1f})")
            full_text.append(item['text'])

        # 14단어 문장 조합
        combined = ' '.join(full_text)
        print(f"\n조합된 텍스트: {combined}")
        print(f"단어 수: {len(combined.split())}")
        return combined
    else:
        print("숨겨진 텍스트를 찾지 못했습니다.")
        return None

def find_hidden_text_pdf2(pdf_path):
    """
    PDF 2: 흰색의 작은 텍스트
    11단어
    """
    print(f"\n{'='*60}")
    print(f"PDF 2: {pdf_path.name}")
    print(f"{'='*60}")

    doc = fitz.open(pdf_path)
    hidden_texts = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        text_instances = page.get_text("dict")["blocks"]

        for block in text_instances:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        color = span["color"]
                        size = span["size"]

                        if text:
                            # 흰색 (0xFFFFFF) 또는 매우 작은 폰트
                            if color == 0xFFFFFF or size < 2:
                                hidden_texts.append({
                                    "page": page_num + 1,
                                    "text": text,
                                    "color_hex": f"#{color:06x}",
                                    "size": size
                                })

    doc.close()

    if hidden_texts:
        print(f"\n발견된 숨겨진 텍스트 ({len(hidden_texts)}개):")
        full_text = []
        for item in hidden_texts:
            print(f"  Page {item['page']}: '{item['text']}' (Color: {item['color_hex']}, Size: {item['size']:.1f})")
            full_text.append(item['text'])

        combined = ' '.join(full_text)
        print(f"\n조합된 텍스트: {combined}")
        print(f"단어 수: {len(combined.split())}")
        return combined
    else:
        print("숨겨진 텍스트를 찾지 못했습니다.")
        return None

def find_hidden_text_pdf3(pdf_path):
    """
    PDF 3: 보이는 레이어 아래에 보이지 않는 텍스트
    5단어
    """
    print(f"\n{'='*60}")
    print(f"PDF 3: {pdf_path.name}")
    print(f"{'='*60}")

    doc = fitz.open(pdf_path)
    all_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        # 모든 텍스트 추출 (레이어 무시)
        text = page.get_text()
        all_text.append(text)

        print(f"\nPage {page_num + 1} 텍스트:")
        print(text[:500])  # 처음 500자만

    doc.close()

    # 전체 텍스트에서 5단어 패턴 찾기
    combined = '\n'.join(all_text)
    return combined

def find_hidden_text_pdf4(pdf_path):
    """
    PDF 4: 5개의 문장이 다양한 방식으로 숨겨짐
    노래 가사
    """
    print(f"\n{'='*60}")
    print(f"PDF 4: {pdf_path.name}")
    print(f"{'='*60}")

    doc = fitz.open(pdf_path)
    hidden_texts_by_page = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_hidden = []

        text_instances = page.get_text("dict")["blocks"]

        for block in text_instances:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        color = span["color"]
                        size = span["size"]

                        if text:
                            # 여러 조건으로 숨겨진 텍스트 찾기
                            # 1. 흰색
                            # 2. 매우 작은 폰트
                            # 3. 밝은 색상
                            r = (color >> 16) & 0xFF
                            g = (color >> 8) & 0xFF
                            b = color & 0xFF

                            is_hidden = (
                                color == 0xFFFFFF or  # 흰색
                                size < 3 or           # 매우 작은 폰트
                                (r > 200 and g > 200 and b > 200)  # 밝은 색
                            )

                            if is_hidden:
                                page_hidden.append({
                                    "text": text,
                                    "color_hex": f"#{color:06x}",
                                    "size": size
                                })

        if page_hidden:
            hidden_texts_by_page[page_num + 1] = page_hidden

    doc.close()

    # 페이지별 결과
    sentences = []
    for page_num in sorted(hidden_texts_by_page.keys()):
        items = hidden_texts_by_page[page_num]
        print(f"\nPage {page_num} 숨겨진 텍스트:")
        page_text = []
        for item in items:
            print(f"  '{item['text']}' (Color: {item['color_hex']}, Size: {item['size']:.1f})")
            page_text.append(item['text'])

        sentence = ' '.join(page_text)
        sentences.append(sentence)
        print(f"  → 문장: {sentence}")

    # 콤마로 구분
    result = ', '.join(sentences)
    print(f"\n최종 답안: {result}")
    return result

def main():
    base_dir = Path(".")

    print("="*60)
    print("PDF 숨겨진 텍스트 추출기")
    print("AI_TOP_100 Textfinder Challenge")
    print("="*60)

    # PDF 1
    pdf1 = base_dir / "pdf_1.pdf"
    if pdf1.exists():
        answer1 = find_hidden_text_pdf1(pdf1)

    # PDF 2
    pdf2 = base_dir / "pdf_2.pdf"
    if pdf2.exists():
        answer2 = find_hidden_text_pdf2(pdf2)

    # PDF 3
    pdf3 = base_dir / "pdf_3.pdf"
    if pdf3.exists():
        answer3 = find_hidden_text_pdf3(pdf3)

    # PDF 4
    pdf4 = base_dir / "pdf_4.pdf"
    if pdf4.exists():
        answer4 = find_hidden_text_pdf4(pdf4)

    print("\n" + "="*60)
    print("최종 답안 요약")
    print("="*60)
    print(f"문제 1: {answer1 if 'answer1' in locals() else 'N/A'}")
    print(f"문제 2: {answer2 if 'answer2' in locals() else 'N/A'}")
    print(f"문제 3: {answer3[:100] if 'answer3' in locals() else 'N/A'}...")
    print(f"문제 4: {answer4 if 'answer4' in locals() else 'N/A'}")

if __name__ == "__main__":
    main()
