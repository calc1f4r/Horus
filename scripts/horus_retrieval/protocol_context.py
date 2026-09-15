"""Canonical protocol context taxonomy for Horus retrieval artifacts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProtocolContext:
    description: str
    manifests: tuple[str, ...]
    focus_patterns: tuple[str, ...]

    def as_router_entry(self) -> dict:
        return {
            "description": self.description,
            "manifests": list(self.manifests),
            "focusPatterns": list(self.focus_patterns),
        }


PROTOCOL_CONTEXTS: dict[str, ProtocolContext] = {
    "lending_protocol": ProtocolContext(
        description="Aave, Compound, lending/borrowing protocols",
        manifests=("lending", "oracle", "general-defi", "tokens", "general-security"),
        focus_patterns=(
            "staleness", "price manipulation", "liquidation",
            "flash loan", "precision", "rounding", "inflation attack",
            "reentrancy", "token compatibility",
            "bad debt", "health factor", "collateral", "supply cap", "borrow cap",
            "self liquidation", "interest accrual",
        ),
    ),
    "dex_amm": ProtocolContext(
        description="Uniswap, SushiSwap, decentralized exchanges",
        manifests=("amm", "general-defi", "oracle"),
        focus_patterns=(
            "slippage", "sandwich", "MEV", "TWAP", "slot0",
            "liquidity", "constant product", "fee", "reentrancy",
        ),
    ),
    "vault_yield": ProtocolContext(
        description="ERC4626 vaults, yield aggregators, strategies",
        manifests=("tokens", "general-defi", "oracle", "unique"),
        focus_patterns=(
            "ERC4626", "inflation attack", "first depositor",
            "rounding", "share price", "harvest", "strategy",
        ),
    ),
    "governance_dao": ProtocolContext(
        description="DAOs, governance systems, voting contracts",
        manifests=("general-governance",),
        focus_patterns=(
            "governance", "voting power", "quorum", "timelock",
            "proposal", "flash loan governance", "delegation",
        ),
    ),
    "cross_chain_bridge": ProtocolContext(
        description="Bridges, LayerZero, Wormhole, cross-chain messaging",
        manifests=("bridge", "general-infrastructure"),
        focus_patterns=(
            "replay", "message validation", "gas", "trusted remote",
            "VAA", "lzReceive", "stored payload",
        ),
    ),
    "cosmos_appchain": ProtocolContext(
        description="Cosmos SDK chains, IBC, app-chains",
        manifests=("cosmos",),
        focus_patterns=(
            "IBC", "staking", "slashing", "precompile",
            "chain halt", "governance", "hooks",
        ),
    ),
    "solana_program": ProtocolContext(
        description="Solana programs, Anchor, SPL tokens",
        manifests=("solana",),
        focus_patterns=(
            "PDA", "CPI", "anchor", "token-2022",
            "transfer hook", "account validation",
        ),
    ),
    "perpetuals_derivatives": ProtocolContext(
        description="Perpetual DEXes, options, derivatives",
        manifests=("oracle", "general-defi", "amm"),
        focus_patterns=(
            "staleness", "price manipulation", "liquidation",
            "flash loan", "precision", "funding rate",
        ),
    ),
    "token_launch": ProtocolContext(
        description="New token launches, meme coins, trading contracts",
        manifests=("general-governance", "tokens", "general-security"),
        focus_patterns=(
            "rug pull", "honeypot", "backdoor", "hidden mint",
            "fee extraction", "access control", "proxy initialization",
        ),
    ),
    "staking_liquid_staking": ProtocolContext(
        description="Staking protocols, liquid staking derivatives",
        manifests=("general-defi", "tokens", "oracle"),
        focus_patterns=(
            "reward calculation", "precision", "rounding",
            "ERC4626", "reentrancy", "staking",
        ),
    ),
    "nft_marketplace": ProtocolContext(
        description="NFT platforms, ERC721 marketplaces",
        manifests=("tokens", "general-infrastructure"),
        focus_patterns=(
            "ERC721", "callback", "onERC721Received",
            "reentrancy", "approval",
        ),
    ),
    "sui_move": ProtocolContext(
        description="Sui Move programs, DeFi on Sui, Sui object model",
        manifests=("sui-move", "general-defi", "general-security"),
        focus_patterns=(
            "UID", "object_id", "dynamic_field", "kiosk",
            "overflow", "share_price", "package_upgrade",
            "public_package", "capability", "flash_receipt",
            "sui_bridge", "cross_chain_bridge", "snap_rpc",
        ),
    ),
    "l2_rollup": ProtocolContext(
        description="zk/optimistic rollups, L2s, fraud proofs, sequencers",
        manifests=("zk-rollup", "bridge", "general-infrastructure"),
        focus_patterns=(
            "fraud proof", "circuit", "sequencer", "batch",
            "reorg", "withdrawal", "message validation", "bridge",
        ),
    ),
    "smart_account_aa": ProtocolContext(
        description="ERC-4337/7579 smart accounts, paymasters, module systems",
        manifests=("account-abstraction", "general-security", "tokens"),
        focus_patterns=(
            "ERC-4337", "ERC-7579", "paymaster", "bundler",
            "module", "session key", "UserOperation", "validation",
        ),
    ),
    "substrate_parachain": ProtocolContext(
        description="Substrate/Polkadot pallets, FRAME runtimes, parachains, ink! contracts",
        manifests=("substrate", "bridge", "general-security"),
        focus_patterns=(
            "pallet", "origin", "dispatchable", "weight", "ensure_signed",
            "ensure_root", "runtime upgrade", "governance", "referendum",
            "XCM", "GRANDPA", "BEEFY", "slot lease", "crowdloan",
            "existential deposit", "reserve", "lockable currency",
            "account derivation", "ed25519", "sr25519", "ink",
        ),
    ),
    "eth_l1_client": ProtocolContext(
        description="Ethereum L1 execution/consensus clients, node software, P2P networking",
        manifests=("eth-l1-clients", "bridge", "general-infrastructure"),
        focus_patterns=(
            "RLP", "devp2p", "discv4", "discv5", "ENR", "gossipsub",
            "libp2p", "snappy", "SSZ", "BLS", "KZG", "blob sidecar",
            "block validation", "state root", "txpool", "mempool",
            "engine API", "fork choice", "remote DoS", "OOM",
            "consensus", "Pectra", "Deneb", "EOF", "precompile",
        ),
    ),
    "bnb_chain_l1": ProtocolContext(
        description="BNB Chain L1: BSC core, Parlia/CometBFT consensus, Greenfield, opBNB",
        manifests=("bnb-chain", "cosmos", "bridge"),
        focus_patterns=(
            "Parlia", "CometBFT", "validator set", "cross-chain bridge",
            "Greenfield", "opBNB", "staking", "slash", "bundle",
            "fast finality", "governance", "native token",
        ),
    ),
}


def router_protocol_mappings() -> dict[str, dict]:
    return {
        name: context.as_router_entry()
        for name, context in PROTOCOL_CONTEXTS.items()
    }


def bundle_manifest_mapping() -> dict[str, list[str]]:
    return {
        name: list(context.manifests)
        for name, context in PROTOCOL_CONTEXTS.items()
    }

