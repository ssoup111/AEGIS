from agents.base_agent import BaseAgent, AgentOpinion

class InsiderPoliticianMonitor(BaseAgent):
    name = "Insider/Politician Intelligence"

    def analyze(self, symbol: str, context: dict) -> AgentOpinion:
        public_signal = context.get("public_disclosure_signal", "none")

        if public_signal == "bullish":
            return AgentOpinion(self.name, symbol, "BUY", 62, "Public disclosure signal is bullish but may be delayed.", ["delayed_data"])
        if public_signal == "bearish":
            return AgentOpinion(self.name, symbol, "REJECT", 62, "Public disclosure signal is bearish but may be delayed.", ["delayed_data"])

        return AgentOpinion(self.name, symbol, "HOLD", 45, "No useful public disclosure signal yet.", ["no_signal"])
