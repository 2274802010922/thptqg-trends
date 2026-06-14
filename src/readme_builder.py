"""Sinh README.md duy nhat — bao cao + huong dan + bieu do."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from .advanced_report import (
    build_advanced_charts_section,
    build_advanced_results_section,
    build_forecast_reliability_section,
)
from .charts_report import build_readme_charts_section
from .config import (
    CSV_PATH,
    PROJECT_ROOT,
    RAW_DATA_DRIVE_ID,
    RAW_DATA_DRIVE_URL,
    RAW_DATA_FILENAME,
    RAW_DATA_SHA256,
    RAW_DATA_SIZE_BYTES,
    RAW_DATA_TOTAL_ROWS,
    RAW_DATA_YEAR_COUNTS,
    TABLES_DIR,
    YEAR_MAX,
    YEAR_MIN,
)
from .labels import fmt_float, fmt_int, subject_vi
from .plain_language import (
    explain_candidates_table,
    explain_province_ranking,
    explain_trends_table,
    section_6_intro,
    section_forecast_plain,
    section_glossary,
    section_method_plain,
)
from .report import build_trends_table, top_bottom_provinces


def _header() -> str:
    return f"""# THPTQG Trends — Phân tích & dự báo điểm thi THPT quốc gia

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb)

**Repository:** [github.com/2274802010922/thptqg-trends](https://github.com/2274802010922/thptqg-trends)

Đồ án phân tích dữ liệu điểm **Kỳ thi tốt nghiệp THPT quốc gia** ({YEAR_MIN}–{YEAR_MAX}). **Toàn bộ báo cáo nằm trong file README này** — viết sao cho **giáo viên, phụ huynh, sinh viên ngành khác** cũng đọc được.

**Cập nhật lần chạy pipeline gần nhất:** {datetime.now():%d/%m/%Y %H:%M}

---

## Mục lục

- [Đọc trước — Thuật ngữ & hướng dẫn nhanh](#đọc-trước--dành-cho-người-chưa-quen-phân-tích-dữ-liệu)
1. [Tóm tắt](#1-tóm-tắt)
2. [Mục tiêu & phạm vi](#2-mục-tiêu--phạm-vi)
3. [Nguồn dữ liệu](#3-nguồn-dữ-liệu)
4. [Mô tả dữ liệu](#4-mô-tả-dữ-liệu)
5. [Phương pháp & quy trình](#5-phương-pháp--quy-trình-giải-thích-đơn-giản)
6. [Kết quả phân tích](#6-kết-quả-phân-tích--kèm-giải-thích)
7. [Dự báo 2026](#7-dự-báo-2026--giải-thích-cho-người-không-chuyên)
8. [Báo cáo chi tiết biểu đồ](#8-báo-cáo-chi-tiết-biểu-đồ)
9. [Cấu trúc repository](#9-cấu-trúc-repository)
10. [Hướng dẫn chạy](#10-hướng-dẫn-chạy)
11. [Kết quả đầu ra (outputs)](#11-kết-quả-đầu-ra-outputs)
12. [Giới hạn & lưu ý](#12-giới-hạn--lưu-ý)
"""


def _section_static_2_to_4() -> str:
    return f"""
---

## 2. Mục tiêu & phạm vi

**Câu hỏi đồ án muốn trả lời:**

| # | Câu hỏi | Trả lời bằng gì? |
|---|---------|------------------|
| 1 | Mỗi năm có bao nhiêu thí sinh? | Biểu đồ cột, bảng mục 6.1 |
| 2 | Điểm TB từng môn đang tăng hay giảm? | Bảng mục 6.2, biểu đồ mục 8.2 |
| 3 | Tỉnh nào cao/thấp hơn trung bình? | Heatmap mục 8.3 |
| 4 | Năm sau TB có thể quanh bao nhiêu? | Mục 7, biểu đồ mục 8.4 |

**Phạm vi:**

- ✅ Thống kê **tổng hợp** (toàn quốc, theo tỉnh) — an toàn để public
- ❌ **Không** dự đoán điểm của từng số báo danh (`SBD`) cá nhân

---

## 3. Nguồn dữ liệu

| | |
|---|---|
| **Google Drive** | [{RAW_DATA_FILENAME}]({RAW_DATA_DRIVE_URL}) |
| **File ID** | `{RAW_DATA_DRIVE_ID}` |
| **Local (Windows)** | `{CSV_PATH}` |
| **Dung lượng** | `{RAW_DATA_SIZE_BYTES:,}` bytes |
| **SHA256** | `{RAW_DATA_SHA256}` |

File CSV khoảng **844 MB** — quá lớn để đưa lên GitHub, nên tải riêng từ Drive hoặc đặt đúng đường dẫn local rồi chạy pipeline.

Raw CSV có **{RAW_DATA_TOTAL_ROWS:,} dòng** trong giai đoạn 2020–2025. Đồ án này cố ý chọn **{YEAR_MIN}–{YEAR_MAX}** để đúng phạm vi 5 năm gần nhất:

| Năm | Số dòng raw |
|-----|-------------|
{chr(10).join(f"| {year} | {fmt_int(count)} |" for year, count in RAW_DATA_YEAR_COUNTS.items())}

Chi tiết schema nằm ở [`docs/data_dictionary.md`](docs/data_dictionary.md); hướng dẫn dữ liệu nằm ở [`data/README.md`](data/README.md).

---

## 4. Mô tả dữ liệu (dễ hiểu)

Mỗi **dòng** trong file ≈ **một thí sinh một năm**, gồm:

- **SBD** — số báo danh (mã định danh, không public chi tiết trong báo cáo này)
- **Nam** — năm thi (2021–2025)
- **Tinh** — mã tỉnh (1–63)
- **Điểm từng môn** — Toán, Văn, Anh, Lý, Hóa, …

**Quy ước quan trọng:** điểm **0.0** = thí sinh **không thi môn đó**. Khi tính điểm TB môn, chỉ lấy người đã thi (điểm > 0).

Danh sách tên tỉnh đầy đủ: `data/provinces.csv`.
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
        "*(Đọc mục này trước nếu bạn chỉ có 2 phút.)*",
        "",
        "| Hạng mục | Giá trị | Ý nghĩa ngắn |",
        "|----------|---------|--------------|",
        f"| Phạm vi | {YEAR_MIN} – {YEAR_MAX} | 5 kỳ thi liên tiếp |",
        f"| Tổng thí sinh (cộng 5 năm) | **{fmt_int(total)}** | Tổng lượt có trong dữ liệu |",
        f"| Mô hình dự báo | Chọn theo rolling backtest | So sánh baseline, trung bình trượt, hồi quy tuyến tính, san bằng mũ |",
        "",
        f"- Số thí sinh mỗi năm **tăng dần**: {fmt_int(n2021)} ({YEAR_MIN}) → {fmt_int(n2025)} ({YEAR_MAX}), tức **{pct_growth:+.1f}%**.",
    ]
    if not trends.empty:
        top_up = trends.nlargest(1, "change_pct").iloc[0]
        top_down = trends.nsmallest(1, "change_pct").iloc[0]
        lines += [
            f"- Môn **tăng** mạnh nhất (TB {YEAR_MIN}→{YEAR_MAX}): **{top_up['Môn']}** ({top_up['change_pct']:+.1f}%).",
            f"- Môn **giảm** mạnh nhất: **{top_down['Môn']}** ({top_down['change_pct']:+.1f}%).",
            "",
            "**Điều cần nhớ:** TB giảm không luôn có nghĩa “học kém hơn” — có thể do **nhiều người hơn** thi môn đó. Chi tiết từng môn ở [Mục 8](#8-báo-cáo-chi-tiết-biểu-đồ).",
        ]
    return "\n".join(lines)


def _section_6_results(cand: pd.DataFrame, trends: pd.DataFrame, named: pd.DataFrame) -> str:
    lines = [
        section_6_intro().strip(),
        "",
        "### 6.1. Số thí sinh theo năm",
        "",
        explain_candidates_table().strip(),
        "",
        "| Năm | Số thí sinh |",
        "|-----|-------------|",
    ]
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

    lines += [
        "",
        "### 6.2. Xu hướng điểm TB (2021 → 2025)",
        "",
        explain_trends_table().strip(),
        "",
        "| Môn | TB đầu | TB cuối | Thay đổi | % ≥ 8 cuối |",
        "|-----|--------|---------|----------|------------|",
    ]
    for _, r in trends.iterrows():
        ch = f"{r['change_pct']:+.1f}%" if pd.notna(r["change_pct"]) else "—"
        p8 = f"{r['pct_ge_8_last']:.1f}%" if pd.notna(r.get("pct_ge_8_last")) else "—"
        lines.append(f"| {r['Môn']} | {fmt_float(r['mean_first'])} | {fmt_float(r['mean_last'])} | {ch} | {p8} |")

    top, bottom = top_bottom_provinces(named, YEAR_MAX, "Toan")
    lines += [
        "",
        f"### 6.3. Top 10 tỉnh — Toán {YEAR_MAX}",
        "",
        explain_province_ranking("Toán").strip(),
        "",
    ]
    for i, (_, r) in enumerate(top.iterrows(), 1):
        lines.append(f"{i}. **{r['TenTinh']}** — {fmt_float(r['mean'])} ({fmt_int(int(r['count']))} thí sinh)")
    lines += ["", f"### 6.4. Bottom 10 tỉnh — Toán {YEAR_MAX}", ""]
    for i, (_, r) in enumerate(bottom.iterrows(), 1):
        lines.append(f"{i}. **{r['TenTinh']}** — {fmt_float(r['mean'])} ({fmt_int(int(r['count']))} thí sinh)")
    return "\n".join(lines)


def _section_7_forecast(forecast: pd.DataFrame) -> str:
    rows = []
    for _, r in forecast.iterrows():
        mae = fmt_float(r["backtest_mae"], 4) if pd.notna(r.get("backtest_mae")) else "—"
        rmse = fmt_float(r["backtest_rmse"], 4) if pd.notna(r.get("backtest_rmse")) else "—"
        interval = (
            f"{fmt_float(r.get('forecast_lower'), 3)}–{fmt_float(r.get('forecast_upper'), 3)}"
            if pd.notna(r.get("forecast_lower")) and pd.notna(r.get("forecast_upper"))
            else "—"
        )
        rows.append(
            f"| {subject_vi(r['Mon'])} | {r.get('selected_model_label', '—')} | "
            f"{fmt_float(r['forecast_mean'], 3)} | {interval} | {mae} | {rmse} |"
        )
    return section_forecast_plain(rows)


def _section_static_9_to_12() -> str:
    return """
---

## 9. Cấu trúc repository

```text
thptqg-trends/
├── .github/workflows/ci.yml
├── README.md              ← Báo cáo duy nhất (file này)
├── .env.example           ← Mẫu cấu hình đường dẫn raw CSV
├── run.ps1 / run.bat
├── colab/THPTQG_Colab.ipynb
├── data/provinces.csv
├── data/province_regions.csv
├── data/README.md
├── docs/data_dictionary.md
├── docs/report.md
├── src/                   ← Pipeline Python
├── scripts/run_all.py
├── tests/                 ← Unit tests tối thiểu
├── outputs/tables/        ← CSV tổng hợp
└── outputs/figures/       ← Biểu đồ PNG
```

---

## 10. Hướng dẫn chạy

### Google Colab (khuyên dùng nếu không có máy mạnh)

1. Mở [THPTQG_Colab.ipynb](https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb)
2. Chạy lần lượt các cell từ trên xuống
3. Tải dataset từ [Google Drive](https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view) hoặc mount Drive
4. Chạy pipeline để sinh lại `outputs/`, `README.md`, `docs/report.md`
5. Cell cuối: zip kết quả và tải về

### Windows (máy local)

```powershell
git clone https://github.com/2274802010922/thptqg-trends.git
cd thptqg-trends
$env:THPTQG_CSV_PATH="D:\\do an thuc tap\\cleaned_data.csv"
.\\run.ps1
```

Lệnh trên chạy `python scripts/run_all.py` → cập nhật **README.md**, `docs/report.md` và thư mục `outputs/`.

---

## 11. Kết quả đầu ra (outputs)

| File | Mô tả | Ai cần đọc? |
|------|--------|-------------|
| `README.md` | Báo cáo đầy đủ (tự cập nhật) | Mọi người |
| `docs/report.md` | Báo cáo học thuật theo cấu trúc đồ án | Hội đồng / giảng viên |
| `data/README.md` | Thông tin raw data và cách cấu hình | Người muốn chạy lại |
| `docs/data_dictionary.md` | Giải thích schema dữ liệu | Người kiểm chứng dữ liệu |
| `docs/analysis_questions.md` | Câu hỏi phân tích và giả thuyết | Hội đồng / người review hướng DA |
| `tests/` | Kiểm tra logic xử lý và dự báo bằng dữ liệu mẫu | Người review code |
| `outputs/tables/*.csv` | Bảng số liệu thô đã tổng hợp | Người muốn tự vẽ biểu đồ / kiểm chứng |
| `outputs/figures/*.png` | Biểu đồ tổng quan, heatmap, dự báo | Slide, báo cáo miệng |

---

## 12. Giới hạn & lưu ý

| Giới hạn | Giải thích đơn giản |
|----------|---------------------|
| Dự báo 2026 | Chỉ là **ước lượng học thuật**, không thay thế thông tin Bộ GD&ĐT |
| Raw data | Không push lên GitHub vì quá lớn; tải qua Google Drive hoặc đặt local path |
| Điểm 0.0 | = không thi môn → khi TB giảm, xem thêm **số người thi** |
| So sánh tỉnh | Tỉnh ít thí sinh thi môn → số liệu dễ **lệch** |
| Quyền riêng tư | Không public từng dòng `SBD` nếu không cần thiết |

---

*Tái tạo báo cáo: `python scripts/run_all.py` hoặc `.\\run.ps1`*
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
        section_glossary(),
        _section_1_summary(cand, trends),
        _section_static_2_to_4(),
        section_method_plain(),
        _section_6_results(cand, trends, named),
        build_advanced_results_section(),
        _section_7_forecast(forecast),
        build_forecast_reliability_section(),
        build_readme_charts_section(),
        build_advanced_charts_section(),
        _section_static_9_to_12(),
    ]
    out_path.write_text("\n".join(parts), encoding="utf-8")
    return out_path
