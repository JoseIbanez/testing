# Yahoo Finance Analysis Project

## Overview

This is a Python-based financial analysis toolkit that fetches and analyzes stock market data from Yahoo Finance. The project performs technical analysis and calculates key performance indicators (KPIs) for various stock ticker symbols.

## Project Structure

```
yahoo-finance/
├── finance/
│   ├── yfin/              # Main Yahoo Finance module
│   │   ├── main.py        # Entry point for analysis
│   │   ├── fetch_serie.py # Data fetching utilities
│   │   ├── fetch_info.py  # Stock information fetching
│   │   ├── kpi.py         # KPI calculations
│   │   ├── levels.py      # Support/resistance level analysis
│   │   ├── cache.py       # Caching functionality
│   │   ├── inventory.py   # Ticker inventory management
│   │   └── many_get.py    # Batch ticker analysis
│   ├── scrape/            # Web scraping utilities
│   └── tests/             # Unit tests
├── data/                  # Data storage
├── sample_data/           # Sample datasets
├── documentation/         # Project documentation
└── setup/                 # Setup configuration
```

## Features

- **Data Fetching**: Download historical stock price data using yfinance
- **Technical Analysis**: Calculate technical indicators for stock analysis
- **KPI Calculations**: Compute financial metrics and volatility measures
- **Level Detection**: Identify support and resistance levels using clustering algorithms
- **Dividend Adjustments**: Handle dividend-adjusted pricing
- **Caching**: Efficient data caching to reduce API calls
- **Batch Processing**: Analyze multiple tickers simultaneously

## Technology Stack

- **Python**: 3.13+
- **Data Processing**: pandas, numpy
- **Statistical Analysis**: scipy, statsmodels
- **Machine Learning**: scikit-learn (for clustering)
- **Visualization**: matplotlib
- **Financial Data**: yfinance
- **Caching**: cachetools
- **Build Tool**: uv (modern Python package manager)

## Installation

### Setup Virtual Environment
```bash
make venv
```

### Install Dependencies
```bash
make sync
```

## Usage

### Analyze Single Ticker
```bash
python -m finance.yfin.main --ticker AAPL
```

### Batch Analysis
```bash
ticker_rev
```

### Run Tests
```bash
make test
```

## Command Line Interface

The main entry point accepts the following arguments:

- `--ticker`, `-t`: Ticker symbol to analyze (default: AAPL)

Example:
```bash
python -m finance.yfin.main -t MSFT
```

## Key Modules

### fetch_serie.py
Handles fetching historical price data for ticker symbols.

### kpi.py
Calculates key performance indicators including:
- Technical indicators
- Volatility metrics
- Summary statistics
- Dividend adjustments

### levels.py
Evaluates support and resistance levels using:
- K-means clustering
- Price level analysis
- Swing point detection

### cache.py
Implements caching mechanisms to optimize data retrieval and reduce redundant API calls.

### inventory.py
Manages ticker symbol inventories for batch processing.

### many_get.py
Entry point for batch processing multiple ticker symbols.

## Development

### Project Configuration
- **Build System**: setuptools >= 77.0
- **Package Manager**: uv
- **Python Version**: >= 3.13

### Running Tests
```bash
cd /home/ibanez/Projects/testing/yahoo-finance && python -m unittest discover -v
```

### Makefile Commands
- `make venv`: Create virtual environment
- `make sync`: Sync dependencies
- `make test`: Run unit tests
- `make branch-cleanup`: Clean up merged git branches

## Data Storage

- `data/`: Primary data storage directory
- `sample_data/`: Sample datasets for testing and examples

## Notes

- The project uses modern Python packaging with `pyproject.toml`
- Caching is implemented to optimize repeated queries
- Supports various international stock exchanges (e.g., .DE for Germany, .OL for Oslo)
- Default analysis period is 5 years

## License

Not specified

## Version

0.0.1
