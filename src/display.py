"""Cau hinh hien thi dep cho notebook / Colab."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .labels import fmt_float, fmt_int, subject_vi


def setup_display():
    """Go font tieng Viet (Colab) va dinh dang pandas."""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm

        font_path = Path("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf")
        if not font_path.exists():
            import urllib.request
            font_path = Path("/tmp/NotoSans-Regular.ttf")
            if not font_path.exists():
                urllib.request.urlretrieve(
                    "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf",
                    font_path,
                )
            fm.fontManager.addfont(str(font_path))
        plt.rcParams["font.family"] = "Noto Sans"
        plt.rcParams["axes.unicode_minus"] = False
    except Exception:
        pass

    pd.set_option("display.max_columns", 20)
    pd.set_option("display.width", 120)
    pd.set_option("display.float_format", lambda x: fmt_float(x, 2))


def pretty_counts(counts: dict[int, int]) -> pd.DataFrame:
    rows = [{"Năm": y, "Số thí sinh": fmt_int(n), "Số thí sinh (raw)": n} for y, n in sorted(counts.items())]
    return pd.DataFrame(rows)


def pretty_forecast(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["Môn"] = out["Mon"].map(subject_vi)
    out["Năm dự báo"] = out["forecast_year"].astype(int)
    out["Điểm TB dự kiến"] = out["forecast_mean"].map(lambda x: fmt_float(x, 3))
    out["MAE backtest"] = out["backtest_mae"].map(lambda x: fmt_float(x, 4) if pd.notna(x) else "—")
    cols = ["Môn", "Năm dự báo", "Điểm TB dự kiến", "MAE backtest"]
    if "backtest_actual" in out.columns:
        out["Thực tế năm cuối"] = out["backtest_actual"].map(lambda x: fmt_float(x, 3))
        cols.append("Thực tế năm cuối")
    return out[cols]
