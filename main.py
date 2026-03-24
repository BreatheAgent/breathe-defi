#!/usr/bin/env python3
"""
🌿 Breathe DeFi — DeFi Yield Farming Engine (Base Mainnet)

Scans, evaluates, and deploys capital across DeFi protocols for optimal yield.

Usage:
    python main.py --scan                  # Scan for yield opportunities
    python main.py --propose 500           # Generate allocation for $500
    python main.py --execute --dry-run     # Simulate execution
"""

import argparse
import json
from scanner import YieldScanner
from strategy import StrategyEngine
from rebalancer import Rebalancer


def scan_yields():
    print("🔍 Scanning Base Mainnet DeFi protocols...\n")
    scanner = YieldScanner()
    opps = scanner.scan_all()
    print(f"Found {len(opps)} opportunities:\n")
    for i, opp in enumerate(opps[:10], 1):
        print(f"  {i}. {opp['protocol']:12s} | {opp['pool']:20s} | APY: {opp['apy']:.2%} | Risk: {opp['risk_score']:.1f} | TVL: ${opp['tvl']:,.0f}")


def propose_allocation(amount: float, risk: str = "moderate"):
    print(f"📊 Generating allocation proposal for ${amount:.2f} ({risk} risk)...\n")
    scanner = YieldScanner()
    scanner.scan_all()
    engine = StrategyEngine(risk_tolerance=risk)
    best = scanner.get_best_opportunities(top_n=10)
    proposal = engine.generate_allocation_proposal(best, amount)
    print(json.dumps(proposal, indent=2))


def main():
    parser = argparse.ArgumentParser(description="🌿 Breathe DeFi Engine")
    parser.add_argument("--scan", action="store_true", help="Scan for yields")
    parser.add_argument("--propose", type=float, help="Generate allocation for amount")
    parser.add_argument("--risk", default="moderate", choices=["conservative", "moderate", "aggressive"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.scan:
        scan_yields()
    elif args.propose:
        propose_allocation(args.propose, args.risk)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
