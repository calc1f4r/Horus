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
solodit_id: 61461
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

[M-03] Wrong fee share calculations in `_takeFee()`

### Overview


The `HyperEvmVault` contract has a function called `_takeFee()` which is used to calculate and collect management fees from the vault. However, there is a bug in the code where the function uses the total assets, including the current fee assets, to calculate the fee shares. This results in the fee being taken from already collected fee assets, leading to a lower fee amount than intended. To fix this, the code should use the total fee amount and total fee shares when calculating the fee shares to mint.

### Original Finding Content


## Severity

**Impact:** Medium  

**Likelihood:** Medium  

## Description
In the `HyperEvmVault` contract, the `_takeFee()` function is used to calculate and collect management fees from the vault. The function calculates the fee amount and mints corresponding shares to the `feeRecipient` to deduct the fee from **depositors**. 

```solidity
function _takeFee(V1Storage storage $, uint256 grossAssets) private returns (uint256) {
    uint256 feeTake_ = _calculateFee($, grossAssets);

    // Only update state if there's a fee to take
    if (feeTake_ > 0) {
        $.lastFeeCollectionTimestamp = uint64(block.timestamp);
        uint256 sharesToMint = _convertToShares(feeTake_, Math.Rounding.Floor);
        _mint($.feeRecipient, sharesToMint);
    }
    return feeTake_;
}

function _convertToShares(uint256 assets, Math.Rounding /*rounding*/ ) internal view override returns (uint256) {
    return assets.mulDivDown(totalSupply(), tvl());
}

```
The issue arises in using `_convertToShares()` function to calculate the fee shares. It uses the total assets (`tvl()`) which includes the current fee assets, meaning the fee is taken from already collected fee assets too. As a result, the fee taken will be less than the intended amount.

## Recommendations
To calculate new fee shares to mint, consider the total fee amount and total fee shares. Code should use `tvl() - feeTake_` as total assets when calculating fee share.





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

