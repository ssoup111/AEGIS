from aegis.scanner import scan_watchlist
from aegis.portfolio import paper_buy, portfolio_value
from aegis.journal import write_trade_journal


def print_report(decisions):
    print("\nPROJECT AEGIS v0.2 - FULL TRADING REPORT")
    print("=" * 52)

    for rank, decision in enumerate(decisions, start=1):
        context = decision.get("market_context", {})
        symbol = decision["symbol"]

        print(f"\n#{rank} {symbol}")
        print("-" * 20)
        print(f"Final Decision: {decision['final_action']}")
        print(f"Opportunity Score: {decision.get('opportunity_score', 0)}")
        print(f"Confidence: {decision.get('confidence', 0)}%")
        print(f"CIO Reason: {decision.get('reason')}")

        if context:
            print(f"Last Close: ${context.get('last_close')}")
            print(f"Price Change: {context.get('price_change_pct')}%")
            print(f"Volume Change: {context.get('volume_change_pct')}%")

        print("Agent Votes:")
        for opinion in decision.get("agent_opinions", []):
            print(
                f"  - {opinion['agent']}: "
                f"{opinion['action']} "
                f"({opinion['confidence']}%) - "
                f"{opinion['reason']}"
            )

        headlines = context.get("headlines", []) if context else []
        if headlines:
            print("Headlines:")
            for headline in headlines[:3]:
                print(f"  - {headline}")


def update_virtual_portfolio(decisions):
    price_lookup = {}

    for decision in decisions:
        context = decision.get("market_context", {})
        last_close = context.get("last_close")
        if last_close:
            price_lookup[decision["symbol"]] = last_close

    executed_trades = []

    for decision in decisions:
        if decision["final_action"] != "BUY":
            continue

        context = decision.get("market_context", {})
        price = context.get("last_close")
        if not price:
            continue

        portfolio, result = paper_buy(
            decision["symbol"],
            price,
            decision.get("reason", ""),
        )
        journal_path = write_trade_journal(decision, result)

        executed_trades.append({
            "symbol": decision["symbol"],
            "result": result,
            "journal_path": journal_path,
        })

    current_value = portfolio_value(price_lookup)
    return executed_trades, current_value


def print_portfolio_report(executed_trades, current_value):
    print("\nVIRTUAL PORTFOLIO ACTIONS")
    print("=" * 28)

    if executed_trades:
        for trade in executed_trades:
            print(trade["result"])
            print(f"Journal: {trade['journal_path']}")
    else:
        print("No BUY decisions executed.")

    print("\nVIRTUAL PORTFOLIO")
    print("=" * 28)
    print(f"Current Value: ${current_value}")


def main():
    decisions = scan_watchlist()

    if not decisions:
        print("No trading decisions were produced.")
        return

    print_report(decisions)

    executed_trades, current_value = update_virtual_portfolio(decisions)
    print_portfolio_report(executed_trades, current_value)


if __name__ == "__main__":
    main()
