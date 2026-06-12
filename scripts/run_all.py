"""Pipeline end-to-end: validate -> aggregate -> forecast -> charts -> README."""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import CSV_PATH, YEAR_MIN, YEAR_MAX, PROJECT_ROOT, TABLES_DIR, FIGURES_DIR
from src.load_data import count_rows
from src.aggregates import save_aggregates
from src.plots import generate_all_figures
from src.forecast import run_forecast_pipeline
from src.readme_builder import build_readme
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

    step("2/5 Tong hop (aggregate)")
    save_aggregates()

    step("3/5 Du bao")
    print(run_forecast_pipeline().to_string(index=False))

    step("4/5 Ve bieu do")
    for f in generate_all_figures():
        print(f"  {f.name}")

    step("5/5 Cap nhat README.md va docs/report.md")
    readme = build_readme()
    print(f"  {readme}")
    report = generate_report()
    print(f"  {report}")

    elapsed = time.time() - t0
    print(f"\nHOAN TAT trong {elapsed/60:.1f} phut.")
    print(f"  README: {PROJECT_ROOT / 'README.md'}")
    print(f"  Report: {PROJECT_ROOT / 'docs' / 'report.md'}")
    print(f"  Bang: {TABLES_DIR}")
    print(f"  Hinh: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
