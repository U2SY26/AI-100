#!/usr/bin/env python3
"""
암호 석판 정답 - 수정된 버전
"""

print("=" * 60)
print("암호 석판 챌린지 - 정답")
print("=" * 60)

# 변수 초기화 (이미지 첫 줄)
a = "G"
a += "NO"       # "GNO"
b = "R" + "W"   # "RW"
a += b          # "GNORW"
a = a[::-1]     # "WRONG" (역순!)

q = "TL"
q += "AH"       # "TLAH"
q = q[::-1]     # "HALT" (역순!)

print(f"\na (오답 메시지): {a}")
print(f"q (정답 키워드): {q}")

# r 변수 구성 (HALT 입력 시에만 실행)
r = "A"
r += "I"    # "AI"
r += "T"    # "AIT"
r += "O"    # "AITO"  ← 'O'입니다!
r += "P"    # "AITOP"
r += "1"    # "AITOP1"
r += "0"    # "AITOP10"
r += "0"    # "AITOP100"

print(f"\nr (정답 메시지): {r}")

print("\n" + "=" * 60)
print("문제 풀이")
print("=" * 60)

print("\n문제 1: 프로그래밍 언어")
print("답: C")

print("\n문제 2: 입력 '1q2w3e4r'")
inp2 = "1q2w3e4r"
if inp2 != q:  # "1q2w3e4r" != "HALT"
    print(f"조건: '{inp2}' != '{q}' → True")
    print(f"답: {a}")  # WRONG
else:
    print(f"답: {r}")

print("\n문제 3: 입력 'HALT'")
inp3 = "HALT"
if inp3 != q:  # "HALT" != "HALT"
    print(f"조건: '{inp3}' != '{q}' → False")
    print(f"답: {a}")
else:
    print(f"조건: '{inp3}' == '{q}' → True")
    print(f"답: {r}")  # AITOP100

print("\n" + "=" * 60)
print("최종 답안")
print("=" * 60)
print("문제 1: C")
print("문제 2: WRONG")
print("문제 3: AITOP100")
