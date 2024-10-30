# -*- coding: utf-8 -*-
"""Script

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Oe1p381fx53IFMULgqMLN234hrYEx9pN
"""

import yfinance as yf
import pandas as pd

# Define the date range
start_date = "2023-01-01"
end_date = "2024-09-30"

# Download EUR/INR currency data from Yahoo Finance
data = yf.download("EURINR=X", start=start_date, end=end_date)

# Display the first few rows of the data
print(data.head())

# Save the data to a CSV file
data.to_csv('EUR_INR_data.csv')

pip install yfinance

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

start_date = "2023-01-01"
end_date = "2024-09-30"

data = yf.download("EURINR=X", start=start_date, end=end_date)
data['MA20'] = data['Close'].rolling(window=20).mean()
data['STD20'] = data['Close'].rolling(window=20).std()
data['Bollinger_Upper'] = data['MA20'] + (data['STD20'] * 2)
data['Bollinger_Lower'] = data['MA20'] - (data['STD20'] * 2)

typical_price = (data['High'] + data['Low'] + data['Close']) / 3
moving_avg = typical_price.rolling(window=20).mean()
mean_dev = typical_price.rolling(window=20).apply(lambda x: (abs(x - x.mean())).mean())
data['CCI'] = (typical_price - moving_avg) / (0.015 * mean_dev)

latest_data = data.loc['2024-09-26']

one_day_data = data.loc['2024-09-27']
one_day_indicators = {
    'MA20': one_day_data['MA20'].iloc[0],
    'Bollinger_Upper': one_day_data['Bollinger_Upper'].iloc[0],
    'Bollinger_Lower': one_day_data['Bollinger_Lower'].iloc[0],
    'CCI': one_day_data['CCI'].iloc[0]
}

one_week_data = data.loc['2024-09-27']
one_week_indicators = {
    'MA20': one_week_data['MA20'].iloc[0],
    'Bollinger_Upper': one_week_data['Bollinger_Upper'].iloc[0],
    'Bollinger_Lower': one_week_data['Bollinger_Lower'].iloc[0],
    'CCI': one_week_data['CCI'].iloc[0]
}

print("Indicators for 1-day (October 1, 2024):")
print(one_day_indicators)

print("\nIndicators for 1-week (October 7, 2024):")
print(one_week_indicators)

def decision_based_on_indicators(latest_data, indicators):
    decision = {}
    latest_close = latest_data['Close'].iloc[0]
    decision['MA20'] = 'BUY' if latest_close > indicators['MA20'] else 'SELL' if latest_close < indicators['MA20'] else 'NEUTRAL'
    decision['Bollinger'] = 'SELL' if latest_close > indicators['Bollinger_Upper'] else 'BUY' if latest_close < indicators['Bollinger_Lower'] else 'NEUTRAL'
    decision['CCI'] = 'BUY' if indicators['CCI'] < -100 else 'SELL' if indicators['CCI'] > 100 else 'NEUTRAL'
    return decision

one_day_decision = decision_based_on_indicators(latest_data, one_day_indicators)
one_week_decision = decision_based_on_indicators(latest_data, one_week_indicators)

print("\nDecision for 1-day (October 1, 2024):")
print(one_day_decision)

print("\nDecision for 1-week (October 7, 2024):")
print(one_week_decision)

plt.figure(figsize=(14, 10))

plt.subplot(2, 1, 1)
plt.plot(data['Close'], label='EUR/INR Close', color='blue', linewidth=1.5)
plt.plot(data['MA20'], label='20-Day MA', color='orange', linewidth=1.5)
plt.fill_between(data.index, data['Bollinger_Upper'], data['Bollinger_Lower'], color='lightgray', label='Bollinger Bands')
plt.title('EUR/INR Price Chart with Technical Indicators')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(data['CCI'], label='CCI', color='green', linewidth=1.5)
plt.axhline(100, color='red', linestyle='--', linewidth=1)
plt.axhline(-100, color='red', linestyle='--', linewidth=1)
plt.title('Commodity Channel Index (CCI)')
plt.xlabel('Date')
plt.ylabel('CCI')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()