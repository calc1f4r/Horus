---
# Core Classification
protocol: Maple Finance
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6951
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MapleV2.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MapleV2.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - don't_update_state

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Devtooligan
  - Riley Holterhus
  - Jonatas Martins
  - Christoph Michel
  - 0xleastwood
---

## Vulnerability Title

TransitionLoanManager.add does not account for accrued interest since last call

### Overview


This bug report concerns a medium risk issue with the TransitionLoanManager.sol#L74 code in the pool-v2. The problem is that when the add function is called, it advances the domain start without accounting for the accrued interest since the last domain start. This will cause the _accountedInterest variable to be tracked incorrectly if the add function is called multiple times. 

The recommendation is to either track the accrued interest or ensure that the MigrationHelper.addLoansToLM is only called once in the final migration script, adding all loans at the same time. The code has been updated to mimic LoanManager._advanceGlobal as long as there are no late payments, with the precondition that loans have at least 5 days for any payment to be due. 

Maple suggested that all loans should be added atomically, which would not be an issue, and a PR was created to fix the comment #218. Spearbit confirmed that the issue was fixed.

### Original Finding Content

## Severity: Medium Risk

## Context
`pool-v2::TransitionLoanManager.sol#L74`

## Description
The `TransitionLoanManager.add` advances the domain start but the accrued interest since the last domain start is not accounted for. It therefore wrongly tracks the `_accountedInterest` variable. If `add` is called several times, the accounting will be wrong.

## Recommendation
Consider tracking the accrued interest or ensure that the `MigrationHelper.addLoansToLM` is called only once in the final migration script, adding all loans at the same time.

```solidity
function add(address loan_) external override nonReentrant {
    ...
    uint256 domainStart_ = domainStart;
    + uint256 accruedInterest;
    if (domainStart_ == 0 || domainStart_ != block.timestamp) {
        + accruedInterest = getAccruedInterest();
        domainStart = _uint48(block.timestamp);
    }
    ...
    + _updateIssuanceParams(issuanceRate += newRate_, accountedInterest + accruedInterest);
}
```

This mimics `LoanManager._advanceGlobal` as long as there are no late payments, but that's also the case for `TransitionLoanManager` as one of the preconditions for the migration is that loans have at least 5 days for any payment to be due.

## Discussion
**Maple:** In theory yes, but realistically we'll add all loans atomically. Even in the largest pool, we have around 30 active loans, which is feasible to do in one transaction. This is not an issue since all loans are added atomically, but we can add this functionality to be defensive on the TLM side.  
**Spearbit:** Not fixed, see comment.  
**Maple:** Here is the PR for the fix to your comment #218.  
**Spearbit:** Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Maple Finance |
| Report Date | N/A |
| Finders | Devtooligan, Riley Holterhus, Jonatas Martins, Christoph Michel, 0xleastwood |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/MapleV2.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/MapleV2.pdf

### Keywords for Search

`Don't update state`

