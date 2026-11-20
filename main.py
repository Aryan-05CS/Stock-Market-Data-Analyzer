"""Command-line entry point for the Stock Market Data Analyzer."""

import argparse
from datetime import date, timedelta
from pathlib import Path

from src.analyzer import analyze_stock_data
from src.data_loader import load_stock_data
from src.reporting import write_summary_report
from src.visualizations import create_charts


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze a stock using Yahoo Finance data or a local CSV."
    )
    parser.add_argument("--ticker", default="AAPL", help="Ticker symbol (default: AAPL)")
    parser.add_argument(
        "--start",
        default=(date.today() - timedelta(days=365)).isoformat(),
        help="Start date in YYYY-MM-DD format (default: one year ago)",
    )
    parser.add_argument(
        "--end",
        default=date.today().isoformat(),
        help="End date in YYYY-MM-DD format (Yahoo Finance end date is exclusive)",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        help="Use a local CSV instead of downloading data; CSV needs Date and Close columns",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory for generated CSV, charts, and report (default: outputs)",
    )
    return parser


def main() -> None:
    """Run the full analysis workflow and save its outputs."""
    args = build_parser().parse_args()
    if args.start >= args.end:
        raise SystemExit("Start date must be earlier than end date.")

    data = load_stock_data(args.ticker, args.start, args.end, args.csv)
    analysis, summary = analyze_stock_data(data, args.ticker)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    symbol = args.ticker.strip().upper().replace("/", "_")
    data_path = args.output_dir / "{}_analyzed_data.csv".format(symbol)
    report_path = args.output_dir / "{}_analysis_report.md".format(symbol)
    analysis.to_csv(data_path, index_label="Date")
    chart_paths = create_charts(analysis, symbol, args.output_dir)
    write_summary_report(summary, report_path)

    print("\nStock Market Data Analyzer")
    print("=" * 28)
    print("Ticker: {}".format(summary["ticker"]))
    print("Period: {} to {}".format(summary["start_date"].date(), summary["end_date"].date()))
    print("Rows analyzed: {}".format(summary["observations"]))
    print("Latest analysis price: ${:,.2f}".format(summary["latest_price"]))
    print("Period total return: {:.2%}".format(summary["total_return"]))
    volatility = summary["annualized_volatility"]
    print(
        "Annualized historical volatility: {:.2%}".format(volatility)
        if volatility == volatility
        else "Annualized historical volatility: Not available"
    )
    print("Highest / lowest: ${:,.2f} / ${:,.2f}".format(
        summary["highest_price"], summary["lowest_price"]
    ))
    print("Trend note: {}".format(summary["trend"]))
    print("\nSaved analyzed data: {}".format(data_path))
    for name, path in chart_paths.items():
        print("Saved {} chart: {}".format(name.replace("_", " "), path))
    print("Saved report: {}".format(report_path))
    print("\nEducational analysis only; not financial advice.")


if __name__ == "__main__":
    main()
