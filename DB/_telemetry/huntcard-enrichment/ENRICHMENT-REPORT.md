# Hunt Card Enrichment Inventory

- Manifest source: `DB/manifests/huntcards/all-huntcards.json`
- Cards processed: 1362
- Reports dir: `not provided`
- Cards with unresolved report map: 578
- Report refs by confidence: {'explicit': 2653, 'weak_keyword': 1967}

## Quality Averages

- grep_specificity: 2.999
- detect_correctness: 2.2
- check_actionability: 2.512
- false_positive_guard: 1.003
- impact_clarity: 0.16
- report_support: 1.069
- graph_connectivity: 0.0

## Lowest Scoring Cards

- `general-security-defihacklabs-access-control-2021-2022-pa-static-analysis-003` (4/21): Static Analysis
- `cosmos-frontrunning-mev-vulnerabilities-umee-security-assessment-006` (5/21): Umee Security Assessment
- `bridge-defihacklabs-bridge-2022-patterns-high-signal-grep-seeds-004` (6/21): High-Signal Grep Seeds
- `bridge-defihacklabs-bridge-l2-replay-2022-patte-high-signal-grep-seeds-004` (6/21): High-Signal Grep Seeds
- `bridge-defihacklabs-bridge-patterns-high-signal-grep-seeds-004` (6/21): High-Signal Grep Seeds
- `cosmos-authorization-vulnerabilities-severity-high-risk-003` (6/21): Severity: High Risk
- `cosmos-btc-staking-vulnerabilities-lombard-transfer-signing-strat-005` (6/21): Lombard Transfer Signing Strategy
- `cosmos-consensus-finality-vulnerabilities-severity-medium-risk-013` (6/21): Severity: Medium Risk
- `cosmos-delegation-redelegation-vulnerabilities-denial-of-service-vulnerabilit-003` (6/21): Denial of Service Vulnerability
- `cosmos-frontrunning-mev-vulnerabilities-data-validation-008` (6/21): Data Validation
- `cosmos-fund-theft-vulnerabilities-security-report-005` (6/21): Security Report
- `cosmos-minipool-node-vulnerabilities-severity-medium-risk-009` (6/21): Severity: Medium Risk
- `cosmos-security-infrastructure-vulnerabilities-di-culty-high-001` (6/21): Diculty: High
- `cosmos-security-infrastructure-vulnerabilities-di-culty-high-003` (6/21): Diculty: High
- `cosmos-signature-replay-vulnerabilities-di-culty-high-009` (6/21): Diculty: High
- `cosmos-state-store-vulnerabilities-error-reporting-005` (6/21): Error Reporting
- `cosmos-upgrade-migration-vulnerabilities-error-reporting-001` (6/21): Error Reporting
- `cosmos-upgrade-migration-vulnerabilities-error-reporting-003` (6/21): Error Reporting
- `cosmos-vault-share-vulnerabilities-superform-audit-summary-005` (6/21): Superform Audit Summary
- `general-defi-bonding-curve-misc-vulnerabilities-8-collateral-depeg-cascading-t-007` (6/21): 8. Collateral Depeg Cascading to Bonding Curve

## Unresolved Sample

- `account-abstraction-aa-erc7579-module-system-enable-mode-erc-7579-module-system-registr-000`: ERC-7579 Module System - Registry Bypass, moduleType Confusion, Hook PostCheck Skip, Fallback Flaws (DB/account-abstraction/aa-erc7579-module-system-enable-mode.md:[148, 325])
- `account-abstraction-aa-paymaster-gas-accounting-vulnerabilit-aa-paymaster-gas-accounting-pr-000`: AA Paymaster Gas Accounting - Prefund Errors, Duplicate Snapshots, Stake Bypass, and Fee Escape (DB/account-abstraction/aa-paymaster-gas-accounting-vulnerabilities.md:[145, 300])
- `account-abstraction-aa-session-key-permission-abuse-session-key-abuse-spend-limit--000`: Session Key Abuse - Spend Limit Bypass, Cross-Wallet Consumption, Permission Overwrite, PermissionId Frontrun (DB/account-abstraction/aa-session-key-permission-abuse.md:[133, 333])
- `account-abstraction-aa-signature-replay-attacks-aa-signature-replay-missing-bi-000`: AA Signature Replay - Missing Binding Fields in UserOperation and Enable Mode Hashes (DB/account-abstraction/aa-signature-replay-attacks.md:[133, 310])
- `amm-dos-arithmetic-initialization-secure-pattern-2-consistent-un-002`: Secure Pattern 2: Consistent Underflow Handling (DB/amm/concentrated-liquidity/dos-arithmetic-initialization.md:[545, 566])
- `amm-dos-arithmetic-initialization-secure-pattern-3-first-deposit-003`: Secure Pattern 3: First Depositor Protection (DB/amm/concentrated-liquidity/dos-arithmetic-initialization.md:[567, 595])
- `amm-dos-arithmetic-initialization-secure-pattern-4-bounded-queue-004`: Secure Pattern 4: Bounded Queue with Rate Limiting (DB/amm/concentrated-liquidity/dos-arithmetic-initialization.md:[596, 620])
- `amm-fee-collection-distribution-secure-pattern-3-proportional--003`: Secure Pattern 3: Proportional Fee Collection (DB/amm/concentrated-liquidity/fee-collection-distribution.md:[467, 487])
- `amm-fee-collection-distribution-keywords-008`: Keywords (DB/amm/concentrated-liquidity/fee-collection-distribution.md:[557, 586])
- `amm-liquidity-management-vulnerabilities-secure-pattern-2-per-position--002`: Secure Pattern 2: Per-Position Liquidity Accounting (DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md:[519, 547])
- `amm-price-oracle-manipulation-secure-pattern-1-twap-oracle-w-001`: Secure Pattern 1: TWAP Oracle with Proper Configuration (DB/amm/concentrated-liquidity/price-oracle-manipulation.md:[417, 445])
- `amm-price-oracle-manipulation-secure-pattern-2-dual-price-va-002`: Secure Pattern 2: Dual Price Validation (DB/amm/concentrated-liquidity/price-oracle-manipulation.md:[446, 475])
- `amm-price-oracle-manipulation-secure-pattern-3-sqrtprice-bas-003`: Secure Pattern 3: sqrtPrice-Based Tick Derivation (DB/amm/concentrated-liquidity/price-oracle-manipulation.md:[476, 494])
- `amm-slippage-sandwich-frontrun-vulnerability-title-000`: Vulnerability Title (DB/amm/concentrated-liquidity/slippage-sandwich-frontrun.md:[91, 405])
- `amm-tick-range-position-vulnerabilities-secure-pattern-1-proper-tick-v-001`: Secure Pattern 1: Proper Tick Validation (DB/amm/concentrated-liquidity/tick-range-position-vulnerabilities.md:[290, 301])
- `amm-tick-range-position-vulnerabilities-secure-pattern-2-fee-growth-wi-002`: Secure Pattern 2: Fee Growth with unchecked{} (DB/amm/concentrated-liquidity/tick-range-position-vulnerabilities.md:[302, 312])
- `amm-tick-range-position-vulnerabilities-keywords-008`: Keywords (DB/amm/concentrated-liquidity/tick-range-position-vulnerabilities.md:[387, 416])
- `amm-v4-hook-token-compatibility-secure-pattern-2-robust-token--002`: Secure Pattern 2: Robust Token Transfer Handling (DB/amm/concentrated-liquidity/v4-hook-token-compatibility.md:[611, 637])
- `amm-v4-hook-token-compatibility-secure-pattern-3-gas-optimized-003`: Secure Pattern 3: Gas-Optimized Hook Callbacks (DB/amm/concentrated-liquidity/v4-hook-token-compatibility.md:[638, 668])
- `amm-constant-product-amm-vulnerabilities-13-detection-patterns-audit-ch-012`: 13. Detection Patterns & Audit Checklist (DB/amm/constantproduct/CONSTANT_PRODUCT_AMM_VULNERABILITIES.md:[1435, 1474])
