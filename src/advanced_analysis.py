"""Cac buoc phan tich DA nang cao: quality, distribution, region, anomaly, correlation."""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from .config import (
    COMBINATION_COLUMNS,
    CSV_PATH,
    DATA_DIR,
    DOCS_DIR,
    MAIN_SUBJECTS,
    SUBJECT_COLUMNS,
    TABLES_DIR,
    YEAR_MAX,
    YEAR_MIN,
)
from .load_data import filter_years, iter_chunks, load_provinces


REGIONS_CSV = DATA_DIR / "province_regions.csv"
CORRELATION_SUBJECTS = [
    "Toan",
    "NguVan",
    "NgoaiNgu",
    "VatLy",
    "HoaHoc",
    "SinhHoc",
    "LichSu",
    "DiaLy",
    "GDCD",
]


def _bucket():
    return {"sum": 0.0, "sum_sq": 0.0, "count": 0, "ge_high": 0, "lt_low": 0}


def _quality_bucket():
    return {
        "total_rows": 0,
        "missing_count": 0,
        "zero_count": 0,
        "invalid_count": 0,
        "valid_score_count": 0,
    }


def _corr_bucket():
    return {"n": 0, "sum_x": 0.0, "sum_y": 0.0, "sum_x2": 0.0, "sum_y2": 0.0, "sum_xy": 0.0}


def _add_series_stats(bucket: dict, values: pd.Series, high_threshold: float, low_threshold: float):
    s = values.dropna()
    s = s[s > 0]
    if s.empty:
        return
    bucket["sum"] += float(s.sum())
    bucket["sum_sq"] += float((s**2).sum())
    bucket["count"] += int(len(s))
    bucket["ge_high"] += int((s >= high_threshold).sum())
    bucket["lt_low"] += int((s < low_threshold).sum())


def _weighted_percentile(scores: np.ndarray, counts: np.ndarray, percentile: float) -> float | None:
    total = int(counts.sum())
    if total <= 0:
        return None
    order = np.argsort(scores)
    scores = scores[order]
    counts = counts[order]
    threshold = percentile / 100.0 * total
    idx = int(np.searchsorted(np.cumsum(counts), threshold, side="left"))
    idx = min(max(idx, 0), len(scores) - 1)
    return round(float(scores[idx]), 4)


def _distribution_from_hist(hist: dict[tuple[int, str, float], int]) -> pd.DataFrame:
    grouped: dict[tuple[int, str], list[tuple[float, int]]] = defaultdict(list)
    for (year, subject, score), count in hist.items():
        grouped[(year, subject)].append((float(score), int(count)))

    rows = []
    for (year, subject), items in sorted(grouped.items()):
        scores = np.array([x[0] for x in items], dtype=float)
        counts = np.array([x[1] for x in items], dtype=int)
        n = int(counts.sum())
        if n == 0:
            continue
        mean = float(np.average(scores, weights=counts))
        var = max(float(np.average((scores - mean) ** 2, weights=counts)), 0.0)
        rows.append(
            {
                "Nam": int(year),
                "Mon": subject,
                "count": n,
                "mean_from_distribution": round(mean, 4),
                "std_from_distribution": round(float(np.sqrt(var)), 4),
                "min_score": round(float(scores.min()), 4),
                "p10": _weighted_percentile(scores, counts, 10),
                "p25": _weighted_percentile(scores, counts, 25),
                "median": _weighted_percentile(scores, counts, 50),
                "p75": _weighted_percentile(scores, counts, 75),
                "p90": _weighted_percentile(scores, counts, 90),
                "max_score": round(float(scores.max()), 4),
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["iqr"] = (out["p75"] - out["p25"]).round(4)
    return out


def _score_bands_from_hist(hist: dict[tuple[int, str, float], int]) -> pd.DataFrame:
    buckets: dict[tuple[int, str], dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for (year, subject, score), count in hist.items():
        score = float(score)
        if score < 5:
            band = "lt_5"
        elif score < 6.5:
            band = "5_to_6_5"
        elif score < 8:
            band = "6_5_to_8"
        else:
            band = "ge_8"
        buckets[(year, subject)][band] += int(count)

    rows = []
    for (year, subject), b in sorted(buckets.items()):
        total = sum(b.values())
        row = {"Nam": int(year), "Mon": subject, "count": int(total)}
        for band in ["lt_5", "5_to_6_5", "6_5_to_8", "ge_8"]:
            c = int(b.get(band, 0))
            row[f"count_{band}"] = c
            row[f"pct_{band}"] = round(c / total * 100, 4) if total else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def _quality_to_frame(quality: dict[tuple[int, str], dict]) -> pd.DataFrame:
    rows = []
    for (year, subject), q in sorted(quality.items()):
        total = int(q["total_rows"])
        row = {"Nam": int(year), "Mon": subject, **q}
        for col in ["missing_count", "zero_count", "invalid_count", "valid_score_count"]:
            row[col.replace("_count", "_pct")] = round(q[col] / total * 100, 4) if total else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def _data_quality_summary(
    missing: pd.DataFrame,
    duplicate_sbd_year_count: int,
    total_rows: int,
    province_year_counts: dict[tuple[int, int], int],
) -> pd.DataFrame:
    invalid = int(missing["invalid_count"].sum()) if not missing.empty else 0
    missing_cells = int(missing["missing_count"].sum()) if not missing.empty else 0
    zero_cells = int(missing["zero_count"].sum()) if not missing.empty else 0
    province_count = len({t for (_, t) in province_year_counts})
    rows = [
        {
            "metric": "filtered_rows",
            "value": total_rows,
            "note": f"Số dòng trong phạm vi {YEAR_MIN}-{YEAR_MAX}.",
        },
        {"metric": "province_count", "value": province_count, "note": "Số tỉnh/thành xuất hiện trong dữ liệu."},
        {
            "metric": "duplicate_sbd_year_count",
            "value": duplicate_sbd_year_count,
            "note": "Số dòng trùng khóa Nam + SBD, dùng để kiểm tra chất lượng dữ liệu.",
        },
        {"metric": "missing_score_cells", "value": missing_cells, "note": "Số ô điểm bị thiếu/null."},
        {"metric": "zero_score_cells", "value": zero_cells, "note": "Số ô điểm bằng 0.0; trong đồ án được hiểu là không thi môn."},
        {"metric": "invalid_score_cells", "value": invalid, "note": "Số ô điểm ngoài khoảng hợp lệ 0-10."},
    ]
    return pd.DataFrame(rows)


def _update_by_year_subject_with_distribution(tables_dir: Path, distribution: pd.DataFrame) -> None:
    path = tables_dir / "by_year_subject.csv"
    if not path.exists() or distribution.empty:
        return
    by = pd.read_csv(path)
    extra_cols = ["median", "p10", "p25", "p75", "p90", "iqr", "min_score", "max_score"]
    by = by.drop(columns=[c for c in extra_cols if c in by.columns and c != "median"], errors="ignore")
    by = by.drop(columns=["median"], errors="ignore")
    dist = distribution[["Nam", "Mon", *extra_cols]].copy()
    out = by.merge(dist, on=["Nam", "Mon"], how="left")
    ordered = ["Nam", "Mon", "count", "mean", "median", "std", "pct_ge_8", "p10", "p25", "p75", "p90", "iqr", "min_score", "max_score"]
    out = out[[c for c in ordered if c in out.columns] + [c for c in out.columns if c not in ordered]]
    out.to_csv(path, index=False)


def _build_yearly_changes(tables_dir: Path, bands: pd.DataFrame) -> pd.DataFrame:
    by = pd.read_csv(tables_dir / "by_year_subject.csv")
    band_cols = ["Nam", "Mon", "pct_lt_5", "pct_5_to_6_5", "pct_6_5_to_8", "pct_ge_8"]
    band_view = bands[[c for c in band_cols if c in bands.columns]].copy()
    band_view = band_view.rename(columns={"pct_ge_8": "pct_ge_8_band"})
    df = by.merge(band_view, on=["Nam", "Mon"], how="left").sort_values(["Mon", "Nam"])
    rows = []
    for subject, g in df.groupby("Mon", sort=False):
        g = g.sort_values("Nam")
        prev = None
        for _, r in g.iterrows():
            row = {"Nam": int(r["Nam"]), "Mon": subject}
            if prev is None or pd.isna(r.get("mean")) or pd.isna(prev.get("mean")):
                row.update(
                    {
                        "mean_prev": np.nan,
                        "mean_change": np.nan,
                        "mean_change_pct": np.nan,
                        "median_change": np.nan,
                        "pct_lt_5_change": np.nan,
                        "pct_ge_8_change": np.nan,
                        "count_change_pct": np.nan,
                    }
                )
            else:
                row["mean_prev"] = float(prev["mean"])
                row["mean_change"] = round(float(r["mean"] - prev["mean"]), 4)
                row["mean_change_pct"] = round(float((r["mean"] - prev["mean"]) / prev["mean"] * 100), 4) if prev["mean"] else np.nan
                row["median_change"] = round(float(r.get("median", np.nan) - prev.get("median", np.nan)), 4)
                row["pct_lt_5_change"] = round(float(r.get("pct_lt_5", np.nan) - prev.get("pct_lt_5", np.nan)), 4)
                row["pct_ge_8_change"] = round(float(r.get("pct_ge_8", np.nan) - prev.get("pct_ge_8", np.nan)), 4)
                row["count_change_pct"] = round(float((r["count"] - prev["count"]) / prev["count"] * 100), 4) if prev["count"] else np.nan
            row["mean"] = r.get("mean")
            row["median"] = r.get("median")
            row["count"] = r.get("count")
            row["pct_lt_5"] = r.get("pct_lt_5")
            row["pct_ge_8"] = r.get("pct_ge_8")
            rows.append(row)
            prev = r
    return pd.DataFrame(rows)


def _build_region_tables(tables_dir: Path) -> pd.DataFrame:
    named_path = tables_dir / "by_year_province_subject_named.csv"
    if not named_path.exists() or not REGIONS_CSV.exists():
        return pd.DataFrame()
    named = pd.read_csv(named_path)
    regions = pd.read_csv(REGIONS_CSV)
    df = named.merge(regions[["MaTinh", "Vung"]], left_on="Tinh", right_on="MaTinh", how="left")
    df = df.dropna(subset=["Vung", "mean", "count"])
    df = df[df["count"] > 0].copy()
    if df.empty:
        return pd.DataFrame()
    df["score_sum"] = df["mean"] * df["count"]
    df["ge8_est"] = df["pct_ge_8"].fillna(0) / 100 * df["count"]
    rows = []
    for (year, region, subject), g in df.groupby(["Nam", "Vung", "Mon"]):
        count = int(g["count"].sum())
        rows.append(
            {
                "Nam": int(year),
                "Vung": region,
                "Mon": subject,
                "count": count,
                "mean": round(float(g["score_sum"].sum() / count), 4) if count else np.nan,
                "pct_ge_8": round(float(g["ge8_est"].sum() / count * 100), 4) if count else np.nan,
                "province_count": int(g["Tinh"].nunique()),
                "min_province_mean": round(float(g["mean"].min()), 4),
                "max_province_mean": round(float(g["mean"].max()), 4),
            }
        )
    return pd.DataFrame(rows)


def _build_province_anomalies(tables_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    named_path = tables_dir / "by_year_province_subject_named.csv"
    national_path = tables_dir / "by_year_subject.csv"
    if not named_path.exists() or not national_path.exists():
        return pd.DataFrame(), pd.DataFrame()
    province = pd.read_csv(named_path).dropna(subset=["mean"])
    national = pd.read_csv(national_path)[["Nam", "Mon", "mean"]].rename(columns={"mean": "national_mean"})
    df = province.merge(national, on=["Nam", "Mon"], how="left")
    df = df[df["count"] >= 500].copy()
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    df["delta_from_national"] = (df["mean"] - df["national_mean"]).round(4)
    df["province_mean_std"] = df.groupby(["Nam", "Mon"])["mean"].transform("std")
    df["z_score"] = (df["delta_from_national"] / df["province_mean_std"]).replace([np.inf, -np.inf], np.nan).round(4)
    anomalies = df[(df["z_score"].abs() >= 2.0) | (df["delta_from_national"].abs() >= 0.8)].copy()
    anomalies["severity"] = anomalies["z_score"].abs().fillna(0) + anomalies["delta_from_national"].abs().fillna(0)
    anomalies = anomalies.sort_values(["severity", "Nam"], ascending=[False, False])[
        ["Nam", "Tinh", "TenTinh", "Mon", "count", "mean", "national_mean", "delta_from_national", "z_score", "severity"]
    ]

    rows = []
    for (province_code, subject), g in df.groupby(["Tinh", "Mon"]):
        g = g.sort_values("Nam")
        if len(g) < 3:
            continue
        deltas = g["mean"].diff().abs().dropna()
        first, last = g.iloc[0], g.iloc[-1]
        rows.append(
            {
                "Tinh": int(province_code),
                "TenTinh": last["TenTinh"],
                "Mon": subject,
                "n_years": int(len(g)),
                "mean_first": round(float(first["mean"]), 4),
                "mean_last": round(float(last["mean"]), 4),
                "change": round(float(last["mean"] - first["mean"]), 4),
                "volatility_std": round(float(g["mean"].std()), 4),
                "max_yoy_abs_change": round(float(deltas.max()), 4) if not deltas.empty else 0.0,
                "latest_count": int(last["count"]),
            }
        )
    volatility = pd.DataFrame(rows)
    if not volatility.empty:
        volatility = volatility.sort_values(["max_yoy_abs_change", "volatility_std"], ascending=False)
    return anomalies, volatility


def _build_subject_year_anomalies(yearly: pd.DataFrame) -> pd.DataFrame:
    df = yearly.dropna(subset=["mean_change_pct"]).copy()
    if df.empty:
        return df
    df["severity"] = (
        df["mean_change_pct"].abs().fillna(0)
        + df["pct_lt_5_change"].abs().fillna(0) * 0.5
        + df["pct_ge_8_change"].abs().fillna(0) * 0.5
    )
    out = df[
        (df["mean_change_pct"].abs() >= 8)
        | (df["pct_lt_5_change"].abs() >= 5)
        | (df["pct_ge_8_change"].abs() >= 5)
    ].copy()
    return out.sort_values(["severity", "Nam"], ascending=[False, False])


def _corr_to_frame(corr_stats: dict[tuple[int, str, str], dict]) -> pd.DataFrame:
    rows = []
    for (year, sx, sy), b in sorted(corr_stats.items()):
        n = int(b["n"])
        if n < 2:
            corr = np.nan
        else:
            numerator = n * b["sum_xy"] - b["sum_x"] * b["sum_y"]
            den_x = n * b["sum_x2"] - b["sum_x"] ** 2
            den_y = n * b["sum_y2"] - b["sum_y"] ** 2
            corr = numerator / np.sqrt(den_x * den_y) if den_x > 0 and den_y > 0 else np.nan
        rows.append({"Nam": int(year), "MonX": sx, "MonY": sy, "n_pair": n, "correlation": round(float(corr), 4) if pd.notna(corr) else np.nan})
    return pd.DataFrame(rows)


def generate_da_tables(path=CSV_PATH, tables_dir=TABLES_DIR) -> dict[str, Path]:
    """Sinh cac bang phan tich DA nang cao tu raw CSV."""
    tables_dir = Path(tables_dir)
    tables_dir.mkdir(parents=True, exist_ok=True)

    quality: dict[tuple[int, str], dict] = defaultdict(_quality_bucket)
    hist: dict[tuple[int, str, float], int] = defaultdict(int)
    combo_stats: dict[tuple[int, str], dict] = defaultdict(_bucket)
    corr_stats: dict[tuple[int, str, str], dict] = defaultdict(_corr_bucket)
    province_year_counts: dict[tuple[int, int], int] = defaultdict(int)
    seen_sbd_year: set[int] = set()
    duplicate_sbd_year_count = 0
    total_rows = 0

    usecols = ["SBD", "Nam", "Tinh", *SUBJECT_COLUMNS, *COMBINATION_COLUMNS]
    for chunk in iter_chunks(path, usecols=usecols):
        chunk = filter_years(chunk, YEAR_MIN, YEAR_MAX)
        if chunk.empty:
            continue
        total_rows += int(len(chunk))

        for (year, province), n in chunk.groupby(["Nam", "Tinh"]).size().items():
            province_year_counts[(int(year), int(province))] += int(n)

        key_df = chunk[["Nam", "SBD"]].dropna()
        if not key_df.empty:
            hashes = pd.util.hash_pandas_object(key_df.astype(str), index=False).to_numpy(dtype=np.uint64)
            for h in hashes:
                key = int(h)
                if key in seen_sbd_year:
                    duplicate_sbd_year_count += 1
                else:
                    seen_sbd_year.add(key)

        for subject in SUBJECT_COLUMNS:
            gdf = chunk[["Nam", subject]]
            for year, g in gdf.groupby("Nam"):
                s = g[subject]
                q = quality[(int(year), subject)]
                q["total_rows"] += int(len(s))
                q["missing_count"] += int(s.isna().sum())
                q["zero_count"] += int((s == 0).sum())
                q["invalid_count"] += int(((s < 0) | (s > 10)).sum())
                q["valid_score_count"] += int(((s > 0) & (s <= 10)).sum())

            valid = gdf[(gdf[subject] > 0) & (gdf[subject] <= 10)].dropna().copy()
            if not valid.empty:
                valid[subject] = valid[subject].round(2)
                for (year, score), n in valid.groupby(["Nam", subject]).size().items():
                    hist[(int(year), subject, float(score))] += int(n)

        for combo in COMBINATION_COLUMNS:
            gdf = chunk[["Nam", combo]]
            valid = gdf[(gdf[combo] > 0) & (gdf[combo] <= 30)]
            if valid.empty:
                continue
            for year, g in valid.groupby("Nam"):
                _add_series_stats(combo_stats[(int(year), combo)], g[combo], high_threshold=24, low_threshold=15)

        corr_subjects = [s for s in CORRELATION_SUBJECTS if s in chunk.columns]
        for year, g in chunk.groupby("Nam"):
            y = int(year)
            for sx, sy in combinations(corr_subjects, 2):
                pair = g[[sx, sy]].dropna()
                pair = pair[(pair[sx] > 0) & (pair[sx] <= 10) & (pair[sy] > 0) & (pair[sy] <= 10)]
                if len(pair) < 2:
                    continue
                x = pair[sx].to_numpy(dtype=float)
                yv = pair[sy].to_numpy(dtype=float)
                b = corr_stats[(y, sx, sy)]
                b["n"] += int(len(pair))
                b["sum_x"] += float(x.sum())
                b["sum_y"] += float(yv.sum())
                b["sum_x2"] += float((x**2).sum())
                b["sum_y2"] += float((yv**2).sum())
                b["sum_xy"] += float((x * yv).sum())

    paths: dict[str, Path] = {}

    missing = _quality_to_frame(quality)
    p = tables_dir / "missing_by_subject_year.csv"
    missing.to_csv(p, index=False)
    paths["missing_by_subject_year"] = p

    summary = _data_quality_summary(missing, duplicate_sbd_year_count, total_rows, province_year_counts)
    p = tables_dir / "data_quality_summary.csv"
    summary.to_csv(p, index=False)
    paths["data_quality_summary"] = p

    province_counts = pd.DataFrame(
        [{"Nam": y, "Tinh": t, "row_count": n} for (y, t), n in sorted(province_year_counts.items())]
    )
    p = tables_dir / "province_year_counts.csv"
    province_counts.to_csv(p, index=False)
    paths["province_year_counts"] = p

    hist_df = pd.DataFrame(
        [{"Nam": y, "Mon": m, "score": s, "count": n} for (y, m, s), n in sorted(hist.items())]
    )
    p = tables_dir / "score_histogram_by_year_subject.csv"
    hist_df.to_csv(p, index=False)
    paths["score_histogram_by_year_subject"] = p

    distribution = _distribution_from_hist(hist)
    p = tables_dir / "score_distribution_by_year_subject.csv"
    distribution.to_csv(p, index=False)
    paths["score_distribution_by_year_subject"] = p
    _update_by_year_subject_with_distribution(tables_dir, distribution)

    bands = _score_bands_from_hist(hist)
    p = tables_dir / "score_bands_by_year_subject.csv"
    bands.to_csv(p, index=False)
    paths["score_bands_by_year_subject"] = p

    yearly = _build_yearly_changes(tables_dir, bands)
    p = tables_dir / "yearly_change_by_subject.csv"
    yearly.to_csv(p, index=False)
    paths["yearly_change_by_subject"] = p

    regions = _build_region_tables(tables_dir)
    p = tables_dir / "by_region_subject_year.csv"
    regions.to_csv(p, index=False)
    paths["by_region_subject_year"] = p

    province_anomalies, province_volatility = _build_province_anomalies(tables_dir)
    p = tables_dir / "province_anomalies.csv"
    province_anomalies.to_csv(p, index=False)
    paths["province_anomalies"] = p
    p = tables_dir / "province_volatility.csv"
    province_volatility.to_csv(p, index=False)
    paths["province_volatility"] = p

    subject_anomalies = _build_subject_year_anomalies(yearly)
    p = tables_dir / "anomaly_subject_year.csv"
    subject_anomalies.to_csv(p, index=False)
    paths["anomaly_subject_year"] = p

    corr = _corr_to_frame(corr_stats)
    p = tables_dir / "subject_correlation_by_year.csv"
    corr.to_csv(p, index=False)
    paths["subject_correlation_by_year"] = p

    combo_rows = []
    for (year, combo), b in sorted(combo_stats.items()):
        n = int(b["count"])
        mean = b["sum"] / n if n else np.nan
        var = max(b["sum_sq"] / n - mean**2, 0.0) if n else np.nan
        combo_rows.append(
            {
                "Nam": int(year),
                "ToHop": combo,
                "count": n,
                "mean": round(float(mean), 4) if n else np.nan,
                "std": round(float(np.sqrt(var)), 4) if n else np.nan,
                "pct_ge_24": round(float(b["ge_high"] / n * 100), 4) if n else np.nan,
                "pct_lt_15": round(float(b["lt_low"] / n * 100), 4) if n else np.nan,
            }
        )
    combo = pd.DataFrame(combo_rows)
    p = tables_dir / "combination_scores_by_year.csv"
    combo.to_csv(p, index=False)
    paths["combination_scores_by_year"] = p

    return paths


def build_forecast_reliability(tables_dir=TABLES_DIR) -> Path:
    """Gan nhan do tin cay cho forecast dua tren sai so va do rong khoang du bao."""
    tables_dir = Path(tables_dir)
    forecast_path = tables_dir / "forecast_next_year.csv"
    out_path = tables_dir / "forecast_reliability.csv"
    if not forecast_path.exists():
        pd.DataFrame().to_csv(out_path, index=False)
        return out_path

    forecast = pd.read_csv(forecast_path)
    rows = []
    for _, r in forecast.iterrows():
        mae = float(r["backtest_mae"]) if pd.notna(r.get("backtest_mae")) else np.nan
        rmse = float(r["backtest_rmse"]) if pd.notna(r.get("backtest_rmse")) else np.nan
        mape = float(r["backtest_mape"]) if pd.notna(r.get("backtest_mape")) else np.nan
        n = int(r.get("backtest_n", 0))
        width = (
            float(r["forecast_upper"] - r["forecast_lower"])
            if pd.notna(r.get("forecast_upper")) and pd.notna(r.get("forecast_lower"))
            else np.nan
        )

        if n < 2 or (pd.notna(mae) and mae > 0.6) or (pd.notna(width) and width > 1.6) or (pd.notna(mape) and mape > 10):
            label = "Thấp"
        elif pd.notna(mae) and mae <= 0.2 and pd.notna(width) and width <= 0.8:
            label = "Tương đối"
        else:
            label = "Trung bình"

        reasons = []
        if n < 3:
            reasons.append("chỉ có 2 điểm backtest do chuỗi 5 năm")
        if pd.notna(mae):
            reasons.append(f"MAE={mae:.4f}")
        if pd.notna(width):
            reasons.append(f"khoảng dự báo rộng {width:.3f} điểm")
        if pd.notna(mape):
            reasons.append(f"MAPE={mape:.2f}%")

        rows.append(
            {
                "Mon": r["Mon"],
                "forecast_year": int(r["forecast_year"]),
                "forecast_mean": r["forecast_mean"],
                "selected_model": r["selected_model"],
                "selected_model_label": r["selected_model_label"],
                "backtest_n": n,
                "backtest_mae": mae,
                "backtest_rmse": rmse,
                "backtest_mape": mape,
                "interval_width": round(width, 4) if pd.notna(width) else np.nan,
                "reliability_label": label,
                "reliability_note": "; ".join(reasons),
            }
        )

    out = pd.DataFrame(rows)
    out.to_csv(out_path, index=False)
    return out_path


def write_analysis_questions(out_path: Path | None = None) -> Path:
    out_path = out_path or Path(DOCS_DIR) / "analysis_questions.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    text = f"""# Analytical Questions & Hypotheses

Tài liệu này khóa lại hướng phân tích để project không dừng ở việc đọc số liệu.

## Câu hỏi chính

1. Quy mô thí sinh thay đổi thế nào trong giai đoạn {YEAR_MIN}-{YEAR_MAX}?
2. Điểm trung bình, trung vị và phân phối điểm của từng môn thay đổi ra sao?
3. Mức thay đổi đến từ toàn bộ phổ điểm hay chỉ từ nhóm điểm thấp/cao?
4. Tỉnh/thành và vùng nào lệch đáng kể so với mặt bằng toàn quốc?
5. Môn/tỉnh/năm nào có biến động bất thường cần giải thích thận trọng?
6. Các môn và tổ hợp môn có quan hệ với nhau thế nào qua tương quan điểm?
7. Dự báo năm tiếp theo có độ tin cậy ra sao khi chỉ có chuỗi 5 năm?

## Giả thuyết phân tích

- H1: Một số môn có thay đổi điểm trung bình mạnh do phân phối điểm dịch chuyển, không chỉ do thay đổi số thí sinh.
- H2: Chênh lệch theo tỉnh/vùng tồn tại rõ hơn ở các môn có số thí sinh thi chọn lọc.
- H3: Các môn tự nhiên có tương quan nội bộ cao hơn các môn thuộc nhóm xã hội.
- H4: Forecast cấp toàn quốc chỉ nên dùng như ước lượng xu hướng vì số điểm thời gian còn ít.
"""
    out_path.write_text(text, encoding="utf-8")
    return out_path
