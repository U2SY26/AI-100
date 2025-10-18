#!/usr/bin/env python3
"""
AI_TOP_100 Textfinder Challenge - Solution
PDF 숨겨진 텍스트 찾기
"""

import fitz
from pathlib import Path

def solve_pdf1():
    """
    PDF 1: 이미지 기반 PDF (14단어)
    이미지에 배경색과 비슷한 색상의 텍스트

    ⚠️ OCR 필요 - Tesseract 미설치로 수동 확인 필요
    """
    print(f"\n{'='*60}")
    print("PDF 1: 이미지 기반 PDF")
    print(f"{'='*60}")
    print("이 PDF는 스캔 이미지로 OCR이 필요합니다.")
    print("향상된 이미지를 수동으로 확인하세요:")
    print("  - pdf_1_page1_enhanced.png")
    print("  - pdf_1_page2_enhanced.png")
    print("  - pdf_1_page3_enhanced.png")
    print("  - pdf_1_page4_enhanced.png")
    print("  - pdf_1_page5_enhanced.png")
    print("\n예상: 14단어의 숨겨진 텍스트")
    return "수동 확인 필요"

def solve_pdf2():
    """
    PDF 2: 흰색의 작은 텍스트 (11단어)
    """
    print(f"\n{'='*60}")
    print("PDF 2: 흰색/작은 텍스트")
    print(f"{'='*60}")

    pdf_path = "pdf_2.pdf"
    doc = fitz.open(pdf_path)
    hidden_texts = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        color = span["color"]
                        size = span["size"]

                        if text:
                            r = (color >> 16) & 0xFF
                            g = (color >> 8) & 0xFF
                            b = color & 0xFF

                            # 매우 밝은 색상 또는 흰색
                            if (r > 230 and g > 230 and b > 230) or color == 0xFFFFFF:
                                hidden_texts.append({
                                    "page": page_num + 1,
                                    "text": text
                                })

    doc.close()

    if hidden_texts:
        answer = ' '.join([item['text'] for item in hidden_texts])
        word_count = len(answer.split())

        print(f"발견: Page {hidden_texts[0]['page']}")
        print(f"텍스트: {answer}")
        print(f"단어 수: {word_count}")

        return answer
    else:
        return "찾지 못함"

def solve_pdf3():
    """
    PDF 3: 보이지 않는 레이어 텍스트 (5단어)
    """
    print(f"\n{'='*60}")
    print("PDF 3: 레이어 숨김 텍스트")
    print(f"{'='*60}")

    pdf_path = "pdf_3.pdf"
    doc = fitz.open(pdf_path)

    # 모든 텍스트 추출 (레이어 무시)
    all_text = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        all_text.append(text)

    doc.close()

    full_text = '\n'.join(all_text)

    # 5단어 패턴 찾기 (간단히 전체 텍스트에서 확인)
    print(f"전체 텍스트 길이: {len(full_text)} chars")
    print(f"샘플: {full_text[:200]}")

    # TODO: 5단어 패턴 식별 필요
    return "전체 텍스트 확인 필요"

def solve_pdf4():
    """
    PDF 4: 5개의 노래 가사 문장
    다양한 방식으로 숨겨짐
    """
    print(f"\n{'='*60}")
    print("PDF 4: 노래 가사 (5개 문장)")
    print(f"{'='*60}")

    pdf_path = "pdf_4.pdf"
    doc = fitz.open(pdf_path)
    hidden_texts = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        color = span["color"]
                        size = span["size"]

                        if text:
                            r = (color >> 16) & 0xFF
                            g = (color >> 8) & 0xFF
                            b = color & 0xFF

                            # 밝은 색상, 흰색, 또는 작은 폰트
                            is_hidden = (
                                (r > 200 and g > 200 and b > 200) or
                                color == 0xFFFFFF or
                                size < 3
                            )

                            if is_hidden and color != 0x000000:
                                hidden_texts.append({
                                    "page": page_num + 1,
                                    "text": text
                                })

    doc.close()

    # 문장만 (길이 > 10)
    sentences = []
    for item in hidden_texts:
        if len(item['text']) > 10:
            sentences.append(item['text'])
            print(f"Page {item['page']}: {item['text']}")

    # 콤마로 구분
    answer = ', '.join(sentences)
    print(f"\n최종 답안: {answer}")
    print(f"문장 개수: {len(sentences)}")

    if len(sentences) < 5:
        print(f"⚠️  {5 - len(sentences)}개 문장이 더 필요합니다!")

    return answer

def main():
    print("="*60)
    print("AI_TOP_100 Textfinder Challenge - 솔루션")
    print("="*60)

    # PDF 1
    answer1 = solve_pdf1()

    # PDF 2
    answer2 = solve_pdf2()

    # PDF 3
    answer3 = solve_pdf3()

    # PDF 4
    answer4 = solve_pdf4()

    # 최종 요약
    print(f"\n\n{'='*60}")
    print("최종 답안 요약")
    print(f"{'='*60}")
    print(f"문제 1 (14단어): {answer1}")
    print(f"문제 2 (11단어): {answer2}")
    print(f"문제 3 (5단어):  {answer3}")
    print(f"문제 4 (5문장):  {answer4}")

if __name__ == "__main__":
    main()
