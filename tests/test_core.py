import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.advanced_analysis import _distribution_from_hist, _score_bands_from_hist, build_forecast_reliability
from src.aggregates import _add_series, _finalize_bucket, _new_bucket
from src.forecast import rolling_backtest, run_forecast_pipeline
from src.load_data import filter_years


class CorePipelineTests(unittest.TestCase):
    def test_filter_years_keeps_requested_range(self):
        df = pd.DataFrame({"Nam": [2020, 2021, 2022, 2025, 2026]})
        out = filter_years(df, 2021, 2025)
        self.assertEqual(out["Nam"].tolist(), [2021, 2022, 2025])

    def test_zero_scores_are_excluded_from_subject_stats(self):
        bucket = _new_bucket()
        _add_series(bucket, pd.Series([0.0, 5.0, 8.0, 9.0, None]))
        out = _finalize_bucket(bucket)
        self.assertEqual(out["count"], 3)
        self.assertAlmostEqual(out["mean"], 7.3333, places=4)
        self.assertAlmostEqual(out["pct_ge_8"], 66.67, places=2)

    def test_rolling_backtest_compares_models(self):
        df = pd.DataFrame(
            {
                "Nam": [2021, 2022, 2023, 2024, 2025],
                "mean": [6.0, 6.2, 6.4, 6.5, 6.7],
            }
        )
        bt = rolling_backtest(df)
        self.assertFalse(bt.empty)
        self.assertIn("linear_trend", set(bt["model"]))
        self.assertIn(2025, set(bt["test_year"]))

    def test_forecast_pipeline_writes_expected_outputs(self):
        by_year_subject = pd.DataFrame(
            {
                "Nam": [2021, 2022, 2023, 2024, 2025],
                "Mon": ["Toan"] * 5,
                "count": [100] * 5,
                "mean": [6.0, 6.1, 6.2, 6.4, 6.5],
                "median": [None] * 5,
                "std": [1.0] * 5,
                "pct_ge_8": [10, 11, 12, 13, 14],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            by_year_subject.to_csv(tmp_path / "by_year_subject.csv", index=False)
            out = run_forecast_pipeline(tmp_path, subjects=["Toan"])
            self.assertEqual(len(out), 1)
            self.assertTrue((tmp_path / "forecast_next_year.csv").exists())
            self.assertTrue((tmp_path / "forecast_series.csv").exists())
            self.assertTrue((tmp_path / "model_comparison.csv").exists())
            self.assertTrue((tmp_path / "backtest_predictions.csv").exists())

    def test_distribution_from_hist_computes_percentiles(self):
        hist = {
            (2025, "Toan", 4.0): 1,
            (2025, "Toan", 6.0): 2,
            (2025, "Toan", 8.0): 1,
            (2025, "Toan", 9.0): 1,
        }
        out = _distribution_from_hist(hist)
        row = out.iloc[0]
        self.assertEqual(row["count"], 5)
        self.assertEqual(row["median"], 6.0)
        self.assertEqual(row["p90"], 9.0)

    def test_score_bands_from_hist(self):
        hist = {
            (2025, "Toan", 4.0): 1,
            (2025, "Toan", 5.5): 1,
            (2025, "Toan", 7.0): 1,
            (2025, "Toan", 8.0): 1,
        }
        out = _score_bands_from_hist(hist)
        row = out.iloc[0]
        self.assertEqual(row["count_lt_5"], 1)
        self.assertEqual(row["count_5_to_6_5"], 1)
        self.assertEqual(row["count_6_5_to_8"], 1)
        self.assertEqual(row["count_ge_8"], 1)

    def test_forecast_reliability_writes_label(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pd.DataFrame(
                [
                    {
                        "Mon": "Toan",
                        "forecast_year": 2026,
                        "forecast_mean": 6.0,
                        "forecast_lower": 5.5,
                        "forecast_upper": 6.5,
                        "selected_model": "naive_last",
                        "selected_model_label": "Naive",
                        "backtest_n": 2,
                        "backtest_mae": 0.2,
                        "backtest_rmse": 0.25,
                        "backtest_mape": 3.0,
                    }
                ]
            ).to_csv(tmp_path / "forecast_next_year.csv", index=False)
            out_path = build_forecast_reliability(tmp_path)
            out = pd.read_csv(out_path)
            self.assertEqual(len(out), 1)
            self.assertIn(out.loc[0, "reliability_label"], {"Thấp", "Trung bình", "Tương đối"})


if __name__ == "__main__":
    unittest.main()
