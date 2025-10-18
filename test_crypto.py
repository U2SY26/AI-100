# 샘플 코드에서 Python 로직 추출
# 역순 문자열 생성 로직

r = ""
r += "D"
r = r[::-1]  # 역순
r += "R"
r += "Q"
r = r[::-1]  # 역순
r += "T"
r = r[::-1]  # 역순
r += "C"
r = r[::-1]  # 역순
r = r + "O"
r += "V"
r += "L"
r += "E"
r += "S"
r += "M"

print("고정 문자열:", r)

# 입력 받기
inp = input("입력: ")
print("출력:", r + inp)
