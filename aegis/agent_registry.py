from agents.technical_analyst import TechnicalAnalyst
from agents.news_analyst import NewsAnalyst
from agents.insider_politician_monitor import InsiderPoliticianMonitor
from agents.devils_advocate import DevilsAdvocate
from agents.risk_manager import RiskManager

def get_agents():
    return [
        TechnicalAnalyst(),
        NewsAnalyst(),
        InsiderPoliticianMonitor(),
        DevilsAdvocate(),
        RiskManager(),
    ]
