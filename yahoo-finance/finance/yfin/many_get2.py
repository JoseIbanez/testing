import yfinance as yf
import pandas as pd


# Download any collection
df = yf.download(list(fse_prime_standard['Ticker'].values), period="1y", interval="1d")

# Swap axis if you prefer df['Ticker']['Value'] over df['Value']['Ticker']
df = df.swaplevel(axis=1)
print(df)

