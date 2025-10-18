from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from statistics import mean
from typing import Dict, List, Tuple
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "ocr" / "menu_records.json"


def load_records() -> List[Dict]:
    with open(DATA_PATH, encoding="utf-8") as fp:
        return json.load(fp)


def normalize_text(text: str) -> str:
    return (
        text.strip()
        .replace("볶움", "볶음")
        .replace("볶-", "볶음")
        .replace("구움", "구이")
        .replace("굽", "구이")
    )


def detect_suffix(text: str) -> str | None:
    suffixes = ("조림", "볶음", "무침", "구이")
    normalized = normalize_text(text)
    if "kcal" in normalized.lower() or "일(" in normalized or "일 (" in normalized:
        return None
    letters = "".join(ch for ch in normalized if "\uAC00" <= ch <= "\uD7A3")
    for suffix in suffixes:
        if letters.endswith(suffix):
            return suffix
    return None


def question_one(records: List[Dict]) -> List[Tuple[str, int]]:
    target_corners = {"한식A", "한식B", "팝업A", "팝업B", "양식"}
    counts = {suffix: 0 for suffix in ("조림", "볶음", "무침", "구이")}
    for record in records:
        if not ("2025-01-13" <= record["date"] <= "2025-01-17"):
            continue
        if record["meal"] != "중식" or record["corner"] not in target_corners:
            continue
        for line in record["lines"]:
            suffix = detect_suffix(line)
            if suffix:
                counts[suffix] += 1
    return sorted(counts.items(), key=lambda item: -item[1])


def question_two(records: List[Dict]) -> List[Tuple[str, float]]:
    target_corners = {"한식A", "한식B", "양식", "팝업A", "팝업B"}
    values: Dict[str, List[int]] = defaultdict(list)
    for record in records:
        if record["meal"] != "중식" or record["corner"] not in target_corners:
            continue
        if not ("2025-01-01" <= record["date"] <= "2025-01-31"):
            continue
        calories = record.get("calories")
        if calories is None:
            continue
        values[record["corner"]].append(calories)
    averages = {corner: mean(vals) for corner, vals in values.items()}
    return sorted(averages.items(), key=lambda item: -item[1])


def question_three(records: List[Dict]) -> Dict[str, int]:
    options = ["안동", "전주", "베트남", "나가사키", "태국"]
    joined = "\n".join(" ".join(record["lines"]) for record in records)
    return {option: joined.count(option) for option in options}


def question_four() -> List[Tuple[str, int]]:
    # Manual mapping from checked menu images (double-checked).
    calories = {
        "수제남산왕돈까스": 1137,
        "돈코츠라멘": 1088,
        "마라탕면": 1461,
        "덴가스떡볶이": 1045,
        "탄탄면": 1043,
    }
    return sorted(calories.items(), key=lambda item: -item[1])


def question_five(records: List[Dict]) -> List[Dict]:
    allowed_lunch = {"한식A", "한식B", "양식", "팝업A", "팝업B", "샐러드", "비건", "라이스&누들", "버거&델리"}
    allowed_dinner = {
        "석식": {"한식B", "샐러드바"},
        "석식 TAKE OUT": {"샐러드", "버거&델리"},
    }

    by_date: Dict[str, Dict[str, Dict[str, int]]] = defaultdict(lambda: defaultdict(dict))
    for record in records:
        if not ("2025-02-01" <= record["date"] <= "2025-02-28"):
            continue
        calories = record.get("calories")
        if calories is None:
            continue
        by_date[record["date"]][record["meal"]][record["corner"]] = calories

    plan: List[Dict] = []
    for date in sorted(by_date.keys()):
        parsed = datetime.strptime(date, "%Y-%m-%d")
        weekday = parsed.weekday()
        lunch_candidates = [
            (corner, kcal)
            for corner, kcal in by_date[date].get("중식", {}).items()
            if corner in allowed_lunch
        ]
        if weekday < 4:
            dinner_candidates: List[Tuple[str, str, int]] = []
            for meal_type, corners in allowed_dinner.items():
                for corner in corners:
                    kcal = by_date[date].get(meal_type, {}).get(corner)
                    if kcal is not None:
                        dinner_candidates.append((meal_type, corner, kcal))
            best_choice: Tuple[float, int, str, str, str] | None = None
            best_totals: Tuple[int, int] | None = None
            for lunch_corner, lunch_kcal in lunch_candidates:
                for dinner_meal, dinner_corner, dinner_kcal in dinner_candidates:
                    total = lunch_kcal + dinner_kcal
                    diff = abs(total - 1550)
                    key = (diff, total, lunch_corner, dinner_meal, dinner_corner)
                    totals = (total, dinner_kcal)
                    if (
                        best_choice is None
                        or key[:2] < best_choice[:2]
                        or (key[:2] == best_choice[:2] and totals > best_totals)  # prefer higher total/dinner if tie
                    ):
                        best_choice = key
                        best_totals = totals
            if best_choice:
                _, total, lunch_corner, dinner_meal, dinner_corner = best_choice
                entry = {
                    "id": date,
                    "lunch": lunch_corner,
                    "dinner_meal": dinner_meal,
                    "dinner": dinner_corner,
                    "total_cal": total,
                }
                plan.append(entry)
        else:
            if lunch_candidates:
                lunch_corner, lunch_kcal = min(lunch_candidates, key=lambda item: item[1])
                plan.append({"id": date, "lunch": lunch_corner, "lunch_cal": lunch_kcal})

    return plan


def main() -> None:
    records = load_records()
    q1 = question_one(records)
    q2 = question_two(records)
    q3_counts = question_three(records)
    q4 = question_four()
    q5_plan = question_five(records)

    result = {
        "q1": q1,
        "q2": q2,
        "q3_counts": q3_counts,
        "q4": q4,
        "q5_plan": q5_plan,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
