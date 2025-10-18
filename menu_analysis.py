"""
춘식도락 메뉴판 이미지 분석 스크립트
AI_100 대회용 - 카카오 구내식당 메뉴 데이터 추출 및 분석
"""

import os
import json
import re
from datetime import datetime
from typing import List, Dict, Any
from PIL import Image
import pytesseract
import pandas as pd

# OCR 설정 (한글 인식)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows 기본 경로

class MenuAnalyzer:
    """메뉴판 이미지 분석 클래스"""

    def __init__(self, image_dir: str = "menu_images"):
        self.image_dir = image_dir
        self.menu_data = []

        # 코너 정보
        self.lunch_corners = ["한식A", "한식B", "팝업A", "팝업B", "양식", "샐러드바"]
        self.lunch_takeout_corners = ["샐러드", "비건", "버거&델리", "라이스&누들"]
        self.dinner_corners = ["한식B", "샐러드바"]
        self.dinner_takeout_corners = ["샐러드", "버거&델리"]

        # 조리법 키워드
        self.cooking_methods = ["조림", "볶음", "무침", "구이"]

        # 지역명 패턴
        self.regions = ["안동", "전주", "베트남", "나가사키", "태국", "춘천", "제주", "부산", "일본", "중국"]

    def extract_text_from_image(self, image_path: str) -> str:
        """이미지에서 텍스트 추출 (OCR)"""
        try:
            img = Image.open(image_path)
            # 한글+영문 인식
            text = pytesseract.image_to_string(img, lang='kor+eng')
            return text
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return ""

    def parse_menu_text(self, text: str, week_date: str) -> List[Dict]:
        """추출된 텍스트를 파싱하여 구조화된 데이터로 변환"""
        menus = []

        # 날짜, 코너, 메뉴명, 칼로리 등 추출
        # 실제 메뉴판 구조에 맞게 정규식 작성 필요

        return menus

    def extract_calorie(self, text: str) -> int:
        """텍스트에서 칼로리 정보 추출"""
        # 예: "850kcal" -> 850
        match = re.search(r'(\d+)\s*kcal', text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 0

    def analyze_all_images(self):
        """모든 이미지 분석"""
        image_files = sorted([f for f in os.listdir(self.image_dir) if f.endswith('.png')])

        for img_file in image_files:
            # 2025년 1-2월만 분석
            if not (img_file.startswith('2025-01') or img_file.startswith('2025-02')):
                continue

            print(f"Analyzing {img_file}...")
            image_path = os.path.join(self.image_dir, img_file)

            # OCR 수행
            text = self.extract_text_from_image(image_path)

            # 파싱
            week_date = img_file.replace('.png', '')
            parsed_data = self.parse_menu_text(text, week_date)
            self.menu_data.extend(parsed_data)

        # 데이터프레임으로 변환
        self.df = pd.DataFrame(self.menu_data)
        return self.df

    def solve_question_1(self) -> str:
        """
        문제 1: 1월 13일 주간 중식 반찬 조리법 분석
        조림, 볶음, 무침, 구이로 끝나는 반찬 개수를 내림차순 정렬
        """
        # 1/13-1/17 주간 데이터 필터링
        target_week = self.df[
            (self.df['date'] >= '2025-01-13') &
            (self.df['date'] <= '2025-01-17') &
            (self.df['meal_type'] == '중식') &
            (self.df['corner'].isin(self.lunch_corners))
        ]

        # 조리법별 카운트
        cooking_counts = {method: 0 for method in self.cooking_methods}

        for _, row in target_week.iterrows():
            side_dishes = row.get('side_dishes', [])
            for dish in side_dishes:
                for method in self.cooking_methods:
                    if dish.endswith(method):
                        cooking_counts[method] += 1

        # 내림차순 정렬
        sorted_methods = sorted(cooking_counts.items(), key=lambda x: x[1], reverse=True)
        result = ' > '.join([method for method, count in sorted_methods])

        return result

    def solve_question_2(self) -> str:
        """
        문제 2: 1월 전체 중식 코너별 평균 칼로리 분석
        한식A, 한식B, 양식, 팝업A, 팝업B 평균 칼로리를 내림차순 정렬
        """
        # 1월 중식 데이터
        jan_lunch = self.df[
            (self.df['date'].str.startswith('2025-01')) &
            (self.df['meal_type'] == '중식') &
            (self.df['corner'].isin(['한식A', '한식B', '양식', '팝업A', '팝업B']))
        ]

        # 코너별 평균 칼로리
        avg_calories = jan_lunch.groupby('corner')['calories'].mean()
        sorted_corners = avg_calories.sort_values(ascending=False)

        result = ' > '.join(sorted_corners.index.tolist())
        return result

    def solve_question_3(self) -> List[str]:
        """
        문제 3: 1-2월 메뉴명에 포함된 지역명 분석
        2회 이상 등장한 지역명 추출
        """
        # 모든 메뉴명에서 지역명 검색
        region_counts = {region: 0 for region in self.regions}

        for _, row in self.df.iterrows():
            menu_name = row.get('menu_name', '')
            for region in self.regions:
                if region in menu_name:
                    region_counts[region] += 1

        # 2회 이상 등장한 지역
        result = [region for region, count in region_counts.items() if count >= 2]
        return result

    def solve_question_4(self) -> str:
        """
        문제 4: 특정 메뉴 칼로리 비교
        덴가스떡볶이, 돈코츠라멘, 마라탕면, 수제남산왕돈까스, 탄탄면
        """
        target_menus = ["덴가스떡볶이", "돈코츠라멘", "마라탕면", "수제남산왕돈까스", "탄탄면"]

        menu_calories = {}
        for menu in target_menus:
            matching = self.df[self.df['menu_name'].str.contains(menu, na=False)]
            if not matching.empty:
                menu_calories[menu] = matching.iloc[0]['calories']

        # 내림차순 정렬
        sorted_menus = sorted(menu_calories.items(), key=lambda x: x[1], reverse=True)
        result = ' > '.join([menu for menu, cal in sorted_menus])

        return result

    def solve_question_5(self) -> List[Dict]:
        """
        문제 5: 2월 식단 최적화
        월-목: 중식+석식 = 1550kcal에 가장 근접
        금: 가장 낮은 칼로리 중식
        """
        # 2월 데이터 필터링
        feb_data = self.df[self.df['date'].str.startswith('2025-02')]

        result = []

        # 2월 각 날짜별로 처리
        dates = feb_data['date'].unique()

        for date in sorted(dates):
            day_data = feb_data[feb_data['date'] == date]
            weekday = datetime.strptime(date, '%Y-%m-%d').weekday()

            if weekday == 4:  # 금요일 (0=월요일)
                # 중식만, 가장 낮은 칼로리
                lunch_data = day_data[day_data['meal_type'] == '중식']
                if not lunch_data.empty:
                    min_cal_corner = lunch_data.loc[lunch_data['calories'].idxmin(), 'corner']
                    result.append({"id": date, "lunch": min_cal_corner})
            else:
                # 월-목: 중식+석식 = 1550kcal에 근접
                lunch_data = day_data[day_data['meal_type'] == '중식']
                dinner_data = day_data[day_data['meal_type'] == '석식']

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
                                "dinner": dinner['corner']
                            }

                if best_combo:
                    result.append(best_combo)

        return result

    def save_results(self, output_file: str = "menu_analysis_results.json"):
        """분석 결과 저장"""
        results = {
            "question_1": self.solve_question_1(),
            "question_2": self.solve_question_2(),
            "question_3": self.solve_question_3(),
            "question_4": self.solve_question_4(),
            "question_5": self.solve_question_5()
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n결과가 {output_file}에 저장되었습니다.")
        return results


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("춘식도락 메뉴판 이미지 분석 시작")
    print("=" * 60)

    # 분석기 초기화
    analyzer = MenuAnalyzer()

    # 모든 이미지 분석
    print("\n[1단계] 이미지 OCR 및 데이터 추출 중...")
    df = analyzer.analyze_all_images()

    print(f"\n총 {len(df)}개의 메뉴 데이터 추출 완료")
    print(df.head())

    # 문제 풀이
    print("\n[2단계] 문제 풀이 시작...")
    results = analyzer.save_results()

    print("\n" + "=" * 60)
    print("분석 결과")
    print("=" * 60)
    print(json.dumps(results, ensure_ascii=False, indent=2))

    return results


if __name__ == "__main__":
    main()
