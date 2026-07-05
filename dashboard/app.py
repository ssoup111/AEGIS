import html
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from aegis.portfolio import load_portfolio, portfolio_value
from aegis.scanner import scan_watchlist


OUTPUT_PATH = PROJECT_ROOT / "dashboard" / "mission_control.html"


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


def text(value, fallback="N/A"):
    if value is None or value == "":
        return fallback
    return html.escape(str(value))


def action_class(action):
    return {
        "BUY": "buy",
        "HOLD": "hold",
        "REJECT": "reject",
        "ERROR": "error",
    }.get(action, "neutral")


def build_price_lookup(decisions):
    price_lookup = {}
    for decision in decisions:
        context = decision.get("market_context", {})
        last_close = context.get("last_close")
        if last_close:
            price_lookup[decision["symbol"]] = last_close
    return price_lookup


def render_agent_votes(decision):
    opinions = decision.get("agent_opinions", [])
    if not opinions:
        return '<p class="muted">No agent votes recorded.</p>'

    rows = []
    for opinion in opinions:
        action = opinion.get("action", "N/A")
        rows.append(
            f"""
            <tr>
                <td>{text(opinion.get("agent"))}</td>
                <td><span class="pill {action_class(action)}">{text(action)}</span></td>
                <td>{text(opinion.get("confidence"), "0")}%</td>
                <td>{text(opinion.get("reason"))}</td>
            </tr>
            """
        )

    return f"""
    <table class="votes">
        <thead>
            <tr>
                <th>Agent</th>
                <th>Vote</th>
                <th>Confidence</th>
                <th>Reason</th>
            </tr>
        </thead>
        <tbody>{''.join(rows)}</tbody>
    </table>
    """


def render_opportunity_card(rank, decision):
    context = decision.get("market_context", {})
    action = decision.get("final_action", "N/A")
    symbol = decision.get("symbol", "N/A")
    score = decision.get("opportunity_score", 0)
    confidence = decision.get("confidence", 0)

    return f"""
    <article class="opportunity">
        <header class="opportunity-header">
            <div>
                <span class="rank">#{rank}</span>
                <h2>{text(symbol)}</h2>
            </div>
            <span class="pill {action_class(action)}">{text(action)}</span>
        </header>

        <div class="metrics">
            <div>
                <span>Score</span>
                <strong>{text(score, "0")}</strong>
            </div>
            <div>
                <span>Confidence</span>
                <strong>{text(confidence, "0")}%</strong>
            </div>
            <div>
                <span>Last Close</span>
                <strong>{money(context.get("last_close")) if context.get("last_close") else "N/A"}</strong>
            </div>
            <div>
                <span>Price Change</span>
                <strong>{pct(context.get("price_change_pct"))}</strong>
            </div>
            <div>
                <span>Volume Change</span>
                <strong>{pct(context.get("volume_change_pct"))}</strong>
            </div>
        </div>

        <p class="reason">{text(decision.get("reason"))}</p>
        {render_agent_votes(decision)}
    </article>
    """


def system_health(decisions):
    if not decisions:
        return "No scan results"
    if any(decision.get("final_action") == "ERROR" for decision in decisions):
        return "Degraded"
    return "Online"


def render_dashboard(decisions, portfolio, current_value, last_scan_time):
    top_decisions = decisions[:10]
    cards = "\n".join(
        render_opportunity_card(rank, decision)
        for rank, decision in enumerate(top_decisions, start=1)
    )

    if not cards:
        cards = '<section class="empty">No opportunities were produced by the scanner.</section>'

    open_positions = len(portfolio.get("positions", {}))
    cash = portfolio.get("cash", 0)
    trade_count = len(portfolio.get("trades", []))
    health = system_health(decisions)

    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AEGIS Mission Control</title>
    <style>
        :root {{
            color-scheme: light;
            --bg: #f6f7f9;
            --panel: #ffffff;
            --ink: #17202a;
            --muted: #637083;
            --line: #d9dee7;
            --buy: #0f8a5f;
            --hold: #946200;
            --reject: #b42318;
            --error: #6b7280;
            --accent: #1d4ed8;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            background: var(--bg);
            color: var(--ink);
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.5;
        }}

        main {{
            width: min(1180px, calc(100% - 32px));
            margin: 0 auto;
            padding: 28px 0 40px;
        }}

        .topbar {{
            display: flex;
            justify-content: space-between;
            gap: 18px;
            align-items: flex-end;
            margin-bottom: 22px;
        }}

        h1, h2, p {{
            margin: 0;
        }}

        h1 {{
            font-size: 30px;
            line-height: 1.15;
        }}

        .subtitle {{
            margin-top: 6px;
            color: var(--muted);
        }}

        .health {{
            text-align: right;
            color: var(--muted);
            font-size: 14px;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin-bottom: 22px;
        }}

        .stat, .opportunity {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
        }}

        .stat {{
            padding: 16px;
        }}

        .stat span, .metrics span {{
            display: block;
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 5px;
        }}

        .stat strong {{
            font-size: 24px;
        }}

        .opportunities {{
            display: grid;
            gap: 14px;
        }}

        .opportunity {{
            padding: 18px;
        }}

        .opportunity-header {{
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: center;
            margin-bottom: 14px;
        }}

        .opportunity-header > div {{
            display: flex;
            align-items: baseline;
            gap: 10px;
        }}

        .rank {{
            color: var(--muted);
            font-weight: 700;
        }}

        h2 {{
            font-size: 22px;
        }}

        .pill {{
            display: inline-flex;
            align-items: center;
            min-height: 26px;
            padding: 3px 10px;
            border-radius: 999px;
            color: #fff;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0;
        }}

        .buy {{ background: var(--buy); }}
        .hold {{ background: var(--hold); }}
        .reject {{ background: var(--reject); }}
        .error, .neutral {{ background: var(--error); }}

        .metrics {{
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
            margin-bottom: 14px;
        }}

        .metrics div {{
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 10px;
            min-width: 0;
        }}

        .metrics strong {{
            font-size: 17px;
            word-break: break-word;
        }}

        .reason {{
            color: var(--muted);
            margin-bottom: 14px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th, td {{
            padding: 10px 8px;
            text-align: left;
            border-top: 1px solid var(--line);
            vertical-align: top;
        }}

        th {{
            color: var(--muted);
            font-size: 13px;
            font-weight: 700;
        }}

        .muted, .empty {{
            color: var(--muted);
        }}

        .empty {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 24px;
        }}

        @media (max-width: 820px) {{
            main {{
                width: min(100% - 20px, 1180px);
                padding-top: 18px;
            }}

            .topbar {{
                display: block;
            }}

            .health {{
                margin-top: 10px;
                text-align: left;
            }}

            .summary, .metrics {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}

            table, thead, tbody, tr, th, td {{
                display: block;
            }}

            thead {{
                display: none;
            }}

            td {{
                padding: 8px 0;
            }}
        }}
    </style>
</head>
<body>
    <main>
        <section class="topbar">
            <div>
                <h1>AEGIS Mission Control</h1>
                <p class="subtitle">Paper-trading command dashboard</p>
            </div>
            <div class="health">
                <strong>System health:</strong> {text(health)}<br>
                <strong>Last scan:</strong> {text(last_scan_time)}
            </div>
        </section>

        <section class="summary">
            <div class="stat">
                <span>Virtual Portfolio Value</span>
                <strong>{money(current_value)}</strong>
            </div>
            <div class="stat">
                <span>Cash Available</span>
                <strong>{money(cash)}</strong>
            </div>
            <div class="stat">
                <span>Trading Status</span>
                <strong>Paper Only</strong>
            </div>
            <div class="stat">
                <span>Positions / Trades</span>
                <strong>{open_positions} / {trade_count}</strong>
            </div>
        </section>

        <section class="opportunities">
            {cards}
        </section>
    </main>
</body>
</html>
"""


def main():
    last_scan_time = datetime.now().isoformat(timespec="seconds")
    decisions = scan_watchlist()
    portfolio = load_portfolio()
    price_lookup = build_price_lookup(decisions)
    current_value = portfolio_value(price_lookup)
    html_output = render_dashboard(decisions, portfolio, current_value, last_scan_time)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(html_output)
    print(f"Mission Control dashboard created: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
