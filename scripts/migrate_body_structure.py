#!/usr/bin/env python3
"""
Add missing body structure sections to DeFiHackLabs DB entries:
  - Agent Quick View table
  - Contract / Boundary Map
  - Valid Bug Signals
  - False Positive Guards
  - Path Variant pathShape tags on existing numbered sections
"""

import os
import re
import sys
from pathlib import Path

DB_DIR = Path(__file__).parent.parent / "DB"

def parse_frontmatter(content):
    """Parse frontmatter into dict."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}, 0
    
    fm_text = match.group(1)
    fm_end = match.end()
    fm = {}
    current_key = None
    current_list = None
    
    for line in fm_text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('#') and ':' not in stripped:
            continue
        
        if stripped.startswith('- ') and current_key:
            if current_list is None:
                current_list = []
            val = stripped[2:].strip().strip('"').strip("'")
            current_list.append(val)
            fm[current_key] = current_list
            continue
        
        if ':' in stripped:
            parts = stripped.split(':', 1)
            key = parts[0].strip().lstrip('# ')
            val = parts[1].strip().strip('"').strip("'")
            if key:
                current_key = key
                current_list = None
                fm[key] = val
    
    return fm, fm_end

def extract_exploit_examples(content):
    """Extract protocol names, dates, and losses from Example lines."""
    examples = []
    for m in re.finditer(r'\*\*(?:Example\s+\d+:\s+)?(\w[\w\s]+?)\s*(?:—|–|-)\s*(.*?)(?:\$[\d,.]+[KMB]?.*?)?\*\*', content):
        examples.append(m.group(1).strip())
    return examples[:8]

def extract_affected_contracts(content):
    """Extract contract/protocol names from content."""
    contracts = set()
    # Protocol names from examples
    for m in re.finditer(r'\*\*(?:Example\s+\d+:\s+)?(\w+(?:\s+\w+)?)\s*(?:—|–)', content):
        contracts.add(m.group(1).strip())
    # Contract names from code
    for m in re.finditer(r'contract\s+(\w+)', content):
        name = m.group(1)
        if name not in {'Test', 'Setup', 'Exploit', 'Attack', 'Attacker'}:
            contracts.add(name)
    return sorted(contracts)[:8]

def extract_numbered_sections(content):
    """Find numbered ## sections like '## 1. Title'."""
    sections = []
    for m in re.finditer(r'^##\s+(\d+)\.\s+(.+)$', content, re.MULTILINE):
        sections.append((m.group(1), m.group(2).strip(), m.start()))
    return sections

def determine_path_shape(section_text):
    """Infer pathShape from section content."""
    text_lower = section_text.lower()
    
    if 'flash loan' in text_lower or 'flashloan' in text_lower:
        if 'callback' in text_lower or 'receive()' in text_lower or 'fallback' in text_lower:
            return 'callback-reentrant'
        return 'atomic'
    if 'reentr' in text_lower:
        if 'cross-contract' in text_lower or 'cross_contract' in text_lower:
            return 'callback-reentrant'
        if 'read-only' in text_lower or 'readonly' in text_lower:
            return 'cross-protocol'
        return 'callback-reentrant'
    if 'loop' in text_lower or 'iterate' in text_lower or 'repeated' in text_lower:
        return 'iterative-loop'
    if 'step 1' in text_lower and 'step 3' in text_lower:
        return 'linear-multistep'
    if 'setup' in text_lower and ('fire' in text_lower or 'trigger' in text_lower or 'exploit' in text_lower):
        return 'staged'
    return 'atomic'

def safe_str(val, default='unknown'):
    """Safely convert a frontmatter value (str or list) to string."""
    if isinstance(val, list):
        return ', '.join(str(v) for v in val)
    if val is None:
        return default
    return str(val).strip('"').strip("'")

def generate_agent_quick_view(fm):
    """Generate Agent Quick View table from frontmatter."""
    root_cause = safe_str(fm.get('root_cause_family', 'unknown'))
    pattern_key = safe_str(fm.get('pattern_key', 'unknown'))
    severity = safe_str(fm.get('severity', 'high'))
    impact = safe_str(fm.get('impact', 'fund_loss'))
    scope = safe_str(fm.get('interaction_scope', 'single_contract'))
    chain = safe_str(fm.get('chain', 'ethereum'))
    
    return f"""
## Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause Family | `{root_cause}` |
| Pattern Key | `{pattern_key}` |
| Severity | {severity.upper()} |
| Impact | {impact} |
| Interaction Scope | {scope} |
| Chain(s) | {chain} |
"""

def generate_valid_bug_signals(fm, content):
    """Generate Valid Bug Signals from content analysis."""
    category = safe_str(fm.get('category', '')).lower()
    vuln_type = safe_str(fm.get('vulnerability_type', '')).lower()
    
    signals = []
    
    # Category-specific signals
    if 'access_control' in category or 'access_control' in vuln_type:
        signals = [
            "State-changing function (`mint`, `burn`, `set*`, `migrate*`) lacks `onlyOwner`/`onlyRole` modifier",
            "External function accepts arbitrary `address` parameter and calls interface methods on it without registry validation",
            "Configuration setter (token address, fee, reward) is callable by non-owner",
            "Migration/upgrade function does not validate source contract against whitelist",
        ]
    elif 'reentrancy' in category:
        signals = [
            "External call (`.call`, `.transfer`, token transfer) occurs before state variable update",
            "Token implements callback hooks (ERC-777 `tokensReceived`, ERC-721 `onERC721Received`) and protocol doesn't use `nonReentrant`",
            "User-supplied token address passed to `transferFrom` / `safeTransferFrom` without callback protection",
            "Read-only function's return value consumed cross-contract during an active callback window",
        ]
    elif 'price_manipulation' in category or 'oracle' in category:
        signals = [
            "Price derived from spot reserve ratio (`getReserves()`, `balanceOf()`) without TWAP or oracle",
            "Flash-loan-borrowable asset used as price source within the same transaction",
            "Low-liquidity pool used as price oracle for high-value lending/collateral decisions",
            "No minimum liquidity / depth check before accepting oracle price",
        ]
    elif 'business_logic' in category or 'protocol_logic' in category or 'share' in vuln_type:
        signals = [
            "State variable updated after external interaction instead of before (CEI violation)",
            "Share/token exchange rate calculable from manipulable on-chain state",
            "Reward accrual continues during paused/emergency state",
            "Withdrawal path produces different accounting than deposit path for same principal",
        ]
    elif 'arbitrary_call' in category or 'arbitrary' in vuln_type:
        signals = [
            "Function accepts user-controlled `target` and `calldata` for low-level `.call()`",
            "Delegatecall to user-supplied address with contract's storage context",
            "Token approval granted to contract that forwards arbitrary calls",
            "Router/aggregator executes user-supplied swap path without validating intermediate targets",
        ]
    elif 'amm_calculation' in category or 'k_invariant' in vuln_type:
        signals = [
            "Fee base constant differs from K-invariant check constant in swap function",
            "UniswapV2 fork modified fee parameters without updating K-check scaling",
            "Swap output calculation uses different precision base than invariant verification",
        ]
    elif 'overflow' in category or 'overflow' in vuln_type:
        signals = [
            "Arithmetic operation on user-controlled input without SafeMath or Solidity >=0.8 checked arithmetic",
            "Casting between different-width integer types (uint256 → uint128/uint96) without bounds check",
            "Multiplication before division where intermediate product can exceed uint256",
        ]
    elif 'initialization' in category:
        signals = [
            "Initializer function callable more than once (missing `initializer` modifier or manual flag)",
            "Proxy implementation has unprotected `initialize()` that can be called by anyone",
            "Constructor logic not replicated in initializer for upgradeable contract",
        ]
    elif 'vault_inflation' in category or 'inflation' in vuln_type:
        signals = [
            "First deposit to vault with zero total supply — share calculation uses `totalAssets / totalSupply`",
            "Direct asset transfer (donation) to vault changes exchange rate before victim's deposit",
            "No minimum initial deposit or dead shares mechanism to prevent share inflation",
        ]
    elif 'governance' in category or 'dao' in category:
        signals = [
            "Flash-loaned tokens usable for voting power within same transaction",
            "Governance proposal executable before timelock delay expires",
            "Quorum threshold bypassable via vote delegation or token transfer timing",
            "No snapshot mechanism — voting power derived from current balance, not past checkpoint",
        ]
    elif 'fee_on_transfer' in category or 'deflationary' in category or 'reflection' in vuln_type:
        signals = [
            "Protocol caches `amount` parameter instead of measuring actual received balance (`balanceAfter - balanceBefore`)",
            "Transfer fee / tax not accounted for in AMM pair reserve calculations",
            "Reflection token's elastic supply causes stale balance assumptions in protocols",
        ]
    elif 'token_compatibility' in category or 'reflection' in vuln_type:
        signals = [
            "Protocol assumes all ERC20 tokens behave identically (no fees, no rebasing, no hooks)",
            "Token balance check uses cached amount instead of actual `balanceOf()` after transfer",
            "Missing support for tokens with non-standard return values (USDT, BNB)",
        ]
    elif 'mev' in category or 'mev_bot' in category:
        signals = [
            "Bot contract has unprotected callback / fallback that processes arbitrary input",
            "Swap execution lacks private mempool or commit-reveal protection",
            "MEV bot approves tokens to unvalidated router addresses",
        ]
    elif 'precision' in category or 'calculation' in category or 'reward' in vuln_type:
        signals = [
            "Division before multiplication truncates intermediate result, accumulating rounding losses",
            "Reward rate calculated with insufficient decimal precision for small stakers",
            "Share price calculation rounds in attacker's favor during mint/redeem operations",
        ]
    elif 'missing_validations' in category or 'input_validation' in vuln_type:
        signals = [
            "Critical function parameter not checked against valid range (zero address, zero amount, overflow bounds)",
            "Array length parameters not validated, allowing empty arrays or excessive gas consumption",
            "Slippage/deadline parameter is zero or user-controllable with no minimum enforcement",
        ]
    else:
        # Generic signals based on content keywords
        signals = [
            "Missing access control on state-changing function",
            "User-supplied input passed to sensitive operation without validation",
            "State update occurs after external interaction (CEI violation)",
            "Protocol assumption about token behavior violated by specific token implementation",
        ]
    
    lines = ["## Valid Bug Signals", ""]
    for i, s in enumerate(signals[:4], 1):
        lines.append(f"{i}. {s}")
    lines.append("")
    return '\n'.join(lines)

def generate_false_positive_guards(fm, content):
    """Generate False Positive Guards from content analysis."""
    category = safe_str(fm.get('category', '')).lower()
    
    guards = []
    
    if 'access_control' in category:
        guards = [
            "Function is `internal`/`private` and only called from access-controlled paths",
            "Contract uses proxy pattern where admin functions are in separate admin-only facet",
            "Function is restricted via `onlyOwner`/`onlyRole`/`require(msg.sender == ...)` check",
            "Token is a governance token where public minting is intentional (e.g., inflationary reward)",
        ]
    elif 'reentrancy' in category:
        guards = [
            "Contract uses OpenZeppelin `ReentrancyGuard` (`nonReentrant` modifier) on all entry points",
            "All state updates complete before any external call (strict CEI compliance)",
            "Token is a standard ERC20 without hooks (not ERC-777, not ERC-721 with callbacks)",
            "Function only interacts with trusted/whitelisted contracts, not user-supplied addresses",
        ]
    elif 'price_manipulation' in category or 'oracle' in category:
        guards = [
            "Protocol uses Chainlink/Pyth oracle with staleness checks instead of spot price",
            "TWAP oracle with sufficient observation window (>= 30 minutes) is used",
            "Flash-loan resistance via multi-block price averaging or commit-reveal",
            "Low-value operations where manipulation cost exceeds extractable value",
        ]
    elif 'business_logic' in category or 'share' in category:
        guards = [
            "Share/exchange rate calculation uses virtual offsets or dead shares to prevent manipulation",
            "Protocol pauses all value-altering operations during emergency mode",
            "Withdrawal enforces same accounting path as deposit with matching decimal handling",
            "Rate changes bounded by maximum per-period adjustment (rate limiter)",
        ]
    elif 'arbitrary_call' in category or 'arbitrary' in category:
        guards = [
            "Target address validated against whitelist of approved contracts",
            "Function selector validated against allowlist before forwarding call",
            "Multicall pattern only relays calls to `address(this)` (self-referential)",
            "User provides structured parameters, not raw calldata (protocol builds the call internally)",
        ]
    elif 'overflow' in category:
        guards = [
            "Solidity >= 0.8.0 with default checked arithmetic (no `unchecked` blocks on user input)",
            "SafeMath library used for all arithmetic on user-controlled values",
            "Input bounds validated before arithmetic operations",
        ]
    elif 'vault_inflation' in category or 'inflation' in category:
        guards = [
            "Vault uses virtual offset (OpenZeppelin ERC4626 with `_decimalsOffset()`) to prevent inflation",
            "Dead shares mechanism: minimum initial deposit burned to address(dead)",
            "First depositor gets shares = assets (no division by totalSupply when totalSupply == 0)",
        ]
    elif 'governance' in category or 'dao' in category:
        guards = [
            "Voting power snapshots taken at proposal creation block (not current block)",
            "Timelock delay enforced between proposal passing and execution",
            "Flash-loan token detection: vote weight requires holding tokens for N blocks",
        ]
    elif 'fee_on_transfer' in category or 'deflationary' in category or 'reflection' in category:
        guards = [
            "Protocol measures actual received amount via `balanceAfter - balanceBefore` pattern",
            "Token whitelist excludes fee-on-transfer and rebasing tokens",
            "Pair contract accounts for transfer fees in reserve synchronization",
        ]
    elif 'token_compatibility' in category:
        guards = [
            "Protocol uses SafeERC20 for all token interactions",
            "Token whitelist restricts to known-safe token implementations",
            "Actual balance change measured post-transfer instead of trusting amount parameter",
        ]
    elif 'mev' in category:
        guards = [
            "Bot uses Flashbots/private mempool for swap execution",
            "Router address hardcoded and verified, not user-supplied",
            "Callback functions validate msg.sender against known pool addresses",
        ]
    elif 'precision' in category or 'calculation' in category:
        guards = [
            "Multiplication performed before division to preserve precision",
            "Scaling factor (1e18, 1e27) applied before division operations",
            "Rounding direction explicitly chosen: round down for mints, round up for burns",
        ]
    elif 'initialization' in category:
        guards = [
            "OpenZeppelin `initializer` modifier prevents re-initialization",
            "Boolean flag checked and set atomically in initializer function",
            "Proxy implementation `initialize()` called in same transaction as deployment",
        ]
    elif 'missing_validations' in category or 'input_validation' in category:
        guards = [
            "All user inputs validated at function entry (require statements)",
            "Address parameters checked against address(0)",
            "Array length bounds enforced to prevent gas griefing",
        ]
    else:
        guards = [
            "Standard security patterns (access control, reentrancy guards, input validation) are in place",
            "Protocol only interacts with whitelisted/trusted contracts",
            "Mathematical operations use safe arithmetic with proper precision handling",
        ]
    
    lines = ["## False Positive Guards", ""]
    for i, g in enumerate(guards[:4], 1):
        lines.append(f"{i}. {g}")
    lines.append("")
    return '\n'.join(lines)

def generate_boundary_map(fm, content):
    """Generate a compact Contract/Boundary Map."""
    contracts = extract_affected_contracts(content)
    scope = safe_str(fm.get('interaction_scope', 'single_contract'))
    component = safe_str(fm.get('affected_component', 'unknown'))
    
    if not contracts:
        contracts = [c.strip() for c in component.split(',')]
    
    lines = ["## Contract / Boundary Map", ""]
    lines.append(f"**Interaction Scope**: `{scope}`")
    lines.append("")
    lines.append("| Component | Role |")
    lines.append("|-----------|------|")
    
    for i, c in enumerate(contracts[:6]):
        role = "Affected component" if i == 0 else "Related component"
        lines.append(f"| `{c}` | {role} |")
    
    lines.append("")
    return '\n'.join(lines)


def add_path_variant_tags(content):
    """Add pathShape tags to existing numbered sections."""
    def replace_section(m):
        num = m.group(1)
        title = m.group(2)
        # Find section content to determine path shape
        start = m.end()
        # Look ahead up to 2000 chars for shape analysis
        section_text = content[start:start + 2000]
        shape = determine_path_shape(section_text)
        return f"## {num}. {title}\n\n> **pathShape**: `{shape}`"
    
    result = re.sub(r'^##\s+(\d+)\.\s+(.+)$', replace_section, content, flags=re.MULTILINE)
    return result


def process_file(filepath):
    """Process a single file to add missing body structure sections."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Skip if already has Agent Quick View
    if 'Agent Quick View' in content or 'Agent Quick-View' in content:
        return False, "Already has Agent Quick View"
    
    fm, fm_end = parse_frontmatter(content)
    if fm_end == 0:
        return False, "No frontmatter"
    
    body = content[fm_end:]
    frontmatter_block = content[:fm_end]
    
    # Find insertion point: after References table or after first ---
    # Look for the end of References table or first ## heading
    ref_end = None
    overview_start = None
    
    # Find "## References" or "## References & Source Reports" section end
    ref_match = re.search(r'^##\s+References.*$', body, re.MULTILINE)
    if ref_match:
        # Find the next ## heading after references
        next_heading = re.search(r'^##\s+(?!References)', body[ref_match.end():], re.MULTILINE)
        if next_heading:
            ref_end = ref_match.end() + next_heading.start()
        else:
            ref_end = ref_match.end() + 200  # fallback
    
    # Also look for "# Title" (H1) followed by "## Overview"
    h1_match = re.search(r'^#\s+[^#].*$', body, re.MULTILINE)
    overview_match = re.search(r'^##\s+Overview', body, re.MULTILINE)
    
    # Determine insertion point
    if ref_end:
        insert_pos = ref_end
    elif overview_match:
        insert_pos = overview_match.start()
    elif h1_match:
        insert_pos = h1_match.end() + 1
    else:
        # Insert right after frontmatter
        insert_pos = 0
    
    # Generate sections
    aqv = generate_agent_quick_view(fm)
    cbm = generate_boundary_map(fm, content)
    vbs = generate_valid_bug_signals(fm, content)
    fpg = generate_false_positive_guards(fm, content)
    
    new_sections = f"\n{aqv}\n{cbm}\n{vbs}\n{fpg}\n"
    
    # Insert new sections
    new_body = body[:insert_pos] + new_sections + body[insert_pos:]
    
    # Add pathShape tags to numbered sections
    new_body = add_path_variant_tags(new_body)
    
    # Reassemble
    new_content = frontmatter_block + new_body
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "Added Agent Quick View, Boundary Map, Valid Bug Signals, False Positive Guards, pathShape tags"


def main():
    """Find and process all legacy defihacklabs files."""
    files = []
    
    for md_file in sorted(DB_DIR.rglob('defihacklabs-*.md')):
        files.append(md_file)
    
    unique_dir = DB_DIR / 'unique' / 'defihacklabs'
    if unique_dir.exists():
        for md_file in sorted(unique_dir.glob('*.md')):
            if md_file not in files:
                files.append(md_file)
    
    print(f"Found {len(files)} DeFiHackLabs files to process\n")
    
    migrated = 0
    skipped = 0
    errors = 0
    
    for filepath in files:
        rel = filepath.relative_to(DB_DIR.parent)
        try:
            success, msg = process_file(filepath)
            if success:
                print(f"  ✅ {rel}: {msg}")
                migrated += 1
            else:
                print(f"  ⏭️  {rel}: {msg}")
                skipped += 1
        except Exception as e:
            import traceback
            print(f"  ❌ {rel}: {e}")
            traceback.print_exc()
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"Results: {migrated} migrated, {skipped} skipped, {errors} errors")

if __name__ == '__main__':
    main()
