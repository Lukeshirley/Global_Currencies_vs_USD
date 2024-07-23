# fetch_data.py 
import requests
import sqlite3
from datetime import datetime
import config

BASE_URL = 'https://openexchangerates.org/api/historical/'

def fetch_currency_data(date):
    url = f"{BASE_URL}{date}.json?app_id={config.API_KEY}&base=USD"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_data_to_db(data, date):
    conn = sqlite3.connect('currency_performance.db')
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

def main():
    dates = ['2017-12-31', '2018-12-31', '2019-12-31', '2020-12-31', '2021-12-31', '2022-12-31', '2023-12-31', datetime.now().strftime('%Y-%m-%d')]
    for date in dates:
        data = fetch_currency_data(date)
        save_data_to_db(data, date)

if __name__ == "__main__":
    main()


