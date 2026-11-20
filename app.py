"""Optional interactive Streamlit dashboard for the stock analyzer."""

from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

from src.analyzer import analyze_stock_data
from src.data_loader import clean_stock_data, load_stock_data
from src.reporting import write_summary_report
from src.visualizations import create_charts


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs"


@st.cache_data(ttl=3600)
def fetch_analysis(ticker: str, start: str, end: str):
    """Cache public market data for an hour to avoid repeat downloads on reruns."""
    return analyze_stock_data(load_stock_data(ticker, start, end), ticker)


st.set_page_config(page_title="Stock Market Data Analyzer", layout="wide")
st.title("Stock Market Data Analyzer")
st.caption("Explore historical prices and risk/return measures. Educational use only.")

with st.sidebar:
    st.header("Analysis inputs")
    ticker = st.text_input("Ticker symbol", value="AAPL").strip().upper()
    today = date.today()
    start_date = st.date_input("Start date", value=today - timedelta(days=365))
    end_date = st.date_input("End date", value=today)
    uploaded_file = st.file_uploader("Optional CSV (use instead of online data)", type="csv")
    run_analysis = st.button("Analyze", type="primary")

if run_analysis:
    if start_date >= end_date and uploaded_file is None:
        st.error("Choose a start date earlier than the end date.")
        st.stop()
    try:
        if uploaded_file is not None:
            raw_data = pd.read_csv(uploaded_file)
            data = clean_stock_data(raw_data)
            analysis, summary = analyze_stock_data(data, ticker or "CSV")
        else:
            analysis, summary = fetch_analysis(
                ticker,
                start_date.isoformat(),
                end_date.isoformat(),
            )
    except (FileNotFoundError, ImportError, RuntimeError, ValueError) as exc:
        st.error(str(exc))
        st.stop()

    OUTPUT_DIR.mkdir(exist_ok=True)
    chart_paths = create_charts(analysis, summary["ticker"], OUTPUT_DIR)
    report_path = write_summary_report(
        summary, OUTPUT_DIR / "{}_analysis_report.md".format(summary["ticker"])
    )

    columns = st.columns(4)
    columns[0].metric("Latest analysis price", "${:,.2f}".format(summary["latest_price"]))
    columns[1].metric("Period total return", "{:.2%}".format(summary["total_return"]))
    volatility = summary["annualized_volatility"]
    columns[2].metric(
        "Annualized volatility",
        "{:.2%}".format(volatility) if pd.notna(volatility) else "N/A",
    )
    columns[3].metric("Observations", str(summary["observations"]))

    st.info(summary["trend"])
    st.subheader("Historical price and moving averages")
    st.image(str(chart_paths["moving_averages"]), use_container_width=True)
    left, right = st.columns(2)
    with left:
        st.subheader("Closing price")
        st.image(str(chart_paths["price"]), use_container_width=True)
        st.subheader("Daily returns")
        st.image(str(chart_paths["daily_returns"]), use_container_width=True)
    with right:
        st.subheader("Return distribution")
        st.image(str(chart_paths["return_distribution"]), use_container_width=True)
        st.subheader("Risk and price range")
        st.write(
            "Maximum observed drawdown: {:.2%}".format(summary["max_drawdown"])
            if pd.notna(summary["max_drawdown"])
            else "Maximum observed drawdown: N/A"
        )
        st.write(
            "High: ${:,.2f} on {} · Low: ${:,.2f} on {}".format(
                summary["highest_price"],
                summary["highest_price_date"].date(),
                summary["lowest_price"],
                summary["lowest_price_date"].date(),
            )
        )

    st.subheader("Analyzed data")
    st.dataframe(analysis.tail(20), use_container_width=True)
    st.download_button(
        "Download analyzed CSV",
        data=analysis.to_csv(index_label="Date"),
        file_name="{}_analyzed_data.csv".format(summary["ticker"]),
        mime="text/csv",
    )
    st.download_button(
        "Download analysis report",
        data=report_path.read_text(encoding="utf-8"),
        file_name=report_path.name,
        mime="text/markdown",
    )
else:
    st.markdown(
        "Enter a ticker and date range, or upload a CSV with a `Date` and `Close` "
        "column. Click **Analyze** to view charts and summary statistics."
    )

st.caption("Historical analysis is not a forecast or investment recommendation.")
