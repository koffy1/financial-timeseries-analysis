# Financial Time-Series Analysis

A small Python toolkit for pulling market data and running common
quantitative analyses on it: returns, drawdowns, and a CAPM-style
single-factor regression. Built while studying quantitative methods,
using NumPy, pandas, and statsmodels.

## Contents

| File | What it does |
|------|--------------|
| `yahoo.py` | A dependency-light downloader that fetches OHLCV + adjusted-close data straight from Yahoo Finance's chart API. A drop-in replacement for `yfinance.download()` for when the normal path gets rate-limited; returns a tidy (single ticker) or MultiIndex (multiple tickers) pandas DataFrame. |
| `notebooks/drawdowns.ipynb` | Computes drawdowns and drawdown *duration* from a price series using an expanding-maximum peak, and plots both. |
| `notebooks/capm_regression.ipynb` | Runs an OLS single-factor regression of a stock's returns on the market (SPY) with statsmodels, decomposes beta vs. alpha contributions, and computes an annualized information ratio and alpha t-stat. |

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

```python
import yahoo

# Drop-in for yf.download — returns a pandas DataFrame
px = yahoo.download(["SPY", "META"], start="2016-01-01")["Adj Close"]
```

## Analyses

**Drawdowns.** Drawdown at each point is `price / running_peak - 1`, where the
running peak is an expanding maximum. The duration function tracks how many
periods each series has spent below its prior peak.

**CAPM regression.** Regresses a stock's daily returns on the market's
(`stock_t ~ beta * SPY_t + alpha + e_t`), then separates the beta contribution
(market-explained) from the alpha contribution (residual return), and reports
the annualized information ratio (`mean/std * sqrt(252)`) and the alpha t-stat.

## Notes

Market data is sourced from Yahoo Finance for study purposes. Figures in the
notebooks are illustrative, not investment advice.
