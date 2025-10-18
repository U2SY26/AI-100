#!/usr/bin/env python3
"""
모든 PDF에서 숨겨진 텍스트 종합 검색
"""

import fitz
import re

def analyze_pdf3():
    """PDF 3: 레이어 숨김 텍스트 (5단어)"""
    print("="*60)
    print("PDF 3: 레이어 숨김 텍스트 분석")
    print("="*60)

    doc = fitz.open("pdf_3.pdf")

    # 모든 텍스트 추출
    all_text = ""
    for page_num in range(len(doc)):
        page = doc[page_num]
        all_text += page.get_text()

    # 5단어 패턴 찾기 (공백으로 구분)
    words = all_text.split()

    # 특이한 패턴 찾기
    suspicious_patterns = []

    # 연속된 5단어 조합 중 특이한 것 찾기
    for i in range(len(words) - 4):
        five_words = ' '.join(words[i:i+5])
        # 대문자로만 구성되거나, 특수한 패턴
        if five_words.isupper() or re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+$', five_words):
            suspicious_patterns.append(five_words)

    print(f"\n의심스러운 5단어 패턴: {len(suspicious_patterns)}개")
    for pattern in suspicious_patterns[:20]:  # 처음 20개만
        print(f"  - {pattern}")

    # 색상별 텍스트 분석
    print("\n색상별 텍스트 분석:")
    color_texts = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        color = span["color"]

                        if text and len(text.split()) <= 5:  # 5단어 이하
                            if color not in color_texts:
                                color_texts[color] = []
                            color_texts[color].append((page_num + 1, text))

    # 특이한 색상 찾기
    for color, texts in sorted(color_texts.items()):
        if color != 0x000000:  # 검정색이 아닌 것
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF

            # 5단어 정확히 있는지 확인
            for page, text in texts:
                if len(text.split()) == 5:
                    print(f"  Page {page}, 색상: #{color:06x} RGB({r},{g},{b})")
                    print(f"    텍스트: {text}")

    doc.close()
    print()

def analyze_pdf4_comprehensive():
    """PDF 4: 더 낮은 임계값으로 검색"""
    print("="*60)
    print("PDF 4: 종합 검색 (더 낮은 임계값)")
    print("="*60)

    doc = fitz.open("pdf_4.pdf")
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

                        if text and len(text.split()) >= 3:  # 3단어 이상
                            r = (color >> 16) & 0xFF
                            g = (color >> 8) & 0xFF
                            b = color & 0xFF

                            # 더 낮은 임계값: RGB > 150
                            if r > 150 and g > 150 and b > 150:
                                # 너무 흔한 색상 제외 (순수 검정 제외)
                                if not (r < 50 and g < 50 and b < 50):
                                    hidden_texts.append({
                                        "page": page_num + 1,
                                        "text": text,
                                        "color": f"#{color:06x}",
                                        "rgb": (r, g, b),
                                        "size": size
                                    })

    doc.close()

    print(f"\n발견된 텍스트: {len(hidden_texts)}개")

    # 페이지 순으로 정렬
    hidden_texts.sort(key=lambda x: x["page"])

    # 노래 가사일 가능성 있는 것만 필터링
    song_candidates = []
    for item in hidden_texts:
        text_lower = item["text"].lower()
        # 노래 가사 특징: 반복 단어, 특정 키워드
        if (any(word in text_lower for word in ['twinkle', 'danny', 'row', 'star', 'boy', 'boat', 'shine', 'sky', 'love', 'baby', 'heart', 'dream', 'night', 'day'])
            or len(set(item["text"].split())) < len(item["text"].split()) * 0.7):  # 반복 단어 많음
            song_candidates.append(item)

    print(f"\n노래 가사 후보: {len(song_candidates)}개")
    for i, item in enumerate(song_candidates, 1):
        print(f"{i}. Page {item['page']}: '{item['text']}'")
        print(f"   색상: {item['color']} RGB{item['rgb']}, 크기: {item['size']:.1f}pt")

    # 모든 후보 출력
    if song_candidates:
        print(f"\n{'='*60}")
        print("가능한 답안 (페이지 순):")
        print(f"{'='*60}")
        result = ', '.join([item['text'] for item in song_candidates])
        print(result)
        print(f"\n문장 개수: {len(song_candidates)}")

    print()

def analyze_pdf1_images():
    """PDF 1: 생성된 이미지 확인"""
    print("="*60)
    print("PDF 1: 이미지 기반 - 수동 확인 필요")
    print("="*60)
    print("\n생성된 향상된 이미지 파일:")
    import os
    for i in range(1, 6):
        filename = f"pdf_1_page{i}_enhanced.png"
        if os.path.exists(filename):
            print(f"  - {filename}")
    print("\n이 이미지들을 수동으로 확인하여 14단어를 찾으세요.")
    print()

if __name__ == "__main__":
    analyze_pdf1_images()
    analyze_pdf3()
    analyze_pdf4_comprehensive()
