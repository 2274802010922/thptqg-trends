import tempfile
import unittest
from pathlib import Path

import pandas as pd

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


if __name__ == "__main__":
    unittest.main()
