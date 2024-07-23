# process_data.py
import sqlite3
import pandas as pd

def load_data():
    conn = sqlite3.connect('currency_performance.db')
    df = pd.read_sql_query("SELECT * FROM currency_data", conn)
    conn.close()
    return df

def calculate_performance(df):
    df = df.drop_duplicates(subset=['date', 'currency'])
    base_year = '2017-12-31'
    base_rates = df[df['date'] == base_year].set_index('currency')['rate']
    performance = pd.DataFrame()

    for date in df['date'].unique():
        if date != base_year:
            date_rates = df[df['date'] == date].set_index('currency')['rate']
            performance[date] = (date_rates / base_rates - 1) * 100

    performance = performance.T
    performance.reset_index(inplace=True)
    performance.rename(columns={'index': 'currency'}, inplace=True)
    return performance

def main():
    df = load_data()
    performance = calculate_performance(df)
    performance.to_csv('currency_performance.csv', index=False)

if __name__ == "__main__":
    main()







