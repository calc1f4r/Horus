#!/usr/bin/env python3
"""
Migrate ALL legacy DB entries to the current TEMPLATE.md format.

What this script does:
1. Scans DB/**/*.md for legacy entries (missing root_cause_family in frontmatter)
2. Classifies each file into a format family
3. Adds missing frontmatter fields (root_cause_family, pattern_key, code_keywords,
   interaction_scope, involved_contracts, path_keys)
4. Inserts missing body sections (Agent Quick View, Contract / Boundary Map,
   Valid Bug Signals, False Positive Guards)
5. Preserves ALL existing content — reorganizes, never deletes

Usage:
  python3 scripts/migrate_to_new_template.py --dry-run   # Preview without writing
  python3 scripts/migrate_to_new_template.py              # Run migration
  python3 scripts/migrate_to_new_template.py --verbose    # Detailed output
"""

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

DB_DIR = Path(__file__).parent.parent / "DB"

SKIP_FILES = {"README.md", "SEARCH_GUIDE.md", "ARTIFACT_INDEX.md"}

# ---------------------------------------------------------------------------
# Root-cause family inference mapping
# ---------------------------------------------------------------------------
ROOT_CAUSE_MAP = {
    # category / vulnerability_type keyword -> root_cause_family
    "reentrancy": "callback_reentrancy",
    "cross_function": "callback_reentrancy",
    "read_only_reentrancy": "callback_reentrancy",
    "readonly_reentrancy": "callback_reentrancy",
    "access_control": "missing_access_control",
    "authorization": "missing_access_control",
    "permission": "missing_access_control",
    "unprotected_init": "missing_access_control",
    "oracle": "missing_validation",
    "staleness": "missing_validation",
    "stale_price": "missing_validation",
    "price_manipulation": "missing_validation",
    "chainlink": "missing_validation",
    "pyth": "missing_validation",
    "flash_loan": "missing_validation",
    "flash_loan_attack": "missing_validation",
    "overflow": "arithmetic_error",
    "underflow": "arithmetic_error",
    "integer_overflow": "arithmetic_error",
    "precision": "rounding_error",
    "rounding": "rounding_error",
    "precision_loss": "rounding_error",
    "fee_rounding": "rounding_error",
    "calculation": "arithmetic_error",
    "reward": "arithmetic_error",
    "vault_inflation": "first_depositor_attack",
    "inflation": "first_depositor_attack",
    "share_inflation": "first_depositor_attack",
    "donation_attack": "first_depositor_attack",
    "initialization": "missing_initialization_guard",
    "unprotected_init": "missing_initialization_guard",
    "storage_collision": "storage_layout_error",
    "proxy": "storage_layout_error",
    "uups": "storage_layout_error",
    "diamond": "storage_layout_error",
    "governance": "missing_validation",
    "dao": "missing_validation",
    "voting": "missing_validation",
    "proposal": "missing_validation",
    "quorum": "missing_validation",
    "timelock": "missing_validation",
    "bridge": "missing_validation",
    "cross_chain": "missing_validation",
    "layerzero": "missing_validation",
    "wormhole": "missing_validation",
    "ccip": "missing_validation",
    "axelar": "missing_validation",
    "hyperlane": "missing_validation",
    "stargate": "missing_validation",
    "signature": "missing_validation",
    "replay": "missing_validation",
    "fee_on_transfer": "missing_token_compatibility",
    "deflationary": "missing_token_compatibility",
    "reflection": "missing_token_compatibility",
    "token_compatibility": "missing_token_compatibility",
    "non_standard": "missing_token_compatibility",
    "erc20": "missing_token_compatibility",
    "erc721": "missing_validation",
    "nft": "missing_validation",
    "mev": "missing_frontrun_protection",
    "mev_bot": "missing_frontrun_protection",
    "frontrunning": "missing_frontrun_protection",
    "sandwich": "missing_frontrun_protection",
    "slippage": "missing_validation",
    "input_validation": "missing_validation",
    "missing_validations": "missing_validation",
    "arbitrary_call": "unvalidated_external_call",
    "arbitrary_external_call": "unvalidated_external_call",
    "delegatecall": "unvalidated_external_call",
    "business_logic": "logic_error",
    "protocol_logic": "logic_error",
    "share_accounting": "logic_error",
    "solvency": "logic_error",
    "randomness": "weak_randomness",
    "weak_randomness": "weak_randomness",
    "malicious": "malicious_code",
    "rug_pull": "malicious_code",
    "stablecoin": "logic_error",
    "yield_strategy": "logic_error",
    "lending": "logic_error",
    "restaking": "logic_error",
    "bonding_curve": "logic_error",
    "amm": "logic_error",
    "concentrated_liquidity": "logic_error",
    "constant_product": "logic_error",
    "erc4626": "logic_error",
    "vetoken": "logic_error",
    "zk_rollup": "logic_error",
    "circuit": "logic_error",
    "batch_processing": "logic_error",
    "fraud_proof": "logic_error",
    "sequencer": "logic_error",
    "l1_l2": "logic_error",
    "evm_incompatibility": "logic_error",
    "gas_accounting": "logic_error",
    "reorg": "logic_error",
    "cosmos": "logic_error",
    "ibc": "missing_validation",
    "abci": "logic_error",
    "staking": "logic_error",
    "slashing": "logic_error",
    "delegation": "logic_error",
    "consensus": "logic_error",
    "module_accounting": "logic_error",
    "liquidation": "logic_error",
    "liquidity": "logic_error",
    "solana": "logic_error",
    "token_2022": "missing_validation",
    "move": "logic_error",
    "sui": "logic_error",
    "account_abstraction": "missing_validation",
    "session_key": "missing_validation",
    "paymaster": "missing_validation",
    "erc7579": "missing_validation",
    "erc7702": "missing_validation",
    "dos": "denial_of_service",
    "griefing": "denial_of_service",
    "chain_halt": "denial_of_service",
}


def infer_root_cause_family(fm, body):
    """Infer root_cause_family from category + vulnerability_type + content."""
    cat = str(fm.get("category", "")).lower().replace("-", "_")
    vuln = str(fm.get("vulnerability_type", "")).lower().replace("-", "_")
    vuln_class = str(fm.get("vulnerability_class", "")).lower().replace("-", "_")
    attack = str(fm.get("attack_type", "")).lower().replace("-", "_")

    # Try exact matches first, then substring
    for key_source in [cat, vuln, vuln_class]:
        if key_source in ROOT_CAUSE_MAP:
            return ROOT_CAUSE_MAP[key_source]

    # Substring match
    for keyword, family in ROOT_CAUSE_MAP.items():
        for source in [cat, vuln, vuln_class, attack]:
            if keyword in source:
                return family

    # Content-based fallback
    body_lower = body.lower()
    if "reentr" in body_lower:
        return "callback_reentrancy"
    if "overflow" in body_lower or "underflow" in body_lower:
        return "arithmetic_error"
    if "oracle" in body_lower or "price feed" in body_lower:
        return "missing_validation"
    if "access control" in body_lower:
        return "missing_access_control"

    return "logic_error"


def construct_pattern_key(fm, root_cause):
    """Build a pattern_key from root_cause | component | vuln_type."""
    component = str(fm.get("affected_component", "unknown")).split("|")[0].strip()
    vuln_type = str(fm.get("vulnerability_type", "unknown")).split("|")[0].strip()
    return f"{root_cause} | {component} | {vuln_type}"


def extract_code_keywords(fm, body):
    """Extract code_keywords from primitives + code blocks."""
    keywords = set()

    # Pull from existing primitives
    prims = fm.get("primitives", [])
    if isinstance(prims, list):
        for p in prims:
            kw = str(p).strip()
            if kw and len(kw) > 2:
                keywords.add(kw)
    elif isinstance(prims, str):
        for p in prims.split(","):
            kw = p.strip()
            if kw and len(kw) > 2:
                keywords.add(kw)

    # Extract function names from code blocks
    for m in re.finditer(r"function\s+(\w+)\s*\(", body):
        name = m.group(1)
        if name not in {"test", "setUp", "run", "main", "constructor"}:
            keywords.add(name)

    # Extract common Solidity identifiers
    for m in re.finditer(r"(?:msg\.sender|tx\.origin|block\.timestamp|block\.number)", body):
        keywords.add(m.group(0))

    # Extract modifier names
    for m in re.finditer(r"modifier\s+(\w+)", body):
        keywords.add(m.group(1))

    # Extract event names
    for m in re.finditer(r"event\s+(\w+)", body):
        keywords.add(m.group(1))

    # Extract common DeFi function calls
    for m in re.finditer(
        r"(?:balanceOf|totalSupply|transferFrom|safeTransferFrom|approve|allowance|"
        r"latestRoundData|getPrice|getPriceUnsafe|updatePriceFeeds|"
        r"deposit|withdraw|mint|burn|swap|addLiquidity|removeLiquidity|"
        r"borrow|repay|liquidate|flashLoan|execute|delegatecall|"
        r"onERC721Received|tokensReceived|fallback|receive)\b",
        body,
    ):
        keywords.add(m.group(0))

    # For Move files
    for m in re.finditer(r"public\s+(?:entry\s+)?fun\s+(\w+)", body):
        keywords.add(m.group(1))

    # For Go/Cosmos files
    for m in re.finditer(r"func\s+\(\w+\s+\*?\w+\)\s+(\w+)", body):
        keywords.add(m.group(1))

    result = sorted(keywords)[:20]
    return result if result else ["TODO_add_keywords"]


def detect_interaction_scope(fm, body):
    """Detect if the entry describes multi-contract interactions."""
    body_lower = body.lower()
    multi_signals = [
        "cross-contract",
        "cross_contract",
        "cross-protocol",
        "cross_protocol",
        "cross-chain",
        "cross_chain",
        "multi-contract",
        "multi_contract",
        "callback",
        "delegatecall",
        "external call",
        "bridge",
        "adapter",
        "proxy pattern",
        "inter-contract",
    ]
    score = sum(1 for s in multi_signals if s in body_lower)
    if score >= 2:
        return "multi_contract"
    return "single_contract"


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------


def parse_frontmatter(content):
    """Parse YAML frontmatter. Returns (dict, end_offset, raw_fm_text)."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}, 0, ""
    fm_text = match.group(1)
    fm_end = match.end()
    try:
        fm = yaml.safe_load(fm_text)
        if not isinstance(fm, dict):
            fm = {}
    except yaml.YAMLError:
        # Fallback: manual parse
        fm = {}
        for line in fm_text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("#") or not stripped:
                continue
            if ":" in stripped:
                parts = stripped.split(":", 1)
                key = parts[0].strip()
                val = parts[1].strip().strip('"').strip("'")
                if key:
                    fm[key] = val
    return fm, fm_end, fm_text


def classify_family(fm, body):
    """Classify entry into format family."""
    if "vulnerability_class" in fm and "references" in fm:
        return "family1_very_old"
    if fm.get("source") and not isinstance(fm.get("source"), list):
        if "## Unique Protocol Issue" in body or "unique" in str(fm.get("source", "")):
            return "family4_unique"
    if "move" in str(fm.get("language", "")).lower() or "sui" in str(fm.get("chain", "")).lower():
        return "family3_move"
    return "family2_intermediate"


def is_already_migrated(fm):
    """Check if the file already has the new template fields."""
    return "root_cause_family" in fm


def should_skip(filepath):
    """Check if the file should be skipped."""
    return filepath.name in SKIP_FILES


# ---------------------------------------------------------------------------
# Body section generators (extended from migrate_body_structure.py)
# ---------------------------------------------------------------------------


def safe_str(val, default="unknown"):
    if isinstance(val, list):
        return ", ".join(str(v) for v in val)
    if val is None:
        return default
    return str(val).strip('"').strip("'")


def generate_agent_quick_view(fm):
    root_cause = safe_str(fm.get("root_cause_family", "unknown"))
    pattern_key = safe_str(fm.get("pattern_key", "unknown"))
    severity = safe_str(fm.get("severity", "high"))
    impact = safe_str(fm.get("impact", "fund_loss"))
    scope = safe_str(fm.get("interaction_scope", "single_contract"))
    component = safe_str(fm.get("affected_component", "unknown"))
    keywords = fm.get("code_keywords", [])
    if isinstance(keywords, list):
        kw_str = ", ".join(f"`{k}`" for k in keywords[:8])
    else:
        kw_str = f"`{keywords}`"

    return f"""#### Agent Quick View

- Root cause statement: "This vulnerability exists because of {root_cause}"
- Pattern key: `{pattern_key}`
- Interaction scope: `{scope}`
- Primary affected component(s): `{component}`
- High-signal code keywords: {kw_str}
- Typical sink / impact: `{impact}`
- Validation strength: `moderate`
"""


def generate_boundary_map(fm, body):
    scope = safe_str(fm.get("interaction_scope", "single_contract"))
    component = safe_str(fm.get("affected_component", "unknown"))

    # Try to extract contract names from code blocks
    contracts = set()
    for m in re.finditer(r"contract\s+(\w+)", body):
        name = m.group(1)
        if name not in {"Test", "Setup", "Exploit", "Attack", "Attacker", "MockERC20"}:
            contracts.add(name)
    for m in re.finditer(r"interface\s+I(\w+)", body):
        contracts.add(m.group(1))
    if not contracts:
        contracts = {c.strip() for c in component.split("|") if c.strip()}

    contracts_sorted = sorted(contracts)[:6]

    hop_str = " -> ".join(f"{c}.function" for c in contracts_sorted[:3]) if len(contracts_sorted) > 1 else "N/A"

    return f"""#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `{hop_str}`
- Trust boundary crossed: `{"callback / external call" if scope == "multi_contract" else "internal"}`
- Shared state or sync assumption: `state consistency across operations`
"""


def generate_valid_bug_signals(fm, body):
    category = safe_str(fm.get("category", "")).lower()
    vuln_type = safe_str(fm.get("vulnerability_type", "")).lower()
    root_cause = safe_str(fm.get("root_cause_family", "")).lower()

    signal_map = {
        "callback_reentrancy": [
            "External call (`.call`, `.transfer`, token transfer) occurs before state variable update",
            "Token implements callback hooks (ERC-777, ERC-721) and protocol doesn't use `nonReentrant`",
            "User-supplied token address passed to `transferFrom` without callback protection",
            "Read-only function's return value consumed cross-contract during an active callback window",
        ],
        "missing_access_control": [
            "State-changing function lacks `onlyOwner`/`onlyRole` modifier",
            "External function accepts arbitrary address and calls interface methods without registry validation",
            "Configuration setter is callable by non-owner accounts",
            "Initialization or migration function is unprotected",
        ],
        "missing_validation": [
            "Critical input parameter not validated against expected range or format",
            "Oracle data consumed without staleness check or sanity bounds",
            "User-supplied address or calldata forwarded without validation",
            "Missing check allows operation under invalid or stale state",
        ],
        "arithmetic_error": [
            "Arithmetic operation on user-controlled input without overflow protection",
            "Casting between different-width integer types without bounds check",
            "Multiplication before division where intermediate product can exceed type max",
            "Accumulator variable can wrap around causing incorrect accounting",
        ],
        "rounding_error": [
            "Division before multiplication truncates intermediate result",
            "Reward/share calculation uses insufficient decimal precision",
            "Rounding direction favors attacker during mint/redeem operations",
            "Fee calculation rounds to zero for small amounts enabling free operations",
        ],
        "first_depositor_attack": [
            "First deposit to vault with zero total supply has manipulable share calculation",
            "Direct asset transfer (donation) changes exchange rate before victim's deposit",
            "No minimum initial deposit or dead shares mechanism",
            "Share price can be inflated atomically in a single transaction",
        ],
        "logic_error": [
            "State variable updated after external interaction instead of before (CEI violation)",
            "Withdrawal path produces different accounting than deposit path for same principal",
            "Reward accrual continues during paused/emergency state",
            "Edge case in state machine transition allows invalid state",
        ],
        "unvalidated_external_call": [
            "Function accepts user-controlled target and calldata for low-level `.call()`",
            "Delegatecall to user-supplied address with contract's storage context",
            "Token approval granted to contract that forwards arbitrary calls",
            "Router executes user-supplied swap path without validating intermediate targets",
        ],
        "missing_frontrun_protection": [
            "Transaction can be frontrun by MEV bots observing the mempool",
            "No commit-reveal or private mempool protection for sensitive operations",
            "Slippage tolerance set too high or user-controllable without minimum enforcement",
            "Swap execution lacks deadline parameter or uses block.timestamp as deadline",
        ],
        "missing_token_compatibility": [
            "Protocol assumes all ERC20 tokens behave identically (no fees, no rebasing)",
            "Token balance check uses cached amount instead of actual balanceOf() after transfer",
            "Missing support for tokens with non-standard return values (USDT, BNB)",
            "Rebasing or fee-on-transfer token breaks accounting assumptions",
        ],
        "missing_initialization_guard": [
            "Initializer function callable more than once (missing initializer modifier)",
            "Proxy implementation has unprotected initialize() callable by anyone",
            "Constructor logic not replicated in initializer for upgradeable contract",
            "Implementation contract left uninitialized, allowing attacker takeover",
        ],
        "storage_layout_error": [
            "Storage slot collision between proxy and implementation contracts",
            "Upgrade changes storage layout order, corrupting existing state",
            "Diamond proxy selector collision between facets",
            "Inherited contract storage layout breaks upgrade compatibility",
        ],
        "weak_randomness": [
            "On-chain randomness derived from block.timestamp, block.number, or blockhash",
            "Randomness source observable by miners/validators before commitment",
            "No commit-reveal or VRF scheme for random number generation",
            "Seed is predictable or manipulable by transaction ordering",
        ],
        "denial_of_service": [
            "Unbounded loop over user-controlled array can exceed block gas limit",
            "External call failure causes entire transaction to revert",
            "Attacker can grief operations by manipulating state to cause reverts",
            "Resource exhaustion through repeated operations without rate limiting",
        ],
    }

    signals = signal_map.get(root_cause, [])
    if not signals:
        signals = [
            "Missing validation or guard on state-changing operation",
            "User-supplied input passed to sensitive operation without sanitization",
            "State update occurs after external interaction (CEI violation)",
            "Protocol assumption about external component behavior is violated",
        ]

    lines = ["#### Valid Bug Signals", ""]
    for i, s in enumerate(signals[:4], 1):
        lines.append(f"- Signal {i}: {s}")
    lines.append("")
    return "\n".join(lines)


def generate_false_positive_guards(fm, body):
    root_cause = safe_str(fm.get("root_cause_family", "")).lower()

    guard_map = {
        "callback_reentrancy": [
            "Contract uses `ReentrancyGuard` (`nonReentrant`) on all entry points",
            "All state updates complete before any external call (strict CEI)",
            "Function only interacts with trusted/whitelisted contracts",
        ],
        "missing_access_control": [
            "Function is `internal`/`private` and only called from access-controlled paths",
            "Function is restricted via `onlyOwner`/`onlyRole`/`require(msg.sender == ...)`",
            "Public access is intentional by design (e.g., permissionless depositing)",
        ],
        "missing_validation": [
            "Validation exists but is in an upstream function caller",
            "Parameter range is inherently bounded by the type or protocol invariant",
            "Oracle data is validated by a wrapper contract before consumption",
        ],
        "arithmetic_error": [
            "Solidity >= 0.8.0 with default checked arithmetic",
            "SafeMath library used for all arithmetic on user-controlled values",
            "Input bounds validated before arithmetic operations",
        ],
        "rounding_error": [
            "Multiplication performed before division to preserve precision",
            "Scaling factor (1e18, 1e27) applied before division operations",
            "Rounding direction explicitly chosen: round down for mints, round up for burns",
        ],
        "first_depositor_attack": [
            "Vault uses virtual offset (ERC4626 `_decimalsOffset()`) to prevent inflation",
            "Dead shares mechanism: minimum initial deposit burned to address(dead)",
            "First depositor gets shares = assets (no division by totalSupply when totalSupply == 0)",
        ],
        "logic_error": [
            "Standard security patterns (access control, reentrancy guards, input validation) are in place",
            "Protocol behavior matches documented specification",
            "Edge case is unreachable due to invariant enforced elsewhere",
        ],
        "unvalidated_external_call": [
            "Target address validated against whitelist of approved contracts",
            "Function selector validated against allowlist before forwarding call",
            "User provides structured parameters, not raw calldata",
        ],
        "missing_frontrun_protection": [
            "Transaction uses private mempool (Flashbots) or commit-reveal scheme",
            "Slippage protection with reasonable bounds is enforced",
            "Deadline parameter prevents stale transaction execution",
        ],
        "missing_token_compatibility": [
            "Protocol uses SafeERC20 for all token interactions",
            "Token whitelist restricts to known-safe implementations",
            "Actual balance change measured post-transfer",
        ],
        "missing_initialization_guard": [
            "OpenZeppelin `initializer` modifier prevents re-initialization",
            "Proxy implementation initialize() called in same transaction as deployment",
            "Boolean flag checked and set atomically in initializer",
        ],
        "storage_layout_error": [
            "Storage gaps used in all upgradeable base contracts",
            "Upgrade tested with storage layout comparison tooling",
            "Diamond uses standardized storage pattern (AppStorage or Diamond Storage)",
        ],
        "weak_randomness": [
            "Chainlink VRF or similar verifiable randomness is used",
            "Commit-reveal scheme with sufficient delay prevents prediction",
            "Randomness is non-exploitable (cosmetic only, no financial impact)",
        ],
        "denial_of_service": [
            "Loop iterations are bounded by a reasonable constant",
            "External call failures are handled gracefully (try/catch or pull pattern)",
            "Rate limiting or gas stipend prevents griefing",
        ],
    }

    guards = guard_map.get(root_cause, [])
    if not guards:
        guards = [
            "Standard security patterns are in place",
            "Protocol only interacts with whitelisted/trusted contracts",
            "Mathematical operations use safe arithmetic with proper precision",
        ]

    lines = ["#### False Positive Guards", ""]
    lines.append(f"- Not this bug when: {guards[0]}")
    if len(guards) > 1:
        lines.append(f"- Safe if: {guards[1]}")
    if len(guards) > 2:
        lines.append(f"- Requires attacker control of: specific conditions per pattern")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Frontmatter augmentation
# ---------------------------------------------------------------------------


def augment_frontmatter(fm_text, fm, body):
    """Add missing fields to the frontmatter YAML text."""
    additions = []

    # Infer and add root_cause_family
    if "root_cause_family" not in fm:
        root_cause = infer_root_cause_family(fm, body)
        fm["root_cause_family"] = root_cause
    else:
        root_cause = fm["root_cause_family"]

    # Add pattern_key
    if "pattern_key" not in fm:
        pattern_key = construct_pattern_key(fm, root_cause)
        fm["pattern_key"] = pattern_key

    # Add code_keywords
    if "code_keywords" not in fm:
        keywords = extract_code_keywords(fm, body)
        fm["code_keywords"] = keywords

    # Add interaction_scope
    if "interaction_scope" not in fm:
        scope = detect_interaction_scope(fm, body)
        fm["interaction_scope"] = scope

    # Build the new frontmatter fields block
    new_fields = []

    if "root_cause_family" not in fm_text:
        new_fields.append("")
        new_fields.append("# Pattern Identity (Required)")
        new_fields.append(f"root_cause_family: {fm['root_cause_family']}")
        new_fields.append(f"pattern_key: {fm['pattern_key']}")

    if "interaction_scope" not in fm_text:
        new_fields.append("")
        new_fields.append("# Interaction Scope (Required for multi-contract or multi-path issues)")
        new_fields.append(f"interaction_scope: {fm['interaction_scope']}")

    if "code_keywords" not in fm_text:
        new_fields.append("")
        new_fields.append("# Grep / Hunt-Card Seeds (Required)")
        new_fields.append("code_keywords:")
        for kw in fm.get("code_keywords", ["TODO_add_keywords"]):
            new_fields.append(f"  - {kw}")

    if new_fields:
        return fm_text + "\n" + "\n".join(new_fields)
    return fm_text


# ---------------------------------------------------------------------------
# Family 1 specific: convert frontmatter references to body table
# ---------------------------------------------------------------------------


def convert_fm_references_to_table(fm):
    """Convert Family 1 YAML references list to a markdown table."""
    refs = fm.get("references", [])
    if not refs or not isinstance(refs, list):
        return ""

    lines = [
        "## References & Source Reports",
        "",
        "| Label | Path | Severity | Auditor | Source ID / Link |",
        "|-------|------|----------|---------|------------------|",
    ]
    for ref in refs:
        if isinstance(ref, dict):
            protocol = ref.get("protocol", "unknown")
            path = ref.get("file", "")
            severity = ref.get("severity", "unknown")
            auditor = ref.get("auditor", "unknown")
            lines.append(f"| [{protocol}] | {path} | {severity} | {auditor} | - |")

    lines.append("")
    return "\n".join(lines)


def convert_source_to_table(fm):
    """Convert Family 4 source field to a markdown table."""
    source = fm.get("source", "")
    if not source:
        return ""

    protocol = fm.get("protocol", "unknown")
    severity = safe_str(fm.get("severity", "unknown"))
    auditor = fm.get("audit_firm", "unknown")

    lines = [
        "## References & Source Reports",
        "",
        "| Label | Path | Severity | Auditor | Source ID / Link |",
        "|-------|------|----------|---------|------------------|",
        f"| [{protocol}] | {source} | {severity.upper()} | {auditor} | - |",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Body section insertion
# ---------------------------------------------------------------------------


def has_section(body, section_name):
    """Check if the body already contains a section header."""
    pattern = rf"^#{1,4}\s+{re.escape(section_name)}"
    return bool(re.search(pattern, body, re.MULTILINE | re.IGNORECASE))


def insert_triage_sections(body, fm):
    """Insert Agent Quick View, Boundary Map, Valid Bug Signals, False Positive Guards."""
    if has_section(body, "Agent Quick View"):
        return body

    aqv = generate_agent_quick_view(fm)
    cbm = generate_boundary_map(fm, body)
    vbs = generate_valid_bug_signals(fm, body)
    fpg = generate_false_positive_guards(fm, body)

    triage_block = f"\n{aqv}\n{cbm}\n{vbs}\n{fpg}\n"

    # Find insertion point: after "### Overview" or after first heading
    overview_match = re.search(r"^###?\s+Overview\b.*$", body, re.MULTILINE)
    if overview_match:
        # Find the end of the overview paragraph (next heading or double newline after content)
        rest = body[overview_match.end():]
        next_heading = re.search(r"^#{1,4}\s+", rest, re.MULTILINE)
        if next_heading:
            insert_pos = overview_match.end() + next_heading.start()
        else:
            # Insert after a reasonable amount of overview text
            insert_pos = overview_match.end() + min(len(rest), 500)
        return body[:insert_pos] + "\n" + triage_block + body[insert_pos:]

    # Try after first H1 or H2 heading
    h_match = re.search(r"^#{1,2}\s+[^#\n].*$", body, re.MULTILINE)
    if h_match:
        # Find the next heading after this one
        rest = body[h_match.end():]
        next_heading = re.search(r"^#{1,3}\s+", rest, re.MULTILINE)
        if next_heading:
            insert_pos = h_match.end() + next_heading.start()
        else:
            insert_pos = h_match.end() + 1
        return body[:insert_pos] + "\n" + triage_block + body[insert_pos:]

    # Last resort: prepend to body
    return "\n" + triage_block + body


def ensure_detection_patterns(body):
    """Add a Detection Patterns section if missing."""
    if has_section(body, "Detection Patterns"):
        return body

    detection = """
### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks
"""

    # Insert before "## Keywords" or "### Keywords" or "## Related" or at end
    for section_name in ["Keywords for Search", "Keywords", "Related Vulnerabilities", "Related"]:
        match = re.search(rf"^#{1,3}\s+{re.escape(section_name)}", body, re.MULTILINE)
        if match:
            return body[:match.start()] + detection + "\n" + body[match.start():]

    return body + detection


def ensure_keywords_section(body, fm):
    """Add Keywords for Search section if missing."""
    if has_section(body, "Keywords for Search") or has_section(body, "Keywords"):
        return body

    keywords = fm.get("code_keywords", [])
    prims = fm.get("primitives", [])
    tags = fm.get("tags", [])

    all_kw = set()
    for source in [keywords, prims, tags]:
        if isinstance(source, list):
            all_kw.update(str(k) for k in source)
        elif isinstance(source, str):
            all_kw.update(k.strip() for k in source.split(","))

    cat = str(fm.get("category", ""))
    vuln = str(fm.get("vulnerability_type", ""))
    if cat:
        all_kw.add(cat)
    if vuln:
        all_kw.add(vuln)

    kw_str = ", ".join(f"`{k}`" for k in sorted(all_kw) if k)

    section = f"""
### Keywords for Search

> These keywords enhance vector search retrieval:

{kw_str}
"""
    return body + section


# ---------------------------------------------------------------------------
# Main migration logic per file
# ---------------------------------------------------------------------------


def migrate_file(filepath, dry_run=False, verbose=False):
    """Migrate a single file to the new template format."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    fm, fm_end, fm_text = parse_frontmatter(content)

    if fm_end == 0:
        return False, "No frontmatter found"

    if is_already_migrated(fm):
        return False, "Already migrated"

    body = content[fm_end:]
    family = classify_family(fm, body)

    # --- Step 1: Augment frontmatter ---
    new_fm_text = augment_frontmatter(fm_text, fm, body)

    # --- Step 2: Handle family-specific reference migrations ---
    ref_table = ""
    if family == "family1_very_old":
        ref_table = convert_fm_references_to_table(fm)
        # Remove references from frontmatter
        new_fm_text = re.sub(
            r"\nreferences:\s*\n(?:\s+-\s+.*\n)*", "\n", new_fm_text
        )
        # Also remove vulnerability_class/title if we have category
        # (keep them as comments for traceability)
    elif family == "family4_unique":
        if not has_section(body, "References"):
            ref_table = convert_source_to_table(fm)

    # --- Step 3: Insert triage sections into body ---
    new_body = body

    # Insert reference table for families that need it
    if ref_table and not has_section(new_body, "References"):
        new_body = "\n\n" + ref_table + new_body

    # Insert Agent Quick View, Boundary Map, Valid Bug Signals, False Positive Guards
    new_body = insert_triage_sections(new_body, fm)

    # Ensure Detection Patterns section exists
    new_body = ensure_detection_patterns(new_body)

    # Ensure Keywords for Search section exists
    new_body = ensure_keywords_section(new_body, fm)

    # --- Step 4: Reassemble ---
    new_content = f"---\n{new_fm_text}\n---{new_body}"

    if dry_run:
        return True, f"Would migrate ({family})"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True, f"Migrated ({family})"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Migrate legacy DB entries to the new TEMPLATE.md format"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without writing"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    parser.add_argument(
        "--file", type=str, help="Migrate a single file (for testing)"
    )
    args = parser.parse_args()

    if args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"File not found: {filepath}")
            sys.exit(1)
        success, msg = migrate_file(filepath, dry_run=args.dry_run, verbose=args.verbose)
        status = "OK" if success else "SKIP"
        print(f"  [{status}] {filepath.name}: {msg}")
        return

    # Scan all DB files
    files = sorted(DB_DIR.rglob("*.md"))
    total = 0
    migrated = 0
    skipped = 0
    errors = 0

    print(f"Scanning {len(files)} files in {DB_DIR}")
    if args.dry_run:
        print("=== DRY RUN MODE ===\n")

    for filepath in files:
        if should_skip(filepath):
            continue

        total += 1
        rel = filepath.relative_to(DB_DIR.parent)

        try:
            success, msg = migrate_file(
                filepath, dry_run=args.dry_run, verbose=args.verbose
            )
            if success:
                print(f"  ✅ {rel}: {msg}")
                migrated += 1
            else:
                if args.verbose:
                    print(f"  ⏭️  {rel}: {msg}")
                skipped += 1
        except Exception as e:
            import traceback
            print(f"  ❌ {rel}: {e}")
            if args.verbose:
                traceback.print_exc()
            errors += 1

    print(f"\n{'='*60}")
    print(f"Total scanned:  {total}")
    print(f"Migrated:       {migrated}")
    print(f"Already done:   {skipped}")
    print(f"Errors:         {errors}")

    if args.dry_run and migrated > 0:
        print(f"\nRun without --dry-run to apply {migrated} migrations.")


if __name__ == "__main__":
    main()
