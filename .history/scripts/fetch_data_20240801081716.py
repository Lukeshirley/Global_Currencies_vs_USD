import requests
import sqlite3
from datetime import datetime
import config
import yfinance as yf
import pandas as pd

BASE_URL = 'https://openexchangerates.org/api/historical/'

def fetch_currency_data(date):
    url = f"{BASE_URL}{date}.json?app_id={config.API_KEY}&base=USD"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_data_to_db(data, date):
    conn = sqlite3.connect('data/currency_performance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS currency_data (
                        date TEXT,
                        currency TEXT,
                        rate REAL
                    )''')
    for currency, rate in data['rates'].items():
        cursor.execute('INSERT INTO currency_data (date, currency, rate) VALUES (?, ?, ?)',
                       (date, currency, rate))
    conn.commit()
    conn.close()

def fetch_crypto_data(tickers, start_date):
    data = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start_date)
        data[ticker] = df['Adj Close']
    return pd.DataFrame(data)

def combine_data(dates, crypto_tickers, start_date):
    conn = sqlite3.connect('data/currency_performance.db')
    df_list = []
    for date in dates:
        query = f"SELECT date, currency, rate FROM currency_data WHERE date='{date}'"
        df = pd.read_sql(query, conn)
        df_list.append(df)
    conn.close()

    currency_data = pd.concat(df_list).drop_duplicates(subset=['date', 'currency'])

    # Pivot the DataFrame to have dates as rows and currencies as columns
    currency_data_pivoted = currency_data.pivot(index='date', columns='currency', values='rate')

    # Fetch cryptocurrency data
    crypto_data = fetch_crypto_data(crypto_tickers, start_date)
    
    # Combine data
    combined_data = currency_data_pivoted.join(crypto_data, how='outer')
    
    # Calculate performance relative to the baseline date
    baseline_date = '2017-12-31'
    baseline = combined_data.loc[baseline_date]
    performance = (combined_data / baseline - 1) * 100
    
    # Save combined data
    performance.to_csv('data/combined_currency_performance.csv')

def main():
    dates = ['2017-12-31', '2018-12-31', '2019-12-31', '2020-12-31', '2021-12-31', '2022-12-31', datetime.now().strftime('%Y-%m-%d')]
    
    # Fetch and save currency data
    for date in dates:
        data = fetch_currency_data(date)
        save_data_to_db(data, date)
    
    # Define cryptocurrency tickers and start date
    crypto_tickers = ['BTC-USD', 'ETH-USD', 'SOL-USD']
    start_date = '2017-12-31'
    
    # Combine currency and cryptocurrency data
    combine_data(dates, crypto_tickers, start_date)

if __name__ == "__main__":
    main()




