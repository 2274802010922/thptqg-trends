"""Tạo báo cáo Markdown từ bảng aggregate và dự báo."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json

import pandas as pd

from .config import CSV_PATH, REPORTS_DIR, TABLES_DIR, YEAR_MIN, YEAR_MAX
from .labels import fmt_float, fmt_int, subject_vi


def _pct_change(first, last):
    if first is None or last is None or first == 0:
        return None
    return round((last - first) / first * 100, 2)


def build_trends_table(by_year_subject: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mon, g in by_year_subject.groupby("Mon"):
        g = g.dropna(subset=["mean"]).sort_values("Nam")
        if g.empty:
            continue
        first, last = g.iloc[0], g.iloc[-1]
        rows.append({
            "Mon": mon,
            "Môn": subject_vi(mon),
            "mean_first": first["mean"],
            "mean_last": last["mean"],
            "change_pct": _pct_change(first["mean"], last["mean"]),
            "pct_ge_8_last": last.get("pct_ge_8"),
        })
    return pd.DataFrame(rows).sort_values("Môn")


def top_bottom_provinces(named: pd.DataFrame, year: int, subject: str = "Toan", n: int = 10):
    df = named[(named["Nam"] == year) & (named["Mon"] == subject)].dropna(subset=["mean"])
    df = df.sort_values("mean", ascending=False)
    top = df.head(n)[["TenTinh", "mean", "count"]]
    bottom = df.tail(n).sort_values("mean")[["TenTinh", "mean", "count"]]
    return top, bottom


def generate_report(out_path: Path | None = None) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = out_path or REPORTS_DIR / "BAO_CAO.md"
    tables = Path(TABLES_DIR)
    by_ys = pd.read_csv(tables / "by_year_subject.csv")
    cand = pd.read_csv(tables / "candidates_by_year.csv")
    named = pd.read_csv(tables / "by_year_province_subject_named.csv")
    forecast = pd.read_csv(tables / "forecast_next_year.csv")
    trends = build_trends_table(by_ys)
    trends.to_csv(tables / "trends_summary.csv", index=False)
    top, bottom = top_bottom_provinces(named, YEAR_MAX, "Toan")

    lines = [
        "# Báo cáo phân tích điểm THPT quốc gia",
        "",
        f"**Ngày tạo:** {datetime.now():%d/%m/%Y %H:%M}",
        f"**Dữ liệu:** `{CSV_PATH}`",
        f"**Phạm vi:** {YEAR_MIN} – {YEAR_MAX}",
        "",
        "## 1. Tổng quan",
        "",
        f"- Tổng số thí sinh ({YEAR_MAX - YEAR_MIN + 1} năm): **{fmt_int(int(cand['SoThiSinh'].sum()))}**",
    ]
    for _, r in cand.iterrows():
        lines.append(f"- Năm **{int(r['Nam'])}**: {fmt_int(int(r['SoThiSinh']))} thí sinh")

    lines += [
        "",
        "## 2. Xu hướng điểm trung bình",
        "",
        "| Môn | TB đầu kỳ | TB cuối kỳ | Thay đổi | Tỷ lệ ≥ 8 (cuối kỳ) |",
        "|-----|-----------|------------|----------|---------------------|",
    ]
    for _, r in trends.iterrows():
        ch = r["change_pct"]
        chs = f"{ch:+.2f}%" if pd.notna(ch) else "—"
        p8 = f"{r['pct_ge_8_last']:.1f}%" if pd.notna(r.get("pct_ge_8_last")) else "—"
        lines.append(
            f"| {r['Môn']} | {fmt_float(r['mean_first'])} | {fmt_float(r['mean_last'])} | {chs} | {p8} |"
        )

    lines += ["", f"## 3. Top 10 tỉnh — Toán {YEAR_MAX}", ""]
    for i, (_, r) in enumerate(top.iterrows(), 1):
        lines.append(f"{i}. **{r['TenTinh']}** — {fmt_float(r['mean'])} điểm ({fmt_int(int(r['count']))} thí sinh)")

    lines += ["", f"## 4. Bottom 10 tỉnh — Toán {YEAR_MAX}", ""]
    for i, (_, r) in enumerate(bottom.iterrows(), 1):
        lines.append(f"{i}. **{r['TenTinh']}** — {fmt_float(r['mean'])} điểm ({fmt_int(int(r['count']))} thí sinh)")

    lines += [
        "",
        "## 5. Dự báo năm tiếp theo",
        "",
        "| Môn | Năm | Điểm TB dự kiến | Sai số backtest (MAE) |",
        "|-----|-----|-----------------|------------------------|",
    ]
    for _, r in forecast.iterrows():
        mae = fmt_float(r["backtest_mae"], 4) if pd.notna(r.get("backtest_mae")) else "—"
        lines.append(
            f"| {subject_vi(r['Mon'])} | {int(r['forecast_year'])} | {fmt_float(r['forecast_mean'], 3)} | {mae} |"
        )

    lines += [
        "",
        "## 6. Hình ảnh",
        "",
        "Xem thư mục `outputs/figures/`.",
        "",
        "## 7. Giới hạn",
        "",
        "- Giả định cơ chế thi ổn định so với các năm trước.",
        "- Điểm 0,0 được coi là không thi môn đó.",
        "- Dự báo trên chỉ số tổng hợp, không phải từng cá nhân.",
        "",
        "---",
        "*Chạy lại: `python scripts/run_all.py` hoặc notebook Colab.*",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")

    profile = {
        "csv": str(CSV_PATH),
        "year_min": YEAR_MIN,
        "year_max": YEAR_MAX,
        "total_candidates": int(cand["SoThiSinh"].sum()),
        "generated_at": datetime.now().isoformat(),
    }
    (tables / "data_profile.json").write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path
