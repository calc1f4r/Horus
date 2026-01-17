---
# Core Classification
protocol: Synonym
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47857
audit_firm: OtterSec
contest_link: https://synonym.to/
source_link: https://synonym.to/
github_link: https://github.com/SynonymFinance/smart-contracts/

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
finders_count: 4
finders:
  - Nicholas R. Putra
  - OtterSec
  - Woosun Song
  - Robert Chen
---

## Vulnerability Title

Double Normalization

### Overview


The getCurrentAccrualIndices function in HubInterestUtilities is used to calculate the interest accrual indices for a specific asset. However, there is a bug where the values for deposited and borrowed assets are being double normalized, leading to incorrect results in interest calculations. This bug has been fixed in version 3b54128 and the function should now directly use the values from storage without double normalizing them.

### Original Finding Content

## getCurrentAccrualIndices Function

The `getCurrentAccrualIndices` function within `HubInterestUtilities` calculates a given asset’s current interest accrual indices. The values of deposited and borrowed assets are fetched from storage, where they are stored in a normalized form. Subsequently, they are normalized a second time, as seen below.

## Solidity Code

```solidity
// contracts/lendingHub/HubInterestUtilities.sol
function getCurrentAccrualIndices(address assetAddress) public view 
    returns(AccrualIndices memory) {
    uint256 lastActivityBlockTimestamp =
        getLastActivityBlockTimestamp(assetAddress);
    uint256 secondsElapsed = block.timestamp - lastActivityBlockTimestamp;
    uint256 deposited = getTotalAssetsDeposited(assetAddress);
    AccrualIndices memory accrualIndices = getInterestAccrualIndices(assetAddress);
    if ((secondsElapsed != 0) && (deposited != 0)) {
        uint256 borrowed = getTotalAssetsBorrowed(assetAddress);
        uint256 normalizedDeposited =
            normalizeAmount(deposited, accrualIndices.deposited, Round.DOWN);
        uint256 normalizedBorrowed =
            normalizeAmount(borrowed, accrualIndices.borrowed, Round.DOWN);
        [...]
    }
}
```

## Issue

This double normalization introduces an issue where the calculated `normalizedDeposited` and `normalizedBorrowed` values are not representative of the actual deposited and borrowed asset amounts. Any interest calculations or updates to interest accrual indices that rely on these double-normalized values will yield incorrect results.

## Remediation

Ensure `getCurrentAccrualIndices` does not double normalize deposited and borrowed values. Instead, it should directly utilize the values fetched from storage, assuming they are already in a normalized form.

## Patch

Fixed in commit `3b54128`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Synonym |
| Report Date | N/A |
| Finders | Nicholas R. Putra, OtterSec, Woosun Song, Robert Chen |

### Source Links

- **Source**: https://synonym.to/
- **GitHub**: https://github.com/SynonymFinance/smart-contracts/
- **Contest**: https://synonym.to/

### Keywords for Search

`vulnerability`

