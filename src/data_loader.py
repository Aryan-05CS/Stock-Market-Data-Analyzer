"""Load and clean stock price data from Yahoo Finance or a local CSV."""

from pathlib import Path
from typing import Optional, Union

import pandas as pd


PathLike = Union[str, Path]
_PRICE_COLUMNS = {"Open", "High", "Low", "Close", "Adj Close", "Volume"}


def _standardize_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Normalize Yahoo Finance and CSV column names to a common format."""
    data = data.copy()

    if isinstance(data.columns, pd.MultiIndex):
        flattened = []
        for column in data.columns:
            parts = [str(part).strip() for part in column if str(part).strip()]
            match = next(
                (part for part in parts if part.lower() in {
                    "open", "high", "low", "close", "adj close", "volume"
                }),
                parts[0] if parts else "",
            )
            flattened.append(match)
        data.columns = flattened

    normalized = {}
    for column in data.columns:
        key = str(column).strip().lower().replace("_", " ")
        aliases = {
            "adjclose": "Adj Close",
            "adjusted close": "Adj Close",
            "date": "Date",
            "datetime": "Date",
        }
        name = aliases.get(key, key.title())
        normalized[column] = name
    return data.rename(columns=normalized)


def clean_stock_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Return sorted, numeric price data with a consistent analysis-price column."""
    if raw_data.empty:
        raise ValueError("The input contains no stock price rows.")

    data = _standardize_columns(raw_data)

    if "Date" in data.columns:
        dates = pd.to_datetime(data.pop("Date"), errors="coerce", utc=True)
    else:
        if not isinstance(data.index, pd.DatetimeIndex) and pd.api.types.is_numeric_dtype(
            data.index.dtype
        ):
            raise ValueError("Input must include a 'Date' column or a date-like index.")
        dates = pd.to_datetime(data.index, errors="coerce", utc=True)

    data.index = pd.DatetimeIndex(dates).tz_convert(None)
    data.index.name = "Date"
    data = data.loc[~data.index.isna()].copy()

    for column in _PRICE_COLUMNS:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    if "Close" not in data.columns and "Adj Close" in data.columns:
        data["Close"] = data["Adj Close"]
    if "Close" not in data.columns:
        raise ValueError("Input must contain a 'Close' or 'Adj Close' column.")

    if "Adj Close" in data.columns:
        data["Analysis Price"] = data["Adj Close"].where(
            data["Adj Close"].notna(), data["Close"]
        )
    else:
        data["Analysis Price"] = data["Close"]

    data = data.dropna(subset=["Analysis Price"])
    data = data.loc[data["Analysis Price"] > 0]
    data = data.sort_index()
    data = data.loc[~data.index.duplicated(keep="last")]

    if data.empty:
        raise ValueError("No valid, positive stock prices remained after cleaning.")
    return data


def load_stock_data(
    ticker: str,
    start_date: str,
    end_date: str,
    csv_path: Optional[PathLike] = None,
) -> pd.DataFrame:
    """Load a ticker from Yahoo Finance, or load a supplied local CSV instead."""
    if csv_path is not None:
        path = Path(csv_path)
        if not path.is_file():
            raise FileNotFoundError("CSV file does not exist: {}".format(path))
        return clean_stock_data(pd.read_csv(path))

    symbol = ticker.strip().upper()
    if not symbol:
        raise ValueError("Ticker symbol cannot be blank.")

    try:
        import yfinance as yf
    except ImportError as exc:
        raise ImportError(
            "Yahoo Finance downloads require yfinance. Install it with "
            "'python -m pip install yfinance', or use --csv."
        ) from exc

    raw_data = yf.download(
        symbol,
        start=start_date,
        end=end_date,
        progress=False,
        auto_adjust=False,
        threads=False,
    )
    if raw_data.empty:
        raise RuntimeError(
            "Yahoo Finance returned no rows for {} between {} and {}. "
            "Check the ticker, date range, and internet connection.".format(
                symbol, start_date, end_date
            )
        )
    return clean_stock_data(raw_data)
