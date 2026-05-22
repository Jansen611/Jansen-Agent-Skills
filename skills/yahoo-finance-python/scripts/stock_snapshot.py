#!/usr/bin/env python3
"""Quick stock snapshot for one or more tickers.

Usage: python3 stock_snapshot.py AAPL MSFT GOOGL
Defaults to AAPL MSFT GOOGL if no tickers provided.
"""

import sys

import yfinance as yf

tickers = sys.argv[1:] if len(sys.argv) > 1 else ["AAPL", "MSFT", "GOOGL"]
for t in tickers:
    tk = yf.Ticker(t)
    info = tk.info
    print(
        f"{info.get('shortName', t):40s} "
        f"${info.get('currentPrice', 'N/A')}  "
        f"MCap: {info.get('marketCap', 'N/A'):,}"
    )
