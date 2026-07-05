from dataclasses import dataclass, field

@dataclass
class AgentOpinion:
    agent: str
    symbol: str
    action: str
    confidence: int
    reason: str
    risk_flags: list = field(default_factory=list)

class BaseAgent:
    name = "Base Agent"

    def analyze(self, symbol: str, context: dict) -> AgentOpinion:
        raise NotImplementedError
