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
solodit_id: 54851
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/78a11a56-9b3d-4584-9c0c-b67194c5238a
source_link: https://cdn.cantina.xyz/reports/cantina_parcel_feb2023.pdf
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
finders_count: 3
finders:
  - Christos Pap
  - Krum Pashov
  - Gerard Persoon
---

## Vulnerability Title

Several issues with strict after balances check in executePayroll() 

### Overview


The report discusses issues with the pattern used to check balances in the `executePayroll()` function in the PayrollManager.sol file, specifically lines 139-244. The report notes that the fix for a previous issue has been applied. However, there are still problems with the balance check, including the possibility of incorrect balances when using certain types of tokens and the potential for malicious external contracts to interfere with payments. The report suggests implementing recommendations from other issues to address these problems. The issue has been verified by Cantina Security and a redesign has been proposed in a pull request.

### Original Finding Content

## PayrollManager.sol Analysis

## Context
**File:** PayrollManager.sol  
**Line Range:** L139-L244

## Description
The pattern to check for exact balances in `executePayroll()` has some notable issues. This analysis assumes that the fix for the issue "Order of `execTransactionFromGnosis()` and `initialBalances()` is reversed" has been applied. The following issues are observed:

- If a token with a transfer fee or a rebalancing token is used, the balances will not match exactly.
- If one of the external contracts called (for example, an ETH recipient or a callback of an ERC777 token) is malicious, it could transfer some ETH or tokens back to the contract, which would revert the call. This could severely hinder the payments.
- The balance check doesn't protect against over- or under-payments because a front runner could call the function `executePayroll()` with updated values for `paymentTokens[]` and `payoutAmounts[]` that satisfy the end check.

### Code Snippet
```solidity
function executePayroll(...) ... {
    ...
    for (uint256 i = 0; i < paymentTokens.length; i++) {
        ... initialBalances[i] = ...
    }
    for (uint256 index = 0; index < paymentTokens.length; index++) {
        execTransactionFromGnosis(...);
    }
    ...
    // send ETH / tokens to recipient
    ...
    for (uint256 i = 0; i < paymentTokens.length; i++) {
        ...
        if (...) {
            require(address(this).balance == initialBalances[i], ...);
        } else if (IERC20(paymentTokens[i]).balanceOf(address(this)) != initialBalances[i]) {
            revert("CS018");
        }
    }
}
```

## Recommendation
To address the issues identified, consider implementing the recommendations from the following issues:
- "Use separate contracts for each Gnosis safe";
- "Token retrieval not linked to signed transactions";
- "ETH and tokens can get stuck".

## Parcel
This has been redesigned using a proxy pattern in PR 53.

## Cantina Security
**Status:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

