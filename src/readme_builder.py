"""Sinh README.md duy nhat — bao cao + huong dan + bieu do."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from .charts_report import _subject_detail, _trend_comment, build_readme_charts_section
from .config import CSV_PATH, PROJECT_ROOT, TABLES_DIR, YEAR_MAX, YEAR_MIN
from .labels import fmt_float, fmt_int, subject_vi
from .report import build_trends_table, top_bottom_provinces


def _header() -> str:
    return f"""# THPTQG Trends — Phân tích & dự báo điểm thi THPT quốc gia

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb)

**Repository:** [github.com/2274802010922/thptqg-trends](https://github.com/2274802010922/thptqg-trends)

Đồ án phân tích dữ liệu điểm **Kỳ thi tốt nghiệp THPT quốc gia** ({YEAR_MIN}–{YEAR_MAX}). **Toàn bộ báo cáo nằm trong file README này.**

**Cập nhật lần chạy pipeline gần nhất:** {datetime.now():%d/%m/%Y %H:%M}

---

## Mục lục

1. [Tóm tắt](#1-tóm-tắt)
2. [Mục tiêu & phạm vi](#2-mục-tiêu--phạm-vi)
3. [Nguồn dữ liệu](#3-nguồn-dữ-liệu)
4. [Mô tả dữ liệu](#4-mô-tả-dữ-liệu)
5. [Phương pháp & quy trình](#5-phương-pháp--quy-trình)
6. [Kết quả phân tích](#6-kết-quả-phân-tích)
7. [Dự báo 2026](#7-dự-báo-2026)
8. [Báo cáo chi tiết biểu đồ](#8-báo-cáo-chi-tiết-biểu-đồ)
9. [Cấu trúc repository](#9-cấu-trúc-repository)
10. [Hướng dẫn chạy](#10-hướng-dẫn-chạy)
11. [Kết quả đầu ra (outputs)](#11-kết-quả-đầu-ra-outputs)
12. [Giới hạn & lưu ý](#12-giới-hạn--lưu-ý)
"""


def _section_static_2_to_5() -> str:
    return f"""
---

## 2. Mục tiêu & phạm vi

| # | Mục tiêu |
|---|----------|
| 1 | Khám phá dữ liệu (EDA) theo năm, môn, tỉnh |
| 2 | Phân tích xu hướng {YEAR_MIN}–{YEAR_MAX} |
| 3 | Dự báo chỉ số tổng hợp năm tiếp theo |
| 4 | Trực quan hóa & báo cáo trong README |

- ✅ Thống kê tổng hợp, có thể public
- ❌ Không dự đoán điểm từng `SBD`

---

## 3. Nguồn dữ liệu

| | |
|---|---|
| **Google Drive** | [cleaned_data.csv](https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view?usp=sharing) |
| **File ID** | `1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc` |
| **Local (Windows)** | `{CSV_PATH}` |

CSV ~805 MB **không** commit GitHub.

---

## 4. Mô tả dữ liệu

- **31 cột:** `SBD`, `Nam`, `Tinh`, điểm môn, tổ hợp khối…
- **63 mã tỉnh** (`data/provinces.csv`)
- **0.0** = không thi môn đó

---

## 5. Phương pháp & quy trình

```text
CSV → Validate → Aggregate → Forecast → Charts → README.md
```

| Bước | Công cụ |
|------|---------|
| Đọc file lớn | pandas chunksize 500k |
| Dự báo | LinearRegression |
| Biểu đồ | matplotlib, seaborn |
"""


def _section_1_summary(cand: pd.DataFrame, trends: pd.DataFrame) -> str:
    total = int(cand["SoThiSinh"].sum())
    n2021 = int(cand.loc[cand["Nam"] == YEAR_MIN, "SoThiSinh"].iloc[0])
    n2025 = int(cand.loc[cand["Nam"] == YEAR_MAX, "SoThiSinh"].iloc[0])
    pct_growth = (n2025 - n2021) / n2021 * 100
    lines = [
        "---",
        "",
        "## 1. Tóm tắt",
        "",
        "| Hạng mục | Giá trị |",
        "|----------|---------|",
        f"| Phạm vi | {YEAR_MIN} – {YEAR_MAX} |",
        f"| Tổng thí sinh | **{fmt_int(total)}** |",
        f"| Mô hình dự báo | Hồi quy tuyến tính + backtest |",
        "",
        f"- Số thí sinh tăng **{pct_growth:+.1f}%** ({fmt_int(n2021)} → {fmt_int(n2025)}).",
    ]
    if not trends.empty:
        top_up = trends.nlargest(1, "change_pct").iloc[0]
        top_down = trends.nsmallest(1, "change_pct").iloc[0]
        lines.append(
            f"- Môn tăng mạnh nhất: **{top_up['Môn']}** ({top_up['change_pct']:+.1f}%). "
            f"Môn giảm mạnh nhất: **{top_down['Môn']}** ({top_down['change_pct']:+.1f}%)."
        )
    return "\n".join(lines)


def _section_6_results(cand: pd.DataFrame, trends: pd.DataFrame, named: pd.DataFrame) -> str:
    lines = ["---", "", "## 6. Kết quả phân tích", "", "### 6.1. Số thí sinh theo năm", "", "| Năm | Số thí sinh |", "|-----|-------------|"]
    prev = None
    for _, r in cand.iterrows():
        n = int(r["SoThiSinh"])
        y = int(r["Nam"])
        if prev:
            ch = f" (+{(n - prev) / prev * 100:.1f}%)"
        else:
            ch = ""
        lines.append(f"| {y} | {fmt_int(n)}{ch} |")
        prev = n

    lines += ["", "### 6.2. Xu hướng điểm TB (2021 → 2025)", "", "| Môn | TB đầu | TB cuối | Thay đổi | % ≥ 8 cuối |", "|-----|--------|---------|----------|------------|"]
    for _, r in trends.iterrows():
        ch = f"{r['change_pct']:+.1f}%" if pd.notna(r["change_pct"]) else "—"
        p8 = f"{r['pct_ge_8_last']:.1f}%" if pd.notna(r.get("pct_ge_8_last")) else "—"
        lines.append(f"| {r['Môn']} | {fmt_float(r['mean_first'])} | {fmt_float(r['mean_last'])} | {ch} | {p8} |")

    top, bottom = top_bottom_provinces(named, YEAR_MAX, "Toan")
    lines += ["", f"### 6.3. Top 10 tỉnh — Toán {YEAR_MAX}", ""]
    for i, (_, r) in enumerate(top.iterrows(), 1):
        lines.append(f"{i}. **{r['TenTinh']}** — {fmt_float(r['mean'])} ({fmt_int(int(r['count']))} thí sinh)")
    lines += ["", f"### 6.4. Bottom 10 tỉnh — Toán {YEAR_MAX}", ""]
    for i, (_, r) in enumerate(bottom.iterrows(), 1):
        lines.append(f"{i}. **{r['TenTinh']}** — {fmt_float(r['mean'])} ({fmt_int(int(r['count']))} thí sinh)")
    return "\n".join(lines)


def _section_7_forecast(forecast: pd.DataFrame) -> str:
    lines = [
        "---",
        "",
        "## 7. Dự báo 2026",
        "",
        "Hồi quy tuyến tính; backtest trên năm 2025.",
        "",
        "| Môn | Dự báo 2026 | Thực tế 2025 | MAE |",
        "|-----|-------------|--------------|-----|",
    ]
    for _, r in forecast.iterrows():
        mae = fmt_float(r["backtest_mae"], 4) if pd.notna(r.get("backtest_mae")) else "—"
        lines.append(
            f"| {subject_vi(r['Mon'])} | {fmt_float(r['forecast_mean'], 3)} | "
            f"{fmt_float(r.get('backtest_actual'), 3)} | {mae} |"
        )
    return "\n".join(lines)


def _section_static_9_to_12() -> str:
    return """
---

## 9. Cấu trúc repository

```text
thptqg-trends/
├── README.md              ← Báo cáo duy nhất (file này)
├── run.ps1 / run.bat
├── colab/THPTQG_Colab.ipynb
├── data/provinces.csv
├── src/                   ← Pipeline Python
├── scripts/run_all.py
├── outputs/tables/        ← CSV tổng hợp
└── outputs/figures/       ← Biểu đồ PNG
```

---

## 10. Hướng dẫn chạy

### Google Colab

1. Mở [THPTQG_Colab.ipynb](https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb)
2. Chạy lần lượt các cell
3. Tải dataset từ [Google Drive](https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view?usp=sharing)
4. Cell cuối: zip `outputs/` + tải về

### Windows

```powershell
git clone https://github.com/2274802010922/thptqg-trends.git
cd thptqg-trends
.\\run.ps1
```

Pipeline: `python scripts/run_all.py` → cập nhật **README.md** + outputs.

---

## 11. Kết quả đầu ra (outputs)

| File | Mô tả |
|------|--------|
| `README.md` | Báo cáo đầy đủ (tự cập nhật) |
| `outputs/tables/*.csv` | Bảng thống kê |
| `outputs/figures/*.png` | Biểu đồ |

---

## 12. Giới hạn & lưu ý

- Dự báo mang tính học thuật; giả định cơ chế thi ổn định.
- Điểm 0.0 = không thi môn → so sánh mean giữa các năm cần xem thêm `count`.
- Không public từng dòng `SBD` nếu không cần thiết.

---

*Tái tạo báo cáo: `python scripts/run_all.py`*
"""


def build_readme(out_path: Path | None = None) -> Path:
    """Ghi toan bo README.md tu du lieu outputs/tables."""
    out_path = out_path or PROJECT_ROOT / "README.md"
    tables = Path(TABLES_DIR)

    by_ys = pd.read_csv(tables / "by_year_subject.csv")
    cand = pd.read_csv(tables / "candidates_by_year.csv")
    named = pd.read_csv(tables / "by_year_province_subject_named.csv")
    forecast = pd.read_csv(tables / "forecast_next_year.csv")

    trends = build_trends_table(by_ys)
    trends.to_csv(tables / "trends_summary.csv", index=False)

    parts = [
        _header(),
        _section_1_summary(cand, trends),
        _section_static_2_to_5(),
        _section_6_results(cand, trends, named),
        _section_7_forecast(forecast),
        build_readme_charts_section(),
        _section_static_9_to_12(),
    ]
    out_path.write_text("\n".join(parts), encoding="utf-8")
    return out_path
