from aegis.scanner import scan_watchlist
from aegis.portfolio import paper_buy, portfolio_value
from aegis.journal import write_trade_journal

def print_report(decisions):
    print("\nPROJECT AEGIS v0.2 — TOP OPPORTUNITY REPORT")
    print("=" * 52)

    for rank, d in enumerate(decisions[:10], start=1):
        ctx = d.get("market_context", {})
        symbol = d["symbol"]
        action = d["final_action"]
        score = d.get("opportunity_score", 0)
        confidence = d.get("confidence", 0)

        print(f"\n#{rank} {symbol}")
        print("-" * 20)
        print(f"Action: {action}")
        print(f"Opportunity Score: {score}")
        print(f"Confidence: {confidence}%")
        print(f"Reason: {d.get('reason')}")

        if ctx:
            print(f"Last Close: ${ctx.get('last_close')}")
            print(f"Price Change: {ctx.get('price_change_pct')}%")
            print(f"Volume Change: {ctx.get('volume_change_pct')}%")

        print("Agent Votes:")
        for opinion in d.get("agent_opinions", []):
            print(f"  - {opinion['agent']}: {opinion['action']} ({opinion['confidence']}%)")

        headlines = ctx.get("headlines", []) if ctx else []
        if headlines:
            print("Headlines:")
            for headline in headlines[:3]:
                print(f"  - {headline}")

def main():
    decisions = scan_watchlist()
    print_report(decisions)

    price_lookup = {}
    for d in decisions:
        ctx = d.get("market_context", {})
        if ctx.get("last_close"):
            price_lookup[d["symbol"]] = ctx["last_close"]

    best = decisions[0]
    if best["final_action"] == "BUY":
        price = best["market_context"]["last_close"]
        portfolio, result = paper_buy(best["symbol"], price, best["reason"])
        print("\nVIRTUAL PORTFOLIO ACTION")
        print("=" * 28)
        print(result)
        journal_path = write_trade_journal(best, result)
        print(f"Journal: {journal_path}")

    value = portfolio_value(price_lookup)
    print("\nVIRTUAL PORTFOLIO")
    print("=" * 28)
    print(f"Current Value: ${value}")

if __name__ == "__main__":
    main()
