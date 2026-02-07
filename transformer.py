import pandas as pd
from config import MOVING_AVERAGE_WINDOW, VOLATILITY_WINDOW
from utils import setup_logger

logger = setup_logger("Transformer")

def transform_data(df):
    """
    Cleans and processes raw stock data.
    Args:
        df (pd.DataFrame): Raw data from fetcher.
    Returns:
        pd.DataFrame: Processed DataFrame ready for DB and Reporting.
    """
    if df.empty:
        logger.warning("Empty DataFrame received for transformation.")
        return df

    try:
        # Sort by date just in case
        df = df.sort_values(by="Date")

        # Clean missing values
        # Forward fill first, then drop any remaining NaNs (e.g. at the start)
        df = df.ffill().dropna()

        # Calculate calculated metrics
        # Daily % Change
        df['Daily_Return'] = df['Close'].pct_change() * 100

        # 5-day Moving Average
        df['MA_5'] = df['Close'].rolling(window=MOVING_AVERAGE_WINDOW).mean()

        # Volatility (Rolling Std Dev)
        df['Volatility'] = df['Close'].rolling(window=VOLATILITY_WINDOW).std()

        # Drop rows with NaN created by rolling windows/pct_change
        df = df.dropna()

        # Standardize timestamps (ensure Date is string in ISO format YYYY-MM-DD for SQLite)
        if pd.api.types.is_datetime64_any_dtype(df['Date']):
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

        # Select and reorder columns to match Database expectation
        # Expected: Ticker, Date, Open, High, Low, Close, Volume, Daily_Return, MA_5, Volatility
        expected_cols = [
            'Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 
            'Daily_Return', 'MA_5', 'Volatility'
        ]
        
        # Ensure all columns exist
        for col in expected_cols:
            if col not in df.columns:
                logger.error(f"Missing column {col} in transformed data.")
                return pd.DataFrame() # Return empty on error/missing

        df = df[expected_cols]

        logger.info(f"Transformed data successfully. Shape: {df.shape}")
        return df

    except Exception as e:
        logger.error(f"Error transforming data: {e}")
        return pd.DataFrame()
