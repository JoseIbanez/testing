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



def meanshift_clustering(ticker: str, df: pd.DataFrame, period_year: int=5, visualize:bool=False) -> pd.DataFrame:
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

    # Identify local maxima, min (swing highs)
    ORDER = 10
    swing_highs   = df.index[argrelextrema(df['High'].values,  np.greater_equal, order=ORDER)]
    swing_lows    = df.index[argrelextrema(df['Low'].values,   np.less_equal,    order=ORDER)]
    swing_h_close = df.index[argrelextrema(df['Close'].values, np.greater_equal, order=ORDER)]
    swing_l_close = df.index[argrelextrema(df['Close'].values, np.less_equal,    order=ORDER)]


    # Collect the identified price pivots
    pivots = np.concatenate((df['High'][swing_highs], df['Low'][swing_lows]), axis=0)
    #pivots = np.concatenate((df['High'][swing_highs], df['Low'][swing_lows], df['Close'][swing_h_close], df['Close'][swing_l_close]), axis=0)

    logger.debug("pivots: %s", pivots)
    #pivots = df[['min', 'max']].stack().dropna().values
    #pivots = pd.concat([df['max'].dropna(), df['min'].dropna()]).values
    pivots_reshaped = pivots.reshape(-1, 1)


    # Apply Mean Shift Clustering
    # estimate_bandwidth automatically determines the cluster radius
    QUANTILE = 0.1
    bandwidth = estimate_bandwidth(pivots_reshaped, quantile=QUANTILE, n_samples=500)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(pivots_reshaped)

    # Extract the support & resistance levels
    levels = ms.cluster_centers_.flatten()
    levels[::-1].sort()

    
    if not visualize:
        return levels

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

    return levels



def eval_levels__old(ticker: str, df:pd.DataFrame, levels: np.ndarray, pivots: np.ndarray) -> dict:

    # Evaluate the number of pivots for each level
    # Evaluate duration of the level, how many days from first touch to last touch, and from last touch to now
    levels_score = {}
    for level in levels:

        level_result = eval_level2(ticker, df, level, pivots)
        date_groups = group_dates(level_result["touch_dates"], max_gap_days=5)


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




def eval_level2(ticker: str, df:pd.DataFrame, level: float, pivots: np.ndarray) -> dict:
    """
    Evaluate a support/resistance level relevance, 
    by counting the number of touches, and the number of breaks.

    Returns a dictionary
    """

    logger.info("Ticker:%s, Evaluating level: %.2f", ticker, level)

    TRM = 0.3 # True Range Margin, % of the true range is used to determine if the price is near the level
    df['true_range'] = df['High'] - df['Low']

    df["sr"] = None
    df["srs"] = None
    df["break"] = None
    df["position"] = range(len(df))

    # Crossing the level, with a margin of TRM% of the true range
    df.loc[(df['High'] - df['true_range'] * TRM  >= level) & (df['Low'] + df['true_range'] * TRM <= level), "sr"] = 0

    # Resistance: High is arround level with margin TRM% of true range, Low is below the level
    df.loc[(df['High'] + df['true_range'] * TRM >= level) & (df['High'] - df['true_range'] * TRM <= level) & (df['Low'] < level), "sr"] = -1

    # Support: Low is arround level with margin TRM% of true range, High is above the level
    df.loc[(df['Low'] + df['true_range'] * TRM >= level) & (df['Low'] - df['true_range'] * TRM <= level) & (df['High'] > level), "sr"] = 1



    # When near crossing the level session, and below level, set resistence
    df.loc[((df['sr'].shift(1) == 0) | (df['sr'].shift(-1) == 0)) & (df['High'] < level), "sr"] = -2

    # When near crossing the level session, and above level, set support
    df.loc[((df['sr'].shift(1) == 0) | (df['sr'].shift(-1) == 0)) & (df['Low'] > level), "sr"] = 2


    #select level dates (sr is not null) adn sr value for further analysis
    level_dates = df[df['sr'].notnull()][['High', 'Low', 'true_range', 'sr', 'position']]
    level_analysis = analyze_level_dates(ticker, level, level_dates)

    swing_group = group_dates(ticker, level_analysis["swing_sessions"], df, max_gap_days=5)
    break_group = group_dates(ticker, level_analysis["break_sessions"], df, max_gap_days=5)

    result = {
        "ticker": ticker,
        "level": level,
        "swing_count": len(swing_group),
        "break_count": len(break_group),
        "first_session_ago": len(df) - level_analysis["swing_sessions"][0] if len(level_analysis["swing_sessions"]) > 0 else None,
        "last_session_ago": len(df) - level_analysis["swing_sessions"][-1] if len(level_analysis["swing_sessions"]) > 0 else None,
        "duration_sessions": level_analysis["swing_sessions"][-1] - level_analysis["swing_sessions"][0] if len(level_analysis["swing_sessions"]) > 0 else None,
    }

    logger.info("Ticker: %s, Level: %.2f, #Swings: %d, #Breaks: %d, First session ago: %s, Last session ago: %s, Duration sessions: %s",
                ticker, level, 
                len(swing_group), len(break_group), 
                result['first_session_ago'], result['last_session_ago'], result['duration_sessions'])

    return result



def analyze_level_dates(ticker: str, level: float, ld: pd.DataFrame) -> list[datetime]:
    """
    Analyze the level dates to find swing dates support or resistance

    Parameters:
    - ticker: str, the stock ticker symbol
    - level: float, the support/resistance level being analyzed
    - ld: pd.DataFrame, a DataFrame containing the level dates with columns ['High', 'Low', 'true_range', 'sr', 'position']
    
    Returns:
      a dictionary with swing sessions and break sessions

    """

    BLOCK_DAYS = 5

    # Identify swing dates
    swing_dates = []
    swing_sessions = []
    cross_dates = []
    cross_sessions = []

    side = 0
    last_session = None
    

    # Iterate through the level dates to find swing dates
    for i in range(1, len(ld)):

        # Current zone, -1, 0, 1: resistence, crossing, support
        cur_sr = ld['sr'].iloc[i] / abs(ld['sr'].iloc[i]) if ld['sr'].iloc[i] != 0 else 0

        # New block of sessions, reset side
        if last_session is None or last_session + BLOCK_DAYS < ld['position'].iloc[i]:
            side = cur_sr

        last_session = ld['position'].iloc[i]

        # Session is crossing the level
        if cur_sr == 0:
            continue

        # Session is crossing the level
        if side == 0:
            side = cur_sr

        # Resistence or support, last zone is the same for the current day (session)
        if cur_sr == side and side != 0:
            swing_dates.append(ld.index[i])
            swing_sessions.append(ld['position'].iloc[i])

        # Break, last zone is different for the current day (session)
        if cur_sr != side and side != 0:
            cross_dates.append(ld.index[i])
            cross_sessions.append(ld['position'].iloc[i])

    logger.info("Break dates for level %.2f: %s", level, [ _date.strftime("%Y-%m-%d") for _date in cross_dates ])

    # Remove swing sessions that are too close to cross/break sessions
    for cross_session in cross_sessions:
        swing_sessions = [swing_session for swing_session in swing_sessions if swing_session < cross_session - BLOCK_DAYS or swing_session > cross_session + BLOCK_DAYS]

    # Convert sessions back to dates
    swing_dates = [swing_date for swing_date in swing_dates if ld['position'].loc[swing_date] in swing_sessions]

    #logger.info("Swing sessions for level %.2f: %s", level, swing_sessions)
    logger.info("Swing dates for level %.2f: %s", level, [ _date.strftime("%Y-%m-%d") for _date in swing_dates ])


    return {"swing_dates": swing_dates, 
            "swing_sessions": swing_sessions,
            "break_dates": cross_dates,
            "break_sessions": cross_sessions}




def group_dates(ticker:str, sessions: list[int], df:pd.DataFrame, max_gap_days: int = 5) -> list:
    """
    Group dates that are close to each other (within max_gap_days)
    dates is a pandas ordered Series of datetime objects 
    """
    if len(sessions) == 0:
        return []

    grouped_sessions = []
    current_group = [sessions[0]]

    for i in range(1, len(sessions)):
        if (sessions[i] - current_group[-1]) <= max_gap_days:
            current_group.append(sessions[i])
        else:
            grouped_sessions.append(current_group)
            current_group = [sessions[i]]

    grouped_sessions.append(current_group)


    date_kpi_list = []
    for group in grouped_sessions:
        kpi = {}
        kpi['start_date'] = df.index[group[0]]
        kpi['end_date'] = df.index[group[-1]]
        date_kpi_list.append(kpi)


    logger.info("Grouped dates: %s", date_kpi_list)


    return date_kpi_list








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
    Calculate support and resistance levels, by volume profile and price bins, 
    and return the levels with the highest volume.
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

