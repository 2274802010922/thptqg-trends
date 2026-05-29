"""Tao bao cao Markdown tu bang aggregate va du bao."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import json
import pandas as pd
from .config import CSV_PATH, TABLES_DIR, YEAR_MIN, YEAR_MAX, REPORTS_DIR

def _pct_change(first, last):
    if first is None or last is None or first == 0:
        return None
    return round((last - first) / first * 100, 2)

def build_trends_table(by_year_subject: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mon, g in by_year_subject.groupby("Mon"):
        g = g.dropna(subset=["mean"]).sort_values("Nam")
        if g.empty:
            continue
        first, last = g.iloc[0], g.iloc[-1]
        rows.append({
            "Mon": mon,
            "mean_first": first["mean"], "mean_last": last["mean"],
            "change_pct": _pct_change(first["mean"], last["mean"]),
            "pct_ge_8_first": first.get("pct_ge_8"), "pct_ge_8_last": last.get("pct_ge_8"),
        })
    return pd.DataFrame(rows).sort_values("Mon")

def top_bottom_provinces(named: pd.DataFrame, year: int, subject: str = "Toan", n: int = 10):
    df = named[(named["Nam"] == year) & (named["Mon"] == subject)].dropna(subset=["mean"])
    df = df.sort_values("mean", ascending=False)
    top = df.head(n)[["TenTinh", "mean", "count"]]
    bottom = df.tail(n).sort_values("mean")[["TenTinh", "mean", "count"]]
    return top, bottom

def generate_report(out_path: Path | None = None) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = out_path or REPORTS_DIR / "BAO_CAO.md"
    tables = Path(TABLES_DIR)
    by_ys = pd.read_csv(tables / "by_year_subject.csv")
    cand = pd.read_csv(tables / "candidates_by_year.csv")
    named = pd.read_csv(tables / "by_year_province_subject_named.csv")
    forecast = pd.read_csv(tables / "forecast_next_year.csv")
    trends = build_trends_table(by_ys)
    trends.to_csv(tables / "trends_summary.csv", index=False)
    top, bottom = top_bottom_provinces(named, YEAR_MAX, "Toan")
    lines = [
        "# Bao cao phan tich diem THPT quoc gia",
        "",
        f"**Ngay tao:** {datetime.now():%Y-%m-%d %H:%M}",
        f"**Du lieu:** `{CSV_PATH}`",
        f"**Pham vi:** {YEAR_MIN} - {YEAR_MAX}",
        "",
        "## 1. Tong quan",
        "",
        f"- Tong thi sinh 5 nam: **{int(cand['SoThiSinh'].sum()):,}**",
    ]
    for _, r in cand.iterrows():
        lines.append(f"- Nam {int(r['Nam'])}: {int(r['SoThiSinh']):,}")
    lines += ["", "## 2. Xu huong diem TB", "", "| Mon | TB dau | TB cuoi | Doi (%) | %>=8 cuoi |", "|-----|--------|---------|---------|-----------|"]
    for _, r in trends.iterrows():
        ch = r["change_pct"]
        chs = f"{ch:+.2f}%" if pd.notna(ch) else "-"
        p8 = f"{r['pct_ge_8_last']:.1f}%" if pd.notna(r.get("pct_ge_8_last")) else "-"
        lines.append(f"| {r['Mon']} | {r['mean_first']:.2f} | {r['mean_last']:.2f} | {chs} | {p8} |")
    lines += ["", f"## 3. Top 10 tinh - Toan {YEAR_MAX}", ""]
    for _, r in top.iterrows():
        lines.append(f"- **{r['TenTinh']}**: {r['mean']:.2f} (n={int(r['count']):,})")
    lines += ["", f"## 4. Bottom 10 tinh - Toan {YEAR_MAX}", ""]
    for _, r in bottom.iterrows():
        lines.append(f"- **{r['TenTinh']}**: {r['mean']:.2f} (n={int(r['count']):,})")
    lines += ["", "## 5. Du bao", "", "| Mon | Nam | Du kien | MAE backtest |", "|-----|-----|---------|--------------|"]
    for _, r in forecast.iterrows():
        mae = f"{r['backtest_mae']:.4f}" if pd.notna(r.get("backtest_mae")) else "-"
        lines.append(f"| {r['Mon']} | {int(r['forecast_year'])} | {r['forecast_mean']:.3f} | {mae} |")
    lines += [
        "",
        "## 6. Hinh anh",
        "",
        "Xem thu muc `outputs/figures/`.",
        "",
        "## 7. Gioi han",
        "",
        "- Gia dinh co che thi on dinh.",
        "- Diem 0.0 = khong thi mon.",
        "- Du bao tren tong hop, khong phai ca nhan.",
        "",
        "---",
        "Chay lai: python scripts/run_all.py",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    profile = {
        "csv": str(CSV_PATH),
        "year_min": YEAR_MIN,
        "year_max": YEAR_MAX,
        "total_candidates": int(cand["SoThiSinh"].sum()),
        "generated_at": datetime.now().isoformat(),
    }
    (tables / "data_profile.json").write_text(json.dumps(profile, indent=2), encoding="utf-8")
    return out_path
