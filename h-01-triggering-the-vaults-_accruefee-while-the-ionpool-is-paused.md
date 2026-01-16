---
# Core Classification
protocol: Ionprotocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36434
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

[H-01] Triggering the vault's `_accrueFee` while the `IonPool` is paused

### Overview


This bug report discusses a problem with the Ion Protocol, specifically with the `IonPool` feature. When the `IonPool` is paused, interest accrual stops and when it is unpaused, all `ilks.lastRateUpdate` will be updated to the current timestamp. However, if the Vault's `_accrueFee` function is triggered while the `IonPool` is paused, it will still calculate interest accrual and mint fee shares. This can lead to incorrect total asset accounting and incorrect amounts of fee shares being minted. The report recommends adding a function to retrieve total underlying claims for each user and incorporating a check to determine if the `IonPool` is paused when calculating total assets. 

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Medium

**Description**

When `IonPool` is paused, interest accrual stops, and when Ion Protocol's unpausing the `IonPool`, all `ilks.lastRateUpdate` will be updated to `block.timestamp`, effectively preventing the protocol from accounting for interest while the pool is paused. However, if Vault's `_accrueFee` is triggered while one of the `IonPool` is paused, it will still calculate interest accrual, account it to total assets, and mint fee shares.

```solidity
    function _accruedFeeShares() internal view returns (uint256 feeShares, uint256 newTotalAssets) {
>>>     newTotalAssets = totalAssets();
        uint256 totalInterest = _zeroFloorSub(newTotalAssets, lastTotalAssets);

        // The new amount of new iTokens that were created for this vault. A
        // portion of this should be claimable by depositors and some portion of
        // this should be claimable by the fee recipient.
        if (totalInterest != 0 && feePercentage != 0) {
            uint256 feeAssets = totalInterest.mulDiv(feePercentage, RAY);

            feeShares =
                _convertToSharesWithTotals(feeAssets, totalSupply(), newTotalAssets - feeAssets, Math.Rounding.Floor);
        }
    }
```

```solidity
    function totalAssets() public view override returns (uint256 assets) {
        uint256 _supportedMarketsLength = supportedMarkets.length();
        for (uint256 i; i != _supportedMarketsLength;) {
            IIonPool pool = IIonPool(supportedMarkets.at(i));

            uint256 assetsInPool =
>>>             pool == IDLE ? BASE_ASSET.balanceOf(address(this)) : pool.getUnderlyingClaimOf(address(this));

            assets += assetsInPool;

            unchecked {
                ++i;
            }
        }
    }
```

It can be observed that `_accrueFee` depends on `totalAssets()` to calculate `newTotalAssets` and `feeShares` for the fee recipient. `totalAssets()` will call `pool.getUnderlyingClaimOf` to calculate assets in each registered pool.

```solidity
    function getUnderlyingClaimOf(address user) public view returns (uint256) {
        RewardTokenStorage storage $ = _getRewardTokenStorage();

        (uint256 totalSupplyFactorIncrease,,,,) = calculateRewardAndDebtDistribution();

>>>     return $._normalizedBalances[user].rayMulDown($.supplyFactor + totalSupplyFactorIncrease);
    }
```

`pool.getUnderlyingClaimOf` will always return assets after considering the increased supply factor, regardless of whether the `IonPool` is currently paused or not. This could lead to incorrect total asset accounting and minting incorrect amounts of fee shares.

**Recommendations**

Consider adding a function inside `IonPool` to retrieve `getTotalUnderlyingClaimsUnaccrued` for each user. Then, incorporate a check to determine whether the `IonPool` is paused when calculating total assets inside the vault. If the pool is paused, utilize that function instead of `getUnderlyingClaimOf`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ionprotocol |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

