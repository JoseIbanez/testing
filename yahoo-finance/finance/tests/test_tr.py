import pandas as pd

df = pd.DataFrame({
    'High': [10, 12, 11],
    'Low': [8, 9, 8],
    'Close': [9, 11, 10]
})

prev_close = df['Close'].shift(1)
tr1 = df['High'] - df['Low']
tr2 = (df['High'] - prev_close).abs()
tr3 = (df['Low'] - prev_close).abs()
true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
df['Volatility'] = true_range / df['Close'] * 100

print(df)
