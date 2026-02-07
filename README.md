# MarketPulse – Automated Financial Data Pipeline

MarketPulse is a modular Python system that fetches financial market data, processes and cleans the data using Pandas, stores structured results in SQLite, and generates daily CSV + HTML reports.

## Features
- **Data Ingestion**: Fetches stock market data using `yfinance`.
- **Data Transformation**: Cleans missing values, standardizes timestamps, and calculates:
  - Daily % Change
  - 5-Day Moving Average
  - Volatility (Rolling Std Dev)
- **Database Storage**: Stores processed records in a SQLite database (`data/market_data.db`), avoiding duplicates.
- **Reporting**: Generates:
  - `reports/market_report.csv`: Consolidated data CSV.
  - `reports/market_summary.html`: HTML report with summary statistics and price trend charts.
- **Logging**: detailed execution logs in `logs/pipeline.log`.

## Project Structure
```
MarketPulse/
├── config.py           # Configuration settings
├── data_fetcher.py     # Data fetching logic (yfinance)
├── transformer.py      # Data cleaning and feature engineering
├── database.py         # SQLite database operations
├── reporter.py         # CSV and HTML report generation
├── utils.py            # Logging utility
├── main.py             # Main execution script
├── requirements.txt    # Project dependencies
├── README.md           # Documentation
├── logs/               # Log files
├── reports/            # Generated reports
└── data/               # SQLite database
```

## Setup

1.  **Clone the repository** (if applicable) or navigate to the project folder.

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the pipeline with default tickers (AAPL, GOOGL, MSFT, AMZN, TSLA):
```bash
python main.py
```

Run with specific tickers:
```bash
python main.py --tickers NVDA META AMD
```

## Output

- **Logs**: Check `logs/pipeline.log` for execution details.
- **Database**: Data is stored in `data/market_data.db`.
- **Reports**: Open `reports/market_summary.html` in your browser to view the dashboard.

## Requirements
- Python 3.8+
- pandas, yfinance, matplotlib, jinja2

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Connect with me

If you'd like to connect, feel free to reach out — [Click here](https://minianonlink.vercel.app/tusharbhardwaj)

