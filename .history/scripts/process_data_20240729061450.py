import pandas as pd
import sqlite3
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger()

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
    performance = df_pivot.pct_change().dropna() * 100
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
    performance = df_pivot.pct_change().dropna() * 100
    return performance

def main():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'currency_performance.db')
    
    logger.info("Processing currency data")
    currency_performance = process_currency_data(db_path)
    logger.info("Currency data processing complete")
    
    logger.info("Processing cryptocurrency data")
    crypto_performance = process_crypto_data(db_path)
    logger.info("Cryptocurrency data processing complete")
    
    # Combine currency and cryptocurrency data
    logger.info("Combining currency and cryptocurrency data")
    combined_performance = pd.concat([currency_performance, crypto_performance], axis=1)
    combined_performance.to_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'combined_performance.csv'))
    
    logger.info("Data processing complete, results saved to combined_performance.csv")

if __name__ == "__main__":
    main()





