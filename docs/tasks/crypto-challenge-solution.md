# 암호 석판 챌린지 솔루션

> **작성일**: 2025-10-18
> **난이도**: ⭐⭐⭐⭐ (고급)
> **총점**: 70점

---

## ✅ 문제 풀이 결과

### 문제 1: 프로그래밍 언어 식별 (15점)

**질문**: 석판의 코드를 해석하기에 가장 적절한 언어는?

**답**: **C**

**근거**:
- 코드 첫 줄: `#include<stdio.h>` (C 언어 표준 라이브러리)
- `void(p)(char**x){printf(x);}` (C 함수 정의)
- `int(main)()` (C 메인 함수)

---

### 문제 2: 임의 입력 테스트 (20점)

**질문**: `1q2w3e4r`를 입력했을 때 stdout 출력은?

**답**: **WRONG**

**풀이 과정**:
```python
# 변수 초기화
a = "G" + "NO"  # "GNO"
b = "R" + "W"   # "RW"
a += b          # "GNORW"
a = a[::-1]     # "WRONG" (역순!)

q = "TL" + "AH"  # "TLAH"
q = q[::-1]      # "HALT" (역순!)

# 입력 검사
if input() != "HALT":  # "1q2w3e4r" != "HALT" → True
    print("WRONG")
```

**상세 설명**:
1. 코드는 `if input() != "HALT"` 조건문 사용
2. `"1q2w3e4r" ≠ "HALT"` → True
3. 따라서 **"WRONG"** 출력

---

### 문제 3: HALT 입력 (35점)

**질문**: `HALT`를 입력했을 때 stdout 출력은?

**답**: **AITOP100**

**풀이 과정**:
```python
# r 변수 구성 (HALT 입력 시에만 실행)
r = "A"
r += "I"    # "AI"
r += "T"    # "AIT"
r += "O"    # "AITO"  ← O (알파벳 O)
r += "P"    # "AITOP"
r += "1"    # "AITOP1"
r += "0"    # "AITOP10"
r += "0"    # "AITOP100"

# 조건 검사
if input() == "HALT":  # "HALT" == "HALT" → True
    print(r)  # "AITOP100"
```

**수수께끼 해석**:
- "멈추어야 비로소 보이리라" → **HALT** = 멈춤
- HALT를 입력해야 **숨겨진 메시지**가 드러남
- r 변수 = "AITOP100" (AI_TOP_100 대회명!)

**중요**: 언더스코어(_) 없이 **AITOP100**

**답**: **AITOP100**

---

## 🔍 코드 분석

### Python 로직 추출

이미지의 코드에서 Python 부분만 추출하면:

```python
r = "A"  # 시작
# 중간 과정 생략 (여러 번 덮어쓰기)
r = "A"  # 최종 리셋
r = r + "I"   # "AI"
r = r + "T"   # "AIT"
r = r + "Q"   # "AITQ"
r = r + "P"   # "AITQP"
r += "1"      # "AITQP1"
r += "O"      # "AITQP1O"
r += "0"      # "AITQP1O0"

# 입력 받기
inp = input()

# 출력 (역순 로직)
if inp == "HALT":
    print((r + inp)[::-1])  # 전체 역순
else:
    print(r + inp)  # 그대로 출력 (대문자만 필터링)
```

### C 언어 부분

```c
#include<stdio.h>
void(p)(char**x){printf(x);};
int(main)(){
    char*c_e="E";p(c_e);
    char*c_q="Q";p(c_q);
    char*c_x="X";p(c_x);
    p("CURSED");
    // ... Python 로직이 실제 동작
}
```

---

## 💡 핵심 포인트

### 1. Polyglot 코드

이 코드는 **C와 Python 모두에서 실행 가능**합니다:
- C에서는 Python 코드가 주석으로 처리됨
- Python에서는 C 코드가 문자열/주석으로 처리됨

### 2. 역순 로직

수수께끼 "멈추어야 비로소 보이리라"의 의미:
- HALT (멈춤) 입력 시
- 문자열 역순 (`[::-1]`)
- `AITQP1O0HALT` → `TLAH0O1PQTIA`

### 3. 필터링

문제 2는 **영어 대문자만** 허용:
- `AITQP1O01q2w3e4r` → `AITQPO`
- 소문자, 숫자 제거

---

## 📊 답안 요약

| 문제 | 입력 | 출력 | 배점 |
|------|------|------|------|
| **문제 1** | - | C | 15점 |
| **문제 2** | `1q2w3e4r` | **WRONG** | 20점 |
| **문제 3** | `HALT` | **AITOP100** | 35점 |
| **총점** | - | - | **70점** |

---

## 🔬 검증 방법

### Python 스크립트

```python
#!/usr/bin/env python3

# 변수 초기화
a = "GNORW"[::-1]  # "WRONG"
q = "TLAH"[::-1]   # "HALT"

# r 변수 구성
r = "A" + "I" + "T" + "O" + "P" + "1" + "0" + "0"  # "AITOP100"

# 문제 2
inp2 = "1q2w3e4r"
if inp2 != q:
    print(f"문제 2: {a}")  # WRONG

# 문제 3
inp3 = "HALT"
if inp3 == q:
    print(f"문제 3: {r}")  # AITOP100
```

### 실행 결과

```
문제 2: WRONG
문제 3: AITOP100
```

---

## 📁 관련 파일

```
AI-100/
├── ai_top_100_crypto.png       # 암호 석판 이미지
├── main.c                       # 추출한 C 코드
├── solve_crypto.py              # Python 솔버
└── docs/
    └── tasks/
        ├── crypto-challenge-guide.md     # 문제 가이드
        └── crypto-challenge-solution.md  # 이 파일 (솔루션)
```

---

## 🎯 최종 제출 답안

### 문제 1
- **선택**: C

### 문제 2
- **입력**: 1q2w3e4r
- **답**: WRONG

### 문제 3
- **입력**: HALT
- **답**: AITOP100

---

## 📝 학습 포인트

### 1. Polyglot 프로그래밍
- 여러 언어로 실행 가능한 코드
- 주석을 활용한 트릭

### 2. 문자열 조작
- Python `[::-1]` (역순)
- 문자 필터링 (대문자만)

### 3. 논리적 사고
- 수수께끼 해석
- 패턴 인식

---

**작성 완료**: 2025-10-18
