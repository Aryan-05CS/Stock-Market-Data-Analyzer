# Student Build and Portfolio Guide

This guide explains the project from first principles, then gives a practical
build sequence and a portfolio/interview plan. The runnable source is in the
repository root and `src/`.

> **Disclaimer:** Educational project only; not financial advice. Historical
> analysis is not a recommendation or a prediction.

## 1. What the analyzer does

### Simple explanation

A Stock Market Data Analyzer takes historical prices for a ticker, checks
that the rows and prices are usable, calculates how prices changed, and
produces charts and a short report. It helps a learner answer questions such
as: What happened to the price over this period? How variable were daily
returns? How did the short and longer moving averages compare?

### Technical explanation

This is a small data pipeline. It ingests OHLCV-style data from Yahoo Finance
through `yfinance` or from CSV, normalizes columns and dates with Pandas,
derives adjusted-price returns and rolling simple moving averages, computes
historical risk descriptors, then writes figures, a CSV, and a Markdown
summary. It does not place trades, optimize a portfolio, or forecast returns.

### Who might use similar analysis?

- **Investors and researchers:** review historical behavior as one input to
  broader research.
- **Analysts:** monitor price history, compare periods, and communicate
  observed movements.
- **Traders:** inspect historical chart patterns as context, not as a promise
  of future price direction.
- **Finance teams:** prepare repeatable monitoring and reporting outputs.
- **Companies:** combine market data with research, portfolio/risk reporting,
  and decision-support processes. Actual organizations use controls,
  licensed data, and validated methods beyond this student example.

Python is useful here because Pandas handles tabular/time-indexed data, NumPy
supports numerical calculations, plotting libraries turn results into
readable charts, and scripts can make a repeated analysis consistent.

### Workflow

1. **Stock data collection:** accept ticker and dates, request public data or
   read a CSV.
2. **Data cleaning:** parse dates, normalize columns, sort rows, remove
   duplicate dates, coerce numeric values, and reject unusable prices.
3. **Price trend analysis:** plot observed adjusted close/close.
4. **Moving averages:** compare 20-, 50-, and 200-session rolling averages.
5. **Returns calculation:** calculate each session's percentage price change.
6. **Risk analysis:** summarize sample standard deviation annualized with
   `sqrt(252)` and the selected period's maximum drawdown.
7. **Visualization:** save price, average, daily-return, and return-histogram
   charts.
8. **Report generation:** write the selected-period statistics, assumptions,
   and a descriptive—not predictive—note.

### Metric definitions and caveats

- Daily simple return: `price_today / price_previous_session - 1`.
- SMA: arithmetic mean of the last N observed trading sessions; it is undefined
  until N observations exist.
- Annualized historical volatility: sample standard deviation of daily returns
  multiplied by `sqrt(252)`, a common approximate trading-session convention.
- Maximum drawdown: minimum decline from a prior peak in the cumulative
  compounded return series over the selected period.
- Period return: last analysis price divided by first analysis price minus one.

These are descriptive calculations. They do not model transaction costs,
taxes, slippage, liquidity, all corporate-action/data-provider differences,
or an investor's objectives. Volatility is not the same thing as probability
of loss.

## 2. Tech stack choices

| Option | Tools | Difficulty | Expected result |
|---|---|---|---|
| A — Easy | Python, CSV, Pandas, Matplotlib | Beginner | Load a file, inspect prices, make one chart |
| B — Intermediate | Python, Pandas, NumPy, Matplotlib, Seaborn, `yfinance`, `datetime` | Beginner–intermediate | This project: repeatable CLI, metrics, charts, CSV, report |
| C — Advanced | Option B plus Streamlit, optional Plotly, persistence, scheduled refresh, deployment and stronger tests | Intermediate–advanced | Interactive multi-user/dashboard-style product prototype |

**Recommended for students: Option B**, with the included Streamlit dashboard
as a bonus. Build and verify the CLI/CSV workflow first so it still works
without a network connection.

## 3. Architecture and data flow

```text
Inputs: ticker, start/end dates, optional local CSV
                       |
                       v
          Yahoo Finance (yfinance) or CSV
                       |
                       v
         src/data_loader.py: normalize + validate
                       |
                       v
             src/analyzer.py: calculate
            /            |             \
       returns       SMA 20/50/200    risk metrics
            \            |             /
             src/visualizations.py + reporting.py
                       |
                       v
  outputs/: charts, analyzed CSV, human-readable Markdown report
         CLI main.py or optional Streamlit app.py
```

The caller supplies the ticker/date range for an online download; `--csv`
selects a local file instead. `clean_stock_data` standardizes both sources.
Adjusted close is preferred for return/average calculations when available.
The output includes no credentials and needs no paid terminal.

## 4. Ten-phase implementation plan

| Phase | What to do | Why | Expected output | Common beginner mistakes |
|---|---|---|---|---|
| 1. Setup | Install Python, editor, Git; create/activate `.venv`; install `requirements.txt` | Isolate project dependencies and make the environment repeatable | Working Python environment | Installing into a different interpreter; forgetting activation |
| 2. Folders | Create `data/`, `src/`, `outputs/`, `tests/`, docs folders | Separate data, logic, and deliverables | GitHub-ready tree | Putting every function in one script; committing `.venv` |
| 3. Collection | Try the synthetic CSV, then download a ticker with dates | Validate the workflow offline before depending on an API | DataFrame with price rows | Wrong ticker; assuming the end date is inclusive; network/API limits |
| 4. Cleaning | Parse dates, normalize columns, sort, deduplicate, validate prices | Calculations are only as trustworthy as their inputs | Clean, indexed price table | Treating strings as numbers; ignoring timezone and missing values |
| 5. EDA | Inspect row count, range, columns, missing values, and price plot | Understand the data before calculating indicators | Initial chart and sanity checks | Assuming a downloaded dataset is complete or adjusted |
| 6. Moving averages | Calculate rolling 20/50/200-session means | Compare smoothed historical price paths | SMA columns and comparison chart | Calling an SMA a prediction; forgetting early `NaN` values |
| 7. Returns/risk | Calculate daily returns, volatility, drawdown, high/low | Describe period behavior consistently | Numeric risk/return summary | Using price differences instead of returns; claiming volatility guarantees loss |
| 8. Visualization | Save price, SMA, daily-return, distribution figures | Communicate patterns and dispersion | PNG chart files | Missing labels/units; interpreting a histogram as a forecast |
| 9. Reporting | Export analyzed CSV and Markdown report with assumptions | Make work reviewable and repeatable | Files in `outputs/` | Omitting period/units/methods/disclaimer |
| 10. GitHub | Test, review secrets/data rights, document and push | Make proof of work accessible | Public repo with README and screenshots | Uploading `.venv`, credentials, or data without redistribution rights |

The code in this repository already implements the phases; use this sequence
to understand it and to structure your commits.

## 5. Installation and running

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If script activation is restricted, use
`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, then prefix
commands with `.\.venv\Scripts\python.exe`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Commands

```bash
# Offline, synthetic sample; good first run
python main.py --ticker DEMO --csv data/sample_stock_data.csv

# Public data download; end date is exclusive
python main.py --ticker MSFT --start 2023-01-01 --end 2024-01-01

# Optional interactive dashboard
streamlit run app.py

# Run focused tests
python -m unittest discover -s tests -v
```

Expected CLI output includes the ticker, date range, observation count, latest
price, total return, annualized volatility when enough data exists, the high
and low, a moving-average note, and saved output paths. The selected CSV's
short history intentionally cannot populate all 20/50/200-session averages;
use more than 200 rows to see every line.

The generated files are:

```text
outputs/
├── DEMO_analyzed_data.csv
├── DEMO_closing_price.png
├── DEMO_moving_averages.png
├── DEMO_daily_returns.png
├── DEMO_return_distribution.png
└── DEMO_analysis_report.md
```

Filenames use the ticker chosen at runtime. The sample prices are illustrative
synthetic values, not market observations.

## 6. Virtual simulation walkthrough

1. Run the synthetic CSV command. The loader reads dates and prices without
   accessing a network or requiring market-data credentials.
2. The cleaner sorts the dates, drops unusable rows, and creates `Analysis
   Price`, choosing adjusted close when present and close otherwise.
3. The analyzer calculates daily percentage changes and rolling means. A
   moving average smooths short-term variation; it lags actual prices and is
   not a forecast.
4. Return dispersion is summarized as annualized historical volatility. A
   larger past value indicates more variable observed returns in the selected
   window, not certainty about future risk.
5. The report lists the period return, high/low dates, volatility, drawdown,
   and the latest 20/50 average comparison where enough rows exist.
6. Charts and CSV let a reviewer independently inspect how the outputs were
   produced. Replace the short demo with a longer licensed/public dataset to
   display long moving-average lines.

Capture your own screenshots: project folder; sample CSV preview; successful
terminal run; closing-price chart; moving-average chart; daily-return and
distribution charts; report/risk summary; optional dashboard; and GitHub
repository preview. Save these to `images/` with descriptive names. Keep the
synthetic-data label visible when using the demo.

## 7. GitHub publishing steps

1. On GitHub, create a new repository, for example **Stock-Market-Data-Analyzer**.
   Description: *A Python stock-data analysis pipeline with CSV/Yahoo Finance
   input, returns and volatility metrics, charts, reports, and an optional
   Streamlit dashboard.*
2. Choose Public if you want portfolio visibility. Do not initialize a second
   README on GitHub if this local project already has one.
3. In a terminal at the project root, check `git status`, then initialize and
   commit:

   ```bash
   git init
   git add .
   git commit -m "Build stock analysis data pipeline"
   git branch -M main
   git remote add origin https://github.com/<YOUR-USERNAME>/Stock-Market-Data-Analyzer.git
   git push -u origin main
   ```

4. After adding screenshots or improving documentation:

   ```bash
   git add README.md docs/ images/
   git commit -m "Add project walkthrough and analysis screenshots"
   git push
   ```

5. Generated output is ignored by default to avoid committing unreviewed output.
   If you choose to publish a specific reproducible demo output, explicitly
   stage only the intended file, for example:

   ```bash
   git add -f outputs/DEMO_analysis_report.md
   ```

   Review data-provider terms and the report's synthetic/real-data label
   before publishing. Never commit API keys, personal data, `.env`, or `.venv`.

**Suggested repository tags/topics:** `python`, `pandas`, `data-analysis`,
`financial-analysis`, `stock-market`, `yfinance`, `matplotlib`, `seaborn`,
`streamlit`, `beginner-project`.

Good commit messages explain a coherent change: `Add CSV price-data cleaning`,
`Calculate returns and volatility`, `Save analysis visualizations`, and
`Document setup and sample workflow`.

## 8. Six-day proof-of-work plan

| Day | Build and commit | Evidence to save |
|---|---|---|
| 1 — Setup | Create environment, folder structure, requirements and README outline. Commit: `Set up Python project structure` | Project tree screenshot; environment/test command |
| 2 — Data | Add CSV and Yahoo Finance loading. Commit: `Add Yahoo Finance and CSV data loading` | CSV preview; terminal output from offline run |
| 3 — Cleaning/EDA | Validate dates/prices and inspect the dataset. Commit: `Clean and validate stock price data` | Analyzed CSV preview; price chart |
| 4 — Metrics | Add daily returns, SMA, volatility, high/low, drawdown. Commit: `Calculate stock returns and risk metrics` | Report metrics and SMA chart |
| 5 — Visualization | Save labeled charts; optionally finish dashboard. Commit: `Add stock analysis charts and dashboard` | Price, moving-average, daily-return, distribution charts |
| 6 — Reporting/docs | Run tests, generate report, finish README and screenshots. Commit: `Add analysis report and portfolio documentation` | Final report, test output, GitHub repository preview |

Make each commit only after the relevant command works. A sequence of honest
small commits is stronger evidence than a single unexplained upload.

## 9. Screenshot/output checklist

- [ ] Project folder screenshot in VS Code/File Explorer.
- [ ] `sample_stock_data.csv` opened as a table.
- [ ] Terminal output from `python main.py --ticker DEMO --csv data/sample_stock_data.csv`.
- [ ] Closing-price chart.
- [ ] Moving-average chart (for all lines, run at least 200 observations).
- [ ] Daily-return time-series chart.
- [ ] Daily-return distribution chart.
- [ ] Volatility, drawdown, and high/low summary in report or dashboard.
- [ ] Final Markdown report.
- [ ] Optional Streamlit dashboard.
- [ ] GitHub repository page showing README, files, and commit history.

Do not fabricate screenshots or imply that a synthetic demo represents actual
market data.

## 10. Interview preparation

### 1. “Explain your project.”

**Answer:** “I built a Python stock market data analyzer that downloads public
historical prices or reads a CSV, validates and cleans the data, calculates
daily returns, moving averages, annualized historical volatility, and maximum
drawdown, then exports charts, analyzed CSV, and a Markdown report. I also
added an optional Streamlit dashboard and unit tests. I prefer adjusted close
when it is available and document the assumptions. It is an educational
historical-analysis tool, not a trading recommendation.”

### 2. What problem does the project solve?

It reduces repetitive manual steps involved in loading, checking, summarizing,
and visualizing a selected historical price period. It improves repeatability;
it does not eliminate the need to verify data quality or interpret results.

### 3. Why use adjusted close?

Adjusted close generally accounts for certain corporate actions such as stock
splits and distributions, making it more suitable for historical return
comparisons. Provider methodology can vary, so I state which series is used
and fall back to close only if adjusted close is absent.

### 4. How do you calculate daily return?

For each observation, divide today's analysis price by the previous session's
price and subtract one. Pandas `pct_change()` implements that calculation.
The first row has no prior price, so its return is missing.

### 5. What does a moving average tell you?

It smooths a chosen number of observed sessions to make historical direction
easier to inspect. A 20-session SMA reacts faster than a 50-session SMA, but
both lag price and neither predicts future performance.

### 6. How is volatility calculated here?

I take the sample standard deviation of daily returns and multiply by the
square root of 252 to express an annualized historical estimate using a
common trading-session convention. It is window-dependent and is not a
guaranteed future-risk measure.

### 7. What is maximum drawdown?

It is the largest peak-to-trough percentage decline in the compounded return
path during the selected period. It describes a historical decline; the
selected window changes the result.

### 8. What data-quality issues did you handle?

I normalize column names, parse and sort dates, remove duplicate dates,
convert price fields to numeric values, drop missing/non-positive analysis
prices, and fail with a clear error if there is no usable close price.

### 9. How did you test it without depending on the API?

The unit tests construct small in-memory DataFrames and verify date sorting,
adjusted-price selection, return and moving-average arithmetic, summary values,
and invalid input behavior. The included synthetic CSV provides an additional
manual offline run.

### 10. What would you improve for production?

I would add source/version metadata, explicit market-calendar and
corporate-action handling, retry/backoff with provider-aware limits, stronger
schema and integration tests, structured logging, data lineage, monitoring,
configuration, and security/compliance review. I would not use this sample
alone to make portfolio decisions.

### HR / non-technical explanation

“I wanted to apply Python to a real-world data problem without paid terminals.
I built a small end-to-end project that collects public or CSV price data,
checks it, summarizes historical performance and variability, and presents
the results in charts and a report. I focused on making the work reproducible
and explaining its limitations. The project demonstrates my ability to learn
a domain, structure code, test calculations, and communicate findings.”

### Technical explanation

“The CLI calls a loader that normalizes Yahoo Finance's potentially
multi-level columns or local CSV columns. The cleaner parses timestamps,
sorts and deduplicates observations, coerces numeric fields, and creates an
analysis-price series. The analyzer computes `pct_change`, rolling SMAs,
sample standard deviation annualized by `sqrt(252)`, and drawdown from
compounded returns. Visualization and reporting are separate modules. Tests
use in-memory fixtures, so calculation checks do not require external
services. Streamlit optionally caches an online ticker/date result for one
hour.”

## 11. Responsible use

Use data only in accordance with the provider's current terms and applicable
law. Never expose credentials. Check that screenshots and generated reports
clearly distinguish synthetic examples from downloaded data. This work is
for education only and is not financial advice.
