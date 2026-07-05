from agents.base_agent import BaseAgent, AgentOpinion
from config.settings import MAX_TRADE_SIZE, MAX_OPEN_POSITIONS, MAX_DAILY_LOSS

class RiskManager(BaseAgent):
    name = "Risk Manager"

    def analyze(self, symbol: str, context: dict) -> AgentOpinion:
        if context.get("open_positions", 0) >= MAX_OPEN_POSITIONS:
            return AgentOpinion(self.name, symbol, "REJECT", 95, "Maximum open positions reached.", ["position_limit"])

        if context.get("daily_loss", 0) <= -MAX_DAILY_LOSS:
            return AgentOpinion(self.name, symbol, "REJECT", 100, "Daily loss limit reached.", ["daily_loss_limit"])

        return AgentOpinion(self.name, symbol, "ALLOW", 90, f"Trade allowed up to ${MAX_TRADE_SIZE}.", [])
