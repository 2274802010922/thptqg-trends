from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .config import FIGURES_DIR, MAIN_SUBJECTS, TABLES_DIR, YEAR_MAX
from .display import setup_display
from .labels import subject_vi

sns.set_theme(style="whitegrid", font_scale=1.0)


def _apply_font():
    setup_display()


def plot_mean_by_year(by_year_subject, subject="Toan", out_path=None):
    _apply_font()
    df = by_year_subject[by_year_subject["Mon"] == subject].dropna(subset=["mean"])
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(df["Nam"], df["mean"], marker="o", linewidth=2, color="#2563eb")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Điểm trung bình")
    ax.set_title(f"Xu hướng điểm TB — {subject_vi(subject)}")
    ax.set_xticks(df["Nam"])
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"mean_by_year_{subject}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_pct_ge_8(by_year_subject, out_path=None):
    _apply_font()
    df = by_year_subject[by_year_subject["Mon"].isin(MAIN_SUBJECTS)].dropna(subset=["pct_ge_8"])
    fig, ax = plt.subplots(figsize=(10, 5))
    for mon in MAIN_SUBJECTS:
        s = df[df["Mon"] == mon]
        if not s.empty:
            ax.plot(s["Nam"], s["pct_ge_8"], marker="o", label=subject_vi(mon))
    ax.set_xlabel("Năm")
    ax.set_ylabel("Tỷ lệ thí sinh đạt ≥ 8 (%)")
    ax.set_title("Tỷ lệ điểm ≥ 8 theo môn")
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / "pct_ge_8_by_year.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_candidates_by_year(candidates, out_path=None):
    _apply_font()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.bar(candidates["Nam"].astype(str), candidates["SoThiSinh"], color="#0ea5e9")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Số thí sinh")
    ax.set_title("Số thí sinh theo năm")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    for bar, val in zip(bars, candidates["SoThiSinh"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), fmt_int_label(val),
                ha="center", va="bottom", fontsize=8, rotation=0)
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / "candidates_by_year.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def fmt_int_label(n):
    return f"{int(n/1000):,.0f}k".replace(",", ".") if n >= 1000 else str(int(n))


def plot_heatmap_province(by_yps, year, subject="Toan", out_path=None):
    _apply_font()
    df = by_yps[(by_yps["Nam"] == year) & (by_yps["Mon"] == subject)].dropna(subset=["mean"])
    pivot = df.pivot_table(index="Tinh", values="mean", aggfunc="first")
    fig, ax = plt.subplots(figsize=(6, 10))
    sns.heatmap(pivot, cmap="YlOrRd", ax=ax, cbar_kws={"label": "Điểm TB"})
    ax.set_title(f"{subject_vi(subject)} — {year}")
    ax.set_ylabel("Mã tỉnh")
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"heatmap_{subject}_{year}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_forecast(subject, tables_dir=TABLES_DIR, out_path=None):
    _apply_font()
    tables_dir = Path(tables_dir)
    fc = pd.read_csv(tables_dir / "forecast_series.csv")
    df = fc[fc["Mon"] == subject]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    actual = df[df["type"] == "actual"]
    pred = df[df["type"] == "forecast"]
    ax.plot(actual["Nam"], actual["value"], marker="o", label="Thực tế", color="#2563eb")
    ax.plot(
        list(actual["Nam"].iloc[-1:]) + list(pred["Nam"]),
        list(actual["value"].iloc[-1:]) + list(pred["value"]),
        marker="s", linestyle="--", label="Dự báo", color="#dc2626",
    )
    ax.set_xlabel("Năm")
    ax.set_ylabel("Điểm TB")
    ax.set_title(f"Dự báo — {subject_vi(subject)}")
    ax.legend()
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"forecast_{subject}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
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
    if (tables_dir / "forecast_series.csv").exists():
        for s in ["Toan", "NguVan", "NgoaiNgu"]:
            paths.append(plot_forecast(s, tables_dir))
    return paths
