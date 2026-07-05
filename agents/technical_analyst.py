from agents.base_agent import BaseAgent, AgentOpinion

class TechnicalAnalyst(BaseAgent):
    name = "Technical Analyst"

    def analyze(self, symbol: str, context: dict) -> AgentOpinion:
        price_change = context.get("price_change_pct", 0)
        volume_change = context.get("volume_change_pct", 0)

        if price_change > 2 and volume_change > 20:
            return AgentOpinion(self.name, symbol, "BUY", 78, "Positive price movement with stronger volume.", [])
        if price_change > 1:
            return AgentOpinion(self.name, symbol, "BUY", 62, "Positive momentum, but not exceptional.", [])
        if price_change < -2:
            return AgentOpinion(self.name, symbol, "REJECT", 72, "Negative momentum.", ["falling_price"])

        return AgentOpinion(self.name, symbol, "HOLD", 55, "No strong technical signal.", [])
