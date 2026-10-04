#!/usr/bin/env python3
"""
Stage 3: DeFiHackLabs DB Entry Generator
==========================================
Reads classified data and generates:
1. NEW .md files for gap categories (10 files)
2. Appendable enrichment sections for existing categories (28 files)

Input:  scripts/output/defihacklabs_classified.json
Output: DB/**/*.md files (new + enriched)
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "scripts" / "output" / "defihacklabs_classified.json"
DB_DIR = BASE_DIR / "DB"

# ─── Severity Heuristic ──────────────────────────────────────────────────────

def loss_to_severity(loss_usd: float) -> str:
    if loss_usd >= 10_000_000:
        return "CRITICAL"
    elif loss_usd >= 1_000_000:
        return "HIGH"
    elif loss_usd >= 100_000:
        return "MEDIUM"
    elif loss_usd >= 10_000:
        return "LOW"
    return "INFORMATIONAL"


def format_loss(loss_usd: float) -> str:
    if loss_usd >= 1_000_000:
        return f"${loss_usd / 1_000_000:.1f}M"
    elif loss_usd >= 1_000:
        return f"${loss_usd / 1_000:.0f}K"
    elif loss_usd > 0:
        return f"${loss_usd:,.0f}"
    return "N/A"


# ─── New Entry Templates ─────────────────────────────────────────────────────

CATEGORY_META = {
    "input-validation": {
        "title": "Input Validation Vulnerabilities",
        "overview": "Input validation vulnerabilities occur when smart contracts fail to properly validate function parameters, calldata, user-supplied data, or destination addresses before processing them. Attackers exploit these gaps to manipulate contract behavior, bypass security checks, or drain funds through carefully crafted inputs.",
        "root_cause": "Critical functions accept and process user-controlled inputs without sufficient validation of data types, ranges, addresses, or business logic constraints, enabling attackers to pass malicious or unexpected values that subvert intended contract behavior.",
        "primitives": ["calldata_validation", "parameter_check", "address_validation", "token_validation", "owner_verification", "input_sanitization", "range_check", "zero_address_check"],
        "tags": ["input_validation", "parameter_check", "calldata", "missing_validation", "user_input", "address_validation", "real_exploit", "defi", "DeFiHackLabs"],
        "affected_components": ["router_functions", "swap_handlers", "parameter_setters", "migration_functions", "claim_functions"],
        "severity_range": "LOW to CRITICAL",
    },
    "skim-balance": {
        "title": "Skim Token Balance Attack Patterns",
        "overview": "Skim balance attacks exploit the `skim()` function in Uniswap V2-style AMMs, which transfers excess tokens (difference between actual balance and reserves) to a specified address. Attackers manipulate token balances through transfers, rebasing, or reflection mechanics to create exploitable discrepancies between recorded reserves and actual balances.",
        "root_cause": "AMM pairs track reserves via internal state variables that can diverge from actual token balances. The `skim()` function transfers this difference without adequate access control or balance verification, creating an extraction vector when combined with tokens that modify balances externally (reflection, rebasing, fee-on-transfer).",
        "primitives": ["skim_function", "reserve_tracking", "balance_discrepancy", "reflection_token", "sync_function", "pair_manipulation"],
        "tags": ["skim", "uniswap_v2", "pair_manipulation", "reserve_sync", "reflection_token", "balance_manipulation", "real_exploit", "defi", "DeFiHackLabs"],
        "affected_components": ["uniswap_v2_pair", "amm_pair", "liquidity_pool"],
        "severity_range": "LOW to MEDIUM",
    },
    "metapool-attack": {
        "title": "Swap Metapool Attack Patterns",
        "overview": "Metapool attacks target Curve-style metapools that combine a base pool LP token with another asset. Attackers exploit the virtual price calculation and swap mechanics of these nested pool structures to extract value through carefully orchestrated swap sequences that exploit imbalances between the metapool and its underlying base pool.",
        "root_cause": "Metapools rely on virtual price feeds from base pools that can be manipulated through large swaps. The nested pool architecture creates price dependency chains where manipulation in one layer propagates to impact valuations and swap rates in connected pools.",
        "primitives": ["metapool_swap", "virtual_price", "base_pool_lp", "curve_pool", "imbalanced_pool"],
        "tags": ["metapool", "curve", "saddle", "nerve", "virtual_price", "base_pool", "swap_manipulation", "real_exploit", "defi", "DeFiHackLabs"],
        "affected_components": ["curve_metapool", "saddle_pool", "nerve_bridge"],
        "severity_range": "HIGH to CRITICAL",
    },
    "liquidity-migration": {
        "title": "Liquidity Migration Exploit Patterns",
        "overview": "Liquidity migration exploits target the migration mechanisms that protocols use to move liquidity between pool versions (e.g., V2→V3, protocol upgrades). Attackers exploit flaws in the migration logic, including improper price validation during migration, unprotected migration functions, and calculation errors in liquidity conversion ratios.",
        "root_cause": "Migration functions perform complex multi-step operations (remove from old pool, calculate new params, add to new pool) with insufficient validation of intermediate values, price bounds, or access controls. The complexity of cross-version conversions creates windows for exploitation.",
        "primitives": ["liquidity_migration", "version_upgrade", "price_bounds", "tick_calculation", "lp_conversion"],
        "tags": ["liquidity_migration", "v3_migration", "pool_upgrade", "team_finance", "biswap", "version_migration", "real_exploit", "defi", "DeFiHackLabs"],
        "affected_components": ["migrator_contract", "liquidity_router", "pool_factory"],
        "severity_range": "HIGH to CRITICAL",
    },
    "msgvalue-loop": {
        "title": "msg.value in Loop Vulnerability",
        "overview": "When `msg.value` is used inside a loop, the same ETH value is counted multiple times because `msg.value` remains constant throughout the entire transaction. This allows attackers to mint multiple assets, make multiple deposits, or perform multiple operations while only sending ETH once, effectively multiplying their purchasing power.",
        "root_cause": "Solidity's `msg.value` is a transaction-level constant that does not decrease when ETH is spent within the transaction. Using `msg.value` as a payment check inside a loop allows the same ETH to be 'spent' multiple times, as each iteration sees the full original `msg.value`.",
        "primitives": ["msg_value", "loop_iteration", "eth_payment", "batch_operation", "double_spending"],
        "tags": ["msg_value", "loop", "double_spend", "batch_mint", "eth_payment", "opyn", "real_exploit", "defi", "DeFiHackLabs"],
        "affected_components": ["batch_functions", "multi_mint", "loop_payments"],
        "severity_range": "HIGH to CRITICAL",
    },
    "arbitrage": {
        "title": "Economic Arbitrage Design Flaws",
        "overview": "Economic arbitrage design flaws occur when protocol mechanisms create predictable profit opportunities through price discrepancies between internal and external markets, misconfigured swap parameters, or flawed economic incentive structures. Unlike flash loan attacks, these exploit fundamental design weaknesses in the protocol's economic model.",
        "root_cause": "Protocols implement fixed exchange rates, hardcoded price ratios, or incentive mechanisms that diverge from market prices, creating risk-free arbitrage opportunities. The lack of dynamic pricing or oracle integration allows systematic extraction of value.",
        "primitives": ["price_discrepancy", "fixed_rate", "market_arbitrage", "incentive_misalignment", "swap_rate"],
        "tags": ["arbitrage", "economic_design", "price_discrepancy", "fixed_rate", "incentive_flaw", "real_exploit", "defi", "DeFiHackLabs"],
        "affected_components": ["swap_mechanism", "reward_system", "exchange_rate"],
        "severity_range": "MEDIUM to HIGH",
    },
    "nft-specific": {
        "title": "NFT-Specific Exploit Patterns",
        "overview": "NFT-specific exploits target vulnerabilities unique to NFT marketplaces, minting mechanisms, and NFT-integrated DeFi protocols. These include marketplace listing manipulation, NFT-backed lending flaws, and cross-chain NFT bridge vulnerabilities that don't fit into traditional DeFi vulnerability categories.",
        "root_cause": "NFT protocols combine complex stateful operations (listings, auctions, royalties) with token standards that have less battle-tested security patterns than ERC20 tokens. The unique properties of NFTs (non-fungibility, metadata, royalties) introduce attack surfaces not present in fungible token protocols.",
        "primitives": ["nft_listing", "marketplace_logic", "royalty_bypass", "metadata_manipulation", "onERC721Received"],
        "tags": ["nft", "marketplace", "erc721", "listing", "auction", "optimism", "quixotic", "real_exploit", "DeFiHackLabs"],
        "affected_components": ["nft_marketplace", "listing_contract", "auction_contract"],
        "severity_range": "MEDIUM to HIGH",
    },
    "stale-state": {
        "title": "Stale/Cached State Exploit Patterns",
        "overview": "Stale state vulnerabilities occur when contracts use cached or outdated values for critical calculations instead of querying current on-chain state. This includes outdated global variables, price caching without refresh mechanisms, and state variables that should track but lag behind actual protocol conditions.",
        "root_cause": "Contracts cache state variables for gas optimization or simplicity but fail to implement adequate refresh mechanisms, staleness checks, or invalidation logic. When market conditions change rapidly, the gap between cached and actual values becomes exploitable.",
        "primitives": ["cached_state", "stale_variable", "outdated_price", "state_refresh", "global_variable"],
        "tags": ["stale_state", "cached_price", "outdated_variable", "state_refresh", "price_cache", "design_defect", "real_exploit", "defi", "DeFiHackLabs"],
        "affected_components": ["price_oracle", "state_cache", "global_variables"],
        "severity_range": "MEDIUM to HIGH",
    },
    "fee-mechanism": {
        "title": "Fee Mechanism Exploitation Patterns",
        "overview": "Fee mechanism exploits target flaws in how protocols calculate, collect, or distribute fees. This includes zero-fee bypass vulnerabilities, incorrect fee calculation logic, fee-on-transfer token handling errors, and exploitable fee distribution mechanisms that allow attackers to extract value or bypass intended economic constraints.",
        "root_cause": "Fee mechanisms involve complex calculation logic with edge cases (zero amounts, maximum values, rounding) that can be exploited. Protocols may fail to account for fee-on-transfer tokens, implement incorrect fee tiers, or allow fee parameters to be manipulated.",
        "primitives": ["fee_calculation", "zero_fee", "fee_bypass", "fee_distribution", "fee_on_transfer"],
        "tags": ["fee_mechanism", "zero_fee", "fee_bypass", "fee_calculation", "treasure_dao", "real_exploit", "defi", "DeFiHackLabs"],
        "affected_components": ["fee_controller", "marketplace", "swap_router"],
        "severity_range": "MEDIUM to HIGH",
    },
    "compiler-bug": {
        "title": "Compiler-Level Vulnerability Patterns",
        "overview": "Compiler-level vulnerabilities occur when bugs in the compiler itself (Solidity, Vyper, etc.) silently generate incorrect bytecode from correct source code. These are particularly dangerous because auditors reviewing source code cannot detect the vulnerability — the bug exists only in the compiled output. The most notable example is the Vyper compiler reentrancy lock bug that led to $41M in losses from Curve pools.",
        "root_cause": "Compilers are complex software that can contain bugs in code generation, optimization passes, or language feature implementations. When these bugs affect security-critical features (like reentrancy guards), they can silently disable protections that developers and auditors believe are in place.",
        "primitives": ["compiler_bug", "bytecode_generation", "optimization_pass", "reentrancy_lock", "vyper_compiler"],
        "tags": ["compiler", "vyper", "solidity", "bytecode", "reentrancy_lock", "optimization_bug", "curve", "real_exploit", "DeFiHackLabs"],
        "affected_components": ["vyper_compiler", "solidity_compiler", "reentrancy_guard"],
        "severity_range": "CRITICAL",
    },
}


def generate_exploit_table(entries: list[dict], max_rows: int = 30) -> str:
    """Generate a markdown table of exploits."""
    lines = [
        "| Protocol | Date | Loss | Vulnerability Sub-type | Chain |",
        "|----------|------|------|----------------------|-------|",
    ]
    for e in entries[:max_rows]:
        date_str = e.get("date", "")
        if len(date_str) == 8:
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        protocol = e.get("protocol", "Unknown")
        loss = format_loss(e.get("loss_usd_estimate", 0))
        raw_label = e.get("raw_label", "")
        chain = e.get("chain", "unknown")
        lines.append(f"| {protocol} | {date_str} | {loss} | {raw_label} | {chain} |")
    if len(entries) > max_rows:
        lines.append(f"| ... | ... | ... | +{len(entries) - max_rows} more exploits | ... |")
    return "\n".join(lines)


def generate_poc_references(entries: list[dict], max_refs: int = 10) -> str:
    """Generate PoC reference links."""
    lines = []
    for e in entries[:max_refs]:
        poc = e.get("poc_resolved_path")
        if poc:
            protocol = e.get("protocol", "Unknown")
            date = e.get("date", "")
            loss = format_loss(e.get("loss_usd_estimate", 0))
            lines.append(f"- **{protocol}** ({date[:4]}-{date[4:6]}, {loss}): `DeFiHackLabs/{poc}`")
    return "\n".join(lines) if lines else "- No PoC files resolved for this category"


def generate_keywords(group: dict) -> list[str]:
    """Generate keyword list from group data."""
    keywords = set()
    cat = group["category"]
    
    # Add category-level keywords
    meta = CATEGORY_META.get(cat, {})
    keywords.update(meta.get("tags", []))
    
    # Extract keywords from protocol names
    for sv_entries in group["sub_variants"].values():
        for e in sv_entries[:20]:
            protocol = e.get("protocol", "").lower()
            if protocol and len(protocol) > 2:
                keywords.add(protocol.replace(" ", "_"))
            chain = e.get("chain", "")
            if chain:
                keywords.add(chain)
            raw = e.get("raw_label", "").lower()
            # Extract meaningful words
            for word in re.findall(r'[a-z]{4,}', raw):
                if word not in {"that", "this", "with", "from", "through", "does", "lack", "were", "have", "been"}:
                    keywords.add(word)
    
    return sorted(keywords)[:30]


def generate_new_entry(group: dict) -> str:
    """Generate a complete new DB entry file."""
    cat = group["category"]
    meta = CATEGORY_META.get(cat, {})
    
    title = meta.get("title", f"{cat.replace('-', ' ').title()} Vulnerabilities")
    overview = meta.get("overview", f"Vulnerability patterns related to {cat}.")
    root_cause = meta.get("root_cause", f"Missing or flawed {cat} implementation.")
    primitives = meta.get("primitives", [cat.replace("-", "_")])
    tags = meta.get("tags", [cat.replace("-", "_"), "real_exploit", "defi", "DeFiHackLabs"])
    affected = meta.get("affected_components", ["smart_contract"])
    severity_range = meta.get("severity_range", "MEDIUM to CRITICAL")
    
    # Collect all entries flat
    all_entries = []
    for sv_entries in group["sub_variants"].values():
        all_entries.extend(sv_entries)
    all_entries.sort(key=lambda e: e.get("loss_usd_estimate", 0), reverse=True)
    
    total_loss = sum(e.get("loss_usd_estimate", 0) for e in all_entries)
    keywords = generate_keywords(group)
    
    # Build frontmatter
    prim_yaml = "\n".join(f"  - {p}" for p in primitives)
    tags_yaml = "\n".join(f"  - {t}" for t in tags)
    affected_yaml = "\n".join(f"  - {a}" for a in affected)
    
    sections = []
    
    # YAML frontmatter
    sections.append(f"""---
vulnerability_class: {cat}
title: "{title}"
category: {cat.replace('-', ' ').title()}
severity_range: "{severity_range}"
source: DeFiHackLabs

primitives:
{prim_yaml}

affected_components:
{affected_yaml}

tags:
{tags_yaml}

total_exploits_analyzed: {group['total_exploits']}
total_losses: "{format_loss(total_loss)}"
---""")
    
    # Title and overview
    sections.append(f"""# {title}

## Overview

{overview}

**Root Cause Statement**: {root_cause}

**Observed Frequency**: {group['total_exploits']} real-world exploits found in DeFiHackLabs (2017-2025)
**Consensus Severity**: {severity_range}
**Total Historical Losses**: {format_loss(total_loss)}""")
    
    # Vulnerability categories (sub-variants)
    sections.append("---\n\n## Vulnerability Categories")
    for i, (sv_name, sv_entries) in enumerate(group["sub_variants"].items(), 1):
        sv_loss = sum(e.get("loss_usd_estimate", 0) for e in sv_entries)
        sv_display = sv_name.replace("_", " ").title()
        severity = loss_to_severity(sv_loss / max(len(sv_entries), 1))
        sections.append(f"""### Category {i}: {sv_display} [{severity}]

{len(sv_entries)} exploit(s) | Total losses: {format_loss(sv_loss)}""")
        
        # Top exploit example
        if sv_entries:
            top = sv_entries[0]
            sections.append(f"""
**Top Exploit: {top['protocol']} ({top['date'][:4]}-{top['date'][4:6]}) - {format_loss(top.get('loss_usd_estimate', 0))} Lost**""")
            if top.get("poc_resolved_path"):
                sections.append(f"**PoC Reference**: `DeFiHackLabs/{top['poc_resolved_path']}`")
            if top.get("attack_tx"):
                sections.append(f"**Attack TX**: {top['attack_tx']}")
    
    # Full exploit table
    sections.append(f"""---

## Complete Exploit List

{generate_exploit_table(all_entries)}""")
    
    # PoC references
    sections.append(f"""---

## DeFiHackLabs PoC References

{generate_poc_references(all_entries, max_refs=15)}""")
    
    # Keywords
    kw_str = "\n".join(f"- {kw}" for kw in keywords)
    sections.append(f"""---

## Keywords

{kw_str}""")
    
    return "\n\n".join(sections) + "\n"


# ─── Enrichment Section Generator ────────────────────────────────────────────

def generate_enrichment_section(group: dict) -> str:
    """Generate an appendable enrichment section for existing DB files."""
    cat = group["category"]
    
    all_entries = []
    for sv_entries in group["sub_variants"].values():
        all_entries.extend(sv_entries)
    all_entries.sort(key=lambda e: e.get("loss_usd_estimate", 0), reverse=True)
    
    total_loss = sum(e.get("loss_usd_estimate", 0) for e in all_entries)
    
    sections = []
    sections.append(f"""---

## DeFiHackLabs Real-World Exploits ({group['total_exploits']} incidents)

**Category**: {cat.replace('-', ' ').title()} | **Total Losses**: {format_loss(total_loss)} | **Sub-variants**: {group['sub_variant_count']}
""")
    
    # Sub-variant breakdown
    sections.append("### Sub-variant Breakdown\n")
    for sv_name, sv_entries in group["sub_variants"].items():
        sv_loss = sum(e.get("loss_usd_estimate", 0) for e in sv_entries)
        sv_display = sv_name.replace("_", " ").title()
        sections.append(f"#### {sv_display} ({len(sv_entries)} exploits, {format_loss(sv_loss)})\n")
        
        # Top 3 exploits per sub-variant
        for e in sv_entries[:3]:
            date = e.get("date", "")
            date_str = f"{date[:4]}-{date[4:6]}" if len(date) >= 6 else date
            protocol = e.get("protocol", "Unknown")
            loss = format_loss(e.get("loss_usd_estimate", 0))
            chain = e.get("chain", "unknown")
            poc = e.get("poc_resolved_path", "")
            poc_ref = f" | PoC: `DeFiHackLabs/{poc}`" if poc else ""
            sections.append(f"- **{protocol}** ({date_str}, {loss}, {chain}){poc_ref}")
        
        if len(sv_entries) > 3:
            sections.append(f"- *... and {len(sv_entries) - 3} more exploits*")
        sections.append("")
    
    # Full table
    sections.append(f"""### Complete DeFiHackLabs Exploit Table

{generate_exploit_table(all_entries, max_rows=50)}""")
    
    # PoC references
    top_pocs = [e for e in all_entries if e.get("poc_resolved_path")][:10]
    if top_pocs:
        sections.append(f"""
### Top PoC References

{generate_poc_references(top_pocs)}""")
    
    return "\n".join(sections) + "\n"


# ─── Main Pipeline ────────────────────────────────────────────────────────────

def main():
    if not INPUT_FILE.exists():
        print(f"[!] Input file not found: {INPUT_FILE}")
        return
    
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)
    
    groups = data["groups"]
    print(f"[*] Loaded {len(groups)} category groups")
    
    new_created = 0
    enriched = 0
    errors = []
    
    # Group enrichments by target file to avoid duplicates
    enrich_by_file = defaultdict(list)
    
    for group in groups:
        cat = group["category"]
        action = group["action"]
        db_path = group["db_target_path"]
        
        if not db_path:
            print(f"  [SKIP] {cat}: no target path (off-chain)")
            continue
        
        full_path = BASE_DIR / db_path
        
        if action == "create_new":
            # Generate and write new entry
            content = generate_new_entry(group)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)
            new_created += 1
            print(f"  [NEW] Created {db_path} ({group['total_exploits']} exploits)")
        
        elif action == "enrich":
            enrich_by_file[db_path].append(group)
    
    # Process enrichments grouped by target file
    for db_path, file_groups in enrich_by_file.items():
        full_path = BASE_DIR / db_path
        
        # Merge all groups targeting this file into one enrichment section
        total_exploits = sum(g["total_exploits"] for g in file_groups)
        total_loss = sum(g["total_loss_usd"] for g in file_groups)
        
        # Combine sub-variants from all groups
        merged_sub_variants = {}
        for g in file_groups:
            for sv_name, sv_entries in g["sub_variants"].items():
                key = f"{g['category']}/{sv_name}"
                merged_sub_variants[key] = sv_entries
        
        merged_group = {
            "category": ", ".join(g["category"] for g in file_groups),
            "total_exploits": total_exploits,
            "total_loss_usd": total_loss,
            "sub_variant_count": len(merged_sub_variants),
            "sub_variants": merged_sub_variants,
        }
        
        enrichment = generate_enrichment_section(merged_group)
        
        if full_path.exists():
            existing = full_path.read_text()
            if "## DeFiHackLabs Real-World Exploits" in existing:
                marker = "## DeFiHackLabs Real-World Exploits"
                idx = existing.index(marker)
                pre_idx = existing.rfind("\n---\n", 0, idx)
                if pre_idx >= 0:
                    existing = existing[:pre_idx].rstrip()
                else:
                    existing = existing[:idx].rstrip()
            
            with open(full_path, "w") as f:
                f.write(existing.rstrip() + "\n\n" + enrichment)
            enriched += 1
            print(f"  [ENRICH] Updated {db_path} (+{total_exploits} exploits from {len(file_groups)} categories)")
        else:
            content = generate_new_entry(file_groups[0])
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)
            new_created += 1
            print(f"  [NEW*] Created {db_path} (target didn't exist, {total_exploits} exploits)")
    
    print(f"\n{'='*60}")
    print(f"GENERATION SUMMARY")
    print(f"{'='*60}")
    print(f"New entries created:   {new_created}")
    print(f"Existing enriched:     {enriched}")
    if errors:
        print(f"Errors:                {len(errors)}")
        for err in errors:
            print(f"  - {err}")


if __name__ == "__main__":
    main()
