import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_crypto_data(tickers, start_date):
    data = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start_date)
        data[ticker] = df['Adj Close']
    return pd.DataFrame(data)

def calculate_performance(df, baseline_date):
    baseline = df.loc[baseline_date]
    performance = (df / baseline - 1) * 100
    return performance

def main():
    # Define the cryptocurrencies to fetch
    crypto_tickers = ['BTC-USD', 'ETH-USD', 'SOL-USD']
    start_date = '2017-12-31'
    baseline_date = '2017-12-31'
    
    # Fetch cryptocurrency data
    crypto_data = fetch_crypto_data(crypto_tickers, start_date)
    
    # Calculate performance
    crypto_performance = calculate_performance(crypto_data, baseline_date)
    
    # Load existing currency performance data
    currency_performance = pd.read_csv('data/currency_performance.csv', index_col='Date', parse_dates=True)
    
    # Merge with cryptocurrency performance data
    combined_performance = currency_performance.join(crypto_performance, how='outer')
    
    # Save combined data
    combined_performance.to_csv('data/combined_currency_performance.csv')
    
    print("Crypto data successfully added and saved to combined_currency_performance.csv")

if __name__ == "__main__":
    main()
