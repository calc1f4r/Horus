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
solodit_id: 40213
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
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
finders_count: 2
finders:
  - cccz
  - Patrick Drotleff
---

## Vulnerability Title

Incorrect calculation of interests when taking fee 

### Overview


This bug report discusses an issue with the _takeFee() function in the Vault.sol file. The problem occurs when the interest is greater than the collateral, causing the collateral to be taken as interest. This is due to a flaw in the collateralOf() function, which underflows if the interest is greater than the balance. The recommended solution is to change the function and add a public function to collect the fee. This bug has been fixed in the Cryptex and Cantina Managed commits. It is classified as a low risk issue. 

### Original Finding Content

## Context
**File:** Vault.sol  
**Lines:** 331-333  

## Description
In `_takeFee()`, if the interest is greater than the collateral, the collateral is taken as interest.

```solidity
function _takeFee(IPocket pocket, address user, uint96 pocketId) internal {
    uint256 interest = outstandingInterestOf(user, pocketId);
    uint256 collateral = collateralOf(user, pocketId);
    if (interest > collateral) interest = collateral;
```

The problem here is that the `collateralOf()` function already considers the interest. If the interest is greater than the balance, `collateralOf()` will underflow. Even if the balance is enough to cover the interest, the interest will be lower.

```solidity
function collateralOf(address user, uint96 pocketId) public view returns (uint256) {
    IPocket pocket = _getVaultStorage().pockets[pocketId].pocket;
    return pocket.balanceOf(user) - outstandingInterestOf(user, pocketId);
}
```

For example, if the user has 15 USD balance and 10 USD interest, in `_takeFee()`, `collateralOf()` returns 15 - 10 = 5 USD, which means that only 5 USD interest will be charged, even if the 15 USD balance is enough to pay 10 USD interest.

## Recommendation
Change to:

```solidity
function _takeFee(IPocket pocket, address user, uint96 pocketId) internal {
    uint256 interest = outstandingInterestOf(user, pocketId);
    uint256 collateral = pocket.balanceOf(user);
    // uint256 collateral = collateralOf(user, pocketId);
    if (interest > collateral) interest = collateral;

    VaultStorage storage $ = _getVaultStorage();
    address feeRecipient_ = $.feeRecipient;
    if (interest != 0 && feeRecipient_ != address(0)) {
        pocket.withdraw(user, interest, feeRecipient_);
    }
    $.mintData.resetInterestOf(_toMintId(user, pocketId));
}
```

Also, since `_takeFee()` will only be called in `withdraw()` or `liquidate()`, which prevents the fee from being collected in time, it is recommended to wrap `_takeFee()` in a public function so that anyone can call it to collect the fee.

## Cryptex
Fixed in commit `d1799f6e`.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

