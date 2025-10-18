# AI_TOP_100 석판 문제 풀이

## 문제 개요

**대회명**: AI_TOP_100  
**문제**: 고대 유적의 비밀 - 이상한 코드 석판  
**힌트**: "멈추어야 비로소 보이리라"

---

## 문제 내용

석판 이미지에서 OCR로 코드를 추출하고, 다음 3가지 질문에 답해야 합니다:

1. 석판의 코드를 해석하기에 가장 적절한 언어는?
2. `1q2w3e4r`을 입력했을 때 stdout 출력은?
3. `HALT`를 입력했을 때 stdout 출력은?

---

## 코드 분석

### 1. 코드 구조

이 코드는 **C와 Python이 섞인 Polyglot 코드**입니다.

```python
#includestdio.h>//char*c_s="S";...
a="G";i=input;a+="NO";q="TL";b="R";b+="W";a+=b;q+="AH";
q=q[::-1];a=a[::-1];p=lambda x:print(x,end=b[:0])or(exit());
"""char*c_e
void(p)(char*x){printf(x);};
int(main)(){...}
```

### 2. 변수 초기화 분석

**a 변수 (오답 메시지)**
```python
a = "G"
a += "NO"        # a = "GNO"
b = "R" + "W"    # b = "RW"
a += b           # a = "GNORW"
a = a[::-1]      # a = "WRONG" (역순)
```

**q 변수 (정답 키워드)**
```python
q = "TL"
q += "AH"        # q = "TLAH"
q = q[::-1]      # q = "HALT" (역순)
```

### 3. 핵심 로직

```python
if input() != "HALT":
    print("WRONG")
else:
    # r 변수 구성 후 출력
    print(r)
```

### 4. r 변수 구성 (HALT 입력 시)

이미지 중간 부분에 숨겨진 Python 코드:

```python
# ... 여러 줄의 코드 후 ...
r = "A"          # 838 줄에서 리셋
r += "I"         # r = "AI"
r += "T"         # r = "AIT"
r += "O"         # r = "AITO"
r += "P"         # r = "AITOP"
r += "1"         # r = "AITOP1"
r += "0"         # r = "AITOP10"
r += "0"         # r = "AITOP100"
print(r)         # 출력: AITOP100
```

---

## 실행 결과

### 테스트 1: `1q2w3e4r` 입력

```
입력: 1q2w3e4r
조건: "1q2w3e4r" != "HALT" → True
출력: WRONG
```

### 테스트 2: `HALT` 입력

```
입력: HALT
조건: "HALT" == "HALT" → True
r 변수 구성 실행:
  r = "A"
  r += "I"    → "AI"
  r += "T"    → "AIT"
  r += "O"    → "AITO"
  r += "P"    → "AITOP"
  r += "1"    → "AITOP1"
  r += "0"    → "AITOP10"
  r += "0"    → "AITOP100"
출력: AITOP100
```

---

## 최종 답안

### 문제 1: 석판 코드의 언어는?

**답: C**

**근거:**
- `#include<stdio.h>` - C 헤더 파일
- `void(p)(char*x){printf(x);}` - C 함수 정의
- `int(main)()` - C 메인 함수
- 샘플 문제에서 `gcc -w main.c`로 컴파일

### 문제 2: `1q2w3e4r` 입력 시 출력은?

**답: WRONG**

**근거:**
- 코드 로직: `if input() != "HALT": print("WRONG")`
- `"1q2w3e4r" ≠ "HALT"` → True
- 따라서 "WRONG" 출력

### 문제 3: `HALT` 입력 시 출력은?

**답: AITOP100**

**근거:**
- "멈추어야 비로소 보이리라" → HALT가 정답 키워드
- `input() == "HALT"` → else 블록 실행
- r 변수 구성: A + I + T + O + P + 1 + 0 + 0 = "AITOP100"
- 언더스코어(_) 없음!

---

## 주요 포인트

### 🔑 핵심 힌트 해석

**"멈추어야 비로소 보이리라"**
- HALT = 정지, 멈춤
- HALT를 입력해야 숨겨진 메시지가 드러남

### ⚠️ 주의사항

**AI_TOP_100 ❌**  
**AITOP100 ✅**

언더스코어가 없어야 합니다! 코드 내에서 r 변수를 구성할 때 언더스코어를 추가하는 부분이 없었습니다.

### 🎨 Polyglot 기법

이 코드는 C와 Python 양쪽에서 모두 유효하지만:
- C로 컴파일하면 C 부분만 실행
- Python으로 실행하면 Python 부분만 유효

Python의 경우:
- `#include...` 부분은 주석으로 처리
- 삼중 따옴표(`"""`) 내의 C 코드는 문자열로 처리

---

## 요약

| 문제 | 답안 | 배점 |
|------|------|------|
| 1. 프로그래밍 언어 | **C** | 15점 |
| 2. `1q2w3e4r` 출력 | **WRONG** | 20점 |
| 3. `HALT` 출력 | **AITOP100** | 35점 |

**총점: 70점**

---

## 코드 실행 시뮬레이션

```javascript
// 변수 초기화
let a = "GNORW".split('').reverse().join('');  // "WRONG"
let q = "TLAH".split('').reverse().join('');   // "HALT"

// 케이스 1
if ("1q2w3e4r" !== "HALT") {
    console.log("WRONG");  // ✓ 출력됨
}

// 케이스 2
if ("HALT" === "HALT") {
    let r = "A" + "I" + "T" + "O" + "P" + "1" + "0" + "0";
    console.log(r);  // "AITOP100" ✓ 출력됨
}
```

---

**작성일**: 2025년 10월 18일  
**대회**: AI_TOP_100 온라인 예선  
**문제**: 고대 유적의 비밀 - 이상한 코드 석판