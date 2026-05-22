---
name: yahoo-finance-python
description: |
  Download financial & market data from Yahoo Finance using yfinance.
  Supports stock quotes, historical prices, fundamentals, dividends, splits, and more.

  Triggers when user mentions:
  - "get stock price" or "stock data"
  - "download market data" or "financial data"
  - "yahoo finance" or "yfinance"
  - wants to pull ticker data, historical prices, fundamentals
  - "fetch company financials" or "market cap"
author: Jansen Lin
license: MIT
allowed-tools: Bash
---

# Yahoo Finance Python Skill

Fetch financial & market data from Yahoo Finance using [ranaroussi/yfinance](https://github.com/ranaroussi/yfinance).

## Pre-Check

Before using yfinance, follow this check sequence:

### Step 1: Check if the yfinance module is importable

```bash
python -c "import yfinance" 2>/dev/null && echo "found" || echo "not found"
# or check in ~/.venv
~/.venv/bin/python -c "import yfinance" 2>/dev/null && echo "found in venv" || echo "not found in venv"
```

If found → skip to [Usage](#usage).

### Step 2: Check if ~/.venv exists

```bash
test -f ~/.venv/bin/python && echo "venv exists" || echo "venv not found"
```

If not found, create it:

```bash
python3 -m venv ~/.venv
```

### Step 3: Install yfinance into ~/.venv

```bash
~/.venv/bin/pip install yfinance
```

After installation, verify:

```bash
~/.venv/bin/python -c "import yfinance; print(yfinance.__version__)"
```

## Usage

All Python code below should be run with `~/.venv/bin/python` to ensure the module is available.

### Import

```python
import yfinance as yf
```

### Single Ticker

```python
# Create a Ticker object
msft = yf.Ticker("MSFT")

# Get general info
info = msft.info
print(info.get("shortName"))
print(info.get("currentPrice"))
print(info.get("marketCap"))
print(info.get("sector"))
```

### Historical Price Data

```python
# Get historical price data
hist = msft.history(period="1mo")        # 1 day, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
hist = msft.history(start="2025-01-01", end="2025-12-31")  # date range
hist = msft.history(period="1mo", interval="1h")  # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

# Returns a pandas DataFrame with: Open, High, Low, Close, Volume, Dividends, Stock Splits
print(hist)
```

### Multiple Tickers (Download)

```python
# Download data for multiple tickers at once
data = yf.download("AAPL MSFT GOOGL", period="1mo")
print(data)

# Or with a list
tickers = ["AAPL", "MSFT", "GOOGL"]
data = yf.download(tickers, period="6mo")
```

### Fundamentals

```python
msft = yf.Ticker("MSFT")

# Financial statements
msft.financials         # Income statement
msft.balance_sheet      # Balance sheet
msft.cashflow           # Cash flow statement
msft.quarterly_financials
msft.quarterly_balance_sheet
msft.quarterly_cashflow

# Dividends & Splits
msft.dividends          # Dividend history
msft.splits             # Stock split history
msft.actions            # Combined dividends + splits

# Earnings
msft.earnings_dates     # Upcoming/previous earnings dates

# Institutional & major holders
msft.institutional_holders
msft.major_holders

# Analyst recommendations
msft.recommendations
```

### Sector & Industry

```python
# Get sector/industry info
sector = yf.Sector("technology")
print(sector.overview)

industry = yf.Industry("software-infrastructure")
print(industry.top_companies)
```

### Search

```python
# Search for tickers
results = yf.Search("Tesla")
print(results.quotes)    # Matching ticker quotes
print(results.news)      # Related news
```

### Common Info Fields

```python
msft = yf.Ticker("MSFT")
info = msft.info

# Commonly used fields:
info.get("shortName")              # "Microsoft Corporation"
info.get("currentPrice")           # Current stock price
info.get("marketCap")              # Market capitalization
info.get("sector")                 # Sector
info.get("industry")               # Industry
info.get("previousClose")          # Previous close
info.get("open")                   # Today's open
info.get("dayLow") / info.get("dayHigh")
info.get("fiftyTwoWeekLow") / info.get("fiftyTwoWeekHigh")
info.get("volume")                 # Volume
info.get("averageVolume")
info.get("dividendRate")           # Dividend rate
info.get("dividendYield")
info.get("peRatio") / info.get("forwardPE")
info.get("epsTrailingTwelveMonths") / info.get("epsForward")
info.get("beta")                   # Beta
info.get("country")
info.get("website")
info.get("longBusinessSummary")    # Company description
```

### Saving Data to CSV

```bash
~/.venv/bin/python -c "
import yfinance as yf
data = yf.download('AAPL MSFT', period='1mo')
data.to_csv('stock_data.csv')
"
```

### Example: Quick Stock Snapshot

```bash
~/.venv/bin/python << 'EOF'
import yfinance as yf

tickers = ["AAPL", "MSFT", "GOOGL"]
for t in tickers:
    tk = yf.Ticker(t)
    info = tk.info
    print(f"{info.get('shortName', t):40s} ${info.get('currentPrice', 'N/A')}  MCap: {info.get('marketCap', 'N/A'):,}")
EOF
```
