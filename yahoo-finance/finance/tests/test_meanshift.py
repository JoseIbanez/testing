import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth
from scipy.signal import argrelextrema

# 1. Fetch historical data
ticker = "PLD"
df = yf.download(ticker, start="2020-01-01", end="2026-06-01", interval="1d")


# 2. Find local maxima (peaks) and minima (troughs)
# order=3 means it needs 3 lower/higher bars on either side to be a pivot
df['min'] = df['Close'].iloc[argrelextrema(df['Close'].values, np.less_equal, order=3)[0]]
df['max'] = df['Close'].iloc[argrelextrema(df['Close'].values, np.greater_equal, order=3)[0]]





# 3. Collect the identified price pivots
#pivots = df[['min', 'max']].stack().dropna().values
pivots = pd.concat([df['min'].dropna(), df['max'].dropna()]).values
pivots_reshaped = pivots.reshape(-1, 1)


# 4. Apply Mean Shift Clustering
# estimate_bandwidth automatically determines the cluster radius
bandwidth = estimate_bandwidth(pivots_reshaped, quantile=0.15, n_samples=500)
ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(pivots_reshaped)

# 5. Extract the support & resistance levels
levels = ms.cluster_centers_.flatten()

# 6. Visualize
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Close'], label=f'{ticker} Close Price', color='black', alpha=0.6)

# Plot Mean Shift Levels
for level in levels:
    plt.axhline(y=level, color='blue', linestyle='--', alpha=0.8)

plt.title(f'Mean Shift Support and Resistance Levels for {ticker}')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.savefig(f"./data/{ticker}_meanshift.png")
