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
    prev_close = df['Close'].shift(1).fillna(df['Close'])
    tr1 = df['High'] - df['Low']
    tr2 = (df['High'] - prev_close).abs()
    tr3 = (df['Low'] - prev_close).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df['Volatility'] = true_range / prev_close * 100


    logger.info("Added indicators to dataframe for %s", ticker)
    #logger.info("Dataframe: %s", df)

    #Save to csv
    #df.to_csv(f"./data/{ticker}_indicators.csv")

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



def meanshift_clustering(ticker: str, df: pd.DataFrame, period_year: int=5) -> pd.DataFrame:
    """
    Calculate support and resistance levels using Mean Shift Clustering
    Not predefined number of clusters, but a bandwidth parameter that defines the radius of the clusters.
    The bandwidth can be estimated using the estimate_bandwidth function from sklearn.
    """

    # Recent samples, last years
    df = df[df.index >= pd.to_datetime(datetime.now() - timedelta(days=period_year*365), utc=True)]


    # Find local maxima (peaks) and minima (troughs)
    # order=3 means it needs 3 lower/higher bars on either side to be a pivot
    #df['max'] = df['High'].iloc[argrelextrema(df['High'].values, np.greater_equal, order=5)[0]]
    #df['min'] = df['Low'].iloc[argrelextrema(df['Low'].values, np.less_equal, order=5)[0]]

    # Identify local maxima (swing highs)
    swing_highs = df.index[argrelextrema(df['High'].values, np.greater_equal, order=10)]
    swing_lows  = df.index[argrelextrema(df['Low'].values, np.less_equal, order=10)]
    swing_close  = df.index[argrelextrema(df['Close'].values, np.less_equal, order=10)]



    # Collect the identified price pivots

    pivots = np.concatenate((df['High'][swing_highs], df['Low'][swing_lows], df['Close'][swing_close]), axis=0)
    print(pivots)

    #pivots = df[['min', 'max']].stack().dropna().values
    #pivots = pd.concat([df['max'].dropna(), df['min'].dropna()]).values


    pivots_reshaped = pivots.reshape(-1, 1)




    # Apply Mean Shift Clustering
    # estimate_bandwidth automatically determines the cluster radius
    bandwidth = estimate_bandwidth(pivots_reshaped, quantile=0.1, n_samples=500)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(pivots_reshaped)

    # Extract the support & resistance levels
    levels = ms.cluster_centers_.flatten()
    levels[::-1].sort()


    levels_score = eval_levels(ticker, df, levels, pivots)


    # Visualize
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label=f'{ticker} Close Price', color='black', alpha=0.6)

    # Plot swing highs and lows
    plt.scatter(swing_highs, df['High'][swing_highs], color='r', label='Swing Highs', marker='o')
    plt.scatter(swing_lows,  df['Low'][swing_lows],   color='g', label='Swing Lows',  marker='o')

    # Plot Mean Shift Levels
    for level in levels:
        plt.axhline(y=level, color='blue', linestyle='--', alpha=0.8)

    plt.title(f'Mean Shift Support and Resistance Levels for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.savefig(f"./data/{ticker}_meanshift.png")

    return levels_score


def eval_levels(ticker: str, df:pd.DataFrame, levels: np.ndarray, pivots: np.ndarray) -> dict:

    # Evaluate the number of pivots for each level
    # Evaluate duration of the level, how many days from first touch to last touch, and from last touch to now
    levels_score = {}
    for level in levels:

        touch_pivot_count = ((pivots >= level * 0.98) & (pivots <= level * 1.02)).sum()


        touch_high = df[(df['High'] >= level * 0.99) & (df['High'] <= level * 1.01) & (df['Low'] < level * 0.99)]
        touch_low = df[(df['Low'] >= level * 0.99) & (df['Low'] <= level * 1.01) & (df['High'] > level * 1.01)]
        touch_points = pd.concat([touch_high, touch_low]).sort_index()


        duration = touch_points.index
        if len(duration) > 0:
            first_touch = duration[0]
            last_touch = duration[-1]
            level_duration = (last_touch - first_touch).days
            level_ago = (df.index[-1] - last_touch).days
        else:
            level_duration = 0
            level_ago = 5 * 365

        # Score based in duration
        if level_duration > 365:
            duration_score = 10
        elif level_duration > 180:
            duration_score = 5
        elif level_duration > 30:
            duration_score = 3
        elif level_duration > 10:
            duration_score = 1
        else:
            duration_score = 0
            level_ago = 5 * 365

        # Score based in how long ago was the last touch
        if level_ago < 30:
            ago_score = 5
        elif level_ago < 90:
            ago_score = 3
        elif level_ago < 180:
            ago_score = 1
        else:
            ago_score = 0

        # Level score
        logger.info("Level: %.2f, Touches: %d, Duration: %d days, Touch Range: %s - %s, Last touch: %d days ago, Score: %d", level, touch_pivot_count, level_duration, first_touch, last_touch, level_ago, int( touch_pivot_count + duration_score + ago_score))
        levels_score[round(float(level), 2)] = int( touch_pivot_count + duration_score + ago_score)

    return levels_score



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

    # Identify last minima (swing lows)
    swing_lows_idx = argrelextrema(df['Low'].values, np.less_equal, order=5)
    swing_lows = df.index[swing_lows_idx]

    #logger.info("Last swing low: %s", swing_lows[-2:])    
    last_min_date = swing_lows[-1]

    df_200d = df[-200:]
    volatility_200d_max = df_200d['Volatility'].max()
    volatility_200d_p99 = df_200d['Volatility'].quantile(0.99)


    df_20d = df[-20:]
    volatility_20d_mean = df_20d['Volatility'].mean()
    volatility_20d_p90 = df_20d['Volatility'].quantile(0.9)

    df_80d = df[-80:]
    volatility_80d_mean = df_80d['Volatility'].mean()
    volatility_80d_p90 = df_80d['Volatility'].quantile(0.9)

    df_near = df[df.index >= last_min_date]
    volatility_near_mean = df_near['Volatility'].mean()
    volatility_near_p95 = df_near['Volatility'].quantile(0.95)
    volatility_near_max = df_near['Volatility'].max()

    close_price = float(df['Close'].iloc[-1])
    ema_200 = float(df_200d['EMA_200'].iloc[-1])
    rsi_14 = float(df['RSI'].iloc[-1])

    volatility = {
        "ticker": ticker,
        "volatility_200d_max": round(volatility_200d_max, 2),
        "volatility_200d_p99": round(volatility_200d_p99, 2),
        "volatility_80d_mean": round(volatility_80d_mean, 2),
        "volatility_80d_p90": round(volatility_80d_p90, 2),
        "volatility_20d_mean": round(volatility_20d_mean, 2),
        "volatility_20d_p90": round(volatility_20d_p90, 2),
        "volatility_near_days": len(df_near),
        "volatility_near_mean": round(volatility_near_mean, 2),
        "volatility_near_p95": round(volatility_near_p95, 2),
        "volatility_near_max": round(volatility_near_max, 2),
        "close_price": round(close_price, 2),
        "ema_200": round(ema_200, 2),
        "rsi_14": round(rsi_14, 2)
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

    # Recent samples, last years
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
    break_dates["break_max_price"] = df['Close'][break_dates.index]

    #Remove break if max price is higher than resistance * safeguard pct
    #print(break_dates)
    break_dates = break_dates[break_dates["break_max_price"] <= resistance * 1.2]
    #print(break_dates)

    # get top 5 longest breaks
    big_breaks = break_dates[break_dates["break_duration"] > pd.Timedelta(days=10)].sort_values(by="break_duration", ascending=False).head(5)
    big_breaks = big_breaks.sort_index()

    # Calculate how many days ago the break ended from last date in the dataframe
    big_breaks["ago_begin"] = pd.Series(df.index[-1], index=big_breaks.index) - big_breaks["break_begin"]
    big_breaks["ago_end"]   = pd.Series(df.index[-1], index=big_breaks.index) - big_breaks["break_end"]

    # Number of times the price has touched the resistance level
    touch_count = ((df['Close'] > resistance * 0.99) & (df['Close'] < resistance * 1.01)).sum()

    # Last price
    last_price = df['Close'].iloc[-1]
    min_ago_end = big_breaks["ago_end"].min().days if not big_breaks.empty else None
    if not min_ago_end or min_ago_end > 90:
        logger.info("Resistance %s for %s is too old, last touch %s days ago", resistance, ticker, min_ago_end)
        return None

    print(big_breaks)

    breaks_kpi = {
        "ticker": ticker,
        "resistance": float(resistance),
        "price_diff_pct": float((df['Close'].iloc[-1] - resistance) / resistance * 100),
        "breaks_begin": big_breaks["break_begin"].min().to_pydatetime(),
        "breaks_end": big_breaks["break_end"].max().to_pydatetime(),
        "breaks_duration": (big_breaks["break_end"].max() - big_breaks["break_begin"].min()).days, 
        "ago_begin": big_breaks["ago_begin"].max().days,
        "ago_end": big_breaks["ago_end"].min().days,
        "touch_count": int(touch_count)
    }

    print(breaks_kpi)



def adjust_dividents(ticker: str, df_input: pd.DataFrame) -> pd.DataFrame:
    """
    Adjust the price for dividends
    """

    df = df_input

    dividends = df[ df['Dividends'] > 0 ]['Dividends'].to_dict()

    #print("Dividends: ", dividends)
    #print("Dataframe: without adj ", df)

    # Adjust the price for dividends
    for date, dividend in dividends.items():
        df.loc[:date, 'Close'] -= dividend
        df.loc[:date, 'Open'] -= dividend
        df.loc[:date, 'High'] -= dividend
        df.loc[:date, 'Low'] -= dividend

    #print("Dataframe: with adj ", df)

    return df



def detect_break_retest(ticker: str, df_input: pd.DataFrame) -> dict:
    """
    Detect break and retest of a level
    """

    long_period = 200
    short_period = 20

    df = df_input[df_input.index >= pd.to_datetime(datetime.now() - timedelta(days=long_period), utc=True)]

    max_l_price = df['High'].max()
    max_l_date  = df['High'].idxmax()
    max_l_session_ago = len(df.index) - df.index.get_loc(max_l_date)

    # Recent samples, last days
    df = df_input[df_input.index >= pd.to_datetime(datetime.now() - timedelta(days=short_period), utc=True)]
    max_s_price = df['High'].max()
    max_s_date  = df['High'].idxmax()
    max_s_session_ago = len(df.index) - df.index.get_loc(max_s_date)

    # Samples after last maximum, last days
    df = df_input[df_input.index > max_s_date]
    if len(df) == 0:
        logger.info("MAX")
        return {}

    min_s_price = df['Low'].min()
    min_s_date  = df['Low'].idxmin()
    min_s_session_ago = len(df.index) - df.index.get_loc(min_s_date)

    labels = []
    if min_s_price and min_s_price < max_s_price * 0.95:
        logger.info("Found trick")
        labels = ["MAX_FALL"]



    retest = {
        "ticker": ticker,
        "max_l_session_ago": int(max_l_session_ago),
        "max_s_session_ago": int(max_s_session_ago),
        "min_s_session_ago": int(min_s_session_ago),
        "labels": labels,
        "fall_pct": float((max_s_price - min_s_price) / max_s_price * 100) if min_s_price else None
    }

    logger.info(retest)

    return retest