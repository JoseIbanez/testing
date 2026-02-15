import logging
import pandas as pd

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
    #df['RSI'] = df['Close'].rolling(window=14).apply(lambda x: (x[-1] - x.mean()) / x.mean() * 100)
    #df['Volatility'] = df['Close'].rolling(window=20).std()
    df['Volatility'] = (df['High'] - df['Low'])/df['Close'] * 100
    df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
    df['Bollinger_Bands'] = df['Close'].rolling(window=20).mean() + 2 * df['Close'].rolling(window=20).std()
    df['Bollinger_Bands_Lower'] = df['Close'].rolling(window=20).mean() - 2 * df['Close'].rolling(window=20).std()
    df['Bollinger_Bands_Upper'] = df['Close'].rolling(window=20).mean() + 2 * df['Close'].rolling(window=20).std()
    

    logger.info("Added indicators to dataframe for %s (%s)", ticker)
    logger.info("Dataframe: %s", df)

    #Save to csv
    df.to_csv(f"./data/{ticker}_indicators.csv")

    return df