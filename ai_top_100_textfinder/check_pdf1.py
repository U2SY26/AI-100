#!/usr/bin/env python3
"""
PDF 1 상세 분석
"""

import fitz
from PIL import Image
import io

pdf_path = "pdf_1.pdf"
doc = fitz.open(pdf_path)

print(f"총 페이지: {len(doc)}")

for page_num in range(len(doc)):
    page = doc[page_num]

    print(f"\n{'='*60}")
    print(f"Page {page_num + 1}")
    print(f"{'='*60}")

    # 텍스트 추출
    text = page.get_text()
    print(f"텍스트 길이: {len(text)}")
    print(f"텍스트 샘플: {text[:200]}")

    # 이미지 확인
    images = page.get_images()
    print(f"\n이미지 개수: {len(images)}")

    # dict로 상세 정보
    blocks = page.get_text("dict")["blocks"]
    print(f"블록 개수: {len(blocks)}")

    for i, block in enumerate(blocks[:3]):  # 처음 3개만
        print(f"\n블록 {i+1}: {block.get('type', 'unknown')}")
        if block.get('type') == 0:  # text block
            print(f"  Lines: {len(block.get('lines', []))}")
        elif block.get('type') == 1:  # image block
            print(f"  이미지 블록")
            print(f"  bbox: {block.get('bbox')}")

doc.close()
