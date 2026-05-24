# Main Orchestrator Agent

## Overview
The Main Orchestrator Agent coordinates the entire stock analysis workflow. It orchestrates data fetching, technical analysis, and reporting to provide comprehensive stock market insights.

## Location
`finance/yfin/main.py`

## Core Function

### `main()`
Orchestrates the complete analysis pipeline for a stock ticker.

**Process Flow:**
1. **Data Fetching**: Load historical stock data using `load_ticker()`
2. **Technical Indicators**: Compute indicators with `add_indicators()`
3. **Level Identification**: Identify price levels using:
   - K-means clustering
   - Support/Resistance analysis
   - Swing points detection
4. **KPI Calculation**: Calculate summary KPIs
5. **Volatility Analysis**: Analyze volatility patterns
6. **Reporting**: Log results in structured format (JSON)

## Execution Flow

### Step 1: Load Data
```python
df = load_ticker(ticker)
```
Retrieves historical OHLCV data for the specified ticker.

### Step 2: Add Indicators
```python
df = add_indicators(ticker, df)
```
Computes technical indicators:
- Simple Moving Averages (5, 10-day)
- MACD
- Bollinger Bands
- RSI
- Volatility

### Step 3: Identify Price Levels
```python
kmeans_levels = kmeans_clustering(ticker, df)
levels = get_support_resistance(ticker, df)
swing_points = get_swing_points(ticker, df)
```
Identifies key price levels through multiple methods.

### Step 4: Calculate Summary KPIs
```python
summary = get_summary_kpi(ticker, df)
```
Generates trend analysis and key metrics.

### Step 5: Analyze Volatility
```python
last_volatility = get_last_volatility(ticker, df)
```
Analyzes volatility patterns since last swing low.

## Output & Logging

The agent logs detailed information at INFO level:

1. **DataFrame Tail**: Last 5 rows of data with all indicators
2. **Support/Resistance**: JSON-formatted levels
3. **Summary KPIs**: JSON-formatted trend analysis
4. **Volatility Analysis**: JSON-formatted volatility metrics

### Output Format Example
```json
{
  "ticker": "DBK.DE",
  "max_label": "at_max",
  "max_price": 150.25,
  "last_price": 149.87,
  "trend_5_10_pct": 2.34,
  "trend_label": "bullish",
  "diff_200_pct": 5.12
}
```

## Tested Tickers

The agent has been tested with:
- **DBK.DE**: Deutsche Bank (DAX)
- **DTE.DE**: Deutsche Telekom (DAX)
- **XOM**: ExxonMobil (NYSE)
- **DOW**: Dow Inc (NYSE)
- **BAS.DE**: BASF (DAX)

## Entry Points

### Command Line Execution
```bash
# Activate virtual environment
source .venv/bin/activate

# Run analysis
python -m finance.yfin.main
```

### Programmatic Usage
```python
from finance.yfin.main import main

# Run complete analysis
main()
```

## Configuration

### Ticker Selection
Modify the `ticker` variable in `main()` to analyze different stocks:
```python
ticker = "YOUR_TICKER"  # e.g., "AAPL", "SAP.DE", "MSFT"
```

### Data Parameters
Adjust data fetching parameters via `yahoo_fetch()`:
- `period`: "3mo", "1y", "max"
- `interval`: "1d" (daily), "1wk" (weekly), "1mo" (monthly)

## Outputs Generated

The agent creates the following artifacts in `./data/`:

1. **CSV Files**
   - `{ticker}_indicators.csv`: Historical data with computed indicators

2. **Visualizations**
   - `{ticker}_kmeans.png`: K-means clustering visualization
   - `{ticker}_support_resistance.png`: Support/resistance with volume profile
   - `{ticker}_swing_points.png`: Swing highs and lows identification

3. **Console Logs**
   - DataFrame statistics
   - Technical analysis results
   - Trend analysis
   - Volatility metrics

## Dependencies

**Internal:**
- `finance.yfin.fetch.load_ticker`: Data loading
- `finance.yfin.kpi.add_indicators`: Technical indicators
- `finance.yfin.kpi.kmeans_clustering`: Price level clustering
- `finance.yfin.kpi.get_support_resistance`: Support/resistance analysis
- `finance.yfin.kpi.get_swing_points`: Swing point detection
- `finance.yfin.kpi.get_summary_kpi`: Summary metrics
- `finance.yfin.kpi.get_last_volatility`: Volatility analysis

**External:**
- `pandas`: Data manipulation
- `json`: Output formatting
- `logging`: Structured logging

## Logging Configuration

The agent uses Python's logging module with:
- **Logger Name**: Module name (`finance.yfin.main`)
- **Level**: INFO
- **Format**: Standard Python logging format

All analysis steps are logged for debugging and audit trails.

## Error Handling

The agent inherits error handling from child functions:
- Data validation from `load_ticker()`
- DataFrame integrity checks from indicator functions
- Numeric overflow protection from KMeans clustering
