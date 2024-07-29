import requests
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()

BASE_URL = 'https://openexchangerates.org/api/historical/'
API_KEY = os.getenv('API_KEY')

def fetch_currency_data(date):
    url = f"{BASE_URL}{date}.json?app_id={API_KEY}&base=USD"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_crypto_data(ticker, date):
    crypto = yf.Ticker(ticker)
    hist = crypto.history(start=date, end=date)
    if not hist.empty:
        return hist['Close'][0]
    return None

def save_data_to_db(data, date, is_crypto=False):
    conn = sqlite3.connect('data/currency_performance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS currency_data (
                        date TEXT,
                        currency TEXT,
                        rate REAL
                    )''')
    if is_crypto:
        for currency, rate in data.items():
            cursor.execute('INSERT INTO currency_data (date, currency, rate) VALUES (?, ?, ?)',
                           (date, currency, rate))
    else:
        for currency, rate in data['rates'].items():
            cursor.execute('INSERT INTO currency_data (date, currency, rate) VALUES (?, ?, ?)',
                           (date, currency, rate))
    conn.commit()
    conn.close()

def main():
    dates = ['2017-12-31', '2018-12-31', '2019-12-31', '2020-12-31', '2021-12-31', '2022-12-31', datetime.now().strftime('%Y-%m-%d')]
    for date in dates:
        currency_data = fetch_currency_data(date.replace('-', ''))
        save_data_to_db(currency_data, date.replace('-', ''))

        crypto_data = {}
        for ticker in ['BTC-USD', 'ETH-USD', 'SOL-USD']:
            price = fetch_crypto_data(ticker, date)
            if price is not None:
                crypto_data[ticker.split('-')[0]] = price
        save_data_to_db(crypto_data, date.replace('-', ''), is_crypto=True)

if __name__ == "__main__":
    main()



