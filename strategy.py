"""
Breathe DeFi — Yield Strategy Engine
Ranks opportunities by risk-adjusted return, applies risk tolerance filter,
and generates allocation proposals with reasoning.
"""

from typing import Optional


class StrategyEngine:
    """Ranks DeFi opportunities and generates allocation proposals."""

    # Risk tolerance maps to max acceptable risk score
    RISK_THRESHOLDS = {
        "conservative": 0.2,
        "moderate": 0.4,
        "aggressive": 0.7,
    }

    # Target allocation per protocol to avoid concentration
    MAX_PROTOCOL_PCT = 0.40  # Max 40% in any single protocol

    def __init__(self, risk_tolerance: str = "moderate"):
        self.risk_tolerance = risk_tolerance
        self.max_risk = self.RISK_THRESHOLDS.get(risk_tolerance, 0.4)

    def rank_opportunities(self, opportunities: list) -> list:
        """
        Rank opportunities by risk-adjusted APY (Sharpe-like scoring).
        Score = APY / (risk_score + 0.1)  — higher is better
        """
        for opp in opportunities:
            apy = opp.get("apy", 0)
            risk = opp.get("risk_score", 0.5)
            tvl = opp.get("tvl", 0)

            # Risk-adjusted score
            risk_adj_score = apy / (risk + 0.1)

            # TVL bonus: prefer pools with higher TVL (more liquid)
            tvl_bonus = min(tvl / 10_000_000, 0.5)  # Max 0.5 bonus for $10M+ TVL

            opp["score"] = risk_adj_score + tvl_bonus
            opp["reasoning"] = self._generate_reasoning(opp)

        # Filter by risk tolerance
        filtered = [
            opp for opp in opportunities
            if opp.get("risk_score", 1.0) <= self.max_risk
        ]

        # Sort by score descending
        filtered.sort(key=lambda x: x.get("score", 0), reverse=True)
        return filtered

    def generate_allocation_proposal(
        self,
        opportunities: list,
        total_capital: float,
        existing_positions: Optional[dict] = None,
    ) -> dict:
        """
        Generate a capital allocation proposal across top opportunities.

        Returns:
            {
                "proposals": [
                    {"protocol": str, "pool": str, "amount": float, "apy": float, ...},
                    ...
                ],
                "total_deployed": float,
                "expected_daily_yield": float,
                "expected_annual_yield": float,
            }
        """
        ranked = self.rank_opportunities(opportunities)
        existing = existing_positions or {}

        proposals = []
        total_deployed = 0
        remaining = total_capital

        for opp in ranked[:5]:  # Top 5 opportunities
            protocol = opp["protocol"]

            # Check protocol concentration
            existing_in_protocol = existing.get(protocol, 0)
            max_for_protocol = total_capital * self.MAX_PROTOCOL_PCT
            available_for_protocol = max_for_protocol - existing_in_protocol

            if available_for_protocol <= 0:
                continue

            # Allocate proportionally based on score
            allocation = min(
                remaining * 0.35,  # Max 35% of remaining capital per opportunity
                available_for_protocol,
                remaining,
            )

            if allocation < 1.0:  # Min $1 allocation
                continue

            proposals.append({
                "protocol": protocol,
                "pool": opp.get("pool", "unknown"),
                "action": opp.get("action", "supply"),
                "amount": round(allocation, 2),
                "apy": opp.get("apy", 0),
                "risk_score": opp.get("risk_score", 0),
                "score": opp.get("score", 0),
                "reasoning": opp.get("reasoning", ""),
            })

            total_deployed += allocation
            remaining -= allocation

        expected_daily = sum(
            p["amount"] * p["apy"] / 365 for p in proposals
        )
        expected_annual = sum(
            p["amount"] * p["apy"] for p in proposals
        )

        return {
            "proposals": proposals,
            "total_deployed": round(total_deployed, 2),
            "remaining_idle": round(remaining, 2),
            "expected_daily_yield": round(expected_daily, 4),
            "expected_annual_yield": round(expected_annual, 2),
            "risk_tolerance": self.risk_tolerance,
        }

    def _generate_reasoning(self, opp: dict) -> str:
        """Generate human-readable reasoning for why this opportunity is ranked."""
        apy = opp.get("apy", 0)
        risk = opp.get("risk_score", 0)
        tvl = opp.get("tvl", 0)
        protocol = opp.get("protocol", "unknown")

        parts = []
        parts.append(f"{protocol} offering {apy:.1%} APY")

        if risk <= 0.2:
            parts.append("very low risk (battle-tested protocol)")
        elif risk <= 0.4:
            parts.append("moderate risk")
        else:
            parts.append("higher risk — proceed with caution")

        if tvl > 1_000_000:
            parts.append(f"strong liquidity (${tvl / 1_000_000:.1f}M TVL)")
        elif tvl > 100_000:
            parts.append(f"decent liquidity (${tvl / 1_000:.0f}K TVL)")
        else:
            parts.append("low liquidity — size position carefully")

        return " | ".join(parts)
