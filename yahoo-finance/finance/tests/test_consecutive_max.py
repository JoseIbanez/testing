import pandas as pd
import numpy as np

# 1. Create a dummy DataFrame
np.random.seed(42)
df = pd.DataFrame({
    'value': [10, 12, 5, 18, 22, 25, 30, 21, 5, 12, 16, 16, 16, 16, 16]
})

threshold = 15
window_size = 5

# 2. Identify where values are greater than the threshold
is_above_threshold = df['value'] > threshold

# 3. Use a rolling sum to find 5 consecutive True values
consecutive_count = is_above_threshold.rolling(window=window_size).sum()

# 4. Filter for rows where the rolling sum equals the window size
# (This marks the END row of each 5-row consecutive sequence)
end_indices = df[consecutive_count == window_size].index

print("End indices of the 5 consecutive rows:", end_indices.tolist())
