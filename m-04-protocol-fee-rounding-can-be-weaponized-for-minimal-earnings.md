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
solodit_id: 61462
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

[M-04] Protocol fee rounding can be weaponized for minimal earnings

### Overview


The report discusses a bug in the `_previewFeeShares` and `_takeFee` functions of the protocol. These functions calculate and convert fees to shares, but the rounding direction specified is not being used. This can lead to a situation where fees are repeatedly taken without actually minting any shares, due to rounding down to 0. The report recommends rounding up fees in the protocol's favor or updating the `lastFeeCollectionTimestamp` only if shares are actually minted.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** Low

## Description

In `_previewFeeShares` and `_takeFee`, we can see that after calculating the fee assets that the protocol is entitled to, a conversion of the assets is made to fees, via the `_convertToShares` functions. Observe the specified, albeit unused rounding direction.

```solidity
    function _previewFeeShares(V1Storage storage $, uint256 tvl_) internal view returns (uint256) {
        uint256 expectedFee = _calculateFee($, tvl_);
@>1     return _convertToShares(expectedFee, Math.Rounding.Floor);
    }

    /**
     * @notice Takes the management fee from the vault
     * @dev There is a 0.015% annual management fee on the vault's total assets.
     * @param grossAssets The total value of the vault
     * @return The amount of fees to take in underlying assets
     */
    function _takeFee(V1Storage storage $, uint256 grossAssets) private returns (uint256) {
        uint256 feeTake_ = _calculateFee($, grossAssets);

        // Only update state if there's a fee to take
        if (feeTake_ > 0) {
            $.lastFeeCollectionTimestamp = uint64(block.timestamp);
@>2         uint256 sharesToMint = _convertToShares(feeTake_, Math.Rounding.Floor);
            _mint($.feeRecipient, sharesToMint);
        }
        return feeTake_;
    }

```

`_convertToShares` performs the `mulDivDown` operation on returned fee assets to return the shares the protocol is entitled to.

```solidity
    function _convertToShares(uint256 assets, Math.Rounding /*rounding*/ ) internal view override returns (uint256) {
@>3     return assets.mulDivDown(totalSupply(), tvl());
    }
```

And this fee asset is calculated, time-based in `_calculateFee` as below:

```solidity
    function _calculateFee(V1Storage storage $, uint256 grossAssets) internal view returns (uint256 feeAmount_) {
        if (grossAssets == 0 || block.timestamp <= $.lastFeeCollectionTimestamp) {
            return 0;
        }

        // Calculate time elapsed since last fee collection
@>4     uint256 timeElapsed = block.timestamp - $.lastFeeCollectionTimestamp;

        // We subtract the pending redemption requests from the total asset value to avoid taking more fees than needed from
        //    users who do not have any pending redemption requests
        uint256 eligibleForFeeTake = grossAssets - $.totalRedeemRequests;
        // Calculate the pro-rated management fee based on time elapsed
@>5     feeAmount_ = eligibleForFeeTake * $.managementFeeBps * timeElapsed / BPS_DENOMINATOR / ONE_YEAR;

        return feeAmount_;
    }
```

So, in a dedicated attack (e.g via a script), in which a function that triggers `_takeFee` (e.g `transfer`) is repeatedly called every certain `timeElapsed` from `lastFeeCollectionTimestamp` (e.g 10 seconds) such that the returned value of `feeAmount_` is greater than 0 but still small enough that converting it to shares i.e multiplying it by `totalSupply()` will be less than `tvl()` and due to `mulDivDown` will round down to 0. Even though no fee shares are minted, the `lastFeeCollectionTimestamp` will still be updated, making a repetition of the attack viable. Note also legitimate transactions that occur between this `timeElapsed` also trigger this situation. 

```solidity
    function _takeFee(V1Storage storage $, uint256 grossAssets) private returns (uint256) {
        uint256 feeTake_ = _calculateFee($, grossAssets);

        // Only update state if there's a fee to take
        if (feeTake_ > 0) {
@>6         $.lastFeeCollectionTimestamp = uint64(block.timestamp);
            uint256 sharesToMint = _convertToShares(feeTake_, Math.Rounding.Floor);
            _mint($.feeRecipient, sharesToMint);
        }
        return feeTake_;
    }

```

## Recommendations

1. As a rule in DeFi, protocol fees should always round up in its favour.
2. If the recommendation above is not to be implemented, `lastFeeCollectionTimestamp` can be updated instead but only if `sharesToMint` > 0.





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

