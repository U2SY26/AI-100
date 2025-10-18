# 암호 석판 챌린지 가이드

> **작성일**: 2025-10-18
> **난이도**: ⭐⭐⭐⭐ (고급)
> **예상 소요시간**: 60-90분

---

## 📋 문제 개요

### 배경
고대 유적의 석판에 새겨진 암호 코드를 해독하는 챌린지입니다.

**수수께끼**: "멈추어야 비로소 보이리라" (HALT와 관련)

### 배점 (총 70점)
| 문제 | 배점 | 난이도 | 설명 |
|------|------|--------|------|
| 문제 1 | 15점 | ⭐⭐ | 프로그래밍 언어 식별 |
| 문제 2 | 20점 | ⭐⭐⭐ | `1q2w3e4r` 입력 시 출력 |
| 문제 3 | 35점 | ⭐⭐⭐⭐ | `HALT` 입력 시 출력 |

---

## 🔍 문제 분석

### 문제 1: 언어 식별 (15점)

**질문**: 석판의 코드를 해석하기에 가장 적절한 언어는?

**선택지**:
- JavaScript
- Rust
- Java
- Python
- C

**힌트**:
- 코드 첫 줄: `#include<stdio.h>`
- C 언어의 전처리기 지시문
- `scanf`, `printf` 등 C 표준 라이브러리 함수

**답**: **C**

---

### 문제 2: 임의 입력 테스트 (20점)

**질문**: `1q2w3e4r`를 입력했을 때 stdout 출력은?

**제약**: 영어 대문자만 허용

**분석**:
- 코드는 입력을 변환하여 출력
- 샘플 문제 참고: "CHOONSIKISACAT" (대문자)
- 역순 로직 또는 필터링 가능성

**답**: (코드 실행 후 확인 필요)

---

### 문제 3: HALT 입력 (35점)

**질문**: `HALT`를 입력했을 때 stdout 출력은?

**제약**: 영어 대문자, 숫자 허용

**힌트**:
- "멈추어야 비로소 보이리라"
- HALT = 멈춤
- 역순 로직: HALT → TLAH?

**답**: (코드 실행 후 확인 필요)

---

## 💻 코드 구조 분석

### Polyglot 패턴

이 코드는 **C와 Python 혼합 코드**(Polyglot)입니다:

```c
#include<stdio.h>  // C 언어
// Python 코드가 C 주석으로 처리됨
"""
C 코드
""" // Python 주석이 C에서는 문자열
```

### 샘플 코드 패턴

샘플을 보면:
1. **Python 부분**: `r=r[::-1]` (역순)
2. **C 부분**: `scanf`로 입력, `printf`로 출력
3. **주석 처리**: Python 코드가 C 주석으로 무시됨

---

## 🔧 실행 방법

### 1. 코드 추출

이미지에서 모든 텍스트를 정확히 타이핑합니다.

```bash
# 1. 이미지 열기
code ai_top_100_crypto.png

# 2. 모든 문자를 main.c에 복사
```

### 2. 컴파일

```bash
gcc -w main.c -o crypto
```

`-w`: 경고 무시

### 3. 실행 및 테스트

```bash
# 문제 2
echo "1q2w3e4r" | ./crypto

# 문제 3
echo "HALT" | ./crypto
```

---

## 📝 샘플 문제 분석

### 샘플 입력: CAT
### 샘플 출력: CHOONSIKISACAT

**분석**:
```
입력: CAT
출력: CHOONSIKISACAT

패턴:
- "CHOONSIKIS" + "ACAT"
- "CAT"의 역순 "TAC" → "ACAT"?
- 또는 "CHOONSIKIS" + "A" + 입력
```

**추정 로직**:
1. 고정 문자열 출력
2. 입력 문자열 변환 (역순? 치환?)
3. 합쳐서 출력

---

## 🎯 풀이 전략

### Step 1: 코드 정확히 추출

**중요 포인트**:
- ✅ 모든 문자 정확히 타이핑
- ✅ 주석 부분도 포함 (C에서 무시됨)
- ✅ 공백, 세미콜론 정확히

### Step 2: 컴파일 성공 확인

```bash
gcc -w main.c -o crypto
echo $?  # 0이면 성공
```

### Step 3: 테스트 실행

```bash
# 샘플 테스트
echo "CAT" | ./crypto
# 예상: CHOONSIKISACAT

# 문제 2
echo "1q2w3e4r" | ./crypto

# 문제 3
echo "HALT" | ./crypto
```

---

## ⚠️ 주의사항

### OCR 오류 가능성

- `0` vs `O` (숫자 0 vs 알파벳 O)
- `1` vs `l` (숫자 1 vs 소문자 L)
- `;` vs `:` (세미콜론 vs 콜론)

### 컴파일 에러 시

```bash
# 에러 메시지 확인
gcc main.c -o crypto 2>&1 | head -20

# 해당 라인 수정
```

---

## 🔍 디버깅 팁

### 1. 단순화된 테스트

```c
// 최소 동작 코드
#include<stdio.h>
int main(){
    char c[100];
    scanf("%s", c);
    printf("%s", c);
}
```

### 2. 역순 로직 확인

```python
# Python에서 역순
text = "HALT"
reversed_text = text[::-1]
print(reversed_text)  # TLAH
```

---

## 📚 관련 개념

### Polyglot 프로그래밍

하나의 소스 코드가 여러 언어로 실행 가능:

```c
#if 0
print("Python")
#endif
#include<stdio.h>
int main(){printf("C\n");}
```

### 역순 문자열 (Reverse String)

```c
// C에서 역순 출력
void reverse(char* str){
    int len = strlen(str);
    for(int i=len-1; i>=0; i--){
        printf("%c", str[i]);
    }
}
```

---

## ✅ 체크리스트

### 문제 1
- [ ] 코드 첫 줄 확인 (`#include`)
- [ ] C 언어 선택

### 문제 2
- [ ] 코드 컴파일 성공
- [ ] `1q2w3e4r` 입력 테스트
- [ ] 출력 확인 (대문자만)
- [ ] 답안 제출

### 문제 3
- [ ] `HALT` 입력 테스트
- [ ] "멈추어야 비로소 보이리라" 힌트 활용
- [ ] 출력 확인 (대문자+숫자)
- [ ] 답안 제출

---

## 📖 참고 자료

### 파일 구조
```
AI-100/
├── ai_top_100_crypto.png     # 암호 석판 이미지
├── main.c                      # 추출한 C 코드
├── crypto                      # 컴파일된 실행 파일
└── docs/
    └── tasks/
        └── crypto-challenge-guide.md  # 이 파일
```

---

## 🚀 빠른 시작

```bash
# 1. 이미지 확인
code ai_top_100_crypto.png

# 2. 코드 추출 (수동)
code main.c
# 이미지의 모든 텍스트 복사

# 3. 컴파일
gcc -w main.c -o crypto

# 4. 테스트
echo "CAT" | ./crypto
echo "1q2w3e4r" | ./crypto
echo "HALT" | ./crypto
```

---

**행운을 빕니다! 🍀**
