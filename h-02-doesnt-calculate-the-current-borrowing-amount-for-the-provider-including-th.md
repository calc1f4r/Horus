---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21139
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-lybra
source_link: https://code4rena.com/reports/2023-06-lybra
github_link: https://github.com/code-423n4/2023-06-lybra-findings/issues/723

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
  - wrong_math

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - turvy\_fuzz
  - SpicyMeatball
---

## Vulnerability Title

[H-02] doesn't calculate the current borrowing amount for the provider, including the provider's borrowed shares and accumulated fees due to inconsistency in `collateralRatio` calculation

### Overview


This bug report is about an inconsistency in the calculation of the collateral ratio in the LybraPeUSDVaultBase smart contract. In the `liquidation()` function, the collateral ratio is calculated by taking into account the borrowed amount, borrowed shares, and accumulated fees. However, in the `rigidRedemption()` function, the collateral ratio is calculated by taking into account only the borrowed amount. The tools used for finding the bug were Visual Studio Code. LybraFinance has confirmed the bug and recommended mitigation steps to be consistent with the collateral ratio calculation.

### Original Finding Content


### Lines of code

<https://github.com/code-423n4/2023-06-lybra/blob/main/contracts/lybra/pools/base/LybraPeUSDVaultBase.sol#L127>

### Proof of Concept

Borrowers `collateralRatio` in the `liquidation()` function is calculated by:

```solidity
uint256 onBehalfOfCollateralRatio = (depositedAsset[onBehalfOf] * assetPrice * 100) / getBorrowedOf(onBehalfOf);
```

Notice it calls the `getBorrowedOf()` function, which
calculates the current borrowing amount for the borrower, including the borrowed shares and accumulated fees, not just the borrowed amount.

<https://github.com/code-423n4/2023-06-lybra/blob/main/contracts/lybra/pools/base/LybraPeUSDVaultBase.sol#L253>

```solidity
function getBorrowedOf(address user) public view returns (uint256) {
        return borrowed[user] + feeStored[user] + _newFee(user);
    }
```

However, the providers `collateralRatio` in the `rigidRedemption()` function is calculated by:

<https://github.com/code-423n4/2023-06-lybra/blob/main/contracts/lybra/pools/base/LybraPeUSDVaultBase.sol#L161>

```solidity
uint256 providerCollateralRatio = (depositedAsset[provider] * assetPrice * 100) / borrowed[provider];
```

Here, the deposit asset is divided by only the borrowed amount, missing out on the borrowed shares and accumulated fees.

### Tools Used

Visual Studio Code

### Recommended Mitigation Steps

Be consistent with `collateralRatio` calculation.

**[LybraFinance confirmed](https://github.com/code-423n4/2023-06-lybra-findings/issues/723#issuecomment-1635550670)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | turvy\_fuzz, SpicyMeatball |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-lybra
- **GitHub**: https://github.com/code-423n4/2023-06-lybra-findings/issues/723
- **Contest**: https://code4rena.com/reports/2023-06-lybra

### Keywords for Search

`Wrong Math`

