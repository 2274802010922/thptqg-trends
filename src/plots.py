from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from .config import FIGURES_DIR, TABLES_DIR, MAIN_SUBJECTS, YEAR_MAX

sns.set_theme(style="whitegrid", font_scale=1.0)

def plot_mean_by_year(by_year_subject, subject="Toan", out_path=None):
    df = by_year_subject[by_year_subject["Mon"] == subject].dropna(subset=["mean"])
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["Nam"], df["mean"], marker="o", linewidth=2)
    ax.set_xlabel("Nam"); ax.set_ylabel("Diem TB"); ax.set_title(f"Xu huong diem TB - {subject}")
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"mean_by_year_{subject}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150); plt.close(fig)
    return out_path

def plot_pct_ge_8(by_year_subject, out_path=None):
    df = by_year_subject[by_year_subject["Mon"].isin(MAIN_SUBJECTS)].dropna(subset=["pct_ge_8"])
    fig, ax = plt.subplots(figsize=(10, 5))
    for mon in MAIN_SUBJECTS:
        s = df[df["Mon"] == mon]
        if not s.empty:
            ax.plot(s["Nam"], s["pct_ge_8"], marker="o", label=mon)
    ax.set_xlabel("Nam"); ax.set_ylabel("% thi sinh >= 8"); ax.set_title("Ty le diem >= 8 theo mon")
    ax.legend(); fig.tight_layout()
    out_path = out_path or FIGURES_DIR / "pct_ge_8_by_year.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150); plt.close(fig)
    return out_path

def plot_candidates_by_year(candidates, out_path=None):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(candidates["Nam"].astype(str), candidates["SoThiSinh"], color="steelblue")
    ax.set_title("So thi sinh theo nam"); fig.tight_layout()
    out_path = out_path or FIGURES_DIR / "candidates_by_year.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150); plt.close(fig)
    return out_path

def plot_heatmap_province(by_yps, year, subject="Toan", out_path=None):
    df = by_yps[(by_yps["Nam"] == year) & (by_yps["Mon"] == subject)].dropna(subset=["mean"])
    pivot = df.pivot_table(index="Tinh", values="mean", aggfunc="first")
    fig, ax = plt.subplots(figsize=(6, 10))
    sns.heatmap(pivot, cmap="YlOrRd", ax=ax)
    ax.set_title(f"{subject} - {year}"); fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"heatmap_{subject}_{year}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150); plt.close(fig)
    return out_path

def plot_forecast(subject, tables_dir=TABLES_DIR, out_path=None):
    tables_dir = Path(tables_dir)
    fc = pd.read_csv(tables_dir / "forecast_series.csv")
    df = fc[fc["Mon"] == subject]
    fig, ax = plt.subplots(figsize=(8, 4))
    actual = df[df["type"] == "actual"]
    pred = df[df["type"] == "forecast"]
    ax.plot(actual["Nam"], actual["value"], marker="o", label="Thuc te")
    ax.plot(list(actual["Nam"].iloc[-1:]) + list(pred["Nam"]), list(actual["value"].iloc[-1:]) + list(pred["value"]), marker="s", linestyle="--", label="Du bao")
    ax.set_title(f"Du bao {subject}"); ax.legend(); fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"forecast_{subject}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150); plt.close(fig)
    return out_path

def generate_all_figures(tables_dir=TABLES_DIR):
    tables_dir = Path(tables_dir)
    by_ys = pd.read_csv(tables_dir / "by_year_subject.csv")
    cand = pd.read_csv(tables_dir / "candidates_by_year.csv")
    by_yps = pd.read_csv(tables_dir / "by_year_province_subject.csv")
    paths = [plot_candidates_by_year(cand), plot_pct_ge_8(by_ys)]
    for s in MAIN_SUBJECTS:
        if s in by_ys["Mon"].values:
            paths.append(plot_mean_by_year(by_ys, s))
    paths.append(plot_heatmap_province(by_yps, year=int(YEAR_MAX), subject="Toan"))
    for s in ["Toan", "NguVan", "NgoaiNgu"]:
        p = FIGURES_DIR / f"forecast_{s}.png"
        if (tables_dir / "forecast_series.csv").exists():
            paths.append(plot_forecast(s, tables_dir))
    return paths
