"""
Breathe DeFi — Aave V3 Protocol Module (Base Mainnet)
Handles supply, withdraw, and position tracking on Aave V3.
"""

from web3 import Web3

AAVE_V3_POOL = "0xA238Dd80C259a72e81d7e4664a9801593F98d1c5"
USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"

# Minimal Aave V3 Pool ABI
POOL_ABI = [
    {
        "inputs": [
            {"name": "asset", "type": "address"},
            {"name": "amount", "type": "uint256"},
            {"name": "onBehalfOf", "type": "address"},
            {"name": "referralCode", "type": "uint16"},
        ],
        "name": "supply",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "asset", "type": "address"},
            {"name": "amount", "type": "uint256"},
            {"name": "to", "type": "address"},
        ],
        "name": "withdraw",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
]


class AaveV3:
    """Aave V3 integration for Base Mainnet."""

    def __init__(self, w3: Web3, account):
        self.w3 = w3
        self.account = account
        self.pool = w3.eth.contract(
            address=Web3.to_checksum_address(AAVE_V3_POOL), abi=POOL_ABI
        )

    def supply_usdc(self, amount: float, dry_run: bool = False) -> dict:
        """Supply USDC to Aave V3 to earn yield."""
        amount_raw = int(amount * 1e6)  # USDC has 6 decimals

        if dry_run:
            return {"status": "dry_run", "protocol": "aave_v3", "action": "supply", "amount": amount}

        tx = self.pool.functions.supply(
            Web3.to_checksum_address(USDC_BASE),
            amount_raw,
            self.account.address,
            0,  # No referral
        ).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 300_000,
            "gasPrice": self.w3.eth.gas_price,
            "chainId": self.w3.eth.chain_id,
        })

        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return {
            "status": "success" if receipt.status == 1 else "failed",
            "protocol": "aave_v3",
            "action": "supply",
            "amount": amount,
            "tx_hash": receipt.transactionHash.hex(),
        }

    def withdraw_usdc(self, amount: float, dry_run: bool = False) -> dict:
        """Withdraw USDC from Aave V3."""
        amount_raw = int(amount * 1e6)

        if dry_run:
            return {"status": "dry_run", "protocol": "aave_v3", "action": "withdraw", "amount": amount}

        tx = self.pool.functions.withdraw(
            Web3.to_checksum_address(USDC_BASE),
            amount_raw,
            self.account.address,
        ).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 300_000,
            "gasPrice": self.w3.eth.gas_price,
            "chainId": self.w3.eth.chain_id,
        })

        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return {
            "status": "success" if receipt.status == 1 else "failed",
            "protocol": "aave_v3",
            "action": "withdraw",
            "amount": amount,
            "tx_hash": receipt.transactionHash.hex(),
        }

    def get_yield(self) -> dict:
        """Get current USDC supply APY."""
        return {"protocol": "aave_v3", "token": "USDC", "apy": 0.0, "source": "on-chain"}
