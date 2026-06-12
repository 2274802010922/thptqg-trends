import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"
REPORTS_DIR = PROJECT_ROOT / "reports"
DOCS_DIR = PROJECT_ROOT / "docs"

RAW_DATA_FILENAME = "cleaned_data.csv"
RAW_DATA_DRIVE_ID = "1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc"
RAW_DATA_DRIVE_URL = f"https://drive.google.com/file/d/{RAW_DATA_DRIVE_ID}/view"
RAW_DATA_SIZE_BYTES = 843_891_415
RAW_DATA_SHA256 = "E11EC167D7073192F719C5A09B2A91556631CA897E998467C2BAF8CA485E86B0"
RAW_DATA_TOTAL_ROWS = 6_068_463
RAW_DATA_YEAR_COUNTS = {
    2020: 870_517,
    2021: 987_704,
    2022: 995_441,
    2023: 1_022_060,
    2024: 1_061_605,
    2025: 1_131_136,
}

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
