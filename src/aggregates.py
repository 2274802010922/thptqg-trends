from pathlib import Path

import numpy as np
import pandas as pd

from .config import CSV_PATH, SUBJECT_COLUMNS, TABLES_DIR, YEAR_MAX, YEAR_MIN, MAIN_SUBJECTS
from .load_data import filter_years, iter_chunks, load_provinces


def _new_bucket():
    return {"sum": 0.0, "sum_sq": 0.0, "count": 0, "ge8": 0}


def _finalize_bucket(b):
    if b["count"] == 0:
        return {"count": 0, "mean": None, "median": None, "std": None, "pct_ge_8": None}
    n = b["count"]
    mean = b["sum"] / n
    var = max(b["sum_sq"] / n - mean**2, 0.0)
    return {
        "count": int(n),
        "mean": round(float(mean), 4),
        "median": None,
        "std": round(float(np.sqrt(var)), 4),
        "pct_ge_8": round(float(b["ge8"] / n * 100), 2),
    }


def _add_series(bucket, series):
    s = series.dropna()
    s = s[s > 0]
    if s.empty:
        return
    bucket["sum"] += float(s.sum())
    bucket["sum_sq"] += float((s ** 2).sum())
    bucket["count"] += int(len(s))
    bucket["ge8"] += int((s >= 8).sum())


def build_by_year_subject(path=CSV_PATH, year_min=YEAR_MIN, year_max=YEAR_MAX):
    buckets: dict[tuple[int, str], dict] = {}
    usecols = ["Nam"] + SUBJECT_COLUMNS
    for chunk in iter_chunks(path, usecols=usecols):
        chunk = filter_years(chunk, year_min, year_max)
        for year, g in chunk.groupby("Nam"):
            y = int(year)
            for subject in SUBJECT_COLUMNS:
                key = (y, subject)
                if key not in buckets:
                    buckets[key] = _new_bucket()
                _add_series(buckets[key], g[subject])
    rows = [{"Nam": y, "Mon": m, **_finalize_bucket(b)} for (y, m), b in sorted(buckets.items())]
    return pd.DataFrame(rows)


def build_by_year_province_subject(path=CSV_PATH, year_min=YEAR_MIN, year_max=YEAR_MAX, subjects=None):
    subjects = subjects or MAIN_SUBJECTS
    buckets: dict[tuple[int, int, str], dict] = {}
    usecols = ["Nam", "Tinh"] + subjects
    for chunk in iter_chunks(path, usecols=usecols):
        chunk = filter_years(chunk, year_min, year_max)
        for (year, tinh), g in chunk.groupby(["Nam", "Tinh"]):
            y, t = int(year), int(tinh)
            for subject in subjects:
                key = (y, t, subject)
                if key not in buckets:
                    buckets[key] = _new_bucket()
                _add_series(buckets[key], g[subject])
    rows = [
        {"Nam": y, "Tinh": t, "Mon": m, **_finalize_bucket(b)}
        for (y, t, m), b in sorted(buckets.items())
    ]
    return pd.DataFrame(rows)


def build_candidates_by_year(path=CSV_PATH, year_min=YEAR_MIN, year_max=YEAR_MAX):
    counts: dict[int, int] = {}
    for chunk in iter_chunks(path, usecols=["Nam"]):
        chunk = filter_years(chunk, year_min, year_max)
        for year, n in chunk["Nam"].value_counts().items():
            counts[int(year)] = counts.get(int(year), 0) + int(n)
    return pd.DataFrame([{"Nam": y, "SoThiSinh": c} for y, c in sorted(counts.items())])


def save_aggregates(path=CSV_PATH, out_dir=TABLES_DIR):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    by_ys = build_by_year_subject(path)
    p1 = out_dir / "by_year_subject.csv"
    by_ys.to_csv(p1, index=False)
    paths["by_year_subject"] = p1
    by_yps = build_by_year_province_subject(path)
    p2 = out_dir / "by_year_province_subject.csv"
    by_yps.to_csv(p2, index=False)
    paths["by_year_province_subject"] = p2
    cand = build_candidates_by_year(path)
    p3 = out_dir / "candidates_by_year.csv"
    cand.to_csv(p3, index=False)
    paths["candidates_by_year"] = p3
    provinces = load_provinces()
    named = by_yps.merge(provinces, left_on="Tinh", right_on="MaTinh", how="left")
    p4 = out_dir / "by_year_province_subject_named.csv"
    named.to_csv(p4, index=False)
    paths["by_year_province_subject_named"] = p4
    return paths
