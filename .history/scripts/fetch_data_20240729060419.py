import requests
import sqlite3
import yfinance as yf
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

BASE_URL = 'https://openexchangerates.org/api/historical/'

def fetch_currency_data(date):
    url = f"{BASE_URL}{date}.json?app_id={API_KEY}&base=USD"
    print(f"Requesting URL: {url}")  # Debugging: Print the request URL
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_data_to_db(data, date):
    conn = sqlite3.connect('../data/currency_performance.db')
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

def fetch_crypto_data(crypto, date):
    data = yf.download(crypto, start=date, end=date)
    if not data.empty:
        return data['Adj Close'][0]
    return None

def save_crypto_data_to_db(crypto_data, date):
    conn = sqlite3.connect('../data/currency_performance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS crypto_data (
                        date TEXT,
                        crypto TEXT,
                        rate REAL
                    )''')
    for crypto, rate in crypto_data.items():
        cursor.execute('INSERT INTO crypto_data (date, crypto, rate) VALUES (?, ?, ?)',
                       (date, crypto, rate))
    conn.commit()
    conn.close()

def main():
    dates = ['2017-12-31', '2018-12-31', '2019-12-31', '2020-12-31', '2021-12-31', '2022-12-31', datetime.now().strftime('%Y-%m-%d')]
    
    for date in dates:
        currency_data = fetch_currency_data(date.replace('-', ''))
        save_data_to_db(currency_data, date)
        
        crypto_data = {}
        for crypto in ['BTC-USD', 'ETH-USD', 'SOL-USD']:
            rate = fetch_crypto_data(crypto, date)
            if rate:
                crypto_data[crypto] = rate
        save_crypto_data_to_db(crypto_data, date)

if __name__ == "__main__":
    main()



