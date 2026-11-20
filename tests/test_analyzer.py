"""Focused tests for data cleaning and stock analysis calculations."""

import unittest

import pandas as pd

from src.analyzer import analyze_stock_data
from src.data_loader import clean_stock_data


class StockAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.raw = pd.DataFrame(
            {
                "Date": ["2024-01-03", "2024-01-01", "2024-01-02"],
                "Close": [121.0, 100.0, 110.0],
                "Adj Close": [121.0, 100.0, 110.0],
                "High": [123.0, 102.0, 112.0],
                "Low": [119.0, 98.0, 108.0],
                "Volume": [1000, 900, 950],
            }
        )

    def test_cleaning_sorts_dates_and_uses_adjusted_price(self):
        cleaned = clean_stock_data(self.raw)
        self.assertEqual(cleaned.index[0], pd.Timestamp("2024-01-01"))
        self.assertEqual(cleaned["Analysis Price"].tolist(), [100.0, 110.0, 121.0])

    def test_analysis_computes_returns_moving_averages_and_summary(self):
        cleaned = clean_stock_data(self.raw)
        analysis, summary = analyze_stock_data(
            cleaned, "demo", moving_average_windows=(2,)
        )
        self.assertAlmostEqual(analysis["Daily Return"].iloc[1], 0.10)
        self.assertAlmostEqual(analysis["SMA 2"].iloc[1], 105.0)
        self.assertAlmostEqual(summary["total_return"], 0.21)
        self.assertEqual(summary["ticker"], "DEMO")
        self.assertEqual(summary["highest_price"], 123.0)
        self.assertEqual(summary["lowest_price"], 98.0)

    def test_cleaning_rejects_data_without_closing_prices(self):
        with self.assertRaisesRegex(ValueError, "Close"):
            clean_stock_data(pd.DataFrame({"Date": ["2024-01-01"], "Volume": [1]}))

    def test_cleaning_rejects_numeric_row_index_without_date_column(self):
        with self.assertRaisesRegex(ValueError, "Date"):
            clean_stock_data(pd.DataFrame({"Close": [100.0]}))

    def test_drawdown_includes_declines_from_the_starting_value(self):
        raw = pd.DataFrame(
            {"Date": ["2024-01-01", "2024-01-02"], "Close": [100.0, 90.0]}
        )
        _, summary = analyze_stock_data(clean_stock_data(raw), "demo")
        self.assertAlmostEqual(summary["max_drawdown"], -0.10)


if __name__ == "__main__":
    unittest.main()
