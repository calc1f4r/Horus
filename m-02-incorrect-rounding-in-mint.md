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
solodit_id: 61460
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

[M-02] Incorrect rounding in `mint()`

### Overview


This bug report is about a problem in the `HyperEvmVault` contract's `mint()` function. The function calculates the number of assets by rounding down, which goes against the ERC4626 standard that expects rounding up. This can lead to two issues - it violates the standard and it can be exploited by malicious users to steal funds from other users. The recommendation is to round up instead of rounding down in the `mint()` function.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description
In the `HyperEvmVault` contract, the `mint()` function calculates the number of assets by rounding down:

```solidity
    function mint(uint256 shares, address receiver) public override(ERC4626Upgradeable, IERC4626) nonReentrant returns (uint256 assets) {
        V1Storage storage $ = _getV1Storage();

        if (totalSupply() == 0) {
            // If the vault is empty then we need to initialize last fee collection timestamp
            assets = shares;
            $.lastFeeCollectionTimestamp = uint64(block.timestamp);
        } else {
            uint256 tvl_ = _totalEscrowValue($);
            _takeFee($, tvl_);
            assets = shares.mulDivDown(tvl_, totalSupply());
        }
       --snip--
    }
```
This implementation has two critical issues:

1. Violation of ERC4626 Standard: The ERC4626 standard expects rounding up for `mint` function.

2. Exploitation Risk: A malicious user can exploit this rounding-down mechanism to deposit the minimum amount of assets while minting more shares. This could allow the attacker to steal funds from other users.

## Recommendations

Round up to calculate amount of assets in `mint()` function.





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

