import yfinance as yf

def get_market_context(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="10d")

    if hist.empty or len(hist) < 2:
        raise ValueError(f"No market data found for {symbol}")

    last_close = float(hist["Close"].iloc[-1])
    previous_close = float(hist["Close"].iloc[-2])
    last_volume = float(hist["Volume"].iloc[-1])
    avg_volume = float(hist["Volume"].tail(10).mean())

    price_change_pct = ((last_close - previous_close) / previous_close) * 100
    volume_change_pct = ((last_volume - avg_volume) / avg_volume) * 100 if avg_volume else 0

    headlines = []
    try:
        news = ticker.news or []
        for item in news[:5]:
            title = item.get("title")
            if title:
                headlines.append(title)
    except Exception:
        pass

    return {
        "symbol": symbol,
        "last_close": round(last_close, 2),
        "previous_close": round(previous_close, 2),
        "price_change_pct": round(price_change_pct, 2),
        "volume_change_pct": round(volume_change_pct, 2),
        "headlines": headlines,
        "headline_count": len(headlines),
        "public_disclosure_signal": "none",
        "open_positions": 0,
        "daily_loss": 0,
    }
