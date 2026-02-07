import yfinance as yf
import pandas as pd
from utils import setup_logger

logger = setup_logger("DataFetcher")

def fetch_data(ticker, period="1mo"):
    """
    Fetches historical stock data for a given ticker.
    Args:
        ticker (str): Stock symbol (e.g., AAPL).
        period (str): Data period to download (default: '1mo').
    Returns:
        pd.DataFrame: DataFrame with stock data, or empty DataFrame on failure.
    """
    logger.info(f"Fetching data for {ticker}...")
    try:
        # yfinance download
        # auto_adjust=True accounts for splits/dividends in the Close price, usually better for analysis
        df = yf.download(ticker, period=period, interval="1d", progress=False, auto_adjust=True)
        
        if df.empty:
            logger.warning(f"No data found for {ticker}.")
            return pd.DataFrame()

        # Reset index to make Date a column
        df = df.reset_index()
        
        # Ensure column names are standard (yfinance capitalizes them: Date, Open, High, Low, Close, Volume)
        # We'll add the Ticker column
        df['Ticker'] = ticker
        
        logger.info(f"Successfully fetched {len(df)} rows for {ticker}.")
        return df

    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()
