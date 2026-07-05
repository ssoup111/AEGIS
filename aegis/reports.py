from datetime import datetime
from pathlib import Path

from aegis.portfolio import load_portfolio, portfolio_value
from aegis.scanner import scan_watchlist


REPORT_PATH = Path("reports/latest_report.txt")


def money(value):
    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return "$0.00"


def pct(value):
    if value is None:
        return "N/A"
    try:
        return f"{float(value):+.2f}%"
    except (TypeError, ValueError):
        return "N/A"


def build_price_lookup(decisions):
    price_lookup = {}
    for decision in decisions:
        context = decision.get("market_context", {})
        last_close = context.get("last_close")
        if last_close:
            price_lookup[decision["symbol"]] = last_close
    return price_lookup


def system_health(decisions):
    if not decisions:
        return "NO SCAN RESULTS"
    if any(decision.get("final_action") == "ERROR" for decision in decisions):
        return "DEGRADED"
    return "ONLINE"


def summarize_actions(decisions):
    counts = {"BUY": 0, "HOLD": 0, "REJECT": 0, "ERROR": 0}
    for decision in decisions:
        action = decision.get("final_action", "ERROR")
        counts[action] = counts.get(action, 0) + 1
    return counts


def render_agent_votes(decision):
    opinions = decision.get("agent_opinions", [])
    if not opinions:
        return ["    Agent votes: none recorded"]

    lines = ["    Agent votes:"]
    for opinion in opinions:
        lines.append(
            "    - "
            f"{opinion.get('agent', 'Unknown Agent')}: "
            f"{opinion.get('action', 'N/A')} "
            f"({opinion.get('confidence', 0)}%) - "
            f"{opinion.get('reason', 'No reason provided')}"
        )
    return lines


def research_director_notes(decisions, portfolio, current_value):
    health = system_health(decisions)
    buy_count = sum(1 for d in decisions if d.get("final_action") == "BUY")
    error_count = sum(1 for d in decisions if d.get("final_action") == "ERROR")
    scored = [d for d in decisions if d.get("final_action") != "ERROR"]
    top_symbol = decisions[0]["symbol"] if decisions else "N/A"
    cash = portfolio.get("cash", 0)

    learned = [
        f"The scan produced {len(decisions)} watchlist decisions with {buy_count} BUY candidates.",
        f"The highest-ranked symbol was {top_symbol}.",
        f"The virtual portfolio is valued at {money(current_value)} with {money(cash)} cash available.",
    ]

    if scored:
        learned[1] = (
            f"The strongest scored opportunity was {top_symbol} "
            f"with an opportunity score of {decisions[0].get('opportunity_score', 0)}."
        )

    risks = [
        "Paper-trading results are not live execution results and should not be treated as brokerage performance.",
        "Market data or dependency failures can reduce decision quality.",
    ]
    if error_count:
        risks[1] = f"{error_count} symbols returned scan errors, so system health is {health}."

    experiment = (
        "Compare tomorrow's top-ranked symbols against today's report and flag any repeated BUY signals."
    )

    return learned, risks, experiment


def render_report(decisions, portfolio, current_value, generated_at):
    counts = summarize_actions(decisions)
    health = system_health(decisions)
    learned, risks, experiment = research_director_notes(decisions, portfolio, current_value)

    lines = [
        "AEGIS PAPER-TRADING EMAIL REPORT",
        "=" * 34,
        f"Generated: {generated_at}",
        "",
        "EXECUTIVE SUMMARY",
        "-" * 17,
        f"System health: {health}",
        f"Watchlist decisions: {len(decisions)}",
        f"BUY: {counts.get('BUY', 0)} | HOLD: {counts.get('HOLD', 0)} | "
        f"REJECT: {counts.get('REJECT', 0)} | ERROR: {counts.get('ERROR', 0)}",
        "Mode: Paper trading only. No emails sent. No Gmail connection. No real trades placed.",
        "",
        "VIRTUAL PORTFOLIO",
        "-" * 17,
        f"Portfolio value: {money(current_value)}",
        f"Cash available: {money(portfolio.get('cash', 0))}",
        f"Open positions: {len(portfolio.get('positions', {}))}",
        f"Recorded paper trades: {len(portfolio.get('trades', []))}",
        "",
        "TOP 10 OPPORTUNITIES",
        "-" * 20,
    ]

    if not decisions:
        lines.append("No opportunities were produced by the scanner.")
    else:
        for rank, decision in enumerate(decisions[:10], start=1):
            context = decision.get("market_context", {})
            lines.extend([
                "",
                f"{rank}. {decision.get('symbol', 'N/A')}",
                f"   Action: {decision.get('final_action', 'N/A')}",
                f"   Score: {decision.get('opportunity_score', 0)}",
                f"   Confidence: {decision.get('confidence', 0)}%",
                f"   Last close: {money(context.get('last_close')) if context.get('last_close') else 'N/A'}",
                f"   Price change: {pct(context.get('price_change_pct'))}",
                f"   Volume change: {pct(context.get('volume_change_pct'))}",
                f"   Reason: {decision.get('reason', 'No reason provided')}",
            ])
            lines.extend(render_agent_votes(decision))

    lines.extend([
        "",
        "RESEARCH DIRECTOR",
        "-" * 17,
        "Three things learned:",
    ])
    lines.extend(f"- {item}" for item in learned)
    lines.append("")
    lines.append("Two mistakes or risks:")
    lines.extend(f"- {item}" for item in risks)
    lines.append("")
    lines.append("One experiment for tomorrow:")
    lines.append(f"- {experiment}")
    lines.append("")
    lines.append("SYSTEM HEALTH")
    lines.append("-" * 13)
    lines.append(f"Status: {health}")
    lines.append(f"Last scan time: {generated_at}")

    return "\n".join(lines) + "\n"


def generate_latest_report():
    generated_at = datetime.now().isoformat(timespec="seconds")
    decisions = scan_watchlist()
    portfolio = load_portfolio()
    current_value = portfolio_value(build_price_lookup(decisions))
    report = render_report(decisions, portfolio, current_value, generated_at)

    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(report)
    return REPORT_PATH


def main():
    path = generate_latest_report()
    print(f"AEGIS paper-trading report created: {path}")


if __name__ == "__main__":
    main()
