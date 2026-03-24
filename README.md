# 🌿 Breathe DeFi — Yield Farming Engine

Part of the [Breathe Ecosystem](https://github.com/BreatheAgent).

## What It Does

Scans Base Mainnet DeFi protocols for optimal yield opportunities and deploys capital with risk-adjusted allocation.

### Supported Protocols

| Protocol | Type | Risk |
|----------|------|------|
| Aave V3 | Lending/Supply | 🟢 Very Low |
| Morpho Blue | Optimized Lending | 🟢 Low |
| Uniswap V3 | Concentrated LP | 🟡 Moderate |
| Aerodrome | LP + Gauges | 🟡 Moderate |

## Quick Start

```bash
pip install -r requirements.txt

# Scan yields
python main.py --scan

# Generate allocation proposal
python main.py --propose 400 --risk moderate

# Simulate
python main.py --propose 400 --dry-run
```

## Architecture

- `scanner.py` — Fetches real-time yields from DeFi Llama API
- `strategy.py` — Ranks by risk-adjusted score, generates allocation
- `rebalancer.py` — Detects allocation drift, triggers rebalance
- `protocols/` — Direct smart contract interactions per protocol

## Part of Breathe Ecosystem

| Repo | Purpose |
|------|---------|
| [breathe-core](https://github.com/BreatheAgent/breathe-core) | Central brain |
| **breathe-defi** | DeFi yield (you are here) |
| [breathe-trading](https://github.com/BreatheAgent/breathe-trading) | Perps + Polymarket |
| [breathe-memes](https://github.com/BreatheAgent/breathe-memes) | Solana memes |
