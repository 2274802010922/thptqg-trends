import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "colab" / "THPTQG_Colab.ipynb"


def md(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.strip().splitlines(True)}


def code(source: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source.strip().splitlines(True)}


cells = [
    md(
        """
# THPTQG Trends — Google Colab Reproducibility Notebook

Notebook này là đường chạy minh chứng cho repository: clone code từ GitHub, lấy raw CSV từ Google Drive hoặc Google Drive mounted path, chạy pipeline end-to-end và sinh lại `outputs/`, `README.md`, `docs/report.md`.

Workflow phân tích gồm: data quality → aggregate → phân phối điểm → biến động theo năm → tỉnh/vùng → bất thường → tương quan/tổ hợp → forecast/backtest → báo cáo.
"""
    ),
    code(
        """
!pip install -q gdown

import os, sys
from pathlib import Path

ROOT = Path("/content/thptqg-trends")
if not ROOT.exists():
    !git clone https://github.com/2274802010922/thptqg-trends.git /content/thptqg-trends
else:
    !cd /content/thptqg-trends && git pull

os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

!pip install -q -r requirements.txt

from src.display import setup_display
setup_display()
print("Repo:", ROOT)
"""
    ),
    md(
        """
## 1. Chuẩn Bị Raw Dataset

Raw CSV không nằm trong GitHub vì file khoảng 844 MB. Chọn một trong hai cách:

- `USE_MOUNTED_DRIVE = False`: tải trực tiếp từ Google Drive public link bằng `gdown`.
- `USE_MOUNTED_DRIVE = True`: mount Google Drive cá nhân rồi trỏ tới file đã có sẵn.
"""
    ),
    code(
        """
from pathlib import Path

RAW_DRIVE_URL = "https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view"
USE_MOUNTED_DRIVE = False

if USE_MOUNTED_DRIVE:
    from google.colab import drive
    drive.mount("/content/drive")
    CSV_PATH = "/content/drive/MyDrive/do an thuc tap/cleaned_data.csv"
else:
    CSV_PATH = "/content/cleaned_data.csv"
    if not Path(CSV_PATH).exists():
        import gdown
        gdown.download(url=RAW_DRIVE_URL, output=CSV_PATH, fuzzy=True, quiet=False)

assert Path(CSV_PATH).exists(), f"Không tìm thấy raw CSV: {CSV_PATH}"
print("CSV:", CSV_PATH)
print("Size (bytes):", Path(CSV_PATH).stat().st_size)
"""
    ),
    md("## 2. Cấu Hình Phạm Vi Nghiên Cứu"),
    code(
        """
from src.config import configure

YEAR_MIN, YEAR_MAX = 2021, 2025
configure(csv_path=CSV_PATH, year_min=YEAR_MIN, year_max=YEAR_MAX)
print(f"Phạm vi đồ án: {YEAR_MIN}-{YEAR_MAX}")
"""
    ),
    md("## 3. Chạy Pipeline End-To-End"),
    code(
        """
import time
from IPython.display import display

from src.load_data import count_rows
from src.aggregates import save_aggregates
from src.advanced_analysis import generate_da_tables, build_forecast_reliability, write_analysis_questions
from src.forecast import run_forecast_pipeline
from src.plots import generate_all_figures
from src.readme_builder import build_readme
from src.report import generate_report
from src.display import pretty_counts, pretty_forecast

t0 = time.time()

print("1/7 Kiểm tra dữ liệu")
counts = count_rows()
display(pretty_counts(counts))

print("2/7 Tổng hợp dữ liệu nền")
paths = save_aggregates()
for name, path in paths.items():
    print(name, "->", path)

print("3/7 Phân tích DA nâng cao")
da_paths = generate_da_tables()
for name, path in da_paths.items():
    print(name, "->", path)
print("analysis_questions ->", write_analysis_questions())

print("4/7 Dự báo + backtest + model comparison")
forecast = run_forecast_pipeline()
display(pretty_forecast(forecast))
print("forecast_reliability ->", build_forecast_reliability())

print("5/7 Vẽ biểu đồ")
figures = generate_all_figures()
print(f"Generated {len(figures)} figures")

print("6/7 Sinh README và report học thuật")
readme_path = build_readme()
report_path = generate_report()
print("README:", readme_path)
print("Report:", report_path)

print("7/7 Hoàn tất")
print(f"Elapsed: {(time.time() - t0) / 60:.1f} phút")
"""
    ),
    md("## 4. Xem Data Quality Và Phân Phối Điểm"),
    code(
        """
import pandas as pd
from IPython.display import display

display(pd.read_csv("outputs/tables/data_quality_summary.csv"))
display(pd.read_csv("outputs/tables/missing_by_subject_year.csv").head(20))
display(pd.read_csv("outputs/tables/score_distribution_by_year_subject.csv").head(20))
display(pd.read_csv("outputs/tables/score_bands_by_year_subject.csv").head(20))
"""
    ),
    md("## 5. Xem Biến Động, Vùng Và Bất Thường"),
    code(
        """
display(pd.read_csv("outputs/tables/yearly_change_by_subject.csv").dropna(subset=["mean_change_pct"]).head(20))
display(pd.read_csv("outputs/tables/by_region_subject_year.csv").head(20))
display(pd.read_csv("outputs/tables/province_anomalies.csv").head(20))
display(pd.read_csv("outputs/tables/province_volatility.csv").head(20))
"""
    ),
    md("## 6. Xem Tương Quan Và Tổ Hợp Môn"),
    code(
        """
display(pd.read_csv("outputs/tables/subject_correlation_by_year.csv").head(20))
display(pd.read_csv("outputs/tables/combination_scores_by_year.csv").head(20))
"""
    ),
    md("## 7. Xem Bảng Đánh Giá Mô Hình"),
    code(
        """
import pandas as pd
from IPython.display import display

model_cmp = pd.read_csv("outputs/tables/model_comparison.csv")
display(model_cmp.sort_values(["Mon", "mae", "rmse"]))

display(pd.read_csv("outputs/tables/forecast_reliability.csv"))

backtest = pd.read_csv("outputs/tables/backtest_predictions.csv")
display(backtest.head(20))
"""
    ),
    md("## 8. Xem Báo Cáo"),
    code(
        """
from IPython.display import Markdown, display
from pathlib import Path

display(Markdown(Path("README.md").read_text(encoding="utf-8")))
"""
    ),
    md("## 9. Xem Biểu Đồ"),
    code(
        """
from IPython.display import Image, display
from pathlib import Path

for p in sorted(Path("outputs/figures").glob("*.png")):
    print(p.name)
    display(Image(filename=str(p)))
"""
    ),
    md("## 10. Tải Kết Quả"),
    code(
        """
import zipfile
from pathlib import Path
from google.colab import files

zip_path = Path("/content/thptqg_full_outputs.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for folder in ["outputs", "docs", "data"]:
        for f in Path(folder).rglob("*"):
            if f.is_file():
                z.write(f, f.as_posix())
    z.write("README.md", "README.md")
    z.write("requirements.txt", "requirements.txt")
    z.write(".env.example", ".env.example")

files.download(str(zip_path))
"""
    ),
]

notebook = {
    "cells": cells,
    "metadata": {
        "colab": {"provenance": []},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
print(OUT)
