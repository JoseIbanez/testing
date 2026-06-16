import pandas as pd

# 1. Sample DataFrame with a datetime index
df = pd.DataFrame(
    index=pd.to_datetime(
        ["2026-06-01", "2026-06-02", "2026-06-05", "2026-06-06"]
    ),
    data={"value": [10, 20, 15, 30]},
)

# 2. Add a column with the previous row's datetime
# (We grab the index values and shift them down by 1)
df["previous_datetime"] = pd.Series(df.index, index=df.index).shift(1)

# 3. Calculate the difference
df["datetime_difference"] = df.index - df["previous_datetime"]

print(df)