---
# Core Classification
protocol: Nouns DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21338
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
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
  - yield
  - cross_chain
  - rwa
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - tchkvsky
  - Christos Papakonstantinou
  - Rajeev
  - r0bert
  - hyh
---

## Vulnerability Title

Missing check for vetoed proposal's target timelock can cancel transactions from other proposals on new DAO treasury

### Overview


This bug report is about an issue with the NounsDAOV3Proposals.sol code. The veto() function always assumes that the proposal being vetoed is targeting the new DAO treasury instead of checking via getProposalTimelock() as done by the queue(), execute() and cancel() functions. This could result in calling cancelTransaction() on the wrong timelock, setting the queuedTransactions[txHash] to false for values of target, value, signature, data and eta. The proposal state is vetoed with zombie queued transactions on timelockV1 which will never get executed. 

The severity of this bug is Medium Risk, with Low likelihood and High impact. A proof of concept was conducted to confirm the issue, and a mitigation was recommended in the form of PR 715. This was verified to fix the issue.

### Original Finding Content

## Severity: Medium Risk

## Context
- `NounsDAOV3Proposals.sol#L527-L544`
- `NounsDAOV3Proposals.sol#L435`
- `NounsDAOV3Proposals.sol#L472`
- `NounsDAOV3Proposals.sol#L590`

## Description
The `veto()` function always assumes that the proposal being vetoed is targeting `ds.timelock` (i.e., the new DAO treasury) instead of checking via `getProposalTimelock()` as done by the `queue()`, `execute()`, and `cancel()` functions. If the proposal being vetoed were targeting `timelockV1` (i.e., the original DAO treasury), then this results in calling `cancelTransaction()` on the wrong timelock which sets `queuedTransactions[txHash]` to false for values of `target`, `value`, `signature`, `data`, and `eta`.

The proposal state is vetoed with zombie queued transactions on `timelockV1`, which will never get executed. However, if there coincidentally were valid transactions with the same values (of `target`, `value`, `signature`, `data`, and `eta`) from other proposals queued (assuming in the same block and that both timelocks have the same delay so that `eta` is the same) on `ds.timelock`, then those would unexpectedly and incorrectly get dequeued and will not be executed, even when these other `ds.timelock` targeting proposals were neither vetoed nor cancelled. Successfully voted proposals on the new DAO treasury have their transactions cancelled before execution.

**Confirmed with PoC:** `veto_poc.txt`

**Low likelihood + High impact = Medium severity.**

## Recommendation
Check the vetoed proposal's target timelock via `getProposalTimelock()` and use that as done by `queue()`, `execute()`, and `cancel()` functions.

## Nouns: Mitigation
PR 715.

## Spearbit
Verified that PR 715 fixes the issue as recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Nouns DAO |
| Report Date | N/A |
| Finders | tchkvsky, Christos Papakonstantinou, Rajeev, r0bert, hyh |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

