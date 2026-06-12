import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.load_data import count_rows
from src.aggregates import save_aggregates
from src.plots import generate_all_figures
from src.forecast import run_forecast_pipeline
from src.readme_builder import build_readme
from src.report import generate_report

def main():
    print("Dem theo nam:", count_rows())
    print("Luu aggregate...")
    paths = save_aggregates()
    for k, v in paths.items():
        print(f"  {k}: {v}")
    print("Ve bieu do...")
    figs = generate_all_figures()
    for f in figs:
        print(f"  {f}")
    print("Du bao...")
    fc = run_forecast_pipeline()
    print(fc.to_string(index=False))
    print("Cap nhat bao cao...")
    print(f"  {build_readme()}")
    print(f"  {generate_report()}")
    print("Xong.")

if __name__ == "__main__":
    main()
