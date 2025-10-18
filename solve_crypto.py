#!/usr/bin/env python3
"""
암호 석판 솔버
이미지의 Python 코드 로직을 재현
"""

# 최종 문자열 생성
r = "A"
r = r + "I"
r = r + "T"
r = r + "Q"
r = r + "P"
r += "1"
r += "O"
r += "0"

print("=" * 60)
print("암호 석판 솔버")
print("=" * 60)
print(f"\n고정 문자열 r = '{r}'")
print(f"역순 r[::-1] = '{r[::-1]}'")

print("\n" + "=" * 60)
print("문제 1: 프로그래밍 언어")
print("=" * 60)
print("답: C (또는 Python polyglot)")

print("\n" + "=" * 60)
print("문제 2: 입력 '1q2w3e4r'")
print("=" * 60)
inp2 = "1q2w3e4r"
# 입력을 역순으로?
output2 = r + inp2[::-1]
print(f"출력 (r + 역순): {output2}")
print(f"역순만: {inp2[::-1]}")

# 또는 입력 그대로
output2_plain = r + inp2
print(f"출력 (r + 입력): {output2_plain}")

# 대문자만 필터링?
output2_upper = ''.join([c for c in output2_plain if c.isupper()])
print(f"대문자만: {output2_upper}")

print("\n" + "=" * 60)
print("문제 3: 입력 'HALT'")
print("=" * 60)
inp3 = "HALT"
output3 = r + inp3[::-1]
print(f"출력 (r + 역순): {output3}")
output3_rev = output3[::-1]
print(f"전체 역순: {output3_rev}")

# HALT의 역순
print(f"HALT 역순: {inp3[::-1]}")

# r 자체를 역순으로
output3_r_rev = r[::-1] + inp3
print(f"r 역순 + HALT: {output3_r_rev}")

# 전체를 역순으로
output3_all_rev = (r + inp3)[::-1]
print(f"(r + HALT) 역순: {output3_all_rev}")

print("\n" + "=" * 60)
print("추정 답안")
print("=" * 60)
print("문제 1: C")
print(f"문제 2: {output2_upper} (대문자만)")
print(f"문제 3: {output3_all_rev} 또는 {output3_r_rev}")
