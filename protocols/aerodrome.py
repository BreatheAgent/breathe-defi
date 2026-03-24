"""Breathe DeFi — Aerodrome DEX Protocol (Base)"""
from web3 import Web3

AERODROME_ROUTER = "0xcF77a3Ba9A5CA399B7c97c74d54e5b1Beb874E43"

class Aerodrome:
    def __init__(self, w3: Web3, account):
        self.w3 = w3
        self.account = account

    def add_liquidity(self, token_a: str, token_b: str, amount: float, dry_run: bool = False) -> dict:
        if dry_run:
            return {"status": "dry_run", "protocol": "aerodrome", "action": "add_lp", "amount": amount}
        return {"status": "pending", "protocol": "aerodrome", "action": "add_lp", "amount": amount}

    def remove_liquidity(self, token_a: str, token_b: str, amount: float, dry_run: bool = False) -> dict:
        if dry_run:
            return {"status": "dry_run", "protocol": "aerodrome", "action": "remove_lp", "amount": amount}
        return {"status": "pending", "protocol": "aerodrome", "action": "remove_lp", "amount": amount}

    def get_yield(self) -> dict:
        return {"protocol": "aerodrome", "token": "LP", "apy": 0.0}
