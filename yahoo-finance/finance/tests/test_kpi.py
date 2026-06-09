import pandas as pd
import numpy as np

def test_vol():
    df = pd.DataFrame({
        'High': [10, 15, 20],
        'Low': [5, 12, 8],
        'Close': [8, 14, 15]
    })
    
    prev_close = df['Close'].shift(1)
    tr1 = df['High'] - df['Low']
    tr2 = (df['High'] - prev_close).abs()
    tr3 = (df['Low'] - prev_close).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    df['Volatility'] = true_range / prev_close * 100
    print(df)

test_vol()
