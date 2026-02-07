import os

# Create directories if they don't exist
os.makedirs("logs", exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Application Settings
APP_NAME = "MarketPulse"
VERSION = "1.0.0"

# Data Fetching Settings
# 'yfinance' or 'alpha_vantage'
DATA_SOURCE = os.getenv("DATA_SOURCE", "yfinance")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")

# Default tickers to track if not provided via CLI
DEFAULT_TICKERS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]

# Analysis Settings
MOVING_AVERAGE_WINDOW = 5
VOLATILITY_WINDOW = 5

# Database Settings
DB_PATH = os.path.join("data", "market_data.db")

# Reporting Settings
REPORTS_DIR = "reports"
LOGS_DIR = "logs"
LOG_FILE = os.path.join(LOGS_DIR, "pipeline.log")
