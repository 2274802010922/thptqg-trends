"""Pipeline end-to-end: validate -> aggregate -> forecast -> charts -> README."""
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import CSV_PATH, YEAR_MIN, YEAR_MAX, PROJECT_ROOT, TABLES_DIR, FIGURES_DIR
from src.load_data import count_rows
from src.aggregates import save_aggregates
from src.advanced_analysis import build_forecast_reliability, generate_da_tables, write_analysis_questions
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

    step("1/7 Kiem tra du lieu")
    counts = count_rows()
    print(f"CSV: {CSV_PATH}")
    print(f"Nam: {YEAR_MIN}-{YEAR_MAX}")
    for y, n in counts.items():
        print(f"  {y}: {n:,}")

    step("2/7 Tong hop (aggregate)")
    save_aggregates()

    step("3/7 Phan tich DA nang cao")
    for name, path in generate_da_tables().items():
        print(f"  {name}: {path.name}")
    questions = write_analysis_questions()
    print(f"  analysis_questions: {questions}")

    step("4/7 Du bao")
    print(run_forecast_pipeline().to_string(index=False))
    reliability = build_forecast_reliability()
    print(f"  forecast_reliability: {reliability.name}")

    step("5/7 Ve bieu do")
    for f in generate_all_figures():
        print(f"  {f.name}")

    step("6/7 Cap nhat README.md va docs/report.md")
    readme = build_readme()
    print(f"  {readme}")
    report = generate_report()
    print(f"  {report}")

    step("7/7 Hoan tat")
    elapsed = time.time() - t0
    print(f"\nHOAN TAT trong {elapsed/60:.1f} phut.")
    print(f"  README: {PROJECT_ROOT / 'README.md'}")
    print(f"  Report: {PROJECT_ROOT / 'docs' / 'report.md'}")
    print(f"  Bang: {TABLES_DIR}")
    print(f"  Hinh: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
