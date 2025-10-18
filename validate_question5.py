"""
문제 5번 답안 검증 스크립트
2월 식단 최적화 답안의 유효성 검사
"""

import json
from datetime import datetime

def validate_question5(answer):
    """
    문제 5번 답안 검증

    검증 항목:
    1. 날짜 개수 (20일)
    2. 날짜 형식 (YYYY-MM-DD)
    3. 2월 날짜만 포함
    4. 금요일은 중식만
    5. 월-목은 중식+석식
    6. 코너명 유효성
    """

    print("=" * 60)
    print("문제 5번 답안 검증")
    print("=" * 60)

    # 유효한 코너명
    valid_lunch_corners = ["한식A", "한식B", "양식", "팝업A", "팝업B",
                           "샐러드", "비건", "라이스&누들", "버거&델리"]
    valid_dinner_corners = ["한식B", "샐러드바", "샐러드", "버거&델리"]

    errors = []
    warnings = []

    # 1. 날짜 개수 확인
    if len(answer) != 20:
        errors.append(f"❌ 날짜 개수 오류: {len(answer)}개 (기대: 20개)")
    else:
        print(f"✅ 날짜 개수: {len(answer)}개")

    # 2. 각 항목 검증
    friday_count = 0
    weekday_count = 0

    for idx, item in enumerate(answer, 1):
        date_str = item.get('id', '')
        lunch = item.get('lunch', '')
        dinner = item.get('dinner', None)

        # 날짜 형식 확인
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')

            # 2월인지 확인
            if date_obj.month != 2:
                errors.append(f"❌ #{idx}: {date_str}은 2월이 아님")
                continue

            # 요일 확인
            weekday = date_obj.weekday()  # 0=월요일, 4=금요일

            if weekday == 4:  # 금요일
                friday_count += 1
                if dinner is not None:
                    errors.append(f"❌ #{idx}: {date_str}(금) - 석식이 있으면 안됨")
                if not lunch:
                    errors.append(f"❌ #{idx}: {date_str}(금) - 중식이 없음")
                elif lunch not in valid_lunch_corners:
                    errors.append(f"❌ #{idx}: {date_str}(금) - 유효하지 않은 중식 코너: {lunch}")
                else:
                    print(f"  ✓ {date_str}(금): 중식={lunch}")

            else:  # 월-목
                weekday_count += 1
                if dinner is None:
                    errors.append(f"❌ #{idx}: {date_str}(월-목) - 석식이 없음")
                if not lunch:
                    errors.append(f"❌ #{idx}: {date_str}(월-목) - 중식이 없음")
                elif lunch not in valid_lunch_corners:
                    errors.append(f"❌ #{idx}: {date_str}(월-목) - 유효하지 않은 중식 코너: {lunch}")

                if dinner and dinner not in valid_dinner_corners:
                    errors.append(f"❌ #{idx}: {date_str}(월-목) - 유효하지 않은 석식 코너: {dinner}")

                if lunch and dinner:
                    print(f"  ✓ {date_str}: 중식={lunch}, 석식={dinner}")

        except ValueError:
            errors.append(f"❌ #{idx}: 잘못된 날짜 형식: {date_str}")

    print(f"\n✅ 금요일: {friday_count}개")
    print(f"✅ 월-목: {weekday_count}개")

    # 결과 출력
    print("\n" + "=" * 60)
    print("검증 결과")
    print("=" * 60)

    if errors:
        print(f"\n❌ 오류 {len(errors)}개 발견:")
        for error in errors:
            print(f"  {error}")

    if warnings:
        print(f"\n⚠️  경고 {len(warnings)}개:")
        for warning in warnings:
            print(f"  {warning}")

    if not errors and not warnings:
        print("\n✅ 모든 검증 통과! 답안이 유효합니다.")

    # 통계
    print("\n" + "=" * 60)
    print("통계")
    print("=" * 60)

    # 중식 코너별 사용 횟수
    lunch_counts = {}
    dinner_counts = {}

    for item in answer:
        lunch = item.get('lunch', '')
        dinner = item.get('dinner', None)

        if lunch:
            lunch_counts[lunch] = lunch_counts.get(lunch, 0) + 1
        if dinner:
            dinner_counts[dinner] = dinner_counts.get(dinner, 0) + 1

    print("\n중식 코너 사용 횟수:")
    for corner, count in sorted(lunch_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {corner}: {count}회")

    print("\n석식 코너 사용 횟수:")
    for corner, count in sorted(dinner_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {corner}: {count}회")

    return len(errors) == 0


# 제공된 답안
answer_json = """
[
  {"id": "2025-02-03", "lunch": "샐러드", "dinner": "한식B"},
  {"id": "2025-02-04", "lunch": "팝업B", "dinner": "샐러드"},
  {"id": "2025-02-05", "lunch": "한식B", "dinner": "샐러드"},
  {"id": "2025-02-06", "lunch": "양식", "dinner": "버거&델리"},
  {"id": "2025-02-07", "lunch": "비건"},
  {"id": "2025-02-10", "lunch": "팝업A", "dinner": "샐러드"},
  {"id": "2025-02-11", "lunch": "한식A", "dinner": "샐러드"},
  {"id": "2025-02-12", "lunch": "팝업A", "dinner": "샐러드"},
  {"id": "2025-02-13", "lunch": "팝업A", "dinner": "샐러드"},
  {"id": "2025-02-14", "lunch": "비건"},
  {"id": "2025-02-17", "lunch": "팝업B", "dinner": "샐러드"},
  {"id": "2025-02-18", "lunch": "양식", "dinner": "샐러드"},
  {"id": "2025-02-19", "lunch": "비건", "dinner": "한식B"},
  {"id": "2025-02-20", "lunch": "양식", "dinner": "샐러드"},
  {"id": "2025-02-21", "lunch": "샐러드"},
  {"id": "2025-02-24", "lunch": "팝업B", "dinner": "샐러드"},
  {"id": "2025-02-25", "lunch": "팝업A", "dinner": "샐러드"},
  {"id": "2025-02-26", "lunch": "샐러드", "dinner": "한식B"},
  {"id": "2025-02-27", "lunch": "팝업A", "dinner": "샐러드"},
  {"id": "2025-02-28", "lunch": "샐러드"}
]
"""

if __name__ == "__main__":
    answer = json.loads(answer_json)
    is_valid = validate_question5(answer)

    if is_valid:
        print("\n🎉 답안이 유효합니다! 제출 가능합니다.")
    else:
        print("\n⚠️  답안을 수정해주세요.")
