---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40211
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
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
finders_count: 2
finders:
  - cccz
  - Patrick Drotleff
---

## Vulnerability Title

Calculating interest without considering the collateral decimals 

### Overview


The bug report is about a function called outstandingInterestOf() in the Vault.sol code. This function is supposed to convert the interest from TCAP amount to collateral amount, but it does not take into account the decimals of TCAP and collateral. This results in a large interest being calculated when using low-decimal tokens such as USDC/USDT as collateral. 

A proof of concept has been provided to show that when collateral is 6 decimals, the function returns 0.1e18 instead of 0.1e6, and the collateralOf function will underflow. 

The recommendation is to consider the decimals of both TCAP and collateral in the outstandingInterestOf() function. This can be done by adding the assetDecimals variable and multiplying it by 10^assetDecimals. The existing code should be replaced with the new code provided in the recommendation. 

The bug has been fixed in PR 9 by Cryptex and in Cantina Managed.

### Original Finding Content

## Vault.sol Analysis

## Context
Lines: [289-L293]

## Description
The `outstandingInterestOf()` function converts the interest from the TCAP amount to the collateral amount. However, it does not consider TCAP and collateral decimals when converting, which results in a rather large interest calculated when using low-decimal tokens such as USDC/USDT as collateral.

```solidity
function outstandingInterestOf(address user, uint96 pocketId) public view returns (uint256) {
    MintData storage $ = _getVaultStorage().mintData;
    uint256 interestAmount = $.interestOf(_toMintId(user, pocketId));
    return interestAmount * TCAPV2.latestPrice() / latestPrice();
}
```

## Proof of Concept
The proof of concept shows that when collateral is 6 decimals, `outstandingInterest()` returns `0.1e18` (should be `0.1e6`), and `collateralOf` will underflow:

```solidity
function test_poc() public {
    address user = makeAddr("user");
    uint256 amount = 100e6;
    deposit(user, amount);
    vm.prank(user);
    vault.mint(pocketId, 10e18);
    uint timestamp = 365 days;
    vm.warp(timestamp);
    uint256 outstandingInterest = vault.outstandingInterestOf(user, pocketId);
    console.logUint(outstandingInterest); // 0.1e18
    console.logUint(vault.collateralOf(user, pocketId)); // [FAIL. Reason: panic: arithmetic underflow or overflow (0x11)]
}
```

## Recommendation
Consider collateral and TCAP decimals in `outstandingInterestOf()`

```solidity
function outstandingInterestOf(address user, uint96 pocketId) public view returns (uint256) {
    MintData storage $ = _getVaultStorage().mintData;
    uint256 interestAmount = $.interestOf(_toMintId(user, pocketId));
    + uint256 assetDecimals = _getVaultStorage().oracle.assetDecimals();
    + return interestAmount * TCAPV2.latestPrice() * 10 ** assetDecimals / latestPrice() / 10 ** 18;
    - return interestAmount * TCAPV2.latestPrice() / latestPrice();
}
```

## Cryptex
Fixed in PR 9.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | cccz, Patrick Drotleff |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a

### Keywords for Search

`vulnerability`

