"""
Breathe DeFi — Portfolio Rebalancer
Monitors allocation drift and triggers rebalancing when thresholds are exceeded.
"""


class Rebalancer:
    """Monitors and corrects DeFi portfolio allocation drift."""

    def __init__(self, drift_threshold: float = 0.05):
        self.drift_threshold = drift_threshold  # 5% drift triggers rebalance

    def check_drift(self, current_positions: dict, target_allocation: dict, total_value: float) -> list:
        """
        Compare current positions vs target allocation.
        Returns list of actions needed to rebalance.
        """
        actions = []

        for protocol, target_pct in target_allocation.items():
            current_value = current_positions.get(protocol, 0)
            current_pct = current_value / total_value if total_value > 0 else 0
            drift = target_pct - current_pct

            if abs(drift) > self.drift_threshold:
                amount = abs(drift) * total_value
                action_type = "deposit" if drift > 0 else "withdraw"

                actions.append({
                    "protocol": protocol,
                    "action": action_type,
                    "amount": round(amount, 2),
                    "current_pct": round(current_pct, 4),
                    "target_pct": round(target_pct, 4),
                    "drift": round(drift, 4),
                })

        return actions

    def should_rebalance(self, current_positions: dict, target_allocation: dict, total_value: float) -> bool:
        """Check if any position has drifted beyond threshold."""
        actions = self.check_drift(current_positions, target_allocation, total_value)
        return len(actions) > 0

    def generate_rebalance_plan(self, current_positions: dict, target_allocation: dict, total_value: float) -> dict:
        """Generate a complete rebalance plan with withdrawals first, then deposits."""
        actions = self.check_drift(current_positions, target_allocation, total_value)

        withdrawals = [a for a in actions if a["action"] == "withdraw"]
        deposits = [a for a in actions if a["action"] == "deposit"]

        return {
            "needs_rebalance": len(actions) > 0,
            "withdrawals_first": withdrawals,  # Always withdraw before depositing
            "then_deposits": deposits,
            "total_moves": len(actions),
            "total_volume": sum(a["amount"] for a in actions),
        }
