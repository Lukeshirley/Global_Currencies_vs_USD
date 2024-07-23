# check_currencies.py
import pandas as pd

def check_available_currencies():
    df = pd.read_csv('currency_performance.csv')
    available_currencies = df.columns.tolist()
    print("Available currencies:", available_currencies)

if __name__ == "__main__":
    check_available_currencies()


