---
# Core Classification
protocol: Tanssi_2025-04-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63294
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tanssi-security-review_2025-04-30.md
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

[M-04] Vault curator can force `operator.claimReward()` to revert with precision

### Overview


This report describes a bug where a vault curator can allocate a very small amount of stake to an operator, resulting in a reward amount of zero. This can cause the operator to be unable to claim their rewards and block other vaults associated with the operator from receiving their share of the rewards. To fix this, safeguards should be implemented to skip vaults with zero reward amounts and set a minimum stake threshold to avoid precision-based exploits.

### Original Finding Content


## Severity

**Impact:** High  

**Likelihood:** Low

## Description

A vault curator can allocate a **very small amount** of stake to an operator. Due to precision loss (e.g., rounding errors) in `_getRewardsAmountPerVault()`, the vault may end up with a **reward amount of zero**.
```solidity
    function _getRewardsAmountPerVault(
        address[] memory operatorVaults,
        uint256 totalVaults,
        uint48 epochStartTs,
        address operator,
        address middlewareAddress,
        uint256 stakerAmount
    ) private view returns (uint256[] memory amountPerVault) {
        --Snipped--
        for (uint256 i; i < totalVaults;) {
            uint256 amountForVault;
            // Last vault gets the remaining amount
            if (i == totalVaults - 1) {
                amountForVault = stakerAmount - distributedAmount;
            } else {
@>              amountForVault = vaultPowers[i].mulDiv(stakerAmount, totalPower);
            }
            amountPerVault[i] = amountForVault;
            unchecked {
                distributedAmount += amountForVault;
                ++i;
            }
        }
    }
```
When the operator later calls `claimReward()`, it triggers `vault.distributeRewards()` and then `_transferAndCheckAmount()` for each vault. If the calculated reward amount for a vault is zero, the `_transferAndCheckAmount()` function can **revert**, causing the **entire claim transaction to fail**.

As a result:
- The operator is **unable to claim their rewards**.
- Other vaults associated with the operator are also blocked from receiving their share of the rewards.

## Recommendations
Implement safeguards to:
- **Skip vaults** with zero reward amounts during distribution.
- **Set a minimum stake threshold** to avoid precision-based exploits..





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tanssi_2025-04-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tanssi-security-review_2025-04-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

