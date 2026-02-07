import sqlite3
import pandas as pd
from config import DB_PATH
from utils import setup_logger

logger = setup_logger("Database")

def get_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return None

def init_db():
    """Initializes the database table if it doesn't exist."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock_prices (
                    ticker TEXT,
                    date TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    daily_return REAL,
                    moving_avg_5d REAL,
                    volatility_5d REAL,
                    PRIMARY KEY (ticker, date)
                )
            """)
            conn.commit()
            logger.info("Database initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")
        finally:
            conn.close()

def save_data(df):
    """
    Saves the processed DataFrame to the database.
    Avoids duplicate entries using INSERT OR IGNORE logic via pandas.
    """
    if df.empty:
        logger.warning("No data to save.")
        return

    conn = get_connection()
    if conn:
        try:
            # We will iterate and insert to avoid replacements or simple appends that might fail or duplicate.
            # Alternatively, we can use to_sql with 'append' and rely on a unique constraint,
            # but pandas to_sql doesn't support 'INSERT OR IGNORE' natively with sqlite easily without a workaround.
            # A simple workaround: Load data to a temporary table and then INSERT OR IGNORE to the main table.

            # Create a list of tuples from the dataframe
            # Columns must match the table structure
            # Ensure the dataframe columns are in the right order for the table or use executemany with named params?
            # It's safer to use raw SQL for INSERT OR IGNORE.
            
            records = df.to_dict('records')
            cursor = conn.cursor()
            
            # Prepare the query
            query = """
                INSERT OR IGNORE INTO stock_prices (
                    ticker, date, open, high, low, close, volume, 
                    daily_return, moving_avg_5d, volatility_5d
                ) VALUES (
                    :Ticker, :Date, :Open, :High, :Low, :Close, :Volume, 
                    :Daily_Return, :MA_5, :Volatility
                )
            """
            
            # Map DataFrame columns to bind parameters if needed, or just rename DF columns to match.
            # Let's assume the transformer returns columns:
            # 'Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Daily_Return', 'MA_5', 'Volatility'
            
            cursor.executemany(query, records)
            conn.commit()
            logger.info(f"Saved {cursor.rowcount} records to database.")
            
        except sqlite3.Error as e:
            logger.error(f"Error saving data to database: {e}")
        finally:
            conn.close()
