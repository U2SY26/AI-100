#!/usr/bin/env python3
"""
모든 텍스트의 색상과 속성 분석
"""

import fitz  # PyMuPDF
from pathlib import Path
from collections import defaultdict

def analyze_pdf_colors(pdf_path):
    """PDF의 모든 텍스트 색상 분석"""
    doc = fitz.open(pdf_path)
    color_stats = defaultdict(list)

    print(f"\n{'='*60}")
    print(f"분석 중: {pdf_path.name}")
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

                            # RGB 변환
                            r = (color >> 16) & 0xFF
                            g = (color >> 8) & 0xFF
                            b = color & 0xFF

                            color_key = f"#{color:06x}"
                            color_stats[color_key].append({
                                "page": page_num + 1,
                                "text": text,
                                "rgb": (r, g, b),
                                "size": size
                            })

    doc.close()

    # 색상별 통계 출력
    print(f"\n발견된 색상 ({len(color_stats)}가지):")
    for color_hex, items in sorted(color_stats.items()):
        rgb = items[0]["rgb"]
        count = len(items)
        avg_size = sum(item["size"] for item in items) / count

        # 샘플 텍스트 (처음 3개)
        samples = [item["text"][:20] for item in items[:3]]

        print(f"\n색상: {color_hex} RGB{rgb} | {count}개 텍스트 | 평균크기: {avg_size:.1f}pt")
        print(f"  샘플: {samples}")

        # 밝은 색상 (RGB > 200) 표시
        if rgb[0] > 200 and rgb[1] > 200 and rgb[2] > 200:
            print(f"  ⚠️  밝은 색상! 숨겨진 텍스트일 가능성")
            # 전체 텍스트 출력
            print(f"  전체 텍스트:")
            for item in items:
                print(f"    Page {item['page']}: '{item['text']}'")

def main():
    base_dir = Path(".")

    # PDF 1-4 분석
    for i in range(1, 5):
        pdf_path = base_dir / f"pdf_{i}.pdf"
        if pdf_path.exists():
            analyze_pdf_colors(pdf_path)
        else:
            print(f"\n{pdf_path} 파일이 없습니다.")

if __name__ == "__main__":
    main()
