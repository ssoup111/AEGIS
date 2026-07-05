from config.settings import WATCHLIST
from aegis.market_data import get_market_context
from aegis.agent_registry import get_agents
from aegis.cio import ChiefInvestmentOfficer
from logger import log_decision

def scan_watchlist(symbols=None):
    symbols = symbols or WATCHLIST
    agents = get_agents()
    cio = ChiefInvestmentOfficer()
    decisions = []

    for symbol in symbols:
        try:
            context = get_market_context(symbol)
            opinions = [agent.analyze(symbol, context) for agent in agents]
            decision = cio.decide(symbol, opinions, context)
            log_decision(decision)
            decisions.append(decision)
        except Exception as e:
            decisions.append({
                "symbol": symbol,
                "final_action": "ERROR",
                "confidence": 0,
                "opportunity_score": -999,
                "reason": str(e),
                "market_context": {},
                "agent_opinions": [],
            })

    return sorted(decisions, key=lambda d: d.get("opportunity_score", -999), reverse=True)
