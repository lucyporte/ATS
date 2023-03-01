import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib

# Load historical price data
df = pd.read_csv('price_data.csv')
df = df.set_index('date')

# Calculate Bollinger Bands
df['SMA'] = talib.SMA(df['close'], timeperiod=20)
df['STD'] = talib.STDDEV(df['close'], timeperiod=20)
df['upper_band'] = df['SMA'] + 2 * df['STD']
df['lower_band'] = df['SMA'] - 2 * df['STD']

# Calculate Fibonacci retracements
last_high = df['high'].rolling(window=21).max().shift(1)
last_low = df['low'].rolling(window=21).min().shift(1)
df['fib_0'] = last_high - (0.236 * (last_high - last_low))
df['fib_382'] = last_high - (0.382 * (last_high - last_low))
df['fib_618'] = last_high - (0.618 * (last_high - last_low))

# Define trading signals
df['long_entry'] = (df['close'] < df['lower_band']) & (df['close'] > df['fib_618'])
df['short_entry'] = (df['close'] > df['upper_band']) & (df['close'] < df['fib_382'])

# Calculate positions
df['position'] = np.nan
df.loc[df['long_entry'], 'position'] = 1
df.loc[df['short_entry'], 'position'] = -1
df['position'] = df['position'].ffill()

# Calculate returns
df['returns'] = df['close'].pct_change() * df['position'].shift(1)

# Plot the results
df[['close', 'SMA', 'upper_band', 'lower_band', 'fib_0', 'fib_382', 'fib_618']].plot(figsize=(10, 6))
plt.legend()
plt.show()
