# AI_TOP_100 Textfinder Challenge - Answers

> **작성일**: 2025-10-18
> **문제**: PDF 숨겨진 텍스트 찾기
> **총점**: 75점

---

## 문제 개요

4개의 PDF 파일에서 다양한 방법으로 숨겨진 텍스트를 찾는 문제입니다.

### 숨김 방식
1. **PDF 1**: 이미지에 배경색과 비슷한 색상의 텍스트 (14단어)
2. **PDF 2**: 흰색 또는 극소 폰트 크기의 텍스트 (11단어)
3. **PDF 3**: 보이지 않는 레이어의 텍스트 (5단어)
4. **PDF 4**: 5개의 노래 가사 문장 (다양한 숨김 방식)

---

## 답안

### 문제 1: PDF 1 (14단어)

**문제 유형**: 이미지 기반 PDF + 배경색 유사 텍스트

**발견 사항**:
- PDF 1은 스캔 이미지 PDF (텍스트 레이어 없음)
- 총 26페이지, 모든 페이지가 이미지 블록
- OCR 필요

**해결 방법**:
1. PyMuPDF로 이미지 추출
2. 대비(Contrast) 3배 증가
3. PNG로 저장
4. OCR 또는 수동 확인

**생성된 파일**:
- `pdf_1_page1_enhanced.png`
- `pdf_1_page2_enhanced.png`
- `pdf_1_page3_enhanced.png`
- `pdf_1_page4_enhanced.png`
- `pdf_1_page5_enhanced.png`

**답**: (Tesseract OCR 미설치로 수동 확인 필요)

---

### 문제 2: PDF 2 (11단어) ✅

**답안**: `I need to get a nice score when it is assessed`

**근거**:
- 페이지: 7
- 색상: `#efefef` RGB(239, 239, 239)
- 폰트 크기: 2.2pt
- 단어 수: 11 ✓

**추출 코드**:
```python
# 매우 밝은 색상 (RGB > 230)
if r > 230 and g > 230 and b > 230:
    # 숨겨진 텍스트 발견
```

---

### 문제 3: PDF 3 (5단어)

**문제 유형**: 보이지 않는 레이어 또는 숨겨진 텍스트

**발견 사항**:
- PDF 문서: NASA EcAMSat 기술 논문
- 총 8페이지
- 정상 텍스트와 함께 5단어가 숨겨져 있음

**추출 방법**:
```python
# 모든 레이어의 텍스트 추출
all_text = page.get_text()
```

**답**: (전체 텍스트에서 5단어 패턴 분석 필요)

**예상**:
- 특정 색상 또는 위치에 숨겨진 5단어
- 또는 특정 페이지에만 존재하는 짧은 문구

---

### 문제 4: PDF 4 (5문장) - 노래 가사 ⚠️

**답안** (3/5 발견):
1. `Twinkle twinkle little star` (Page 14, #ffffff)
2. `Oh Danny boy the pipes the pipes are calling` (Page 109, #ffffff)
3. `Row row row your boat gently down the stream` (Page 162, #efefef)

**제출 형식** (콤마로 구분):
```
Twinkle twinkle little star, Oh Danny boy the pipes the pipes are calling, Row row row your boat gently down the stream
```

**미발견**: 2개 문장 추가 필요

**검색 방법**:
- 흰색 텍스트 (`#ffffff`)
- 밝은 색상 (RGB > 200)
- 작은 폰트 (< 3pt)

**참고**:
- PDF 4는 188페이지의 방대한 문서
- "The Inheritors" 소설 전문
- 추가 문장은 더 낮은 임계값 또는 다른 숨김 방식 가능

---

## 기술적 분석

### PDF 구조 분석

```python
# PDF 1
- 타입: 이미지 기반 PDF
- 텍스트 레이어: 없음
- 이미지 개수: 26개 (페이지당 1개)
- 해결 방법: OCR

# PDF 2
- 타입: 텍스트 PDF
- 숨김 방식: 극도로 밝은 색상 (#efefef) + 작은 폰트 (2.2pt)
- 발견: Page 7

# PDF 3
- 타입: 텍스트 PDF
- 총 페이지: 8
- 문서: NASA 기술 논문
- 숨김 방식: 레이어 또는 특수 색상

# PDF 4
- 타입: 텍스트 PDF
- 총 페이지: 188
- 문서: "The Inheritors" 소설
- 숨김 방식: 흰색 (#ffffff) 및 밝은 색상 (#efefef)
- 발견: 3개 문장 (추가 2개 필요)
```

### 사용된 도구

1. **PyMuPDF (fitz)**: PDF 파싱, 텍스트 추출
2. **PIL (Pillow)**: 이미지 처리, 대비 증가
3. **Python**: 자동화 스크립트

---

## 미해결 과제

### PDF 1
- [ ] Tesseract OCR 설치
- [ ] 모든 26페이지 OCR 수행
- [ ] 14단어 추출

### PDF 3
- [ ] 5단어 패턴 식별
- [ ] 숨겨진 텍스트 위치 찾기

### PDF 4
- [ ] 추가 2개 노래 가사 문장 찾기
- [ ] 더 낮은 RGB 임계값 시도 (150-200 범위)
- [ ] 폰트 크기 기준 조정 (3-5pt 범위)
- [ ] 페이지별 상세 스캔

---

## 실행 파일

### 메인 솔루션
```bash
cd /d/AI-100/ai_top_100_textfinder
python solution.py
```

### 색상 분석
```bash
python analyze_all_colors.py
```

### PDF 1 OCR (Tesseract 필요)
```bash
python ocr_pdf1.py
```

---

## 참고 자료

### 파일 구조
```
ai_top_100_textfinder/
├── pdf_1.pdf                     # 문제 1 (35MB, 이미지 PDF)
├── pdf_2.pdf                     # 문제 2 (6.1MB)
├── pdf_3.pdf                     # 문제 3 (3.2MB)
├── pdf_4.pdf                     # 문제 4 (2.4MB)
├── solution.py                   # 통합 솔루션 스크립트
├── analyze_all_colors.py         # 색상 분석 도구
├── extract_hidden_text.py        # 숨겨진 텍스트 추출 (원본)
├── pdf_1_page*_enhanced.png      # PDF 1 향상된 이미지
└── ANSWERS.md                    # 이 파일
```

---

## 최종 제출 답안 (현재)

| 문제 | 예상 단어/문장 수 | 발견 | 답안 |
|------|-------------------|------|------|
| PDF 1 | 14단어 | 0/14 | OCR 필요 |
| PDF 2 | 11단어 | 11/11 ✅ | I need to get a nice score when it is assessed |
| PDF 3 | 5단어 | 0/5 | 분석 필요 |
| PDF 4 | 5문장 | 3/5 ⚠️ | Twinkle..., Oh Danny..., Row row... |

**완료율**: 14/35 (40%)

---

**다음 단계**:
1. Tesseract 설치하여 PDF 1 처리
2. PDF 3의 5단어 패턴 찾기
3. PDF 4의 추가 2개 문장 찾기
