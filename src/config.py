import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Windows local default; Colab/Drive: set os.environ["THPTQG_CSV_PATH"] truoc khi chay
DEFAULT_CSV = Path(r"D:\do an thuc tap\cleaned_data.csv")
CSV_PATH = Path(os.environ["THPTQG_CSV_PATH"]) if os.environ.get("THPTQG_CSV_PATH") else DEFAULT_CSV


def configure(csv_path: str | Path | None = None, year_min: int | None = None, year_max: int | None = None):
    """Ghi de cau hinh (dung trong Colab)."""
    global CSV_PATH, YEAR_MIN, YEAR_MAX
    if csv_path is not None:
        CSV_PATH = Path(csv_path)
        os.environ["THPTQG_CSV_PATH"] = str(CSV_PATH)
    if year_min is not None:
        YEAR_MIN = year_min
    if year_max is not None:
        YEAR_MAX = year_max
PROVINCES_CSV = DATA_DIR / "provinces.csv"
YEAR_MIN = 2021
YEAR_MAX = 2025
CHUNK_SIZE = 500_000
MAIN_SUBJECTS = ["Toan", "NguVan", "NgoaiNgu", "VatLy", "HoaHoc", "SinhHoc"]
SUBJECT_COLUMNS = ["Toan","NguVan","VatLy","HoaHoc","SinhHoc","LichSu","DiaLy","GDCD","NgoaiNgu","KinhTePhapLuat","TinHoc","CongNgheCongNghiep","CongNgheNongNghiep"]
COMBINATION_COLUMNS = ["TongDiem","KhoiA","KhoiA1","KhoiB","KhoiC","KhoiD","KHTN","KHXH","TongDiemKHTN","TongDiemKHXH"]
