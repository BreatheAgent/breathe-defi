# 🌿 Breathe DeFi — Yield Farming Engine

**Agent Name:** Breathe Defi  
**Token Address:** [0x3d6a4fEa44986Cb2c9745905f3E2BF2A3ea7aFED](https://basescan.org/token/0x3d6a4fEa44986Cb2c9745905f3E2BF2A3ea7aFED)

Part of the [Breathe Ecosystem](https://github.com/BreatheAgent).

## What It Does

Breathe Defi is an autonomous agent dedicated to maximizing capital growth across decentralized finance protocols. It scans Base Mainnet for optimal yield opportunities, evaluates risk-adjusted rewards, and manages liquidity with precision-driven allocation strategies.

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
