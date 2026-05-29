from pathlib import Path
import pandas as pd
from .config import CSV_PATH, SUBJECT_COLUMNS, TABLES_DIR, YEAR_MAX, YEAR_MIN, MAIN_SUBJECTS
from .load_data import filter_years, iter_chunks, load_provinces

def _subject_stats(series):
    s = series.dropna()
    s = s[s > 0]
    if s.empty:
        return {"count": 0, "mean": None, "median": None, "std": None, "pct_ge_8": None}
    return {
        "count": int(len(s)),
        "mean": round(float(s.mean()), 4),
        "median": round(float(s.median()), 4),
        "std": round(float(s.std()), 4),
        "pct_ge_8": round(float((s >= 8).mean() * 100), 2),
    }

def build_by_year_subject(path=CSV_PATH, year_min=YEAR_MIN, year_max=YEAR_MAX):
    usecols = ["Nam"] + SUBJECT_COLUMNS
    rows = []
    for chunk in iter_chunks(path, usecols=usecols):
        chunk = filter_years(chunk, year_min, year_max)
        for year, g in chunk.groupby("Nam"):
            for subject in SUBJECT_COLUMNS:
                rows.append({"Nam": int(year), "Mon": subject, **_subject_stats(g[subject])})
    return pd.DataFrame(rows).sort_values(["Nam", "Mon"]).reset_index(drop=True)

def build_by_year_province_subject(path=CSV_PATH, year_min=YEAR_MIN, year_max=YEAR_MAX, subjects=None):
    subjects = subjects or MAIN_SUBJECTS
    usecols = ["Nam", "Tinh"] + subjects
    rows = []
    for chunk in iter_chunks(path, usecols=usecols):
        chunk = filter_years(chunk, year_min, year_max)
        for (year, tinh), g in chunk.groupby(["Nam", "Tinh"]):
            for subject in subjects:
                rows.append({"Nam": int(year), "Tinh": int(tinh), "Mon": subject, **_subject_stats(g[subject])})
    return pd.DataFrame(rows).sort_values(["Nam", "Tinh", "Mon"]).reset_index(drop=True)

def build_candidates_by_year(path=CSV_PATH, year_min=YEAR_MIN, year_max=YEAR_MAX):
    counts = {}
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
