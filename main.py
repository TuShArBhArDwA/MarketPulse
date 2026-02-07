import argparse
import sys
import pandas as pd
from config import DEFAULT_TICKERS, APP_NAME, VERSION
from utils import setup_logger
from database import init_db, save_data
from data_fetcher import fetch_data
from transformer import transform_data
from reporter import generate_csv_report, generate_html_report

logger = setup_logger("Main")

def main():
    logger.info(f"Starting {APP_NAME} v{VERSION}")

    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="MarketPulse - Automated Financial Data Pipeline")
    parser.add_argument("--tickers", nargs="+", help="List of stock tickers to process (e.g., AAPL GOOGL)", default=DEFAULT_TICKERS)
    args = parser.parse_args()

    tickers = args.tickers
    logger.info(f"Processing tickers: {tickers}")

    # Initialize Database
    init_db()

    all_data = []

    for ticker in tickers:
        try:
            # 1. Fetch Data
            raw_df = fetch_data(ticker)
            if raw_df.empty:
                logger.warning(f"Skipping {ticker} due to fetch failure.")
                continue

            # 2. Transform Data
            clean_df = transform_data(raw_df)
            if clean_df.empty:
                logger.warning(f"Skipping {ticker} due to transformation failure.")
                continue

            # 3. Save to Database
            save_data(clean_df)

            # Collect for reporting
            all_data.append(clean_df)

        except Exception as e:
            logger.error(f"Unexpected error processing {ticker}: {e}")

    if all_data:
        # Concatenate all data for reporting
        final_df = pd.concat(all_data, ignore_index=True)
        
        # 4. Generate Reports
        generate_csv_report(final_df)
        generate_html_report(final_df)
        
        logger.info("Pipeline completed successfully.")
    else:
        logger.warning("Pipeline completed but no data was processed.")

if __name__ == "__main__":
    main()
