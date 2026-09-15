---
# Core Classification
protocol: Maple Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54789
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/8ff1bbc8-5f91-4d10-9eea-cc9f88b82e62
source_link: https://cdn.cantina.xyz/reports/cantina_maple_apr2023.pdf
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Christoph Michel
  - Riley Holterhus
  - Jonatas Martins
---

## Vulnerability Title

Reentrant tokens should not be allowed by governance 

### Overview


The bug report discusses an issue with the Open Term Loan protocol where transfers are happening in the middle of the code, which can cause problems with the contract's consistency. This can happen when using certain types of tokens that have a transfer callback function. While there are some safeguards in place, they may not be enough to prevent all potential issues. The report recommends not using tokens with callbacks in the protocol, and the team behind the protocol has acknowledged the issue.

### Original Finding Content

## Context: Open Term Loan

## Description
The protocol doesn't follow the checks-effects-interactions pattern and performs transfers in the middle of it. This can lead to borrowers or other untrusted third parties receiving a callback in the middle of the execution while the contract is in an inconsistent state. These callbacks can happen when using funds tokens that support an ERC777-style transfer callback. While the LoanManager has some reentrancy guards, this is not enough to fully protect against all reentrancy issues that can span across several contracts (Pool, PoolManager, LoanManager, Loan) that are involved in a single call.

## Examples
- The transfer in `OTLoan.makePayment` happens in the middle of the function, after state updates and before the `LoanManager.claim` call. Inside `LoanManager.claim`, the LoanManager reads the loan's state again:
  
  ```solidity
  // this value might not be the one you expect from the call, might have been changed twice in `makePayment` already,
  uint256 principalRemaining_ = ILoanLike(msg.sender).principal();

  // Calculate the original principal to correctly account for removing `unrealizedLosses` when removing the impairment.
  uint256 originalPrincipal_ = uint256(_int256(principalRemaining_) + principal_);
  _accountForLoanImpairmentRemoval(msg.sender, originalPrincipal_);
  ```

One can break the impairment accounting this way by:
1. `makePayment(principalToReturn_ = principal - 1)`. Get control at the transfer here.
2. Reenter with `makePayment(principalToReturn_ = 0)`.
3. `claim` is called and recomputes `principalToReturn_ + L.principal() = 0 + 1 = 1`.
4. Reduces loan impairment by a much smaller amount, LM keeps unrealized losses.

There might be more severe issues like the pool receiving the interest and principal payments from a transfer while LoanManager's `principalOut` is not decreased yet, resulting in an over-approximation of pool assets.

## Recommendation
Tokens with callbacks should not be listed as funds or collateral assets by governance.

## Maple
Business said that there are no plans for a token that implements a callback, so we'll take no action for now.

## Cantina
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Maple Finance |
| Report Date | N/A |
| Finders | Christoph Michel, Riley Holterhus, Jonatas Martins |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_maple_apr2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/8ff1bbc8-5f91-4d10-9eea-cc9f88b82e62

### Keywords for Search

`vulnerability`

