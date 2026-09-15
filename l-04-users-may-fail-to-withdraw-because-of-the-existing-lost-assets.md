---
# Core Classification
protocol: AmpleEarn_2025-12-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64046
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/AmpleEarn-security-review_2025-12-12.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-04] Users may fail to withdraw because of the existing lost assets

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

AmpleEarn will distribute users' deposit into different strategy vaults to earn interest.
When the strategy vault loses funds, the share price will not be impacted by the actual lose. This will cause the share price will be higher than the actual price. When users want to withdraw assets with the share price, users can fail to withdraw assets.

For example:

- Alice deposits 1000 assets, and Alice will get 1000 shares.

- The vault category loses 400 assets. So the real total assets are 600. The last total assets are 1000.

- Bob deposits 1000 assets, and Bob will get 1000 shares. 

- Alice withdraws 1000 shares, she can get 1000 assets based on the current share price.

- Bob wants to withdraw all shares, the withdrawal will be reverted because there is not enough balance.

```solidity
    function _accrueInterest() internal {
        // The total assets are not the actual real assets for this vault.
        (uint256 feeShares, uint256 newTotalAssets, uint256 newLostAssets) = _accruedFeeAndAssets();
        _updateLastTotalAssets(newTotalAssets);
    }
    function _accruedFeeAndAssets()
        internal
        view
        returns (uint256 feeShares, uint256 newTotalAssets, uint256 newLostAssets)
    {
        // The assets that the Earn vault has on the strategy vaults.
        uint256 realTotalAssets;
        // All vaults must exist in this withdraw queue.
        for (uint256 i; i < withdrawQueue.length; ++i) {
            IERC4626 id = withdrawQueue[i];
            realTotalAssets += expectedSupplyAssets(id);
        }
        uint256 lastTotalAssetsCached = lastTotalAssets;
        // initially, the lostAssets is 0. 
        // lastTotalAssetsCached - lostAssets is actually the last real total assets.
        if (realTotalAssets < lastTotalAssetsCached - lostAssets) {
            newLostAssets = lastTotalAssetsCached - realTotalAssets;
        } else {
            newLostAssets = lostAssets;
        }

@>        newTotalAssets = realTotalAssets + newLostAssets;
        uint256 totalInterest = newTotalAssets - lastTotalAssetsCached;
    }
```

**Recommendations**

Process the lost assets properly.




### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | AmpleEarn_2025-12-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/AmpleEarn-security-review_2025-12-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

