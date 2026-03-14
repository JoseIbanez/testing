import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.signal import argrelextrema


logger = logging.getLogger(__name__)


def add_indicators(ticker: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Add technical indicators to the dataframe
    - SMA(5,10)
    - RSI
    - Volatility
    - MACD
    - Bollinger Bands
    """

    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
    df['Bollinger_Bands'] = df['Close'].rolling(window=20).mean() + 2 * df['Close'].rolling(window=20).std()
    df['Bollinger_Bands_Lower'] = df['Close'].rolling(window=20).mean() - 2 * df['Close'].rolling(window=20).std()
    df['Bollinger_Bands_Upper'] = df['Close'].rolling(window=20).mean() + 2 * df['Close'].rolling(window=20).std()

    # RSI Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Volatility (True Range)
    prev_close = df['Close'].shift(1)
    tr1 = df['High'] - df['Low']
    tr2 = (df['High'] - prev_close).abs()
    tr3 = (df['Low'] - prev_close).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df['Volatility'] = true_range / prev_close.fillna(df['Close']) * 100


    logger.info("Added indicators to dataframe for %s", ticker)
    logger.info("Dataframe: %s", df)

    #Save to csv
    df.to_csv(f"./data/{ticker}_indicators.csv")

    return df


def kmeans_clustering(ticker: str, df: pd.DataFrame) -> pd.DataFrame:
    # href: https://archive.ph/wEnbh#selection-2703.0-2719.7


    # Preparing data for clustering: Normalize time and price to have similar scales
    X_time = np.linspace(0, 1, len(df)).reshape(-1, 1)
    X_price = (df['Close'].values - np.min(df['Close'])) / (np.max(df['Close']) - np.min(df['Close']))
    X_cluster = np.column_stack((X_time, X_price))

    # Applying KMeans clustering
    num_clusters = 5
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(X_cluster)

    # Extract cluster centers and rescale back to original price range
    cluster_centers = kmeans.cluster_centers_[:, 1] * (np.max(df['Close']) - np.min(df['Close'])) + np.min(df['Close'])

    # Plotting
    plt.figure(figsize=(28,7))
    plt.plot(df['Close'], label="Close Price")
    for center in cluster_centers:
        plt.axhline(y=center, color='r', linestyle='--')
        plt.annotate(f"{center:.2f}", xy=(df.index[-1], center * 1.01), xytext=(5,0), textcoords="offset points", fontsize=15, ha='left', va='center', color='r')

    plt.title(f'{ticker} Price Data with KMeans Clustering')
    plt.legend()
    plt.savefig(f"./data/{ticker}_kmeans.png")
    logger.info("Saved plot for %s to %s", ticker, f"./data/{ticker}_kmeans.png")

    return cluster_centers

def get_swing_points(ticker: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate swing points
    """

    # Identify local maxima (swing highs)
    swing_highs_idx = argrelextrema(df['High'].values, np.greater_equal, order=5)
    swing_highs = df.index[swing_highs_idx]
    # Identify local minima (swing lows)
    swing_lows_idx = argrelextrema(df['Low'].values, np.less_equal, order=5)
    swing_lows = df.index[swing_lows_idx]

    logger.info("Swing highs values: \n%s", df['High'][swing_highs])
    logger.info("Swing lows values: \n%s", df['Low'][swing_lows])

    # Preparing data for clustering for swing points:
    sv = np.concatenate((df['High'][swing_highs], df['Low'][swing_lows]), axis=0)
    logger.info("Swing points: %s", sv)

    # Normalize time and price to have similar scales
    X_time = np.linspace(0, 1, len(sv)).reshape(-1, 1)
    X_price = (sv - np.min(sv)) / (np.max(sv) - np.min(sv))
    X_cluster = np.column_stack((X_time, X_price))

    # Applying KMeans clustering
    num_clusters = 8
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(X_cluster)

    # Extract cluster centers and rescale back to original price range
    cluster_centers = kmeans.cluster_centers_[:, 1] * (np.max(df['High']) - np.min(df['Low'])) + np.min(df['Low'])


    # Plotting
    plt.figure(figsize=(24,8))
    plt.plot(df['Close'], label="Close Price")
    plt.scatter(swing_highs, df['High'][swing_highs], color='r', label='Swing Highs', marker='o')
    plt.scatter(swing_lows, df['Low'][swing_lows], color='g', label='Swing Lows', marker='o')

    for center in cluster_centers:
        plt.axhline(y=center, color='r', linestyle='--')
        plt.annotate(f"{center:.2f}", xy=(df.index[-1], center * 1.01), xytext=(5,0), textcoords="offset points", fontsize=15, ha='left', va='center', color='r')



    plt.title(f'{ticker} with Swing Highs & Lows')
    plt.legend()
    plt.savefig(f"./data/{ticker}_swing_points.png")
    logger.info("Saved plot for %s to %s", ticker, f"./data/{ticker}_swing_points.png")

    return df

def get_support_resistance(ticker: str, df: pd.DataFrame) -> dict:
    """
    Calculate support and resistance levels
    """
 
    # Calculate volume profile
    price_bins = np.linspace(df['Low'].min(), df['High'].max(), 100)
    volume_profile = []

    for i in range(len(price_bins)-1):
        bin_mask = (df['Close'] > price_bins[i]) & (df['Close'] <= price_bins[i+1])
        volume_profile.append(df['Volume'][bin_mask].sum())

    # Estimating support and resistance
    current_price = df['Close'].iloc[-1]
    support_idx = np.argmax(volume_profile[:np.digitize(current_price, price_bins)])
    resistance_idx = np.argmax(volume_profile[np.digitize(current_price, price_bins):]) + np.digitize(current_price, price_bins)

    support_price = price_bins[support_idx]
    resistance_price = price_bins[resistance_idx]

    # Plotting
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 5), gridspec_kw={'width_ratios': [3, 1]})
    ax1.plot(df['Close'], label="Close Price")
    ax1.axhline(y=support_price, color='g', linestyle='--', label='Support')
    ax1.axhline(y=resistance_price, color='r', linestyle='--', label='Resistance')
    ax1.legend()
    ax1.set_title(f'{ticker} Price Data')
    ax2.barh(price_bins[:-1], volume_profile, height=(price_bins[1] - price_bins[0]), color='blue', edgecolor='none')
    ax2.set_title('Volume Profile')

    plt.tight_layout()
    plt.savefig(f"./data/{ticker}_support_resistance.png")
    logger.info("Saved plot for %s to %s", ticker, f"./data/{ticker}_support_resistance.png")

    print(f"Estimated Support Price: {support_price:.2f}")
    print(f"Estimated Resistance Price: {resistance_price:.2f}")

    levels = {
        "support": support_price,
        "resistance": resistance_price
    }

    return levels
