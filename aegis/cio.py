class ChiefInvestmentOfficer:
    name = "Chief Investment Officer"

    def decide(self, symbol: str, opinions: list, context: dict) -> dict:
        buy_score = sum(o.confidence for o in opinions if o.action == "BUY")
        reject_score = sum(o.confidence for o in opinions if o.action == "REJECT")
        allow_score = sum(o.confidence for o in opinions if o.action == "ALLOW")

        hard_rejects = [o for o in opinions if o.action == "REJECT" and o.confidence >= 90]

        if hard_rejects:
            final_action = "REJECT"
            confidence = max(o.confidence for o in hard_rejects)
            opportunity_score = 0
            reason = "Hard risk rejection."
        else:
            opportunity_score = buy_score + (allow_score * 0.25) - reject_score
            if opportunity_score >= 110:
                final_action = "BUY"
                confidence = min(90, int(opportunity_score / 2))
                reason = "Weighted agent consensus favors buying."
            elif opportunity_score <= -40:
                final_action = "REJECT"
                confidence = min(90, abs(int(opportunity_score)))
                reason = "Weighted agent consensus rejects trade."
            else:
                final_action = "HOLD"
                confidence = 60
                reason = "No strong enough consensus."

        return {
            "symbol": symbol,
            "final_action": final_action,
            "confidence": confidence,
            "opportunity_score": round(opportunity_score, 2),
            "reason": reason,
            "market_context": context,
            "agent_opinions": [o.__dict__ for o in opinions],
        }
