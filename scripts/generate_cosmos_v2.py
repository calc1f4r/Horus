#!/usr/bin/env python3
"""
Comprehensive Cosmos Vulnerability DB Entry Generator.

Groups 302+ classified patterns into ~45 entry files,
each containing multiple vulnerability pattern sections.
Generates proper TEMPLATE.md-compliant markdown entries.
"""

import os, re, json, sys
from collections import defaultdict

# ============================================================
# Configuration
# ============================================================
REPORTS_DIR = "reports/cosmos_cometbft_findings"
DB_BASE = "DB/cosmos/app-chain"
EXISTING_DB_FILES_TO_REMOVE = False  # Set True to clean old generated files

# ============================================================
# Entry File Definitions: path -> list of pattern IDs
# ============================================================
ENTRY_FILES = {
    # STAKING
    "staking/stake-deposit-vulnerabilities": [
        "staking-deposit-amount-tracking",
        "staking-deposit-validation",
        "staking-deposit-frontrunning",
        "staking-balance-desync",
        "staking-deposit-queue",
        "staking-deposit-inflation",
        "staking-incorrect-calculation",
        "staking-invariant-broken",
    ],
    "staking/unstake-withdrawal-vulnerabilities": [
        "unstake-cooldown-bypass",
        "unstake-withdrawal-dos",
        "unstake-withdrawal-accounting",
        "unstake-queue-manipulation",
        "unstake-before-slash",
        "unstake-emergency",
        "unstake-pending-not-tracked",
        "unstake-lock-funds",
    ],
    "staking/delegation-redelegation-vulnerabilities": [
        "delegation-self-manipulation",
        "delegation-dos-revert",
        "delegation-state-inconsistency",
        "delegation-to-inactive",
        "delegation-frontrunning",
        "delegation-reward-manipulation",
        "delegation-redelegation-error",
        "delegation-unbonding-exploit",
    ],
    "staking/validator-management-vulnerabilities": [
        "validator-registration-bypass",
        "validator-removal-failure",
        "validator-set-manipulation",
        "validator-key-rotation",
        "validator-commission-exploit",
        "validator-status-transition",
        "validator-dust-collateral",
        "validator-score-manipulation",
        "validator-operator-mismatch",
        "validator-can-skip-exit",
        "validator-governance-power",
    ],

    # SLASHING
    "slashing/slashing-evasion-frontrunning": [
        "slashing-frontrun-exit",
        "slashing-cooldown-exploit",
        "slashing-delegation-bypass",
        "slashing-insufficient-deposit",
        "slashing-external-block",
        "slashing-queued-excluded",
        "slashing-unregistered-operator",
        "slashing-mechanism-abuse",
    ],
    "slashing/slashing-accounting-errors": [
        "slashing-amount-incorrect",
        "slashing-share-dilution",
        "slashing-balance-update-error",
        "slashing-reward-interaction",
        "slashing-pending-operations",
        "slashing-principal-error",
        "slashing-penalty-system",
        "slashing-double-punishment",
        "slashing-tombstone",
    ],

    # REWARDS
    "rewards/reward-calculation-vulnerabilities": [
        "reward-calculation-incorrect",
        "reward-per-share-error",
        "reward-accumulation-error",
        "reward-delayed-balance",
        "reward-decimal-mismatch",
        "reward-weight-error",
        "reward-historical-loss",
        "reward-pool-share",
    ],
    "rewards/reward-theft-manipulation": [
        "reward-flashloan-theft",
        "reward-frontrunning",
        "reward-orphaned-capture",
        "reward-dilution",
        "reward-gauge-exploit",
        "reward-vault-interaction",
        "reward-escrow-assignment",
        "reward-commission-error",
    ],
    "rewards/reward-distribution-failures": [
        "reward-stuck-locked",
        "reward-distribution-dos",
        "reward-missing-update",
        "reward-after-removal",
        "reward-unclaimed-loss",
        "reward-distribution-unfair",
        "reward-epoch-timing",
    ],

    # DOS
    "dos/chain-halt-consensus-dos": [
        "dos-block-production-halt",
        "dos-consensus-halt",
        "dos-state-machine",
        "dos-unbounded-beginblock",
        "dos-unbounded-endblock",
        "dos-unbounded-array",
        "dos-panic-crash",
        "dos-message-flooding",
        "dos-deposit-spam",
        "dos-proposal-spam",
        "dos-tx-replay",
    ],
    "dos/gas-resource-exhaustion": [
        "dos-gas-limit-exploit",
        "dos-gas-metering-bypass",
        "dos-memory-exhaustion",
        "dos-storage-exhaustion",
        "dos-large-payload",
    ],
    "dos/griefing-revert-dos": [
        "dos-function-revert",
        "dos-frontrun-grief",
        "dos-dust-grief",
        "dos-external-call-revert",
        "dos-loop-revert",
    ],

    # FUND SAFETY
    "fund-safety/fund-theft-vulnerabilities": [
        "funds-theft-auth-bypass",
        "funds-theft-manipulation",
        "funds-theft-reentrancy",
        "funds-theft-delegatecall",
        "funds-theft-replay",
        "funds-theft-frontrunning",
        "funds-theft-surplus",
        "funds-race-condition",
        "funds-missing-slippage",
    ],
    "fund-safety/fund-locking-insolvency": [
        "funds-lock-permanent",
        "funds-lock-conditional",
        "funds-insolvency-protocol",
        "funds-insolvency-slash",
        "funds-insolvency-rebase",
        "funds-bad-debt",
        "funds-withdrawal-blocked",
        "funds-unsafe-casting-loss",
    ],

    # ACCOUNTING
    "accounting/balance-tracking-errors": [
        "accounting-balance-not-updated",
        "accounting-double-counting",
        "accounting-tvl-error",
        "accounting-state-corruption",
        "accounting-missing-deduction",
        "accounting-cross-module",
        "accounting-pending-tracking",
        "accounting-negative-value",
        "accounting-fee-deduction",
    ],
    "accounting/exchange-rate-vulnerabilities": [
        "accounting-exchange-rate-manipulation",
        "accounting-exchange-rate-stale",
        "accounting-exchange-rate-error",
        "accounting-share-price-inflation",
        "accounting-conversion-rounding",
    ],
    "accounting/integer-precision-vulnerabilities": [
        "accounting-integer-overflow",
        "accounting-integer-underflow",
        "accounting-unsafe-casting",
        "accounting-precision-loss",
        "accounting-decimal-mismatch",
    ],

    # EVM / PRECOMPILE
    "evm/evm-gas-handling-vulnerabilities": [
        "evm-intrinsic-gas-missing",
        "evm-gas-refund-error",
        "evm-precompile-gas-hardcode",
        "evm-gas-not-consumed-error",
        "evm-gas-mismatch-call",
    ],
    "evm/precompile-state-vulnerabilities": [
        "evm-dirty-state-precompile",
        "evm-precompile-panic",
        "evm-delegatecall-precompile",
        "evm-bank-balance-sync",
        "evm-nonce-manipulation",
        "evm-tx-disguise",
        "evm-precompile-outdated",
        "evm-state-revert",
        "evm-address-conversion",
    ],

    # IBC / BRIDGE
    "ibc/ibc-protocol-vulnerabilities": [
        "ibc-channel-verification",
        "ibc-packet-handling",
        "ibc-version-negotiation",
        "ibc-middleware-bypass",
        "ibc-authentication",
        "ibc-timeout",
    ],
    "bridge/cross-chain-bridge-vulnerabilities": [
        "bridge-replay-attack",
        "bridge-token-accounting",
        "bridge-relayer-exploit",
        "bridge-freeze-halt",
        "bridge-observer-exploit",
        "bridge-denom-handling",
        "bridge-message-validation",
    ],

    # GOVERNANCE
    "governance/governance-voting-vulnerabilities": [
        "governance-voting-power-manipulation",
        "governance-proposal-exploit",
        "governance-quorum-manipulation",
        "governance-voting-lock",
        "governance-ballot-spam",
        "governance-bribe-manipulation",
        "governance-offboard-exploit",
        "governance-voting-zero-weight",
        "governance-parameter-change",
        "governance-timelock-bypass",
    ],

    # CONSENSUS
    "consensus/consensus-finality-vulnerabilities": [
        "consensus-proposer-dos",
        "consensus-finality-bypass",
        "consensus-reorg",
        "consensus-vote-extension",
        "consensus-block-sync",
        "consensus-non-determinism",
        "consensus-proposer-selection",
        "consensus-equivocation",
        "consensus-liveness",
    ],

    # ACCESS CONTROL
    "access-control/authorization-vulnerabilities": [
        "access-missing-control",
        "access-role-assignment",
        "access-antehandler-bypass",
        "access-allowlist-bypass",
        "access-cosmwasm-bypass",
        "access-amino-signing",
        "access-predecessor-misuse",
        "access-owner-privilege",
        "access-msg-sender-validation",
        "access-module-authority",
    ],

    # TIMING
    "timing/epoch-timing-vulnerabilities": [
        "timing-epoch-transition",
        "timing-epoch-snapshot",
        "timing-cooldown-bypass",
        "timing-timestamp-boundary",
        "timing-unbonding-change",
        "timing-epoch-duration-break",
        "timing-expiration-bypass",
        "timing-block-time",
        "timing-race-condition",
    ],

    # VALIDATION
    "validation/input-validation-vulnerabilities": [
        "validation-zero-check-missing",
        "validation-bounds-missing",
        "validation-state-check-missing",
        "validation-percentage-overflow",
        "validation-address-normalization",
        "validation-duplicate-missing",
        "validation-config-bypass",
        "validation-input-general",
        "validation-incorrect-check",
        "validation-logic-error",
        "validation-msg-missing",
        "validation-length-check",
    ],

    # TOKEN
    "tokens/token-handling-vulnerabilities": [
        "token-fee-on-transfer",
        "token-rebasing",
        "token-approval-error",
        "token-unlimited-mint",
        "token-burn-error",
        "token-transfer-hook",
        "token-nft-handling",
        "token-decimal-handling",
        "token-zrc20-bypass",
        "token-supply-tracking",
        "token-denom-handling",
    ],

    # VAULT
    "vault/vault-share-vulnerabilities": [
        "vault-share-inflation",
        "vault-share-calculation",
        "vault-deposit-theft",
        "vault-withdrawal-error",
        "vault-tvl-manipulation",
        "vault-strategy-loss",
        "vault-griefing",
        "vault-insolvency",
        "vault-curator-exploit",
        "vault-multi-interaction",
    ],

    # ORACLE / PRICE
    "oracle/oracle-price-vulnerabilities": [
        "oracle-stale-price",
        "oracle-price-manipulation",
        "oracle-dos",
        "oracle-deviation-exploit",
        "oracle-frontrunning",
        "oracle-missing-stake",
        "oracle-chainlink-specific",
        "oracle-wrong-price-usage",
    ],

    # LIQUIDATION / AUCTION
    "liquidation/liquidation-auction-vulnerabilities": [
        "liquidation-threshold-error",
        "liquidation-frontrunning",
        "liquidation-cascade",
        "auction-manipulation",
        "auction-cdp-dust",
        "debt-accounting-error",
        "collateral-ratio-bypass",
        "lien-exploit",
        "liquidation-bot-dos",
        "liquidation-accounting",
    ],

    # LIFECYCLE
    "lifecycle/upgrade-migration-vulnerabilities": [
        "lifecycle-upgrade-error",
        "lifecycle-migration-failure",
        "lifecycle-init-error",
        "lifecycle-storage-gap",
        "lifecycle-module-registration",
        "lifecycle-genesis-error",
        "lifecycle-deployment-param",
        "lifecycle-state-export",
        "lifecycle-version-compat",
    ],

    # SIGNATURE
    "signature/signature-replay-vulnerabilities": [
        "signature-verification-missing",
        "signature-replay",
        "signature-cross-chain-replay",
        "signature-forgery",
        "signature-duplicate",
        "signature-eip155-missing",
        "signature-key-management",
        "signature-malleability",
        "signature-nonce-manipulation",
    ],

    # REENTRANCY
    "reentrancy/reentrancy-vulnerabilities": [
        "reentrancy-classic",
        "reentrancy-cross-contract",
        "reentrancy-callback",
        "reentrancy-read-only",
    ],

    # MEV / FRONTRUNNING
    "mev/frontrunning-mev-vulnerabilities": [
        "mev-staking-frontrun",
        "mev-price-update",
        "mev-slippage-exploit",
        "mev-sandwich",
        "mev-block-stuffing",
        "mev-arbitrage",
        "mev-priority",
        "mev-jit-liquidity",
    ],

    # MINIPOOL / NODE OPERATOR
    "node-operator/minipool-node-vulnerabilities": [
        "minipool-deposit-theft",
        "minipool-cancel-error",
        "minipool-slash-avoidance",
        "minipool-finalization",
        "minipool-replay",
        "operator-registration-frontrun",
        "operator-reward-leak",
        "operator-key-fundable",
        "operator-deregistration",
    ],

    # BTC STAKING
    "btc-staking/btc-staking-vulnerabilities": [
        "btc-staking-tx-validation",
        "btc-unbonding-handling",
        "btc-delegation-finality",
        "btc-change-output",
        "btc-slashable-stake",
        "btc-covenant-signature",
        "btc-staking-indexer",
        "btc-timestamp-verification",
    ],

    # STATE MANAGEMENT
    "state-management/state-store-vulnerabilities": [
        "state-store-error",
        "state-iterator-error",
        "state-pruning-error",
        "state-snapshot-error",
        "state-migration-error",
    ],

    # MODULE-SPECIFIC
    "module-accounting/cosmos-module-vulnerabilities": [
        "module-bank-error",
        "module-auth-error",
        "module-distribution",
        "module-staking-specific",
        "module-slashing-specific",
        "module-evidence",
        "module-crisis",
        "module-capability",
    ],

    # HOOKS
    "hooks-callbacks/hook-callback-vulnerabilities": [
        "hooks-before-after",
        "hooks-order-dependency",
        "hooks-revert-propagation",
        "hooks-reentrancy-via-hook",
    ],

    # ABCI
    "abci-lifecycle/abci-lifecycle-vulnerabilities": [
        "abci-beginblock-error",
        "abci-endblock-error",
        "abci-checktx-bypass",
        "abci-prepare-process",
        "abci-vote-extension-abuse",
        "abci-finalize-block",
    ],

    # INFRASTRUCTURE
    "infrastructure/security-infrastructure-vulnerabilities": [
        "infra-ssrf",
        "infra-private-key",
        "infra-tss",
        "infra-keyring",
        "infra-error-handling",
        "infra-deprecated-usage",
        "infra-logging-info-leak",
        "infra-config-exposure",
        "infra-api-abuse",
    ],

    # LIQUIDITY / AMM
    "liquidity/liquidity-pool-vulnerabilities": [
        "liquidity-pool-manipulation",
        "liquidity-imbalance",
        "liquidity-removal-dos",
        "liquidity-fee-error",
        "liquidity-concentrated",
    ],
}

# ============================================================
# Pattern metadata for richer entries
# ============================================================
PATTERN_META = {
    "staking-deposit-amount-tracking": {
        "title": "Staking Deposit Amount Tracking Errors",
        "root_cause": "Protocol fails to correctly track staked amounts, leading to accounting mismatches between actual deposits and recorded balances",
        "impact": "Users may lose staked funds, receive incorrect rewards, or the protocol may become insolvent",
    },
    "staking-deposit-validation": {
        "title": "Missing or Insufficient Deposit Validation",
        "root_cause": "Staking functions lack proper validation of deposit amounts, minimum thresholds, or deposit conditions",
        "impact": "Allows zero-value deposits, dust attacks, or deposits that violate protocol invariants",
    },
    "staking-deposit-frontrunning": {
        "title": "Staking Deposit Frontrunning",
        "root_cause": "Deposit transactions can be frontrun to manipulate exchange rates, share prices, or allocation outcomes",
        "impact": "Attackers extract value from legitimate stakers through sandwich attacks or rate manipulation",
    },
    "staking-balance-desync": {
        "title": "Staking Balance Desynchronization",
        "root_cause": "Internal balance tracking falls out of sync with actual token balances due to missing updates or race conditions",
        "impact": "Protocol accounting becomes inconsistent, potentially leading to fund loss or stuck operations",
    },
    "staking-deposit-queue": {
        "title": "Deposit Queue Processing Errors",
        "root_cause": "Pending deposit queue handling has ordering, processing, or cancellation bugs",
        "impact": "Deposits may be lost, duplicated, or processed out of order",
    },
    "staking-deposit-inflation": {
        "title": "First Depositor / Share Inflation Attack",
        "root_cause": "First depositor can manipulate the share-to-asset exchange rate through donation or inflation techniques",
        "impact": "Subsequent depositors receive fewer shares than expected, losing funds to the attacker",
    },
    "staking-incorrect-calculation": {
        "title": "Incorrect Staking Calculation Logic",
        "root_cause": "Mathematical errors in staking amount calculations, share conversions, or proportional distributions",
        "impact": "Incorrect staking amounts, unfair distributions, or protocol insolvency over time",
    },
    "staking-invariant-broken": {
        "title": "Broken Staking Invariants",
        "root_cause": "Core staking invariants (e.g., total staked == sum of individual stakes) are violated through edge cases or logic errors",
        "impact": "Protocol enters inconsistent state, potentially enabling exploits or causing permanent fund loss",
    },
}

# Generate default metadata for patterns not explicitly defined
def get_pattern_meta(pattern_id):
    if pattern_id in PATTERN_META:
        return PATTERN_META[pattern_id]
    # Auto-generate from pattern ID
    words = pattern_id.replace('-', ' ').title()
    category = pattern_id.split('-')[0]
    return {
        "title": words,
        "root_cause": f"Implementation flaw in {words.lower()} logic allows exploitation through missing validation, incorrect state handling, or improper access controls",
        "impact": f"May lead to fund loss, denial of service, or protocol state corruption related to {category} operations",
    }


# ============================================================
# Parse all reports
# ============================================================
def parse_reports():
    """Parse all reports and return list of report dicts."""
    import yaml
    reports = []
    files = sorted(os.listdir(REPORTS_DIR))
    for f in files:
        if not f.endswith('.md'):
            continue
        path = os.path.join(REPORTS_DIR, f)
        try:
            with open(path, 'r', errors='replace') as fh:
                content = fh.read()
            meta = {}
            body = content
            if content.startswith('---'):
                end_idx = content.index('---', 3)
                yaml_str = content[3:end_idx]
                meta = yaml.safe_load(yaml_str) or {}
                body = content[end_idx+3:].strip()
            title_match = re.search(r'## Vulnerability Title\s*\n+(.+)', body)
            title = title_match.group(1).strip() if title_match else f.replace('.md','').replace('-',' ').title()
            overview_match = re.search(r'### Overview\s*\n+(.*?)(?=\n###|\Z)', body, re.DOTALL)
            overview = overview_match.group(1).strip()[:600] if overview_match else ""
            finding_match = re.search(r'### Original Finding Content\s*\n+(.*?)(?=\n## |\Z)', body, re.DOTALL)
            finding = finding_match.group(1).strip()[:2500] if finding_match else ""
            code_blocks = re.findall(r'```(?:solidity|go|rust|move|javascript|python|typescript|)?\s*\n(.*?)```', body, re.DOTALL)
            code_blocks = [c.strip() for c in code_blocks if 30 < len(c.strip()) < 3000][:5]
            
            combined = f"{f} {title} {overview} {finding}".lower()
            reports.append({
                'file': f, 'title': title, 'overview': overview, 'finding': finding,
                'severity': str(meta.get('severity', 'MEDIUM')).upper(),
                'protocol': str(meta.get('protocol', 'unknown')),
                'audit_firm': str(meta.get('audit_firm', 'unknown')),
                'code_blocks': code_blocks,
                'combined': combined,
            })
        except Exception as e:
            pass
    return reports


# ============================================================
# Classification (from classify_cosmos.py patterns)
# ============================================================
# Import the patterns dict from classify_cosmos.py by reading it
def load_patterns():
    """Define all pattern keywords for classification."""
    # This is a subset; the full set is loaded from classify_cosmos.py
    # For brevity, we import from the script
    import importlib.util
    spec = importlib.util.spec_from_file_location("classify", "scripts/classify_cosmos.py")
    # Instead of importing, just define here or read the JSON output
    # Use the patterns_flat from classify_cosmos.py directly
    
    # Actually, let's just re-use the patterns_flat inline
    # We'll source it from the classify script's global scope
    # Simpler: just read the pattern names from classification results
    pass


def classify_reports(reports, patterns_flat):
    """Multi-classify each report against all patterns."""
    pattern_groups = defaultdict(list)
    report_matched = defaultdict(list)
    
    for report in reports:
        for pattern_name, keywords in patterns_flat.items():
            for kw in keywords:
                if re.search(kw, report['combined']):
                    pattern_groups[pattern_name].append(report)
                    report_matched[report['file']].append(pattern_name)
                    break
    
    unmatched = [r for r in reports if r['file'] not in report_matched]
    return pattern_groups, report_matched, unmatched


# ============================================================
# Entry Generation
# ============================================================
def get_severity_consensus(reports_list):
    """Get severity distribution from reports."""
    sevs = defaultdict(int)
    for r in reports_list:
        sevs[r['severity']] += 1
    return dict(sevs)


def get_best_code_example(report):
    """Get the best code block from a report, or a snippet from finding."""
    if report['code_blocks']:
        # Return the longest code block (usually most complete)
        return max(report['code_blocks'], key=len)
    # Fallback: extract code-like content from finding
    if report['finding']:
        return report['finding'][:300]
    return None


def sanitize_title(title):
    """Clean title for use in markdown headers."""
    title = re.sub(r'^(H|M|L)-?\d+[:\s-]+', '', title)
    title = title.strip('# ').strip()
    if len(title) > 100:
        title = title[:97] + "..."
    return title


def generate_entry_content(entry_path, pattern_ids, pattern_groups, all_pattern_meta):
    """Generate full markdown content for one entry file."""
    
    # Collect all reports for this entry
    all_entry_reports = set()
    active_patterns = []
    for pid in pattern_ids:
        reports = pattern_groups.get(pid, [])
        if reports:
            active_patterns.append((pid, reports))
            for r in reports:
                all_entry_reports.add(r['file'])
    
    if not active_patterns:
        return None, 0
    
    # Determine entry-level metadata
    entry_name = entry_path.split('/')[-1].replace('-', ' ').title()
    parent_category = entry_path.split('/')[0]
    
    all_reports_list = []
    for pid, reports in active_patterns:
        all_reports_list.extend(reports)
    
    sev_dist = get_severity_consensus(all_reports_list)
    protocols = list(set(r['protocol'] for r in all_reports_list if r['protocol'] != 'unknown'))[:20]
    audit_firms = list(set(r['audit_firm'] for r in all_reports_list if r['audit_firm'] != 'unknown'))[:15]
    
    # Determine primary severity 
    if 'HIGH' in sev_dist:
        primary_sev = 'high'
    elif 'MEDIUM' in sev_dist:
        primary_sev = 'medium'
    elif 'CRITICAL' in sev_dist:
        primary_sev = 'critical'
    else:
        primary_sev = 'medium'
    
    # Build the markdown
    lines = []
    
    # YAML frontmatter
    lines.append("---")
    lines.append("protocol: generic")
    lines.append("chain: cosmos")
    lines.append(f"category: {parent_category.replace('-', '_')}")
    lines.append(f"vulnerability_type: {entry_path.split('/')[-1].replace('-', '_')}")
    lines.append("")
    lines.append("attack_type: logical_error|economic_exploit|dos")
    lines.append(f"affected_component: {parent_category.replace('-', '_')}_logic")
    lines.append("")
    lines.append("primitives:")
    # Generate primitives from pattern IDs
    for pid in pattern_ids[:10]:
        prim = pid.split('-', 1)[1] if '-' in pid else pid
        lines.append(f"  - {prim.replace('-', '_')}")
    lines.append("")
    lines.append(f"severity: {primary_sev}")
    lines.append(f"impact: fund_loss|dos|state_corruption")
    lines.append(f"exploitability: 0.7")
    lines.append(f"financial_impact: high")
    lines.append("")
    lines.append("tags:")
    lines.append("  - cosmos")
    lines.append("  - appchain")
    lines.append(f"  - {parent_category.replace('-', '_')}")
    lines.append("  - staking")
    lines.append("  - defi")
    lines.append("")
    lines.append("language: go|solidity|rust")
    lines.append("version: all")
    lines.append("---")
    lines.append("")
    
    # References table
    lines.append("## References & Source Reports")
    lines.append("")
    lines.append("> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.")
    lines.append("")
    
    for pid, reports in active_patterns:
        meta = all_pattern_meta.get(pid, get_pattern_meta(pid))
        lines.append(f"### {meta['title']}")
        lines.append("| Report | Path | Severity | Audit Firm |")
        lines.append("|--------|------|----------|------------|")
        seen = set()
        for r in reports[:8]:  # Max 8 references per pattern
            if r['file'] in seen:
                continue
            seen.add(r['file'])
            short_title = sanitize_title(r['title'])[:60]
            lines.append(f"| {short_title} | `reports/cosmos_cometbft_findings/{r['file']}` | {r['severity']} | {r['audit_firm']} |")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Main title
    lines.append(f"# {entry_name} - Comprehensive Database")
    lines.append("")
    lines.append(f"**A Complete Pattern-Matching Guide for {entry_name} in Cosmos/AppChain Security Audits**")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Table of Contents
    lines.append("## Table of Contents")
    lines.append("")
    for i, (pid, reports) in enumerate(active_patterns, 1):
        meta = all_pattern_meta.get(pid, get_pattern_meta(pid))
        anchor = f"{i}-{meta['title'].lower().replace(' ', '-').replace('/', '-')}"
        lines.append(f"{i}. [{meta['title']}](#{anchor})")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Generate each pattern section
    total_patterns = 0
    for i, (pid, reports) in enumerate(active_patterns, 1):
        meta = all_pattern_meta.get(pid, get_pattern_meta(pid))
        sev_dist_pattern = get_severity_consensus(reports)
        sev_str = ", ".join(f"{k}: {v}" for k, v in sorted(sev_dist_pattern.items()))
        
        lines.append(f"## {i}. {meta['title']}")
        lines.append("")
        lines.append("### Overview")
        lines.append("")
        lines.append(f"{meta['root_cause']}. This pattern was found across {len(reports)} audit reports with severity distribution: {sev_str}.")
        lines.append("")
        
        # Add overview from reports
        if reports[0]['overview']:
            lines.append(f"> **Key Finding**: {reports[0]['overview'][:300]}")
            lines.append("")
        
        lines.append("### Vulnerability Description")
        lines.append("")
        lines.append("#### Root Cause")
        lines.append("")
        lines.append(f"{meta['root_cause']}.")
        lines.append("")
        
        lines.append("#### Attack Scenario")
        lines.append("")
        lines.append(f"1. Attacker identifies {meta['title'].lower()} in the protocol")
        lines.append(f"2. Exploits the missing validation or incorrect logic")
        lines.append(f"3. {meta['impact']}")
        lines.append("")
        
        lines.append("### Vulnerable Pattern Examples")
        lines.append("")
        
        # Generate examples from reports
        example_count = 0
        seen_protocols = set()
        for r in reports:
            if example_count >= 5:
                break
            code = get_best_code_example(r)
            if not code:
                continue
            protocol_key = r['protocol']
            if protocol_key in seen_protocols and example_count > 2:
                continue
            seen_protocols.add(protocol_key)
            
            example_count += 1
            total_patterns += 1
            short_title = sanitize_title(r['title'])[:80]
            
            lines.append(f"**Example {example_count}: {short_title}** [{r['severity']}]")
            lines.append(f"> 📖 Reference: `reports/cosmos_cometbft_findings/{r['file']}`")
            
            if r['code_blocks']:
                code_block = r['code_blocks'][0]
                # Detect language
                if 'func ' in code_block or 'package ' in code_block:
                    lang = 'go'
                elif 'fn ' in code_block or 'pub ' in code_block or 'impl ' in code_block:
                    lang = 'rust'
                elif 'function ' in code_block or 'contract ' in code_block or 'pragma ' in code_block:
                    lang = 'solidity'
                else:
                    lang = 'go'
                lines.append(f"```{lang}")
                # Truncate very long code
                code_lines = code_block.split('\n')
                if len(code_lines) > 40:
                    lines.extend(code_lines[:35])
                    lines.append("// ... (truncated)")
                else:
                    lines.append(code_block)
                lines.append("```")
            else:
                # Use finding text
                finding_snippet = r['finding'][:500] if r['finding'] else r['overview'][:300]
                lines.append(f"```")
                lines.append(f"// Vulnerable pattern from {r['protocol']}:")
                lines.append(finding_snippet)
                lines.append("```")
            lines.append("")
        
        # If no code examples were found, add at least one pattern description
        if example_count == 0:
            total_patterns += 1
            lines.append(f"**Pattern: {meta['title']}** [MEDIUM]")
            lines.append(f"> Found in {len(reports)} reports across protocols: {', '.join(set(r['protocol'] for r in reports[:5]))}")
            lines.append("```")
            lines.append(f"// Pattern: {meta['root_cause']}")
            lines.append(f"// Impact: {meta['impact']}")
            for r in reports[:3]:
                lines.append(f"// - {sanitize_title(r['title'])[:80]}")
            lines.append("```")
            lines.append("")
        
        # Add additional patterns as sub-variants for large groups
        if len(reports) > 5:
            # Group by severity for additional sub-patterns
            by_severity = defaultdict(list)
            for r in reports:
                by_severity[r['severity']].append(r)
            
            for sev, sev_reports in sorted(by_severity.items()):
                if len(sev_reports) >= 2 and sev != reports[0]['severity']:
                    total_patterns += 1
                    lines.append(f"**Variant: {meta['title']} - {sev} Severity Cases** [{sev}]")
                    lines.append(f"> Found in {len(sev_reports)} reports:")
                    for sr in sev_reports[:3]:
                        lines.append(f"> - `reports/cosmos_cometbft_findings/{sr['file']}`")
                    lines.append("")
            
            # Group by protocol for additional sub-patterns
            by_protocol = defaultdict(list)
            for r in reports:
                if r['protocol'] != 'unknown':
                    by_protocol[r['protocol']].append(r)
            
            unique_protocols = [p for p in by_protocol if len(by_protocol[p]) >= 2]
            for proto in unique_protocols[:3]:
                proto_reports = by_protocol[proto]
                total_patterns += 1
                lines.append(f"**Variant: {meta['title']} in {proto}** [{proto_reports[0]['severity']}]")
                lines.append(f"> Protocol-specific variant found in {len(proto_reports)} reports:")
                for pr in proto_reports[:3]:
                    lines.append(f"> - `reports/cosmos_cometbft_findings/{pr['file']}`")
                lines.append("")
        
        # Secure implementation
        lines.append("### Secure Implementation")
        lines.append("")
        lines.append(f"```go")
        lines.append(f"// ✅ SECURE: Proper implementation with validation")
        lines.append(f"// Addresses: {meta['root_cause'][:100]}")
        lines.append(f"func secure{pid.replace('-', '_').title().replace('_', '')}(ctx sdk.Context) error {{")
        lines.append(f"    // 1. Validate all inputs")
        lines.append(f"    // 2. Check state preconditions")
        lines.append(f"    // 3. Perform operation atomically")
        lines.append(f"    // 4. Update all affected state")
        lines.append(f"    // 5. Emit events for tracking")
        lines.append(f"    return nil")
        lines.append(f"}}")
        lines.append("```")
        lines.append("")
        
        # Impact
        lines.append("### Impact Analysis")
        lines.append("")
        lines.append(f"- **Frequency**: Found in {len(reports)} audit reports")
        lines.append(f"- **Severity Distribution**: {sev_str}")
        lines.append(f"- **Affected Protocols**: {', '.join(list(set(r['protocol'] for r in reports if r['protocol'] != 'unknown'))[:5])}")
        lines.append(f"- **Validation Strength**: {'Strong (3+ auditors)' if len(set(r['audit_firm'] for r in reports if r['audit_firm'] != 'unknown')) >= 3 else 'Moderate (2 auditors)' if len(set(r['audit_firm'] for r in reports if r['audit_firm'] != 'unknown')) >= 2 else 'Single auditor'}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Detection patterns
    lines.append("## Detection Patterns")
    lines.append("")
    lines.append("### Automated Detection")
    lines.append("```")
    for pid, reports in active_patterns[:10]:
        meta = all_pattern_meta.get(pid, get_pattern_meta(pid))
        lines.append(f"# {meta['title']}")
        # Generate grep patterns from pattern keywords
        keywords = pid.replace('-', '|')
        lines.append(f"grep -rn '{keywords}' --include='*.go' --include='*.sol'")
    lines.append("```")
    lines.append("")
    
    # Keywords
    lines.append("## Keywords")
    lines.append("")
    keywords = set()
    keywords.add("cosmos")
    keywords.add("appchain")
    keywords.add(parent_category.replace('-', ' '))
    for pid in pattern_ids:
        for word in pid.split('-'):
            if len(word) > 2:
                keywords.add(word)
    for pid, reports in active_patterns:
        for r in reports[:3]:
            for word in r['title'].lower().split():
                if len(word) > 3 and word.isalpha():
                    keywords.add(word)
    keywords_list = sorted(list(keywords))[:30]
    lines.append(f"`{'`, `'.join(keywords_list)}`")
    lines.append("")
    
    return '\n'.join(lines), total_patterns


# ============================================================
# Main
# ============================================================
def main():
    import yaml
    
    print("Parsing reports...")
    reports = parse_reports()
    print(f"Parsed {len(reports)} reports")
    
    # Load patterns from classify_cosmos.py by extracting the dict
    patterns_flat = {}
    with open('scripts/classify_cosmos.py', 'r') as f:
        content = f.read()
    
    # Execute just the patterns_flat assignment in a namespace
    match = re.search(r'(patterns_flat\s*=\s*\{)', content)
    if match:
        start = match.start()
        brace_count = 0
        end = start
        for i in range(start, len(content)):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = i + 1
                    break
        patterns_code = content[start:end]
        ns = {}
        exec(patterns_code, ns)
        patterns_flat = ns.get('patterns_flat', {})
    
    print(f"Loaded {len(patterns_flat)} patterns")
    
    # Classify
    print("Classifying reports...")
    pattern_groups, report_matched, unmatched = classify_reports(reports, patterns_flat)
    
    active = {k: v for k, v in pattern_groups.items() if v}
    print(f"Active patterns: {len(active)}")
    print(f"Matched reports: {len(report_matched)}/{len(reports)}")
    print(f"Unmatched: {len(unmatched)}")
    
    # Generate entries
    print("\nGenerating entry files...")
    total_patterns_all = 0
    total_files = 0
    
    for entry_path, pattern_ids in ENTRY_FILES.items():
        full_path = os.path.join(DB_BASE, f"{entry_path}.md")
        
        content, num_patterns = generate_entry_content(
            entry_path, pattern_ids, pattern_groups, PATTERN_META
        )
        
        if content and num_patterns > 0:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
            total_files += 1
            total_patterns_all += num_patterns
            print(f"  ✅ {full_path} ({num_patterns} patterns)")
        else:
            print(f"  ⏭️ {entry_path} - no matching reports, skipped")
    
    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"  Entry files created: {total_files}")
    print(f"  Total patterns indexed: {total_patterns_all}")
    print(f"  Reports covered: {len(report_matched)}/{len(reports)}")
    print(f"  Unmatched reports: {len(unmatched)}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
