import pandas as pd
import numpy as np
import talib

# Load price data into pandas DataFrame
df = pd.read_csv('price_data.csv')

# Calculate Bollinger Bands
period = 20
df['MA'] = talib.SMA(df['Close'], period)
df['stddev'] = talib.STDDEV(df['Close'], period)
df['UpperBand'] = df['MA'] + 2 * df['stddev']
df['LowerBand'] = df['MA'] - 2 * df['stddev']

# Calculate Fibonacci retracements
high = df['High'].max()
low = df['Low'].min()
diff = high - low
df['38.2'] = high - (diff * 0.382)
df['50.0'] = high - (diff * 0.5)
df['61.8'] = high - (diff * 0.618)

# Create a new column called "Signal"
df['Signal'] = np.nan

# Populate the "Signal" column based on the trading strategy
for i in range(period, len(df)):
    if df['Close'][i] > df['UpperBand'][i]:
        if df['Close'][i-1] < df['UpperBand'][i-1]:
            if df['Close'][i] > df['38.2'][i]:
                df['Signal'][i] = 1
            else:
                df['Signal'][i] = 0
    elif df['Close'][i] < df['LowerBand'][i]:
        if df['Close'][i-1] > df['LowerBand'][i-1]:
            if df['Close'][i] < df['61.8'][i]:
                df['Signal'][i] = -1
            else:
                df['Signal'][i] = 0

# Backtest the strategy
df['Returns'] = np.log(df['Close'] / df['Close'].shift(1))
df['Strategy'] = df['Signal'].shift(1) * df['Returns']
df['Cumulative Returns'] = df['Strategy'].cumsum()

# Plot the results
import matplotlib.pyplot as plt
plt.plot(df['Cumulative Returns'])
plt.show()
