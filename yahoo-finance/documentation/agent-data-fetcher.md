# Data Fetcher Agent

## Overview
The Data Fetcher Agent is responsible for retrieving and caching historical stock data from Yahoo Finance. It handles data persistence and cache management to optimize performance.

## Location
`finance/yfin/fetch.py`

## Key Functions

### `yahoo_fetch(ticker, period="3mo", interval="1d")`
Fetches historical stock data from Yahoo Finance with intelligent caching.

**Parameters:**
- `ticker` (str): Stock ticker symbol (e.g., "AAPL", "DBK.DE")
- `period` (str): Time period to fetch ("3mo", "1y", "max", "ytd", etc.)
- `interval` (str): Data granularity ("1d", "1wk", "1mo")

**Returns:**
- `pandas.DataFrame`: Historical stock data with OHLCV columns

**Behavior:**
- Checks for cached data in `./data/` directory
- Uses intelligent cache TTL based on period (daily for months, weekly for years)
- Fetches fresh data if cache is stale or missing
- Saves data to CSV for future use

### `load_ticker(ticker)`
Loads ticker data using `yahoo_fetch()` with default parameters.

**Parameters:**
- `ticker` (str): Stock ticker symbol

**Returns:**
- `pandas.DataFrame`: Historical stock data

## Cache Strategy
The agent implements a smart caching mechanism:
- **YTD data**: 30-day cache
- **Annual/Max data**: 7-day cache
- **Monthly data**: 24-hour cache
- **Daily data**: 24-hour cache

Cache files are stored as: `./data/{ticker}_{period}_{suffix}.csv`

## Data Format
The returned DataFrame contains:
- Index: Date (datetime, UTC)
- Columns: Open, High, Low, Close, Volume
- Missing values are handled (NaN rows removed)

## Error Handling
- Logs data type information after loading
- Handles missing cache files gracefully
- Validates data integrity after loading

## Usage Example
```python
from finance.yfin.fetch import load_ticker

# Load data for Deutsche Bank stock
df = load_ticker("DBK.DE")

# Load with custom parameters
from finance.yfin.fetch import yahoo_fetch
df = yahoo_fetch("XOM", period="1y", interval="1wk")
```

## Dependencies
- `yfinance`: Yahoo Finance data provider
- `pandas`: Data manipulation
- `datetime`: Timestamp handling
- `os`, `time`: File and cache management
