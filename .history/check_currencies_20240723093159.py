# check_currencies.py

import sqlite3

def check_database_schema(db_path):
    """
    Print the schema of the database to identify table names and structure.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get the database schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in the database:")
    for table in tables:
        print(table[0])
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print(f"Columns in {table[0]}:")
        for column in columns:
            print(column)
        print("\n")

    conn.close()

def main():
    db_path = 'data/currency_performance.db'
    check_database_schema(db_path)

if __name__ == "__main__":
    main()

