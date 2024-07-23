# check_currencies.py
import pandas as pd

def check_available_currencies():
    df = pd.read_csv('currency_performance.csv')
    print(df.columns)

if __name__ == "__main__":
    check_available_currencies()

