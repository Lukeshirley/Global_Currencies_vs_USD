import pandas as pd
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_currency_data(db_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM currency_data"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df['date'] = pd.to_datetime(df['date'])
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['date', 'currency'])
    
    df_pivot = df.pivot(index='date', columns='currency', values='rate')
    
    logger.info("Calculating percentage change for currencies")
    performance = df_pivot.pct_change(fill_method=None).dropna() * 100
    return performance

def process_crypto_data(db_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM crypto_data"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df['date'] = pd.to_datetime(df['date'])
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['date', 'crypto'])
    
    df_pivot = df.pivot(index='date', columns='crypto', values='rate')
    
    logger.info("Calculating percentage change for cryptocurrencies")
    performance = df_pivot.pct_change(fill_method=None).dropna() * 100
    return performance

def save_data_to_csv(data, filename):
    data.to_csv(filename)
    logger.info(f"Data saved to {filename}")

def main():
    db_path = 'data/currency_performance.db'
    
    logger.info("Processing currency data")
    currency_performance = process_currency_data(db_path)
    
    logger.info("Processing cryptocurrency data")
    crypto_performance = process_crypto_data(db_path)
    
    logger.info("Combining currency and cryptocurrency data")
    combined_performance = pd.concat([currency_performance, crypto_performance], axis=1)
    
    save_data_to_csv(combined_performance, 'data/combined_performance.csv')
    logger.info("Data processing complete")

if __name__ == "__main__":
    main()






