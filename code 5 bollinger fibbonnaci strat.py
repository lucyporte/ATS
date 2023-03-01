import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Download historical data for SPY
ticker = 'SPY'
df = yf.download(ticker, period='1y', interval='1d')

# Calculate the 20-day moving average, standard deviation, upper and lower Bollinger Bands
df['MA20'] = df['Close'].rolling(window=20).mean()
df['stddev'] = df['Close'].rolling(window=20).std()
df['UpperBand'] = df['MA20'] + 2 * df['stddev']
df['LowerBand'] = df['MA20'] - 2 * df['stddev']

# Calculate the Fibonacci retracements levels
high = df['High'].max()
low = df['Low'].min()
diff = high - low
df['38.2'] = high - (diff * 0.382)
df['50'] = high - (diff * 0.5)
df['61.8'] = high - (diff * 0.618)

# Plot the Bollinger Bands and Fibonacci retracements
plt.figure(figsize=(12,6))
plt.plot(df.index, df['Close'], color='blue', label='Close')
plt.plot(df.index, df['MA20'], color='black', label='MA20')
plt.plot(df.index, df['UpperBand'], color='red', label='UpperBand')
plt.plot(df.index, df['LowerBand'], color='green', label='LowerBand')
plt.plot(df.index, df['38.2'], color='orange', label='38.2%')
plt.plot(df.index, df['50'], color='purple', label='50%')
plt.plot(df.index, df['61.8'], color='brown', label='61.8%')
plt.legend()

# Trading strategy based on Bollinger Bands and Fibonacci retracements
df['position'] = np.where(df['Close'] > df['UpperBand'], -1, np.nan)
df['position'] = np.where(df['Close'] < df['LowerBand'], 1, df['position'])
df['position'] = np.where(df['Close'] > df['38.2'], np.nan, df['position'])
df['position'] = np.where(df['Close'] < df['61.8'], np.nan, df['position'])
df['position'] = df['position'].fillna(method='ffill')
df['returns'] = np.log(df['Close'] / df['Close'].shift(1))
df['strategy'] = df['position'].shift(1) * df['returns']
df[['returns', 'strategy']].cumsum().apply(np.exp).plot(figsize=(12,6))

plt.show()
