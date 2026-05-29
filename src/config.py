from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"
REPORTS_DIR = PROJECT_ROOT / "reports"
DEFAULT_CSV = Path(r"D:\do an thuc tap\cleaned_data.csv")
CSV_PATH = DEFAULT_CSV
PROVINCES_CSV = DATA_DIR / "provinces.csv"
YEAR_MIN = 2021
YEAR_MAX = 2025
CHUNK_SIZE = 500_000
MAIN_SUBJECTS = ["Toan", "NguVan", "NgoaiNgu", "VatLy", "HoaHoc", "SinhHoc"]
SUBJECT_COLUMNS = ["Toan","NguVan","VatLy","HoaHoc","SinhHoc","LichSu","DiaLy","GDCD","NgoaiNgu","KinhTePhapLuat","TinHoc","CongNgheCongNghiep","CongNgheNongNghiep"]
COMBINATION_COLUMNS = ["TongDiem","KhoiA","KhoiA1","KhoiB","KhoiC","KhoiD","KHTN","KHXH","TongDiemKHTN","TongDiemKHXH"]
