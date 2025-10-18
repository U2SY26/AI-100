"""
춘식도락 메뉴 데이터 입력 및 분석 도구
Streamlit 기반 웹 인터페이스
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import List, Dict

# 페이지 설정
st.set_page_config(
    page_title="춘식도락 메뉴 분석",
    page_icon="🍽️",
    layout="wide"
)

# 세션 상태 초기화
if 'menu_data' not in st.session_state:
    st.session_state.menu_data = []

# 코너 정보
LUNCH_CORNERS = ["한식A", "한식B", "팝업A", "팝업B", "양식", "샐러드바"]
LUNCH_TAKEOUT_CORNERS = ["샐러드", "비건", "버거&델리", "라이스&누들"]
DINNER_CORNERS = ["한식B", "샐러드바"]
DINNER_TAKEOUT_CORNERS = ["샐러드", "버거&델리"]

# 조리법 키워드
COOKING_METHODS = ["조림", "볶음", "무침", "구이"]

# 지역명
REGIONS = ["안동", "전주", "베트남", "나가사키", "태국", "춘천", "제주", "부산", "일본", "중국", "이탈리아"]

st.title("🍽️ 춘식도락 메뉴판 분석 도구")
st.markdown("---")

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["📝 데이터 입력", "📊 문제 풀이", "📁 데이터 관리", "ℹ️ 도움말"])

with tab1:
    st.header("메뉴 데이터 입력")

    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("날짜", value=datetime(2025, 1, 6))
        meal_type = st.selectbox("식사 구분", ["중식", "중식(TAKE OUT)", "석식", "석식(TAKE OUT)"])

        # 식사 구분에 따라 코너 선택지 변경
        if meal_type == "중식":
            corner_options = LUNCH_CORNERS
        elif meal_type == "중식(TAKE OUT)":
            corner_options = LUNCH_TAKEOUT_CORNERS
        elif meal_type == "석식":
            corner_options = DINNER_CORNERS
        else:  # 석식(TAKE OUT)
            corner_options = DINNER_TAKEOUT_CORNERS

        corner = st.selectbox("코너", corner_options)

    with col2:
        menu_name = st.text_input("메뉴명", placeholder="예: 통마늘간장제육불고기")
        calories = st.number_input("칼로리 (kcal)", min_value=0, max_value=3000, step=10)

    st.markdown("**반찬 입력** (각 줄에 하나씩)")
    side_dishes_text = st.text_area(
        "반찬",
        placeholder="김치콩나물국\n두부조림\n상추양배추쌈*쌈장\n알타리김치",
        height=100
    )

    if st.button("➕ 메뉴 추가", type="primary"):
        side_dishes = [s.strip() for s in side_dishes_text.split('\n') if s.strip()]

        new_entry = {
            "date": str(date),
            "meal_type": meal_type,
            "corner": corner,
            "menu_name": menu_name,
            "calories": calories,
            "side_dishes": side_dishes
        }

        st.session_state.menu_data.append(new_entry)
        st.success(f"✅ {menu_name} 추가 완료! (총 {len(st.session_state.menu_data)}개)")

    # 현재 저장된 데이터 미리보기
    if st.session_state.menu_data:
        st.markdown("---")
        st.subheader(f"저장된 메뉴 ({len(st.session_state.menu_data)}개)")
        df_preview = pd.DataFrame(st.session_state.menu_data)
        st.dataframe(df_preview[['date', 'meal_type', 'corner', 'menu_name', 'calories']], use_container_width=True)

with tab2:
    st.header("문제 풀이")

    if not st.session_state.menu_data:
        st.warning("⚠️ 먼저 '데이터 입력' 탭에서 메뉴 데이터를 입력해주세요.")
    else:
        df = pd.DataFrame(st.session_state.menu_data)

        st.markdown("### 문제 1: 조리법별 메뉴 분석 (1월 13일 주간)")
        if st.button("문제 1 풀이", key="q1"):
            # 1/13-1/17 주간 데이터 필터링
            target_data = df[
                (df['date'] >= '2025-01-13') &
                (df['date'] <= '2025-01-17') &
                (df['meal_type'] == '중식') &
                (df['corner'].isin(['한식A', '한식B', '팝업A', '팝업B', '양식']))
            ]

            # 조리법별 카운트
            cooking_counts = {method: 0 for method in COOKING_METHODS}

            for _, row in target_data.iterrows():
                for dish in row['side_dishes']:
                    for method in COOKING_METHODS:
                        if dish.endswith(method):
                            cooking_counts[method] += 1

            # 내림차순 정렬
            sorted_methods = sorted(cooking_counts.items(), key=lambda x: x[1], reverse=True)

            st.write("**조리법별 개수:**")
            for method, count in sorted_methods:
                st.write(f"- {method}: {count}개")

            result = ' > '.join([method for method, count in sorted_methods])
            st.success(f"**답: {result}**")

        st.markdown("---")
        st.markdown("### 문제 2: 1월 칼로리 순위 분석")
        if st.button("문제 2 풀이", key="q2"):
            jan_lunch = df[
                (df['date'].str.startswith('2025-01')) &
                (df['meal_type'] == '중식') &
                (df['corner'].isin(['한식A', '한식B', '양식', '팝업A', '팝업B']))
            ]

            if not jan_lunch.empty:
                avg_calories = jan_lunch.groupby('corner')['calories'].mean().round(2)
                sorted_corners = avg_calories.sort_values(ascending=False)

                st.write("**코너별 평균 칼로리:**")
                for corner, cal in sorted_corners.items():
                    st.write(f"- {corner}: {cal}kcal")

                result = ' > '.join(sorted_corners.index.tolist())
                st.success(f"**답: {result}**")
            else:
                st.error("1월 중식 데이터가 없습니다.")

        st.markdown("---")
        st.markdown("### 문제 3: 지역 특색 메뉴")
        if st.button("문제 3 풀이", key="q3"):
            region_counts = {region: 0 for region in REGIONS}

            for _, row in df.iterrows():
                menu_name = row['menu_name']
                for region in REGIONS:
                    if region in menu_name:
                        region_counts[region] += 1

            st.write("**지역명 등장 횟수:**")
            for region, count in sorted(region_counts.items(), key=lambda x: x[1], reverse=True):
                if count > 0:
                    st.write(f"- {region}: {count}회")

            result = [region for region, count in region_counts.items() if count >= 2]
            if result:
                st.success(f"**2회 이상 등장한 지역: {', '.join(result)}**")
            else:
                st.warning("2회 이상 등장한 지역이 없습니다.")

        st.markdown("---")
        st.markdown("### 문제 4: 메뉴별 칼로리 비교")
        if st.button("문제 4 풀이", key="q4"):
            target_menus = ["덴가스떡볶이", "돈코츠라멘", "마라탕면", "수제남산왕돈까스", "탄탄면"]
            menu_calories = {}

            for menu in target_menus:
                matching = df[df['menu_name'].str.contains(menu, na=False)]
                if not matching.empty:
                    menu_calories[menu] = matching.iloc[0]['calories']

            if menu_calories:
                sorted_menus = sorted(menu_calories.items(), key=lambda x: x[1], reverse=True)

                st.write("**메뉴별 칼로리:**")
                for menu, cal in sorted_menus:
                    st.write(f"- {menu}: {cal}kcal")

                result = ' > '.join([menu for menu, cal in sorted_menus])
                st.success(f"**답: {result}**")
            else:
                st.error("해당 메뉴를 찾을 수 없습니다.")

        st.markdown("---")
        st.markdown("### 문제 5: 2월 한 달 식단 최적화")
        if st.button("문제 5 풀이", key="q5"):
            feb_data = df[df['date'].str.startswith('2025-02')]

            if not feb_data.empty:
                result = []
                dates = sorted(feb_data['date'].unique())

                for date in dates:
                    day_data = feb_data[feb_data['date'] == date]
                    weekday = datetime.strptime(date, '%Y-%m-%d').weekday()

                    if weekday == 4:  # 금요일
                        lunch_data = day_data[day_data['meal_type'].str.contains('중식')]
                        if not lunch_data.empty:
                            min_row = lunch_data.loc[lunch_data['calories'].idxmin()]
                            result.append({"id": date, "lunch": min_row['corner']})
                    else:  # 월-목
                        lunch_data = day_data[day_data['meal_type'].str.contains('중식')]
                        dinner_data = day_data[day_data['meal_type'].str.contains('석식')]

                        best_diff = float('inf')
                        best_combo = None

                        for _, lunch in lunch_data.iterrows():
                            for _, dinner in dinner_data.iterrows():
                                total_cal = lunch['calories'] + dinner['calories']
                                diff = abs(total_cal - 1550)

                                if diff < best_diff:
                                    best_diff = diff
                                    best_combo = {
                                        "id": date,
                                        "lunch": lunch['corner'],
                                        "dinner": dinner['corner'],
                                        "total_cal": total_cal
                                    }

                        if best_combo:
                            result.append(best_combo)

                st.json(result, expanded=False)
                st.success(f"✅ {len(result)}일 식단 최적화 완료")
            else:
                st.error("2월 데이터가 없습니다.")

with tab3:
    st.header("데이터 관리")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💾 저장")
        filename = st.text_input("파일명", value="menu_data.json")
        if st.button("JSON 저장"):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(st.session_state.menu_data, f, ensure_ascii=False, indent=2)
            st.success(f"✅ {filename}에 저장 완료")

    with col2:
        st.subheader("📂 불러오기")
        uploaded_file = st.file_uploader("JSON 파일 업로드", type=['json'])
        if uploaded_file is not None:
            data = json.load(uploaded_file)
            st.session_state.menu_data = data
            st.success(f"✅ {len(data)}개 메뉴 데이터 로드 완료")

    st.markdown("---")
    if st.button("🗑️ 모든 데이터 삭제", type="secondary"):
        st.session_state.menu_data = []
        st.warning("모든 데이터가 삭제되었습니다.")

with tab4:
    st.header("도움말")
    st.markdown("""
    ### 사용 방법

    #### 1. 데이터 입력
    - 메뉴판 이미지를 보면서 각 메뉴 정보를 입력합니다
    - 날짜, 식사 구분, 코너, 메뉴명, 칼로리, 반찬을 차례로 입력
    - "메뉴 추가" 버튼으로 저장

    #### 2. 문제 풀이
    - 충분한 데이터 입력 후 각 문제의 "풀이" 버튼 클릭
    - 자동으로 조건에 맞는 답을 계산하여 표시

    #### 3. 데이터 관리
    - JSON 파일로 저장/불러오기 가능
    - 작업 중단 후 다시 이어서 할 수 있음

    ### 주의사항
    - 2025년 1-2월 데이터만 입력
    - 메뉴명과 반찬명은 메뉴판에 기재된 그대로 입력
    - 칼로리는 kcal 단위로 입력
    """)

if __name__ == "__main__":
    pass
