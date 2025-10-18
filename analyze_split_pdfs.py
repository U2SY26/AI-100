#!/usr/bin/env python3
"""
분할된 PDF 1-1, 1-2 분석
숨겨진 14단어 찾기
"""

import fitz
from collections import defaultdict

def analyze_pdf_structure(pdf_path):
    """PDF 구조 분석"""
    doc = fitz.open(pdf_path)

    print(f"\n{'='*60}")
    print(f"PDF: {pdf_path}")
    print(f"{'='*60}")
    print(f"총 페이지: {len(doc)}")

    # 첫 페이지 분석
    page = doc[0]
    text = page.get_text()
    images = page.get_images()

    print(f"첫 페이지 텍스트 길이: {len(text)}")
    print(f"첫 페이지 이미지 개수: {len(images)}")

    if len(text) > 0:
        print(f"텍스트 샘플: {text[:200]}")

    # dict로 텍스트 블록 확인
    blocks = page.get_text("dict")["blocks"]
    print(f"첫 페이지 블록 개수: {len(blocks)}")

    doc.close()

def find_hidden_text_in_pdf(pdf_path):
    """숨겨진 텍스트 찾기"""
    doc = fitz.open(pdf_path)
    hidden_texts = []

    print(f"\n{'='*60}")
    print(f"숨겨진 텍스트 검색: {pdf_path}")
    print(f"{'='*60}")

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text:
                            color = span["color"]
                            size = span["size"]

                            r = (color >> 16) & 0xFF
                            g = (color >> 8) & 0xFF
                            b = color & 0xFF

                            # 밝은 색상 찾기 (RGB > 150)
                            if r > 150 and g > 150 and b > 150 and color != 0x000000:
                                hidden_texts.append({
                                    "page": page_num + 1,
                                    "text": text,
                                    "color": f"#{color:06x}",
                                    "rgb": (r, g, b),
                                    "size": size
                                })

    doc.close()

    if hidden_texts:
        print(f"\n발견된 숨겨진 텍스트: {len(hidden_texts)}개\n")

        for i, item in enumerate(hidden_texts, 1):
            print(f"{i}. Page {item['page']}: '{item['text']}'")
            print(f"   색상: {item['color']} RGB{item['rgb']}, 크기: {item['size']:.1f}pt\n")

        # 전체 문장 조합
        all_words = []
        for item in hidden_texts:
            words = item['text'].split()
            all_words.extend(words)

        print(f"{'='*60}")
        print(f"총 단어 수: {len(all_words)}")
        print(f"전체 텍스트: {' '.join([item['text'] for item in hidden_texts])}")
        print(f"{'='*60}")
    else:
        print("숨겨진 텍스트를 찾지 못했습니다.")

    return hidden_texts

def main():
    print("="*60)
    print("PDF 1 분할 파일 분석 (1-1.pdf, 1-2.pdf)")
    print("="*60)

    # 구조 분석
    analyze_pdf_structure("1-1.pdf")
    analyze_pdf_structure("1-2.pdf")

    # 숨겨진 텍스트 찾기
    results_1_1 = find_hidden_text_in_pdf("1-1.pdf")
    results_1_2 = find_hidden_text_in_pdf("1-2.pdf")

    # 전체 결과
    print(f"\n\n{'='*60}")
    print("전체 결과 요약")
    print(f"{'='*60}")

    all_results = results_1_1 + results_1_2

    if all_results:
        all_text = ' '.join([item['text'] for item in all_results])
        word_count = len(all_text.split())

        print(f"1-1.pdf: {len(results_1_1)}개 텍스트")
        print(f"1-2.pdf: {len(results_1_2)}개 텍스트")
        print(f"합계: {len(all_results)}개 텍스트")
        print(f"\n전체 텍스트:")
        print(all_text)
        print(f"\n총 단어 수: {word_count}")

        if word_count == 14:
            print("\n✅ 14단어 발견! 정답일 가능성 높음")
        else:
            print(f"\n⚠️ {word_count}단어 발견 (예상: 14단어)")
    else:
        print("숨겨진 텍스트를 찾지 못했습니다.")

if __name__ == "__main__":
    main()
