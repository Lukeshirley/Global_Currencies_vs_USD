# check_currencies.py

import sqlite3
import pandas as pd

def check_currency_data(db_path):
    """
    Check the availability and integrity of currency data in the database.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to check distinct currencies
    query = "SELECT DISTINCT currency FROM currency_performance"
    cursor.execute(query)
    currencies = cursor.fetchall()

    # Convert list of tuples to list of strings
    currency_list = [currency[0] for currency in currencies]
    print(f"Available currencies: {currency_list}")

    # Check for any missing data or anomalies
    query = "SELECT * FROM currency_performance"
    df = pd.read_sql(query, conn)

    # Print summary statistics
    print("\nData Summary:")
    print(df.describe())

    # Check for missing values
    missing_values = df.isnull().sum()
    print("\nMissing Values:")
    print(missing_values)

    conn.close()

def main():
    db_path = 'data/currency_performance.db'
    check_currency_data(db_path)

if __name__ == "__main__":
    main()
