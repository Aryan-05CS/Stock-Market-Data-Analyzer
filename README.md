# Stock Market Data Analyzer

A beginner-friendly, GitHub-ready Python project that downloads historical
market data or reads a local CSV, cleans it, calculates price and risk/return
statistics, saves charts, and writes a Markdown report. An optional Streamlit
dashboard is included.

> **Disclaimer:** This project is for educational purposes only. It is not
> financial advice, an investment recommendation, or a forecast. Historical
> performance does not guarantee future results. Verify data, licensing, and
> provider terms before using or redistributing it.

## Project overview

Investors, analysts, traders, and finance teams need to inspect price history
to understand how an asset behaved over a selected period. This project
automates a small, reproducible version of that workflow using public data:

**collect prices → clean data → calculate returns and moving averages →
describe volatility and drawdown → visualize → generate a report**

Companies may use stock and market data in investment research, market
monitoring, portfolio reporting, risk analysis, and business decision support.
This project demonstrates the data-processing steps; it is not a trading
system and does not provide predictive signals.

## Features

- Download historical prices from Yahoo Finance with `yfinance`.
- Use a local CSV instead, including the offline synthetic example.
- Clean dates, numeric columns, duplicate rows, and missing/invalid prices.
- Prefer adjusted close for analysis when available; fall back to close.
- Calculate daily returns, 20/50/200-session simple moving averages,
  annualized historical volatility, and maximum observed drawdown.
- Find the highest high and lowest low (or use available close prices).
- Save price, moving-average, daily-return, and return-distribution charts.
- Export the analyzed data as CSV and a summary as Markdown.
- Explore the same analysis in an optional Streamlit dashboard.
- Run focused unit tests without a live market-data connection.

## Tech stack and project levels

| Level | Tools | Difficulty | Expected output |
|---|---|---:|---|
| Easy | Python, CSV, Pandas, Matplotlib | Beginner | Clean data and basic price chart |
| **Intermediate (this project)** | Python, Pandas, NumPy, Matplotlib, Seaborn, yfinance, `datetime` | Beginner–intermediate | Reusable CLI, indicators, risk summary, charts, report |
| Advanced | Intermediate stack plus Streamlit, Plotly, database/storage, scheduled jobs and deployment | Intermediate–advanced | Interactive, deployable analysis dashboard |

The intermediate version is a good student project: it works with free public
data, can also run offline with CSV, and demonstrates reusable Python modules,
data analysis, visualization, testing, and documentation.

## Architecture

```text
Ticker + date range ──┐
                      ├─> Yahoo Finance / local CSV
CSV upload (dashboard)┘
                               |
                               v
                       Load and validate data
                               |
                               v
                      Clean dates and prices
                               |
                               v
              Returns + moving averages + risk metrics
                               |
                               v
                Charts + analyzed CSV + Markdown report
                     |                       |
                  outputs/              CLI / dashboard
```

The adjusted close is used for analysis when supplied (to account for
adjustments such as splits and distributions); otherwise close is used. The
reported high/low use the source High/Low columns when available.

## Folder structure

```text
Stock-Market-Data-Analyzer/
├── data/                 # Synthetic demo CSV and data notes
├── notebooks/            # Optional Jupyter exploration
├── src/                  # Data loading, analysis, charts, reporting modules
├── outputs/              # Generated CSV, charts, and Markdown report
├── images/               # Portfolio screenshots for README
├── reports/              # Optional curated report examples
├── docs/                 # Detailed walkthrough and portfolio plan
├── tests/                # Focused automated tests
├── app.py                # Optional Streamlit dashboard
├── main.py               # Command-line entry point
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements and installation

Use Python 3.10 or later. Open a terminal in the project folder.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell prevents environment activation, either allow activation for
your user following the official Python/PowerShell guidance, or run the
environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the project

### Offline demo using the included synthetic CSV

From the project root:

```bash
python main.py --ticker DEMO --csv data/sample_stock_data.csv
```

The demo data is synthetic and deliberately short. It demonstrates the
workflow, not historical prices for a real company. Moving averages needing
more observations will be blank on this short sample.

### Download public historical data

```bash
python main.py --ticker AAPL --start 2024-01-01 --end 2025-01-01
```

Yahoo Finance's end date is exclusive. A working internet connection and
provider availability are required. If a request returns no rows, check the
ticker, dates, and connection or use `--csv`.

### Your own CSV

```bash
python main.py --ticker MYDATA --csv path/to/prices.csv
```

CSV must have a `Date` column (or date index) and a `Close` or `Adj Close`
column. `Open`, `High`, `Low`, `Volume`, and `Adj Close` are optional.

### Optional dashboard

```bash
streamlit run app.py
```

Enter a ticker and date range in the sidebar, or upload a CSV. The dashboard
offers download buttons for the analyzed data and report. The online download
is cached for one hour per ticker/date selection.

### Run tests

```bash
python -m unittest discover -s tests -v
```

## Generated output

The CLI creates the following files in `outputs/` (with the ticker in each
filename):

- `*_analyzed_data.csv` — cleaned prices, daily returns, and moving averages.
- `*_closing_price.png` — adjusted close/close time series.
- `*_moving_averages.png` — price with available moving-average lines.
- `*_daily_returns.png` — daily return time series.
- `*_return_distribution.png` — histogram of daily returns.
- `*_analysis_report.md` — metrics, descriptive note, and methodology.

The report includes the period return, annualized volatility, maximum observed
drawdown, price high/low and dates, and a cautious moving-average comparison.
These are historical descriptive statistics, not a buy/sell signal.

## Sample output

With the included demo CSV, the terminal shows the actual row count, final
price, period return, volatility availability, and output paths, for example:

```text
Stock Market Data Analyzer
============================
Ticker: DEMO
Rows analyzed: 10
Latest analysis price: $109.00
Saved analyzed data: outputs\DEMO_analyzed_data.csv
Saved report: outputs\DEMO_analysis_report.md

Educational analysis only; not financial advice.
```

Exact dates/metrics and path separators can vary with your environment. The
synthetic demo has no investment meaning.

For the included sample file, the verified example metrics are:

| Metric | Sample result |
|---|---:|
| Observations | 10 |
| First / latest analysis price | $101.00 / $109.00 |
| Period total return | 7.92% |
| Annualized historical volatility | 24.85% |
| Highest / lowest observed price | $110.00 / $99.00 |

These are calculated from the illustrative CSV and are not real market data.

## Screenshots for a portfolio

Capture and add your own screenshots under `images/`:

1. Project tree in VS Code or File Explorer.
2. Preview of `data/sample_stock_data.csv`.
3. Terminal command and successful output.
4. Closing-price chart.
5. Moving-average chart (use a longer dataset to show the lines).
6. Daily-return chart and return-distribution chart.
7. Annualized volatility, drawdown, and price-range summary in the report.
8. Streamlit dashboard, if you run it.
9. Public GitHub repository page with README preview.

Use descriptive filenames such as `project-structure.png`,
`closing-price-chart.png`, and `dashboard.png`. Do not present synthetic data
as live or real market data.

## Learning outcomes

- Python modules, functions, CLI arguments, exceptions, and file paths.
- Pandas data validation, datetime indexes, cleaning, and CSV input/output.
- NumPy/Pandas returns and rolling-window calculations.
- Historical volatility, drawdown, and limitations of summary statistics.
- Matplotlib/Seaborn visualizations and report generation.
- Unit testing, virtual environments, Git, and GitHub documentation.
- Optional interactive data-app development with Streamlit.

## Industry relevance

The project resembles an entry-level analytics pipeline: it ingests external
data, checks and transforms it, calculates business-facing measures, and
publishes repeatable outputs. It can support a discussion of data quality,
assumptions, and communicating results to a non-technical audience. In a
production environment, teams would additionally address source contracts,
market calendars, corporate actions, data lineage, monitoring, permissions,
resilience, and compliance.

## Disclaimer

This project is for educational purposes only and is not financial advice.
Market data may be delayed, incomplete, revised, or unavailable. No metric,
chart, or report here predicts future performance or should be used alone to
make an investment decision.

## More detail

See [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md) for the phase-by-phase
build, architecture explanation, GitHub publishing steps, six-day proof plan,
screenshot checklist, and interview preparation.
