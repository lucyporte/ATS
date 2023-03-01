import numpy as np
import pandas as pd
import talib

# Load historical price data
df = pd.read_csv('path/to/historical/prices.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Calculate Bollinger Bands
df['MA20'] = talib.SMA(df['Close'], timeperiod=20)
df['std20'] = talib.STDDEV(df['Close'], timeperiod=20)
df['UpperBand'] = df['MA20'] + 2 * df['std20']
df['LowerBand'] = df['MA20'] - 2 * df['std20']

# Calculate Fibonacci retracement levels
high = df['High'].max()
low = df['Low'].min()
diff = high - low
df['fib_23.6'] = high - (diff * 0.236)
df['fib_38.2'] = high - (diff * 0.382)
df['fib_50.0'] = high - (diff * 0.5)
df['fib_61.8'] = high - (diff * 0.618)

# Define trading signals
df['long_entry'] = np.where((df['Close'] < df['LowerBand']) & (df['Close'] > df['fib_50.0']), 1, 0)
df['long_exit'] = np.where(df['Close'] > df['MA20'], 1, 0)
df['short_entry'] = np.where((df['Close'] > df['UpperBand']) & (df['Close'] < df['fib_50.0']), 1, 0)
df['short_exit'] = np.where(df['Close'] < df['MA20'], 1, 0)

# Calculate positions and returns
df['position'] = df['long_entry'] - df['long_exit'] - df['short_entry'] + df['short_exit']
df['strategy_returns'] = df['position'].shift(1) * df['Close'].pct_change()

# Calculate cumulative returns
df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()

# Plot cumulative returns
df['cumulative_returns'].plot()
