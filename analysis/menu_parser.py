from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from statistics import mean
from typing import Dict, Iterable, List, Optional, Tuple

from PIL import Image


@dataclass(frozen=True)
class RowDefinition:
    meal: str
    corner: str
    y: float
    lower: float = 0.0
    upper: float = 0.0


@dataclass
class MenuRecord:
    date: datetime
    meal: str
    corner: str
    lines: List[str]
    calories: Optional[int]


VALID_CORNERS = {
    "한식A",
    "한식B",
    "팝업A",
    "팝업B",
    "양식",
    "샐러드바",
    "샐러드",
    "비건",
    "버거&델리",
    "라이스&누들",
}


def load_entries(json_path: Path) -> Tuple[List[Dict], Image.Image]:
    with json_path.open(encoding="utf-8") as fp:
        raw = json.load(fp)

    entries = []
    for item in raw:
        text = item["text"].strip()
        if not text:
            continue
        x = sum(pt[0] for pt in item["box"]) / 4
        y = sum(pt[1] for pt in item["box"]) / 4
        entries.append({"text": text, "x": x, "y": y, "conf": float(item["conf"])})

    image_path = json_path.with_suffix(".png").name
    image = Image.open(json_path.parent.parent / "menu_images" / image_path)
    return entries, image


def cluster_day_centers(xs: Iterable[float], k: int = 5, iterations: int = 12) -> List[float]:
    xs = [x for x in xs if x > 150]
    if not xs:
        raise ValueError("No x positions available to cluster day centers.")

    xs.sort()
    min_x, max_x = xs[0], xs[-1]
    centers = [min_x + (i + 0.5) * (max_x - min_x) / k for i in range(k)]

    for _ in range(iterations):
        clusters = [[] for _ in range(k)]
        for x in xs:
            idx = min(range(k), key=lambda j: abs(x - centers[j]))
            clusters[idx].append(x)
        for idx, cluster in enumerate(clusters):
            if cluster:
                centers[idx] = mean(cluster)

    centers.sort()
    return centers


def combine_row_labels(row_entries: List[Dict]) -> List[Dict]:
    combined: List[Dict] = []
    for entry in sorted(row_entries, key=lambda item: item["y"]):
        if combined and abs(entry["y"] - combined[-1]["y"]) < 18:
            combined[-1]["text"] += entry["text"]
            combined[-1]["y"] = (combined[-1]["y"] + entry["y"]) / 2
        else:
            combined.append({"text": entry["text"], "y": entry["y"]})
    return combined


def normalize_label(text: str) -> str:
    cleaned = text.replace(" ", "")
    cleaned = cleaned.replace("판업", "팝업")
    cleaned = cleaned.replace("설러드", "샐러드")
    cleaned = cleaned.replace("실러드", "샐러드")
    cleaned = cleaned.replace("밀리", "델리")
    cleaned = cleaned.replace("노들", "누들")
    cleaned = cleaned.replace("원", "월")
    cleaned = cleaned.replace("꽉", "깍")
    cleaned = cleaned.replace("석쇠", "석식")
    cleaned = cleaned.replace("중식", "")
    cleaned = cleaned.replace("석식", "석식")
    cleaned = cleaned.replace("TAKEOUT", "")
    cleaned = cleaned.replace("TAKE", "")
    cleaned = cleaned.replace("OUT", "")
    cleaned = cleaned.replace("한주의식탁", "")
    return cleaned


def determine_row(label: str, y: float) -> Optional[Tuple[str, str]]:
    if label not in VALID_CORNERS:
        if label == "한식B석식":
            label = "한식B"
        elif label == "샐러드바석식":
            label = "샐러드바"
        else:
            return None

    if label == "한식B":
        meal = "중식" if y < 800 else "석식"
    elif label == "샐러드바":
        meal = "중식" if y < 900 else "석식"
    elif label in {"샐러드", "비건", "버거&델리", "라이스&누들"}:
        meal = "중식 TAKE OUT" if y < 900 else "석식 TAKE OUT"
    elif label in {"한식A", "팝업A", "팝업B", "양식"}:
        meal = "중식"
    else:
        return None

    return meal, label


def build_rows(entries: List[Dict]) -> List[RowDefinition]:
    row_entries = [entry for entry in entries if entry["x"] < 150]
    combined = combine_row_labels(row_entries)

    rows: List[RowDefinition] = []
    for item in combined:
        normalized = normalize_label(item["text"])
        if not normalized:
            continue
        meal_corner = determine_row(normalized, item["y"])
        if not meal_corner:
            continue
        meal, corner = meal_corner
        rows.append(RowDefinition(meal=meal, corner=corner, y=item["y"]))

    rows.sort(key=lambda row: row.y)
    return rows


def assign_row_bounds(rows: List[RowDefinition], image_height: int) -> List[RowDefinition]:
    bounded: List[RowDefinition] = []
    for index, row in enumerate(rows):
        lower = (rows[index - 1].y + row.y) / 2 if index > 0 else 0.0
        upper = (row.y + rows[index + 1].y) / 2 if index + 1 < len(rows) else float(image_height)
        bounded.append(RowDefinition(meal=row.meal, corner=row.corner, y=row.y, lower=lower, upper=upper))
    return bounded


def parse_calories(lines: List[str]) -> Optional[int]:
    replacements = {
        "o": "0",
        "O": "0",
        "l": "1",
        "I": "1",
        "i": "1",
        "g": "9",
        "G": "9",
        "q": "9",
        "b": "6",
        "B": "8",
        "s": "5",
        "S": "5",
        "z": "2",
        "Z": "2",
    }

    for text in reversed(lines):
        lowered = text.lower()
        if "kcal" not in lowered and "kca" not in lowered:
            continue

        cleaned = (
            lowered.replace(" ", "")
            .replace("kcal", "k")
            .replace("kca", "k")
        )

        for src, dst in replacements.items():
            cleaned = cleaned.replace(src, dst)

        k_index = cleaned.rfind("k")
        if k_index == -1:
            continue
        prefix = cleaned[:k_index]
        digits = "".join(ch for ch in prefix if ch.isdigit())
        if not digits:
            continue
        try:
            value = int(digits)
        except ValueError:
            continue
        if 10 <= value <= 5000:
            return value
    return None


def extract_records(json_path: Path) -> List[MenuRecord]:
    entries, image = load_entries(json_path)
    width, height = image.size

    day_reference = json_path.stem
    monday = datetime.strptime(day_reference, "%Y-%m-%d")
    dates = [monday + timedelta(days=offset) for offset in range(5)]

    kcal_xs = [entry["x"] for entry in entries if "kcal" in entry["text"] and entry["x"] > 150]
    centers = cluster_day_centers(kcal_xs)

    def assign_day(x: float) -> int:
        return min(range(len(centers)), key=lambda idx: abs(x - centers[idx]))

    rows = assign_row_bounds(build_rows(entries), height)

    def find_row(entry: Dict) -> Optional[RowDefinition]:
        y = entry["y"]
        if "kcal" in entry["text"].lower():
            y -= 10.0

        margin = 12.0
        primary = [candidate for candidate in rows if candidate.lower <= y < candidate.upper]
        if primary:
            return primary[0]

        candidates = [
            candidate
            for candidate in rows
            if candidate.lower - margin <= y <= candidate.upper + margin
        ]
        if not candidates:
            return None

        def score(row: RowDefinition) -> Tuple[int, float]:
            above = 0 if y >= row.y else 1
            return (above, abs(y - row.y))

        candidates.sort(key=score)
        return candidates[0]

    records_map: Dict[Tuple[int, str, str], List[Dict]] = defaultdict(list)

    for entry in entries:
        if entry["x"] <= 150:
            continue
        row = find_row(entry)
        if not row:
            continue
        day_idx = assign_day(entry["x"])
        records_map[(day_idx, row.meal, row.corner)].append(entry)

    records: List[MenuRecord] = []
    for (day_idx, meal, corner), group in records_map.items():
        sorted_group = sorted(group, key=lambda item: (item["y"], item["x"]))
        lines = [item["text"].strip() for item in sorted_group if item["text"].strip()]
        calories = parse_calories(lines)
        records.append(
            MenuRecord(
                date=dates[day_idx],
                meal=meal,
                corner=corner,
                lines=lines,
                calories=calories,
            )
        )

    return records


def collect_all_records(ocr_dir: Path) -> List[MenuRecord]:
    records: List[MenuRecord] = []
    for json_path in sorted(ocr_dir.glob("2025-*.json")):
        if json_path.stem < "2025-01-01" or json_path.stem > "2025-02-28":
            continue
        records.extend(extract_records(json_path))
    return records


def serialize_records(records: Iterable[MenuRecord], output_path: Path) -> None:
    serializable = [
        {
            "date": record.date.strftime("%Y-%m-%d"),
            "meal": record.meal,
            "corner": record.corner,
            "lines": record.lines,
            "calories": record.calories,
        }
        for record in records
    ]
    with output_path.open("w", encoding="utf-8") as fp:
        json.dump(serializable, fp, ensure_ascii=False, indent=2)


def main() -> None:
    ocr_dir = Path("ocr")
    output_path = Path("ocr") / "menu_records.json"
    records = collect_all_records(ocr_dir)
    serialize_records(records, output_path)


if __name__ == "__main__":
    main()
