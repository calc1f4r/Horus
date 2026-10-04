---
# Core Classification
protocol: DRAFT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29878
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf
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
finders_count: 4
finders:
  - Milo Truck
  - Christoph Michel
  - Csanuragjain
  - Desmond Ho
---

## Vulnerability Title

Message can be passed through OptimismPortal to maliciously call ethYieldManager

### Overview


The report states that there is a critical risk bug in the OptimismPortal.sol file at line 387. This bug allows someone to use the initiateWithdrawal() function to set the ethYieldManager as the target of the transaction. This can have two consequences: 1) it can break existing LIDO withdrawal requests that have not been finalized yet, and 2) it can cause the withdrawal queue to break if a large amount is requested. The recommendation is to prevent the ethYieldManager from being set as the target by adding a check in the code. This bug has a high risk and should be addressed immediately.

### Original Finding Content

## Security Risk Report

## Severity: 
**Critical Risk**

## Context: 
`OptimismPortal.sol#L387`

## Description:
Through `L2ToL1MessagePasser.initiateWithdrawal()`, one can set `ethYieldManager` as the `_tx.target` to invoke its permissioned `requestWithdrawal()` and `claimWithdrawal()` methods. The consequences are:

1. **Bricks existing finalized LIDO withdrawal requests** that are yet to be finalized on the bridge via `finalizeWithdrawalTransaction()`, since they will revert with `RequestAlreadyClaimed(_requestId);`.
2. **Bricks the withdrawal queue** by requesting a large enough amount such that the cumulative amount is close to `type(uint128).max`, causing subsequent `proveWithdrawalTransaction()` to revert when it tries to increment the cumulative amount.

## Recommendation:
Prevent `tx.target` from being set to `yieldManager`:
```solidity
if (_tx.target == address(yieldManager)) revert Unauthorized();
```

## Risk Level:
**DRAFT5.2 High Risk**

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | DRAFT |
| Report Date | N/A |
| Finders | Milo Truck, Christoph Michel, Csanuragjain, Desmond Ho |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf

### Keywords for Search

`vulnerability`

