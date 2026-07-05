from pathlib import Path
from datetime import datetime

JOURNAL_DIR = Path("journal")
JOURNAL_DIR.mkdir(exist_ok=True)

def write_trade_journal(decision, result):
    symbol = decision["symbol"]
    date = datetime.now().strftime("%Y-%m-%d")
    path = JOURNAL_DIR / f"{date}-{symbol}.md"

    lines = [
        f"# AEGIS Trade Journal: {symbol}",
        "",
        f"Date: {datetime.now().isoformat()}",
        f"Action: {decision['final_action']}",
        f"Confidence: {decision['confidence']}%",
        f"Opportunity Score: {decision.get('opportunity_score')}",
        f"Result: {result}",
        "",
        "## CIO Reason",
        decision.get("reason", ""),
        "",
        "## Agent Votes",
    ]

    for opinion in decision.get("agent_opinions", []):
        lines.append(f"- {opinion['agent']}: {opinion['action']} ({opinion['confidence']}%) — {opinion['reason']}")

    path.write_text("\n".join(lines))
    return path
