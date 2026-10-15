"""Drop-in workaround for yf.download() when Yahoo rate-limits the crumb endpoint."""

import requests
import pandas as pd


_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}


def download(tickers, start=None, end=None, interval="1d", period=None):
    if isinstance(tickers, str):
        tickers = [tickers]

    all_data = {}
    for ticker in tickers:
        params = {"interval": interval}
        if period:
            params["range"] = period
        else:
            params["period1"] = int(pd.Timestamp(start).timestamp())
            params["period2"] = (
                int(pd.Timestamp(end).timestamp())
                if end
                else int(pd.Timestamp.now().timestamp())
            )
        r = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}",
            params=params,
            headers=_HEADERS,
        )
        if r.status_code != 200:
            print(f"Failed to download {ticker}: {r.status_code}")
            continue

        result = r.json()["chart"]["result"][0]
        ts = pd.to_datetime(result["timestamp"], unit="s")
        if interval == "1d" or interval.endswith("wk") or interval.endswith("mo"):
            ts = ts.normalize()
        quotes = result["indicators"]["quote"][0]
        adj = result["indicators"].get("adjclose", [{}])[0]
        df = pd.DataFrame(
            {
                "Open": quotes["open"],
                "High": quotes["high"],
                "Low": quotes["low"],
                "Close": quotes["close"],
                "Volume": quotes["volume"],
                "Adj Close": adj.get("adjclose", quotes["close"]),
            },
            index=ts,
        )
        df.index.name = "Date"
        all_data[ticker] = df

    if not all_data:
        return pd.DataFrame()
    if len(all_data) == 1:
        ticker = list(all_data.keys())[0]
        df = all_data[ticker]
        df.columns = pd.MultiIndex.from_product([df.columns, [ticker]])
        return df
    combined = pd.concat(all_data, axis=1)
    combined.columns = combined.columns.swaplevel(0, 1)
    combined.sort_index(axis=1, level=0, sort_remaining=False, inplace=True)
    return combined
