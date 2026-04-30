"""Canonical category taxonomy for Horus retrieval generation."""

from __future__ import annotations


CATEGORY_MAP = {
    "oracle": ["oracle"],
    "amm": ["amm"],
    "bridge": ["bridge"],
    "tokens": ["tokens"],
    "cosmos": ["cosmos"],
    "solana": ["Solana-chain-specific"],
    "general": ["general"],
    "unique": ["unique"],
    "account-abstraction": ["account-abstraction"],
    "zk-rollup": ["zk-rollup"],
    "sui-move": ["Sui-Move-specific"],
}


GENERAL_SUBCATEGORIES = {
    "general-security": {
        "folders": [
            "access-control", "arbitrary-call", "missing-validations",
            "validation", "initialization", "signature",
        ],
        "description": "Access control, input validation, signatures, initialization",
    },
    "general-defi": {
        "folders": [
            "flash-loan", "slippage-protection",
            "vault-inflation-attack", "yield-strategy-vulnerabilities",
            "fee-on-transfer-tokens", "token-compatibility",
            "precision", "rounding-precision-loss", "calculation",
            "integer-overflow", "business-logic",
            "bonding-curve", "restaking",
            "perpetuals-derivatives", "lending-rate-model",
            "nft-marketplace",
        ],
        "description": "DeFi-specific: flash loans, slippage, vaults, precision, calculations, bonding curves, restaking, perpetuals, lending rates, NFT marketplaces",
    },
    "general-infrastructure": {
        "folders": [
            "proxy-vulnerabilities", "uups-proxy", "diamond-proxy",
            "storage-collision", "reentrancy", "bridge",
            "erc7702-integration",
        ],
        "description": "Smart contract infrastructure: proxies, reentrancy, storage, bridges",
    },
    "general-governance": {
        "folders": [
            "dao-governance-vulnerabilities", "dao-governance",
            "vetoken-governance",
            "stablecoin-vulnerabilities",
            "malicious", "mev-bot", "randomness",
        ],
        "description": "Governance, stablecoins, veToken voting, DAO governance, malicious patterns, MEV, randomness",
    },
}
