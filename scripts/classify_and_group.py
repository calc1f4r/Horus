#!/usr/bin/env python3
"""
Stage 2: DeFiHackLabs Classification & Grouping
=================================================
Normalizes raw vulnerability labels into DB categories, splits compound labels,
assigns sub-variant tags, routes to target DB files, and groups exploits by pattern.

Input:  scripts/output/defihacklabs_raw_index.json
Output: scripts/output/defihacklabs_classified.json
        scripts/output/coverage_report.json
        scripts/output/unmapped.json
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "scripts" / "output" / "defihacklabs_raw_index.json"
OUTPUT_FILE = BASE_DIR / "scripts" / "output" / "defihacklabs_classified.json"
COVERAGE_FILE = BASE_DIR / "scripts" / "output" / "coverage_report.json"
UNMAPPED_FILE = BASE_DIR / "scripts" / "output" / "unmapped.json"

# ─── Taxonomy: Raw Label → Normalized Category + Sub-variant ──────────────────

# Each rule: (regex_pattern, category, sub_variant_extractor_func_or_none)
# Order matters — first match wins for primary classification
TAXONOMY_RULES = [
    # Specific patterns first (before generic ones)
    (r"skim.*balance|skim\(\)", "skim-balance", None),
    (r"swap\s*metapool|metapool.*attack", "metapool-attack", None),
    (r"msg\.?value.*loop|msgvalue.*loop", "msgvalue-loop", None),
    (r"k\s*value|error\s*k\s*value|bad\s*[`'\"]?k[`'\"]?\s*value", "k-value-manipulation", None),
    (r"liquidity\s*migrat|v\d.*migrat", "liquidity-migration", None),
    (r"compiler|vyper.*bug", "compiler-bug", None),
    (r"phishing", "off-chain", None),
    (r"private\s*key\s*compromis|lost\s*keys", "off-chain", None),
    (r"accidentally\s*killed|selfdestruct|self-?destruct", "business-logic", lambda l: "selfdestruct"),
    (r"denial\s*of\s*service|^dos$", "dos", None),
    (r"subscription.*incentive", "business-logic", lambda l: "subscription_incentive"),
    (r"zero\s*fee", "fee-mechanism", lambda l: "zero_fee"),
    (r"fee\s*mech|fee.*exploit", "fee-mechanism", lambda l: "fee_mechanism"),
    (r"uninitialized\s*proxy", "initialization", lambda l: "uninitialized_proxy"),
    
    # Hyphenated labels (common in newer entries)
    (r"price[\s-]manipulation", "price-manipulation", lambda l: "generic"),
    (r"business[\s-]logic[\s-]flaw", "business-logic", lambda l: _classify_business_logic_subvariant(l)),
    (r"arbitrary[\s-](?:external[\s-])?call", "arbitrary-call", lambda l: "generic"),

    # Reentrancy variants
    (r"read[\s-]*only[\s-]*reentrancy", "reentrancy", lambda l: "read_only"),
    (r"cross[\s-]*contract[\s-]*reentrancy", "reentrancy", lambda l: "cross_contract"),
    (r"erc777[\s-]*reentrancy", "reentrancy", lambda l: "erc777_callback"),
    (r"erc667[\s-]*reentrancy", "reentrancy", lambda l: "erc667_callback"),
    (r"reentrancy.*sell\s*nft", "reentrancy", lambda l: "nft_sell_callback"),
    (r"reentrancy.*reward", "reentrancy", lambda l: "reward_manipulation"),
    (r"flashloan.*reentrancy|reentrancy.*flashloan|flash\s*loan.*reentrancy", "reentrancy", lambda l: "flash_loan_combined"),
    (r"reentrancy", "reentrancy", lambda l: "classic"),

    # Price manipulation variants
    (r"twap.*oracle.*manip|twap.*manip", "price-manipulation", lambda l: "twap_oracle"),
    (r"flash\s*loan.*price.*manip|flashloan.*price.*manip", "price-manipulation", lambda l: "flash_loan_price"),
    (r"share\s*price\s*manip", "price-manipulation", lambda l: "share_price"),
    (r"pair\s*(?:balance\s*)?manip|pair\s*manipulate", "price-manipulation", lambda l: "pair_balance"),
    (r"pool\s*manip", "price-manipulation", lambda l: "pool_manipulation"),
    (r"price[\s-]*cach|outdated.*(?:price|variable|global)", "stale-state", None),
    (r"flashloan.*oracle|oracle.*flashloan", "price-manipulation", lambda l: "flash_loan_oracle"),
    (r"manipulat.*price|price\s*manip|wrong\s*price|flawed\s*price|incorrect.*price", "price-manipulation", lambda l: "generic"),
    (r"price\s*oracle\s*manip", "price-manipulation", lambda l: "oracle_manipulation"),
    (r"price\s*manipulation", "price-manipulation", lambda l: "generic"),

    # Oracle issues (not manipulation)
    (r"faulty\s*oracle|bad\s*oracle|oracle\s*bad", "oracle-issues", lambda l: "faulty_oracle"),
    (r"price\s*out\s*of\s*date", "oracle-issues", lambda l: "stale_price"),
    (r"overpriced\s*asset", "oracle-issues", lambda l: "overpriced_asset"),
    (r"health\s*factor|bad\s*health", "oracle-issues", lambda l: "health_factor_check"),
    (r"vulnerable\s*price\s*depend", "oracle-issues", lambda l: "price_dependency"),

    # Access control variants
    (r"parameter\s*access\s*control", "access-control", lambda l: "parameter_access"),
    (r"custom\s*approval|unrestricted\s*approval", "access-control", lambda l: "approval_logic"),
    (r"unprotected\s*(?:public\s*)?function|public\s*internal\s*function", "access-control", lambda l: "unprotected_function"),
    (r"unauthorized\s*transfer", "access-control", lambda l: "unauthorized_transfer"),
    (r"lack.*access.*control|lack.*permission|access[\s-]*control|insufficient\s*access|broken\s*access|improper\s*access|incorrect\s*access|bad\s*access", "access-control", lambda l: "missing_access"),
    (r"access[\s-]control", "access-control", lambda l: "generic"),
    (r"permission\s*check|permission\s*control", "access-control", lambda l: "missing_permission"),
    (r"msg\.sender.*verif|address\s*verification", "access-control", lambda l: "sender_verification"),

    # Arbitrary call variants
    (r"arbitrary\s*yul\s*calldata", "arbitrary-call", lambda l: "yul_calldata"),
    (r"arbitrary.*address\s*spoofing", "arbitrary-call", lambda l: "address_spoofing"),
    (r"arbitrary\s*(?:external\s*)?call|arbitrary.*user\s*input|unverified\s*external\s*call", "arbitrary-call", lambda l: "generic"),
    (r"unchecked\s*external\s*call", "arbitrary-call", lambda l: "unchecked_external"),

    # Input validation variants
    (r"calldata\s*validation", "input-validation", lambda l: "calldata"),
    (r"(?:lack.*)?validation\s*pool", "input-validation", lambda l: "pool_validation"),
    (r"validation\s*(?:user)?data", "input-validation", lambda l: "userdata"),
    (r"lack.*validation.*dst|validation.*dst\s*address", "input-validation", lambda l: "dst_address"),
    (r"insufficient\s*token\s*validation", "input-validation", lambda l: "token_validation"),
    (r"incorrect\s*owner.*validation|owner\s*address\s*validation", "input-validation", lambda l: "owner_validation"),
    (r"no\s*input\s*(?:parameter\s*)?(?:check|validation)", "input-validation", lambda l: "no_input_check"),
    (r"unchecked\s*user\s*input", "input-validation", lambda l: "unchecked_user_input"),
    (r"wrong\s*(?:balance\s*)?check|wrong\s*visibility", "input-validation", lambda l: "wrong_check"),
    (r"insufficient\s*validation|incorrect\s*input|improper\s*input|input\s*validation|lack.*validation|lack\s*of\s*validation", "input-validation", lambda l: "generic"),
    (r"parameter\s*manipulation", "input-validation", lambda l: "parameter_manipulation"),

    # Precision / rounding
    (r"donate.*inflation.*rounding|inflation.*exchange.*rate.*rounding|rounding\s*error", "precision-loss", lambda l: "donation_inflation_rounding"),
    (r"div\s*precision|precision\s*loss|precission|loss\s*of\s*precision", "precision-loss", lambda l: "division_precision"),
    (r"integer\s*truncation", "precision-loss", lambda l: "integer_truncation"),
    (r"precision\s*truncation", "precision-loss", lambda l: "truncation"),

    # Integer overflow/underflow
    (r"unsafe\s*(?:math|cast)|unsafecast", "integer-overflow", lambda l: "unsafe_cast"),
    (r"integer\s*(?:overflow|underflow)|^overflow$|^underflow$", "integer-overflow", lambda l: "generic"),

    # Flash loan (standalone)
    (r"flashloan\s*attack|flash\s*loan\s*attack|flashloans\s*attack", "flash-loan", lambda l: "standalone"),
    (r"flashmint.*(?:error|receive)|flash\s*mint", "flash-loan", lambda l: "flash_mint"),
    (r"flash\s*loan\s*callback|verify\s*flashloan\s*callback", "flash-loan", lambda l: "callback_validation"),
    (r"flashloan$|flash\s*loan$", "flash-loan", lambda l: "standalone"),

    # Token compatibility variants
    (r"reflection\s*token|bad\s*reflection", "token-compatibility", lambda l: "reflection"),
    (r"deflationary\s*token|deflationary", "token-compatibility", lambda l: "deflationary"),
    (r"rebasing\s*logic|rebasing", "token-compatibility", lambda l: "rebasing"),
    (r"token\s*incompatible|protocol\s*token\s*incompatible", "token-compatibility", lambda l: "incompatible"),
    (r"self\s*transfer|transfer.*self|doubles.*transfer", "transfer-logic", None),

    # Reward / calculation
    (r"reward.*calcul(?:ation)?|incorrect\s*(?:reward|dividend)|dividend.*calcul|reward\s*distribution|reward\s*calculation\s*error", "reward-calculation", lambda l: "generic"),
    (r"claim\s*reward.*(?:without|no)\s*protect", "reward-calculation", lambda l: "unprotected_claim"),
    (r"instant\s*reward|unlocked\s*reward", "reward-calculation", lambda l: "instant_rewards"),
    (r"incorrect\s*calculation|miscalculation|calculation\s*issue", "calculation-errors", lambda l: "generic"),

    # Inflation attack
    (r"compound\s*v2.*inflation|compoundv2.*inflation", "inflation-attack", lambda l: "compound_v2"),
    (r"inflate\s*attack|inflation\s*attack|donate\s*inflation", "inflation-attack", lambda l: "donate_inflation"),

    # Signature
    (r"signature\s*malleab", "signature", lambda l: "malleability"),
    (r"signature\s*replay", "signature", lambda l: "replay"),
    (r"invalid.*signature|incorrect.*signature", "signature", lambda l: "invalid_verification"),

    # Slippage (with typo variant)
    (r"slippage\s*(?:protect|control|absent)|lack.*slippage|not\s*slippage|slippage\s*pro[ei]ction\s*absent", "slippage-protection", lambda l: "missing_slippage"),

    # Governance / DAO
    (r"malicious\s*proposal|dao.*flashloan|flashloan.*dao", "governance", lambda l: "malicious_proposal"),
    (r"^dao$|governance", "governance", lambda l: "generic"),

    # Bridge
    (r"bridge.*logic|bridge.*modifier|bridge.*cross.?chain", "bridge", lambda l: "logic_flaw"),
    (r"^bridge$|^bridges$", "bridge", lambda l: "generic"),

    # Storage collision
    (r"storage.*(?:collision|slot)|slot\d+\s*collision", "storage-collision", lambda l: "generic"),

    # Randomness
    (r"weak\s*random|weak\s*rng|predicting\s*random", "randomness", lambda l: "weak_rng"),

    # MEV / Sandwich
    (r"sandwich\s*ack|sandwich\s*attack|sandwich", "mev", lambda l: "sandwich"),

    # Rug pull
    (r"rug\s*pull|malicious.*(?:unlimited\s*)?mint(?:ing)?|rugged", "rug-pull", lambda l: "generic"),

    # Burn/mint logic
    (r"incorrect.*burn|free\s*mint|doesn.*burn|incorrect\s*(?:token\s*)?burn\s*(?:mechanism|logic|pair)", "burn-mint-logic", None),

    # Business logic (catch-all for various patterns)
    (r"business\s*logic|logic\s*flaw|logic\s*error|wrong\s*impl|bad\s*function|fault\s*logic", "business-logic", lambda l: _classify_business_logic_subvariant(l)),
    (r"scaledbalanceof|balance\s*recalcul", "business-logic", lambda l: "balance_recalculation"),
    (r"insolvency|post\s*insolvency|bypassed\s*insolvency", "business-logic", lambda l: "insolvency_bypass"),
    (r"incorrect\s*logic|incorrect\s*handling|fault\s*logic", "business-logic", lambda l: "generic"),
    (r"wrong\s*approval|unverified\s*contract", "business-logic", lambda l: "approval_logic"),

    # Miscellaneous
    (r"misconfiguration", "misconfiguration", None),
    (r"fake\s*market", "business-logic", lambda l: "fake_market"),
    (r"v3\s*migrator|migrator\s*exploit", "liquidity-migration", None),
    (r"any\s*token.*destroy", "business-logic", lambda l: "token_destruction"),
    (r"infinite.*loan|infinite.*borrow", "business-logic", lambda l: "infinite_loans"),
    (r"token\s*migrate\s*flaw", "business-logic", lambda l: "token_migration"),
    (r"arbitrage|economic\s*design", "arbitrage", None),
    (r"yield\s*protocol\s*flaw", "yield-strategy", None),
    (r"nft.*marketplace|optimism.*nft", "nft-specific", None),

    # Catch remaining variations and typos
    (r"arbitary\s*(?:external\s*)?call", "arbitrary-call", lambda l: "generic"),  # typo: arbitary
    (r"manipulation\s*of\s*funds|manipulat.*asset|manipulat.*amount", "price-manipulation", lambda l: "generic"),
    (r"public\s*function\s*call|public\s*functioncall", "access-control", lambda l: "unprotected_function"),
    (r"incorrect\s*transfer|incorrect\s*recipient", "transfer-logic", None),
    (r"incorrect\s*parameter\s*setting", "input-validation", lambda l: "parameter_setting"),
    (r"invalid\s*emergency\s*withdraw|emergency\s*withdraw", "business-logic", lambda l: "emergency_withdraw"),
    (r"swap\s*eth.*btc.*mint|swap.*1[/:]1\s*in\s*mint", "business-logic", lambda l: "incorrect_swap_logic"),
    (r"wintermute", "off-chain", None),  # Wintermute was a key compromise
    (r"mathematical\s*flaw", "calculation-errors", lambda l: "mathematical_flaw"),
    (r"^bridge[,:]?\s", "bridge", lambda l: "logic_flaw"),
    (r"^bridge$", "bridge", lambda l: "generic"),
    (r"malicious\s*proposal\s*mint|malicious\s*proposal", "governance", lambda l: "malicious_proposal"),
    (r"vulnerable\s*emergency", "business-logic", lambda l: "emergency_withdraw"),
    (r"minting", "business-logic", lambda l: "incorrect_burn_mint"),
    (r"instant\s*reward|unlocked\s*reward|reward.*unlocked|^unlocked$", "reward-calculation", lambda l: "instant_rewards"),
    (r"transfer\s*ownership", "access-control", lambda l: "ownership_transfer"),
    (r"getting\s*around\s*modifier|cross[\s-]*chain\s*message", "bridge", lambda l: "modifier_bypass"),
]


def _classify_business_logic_subvariant(label: str) -> str:
    """Further classify a 'business logic' label by inspecting the full heading context."""
    label_lower = label.lower()
    if any(kw in label_lower for kw in ["burn", "mint"]):
        return "incorrect_burn_mint"
    if any(kw in label_lower for kw in ["insolvency", "health"]):
        return "insolvency_bypass"
    if any(kw in label_lower for kw in ["transfer", "self"]):
        return "transfer_logic"
    if any(kw in label_lower for kw in ["reward", "claim"]):
        return "reward_logic"
    if any(kw in label_lower for kw in ["pair", "sync"]):
        return "pair_manipulation"
    if any(kw in label_lower for kw in ["emergency"]):
        return "emergency_withdraw"
    return "generic"


# ─── Compound Label Splitter ─────────────────────────────────────────────────

COMPOUND_SEPARATORS = re.compile(
    r"\s*(?:&&|\s&\s|\s\+\s|,\s*(?:and\s+)?)\s*", re.IGNORECASE
)

# Special compound patterns that need custom splitting
SPECIAL_COMPOUND_PATTERNS = [
    # "Flashloans & Price Manipulation" → ["flash-loan", "price-manipulation"]
    (re.compile(r"flashloans?\s*&\s*price\s*manip", re.IGNORECASE),
     ["Flashloan attack", "Price Manipulation"]),
    # "(I) X (II) Y" → split on (II)
    (re.compile(r"\(I\)\s*(.*?)\s*\(II\)\s*(.*)", re.IGNORECASE),
     None),  # dynamic split
    # "Business Logic Flaw : description" → use the prefix
    (re.compile(r"^(Business\s*Logic\s*Flaw)\s*:\s*", re.IGNORECASE),
     None),  # dynamic prefix extraction
    # "Mathematical flaw + Reentrancy"
    (re.compile(r"mathematical\s*flaw\s*\+\s*reentrancy", re.IGNORECASE),
     ["Incorrect Calculation", "Reentrancy"]),
]


def split_compound_label(label: str) -> list[str]:
    """Split compound labels like 'Reentrancy && Business Logic Flaw' into parts."""
    # Check special patterns first
    for pat, replacement in SPECIAL_COMPOUND_PATTERNS:
        m = pat.search(label)
        if m:
            if replacement is not None:
                return replacement
            # Dynamic patterns
            if "(I)" in label.upper():
                groups = m.groups()
                return [g.strip() for g in groups if g and g.strip()]
            if ":" in label:
                # "Business Logic Flaw : detailed description" → just the prefix
                return [m.group(1).strip()]

    parts = COMPOUND_SEPARATORS.split(label)
    return [p.strip() for p in parts if p.strip()]


# ─── Category → DB Path Mapping ──────────────────────────────────────────────

CATEGORY_TO_DB_PATH = {
    "reentrancy": "DB/general/reentrancy/defi-reentrancy-patterns.md",
    "access-control": "DB/general/access-control/access-control-vulnerabilities.md",
    "arbitrary-call": "DB/general/arbitrary-call/arbitrary-external-call-vulnerabilities.md",
    "business-logic": "DB/general/business-logic/defi-business-logic-flaws.md",
    "price-manipulation": "DB/oracle/price-manipulation/flash-loan-oracle-manipulation.md",
    "precision-loss": "DB/general/precision/precision-loss-rounding-vulnerabilities.md",
    "integer-overflow": "DB/general/integer-overflow/integer-overflow-vulnerabilities.md",
    "flash-loan": "DB/general/flash-loan/flash-loan-attack-patterns.md",
    "token-compatibility": "DB/general/token-compatibility/non-standard-token-vulnerabilities.md",
    "slippage-protection": "DB/general/slippage-protection/slippage-protection.md",
    "reward-calculation": "DB/general/calculation/incorrect-calculation-vulnerabilities.md",
    "calculation-errors": "DB/general/calculation/incorrect-calculation-vulnerabilities.md",
    "inflation-attack": "DB/general/vault-inflation-attack/vault-inflation-attack.md",
    "oracle-issues": "DB/oracle/price-manipulation/flash-loan-oracle-manipulation.md",
    "signature": "DB/general/signature/signature-verification-vulnerabilities.md",
    "governance": "DB/general/dao-governance-vulnerabilities/governance-takeover.md",
    "bridge": "DB/bridge/custom/cross-chain-general-vulnerabilities.md",
    "storage-collision": "DB/general/storage-collision/storage-collision-vulnerabilities.md",
    "randomness": "DB/general/randomness/weak-randomness-vulnerabilities.md",
    "mev": "DB/general/mev-bot/mev-bot-vulnerabilities.md",
    "rug-pull": "DB/general/malicious/rug-pull-detection-patterns.md",
    "initialization": "DB/general/initialization/initialization-vulnerabilities.md",
    "yield-strategy": "DB/general/yield-strategy-vulnerabilities/yield-strategy-vulnerabilities.md",
    "misconfiguration": "DB/general/business-logic/defi-business-logic-flaws.md",

    # Gap entries → create new
    "input-validation": "DB/general/missing-validations/defihacklabs-input-validation-patterns.md",
    "skim-balance": "DB/unique/defihacklabs/skim-balance-attack.md",
    "metapool-attack": "DB/unique/defihacklabs/swap-metapool-attack.md",
    "liquidity-migration": "DB/unique/defihacklabs/liquidity-migration-exploit.md",
    "msgvalue-loop": "DB/unique/defihacklabs/msgvalue-in-loop.md",
    "arbitrage": "DB/unique/defihacklabs/economic-arbitrage-design-flaws.md",
    "nft-specific": "DB/unique/defihacklabs/nft-specific-exploit-patterns.md",
    "stale-state": "DB/unique/defihacklabs/stale-cached-state-exploits.md",
    "fee-mechanism": "DB/unique/defihacklabs/fee-mechanism-exploitation.md",
    "k-value-manipulation": "DB/amm/constantproduct/CONSTANT_PRODUCT_AMM_VULNERABILITIES.md",
    "compiler-bug": "DB/unique/defihacklabs/compiler-level-vulnerabilities.md",
    "burn-mint-logic": "DB/general/business-logic/defi-business-logic-flaws.md",
    "transfer-logic": "DB/general/business-logic/defi-business-logic-flaws.md",
    "dos": "DB/general/business-logic/defi-business-logic-flaws.md",

    # Off-chain (phishing, key compromise) - document but don't create DB entries
    "off-chain": None,
}

# Categories that need NEW entries (gaps in existing DB)
NEW_ENTRY_CATEGORIES = {
    "input-validation",
    "skim-balance",
    "metapool-attack",
    "liquidity-migration",
    "msgvalue-loop",
    "arbitrage",
    "nft-specific",
    "stale-state",
    "fee-mechanism",
    "compiler-bug",
}

# Categories where entries should ENRICH existing files
ENRICH_CATEGORIES = set(CATEGORY_TO_DB_PATH.keys()) - NEW_ENTRY_CATEGORIES - {"off-chain"}


def classify_entry(entry: dict) -> list[dict]:
    """
    Classify an exploit entry. Returns list of classification dicts
    (multiple if compound label is split).
    """
    raw_label = entry.get("raw_vuln_label", "")
    classifications = []

    # Split compound labels
    parts = split_compound_label(raw_label)

    for part in parts:
        category, sub_variant = _match_taxonomy(part, raw_label)
        action = _determine_action(category)
        db_path = CATEGORY_TO_DB_PATH.get(category)

        classifications.append({
            "category": category,
            "sub_variant": sub_variant,
            "action": action,
            "db_target_path": db_path,
            "matched_label_part": part,
        })

    return classifications


def _match_taxonomy(label_part: str, full_label: str) -> tuple[str, Optional[str]]:
    """Match a label part against taxonomy rules."""
    for pattern, category, subvariant_fn in TAXONOMY_RULES:
        if re.search(pattern, label_part, re.IGNORECASE):
            sub_variant = None
            if subvariant_fn:
                sub_variant = subvariant_fn(full_label)
            return category, sub_variant

    # Fallback: unclassified
    return "unclassified", None


def _determine_action(category: str) -> str:
    """Determine whether to enrich existing entry or create new."""
    if category in NEW_ENTRY_CATEGORIES:
        return "create_new"
    elif category == "off-chain":
        return "skip"
    elif category == "unclassified":
        return "review"
    else:
        return "enrich"


# ─── Main Pipeline ────────────────────────────────────────────────────────────

def main():
    # Load raw index
    if not INPUT_FILE.exists():
        print(f"[!] Input file not found: {INPUT_FILE}")
        print(f"    Run extract_defihacklabs.py first.")
        return

    with open(INPUT_FILE, "r") as f:
        entries = json.load(f)

    print(f"[*] Loaded {len(entries)} entries from raw index")

    # Classify all entries
    groups = defaultdict(lambda: {
        "category": None,
        "db_target_path": None,
        "action": None,
        "sub_variants": defaultdict(list),
        "total_exploits": 0,
        "total_loss_usd": 0.0,
    })

    unclassified = []
    off_chain = []
    compound_dual_routed = []

    for entry in entries:
        classifications = classify_entry(entry)

        if len(classifications) > 1:
            compound_dual_routed.append({
                "id": entry["id"],
                "protocol": entry["protocol"],
                "raw_label": entry["raw_vuln_label"],
                "categories": [c["category"] for c in classifications],
            })

        for cls in classifications:
            cat = cls["category"]

            if cat == "unclassified":
                unclassified.append({
                    "id": entry["id"],
                    "protocol": entry["protocol"],
                    "raw_label": entry["raw_vuln_label"],
                    "date": entry["date"],
                })
                continue

            if cls["action"] == "skip":
                off_chain.append({
                    "id": entry["id"],
                    "protocol": entry["protocol"],
                    "raw_label": entry["raw_vuln_label"],
                })
                continue

            group = groups[cat]
            group["category"] = cat
            group["db_target_path"] = cls["db_target_path"]
            group["action"] = cls["action"]
            group["total_exploits"] += 1
            group["total_loss_usd"] += entry.get("loss_usd_estimate", 0)

            sub_var = cls["sub_variant"] or "generic"
            group["sub_variants"][sub_var].append({
                "id": entry["id"],
                "date": entry["date"],
                "protocol": entry["protocol"],
                "raw_label": entry["raw_vuln_label"],
                "loss_amount": entry.get("loss_amount"),
                "loss_usd_estimate": entry.get("loss_usd_estimate", 0),
                "chain": entry.get("chain"),
                "poc_resolved_path": entry.get("poc_resolved_path"),
                "attack_tx": entry.get("attack_tx"),
                "reference_links": entry.get("reference_links", []),
                "post_mortem_links": entry.get("post_mortem_links", []),
            })

    # Convert to serializable format
    groups_list = []
    for cat, group_data in sorted(groups.items(), key=lambda x: -x[1]["total_loss_usd"]):
        sub_variants_serial = {}
        for sv_name, sv_entries in group_data["sub_variants"].items():
            # Sort by loss within each sub-variant
            sv_entries.sort(key=lambda e: e["loss_usd_estimate"], reverse=True)
            sub_variants_serial[sv_name] = sv_entries

        groups_list.append({
            "category": group_data["category"],
            "db_target_path": group_data["db_target_path"],
            "action": group_data["action"],
            "total_exploits": group_data["total_exploits"],
            "total_loss_usd": round(group_data["total_loss_usd"], 2),
            "sub_variant_count": len(sub_variants_serial),
            "sub_variants": sub_variants_serial,
        })

    # Write classified output
    output = {
        "metadata": {
            "total_entries": len(entries),
            "classified_entries": sum(g["total_exploits"] for g in groups_list),
            "unclassified_count": len(unclassified),
            "off_chain_count": len(off_chain),
            "compound_dual_routed": len(compound_dual_routed),
            "category_count": len(groups_list),
            "new_entry_categories": len([g for g in groups_list if g["action"] == "create_new"]),
            "enrich_categories": len([g for g in groups_list if g["action"] == "enrich"]),
        },
        "groups": groups_list,
        "compound_exploits": compound_dual_routed,
        "off_chain": off_chain,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"[✓] Wrote classified data to {OUTPUT_FILE}")

    # Write unmapped
    with open(UNMAPPED_FILE, "w") as f:
        json.dump(unclassified, f, indent=2, ensure_ascii=False)
    print(f"[✓] Wrote {len(unclassified)} unmapped entries to {UNMAPPED_FILE}")

    # Write coverage report
    total = len(entries)
    classified = sum(g["total_exploits"] for g in groups_list)
    coverage_pct = (classified / total * 100) if total > 0 else 0

    coverage = {
        "total_exploits": total,
        "classified": classified,
        "unclassified": len(unclassified),
        "off_chain_skipped": len(off_chain),
        "compound_dual_routed": len(compound_dual_routed),
        "coverage_percentage": round(coverage_pct, 1),
        "new_entries_to_create": len([g for g in groups_list if g["action"] == "create_new"]),
        "existing_entries_to_enrich": len([g for g in groups_list if g["action"] == "enrich"]),
        "by_category": {},
    }

    for group in groups_list:
        cat = group["category"]
        coverage["by_category"][cat] = {
            "exploits": group["total_exploits"],
            "sub_variants": group["sub_variant_count"],
            "total_loss_usd": group["total_loss_usd"],
            "action": group["action"],
            "db_target": group["db_target_path"],
        }

    with open(COVERAGE_FILE, "w") as f:
        json.dump(coverage, f, indent=2, ensure_ascii=False)
    print(f"[✓] Wrote coverage report to {COVERAGE_FILE}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"CLASSIFICATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total entries:        {total}")
    print(f"Classified:           {classified} ({coverage_pct:.1f}%)")
    print(f"Unclassified:         {len(unclassified)}")
    print(f"Off-chain (skipped):  {len(off_chain)}")
    print(f"Compound (dual):      {len(compound_dual_routed)}")
    print(f"Categories:           {len(groups_list)}")
    print(f"  - Enrich existing:  {len([g for g in groups_list if g['action'] == 'enrich'])}")
    print(f"  - Create new:       {len([g for g in groups_list if g['action'] == 'create_new'])}")

    print(f"\n{'='*60}")
    print(f"GROUPS BY CATEGORY (sorted by total loss)")
    print(f"{'='*60}")
    for g in groups_list:
        action_tag = "NEW" if g["action"] == "create_new" else "ENRICH"
        loss_str = f"${g['total_loss_usd']:,.0f}" if g["total_loss_usd"] > 0 else "$0"
        print(f"  [{action_tag:7s}] {g['category']:25s} | {g['total_exploits']:3d} exploits | {g['sub_variant_count']:2d} sub-variants | {loss_str}")

    if unclassified:
        print(f"\n{'='*60}")
        print(f"UNCLASSIFIED ENTRIES ({len(unclassified)})")
        print(f"{'='*60}")
        for u in unclassified[:20]:
            print(f"  {u['date']} {u['protocol']}: {u['raw_label']}")
        if len(unclassified) > 20:
            print(f"  ... and {len(unclassified) - 20} more")


if __name__ == "__main__":
    main()
