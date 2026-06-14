from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .config import FIGURES_DIR, MAIN_SUBJECTS, SUBJECT_COLUMNS, TABLES_DIR, YEAR_MAX
from .display import setup_display
from .labels import subject_vi

sns.set_theme(style="whitegrid", font_scale=1.0)


def _apply_font():
    setup_display()


def _subjects_with_data(by_year_subject: pd.DataFrame) -> list[str]:
    ok = by_year_subject.groupby("Mon")["count"].sum()
    return [m for m in SUBJECT_COLUMNS if m in ok.index and ok[m] > 0]


def plot_mean_by_year(by_year_subject, subject="Toan", out_path=None):
    _apply_font()
    df = by_year_subject[by_year_subject["Mon"] == subject].dropna(subset=["mean"]).sort_values("Nam")
    if df.empty:
        return None
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(df["Nam"], df["mean"], marker="o", linewidth=2, color="#2563eb")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Điểm trung bình")
    ax.set_title(f"Xu hướng điểm TB — {subject_vi(subject)}")
    ax.set_xticks(df["Nam"])
    for _, row in df.iterrows():
        ax.annotate(
            f"{row['mean']:.2f}",
            (row["Nam"], row["mean"]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8,
        )
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"mean_by_year_{subject}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_pct_ge_8(by_year_subject, subjects=None, out_path=None):
    _apply_font()
    subjects = subjects or _subjects_with_data(by_year_subject)
    df = by_year_subject[by_year_subject["Mon"].isin(subjects)].dropna(subset=["pct_ge_8"])
    fig, ax = plt.subplots(figsize=(12, 6))
    for mon in subjects:
        s = df[df["Mon"] == mon].sort_values("Nam")
        if not s.empty:
            ax.plot(s["Nam"], s["pct_ge_8"], marker="o", label=subject_vi(mon))
    ax.set_xlabel("Năm")
    ax.set_ylabel("Tỷ lệ thí sinh đạt >= 8 (%)")
    ax.set_title("Tỷ lệ điểm >= 8 — tất cả các môn có dữ liệu")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=8)
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / "pct_ge_8_by_year.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
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
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            fmt_int_label(val),
            ha="center",
            va="bottom",
            fontsize=8,
        )
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
    if df.empty:
        return None
    pivot = df.pivot_table(index="Tinh", values="mean", aggfunc="first")
    fig, ax = plt.subplots(figsize=(6, 10))
    sns.heatmap(pivot, cmap="YlOrRd", ax=ax, cbar_kws={"label": "Điểm TB"})
    ax.set_title(f"Phân bố theo tỉnh — {subject_vi(subject)} ({year})")
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
    if df.empty:
        return None
    fig, ax = plt.subplots(figsize=(9, 4.5))
    actual = df[df["type"] == "actual"]
    pred = df[df["type"] == "forecast"]
    ax.plot(actual["Nam"], actual["value"], marker="o", label="Thực tế", color="#2563eb")
    ax.plot(
        list(actual["Nam"].iloc[-1:]) + list(pred["Nam"]),
        list(actual["value"].iloc[-1:]) + list(pred["value"]),
        marker="s",
        linestyle="--",
        label="Dự báo",
        color="#dc2626",
    )
    if not pred.empty and {"lower", "upper"}.issubset(pred.columns):
        pi = pred.dropna(subset=["lower", "upper"])
        if not pi.empty:
            x = pd.to_numeric(pi["Nam"])
            lower = pd.to_numeric(pi["lower"])
            upper = pd.to_numeric(pi["upper"])
            ax.fill_between(x, lower, upper, color="#dc2626", alpha=0.12, label="Khoảng dự báo")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Điểm TB")
    model_label = ""
    if "selected_model_label" in df.columns and df["selected_model_label"].notna().any():
        model_label = f" ({df['selected_model_label'].dropna().iloc[0]})"
    ax.set_title(f"Dự báo — {subject_vi(subject)}{model_label}")
    ax.legend()
    for _, row in actual.iterrows():
        ax.annotate(
            f"{row['value']:.2f}",
            (row["Nam"], row["value"]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8,
        )
    if not pred.empty:
        row = pred.iloc[0]
        ax.annotate(
            f"{row['value']:.2f}",
            (row["Nam"], row["value"]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8,
            color="#dc2626",
        )
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"forecast_{subject}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def _exists(tables_dir: Path, name: str) -> bool:
    return (tables_dir / name).exists()


def plot_data_quality_missingness(tables_dir=TABLES_DIR, out_path=None):
    _apply_font()
    tables_dir = Path(tables_dir)
    path = tables_dir / "missing_by_subject_year.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    last = df[df["Nam"] == int(YEAR_MAX)].copy()
    if last.empty:
        return None
    last["Môn"] = last["Mon"].map(subject_vi)
    last = last.sort_values("zero_pct", ascending=False)
    fig, ax = plt.subplots(figsize=(12, 5.5))
    x = np.arange(len(last))
    ax.bar(x, last["zero_pct"], label="0.0 (không thi)", color="#f59e0b")
    ax.bar(x, last["missing_pct"], bottom=last["zero_pct"], label="Thiếu/null", color="#64748b")
    ax.set_xticks(x)
    ax.set_xticklabels(last["Môn"], rotation=45, ha="right")
    ax.set_ylabel("Tỷ lệ trên tổng dòng (%)")
    ax.set_title(f"Data quality theo môn ({YEAR_MAX})")
    ax.legend()
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / "data_quality_missingness.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_score_bands(subject, tables_dir=TABLES_DIR, out_path=None):
    _apply_font()
    tables_dir = Path(tables_dir)
    path = tables_dir / "score_bands_by_year_subject.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    s = df[df["Mon"] == subject].sort_values("Nam")
    if s.empty:
        return None
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.stackplot(
        s["Nam"],
        s["pct_lt_5"],
        s["pct_5_to_6_5"],
        s["pct_6_5_to_8"],
        s["pct_ge_8"],
        labels=["<5", "5-6.5", "6.5-8", ">=8"],
        colors=["#ef4444", "#f59e0b", "#3b82f6", "#16a34a"],
        alpha=0.82,
    )
    ax.set_ylim(0, 100)
    ax.set_xticks(s["Nam"])
    ax.set_ylabel("Tỷ lệ thí sinh có thi môn (%)")
    ax.set_title(f"Cơ cấu dải điểm — {subject_vi(subject)}")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=4)
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"score_bands_{subject}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_histogram_from_hist(subject, year=YEAR_MAX, tables_dir=TABLES_DIR, out_path=None):
    _apply_font()
    tables_dir = Path(tables_dir)
    path = tables_dir / "score_histogram_by_year_subject.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    s = df[(df["Mon"] == subject) & (df["Nam"] == int(year))].sort_values("score")
    if s.empty:
        return None
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.bar(s["score"], s["count"], width=0.08, color="#2563eb", alpha=0.85)
    ax.set_xlim(0, 10)
    ax.set_xlabel("Điểm")
    ax.set_ylabel("Số thí sinh")
    ax.set_title(f"Phân phối điểm — {subject_vi(subject)} ({year})")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"histogram_{subject}_{year}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_boxplot_from_distribution(subject, tables_dir=TABLES_DIR, out_path=None):
    _apply_font()
    tables_dir = Path(tables_dir)
    path = tables_dir / "score_distribution_by_year_subject.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    s = df[df["Mon"] == subject].dropna(subset=["median", "p25", "p75"]).sort_values("Nam")
    if s.empty:
        return None
    stats = []
    for _, row in s.iterrows():
        stats.append(
            {
                "label": str(int(row["Nam"])),
                "med": float(row["median"]),
                "q1": float(row["p25"]),
                "q3": float(row["p75"]),
                "whislo": float(row["p10"]),
                "whishi": float(row["p90"]),
                "fliers": [],
            }
        )
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.bxp(stats, showfliers=False, patch_artist=True, boxprops={"facecolor": "#bfdbfe", "edgecolor": "#1d4ed8"})
    ax.set_ylim(0, 10)
    ax.set_xlabel("Năm")
    ax.set_ylabel("Điểm (P10-P90, hộp P25-P75)")
    ax.set_title(f"Boxplot xấp xỉ theo percentile — {subject_vi(subject)}")
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"boxplot_{subject}_by_year.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_yoy_change_heatmap(tables_dir=TABLES_DIR, out_path=None):
    _apply_font()
    tables_dir = Path(tables_dir)
    path = tables_dir / "yearly_change_by_subject.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path).dropna(subset=["mean_change_pct"])
    if df.empty:
        return None
    df["Môn"] = df["Mon"].map(subject_vi)
    pivot = df.pivot_table(index="Môn", columns="Nam", values="mean_change_pct", aggfunc="first")
    fig, ax = plt.subplots(figsize=(9, max(5, len(pivot) * 0.45)))
    sns.heatmap(pivot, cmap="RdBu_r", center=0, annot=True, fmt=".1f", cbar_kws={"label": "% thay đổi ĐTB"}, ax=ax)
    ax.set_title("Biến động điểm trung bình so với năm trước")
    ax.set_xlabel("Năm")
    ax.set_ylabel("")
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / "yoy_change_heatmap.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_region_comparison(subject, tables_dir=TABLES_DIR, out_path=None):
    _apply_font()
    tables_dir = Path(tables_dir)
    path = tables_dir / "by_region_subject_year.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    s = df[df["Mon"] == subject].sort_values(["Vung", "Nam"])
    if s.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 5.2))
    for region, g in s.groupby("Vung"):
        ax.plot(g["Nam"], g["mean"], marker="o", linewidth=2, label=region)
    ax.set_xticks(sorted(s["Nam"].unique()))
    ax.set_ylabel("Điểm trung bình")
    ax.set_title(f"So sánh vùng — {subject_vi(subject)}")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, fontsize=8)
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"region_comparison_{subject}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_province_volatility(subject, tables_dir=TABLES_DIR, out_path=None):
    _apply_font()
    tables_dir = Path(tables_dir)
    path = tables_dir / "province_volatility.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    s = df[df["Mon"] == subject].sort_values("max_yoy_abs_change", ascending=False).head(12)
    if s.empty:
        return None
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.barh(s["TenTinh"].astype(str)[::-1], s["max_yoy_abs_change"][::-1], color="#dc2626", alpha=0.85)
    ax.set_xlabel("Mức biến động tuyệt đối lớn nhất giữa hai năm")
    ax.set_title(f"Tỉnh biến động mạnh nhất — {subject_vi(subject)}")
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"province_volatility_{subject}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_correlation_heatmap(year=YEAR_MAX, tables_dir=TABLES_DIR, out_path=None):
    _apply_font()
    tables_dir = Path(tables_dir)
    path = tables_dir / "subject_correlation_by_year.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    s = df[df["Nam"] == int(year)]
    if s.empty:
        return None
    subjects = sorted(set(s["MonX"]).union(set(s["MonY"])), key=lambda x: subject_vi(x))
    mat = pd.DataFrame(np.eye(len(subjects)), index=subjects, columns=subjects)
    for _, row in s.iterrows():
        mat.loc[row["MonX"], row["MonY"]] = row["correlation"]
        mat.loc[row["MonY"], row["MonX"]] = row["correlation"]
    mat.index = [subject_vi(x) for x in mat.index]
    mat.columns = [subject_vi(x) for x in mat.columns]
    fig, ax = plt.subplots(figsize=(9, 7.5))
    sns.heatmap(mat.astype(float), cmap="RdBu_r", vmin=-1, vmax=1, center=0, annot=True, fmt=".2f", ax=ax)
    ax.set_title(f"Tương quan điểm giữa các môn ({year})")
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"correlation_heatmap_{year}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_combination_trends(tables_dir=TABLES_DIR, out_path=None):
    _apply_font()
    tables_dir = Path(tables_dir)
    path = tables_dir / "combination_scores_by_year.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    combos = ["KhoiA", "KhoiA1", "KhoiB", "KhoiC", "KhoiD", "KHTN", "KHXH"]
    s = df[df["ToHop"].isin(combos)].sort_values(["ToHop", "Nam"])
    if s.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 5.2))
    for combo, g in s.groupby("ToHop"):
        ax.plot(g["Nam"], g["mean"], marker="o", linewidth=2, label=combo)
    ax.set_xticks(sorted(s["Nam"].unique()))
    ax.set_ylabel("Điểm trung bình tổ hợp")
    ax.set_title("Xu hướng điểm theo tổ hợp/khối thi")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=4)
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / "combination_trends.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_backtest_actual_vs_predicted(subject, tables_dir=TABLES_DIR, out_path=None):
    _apply_font()
    tables_dir = Path(tables_dir)
    bt_path = tables_dir / "backtest_predictions.csv"
    fc_path = tables_dir / "forecast_next_year.csv"
    if not bt_path.exists() or not fc_path.exists():
        return None
    bt = pd.read_csv(bt_path)
    forecast = pd.read_csv(fc_path)
    if subject not in set(forecast["Mon"]):
        return None
    model = forecast.loc[forecast["Mon"] == subject, "selected_model"].iloc[0]
    s = bt[(bt["Mon"] == subject) & (bt["model"] == model)].sort_values("test_year")
    if s.empty:
        return None
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(s["test_year"], s["actual"], marker="o", label="Thực tế", color="#2563eb")
    ax.plot(s["test_year"], s["predicted"], marker="s", linestyle="--", label="Dự đoán backtest", color="#dc2626")
    ax.set_xticks(s["test_year"])
    ax.set_ylabel("Điểm trung bình")
    ax.set_title(f"Backtest actual vs predicted — {subject_vi(subject)}")
    ax.legend()
    fig.tight_layout()
    out_path = out_path or FIGURES_DIR / f"backtest_actual_vs_predicted_{subject}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def generate_all_figures(tables_dir=TABLES_DIR):
    tables_dir = Path(tables_dir)
    by_ys = pd.read_csv(tables_dir / "by_year_subject.csv")
    cand = pd.read_csv(tables_dir / "candidates_by_year.csv")
    by_yps = pd.read_csv(tables_dir / "by_year_province_subject.csv")
    subjects = _subjects_with_data(by_ys)

    paths = []
    p = plot_candidates_by_year(cand)
    if p:
        paths.append(p)
    p = plot_pct_ge_8(by_ys, subjects=subjects)
    if p:
        paths.append(p)

    for s in subjects:
        p = plot_mean_by_year(by_ys, s)
        if p:
            paths.append(p)

    for s in MAIN_SUBJECTS:
        p = plot_heatmap_province(by_yps, year=int(YEAR_MAX), subject=s)
        if p:
            paths.append(p)

    if (tables_dir / "forecast_series.csv").exists():
        fc = pd.read_csv(tables_dir / "forecast_series.csv")
        for s in fc["Mon"].unique():
            p = plot_forecast(s, tables_dir)
            if p:
                paths.append(p)

    for plotter in [plot_data_quality_missingness, plot_yoy_change_heatmap, plot_combination_trends]:
        p = plotter(tables_dir)
        if p:
            paths.append(p)

    if _exists(tables_dir, "score_bands_by_year_subject.csv"):
        for s in subjects:
            p = plot_score_bands(s, tables_dir)
            if p:
                paths.append(p)

    if _exists(tables_dir, "score_histogram_by_year_subject.csv"):
        for s in subjects:
            p = plot_histogram_from_hist(s, YEAR_MAX, tables_dir)
            if p:
                paths.append(p)

    if _exists(tables_dir, "score_distribution_by_year_subject.csv"):
        for s in subjects:
            p = plot_boxplot_from_distribution(s, tables_dir)
            if p:
                paths.append(p)

    if _exists(tables_dir, "by_region_subject_year.csv"):
        for s in MAIN_SUBJECTS:
            p = plot_region_comparison(s, tables_dir)
            if p:
                paths.append(p)

    if _exists(tables_dir, "province_volatility.csv"):
        for s in MAIN_SUBJECTS:
            p = plot_province_volatility(s, tables_dir)
            if p:
                paths.append(p)

    if _exists(tables_dir, "subject_correlation_by_year.csv"):
        for y in sorted(by_ys["Nam"].unique()):
            p = plot_correlation_heatmap(int(y), tables_dir)
            if p:
                paths.append(p)

    if _exists(tables_dir, "backtest_predictions.csv") and _exists(tables_dir, "forecast_next_year.csv"):
        fc = pd.read_csv(tables_dir / "forecast_next_year.csv")
        for s in fc["Mon"].unique():
            p = plot_backtest_actual_vs_predicted(s, tables_dir)
            if p:
                paths.append(p)

    return paths
