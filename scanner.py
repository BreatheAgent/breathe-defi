"""
Breathe DeFi — Multi-Protocol Yield Scanner
Scans Base Mainnet DeFi protocols for current yield opportunities.
Fetches real APY/APR data from Aave V3, Morpho, Aerodrome, and Uniswap V3.
"""

import requests
from datetime import datetime, timezone


class YieldScanner:
    """Scans DeFi protocols on Base for yield opportunities."""

    def __init__(self):
        self.opportunities = []

    def scan_all(self) -> list:
        """Scan all supported protocols and return normalized yield data."""
        self.opportunities = []

        # Scan each protocol
        self.opportunities.extend(self._scan_aave_v3())
        self.opportunities.extend(self._scan_morpho())
        self.opportunities.extend(self._scan_aerodrome())
        self.opportunities.extend(self._scan_uniswap_v3())

        # Sort by APY descending
        self.opportunities.sort(key=lambda x: x["apy"], reverse=True)
        return self.opportunities

    def _scan_aave_v3(self) -> list:
        """Fetch Aave V3 supply rates on Base."""
        try:
            # Using DeFi Llama API for yield data
            resp = requests.get(
                "https://yields.llama.fi/pools",
                params={"chain": "Base"},
                timeout=15,
            )
            data = resp.json().get("data", [])

            aave_pools = [
                p for p in data
                if "aave" in p.get("project", "").lower()
                and p.get("chain", "").lower() == "base"
            ]

            return [
                {
                    "protocol": "aave_v3",
                    "pool": p.get("symbol", "unknown"),
                    "apy": p.get("apy", 0) / 100,  # Convert to decimal
                    "tvl": p.get("tvlUsd", 0),
                    "risk_score": 0.1,
                    "chain": "base",
                    "action": "supply",
                    "token": p.get("symbol", "").split("-")[0] if p.get("symbol") else "USDC",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                for p in aave_pools[:5]
            ]
        except Exception as e:
            print(f"[Scanner] Aave V3 scan failed: {e}")
            return []

    def _scan_morpho(self) -> list:
        """Fetch Morpho Blue market rates on Base."""
        try:
            resp = requests.get(
                "https://yields.llama.fi/pools",
                params={"chain": "Base"},
                timeout=15,
            )
            data = resp.json().get("data", [])

            morpho_pools = [
                p for p in data
                if "morpho" in p.get("project", "").lower()
                and p.get("chain", "").lower() == "base"
            ]

            return [
                {
                    "protocol": "morpho",
                    "pool": p.get("symbol", "unknown"),
                    "apy": p.get("apy", 0) / 100,
                    "tvl": p.get("tvlUsd", 0),
                    "risk_score": 0.2,
                    "chain": "base",
                    "action": "supply",
                    "token": p.get("symbol", "").split("-")[0] if p.get("symbol") else "USDC",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                for p in morpho_pools[:5]
            ]
        except Exception as e:
            print(f"[Scanner] Morpho scan failed: {e}")
            return []

    def _scan_aerodrome(self) -> list:
        """Fetch Aerodrome LP yields on Base."""
        try:
            resp = requests.get(
                "https://yields.llama.fi/pools",
                params={"chain": "Base"},
                timeout=15,
            )
            data = resp.json().get("data", [])

            aero_pools = [
                p for p in data
                if "aerodrome" in p.get("project", "").lower()
                and p.get("chain", "").lower() == "base"
                and p.get("tvlUsd", 0) > 100_000  # Min TVL filter
            ]

            return [
                {
                    "protocol": "aerodrome",
                    "pool": p.get("symbol", "unknown"),
                    "apy": p.get("apy", 0) / 100,
                    "tvl": p.get("tvlUsd", 0),
                    "risk_score": 0.35,
                    "chain": "base",
                    "action": "lp",
                    "token": p.get("symbol", ""),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                for p in aero_pools[:5]
            ]
        except Exception as e:
            print(f"[Scanner] Aerodrome scan failed: {e}")
            return []

    def _scan_uniswap_v3(self) -> list:
        """Fetch Uniswap V3 fee yields on Base."""
        try:
            resp = requests.get(
                "https://yields.llama.fi/pools",
                params={"chain": "Base"},
                timeout=15,
            )
            data = resp.json().get("data", [])

            uni_pools = [
                p for p in data
                if "uniswap" in p.get("project", "").lower()
                and p.get("chain", "").lower() == "base"
                and p.get("tvlUsd", 0) > 50_000
            ]

            return [
                {
                    "protocol": "uniswap_v3",
                    "pool": p.get("symbol", "unknown"),
                    "apy": p.get("apy", 0) / 100,
                    "tvl": p.get("tvlUsd", 0),
                    "risk_score": 0.3,
                    "chain": "base",
                    "action": "lp",
                    "token": p.get("symbol", ""),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                for p in uni_pools[:5]
            ]
        except Exception as e:
            print(f"[Scanner] Uniswap V3 scan failed: {e}")
            return []

    def get_best_opportunities(self, min_apy: float = 0.01, max_risk: float = 0.5, top_n: int = 5) -> list:
        """Get the best yield opportunities filtered by APY and risk."""
        if not self.opportunities:
            self.scan_all()

        filtered = [
            opp for opp in self.opportunities
            if opp["apy"] >= min_apy and opp["risk_score"] <= max_risk
        ]

        return filtered[:top_n]
