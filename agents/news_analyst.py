from agents.base_agent import BaseAgent, AgentOpinion

class NewsAnalyst(BaseAgent):
    name = "News Analyst"

    def analyze(self, symbol: str, context: dict) -> AgentOpinion:
        headlines = context.get("headlines", [])
        text = " ".join(headlines).lower()

        good_words = ["beats", "raises", "upgrade", "growth", "contract", "approval", "surge", "record"]
        bad_words = ["misses", "downgrade", "lawsuit", "probe", "recall", "delay", "falls", "cut"]

        good = sum(1 for w in good_words if w in text)
        bad = sum(1 for w in bad_words if w in text)

        if good > bad:
            return AgentOpinion(self.name, symbol, "BUY", 66, "News tone appears positive.", [])
        if bad > good:
            return AgentOpinion(self.name, symbol, "REJECT", 70, "News tone appears negative.", ["negative_news"])

        return AgentOpinion(self.name, symbol, "HOLD", 50, "No strong news signal.", [])
