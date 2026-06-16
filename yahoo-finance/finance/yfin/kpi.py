import json
import logging
from numpy.strings import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift, estimate_bandwidth
from scipy.signal import argrelextrema
from datetime import datetime, timedelta

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
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
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
    #logger.info("Dataframe: %s", df)

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



def meanshift_clustering(ticker: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate support and resistance levels using Mean Shift Clustering
    Not predefined number of clusters, but a bandwidth parameter that defines the radius of the clusters.
    The bandwidth can be estimated using the estimate_bandwidth function from sklearn.
    """

    # Recent samples, last years
    df = df[df.index >= pd.to_datetime(datetime.now() - timedelta(days=10*365), utc=True)]


    # Find local maxima (peaks) and minima (troughs)
    # order=3 means it needs 3 lower/higher bars on either side to be a pivot
    df['min'] = df['Close'].iloc[argrelextrema(df['Close'].values, np.less_equal, order=3)[0]]
    df['max'] = df['Close'].iloc[argrelextrema(df['Close'].values, np.greater_equal, order=3)[0]]


    # Collect the identified price pivots
    #pivots = df[['min', 'max']].stack().dropna().values
    pivots = pd.concat([df['min'].dropna(), df['max'].dropna()]).values
    pivots_reshaped = pivots.reshape(-1, 1)


    # Apply Mean Shift Clustering
    # estimate_bandwidth automatically determines the cluster radius
    bandwidth = estimate_bandwidth(pivots_reshaped, quantile=0.1, n_samples=500)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(pivots_reshaped)

    # Extract the support & resistance levels
    levels = ms.cluster_centers_.flatten()
    levels[::-1].sort()

    # Visualize
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

    return levels


def get_swing_points(ticker: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate swing points
    """

    # Recent samples, last 5 years
    df = df[df.index >= pd.to_datetime(datetime.now() - timedelta(days=5*365), utc=True)]

    # Identify local maxima (swing highs)
    swing_highs_idx = argrelextrema(df['High'].values, np.greater_equal, order=5)
    swing_highs = df.index[swing_highs_idx]
    # Identify local minima (swing lows)
    swing_lows_idx = argrelextrema(df['Low'].values, np.less_equal, order=5)
    swing_lows = df.index[swing_lows_idx]

    #logger.info("Swing highs values: \n%s", df['High'][swing_highs])
    #logger.info("Swing lows values: \n%s", df['Low'][swing_lows])

    # Preparing data for clustering for swing points:
    sv = np.concatenate((df['High'][swing_highs], df['Low'][swing_lows]), axis=0)
    #logger.info("Swing points: %s", sv)

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


    logger.info("Volume profile: %s", volume_profile[np.digitize(current_price, price_bins):])
    logger.info("Price bins: %s", np.digitize(current_price, price_bins))
    resistance_bins = volume_profile[np.digitize(current_price, price_bins):]
    if len(resistance_bins) == 0:
        resistance_idx = len(price_bins) - 2  # Last bin if no bins above current price
    else:
        resistance_idx = np.argmax(resistance_bins) + np.digitize(current_price, price_bins)

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

    #Global kpi
    max_price = df['Close'].max()
    min_price = df['Close'].min()
    last_price = df['Close'].iloc[-1]
    
    max_volatility = df['Volatility'].max()
    

    levels = {
        "support": support_price,
        "resistance": resistance_price,
        "max_price": max_price,
        "min_price": min_price,
        "last_price": last_price,
        "max_volatility": max_volatility
    }

    return levels



def get_summary_kpi(ticker: str, df_input: pd.DataFrame) -> dict:
    """
    Calculate support and resistance levels
    """
 

    # Recent samples, last 2 years
    df = df_input[df_input.index >= pd.to_datetime(datetime.now() - timedelta(days=2*365), utc=True)]


    #Global kpi
    max_price = df['Close'].max()
    last_price = df['Close'].iloc[-1]


    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    
   
    # Trend
    trend_5_10 = ( df['SMA_5'].iloc[-1] - df['SMA_10'].iloc[-1] ) / df['SMA_10'].iloc[-1] * 100
    if trend_5_10 > 1:
        trend = "bullish"
    elif trend_5_10 < -1:
        trend = "bearish"
    else:
        trend = "neutral"

    # Distance to max
    diff_to_max = ( max_price - last_price ) / max_price * 100
    if diff_to_max < 1:
        max_label = "at_max"
    else:
        max_label = None


    diff_200 = ( df['Close'].iloc[-1] - df['SMA_200'].iloc[-1] ) / df['SMA_200'].iloc[-1] * 100


    levels = {
        "ticker": ticker,
        "max_label": max_label,
        "max_price": max_price,
        "last_price": last_price,
        "trend_5_10_pct": trend_5_10,
        "trend_label": trend,
        "diff_200_pct": diff_200
    }

    return levels

def get_last_bb_volatility(ticker: str, df_input: pd.DataFrame) -> dict:
    """
    Calculate volatility
    From last minimum (swing low) to now, 
    Calculate the volatility of bullish vs bearish days, 
    and the price difference in percentage. 
    """


    # Recent samples, last 2 years
    df = df_input[df_input.index >= pd.to_datetime(datetime.now() - timedelta(days=2*365), utc=True)]
    
    # Identify local minima (swing lows)
    swing_lows_idx = argrelextrema(df['Low'].values, np.less_equal, order=5)
    swing_lows = df.index[swing_lows_idx]

    logger.info("Last swing low: %s", swing_lows[-2:])    
    last_min_date = swing_lows[-1]


    last_df = df[df.index >= last_min_date]
    df_bullish = last_df[last_df['Close'] > last_df['Close'].shift(1)]
    df_bearish = last_df[last_df['Close'] < last_df['Close'].shift(1)]

    tr_bullish = (df_bullish['High'] - df_bullish['Low']) / df_bullish['Low'] * 100
    tr_bearish = (df_bearish['High'] - df_bearish['Low']) / df_bearish['Low'] * 100

    #logger.info("tr_bullish: %s", tr_bullish)
    #logger.info("tr_bearish: %s", tr_bearish)

    volatility_mean_bullish = tr_bullish.mean()
    volatility_p80_bullish = tr_bullish.quantile(0.8)

    volatility_mean_bearish = tr_bearish.mean()
    volatility_p80_bearish = tr_bearish.quantile(0.8)

    number_days = len(last_df)
    price_diff = (last_df['Close'].iloc[-1] - last_df['Close'].iloc[0]) / last_df['Close'].iloc[0] * 100

    volatility = {
        "ticker": ticker,
        "number_days": number_days,
        "price_diff": price_diff,
        "volatility_mean_bullish": volatility_mean_bullish,
        "volatility_p80_bullish": volatility_p80_bullish,
        "volatility_mean_bearish": volatility_mean_bearish,
        "volatility_p80_bearish": volatility_p80_bearish
    }

    return volatility



def get_last_volatility(ticker: str, df_input: pd.DataFrame) -> dict:
    """
    Calculate volatility.
    Meditum range (30 days) volatility, from last minimum (swing low) to now,
    """

    # Recent samples, last 1 years
    df = df_input[df_input.index >= pd.to_datetime(datetime.now() - timedelta(days=365), utc=True)]

    # Identify local minima (swing lows)
    swing_lows_idx = argrelextrema(df['Low'].values, np.less_equal, order=5)
    swing_lows = df.index[swing_lows_idx]

    #logger.info("Last swing low: %s", swing_lows[-2:])    
    last_min_date = swing_lows[-1]

    volatility_1y_max = df['Volatility'].max()
    volatility_1y_p90 = df['Volatility'].quantile(0.99)

    df_30d = df[-30:]
    volatility_30s_mean = df_30d['Volatility'].mean()
    volatility_30s_p90 = df_30d['Volatility'].quantile(0.9)

    df_near = df[df.index >= last_min_date]
    volatility_near_mean = df_near['Volatility'].mean()
    volatility_near_p95 = df_near['Volatility'].quantile(0.95)
    volatility_near_max = df_near['Volatility'].max()
    ema_200 = df_near['EMA_200'].iloc[-1]

    volatility = {
        "ticker": ticker,
        "ema_200": round(ema_200, 2),
        "volatility_30s_mean": round(volatility_30s_mean, 2),
        "volatility_30s_p90": round(volatility_30s_p90, 2),
        "volatility_near_days": len(df_near),
        "volatility_near_mean": round(volatility_near_mean, 2),
        "volatility_near_p95": round(volatility_near_p95, 2),
        "volatility_near_max": round(volatility_near_max, 2),
        "volatility_1y_max": round(volatility_1y_max, 2),
        "volatility_1y_p90": round(volatility_1y_p90, 2)
    }
    return volatility


def get_lateral_rectangle(ticker: str, df_input: pd.DataFrame) -> dict:
    """
    Check if the price is in a lateral rectangle (sideways movement)
    """
    RECTANGLE_THRESHOLD_PCT = 3

    # Recent samples, last 2 years
    df = df_input[df_input.index >= pd.to_datetime(datetime.now() - timedelta(days=2*365), utc=True)]
    #df = df[:-1]  # Exclude last day for analysis


    current_price = df['Close'].iloc[-1]
    threshold_price = current_price * (1 + RECTANGLE_THRESHOLD_PCT / 100)

    #Search start date for lateral rectangle, where low price is higher than current price, with a margin of 5%

    #Get dates where low price is higher than current price with a margin of 5%
    higher_dates = df[df['Close'] > threshold_price].index
    #logger.info("Threshold %s, Higher dates: %s", threshold_price, higher_dates[-20:])

    # Get the items position in the original dataframe where close price is higher than current price with a margin of 5%
    higher_items = df.index.get_indexer(higher_dates)
    #logger.info("Higher items: %s", higher_items[-20:])

    #Search last three consecutive items 
    start_index = None
    for i in reversed(range(2,len(higher_items))):
        if higher_items[i] == higher_items[i-1] + 1 == higher_items[i-2] + 2:
            start_index = higher_items[i]
            break
    
    if start_index is None:
        logger.info("Rectacgle start not found for %s", ticker)
        return

    if len(df) - start_index < 30:
        logger.info("Rectangle so short for %s, sessions: %d", ticker, len(df) - start_index)
        return


    df_rectangle = df.iloc[start_index:]
    start_date: pd.Timestamp = df_rectangle.index[0]
    end_date: pd.Timestamp = df_rectangle.index[-1]
    max_price = df_rectangle['High'].max()
    min_price = df_rectangle['Low'].min()
    price_diff_pct = (max_price - min_price) / min_price * 100

    logger.info("Rectangle size date:%s to %s, sessions:(%d), price:%.02f-%.02f (%d%%)", start_date.date(), end_date.date(), len(df_rectangle), min_price, max_price, price_diff_pct)




    date_start = df[df['Low'] > current_price * 1.05].index.max()
    if pd.isna(date_start):
        logger.info("No date found with low price higher than current price for %s", ticker)
    
    logger.info("Current price: %s, Date start for lateral box: %s", current_price, date_start)


    # Identify local maxima (swing highs)
    swing_highs_idx = argrelextrema(df['High'].values, np.greater_equal, order=5)
    swing_highs = df.index[swing_highs_idx]

    #logger.info("Last swing highs: %s", swing_highs)
    logger.info("Swing highs values: \n%s", df['High'][swing_highs[-10:]])

    # Identify local minima (swing lows)
    swing_lows_idx = argrelextrema(df['Low'].values, np.less_equal, order=5)
    swing_lows = df.index[swing_lows_idx]
    logger.info("Swing lows values: \n%s", df['Low'][swing_lows[-10:]])



    #logger.info("Last swing low: %s", swing_lows[-2:])    
    last_min_date = swing_lows[-1]

    df_near = df[df.index >= last_min_date]
    price_diff = (df_near['Close'].iloc[-1] - df_near['Close'].iloc[0]) / df_near['Close'].iloc[0] * 100

    lateral_box = abs(price_diff) < 5  # Example threshold for lateral box

    result = {
        "ticker": ticker,
        "lateral_box": lateral_box,
        "price_diff_pct": price_diff
    }

    return result


def eval_resistance(ticker: str, df_input: pd.DataFrame, resistance: float) -> dict:
    """
    Look for period resistance is not broken
    Evaluate how strong the resistance levels is
    Count how many times the price has touched the resistance level
    """

    # Recent samples, last 5 years
    df = df_input[df_input.index >= pd.to_datetime(datetime.now() - timedelta(days=10*365), utc=True)]
    df['SMA_5'] = df['Close'].rolling(window=5).mean()

    # Resistence duration:
    # Last time the price was above the resistance level for more than 5 consecutive days
    #breaks = df['Close'] > resistance
    breaks = df['SMA_5'] > resistance 
    window_size = 5
    consecutive_count = breaks.rolling(window=window_size).sum()

    break_dates = df[consecutive_count >= window_size][['Close']]
    break_dates["break_begin"] = pd.Series(break_dates.index, index=break_dates.index).shift(1)
    break_dates["break_end"]   = pd.Series(break_dates.index, index=break_dates.index)
    break_dates["break_duration"] = break_dates["break_end"] - break_dates["break_begin"]

    # get top 5 longest breaks
    big_breaks = break_dates[break_dates["break_duration"] > pd.Timedelta(days=10)].sort_values(by="break_duration", ascending=False).head(5)

    # Calculate how many days ago the break ended from last date in the dataframe
    big_breaks["ago_begin"] = pd.Series(df.index[-1], index=big_breaks.index) - big_breaks["break_begin"]
    big_breaks["ago_end"]   = pd.Series(df.index[-1], index=big_breaks.index) - big_breaks["break_end"]


    print(big_breaks)

    breaks_kpi = {
        "ticker": ticker,
        "resistance": float(resistance),
        "price_diff_pct": float((df['Close'].iloc[-1] - resistance) / resistance * 100),
        "breaks_begin": big_breaks["break_begin"].min().to_pydatetime(),
        "breaks_end": big_breaks["break_end"].max().to_pydatetime(),
        "breaks_duration": (big_breaks["break_end"].max() - big_breaks["break_begin"].min()).days, 
        "ago_begin": big_breaks["ago_begin"].max().days,
        "ago_end": big_breaks["ago_end"].min().days
    }

    print(breaks_kpi)


