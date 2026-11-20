# Data

`sample_stock_data.csv` is a small **synthetic** dataset for testing the
CSV workflow without internet access. Its values are illustrative and are
not historical quotes for any real security.

For actual historical prices, run the CLI without `--csv` to request data
from Yahoo Finance. Alternatively, pass your own CSV with a `Date` column
and a `Close` (or `Adj Close`) column. Keep redistribution and API terms in
mind before publishing datasets.
