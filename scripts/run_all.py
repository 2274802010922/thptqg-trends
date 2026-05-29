"""Pipeline end-to-end: validate -> aggregate -> forecast -> charts -> report."""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import CSV_PATH, YEAR_MIN, YEAR_MAX, REPORTS_DIR, TABLES_DIR, FIGURES_DIR
from src.load_data import count_rows
from src.aggregates import save_aggregates
from src.plots import generate_all_figures
from src.forecast import run_forecast_pipeline
from src.report import generate_report

def step(name):
    print(f"\n{'='*60}\n[{name}]\n{'='*60}")

def main():
    t0 = time.time()
    if not CSV_PATH.exists():
        print(f"LOI: Khong tim thay {CSV_PATH}")
        sys.exit(1)

    step("1/5 Kiem tra du lieu")
    counts = count_rows()
    print(f"CSV: {CSV_PATH}")
    print(f"Nam: {YEAR_MIN}-{YEAR_MAX}")
    for y, n in counts.items():
        print(f"  {y}: {n:,}")

    step("2/5 Tong hop (aggregate) - co the mat vai phut")
    paths = save_aggregates()
    for k, v in paths.items():
        print(f"  {k}: {v}")

    step("3/5 Du bao")
    fc = run_forecast_pipeline()
    print(fc.to_string(index=False))

    step("4/5 Ve bieu do")
    figs = generate_all_figures()
    for f in figs:
        print(f"  {f.name}")

    step("5/5 Bao cao")
    report = generate_report()
    print(f"  {report}")

    elapsed = time.time() - t0
    print(f"\nHOAN TAT trong {elapsed/60:.1f} phut.")
    print(f"  Bang: {TABLES_DIR}")
    print(f"  Hinh: {FIGURES_DIR}")
    print(f"  Bao cao: {REPORTS_DIR / 'BAO_CAO.md'}")

if __name__ == "__main__":
    main()
