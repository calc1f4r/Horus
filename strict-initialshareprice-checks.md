---
# Core Classification
protocol: Hyperdrive June 2023
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35864
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Saw-Mon and Natalie
  - Christoph Michel
  - Deivitto
  - M4rio.eth
---

## Vulnerability Title

Strict initialSharePrice checks

### Overview


The bug report describes a medium risk issue in the ERC4626Hyperdrive and StethHyperdrive smart contracts. These contracts check for a specific initial share price that matches the current share price of the yield source. However, due to the constant accrual of interest and the ability for the share price to be manipulated, it is difficult for the deployment to accurately predict and provide the correct share price. This can result in the deployment failing and causing a denial-of-service attack. The recommendation is to remove this attack vector by having the factory fetch the current share price instead of relying on the user to provide it. 

### Original Finding Content

## Risk Assessment Report

## Severity
**Medium Risk**

## Context
- `ERC4626Hyperdrive.sol#L40`
- `StethHyperdrive.sol#L44`

## Description
The `ERC4626Hyperdrive` and `StethHyperdrive` constructors check that the provided `initialSharePrice` exactly matches the current share price of the yield source:

```solidity
uint256 shareEstimate = _pool.convertToShares(FixedPointMath.ONE_18);
if (
    _config.initialSharePrice !=
    FixedPointMath.ONE_18.divDown(shareEstimate)
) {
    revert Errors.InvalidInitialSharePrice();
}
```

It's easy for the deployment to revert here because estimating the exact share price when the transaction is mined is very hard, as the yield sources can accrue new interest every block. Furthermore, the share price of the yield source can usually be manipulated by donating to the vault, which allows an attacker to frontrun the deployment with a tiny donation such that the strict equality check fails.

## Recommendation
Consider removing this denial-of-service attack vector. For example, the factory could fetch the current share price and set it on the config instead of the user having to predict and provide it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Hyperdrive June 2023 |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Christoph Michel, Deivitto, M4rio.eth |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf

### Keywords for Search

`vulnerability`

