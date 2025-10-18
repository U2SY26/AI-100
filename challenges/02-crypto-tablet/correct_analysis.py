#!/usr/bin/env python3
"""
이미지 코드를 정확하게 분석
왼쪽부터 오른쪽으로 순서대로 읽어야 함
"""

# 이미지의 Python 코드 부분만 순서대로 추출
# 첫 줄: r=lambda x:input("TURNAROUND");

# 이후 중간 열들을 왼쪽에서 오른쪽으로 읽으면:
# 왼쪽 열 (8//8;eval; 등): Python 코드
# 중간 열 (hex;j= input; 등): Python 코드  
# 오른쪽 열 (r="A"; 등): Python 코드

# 순서대로 읽기:
r = "A"
# hex는 무시 (함수 호출)
# j = input은 무시
r = "A"  # 다시 시작
# i=input은 무시
# False는 무시
r = "L"  # 덮어쓰기
i = None  # input 무시
# p=print 무시
r = r + "T"  # "LT"
r += "Q"  # "LTQ"
# i=input 무시
r = r + "C"  # "LTQC" 
# p=print 무시
r = r + "T"  # "LTQCT"
# p=print 무시
r = r + "Q"  # "LTQCTQ"
r = r + "Z"  # "LTQCTQZ"
# p=print 무시
r += "S"  # "LTQCTQZS"
r = r + "B"  # "LTQCTQZSB"
# True 무시
r += "E"  # "LTQCTQZSBE"
# False 무시
# r = r + 는 이미 위에 있음
r = r + "S"  # "LTQCTQZSBES"
# r = r + 무시
r = r + "X"  # "LTQCTQZSBESX"
r = r + "T"  # "LTQCTQZSBESXT"
# len, abs 무시
r += "R"  # "LTQCTQZSBESXTR"
r = r + "C"  # "LTQCTQZSBESXTRC"
# 83j는 무시
r = "A"  # 다시 리셋!
# r = r + 무시
r = r + "I"  # "AI"
r = r + "T"  # "AIT"
# r = r + 무시
r = r + "Q"  # "AITQ"
r = r + "P"  # "AITQP"
# p=print 무시
r += "1"  # "AITQP1"
r += "O"  # "AITQP1O"
# pass 무시
r += "0"  # "AITQP1O0"
# pass 무시
# p(r) - 출력!

print("최종 r:", r)
print("r 역순:", r[::-1])

# 실제 동작 추정
print("\n문제 2: 1q2w3e4r")
inp2 = "1q2w3e4r"
# 대문자만 필터링
output2 = ''.join([c for c in (r + inp2) if c.isupper()])
print("출력:", output2)

print("\n문제 3: HALT")
inp3 = "HALT"
# 역순?
output3_1 = (r + inp3)[::-1]
print("방법 1 (전체 역순):", output3_1)

output3_2 = r[::-1] + inp3
print("방법 2 (r 역순):", output3_2)

output3_3 = r + inp3[::-1]
print("방법 3 (HALT 역순):", output3_3)
