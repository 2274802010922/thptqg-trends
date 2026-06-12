from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .config import MAIN_SUBJECTS, TABLES_DIR


MODEL_LABELS = {
    "naive_last": "Naive: lấy năm gần nhất",
    "moving_average_2": "Trung bình trượt 2 năm",
    "moving_average_3": "Trung bình trượt 3 năm",
    "linear_trend": "Hồi quy tuyến tính",
    "exp_smoothing": "San bằng mũ đơn",
}
MODEL_ORDER = list(MODEL_LABELS)


@dataclass(frozen=True)
class ForecastResult:
    value: float
    lower: float | None = None
    upper: float | None = None


def _prepare_series(series_df: pd.DataFrame, year_col: str = "Nam", value_col: str = "mean") -> pd.DataFrame:
    df = series_df.dropna(subset=[year_col, value_col]).sort_values(year_col).copy()
    df[year_col] = df[year_col].astype(int)
    df[value_col] = df[value_col].astype(float)
    return df


def _clip_score(value: float) -> float:
    return float(np.clip(value, 0.0, 10.0))


def _linear_prediction(years: np.ndarray, values: np.ndarray, next_year: int) -> float:
    x = years.astype(float) - float(years.min())
    x_next = float(next_year) - float(years.min())
    slope, intercept = np.polyfit(x, values.astype(float), 1)
    return _clip_score(intercept + slope * x_next)


def _exp_smoothing_prediction(values: np.ndarray) -> float:
    y = values.astype(float)
    if len(y) < 2:
        return _clip_score(float(y[-1]))

    best_alpha, best_sse = 0.5, float("inf")
    for alpha in np.linspace(0.1, 0.9, 17):
        level = float(y[0])
        sse = 0.0
        for actual in y[1:]:
            forecast = level
            sse += float((actual - forecast) ** 2)
            level = float(alpha * actual + (1 - alpha) * level)
        if sse < best_sse:
            best_alpha, best_sse = float(alpha), sse

    level = float(y[0])
    for actual in y[1:]:
        level = float(best_alpha * actual + (1 - best_alpha) * level)
    return _clip_score(level)


def predict_one_step(years: np.ndarray, values: np.ndarray, next_year: int, model: str) -> float:
    if len(values) == 0:
        raise ValueError("Can it nhat 1 diem thoi gian")
    if model == "naive_last":
        return _clip_score(float(values[-1]))
    if model == "moving_average_2":
        return _clip_score(float(np.mean(values[-min(2, len(values)) :])))
    if model == "moving_average_3":
        return _clip_score(float(np.mean(values[-min(3, len(values)) :])))
    if model == "linear_trend":
        if len(values) < 2:
            return _clip_score(float(values[-1]))
        return _linear_prediction(years, values, next_year)
    if model == "exp_smoothing":
        return _exp_smoothing_prediction(values)
    raise ValueError(f"Khong ho tro model: {model}")


def forecast_model(
    series_df: pd.DataFrame,
    model: str,
    year_col: str = "Nam",
    value_col: str = "mean",
    horizon: int = 1,
) -> pd.DataFrame:
    df = _prepare_series(series_df, year_col, value_col)
    if len(df) < 2:
        raise ValueError("Can it nhat 2 diem thoi gian")

    years = df[year_col].to_numpy(dtype=int)
    values = df[value_col].to_numpy(dtype=float)
    rows = []
    current_years = years.copy()
    current_values = values.copy()
    for step in range(1, horizon + 1):
        next_year = int(years.max() + step)
        pred = predict_one_step(current_years, current_values, next_year, model)
        rows.append({year_col: next_year, "value": round(pred, 4), "type": "forecast", "model": model})
        current_years = np.append(current_years, next_year)
        current_values = np.append(current_values, pred)

    actual = df[[year_col, value_col]].rename(columns={value_col: "value"})
    actual["type"] = "actual"
    actual["model"] = model
    return pd.concat([actual, pd.DataFrame(rows)], ignore_index=True)


def forecast_linear(series_df: pd.DataFrame, year_col: str = "Nam", value_col: str = "mean", horizon: int = 1):
    """Backward-compatible wrapper for the original linear forecast API."""
    return forecast_model(series_df, "linear_trend", year_col=year_col, value_col=value_col, horizon=horizon)


def rolling_backtest(
    series_df: pd.DataFrame,
    year_col: str = "Nam",
    value_col: str = "mean",
    models: list[str] | None = None,
    min_train: int = 3,
) -> pd.DataFrame:
    df = _prepare_series(series_df, year_col, value_col)
    models = models or MODEL_ORDER
    if len(df) <= min_train:
        return pd.DataFrame(
            columns=["test_year", "model", "model_label", "actual", "predicted", "error", "abs_error", "ape"]
        )

    rows = []
    for test_pos in range(min_train, len(df)):
        train = df.iloc[:test_pos]
        test = df.iloc[test_pos]
        years = train[year_col].to_numpy(dtype=int)
        values = train[value_col].to_numpy(dtype=float)
        test_year = int(test[year_col])
        actual = float(test[value_col])
        for model in models:
            predicted = predict_one_step(years, values, test_year, model)
            error = predicted - actual
            rows.append(
                {
                    "test_year": test_year,
                    "model": model,
                    "model_label": MODEL_LABELS[model],
                    "actual": round(actual, 4),
                    "predicted": round(predicted, 4),
                    "error": round(error, 4),
                    "abs_error": round(abs(error), 4),
                    "ape": round(abs(error) / actual * 100, 4) if actual != 0 else np.nan,
                }
            )
    return pd.DataFrame(rows)


def summarize_backtest(backtest: pd.DataFrame) -> pd.DataFrame:
    if backtest.empty:
        return pd.DataFrame(columns=["model", "model_label", "n_backtests", "mae", "rmse", "mape", "bias"])

    rows = []
    for model, g in backtest.groupby("model", sort=False):
        rows.append(
            {
                "model": model,
                "model_label": MODEL_LABELS[model],
                "n_backtests": int(len(g)),
                "mae": round(float(g["abs_error"].mean()), 4),
                "rmse": round(float(np.sqrt(np.mean(np.square(g["error"])))), 4),
                "mape": round(float(g["ape"].mean()), 4) if g["ape"].notna().any() else np.nan,
                "bias": round(float(g["error"].mean()), 4),
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values(["mae", "rmse", "model"], kind="stable").reset_index(drop=True)


def select_best_model(metrics: pd.DataFrame) -> str:
    if metrics.empty:
        return "linear_trend"
    ranked = metrics.copy()
    ranked["order"] = ranked["model"].map({m: i for i, m in enumerate(MODEL_ORDER)})
    ranked = ranked.sort_values(["mae", "rmse", "order"], kind="stable")
    return str(ranked.iloc[0]["model"])


def _prediction_interval(pred: float, metrics_row: pd.Series | None, series_df: pd.DataFrame) -> tuple[float, float]:
    if metrics_row is not None and pd.notna(metrics_row.get("rmse")) and float(metrics_row["rmse"]) > 0:
        radius = 1.96 * float(metrics_row["rmse"])
    else:
        values = _prepare_series(series_df)["mean"].to_numpy(dtype=float)
        radius = float(np.std(values, ddof=1)) if len(values) > 1 else 0.5
    radius = max(radius, 0.15)
    return round(_clip_score(pred - radius), 4), round(_clip_score(pred + radius), 4)


def backtest_last_year(series_df: pd.DataFrame, year_col: str = "Nam", value_col: str = "mean"):
    """Backward-compatible single-year check using the linear trend model."""
    df = _prepare_series(series_df, year_col, value_col)
    if len(df) < 4:
        return {"mae": None}
    test_year = int(df[year_col].max())
    train = df[df[year_col] < test_year]
    test = df[df[year_col] == test_year]
    fc = forecast_linear(train, year_col=year_col, value_col=value_col, horizon=1)
    pred = float(fc.loc[fc["type"] == "forecast", "value"].iloc[0])
    actual = float(test[value_col].iloc[0])
    return {"test_year": test_year, "actual": actual, "predicted": pred, "mae": round(abs(pred - actual), 4)}


def run_forecast_pipeline(tables_dir=TABLES_DIR, subjects=None, horizon: int = 1, min_train: int = 3) -> pd.DataFrame:
    subjects = subjects or MAIN_SUBJECTS
    tables_dir = Path(tables_dir)
    by_ys = pd.read_csv(tables_dir / "by_year_subject.csv")

    forecast_rows, series_rows, metric_rows, backtest_rows = [], [], [], []
    for subject in subjects:
        sub = by_ys[by_ys["Mon"] == subject].dropna(subset=["mean"])
        if sub.empty:
            continue

        bt = rolling_backtest(sub, min_train=min_train)
        if not bt.empty:
            bt = bt.assign(Mon=subject)
            backtest_rows.append(bt)

        metrics = summarize_backtest(bt)
        best_model = select_best_model(metrics)
        if not metrics.empty:
            metrics = metrics.assign(Mon=subject, is_selected=lambda d: d["model"] == best_model)
            metric_rows.append(metrics)

        fc = forecast_model(sub, best_model, horizon=horizon)
        next_row = fc[fc["type"] == "forecast"].iloc[0]
        pred = float(next_row["value"])
        best_metrics = None
        if not metrics.empty and best_model in metrics["model"].values:
            best_metrics = metrics.loc[metrics["model"] == best_model].iloc[0]
        lower, upper = _prediction_interval(pred, best_metrics, sub)

        fc = fc.assign(
            Mon=subject,
            selected_model=best_model,
            selected_model_label=MODEL_LABELS[best_model],
            lower=np.nan,
            upper=np.nan,
        )
        fc.loc[fc["type"] == "forecast", "lower"] = lower
        fc.loc[fc["type"] == "forecast", "upper"] = upper
        series_rows.append(fc)

        last_bt = pd.Series(dtype=object)
        if not bt.empty and best_model in bt["model"].values:
            last_bt = bt[bt["model"] == best_model].sort_values("test_year").iloc[-1]

        forecast_rows.append(
            {
                "Mon": subject,
                "forecast_year": int(next_row["Nam"]),
                "forecast_mean": round(pred, 4),
                "forecast_lower": lower,
                "forecast_upper": upper,
                "selected_model": best_model,
                "selected_model_label": MODEL_LABELS[best_model],
                "backtest_n": int(best_metrics["n_backtests"]) if best_metrics is not None else 0,
                "backtest_mae": float(best_metrics["mae"]) if best_metrics is not None else np.nan,
                "backtest_rmse": float(best_metrics["rmse"]) if best_metrics is not None else np.nan,
                "backtest_mape": float(best_metrics["mape"]) if best_metrics is not None else np.nan,
                "backtest_bias": float(best_metrics["bias"]) if best_metrics is not None else np.nan,
                "backtest_year": int(last_bt["test_year"]) if not last_bt.empty else np.nan,
                "backtest_actual": float(last_bt["actual"]) if not last_bt.empty else np.nan,
                "backtest_predicted": float(last_bt["predicted"]) if not last_bt.empty else np.nan,
                "backtest_abs_error": float(last_bt["abs_error"]) if not last_bt.empty else np.nan,
            }
        )

    forecast_out = pd.DataFrame(forecast_rows)
    forecast_out.to_csv(tables_dir / "forecast_next_year.csv", index=False)

    if series_rows:
        pd.concat(series_rows, ignore_index=True).to_csv(tables_dir / "forecast_series.csv", index=False)
    if metric_rows:
        pd.concat(metric_rows, ignore_index=True).to_csv(tables_dir / "model_comparison.csv", index=False)
    if backtest_rows:
        pd.concat(backtest_rows, ignore_index=True).to_csv(tables_dir / "backtest_predictions.csv", index=False)

    return forecast_out
