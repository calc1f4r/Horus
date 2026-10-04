---
# Core Classification
protocol: Parcel
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54848
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/78a11a56-9b3d-4584-9c0c-b67194c5238a
source_link: https://cdn.cantina.xyz/reports/cantina_parcel_feb2023.pdf
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
finders_count: 3
finders:
  - Christos Pap
  - Krum Pashov
  - Gerard Persoon
---

## Vulnerability Title

Order of execTransactionFromGnosis() and initialBalances() is reversed 

### Overview


The bug report describes an issue in the `PayrollManager.sol` file, specifically in lines 139-244. The function `executePayroll()` is not working as intended and allows for tokens to be stolen. The current workaround is not ideal and can cause tokens to get stuck. The recommendation is to make some changes to the code to fix the issue and make it more secure. This issue has been verified by Cantina Security.

### Original Finding Content

## Context
**File:** `PayrollManager.sol`  
**Line Numbers:** 139-244

## Description
The function `executePayroll()` first pulls ETH/tokens and then determines initial balances. It transfers ETH/tokens out and checks balances again. The before and after balances can only be equal if no ETH/tokens have been transferred, which is not the intended behavior. 

The after-balance check for tokens is `<`, which seems to be a workaround to get tests working. This way, tokens that are previously stored in the contract are used and can be stolen. This is also unwanted, although normally there shouldn't be tokens left in the contract.

```solidity
function executePayroll(...) {
    ...
    for (uint256 index = 0; index < paymentTokens.length; index++) {
        execTransactionFromGnosis(...);
    }
    for (uint256 i = 0; i < paymentTokens.length; i++) {
        ... initialBalances[i] = ...
    }
    ...
    // send ETH / tokens to recepient
    ...
    for (uint256 i = 0; i < paymentTokens.length; i++) {
        ...
        if (...) {
            require(address(this).balance == initialBalances[i], ...);
        } else if (IERC20(paymentTokens[i]).balanceOf(address(this)) > initialBalances[i]) {
            revert("CS018");
        }
    }
}
```

## Recommendation
Strict checks are not necessary when using the recommendations for the following issues:
- Use separate contracts for each Gnosis safe
- Token retrieval not linked to signed transactions
- ETH and tokens can get stuck 

Otherwise, determine the initial balances before `execTransactionFromGnosis()`. Change the tokens check to a strict check. So change the code to something like the following:

```solidity
function executePayroll(...) {
    ...
    + for (uint256 i = 0; i < paymentTokens.length; i++) {
    +     ... initialBalances[i] = ...
    + }
    for (uint256 index = 0; index < paymentTokens.length; index++) {
        execTransactionFromGnosis(...);
    }
    - for (uint256 i = 0; i < paymentTokens.length; i++) {
    -     ... initialBalances[i] = ...
    - }
    ...
    // send ETH / tokens to recepient
    ...
    for (uint256 i = 0; i < paymentTokens.length; i++) {
        ...
        if (...) {
            require(address(this).balance == initialBalances[i], ...);
        } else
            - if (IERC20(paymentTokens[i]).balanceOf(address(this)) > initialBalances[i]) {
            + if (IERC20(paymentTokens[i]).balanceOf(address(this)) != initialBalances[i]) {
                revert("CS018");
            }
        }
    }
}
```

## Parcel
This issue is made redundant by the Proxy pattern and a redesign of `executePayroll()`.

## Cantina Security
**Status:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Parcel |
| Report Date | N/A |
| Finders | Christos Pap, Krum Pashov, Gerard Persoon |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_parcel_feb2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/78a11a56-9b3d-4584-9c0c-b67194c5238a

### Keywords for Search

`vulnerability`

