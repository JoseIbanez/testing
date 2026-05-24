# KPI Analysis Agent

## Overview
The KPI Analysis Agent calculates technical indicators and key performance indicators for stock analysis. It performs clustering, pattern recognition, and volatility analysis to identify trading levels and market trends.

## Location
`finance/yfin/kpi.py`

## Core Functions

### `add_indicators(ticker, df)`
Computes technical indicators and adds them to the dataframe.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `df` (pd.DataFrame): Historical stock data

**Returns:**
- `pd.DataFrame`: Enhanced dataframe with indicators

**Indicators Added:**
- **SMA_5, SMA_10**: Simple Moving Averages (5 and 10-day)
- **MACD**: Moving Average Convergence Divergence
- **Bollinger Bands**: Upper, Lower, and Middle bands
- **RSI**: Relative Strength Index (14-period)
- **Volatility**: True Range percentage volatility

**Output:** Saves indicator data to `./data/{ticker}_indicators.csv`

### `kmeans_clustering(ticker, df)`
Identifies price levels using K-means clustering algorithm.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `df` (pd.DataFrame): Historical stock data with Close prices

**Returns:**
- `numpy.ndarray`: Cluster center prices

**Process:**
1. Normalizes time and price on 0-1 scale
2. Applies K-means clustering (5 clusters)
3. Rescales cluster centers to original price range
4. Generates visualization with price levels

**Output:** Saves plot to `./data/{ticker}_kmeans.png`

### `get_swing_points(ticker, df)`
Identifies swing highs and lows using local extrema detection.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `df` (pd.DataFrame): Historical stock data

**Returns:**
- `pd.DataFrame`: Input dataframe (filtered to last 2 years)

**Process:**
1. Filters data to last 2 years
2. Identifies local maxima (swing highs) with order=5
3. Identifies local minima (swing lows) with order=5
4. Clusters swing points into 8 levels
5. Visualizes with scatter plot overlay

**Output:** Saves plot to `./data/{ticker}_swing_points.png`

### `get_support_resistance(ticker, df)`
Calculates support and resistance levels using volume profile analysis.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `df` (pd.DataFrame): Historical stock data

**Returns:**
- `dict`: Dictionary with keys:
  - `support`: Support price level
  - `resistance`: Resistance price level
  - `max_price`: Historical maximum price
  - `min_price`: Historical minimum price
  - `last_price`: Current price
  - `max_volatility`: Maximum volatility

**Process:**
1. Creates 100 price bins across High-Low range
2. Calculates volume profile for each bin
3. Finds support: highest volume below current price
4. Finds resistance: highest volume above current price
5. Generates dual-panel visualization (price + volume profile)

**Output:** Saves plot to `./data/{ticker}_support_resistance.png`

### `get_summary_kpi(ticker, df_input)`
Calculates summary KPIs for trend analysis.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `df_input` (pd.DataFrame): Historical stock data

**Returns:**
- `dict`: Dictionary with keys:
  - `ticker`: Ticker symbol
  - `max_label`: "at_max" if within 1% of all-time high
  - `max_price`: All-time high price
  - `last_price`: Current price
  - `trend_5_10_pct`: SMA(5) vs SMA(10) divergence percentage
  - `trend_label`: "bullish", "bearish", or "neutral"
  - `diff_200_pct`: Distance from 200-day SMA

**Analysis Period:** Last 2 years

**Trend Rules:**
- Bullish: SMA(5) > SMA(10) by >1%
- Bearish: SMA(5) < SMA(10) by >1%
- Neutral: Difference within ±1%

### `get_last_volatility(ticker, df_input)`
Analyzes volatility since the last swing low.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `df_input` (pd.DataFrame): Historical stock data

**Returns:**
- `dict`: Dictionary with keys:
  - `ticker`: Ticker symbol
  - `number_days`: Days since last swing low
  - `price_diff`: Price change percentage from last swing low
  - `volatility_mean_bullish`: Average volatility on up days
  - `volatility_p80_bullish`: 80th percentile volatility on up days
  - `volatility_mean_bearish`: Average volatility on down days
  - `volatility_p80_bearish`: 80th percentile volatility on down days

**Process:**
1. Identifies last swing low (local minimum with order=5)
2. Filters data from last swing low to present
3. Separates bullish (up) and bearish (down) days
4. Calculates True Range percentage for each
5. Computes mean and 80th percentile for each direction

## Data Persistence

All functions save visualizations as PNG files:
- KMeans: `./data/{ticker}_kmeans.png`
- Swing Points: `./data/{ticker}_swing_points.png`
- Support/Resistance: `./data/{ticker}_support_resistance.png`
- Indicators: `./data/{ticker}_indicators.csv`

## Dependencies
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `scipy.signal.argrelextrema`: Local extrema detection
- `sklearn.cluster.KMeans`: Clustering algorithm
- `matplotlib.pyplot`: Visualization
- `datetime`, `timedelta`: Date handling
