---
# Core Classification
protocol: Fastlane Atlas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36813
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
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
  - Riley Holterhus
  - Blockdev
  - Gerard Persoon
---

## Vulnerability Title

Solvers don't always reimburse the bundler

### Overview


This bug report discusses an issue in the Atlas system where bundlers are not being properly reimbursed for their gas fees. This is caused by two situations where an early return skips a necessary function call. The first situation occurs in the _getBidAmount() function and the second in the _executeSolverOperation() function. The recommendation is to ensure that gas costs are assigned to the bundler at fault by adding a call to a specific function or reworking the gas allocation process. The bug has been fixed in PR 271 and a follow-up change has been made in PR 371. Spearbit has verified the fix.

### Original Finding Content

## Severity: Medium Risk

## Context
- Escrow.sol#L320-L387
- Escrow.sol#L97-L168

## Description
In the Atlas system, bundlers pay gas fees upfront and are eventually reimbursed throughout the transaction flow. This is facilitated through the claims storage variable (which tracks the total amount due), the `_releaseSolverLock()` function (which assigns a reimbursement amount to a specific solver), and finally the `_settle()` function (which ensures that deposits >= withdrawals + claims).

While this system generally assigns costs fairly, there are two situations where reimbursements are not made as expected. Both situations are the result of an early return that skips a call to `_releaseSolverLock()`, even though the early return may be caused by a `_PARTIAL_REFUND` error (which is expected to result in a gas reimbursement).

The first location of this issue is in the `_getBidAmount()` function, where `_releaseSolverLock()` is only reached if all validation succeeds and the `solverMetaTryCatch()` call is made. Also, note that since there are situations where gas is charged, there seems to be a contradiction with the following comment in the function:

> // NOTE: To prevent a malicious bundler from aggressively collecting storage refunds, solvers should not be on the hook for any 'on chain bid finding' gas usage.

The second location of this issue is in the `_executeSolverOperation()` function, where an early return can happen if the `_handleAltOpHash()` logic fails.

## Recommendation
Whenever an error leads to an early return, ensure that the relevant gas costs are assigned to the solver at fault. This can be achieved by adding a call to `_releaseSolverLock()` before each early return, or potentially by reworking the way that gas costs are allocated.

## Fastlane
Fixed in PR 271. Also added a follow-up change to assign the bid-finding gas costs to the bundler in PR 371.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Fastlane Atlas |
| Report Date | N/A |
| Finders | Riley Holterhus, Blockdev, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf

### Keywords for Search

`vulnerability`

