# Yahoo Finance Analysis System - Agent Documentation

## System Overview

The Yahoo Finance Analysis System is a modular Python application designed for comprehensive stock market analysis. It consists of three integrated agents that work together to fetch data, analyze trends, and identify trading opportunities.

## Agent Architecture

```
┌─────────────────────────────────────────────────────┐
│   Main Orchestrator Agent (main.py)                 │
│   Coordinates the complete analysis workflow         │
└────────────┬─────────────────────────────────────────┘
             │
     ┌───────┴────────┐
     │                │
     ▼                ▼
┌──────────────┐  ┌──────────────────┐
│ Data Fetcher │  │ KPI Analysis     │
│ Agent        │  │ Agent            │
│ (fetch.py)   │  │ (kpi.py)         │
└──────────────┘  └──────────────────┘
```

## Agent Descriptions

### 1. Data Fetcher Agent (`finance/yfin/fetch.py`)
**Responsibility**: Retrieve and cache stock market data

**Key Capabilities:**
- Fetches historical OHLCV data from Yahoo Finance
- Implements intelligent caching with period-based TTL
- Validates data integrity
- Supports flexible time periods and intervals

**Main Functions:**
- `yahoo_fetch(ticker, period, interval)`: Fetch with caching
- `load_ticker(ticker)`: Load ticker with defaults

**Data Flow:**
```
User Request → Cache Check → Yahoo Finance API → Store CSV → Return DataFrame
```

**Documentation**: See `agent-data-fetcher.md`

---

### 2. KPI Analysis Agent (`finance/yfin/kpi.py`)
**Responsibility**: Calculate technical indicators and trading levels

**Key Capabilities:**
- Computes 5+ technical indicators (SMA, MACD, RSI, Bollinger Bands, Volatility)
- Identifies price levels through K-means clustering
- Detects swing points using local extrema analysis
- Calculates support and resistance using volume profile
- Analyzes trend direction and volatility patterns

**Main Functions:**
- `add_indicators()`: Compute technical indicators
- `kmeans_clustering()`: Identify price clusters
- `get_swing_points()`: Detect swing highs/lows
- `get_support_resistance()`: Find key price levels
- `get_summary_kpi()`: Trend analysis
- `get_last_volatility()`: Volatility metrics

**Analysis Methods:**
- **Clustering**: K-means with normalized time and price
- **Pattern Recognition**: Local extrema detection (order=5)
- **Volume Profile**: Density-weighted support/resistance
- **Volatility**: True Range percentages

**Documentation**: See `agent-kpi-analysis.md`

---

### 3. Main Orchestrator Agent (`finance/yfin/main.py`)
**Responsibility**: Coordinate complete analysis workflow

**Key Capabilities:**
- Orchestrates data fetching and analysis pipeline
- Consolidates results from all agents
- Generates comprehensive reports
- Manages logging and output

**Execution Flow:**
```
1. Load ticker data
2. Compute indicators
3. Identify price levels (3 methods)
4. Calculate summary KPIs
5. Analyze volatility
6. Log results
```

**Documentation**: See `agent-main-orchestrator.md`

---

## Data Flow Overview

```
Yahoo Finance API
       │
       ▼
┌──────────────────┐
│ Data Fetcher     │ (Cached locally)
│ fetch.py         │
└────────┬─────────┘
         │
         ▼
    DataFrame
  (OHLCV data)
         │
         ▼
┌──────────────────┐
│ KPI Analysis     │
│ kpi.py           │
│ - Indicators     │
│ - Levels         │
│ - Trends         │
│ - Volatility     │
└────────┬─────────┘
         │
         ▼
    Analysis Results
  - JSON reports
  - PNG visualizations
  - CSV exports
```

## Key Outputs

### Data Artifacts
- **CSV Files**: Indicator calculations and raw data
- **PNG Visualizations**: K-means, swing points, support/resistance
- **JSON Reports**: Structured analysis results

### Analysis Metrics
1. **Support/Resistance Levels**: Key price zones
2. **Trend Analysis**: Bullish/bearish/neutral classification
3. **Volatility Metrics**: Intraday and directional volatility
4. **Technical Indicators**: SMA, MACD, RSI, Bollinger Bands

## Usage Example

```python
# Run complete analysis
python -m finance.yfin.main

# Analyze specific ticker (modify in main.py)
# Change: ticker = "YOUR_TICKER"
# Run: python -m finance.yfin.main
```

## Directory Structure

```
yahoo-finance/
├── finance/
│   ├── yfin/
│   │   ├── __init__.py
│   │   ├── main.py          # Main Orchestrator
│   │   ├── fetch.py         # Data Fetcher Agent
│   │   ├── kpi.py           # KPI Analysis Agent
│   │   └── test_*.py        # Unit tests
│   └── scrape/
├── data/                     # Cache and outputs
├── documentation/
│   ├── agent-data-fetcher.md
│   ├── agent-kpi-analysis.md
│   ├── agent-main-orchestrator.md
│   └── agents.md            # This file
└── pyproject.toml
```

## Agent Dependencies

```
Main Orchestrator
├── Data Fetcher
│   └── yfinance, pandas, os, time
├── KPI Analysis
│   └── pandas, numpy, sklearn, scipy, matplotlib
└── Logging
    └── logging, json
```

## Configuration & Customization

### Adjust Analysis Parameters
Edit `finance/yfin/main.py`:
```python
ticker = "DBK.DE"  # Change ticker
```

### Modify Cache TTL
Edit `finance/yfin/fetch.py`:
```python
period_cache = 24 * 3600  # Adjust cache duration
```

### Change Clustering Parameters
Edit `finance/yfin/kpi.py`:
```python
num_clusters = 5  # Adjust number of price levels
```

## Testing

Run tests with:
```bash
make test
# or
python -m unittest discover -v
```

Test files:
- `finance/yfin/test_kpi.py`: KPI Analysis tests
- `finance/yfin/test_tr.py`: True Range tests

## Performance Considerations

### Caching Strategy
- YTD data: 30-day cache
- Annual data: 7-day cache
- Monthly+ data: 24-hour cache

### Computation Complexity
- Data Fetching: O(n) - linear in period
- Indicator Calculation: O(n) - vectorized operations
- Clustering: O(k*i*n) - k clusters, i iterations, n samples
- Support/Resistance: O(n*bins) - typically 100 bins

## Troubleshooting

### No Data Retrieved
- Check internet connection
- Verify ticker symbol is correct
- Check Yahoo Finance API availability

### Cache Issues
- Delete `./data/{ticker}_*.csv` files to refresh
- Check disk space in data folder

### Visualization Errors
- Ensure matplotlib display backend is configured
- Check file permissions in `./data/` folder

## Future Enhancements

1. **Multi-ticker Analysis**: Batch process multiple stocks
2. **Strategy Backtesting**: Historical performance testing
3. **Alert System**: Notifications for level breaches
4. **Real-time Updates**: Live price monitoring
5. **Web Dashboard**: Interactive visualization
6. **Database Integration**: Persistent storage of analysis

## Support

For detailed agent documentation, see:
- `agent-data-fetcher.md` - Data retrieval details
- `agent-kpi-analysis.md` - Analysis methodology
- `agent-main-orchestrator.md` - Orchestration patterns

For issues or feedback: https://github.com/anomalyco/opencode
