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
solodit_id: 63296
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

[M-06] `_getRewardsAmountPerVault` might be using an outdated vault power

### Overview


This bug report talks about a problem in Symbiotic, which is a platform for staking cryptocurrency. The problem is that if a vault is slashed (meaning a penalty is imposed) in the current epoch, its active stake (the amount of cryptocurrency being staked) is immediately reduced. However, in the current implementation, the power of different vaults (the influence they have in the platform) is still calculated based on the power weights at the beginning of the epoch. This means that if a vault is slashed during an epoch, its rewards should be reduced, but in Symbiotic, its rewards remain unchanged. The recommendation is to calculate power using the timestamp starting from the current eraIndex.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** Low

## Description

In Symbiotic, if a vault is slashed in the current epoch, its `activeStake` will be immediately reduced:
```solidity
// https://github.com/symbioticfi/core/blob/main/src/contracts/vault/Vault.sol#L237
            if (slashedAmount > 0) {
                uint256 activeSlashed = slashedAmount.mulDiv(activeStake_, slashableStake);
                uint256 nextWithdrawalsSlashed = slashedAmount - activeSlashed;

                _activeStake.push(Time.timestamp(), activeStake_ - activeSlashed);
                withdrawals[captureEpoch + 1] = nextWithdrawals - nextWithdrawalsSlashed;
            }
```

However, in the current Tanssi implementation, regardless of how many times `_distributeRewardsToStakers` is called in an epoch, the power of different vaults is still calculated based on the power weights at the beginning of the epoch:

```solidity
//ODefaultOperatorRewards.sol::L242
        uint256[] memory amountPerVault = _getRewardsAmountPerVault(
            operatorVaults, totalVaults, epochStartTs, operator, middlewareAddress, stakerAmount
        );
```

This means that if a vault is slashed during an epoch, the rewards it deserves should be reduced in the consensus layer of the Tanssi mainnet, but in Symbiotic, its rewards remain unchanged.

## Recommendations

Calculate power using the timestamp starting from the current eraIndex.





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

