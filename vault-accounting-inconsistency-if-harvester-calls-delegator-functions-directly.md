---
# Core Classification
protocol: Affine Labs - UltraETH LRT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59385
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/affine-labs-ultra-eth-lrt/f1c58be1-9f7a-4716-b96a-6d38816396d2/index.html
source_link: https://certificate.quantstamp.com/full/affine-labs-ultra-eth-lrt/f1c58be1-9f7a-4716-b96a-6d38816396d2/index.html
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
finders_count: 3
finders:
  - Andy Lin
  - Hytham Farah
  - Gelei Deng
---

## Vulnerability Title

Vault Accounting Inconsistency if Harvester Calls Delegator Functions Directly

### Overview


The report discusses a bug in the `AffineDelegator` implementation that can cause accounting errors in the `UltraLRT` vault contract. The bug occurs when the harvester calls functions on the delegator directly, instead of going through the vault. This leads to discrepancies in the recorded balances, resulting in an incorrect conversion rate of shares to asset amounts. The team is recommended to clarify the necessity of this feature and implement a better mechanism to ensure the vault and delegators are in sync.

### Original Finding Content

**Update**
We reviewed the fix and confirmed that the team made the following changes to resolve the issue:

*   `delegate()` function now transfers tokens from `msg.sender` instead of the vault
*   The `withdraw()` function is restricted to the vault

![Image 16: Alert icon](https://certificate.quantstamp.com/full/affine-labs-ultra-eth-lrt/f1c58be1-9f7a-4716-b96a-6d38816396d2/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Fixed by the clients: Addressed in: `136628ef7790204f3885457117fba0094c931fb7`. The client provided the following explanation:

> Delegator will transfer assets from msg.sender. This will open access to delegateTo function.

**File(s) affected:**`UltraLRT`, `AffineDelegator`, `EigenDelegator`, `SymbioticDelegator`

**Description:** The `AffineDelegator` implementation includes the modifier `onlyVaultOrHarvester()`, which checks if the `msg.sender` is the vault or the harvester for several functions. However, the `UltraLRT` vault contract has its own variables for accounting changes to the delegators. If the delegators are changed without going through the vault functions, this can lead to accounting errors.

1.   The `UltraLRT.delegateToDelegator()` function updates the `delegatorMap` and `delegatorAssets`. If the harvester calls `AffineDelegator.delegate()` directly, these updates will not be recorded.
2.   The `UltraLRT._getDelegatorLiquidAssets()` function records the balances of `delegatorAssets` and `delegatorMap`. Similarly, if the harvester calls `AffineDelegator.withdraw()` directly, these changes will not be recorded.

In the second case, `delegatorAssets` will not record the change from the `withdraw()` function, causing `totalAssets()` to falsely assume it has more assets than it actually does. This discrepancy will result in an incorrect conversion rate of shares to asset amounts.

**Recommendation:** The team should first clarify if it is necessary to allow the harvester to call functions on the delegator without going through the vault. If not, consider removing this feature. If it is necessary, implement a better mechanism to ensure the vault and the delegators remain in sync.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Affine Labs - UltraETH LRT |
| Report Date | N/A |
| Finders | Andy Lin, Hytham Farah, Gelei Deng |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/affine-labs-ultra-eth-lrt/f1c58be1-9f7a-4716-b96a-6d38816396d2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/affine-labs-ultra-eth-lrt/f1c58be1-9f7a-4716-b96a-6d38816396d2/index.html

### Keywords for Search

`vulnerability`

