"""Format and write a human-readable analysis report."""

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


def _percent(value: object) -> str:
    if pd.isna(value):
        return "Not available"
    return "{:.2%}".format(float(value))


def write_summary_report(summary: Dict[str, object], output_path: Path) -> Path:
    """Write summary statistics and a short descriptive interpretation to Markdown."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    volatility = summary["annualized_volatility"]
    drawdown = summary["max_drawdown"]
    volatility_text = (
        "{:.2%}".format(float(volatility))
        if np.isfinite(volatility)
        else "Not available"
    )
    drawdown_text = (
        "{:.2%}".format(float(drawdown))
        if np.isfinite(drawdown)
        else "Not available"
    )
    report = """# {ticker} Stock Analysis

**Period:** {start_date:%Y-%m-%d} to {end_date:%Y-%m-%d}  
**Observations:** {observations}

## Summary

| Metric | Result |
|---|---:|
| First analysis price | ${start_price:,.2f} |
| Latest analysis price | ${latest_price:,.2f} |
| Period total return | {total_return} |
| Annualized historical volatility | {volatility} |
| Maximum observed drawdown | {drawdown} |
| Highest observed price | ${highest_price:,.2f} ({highest_price_date:%Y-%m-%d}) |
| Lowest observed price | ${lowest_price:,.2f} ({lowest_price_date:%Y-%m-%d}) |

## Descriptive note

{trend} These values describe historical observations only. They do not predict
future performance or account for an individual investor's circumstances.

## Method

Returns use the adjusted closing price when available, otherwise the closing
price. Annualized volatility is the sample standard deviation of daily returns
multiplied by the square root of 252 trading sessions. Maximum drawdown is
calculated from the cumulative daily-return series for this selected period.

> **Educational use only; not financial advice.**
""".format(
        ticker=summary["ticker"],
        start_date=summary["start_date"],
        end_date=summary["end_date"],
        observations=summary["observations"],
        start_price=summary["start_price"],
        latest_price=summary["latest_price"],
        total_return=_percent(summary["total_return"]),
        volatility=volatility_text,
        drawdown=drawdown_text,
        highest_price=summary["highest_price"],
        highest_price_date=summary["highest_price_date"],
        lowest_price=summary["lowest_price"],
        lowest_price_date=summary["lowest_price_date"],
        trend=summary["trend"],
    )
    output_path.write_text(report, encoding="utf-8")
    return output_path
