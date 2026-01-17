---
# Core Classification
protocol: Sturdy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54508
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7dae5fff-ba32-4207-9843-c607f15464a3
source_link: https://cdn.cantina.xyz/reports/cantina_sturdy_sep2023.pdf
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

protocol_categories:
  - liquid_staking
  - lending
  - bridge
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Manuel
  - HickupHH3
---

## Vulnerability Title

Collateral & debt position may be accounted to SiloGateway instead of user 

### Overview


This bug report is about a function called `borrowAsset()` in a file called `SiloGateway.sol`. This function is supposed to add collateral and borrow an asset for the user, but it may not work properly with some protocols. One example is `FraxLend`, where the user's collateral can get permanently locked up even after the debt is repaid. The recommendation is to carefully check protocols to make sure they support borrowing on behalf of the user. The bug has been acknowledged and will be addressed in future versions of the software.

### Original Finding Content

## SiloGateway Documentation

## Context
**File**: SiloGateway.sol  
**Lines**: 92-96

## Description
The `borrowAsset()` function is intended to add collateral and borrow the asset on behalf of the user. However, this feature may not be supported by some protocols. For instance, certain protocols may accrue the collateral and debt to the caller, specifically, the `SiloGateway`.

An example of this is `FraxLend`, which was one of the protocols used for end-to-end tests. Below is a code snippet taken from the `borrowAsset()` function of `FraxLendPair`:

```solidity
if (_collateralAmount > 0) {
    _addCollateral(msg.sender, _collateralAmount, msg.sender);
}

function _addCollateral(
    address _sender,
    uint256 _collateralAmount,
    address _borrower
) internal {
    userCollateralBalance[_borrower] += _collateralAmount;
}
```

This results in the user's collateral being permanently locked up, even if the debt is repaid on behalf of the contract.

## Recommendation
Protocols need to be carefully checked to ensure that borrowing on behalf of the user is supported.

## Sturdy
**Status**: Acknowledged  
(See commit b0a71073.) We will use this contract when we deploy our Sturdy V2 silos, which have the feature of borrowing on behalf of the user, or implement another gateway contract for the Aave V3 and Compound V3 silos.

## Cantina
**Status**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sturdy |
| Report Date | N/A |
| Finders | Manuel, HickupHH3 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sturdy_sep2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7dae5fff-ba32-4207-9843-c607f15464a3

### Keywords for Search

`vulnerability`

