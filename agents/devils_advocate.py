from agents.base_agent import BaseAgent, AgentOpinion

class DevilsAdvocate(BaseAgent):
    name = "Devil's Advocate"

    def analyze(self, symbol: str, context: dict) -> AgentOpinion:
        risks = []

        if context.get("price_change_pct", 0) > 8:
            risks.append("possible_chase_after_big_move")
        if context.get("volume_change_pct", 0) < -35:
            risks.append("weak_volume")
        if context.get("headline_count", 0) == 0:
            risks.append("no_news_confirmation")
        if context.get("last_close", 0) <= 0:
            risks.append("bad_price_data")

        if "bad_price_data" in risks:
            return AgentOpinion(self.name, symbol, "REJECT", 95, "Market data appears invalid.", risks)

        if risks:
            return AgentOpinion(self.name, symbol, "HOLD", 65, "Trade has caution flags, but not enough to block.", risks)

        return AgentOpinion(self.name, symbol, "HOLD", 50, "No major objection found.", [])
