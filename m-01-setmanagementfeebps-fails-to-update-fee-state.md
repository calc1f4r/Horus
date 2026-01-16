---
# Core Classification
protocol: Blueberry_2025-03-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61459
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-03-12.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] `setManagementFeeBps()` fails to update fee state

### Overview


The report states that there is a bug in the `setManagementFeeBps()` function in the `HyperEvmVault` contract that allows the owner to update the management fee rate. However, when the fee rate is changed, the fee state is not updated, which can result in incorrect fee calculations. This is especially problematic for less active vaults. The bug can occur if the fee rate was previously set to 0 for a long period of time and then increased to a higher rate. The contract may then incorrectly calculate fees based on an outdated timestamp, resulting in excessive fee collection. The recommendation is to update the function to reset the fee and update the timestamp when the fee rate is changed.

### Original Finding Content


## Severity

**Impact:** Medium  

**Likelihood:** Medium  

## Description

The `setManagementFeeBps()` function in the `HyperEvmVault` contract allows the owner to update the management fee rate. However, it does not update the fee state (e.g., `lastFeeCollectionTimestamp`) when the fee rate is changed. This can lead to incorrect fee calculations, especially in less active vaults.
```solidity
    function setManagementFeeBps(uint64 newManagementFeeBps_) external onlyOwner {
        require(newManagementFeeBps_ <= BPS_DENOMINATOR, Errors.FEE_TOO_HIGH());
        _getV1Storage().managementFeeBps = newManagementFeeBps_;
    }
```

If the fee rate was previously set to 0 for an extended period (e.g., 1 year to attract users), the `lastFeeCollectionTimestamp` could be set in a long time ago. After increasing the fee rate (e.g., to 0.01%), the contract may incorrectly calculate fees based on the entire time elapsed since the outdated `lastFeeCollectionTimestamp`, leading to excessive fee collection.

## Recommendations

Update the `setManagementFeeBps()` function to take the fee and reset the `lastFeeCollectionTimestamp` when the fee rate is changed.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Blueberry_2025-03-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-03-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

