from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from .config import TABLES_DIR, MAIN_SUBJECTS

def forecast_linear(series_df, year_col="Nam", value_col="mean", horizon=1):
    df = series_df.dropna(subset=[value_col]).sort_values(year_col)
    if len(df) < 3:
        raise ValueError("Can it nhat 3 diem thoi gian")
    X = df[[year_col]].values
    y = df[value_col].values
    model = LinearRegression().fit(X, y)
    last_year = int(df[year_col].max())
    future_years = [last_year + i for i in range(1, horizon + 1)]
    preds = model.predict(np.array(future_years).reshape(-1, 1))
    actual = df[[year_col, value_col]].rename(columns={value_col: "value"})
    actual["type"] = "actual"
    forecast = pd.DataFrame({year_col: future_years, "value": np.round(preds, 4), "type": "forecast"})
    return pd.concat([actual, forecast], ignore_index=True)

def backtest_last_year(series_df, year_col="Nam", value_col="mean"):
    df = series_df.dropna(subset=[value_col]).sort_values(year_col)
    if len(df) < 4:
        return {"mae": None}
    test_year = int(df[year_col].max())
    train = df[df[year_col] < test_year]
    test = df[df[year_col] == test_year]
    fc = forecast_linear(train, year_col=year_col, value_col=value_col, horizon=1)
    pred = float(fc.loc[fc["type"] == "forecast", "value"].iloc[0])
    actual = float(test[value_col].iloc[0])
    return {"test_year": test_year, "actual": actual, "predicted": pred, "mae": round(abs(pred - actual), 4)}

def run_forecast_pipeline(tables_dir=TABLES_DIR, subjects=None):
    subjects = subjects or MAIN_SUBJECTS
    tables_dir = Path(tables_dir)
    by_ys = pd.read_csv(tables_dir / "by_year_subject.csv")
    rows, series_rows = [], []
    for subject in subjects:
        sub = by_ys[by_ys["Mon"] == subject]
        if sub.empty:
            continue
        bt = backtest_last_year(sub)
        fc = forecast_linear(sub, horizon=1)
        fc = fc.assign(Mon=subject)
        series_rows.append(fc)
        nxt = fc[fc["type"] == "forecast"].iloc[0]
        rows.append({
            "Mon": subject,
            "forecast_year": int(nxt["Nam"]),
            "forecast_mean": float(nxt["value"]),
            "backtest_year": bt.get("test_year"),
            "backtest_actual": bt.get("actual"),
            "backtest_predicted": bt.get("predicted"),
            "backtest_mae": bt.get("mae"),
        })
    out = pd.DataFrame(rows)
    out.to_csv(tables_dir / "forecast_next_year.csv", index=False)
    if series_rows:
        pd.concat(series_rows, ignore_index=True).to_csv(tables_dir / "forecast_series.csv", index=False)
    return out
