"""Sinh bao cao chi tiet cho tat ca bieu do."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from .config import FIGURES_DIR, REPORTS_DIR, TABLES_DIR, YEAR_MAX, YEAR_MIN
from .labels import fmt_float, fmt_int, subject_vi


def _trend_comment(change_pct: float | None) -> str:
    if change_pct is None or pd.isna(change_pct):
        return "Không đủ dữ liệu để nhận xét xu hướng."
    if change_pct > 5:
        return f"Xu hướng **tăng** rõ ({change_pct:+.1f}% TB 2021→{YEAR_MAX})."
    if change_pct < -5:
        return f"Xu hướng **giảm** rõ ({change_pct:+.1f}% TB 2021→{YEAR_MAX})."
    return f"Xu hướng **tương đối ổn định** ({change_pct:+.1f}% TB 2021→{YEAR_MAX})."


def _subject_detail(by_ys: pd.DataFrame, mon: str) -> dict:
    sub = by_ys[by_ys["Mon"] == mon].dropna(subset=["mean"]).sort_values("Nam")
    if sub.empty:
        return {}
    first, last = sub.iloc[0], sub.iloc[-1]
    change = None
    if first["mean"] and first["mean"] != 0:
        change = (last["mean"] - first["mean"]) / first["mean"] * 100
    return {
        "mon": mon,
        "name": subject_vi(mon),
        "mean_first": first["mean"],
        "mean_last": last["mean"],
        "change_pct": change,
        "pct_ge_8_last": last.get("pct_ge_8"),
        "count_last": last.get("count"),
        "series": sub[["Nam", "mean", "pct_ge_8", "count"]].to_dict("records"),
    }


def generate_charts_report(out_path: Path | None = None) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = out_path or REPORTS_DIR / "CHARTS_BAO_CAO.md"
    tables = Path(TABLES_DIR)
    figures = Path(FIGURES_DIR)

    by_ys = pd.read_csv(tables / "by_year_subject.csv")
    cand = pd.read_csv(tables / "candidates_by_year.csv")
    forecast = pd.read_csv(tables / "forecast_next_year.csv") if (tables / "forecast_next_year.csv").exists() else pd.DataFrame()

    lines = [
        "# Báo cáo chi tiết biểu đồ — THPTQG Trends",
        "",
        f"**Ngày tạo:** {datetime.now():%d/%m/%Y %H:%M}",
        f"**Phạm vi:** {YEAR_MIN} – {YEAR_MAX}",
        "",
        "Tài liệu này mô tả **toàn bộ biểu đồ** trong `outputs/figures/` kèm số liệu và nhận xét.",
        "",
        "---",
        "",
        "## A. Biểu đồ tổng quan",
        "",
        "### A.1. Số thí sinh theo năm",
        "",
        "`candidates_by_year.png`",
        "",
    ]
    for _, r in cand.iterrows():
        lines.append(f"- **{int(r['Nam'])}:** {fmt_int(int(r['SoThiSinh']))} thí sinh")
    lines += [
        "",
        "**Nhận xét:** Quy mô kỳ thi tăng liên tục trong giai đoạn phân tích; biểu đồ cột thể hiện áp lực tăng số lượng hồ sơ theo thời gian.",
        "",
        f"![Số thí sinh theo năm](../outputs/figures/candidates_by_year.png)",
        "",
        "### A.2. Tỷ lệ điểm ≥ 8 — tất cả môn",
        "",
        "`pct_ge_8_by_year.png` — so sánh trên cùng biểu đồ các môn có dữ liệu.",
        "",
        f"![Tỷ lệ điểm >= 8](../outputs/figures/pct_ge_8_by_year.png)",
        "",
        "---",
        "",
        "## B. Xu hướng điểm trung bình — từng môn",
        "",
    ]

    subjects = [m for m in by_ys["Mon"].unique() if by_ys.loc[by_ys["Mon"] == m, "count"].sum() > 0]
    subjects = sorted(subjects, key=lambda x: subject_vi(x))

    for mon in subjects:
        info = _subject_detail(by_ys, mon)
        if not info:
            continue
        fname = f"mean_by_year_{mon}.png"
        lines += [
            f"### B.{subjects.index(mon)+1}. {info['name']} (`{mon}`)",
            "",
            f"| Chỉ số | Giá trị |",
            f"|--------|---------|",
            f"| TB {YEAR_MIN} | {fmt_float(info['mean_first'])} |",
            f"| TB {YEAR_MAX} | {fmt_float(info['mean_last'])} |",
            f"| Thay đổi | {info['change_pct']:+.1f}% |" if info["change_pct"] is not None else "| Thay đổi | — |",
            f"| Tỷ lệ ≥ 8 ({YEAR_MAX}) | {info['pct_ge_8_last']:.1f}% |" if pd.notna(info.get("pct_ge_8_last")) else f"| Tỷ lệ ≥ 8 ({YEAR_MAX}) | — |",
            f"| Số thí sinh thi môn ({YEAR_MAX}) | {fmt_int(int(info['count_last'])) if pd.notna(info.get('count_last')) else '—'} |",
            "",
            "**Chi tiết theo năm:**",
            "",
            "| Năm | Điểm TB | % ≥ 8 | Số thí sinh |",
            "|-----|---------|-------|-------------|",
        ]
        for row in info["series"]:
            p8 = f"{row['pct_ge_8']:.1f}%" if pd.notna(row.get("pct_ge_8")) else "—"
            cnt = fmt_int(int(row["count"])) if pd.notna(row.get("count")) else "—"
            lines.append(f"| {int(row['Nam'])} | {fmt_float(row['mean'])} | {p8} | {cnt} |")
        lines += [
            "",
            f"**Nhận xét:** {_trend_comment(info['change_pct'])}",
            "",
            f"![{info['name']}](../outputs/figures/{fname})",
            "",
        ]

    lines += ["---", "", "## C. Heatmap phân bố theo tỉnh (2025)", ""]
    heatmaps = sorted(figures.glob(f"heatmap_*_{YEAR_MAX}.png"))
    for i, hp in enumerate(heatmaps, 1):
        mon = hp.stem.replace("heatmap_", "").replace(f"_{YEAR_MAX}", "")
        lines += [
            f"### C.{i}. {subject_vi(mon)}",
            "",
            f"Biểu đồ thể hiện **điểm TB theo mã tỉnh (1–63)** năm {YEAR_MAX}. Màu đậm = điểm cao hơn.",
            "",
            f"![Heatmap {subject_vi(mon)}](../outputs/figures/{hp.name})",
            "",
        ]

    lines += ["---", "", "## D. Biểu đồ dự báo", ""]
    if not forecast.empty:
        lines += [
            "Mô hình hồi quy tuyến tính trên chuỗi điểm TB 2021–2025; đường đứt là năm dự báo tiếp theo.",
            "",
        ]
    for i, fp in enumerate(sorted(figures.glob("forecast_*.png")), 1):
        mon = fp.stem.replace("forecast_", "")
        lines += [f"### D.{i}. {subject_vi(mon)}", ""]
        if not forecast.empty and mon in forecast["Mon"].values:
            row = forecast[forecast["Mon"] == mon].iloc[0]
            mae = fmt_float(row["backtest_mae"], 4) if pd.notna(row.get("backtest_mae")) else "—"
            lines += [
                f"- Dự báo **{int(row['forecast_year'])}:** {fmt_float(row['forecast_mean'], 3)} điểm",
                f"- Thực tế {YEAR_MAX}: {fmt_float(row.get('backtest_actual'), 3)} | MAE backtest: {mae}",
                "",
            ]
        lines += [f"![Dự báo {subject_vi(mon)}](../outputs/figures/{fp.name})", ""]

    lines += [
        "---",
        "",
        "## E. Danh mục file hình",
        "",
        "| # | File | Loại |",
        "|---|------|------|",
    ]
    for i, fp in enumerate(sorted(figures.glob("*.png")), 1):
        lines.append(f"| {i} | `{fp.name}` | PNG |")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def build_readme_charts_section() -> str:
    """Trả về markdown section 8 nhúng TOÀN BỘ hình cho README (đường dẫn relative)."""
    tables = Path(TABLES_DIR)
    figures = Path(FIGURES_DIR)
    by_ys = pd.read_csv(tables / "by_year_subject.csv")
    forecast = pd.read_csv(tables / "forecast_next_year.csv") if (tables / "forecast_next_year.csv").exists() else pd.DataFrame()

    lines = [
        "## 8. Báo cáo chi tiết biểu đồ",
        "",
        "Phần này trình bày **tất cả biểu đồ** và nhận xét theo từng môn.",
        "",
        "### 8.1. Tổng quan",
        "",
        "#### Số thí sinh theo năm",
        "",
        "![Số thí sinh theo năm](outputs/figures/candidates_by_year.png)",
        "",
        "#### Tỷ lệ điểm ≥ 8 — tất cả môn",
        "",
        "![Tỷ lệ điểm >= 8](outputs/figures/pct_ge_8_by_year.png)",
        "",
        "### 8.2. Xu hướng điểm TB — từng môn",
        "",
    ]

    subjects = sorted(
        [m for m in by_ys["Mon"].unique() if by_ys.loc[by_ys["Mon"] == m, "count"].sum() > 0],
        key=lambda x: subject_vi(x),
    )
    for mon in subjects:
        info = _subject_detail(by_ys, mon)
        if not info:
            continue
        ch = f"{info['change_pct']:+.1f}%" if info["change_pct"] is not None else "—"
        lines += [
            f"#### {info['name']}",
            "",
            f"- TB {YEAR_MIN}: **{fmt_float(info['mean_first'])}** → TB {YEAR_MAX}: **{fmt_float(info['mean_last'])}** ({ch})",
            f"- Tỷ lệ ≥ 8 năm {YEAR_MAX}: **{info['pct_ge_8_last']:.1f}%**" if pd.notna(info.get("pct_ge_8_last")) else "",
            f"- {_trend_comment(info['change_pct'])}",
            "",
            f"![{info['name']}](outputs/figures/mean_by_year_{mon}.png)",
            "",
        ]

    lines += ["### 8.3. Heatmap theo tỉnh (2025)", ""]
    for hp in sorted(figures.glob(f"heatmap_*_{YEAR_MAX}.png")):
        mon = hp.stem.replace("heatmap_", "").replace(f"_{YEAR_MAX}", "")
        lines += [
            f"#### {subject_vi(mon)} — phân bố 63 tỉnh",
            "",
            f"![Heatmap {subject_vi(mon)}](outputs/figures/{hp.name})",
            "",
        ]

    lines += ["### 8.4. Dự báo", ""]
    for fp in sorted(figures.glob("forecast_*.png")):
        mon = fp.stem.replace("forecast_", "")
        extra = "Đường xanh: thực tế; đường đứt đỏ: extrapolation tuyến tính. "
        if not forecast.empty and mon in forecast["Mon"].values:
            row = forecast[forecast["Mon"] == mon].iloc[0]
            extra = f"Dự báo {int(row['forecast_year'])}: **{fmt_float(row['forecast_mean'], 3)}** điểm. " + extra
        lines += [
            f"#### {subject_vi(mon)}",
            "",
            extra,
            "",
            f"![Dự báo {subject_vi(mon)}](outputs/figures/{fp.name})",
            "",
        ]

    return "\n".join(line for line in lines if line is not None)


def patch_readme(readme_path: Path | None = None) -> Path:
    """Thay section 8 trong README.md bằng bản đầy đủ."""
    from .config import PROJECT_ROOT

    readme_path = readme_path or PROJECT_ROOT / "README.md"
    text = readme_path.read_text(encoding="utf-8")
    new_section = build_readme_charts_section()
    start = text.find("## 8.")
    end = text.find("\n---\n\n## 9.")
    if start == -1 or end == -1:
        raise ValueError("Không tìm thấy section 8 hoặc 9 trong README.md")
    updated = text[:start] + new_section + text[end:]
    readme_path.write_text(updated, encoding="utf-8")
    return readme_path
