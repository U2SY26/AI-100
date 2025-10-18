#!/usr/bin/env python3
"""
PDF 4에서 모든 숨겨진 텍스트 찾기 (5개 문장)
"""

import fitz

pdf_path = "pdf_4.pdf"
doc = fitz.open(pdf_path)

print(f"PDF 4 전체 페이지 스캔: {len(doc)} pages")
print(f"{'='*60}\n")

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

                        # 밝은 색상 또는 흰색
                        if (r > 200 and g > 200 and b > 200) or color == 0xFFFFFF:
                            hidden_texts.append({
                                "page": page_num + 1,
                                "text": text,
                                "color": f"#{color:06x}",
                                "rgb": (r, g, b),
                                "size": size
                            })

doc.close()

# 결과 출력
print(f"발견된 숨겨진 텍스트: {len(hidden_texts)}개\n")

for i, item in enumerate(hidden_texts, 1):
    print(f"{i}. Page {item['page']}: '{item['text']}'")
    print(f"   색상: {item['color']} RGB{item['rgb']}, 크기: {item['size']:.1f}pt\n")

# 전체 문장 조합
if hidden_texts:
    sentences = [item['text'] for item in hidden_texts]
    result = ', '.join(sentences)
    print(f"{'='*60}")
    print(f"최종 답안 (콤마로 구분):")
    print(f"{'='*60}")
    print(result)
    print(f"\n문장 개수: {len(sentences)}")
