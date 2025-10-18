# 이미지 코드에서 Python 로직만 추출
# 첫 줄: r=lambda x:input("TURNAROUND");char*a="G";i=input;a+="NO";q="TL";b="R";b+="W";a+=b;q+="AH";q=q[::-1];a=a[::-1];

# 이후 코드에서 r 문자열 조립
r = "A"  # 시작
# r = "H" → 덮어쓰기
# r = "L" → 덮어쓰기
# r = "T" → 덮어쓰기
# r += "Q"
# r = r + "C"
# r = r + "T"
# r = r + "Q"
# r = r + "Z"
# r += "S"
# r = r + "B"
# r += "E"
# r = r + "S"
# r = r + "X"
# r = r + "T"
# r = r + "V"
# r += "R"
# r = r + "C"
# r = "A" → 다시 덮어쓰기!
# r = r + "I"
# r = r + "T"
# r = r + "Q"
# r = r + "P"
# r += "1"
# r += "O"
# r += "0"

# 중간에 r = "A"로 덮어쓰기가 있음!
r = "A"
r = r + "I"  # AI
r = r + "T"  # AIT
r = r + "Q"  # AITQ
r = r + "P"  # AITQP
r += "1"     # AITQP1
r += "O"     # AITQP1O
r += "0"     # AITQP1O0

print("최종 r:", r)
print("역순:", r[::-1])
