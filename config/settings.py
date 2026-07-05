import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_PAPER = os.getenv("ALPACA_PAPER", "true").lower() == "true"

MAX_ACCOUNT_SIZE = float(os.getenv("MAX_ACCOUNT_SIZE", "100"))
MAX_TRADE_SIZE = float(os.getenv("MAX_TRADE_SIZE", "15"))
MAX_OPEN_POSITIONS = int(os.getenv("MAX_OPEN_POSITIONS", "3"))
MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", "10"))

WATCHLIST = [
    "AAPL", "MSFT", "NVDA", "AMD", "TSLA",
    "AMZN", "META", "GOOGL", "PLTR", "SOFI"
]
