---
# Core Classification
protocol: August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38519
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/august/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/august/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Two nonReentrancy Modiﬁers Prevent liquidate() Execution

### Overview


This bug report describes an issue where two nonReentrant modifiers are being executed in a single call, causing the ReentrancyGuard to revert during the liquidate() function. This occurs because the _reentrancyStatus is set to _REENTRANCY_ENTERED in step (1) and then a call is made to the lender contract in step (3), causing a revert on the _nonReentrantBefore() function. This prevents the liquidate() function from being called and can result in losses at the pool level. The recommendation is to remove one of the nonReentrant modifiers on either the AbstractLender or HookableLender contract, which was eventually resolved in a commit.

### Original Finding Content

## Description

Two `nonReentrant` modifiers are executed in a single call, causing `ReentrancyGuard` to revert during `liquidate()`.

When the function `AbstractLender.liquidate()` is called, the following call sequence occurs:

1. `AbstractLender.liquidate()` is called on the lender contract. The function has a `nonReentrant` modifier. At this point, `_reentrancyStatus` is set to `_REENTRANCY_ENTERED`.
2. `IPeerToPeerOpenTermLoan(loanAddr).liquidate()` is called on the respective loan contract. This code may execute `InitializableOpenTermLoan.liquidate()`.
3. `IHookableLender(lender).notifyLoanMatured()` is called on the lender contract. The function has a `nonReentrant` modifier as described in `HookableLender.sol`.

Since the `_reentrancyStatus` of the lender contract was already set to `_REENTRANCY_ENTERED` in step (1), the call in step (3) would cause a revert on `BaseReentrancyGuard._nonReentrantBefore()`. The result is that `AbstractLender.liquidate()` will revert.

The impact is rated as medium severity as being unable to call `liquidate()` prevents losses from being accounted for at the pool level.

## Recommendations

Consider removing one of the `nonReentrant` modifiers, either on `AbstractLender` or `HookableLender` contract.

## Resolution

The issue was resolved on commit `2196d53`. The `nonReentrant` modifier on `AbstractLender.liquidate()` was removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | August |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/august/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/august/review.pdf

### Keywords for Search

`vulnerability`

