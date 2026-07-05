import json
from pathlib import Path
from datetime import datetime

PORTFOLIO_PATH = Path("data/virtual_portfolio.json")

STARTING_CASH = 100.00
TRADE_SIZE = 10.00

def load_portfolio():
    PORTFOLIO_PATH.parent.mkdir(exist_ok=True)

    if not PORTFOLIO_PATH.exists():
        portfolio = {
            "starting_cash": STARTING_CASH,
            "cash": STARTING_CASH,
            "positions": {},
            "trades": [],
            "created_at": datetime.now().isoformat()
        }
        save_portfolio(portfolio)
        return portfolio

    return json.loads(PORTFOLIO_PATH.read_text())

def save_portfolio(portfolio):
    PORTFOLIO_PATH.write_text(json.dumps(portfolio, indent=2))

def paper_buy(symbol, price, reason):
    portfolio = load_portfolio()

    if portfolio["cash"] < TRADE_SIZE:
        return portfolio, "SKIPPED: not enough virtual cash"

    shares = round(TRADE_SIZE / price, 6)

    portfolio["cash"] = round(portfolio["cash"] - TRADE_SIZE, 2)
    portfolio["positions"][symbol] = portfolio["positions"].get(symbol, 0) + shares
    portfolio["trades"].append({
        "timestamp": datetime.now().isoformat(),
        "type": "PAPER_BUY",
        "symbol": symbol,
        "price": price,
        "dollars": TRADE_SIZE,
        "shares": shares,
        "reason": reason
    })

    save_portfolio(portfolio)
    return portfolio, f"PAPER BUY: ${TRADE_SIZE} of {symbol}"

def portfolio_value(price_lookup):
    portfolio = load_portfolio()
    value = portfolio["cash"]

    for symbol, shares in portfolio["positions"].items():
        value += shares * price_lookup.get(symbol, 0)

    return round(value, 2)
