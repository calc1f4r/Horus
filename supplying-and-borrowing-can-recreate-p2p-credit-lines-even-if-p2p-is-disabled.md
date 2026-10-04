---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: bypass_limit

# Attack Vector Details
attack_type: bypass_limit
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6910
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - bypass_limit

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - EBaizel
  - JayJonah8
  - Christoph Michel
  - Datapunk
  - Emanuele Ricci
---

## Vulnerability Title

Supplying and borrowing can recreate p2p credit lines even if p2p is disabled

### Overview


This bug report is about a problem found in the Aave-V2, Compound and PositionsManager.sol. The issue is that when supplying or borrowing, the algorithm tries to reduce the deltas (p2pBorrowDelta/p2pSupplyDelta) by moving borrowers/suppliers back to P2P, but it does not check if P2P is enabled. This can lead to users entering P2P again when governance disables P2P and wants to put users and liquidity back on the pool.

The recommendation to fix the issue is to disable the initial delta-matching step in supply and borrow if P2P is disabled. This is only necessary for supply and borrow, and not for repay and withdraw, because when repaying and withdrawing, the p2pAmount also decreases, so the diff is zero.

The issue has been fixed in PR 1453 and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

**Context:** 
- aave-v2/EntryPositionsManager.sol#L117
- aave-v2/EntryPositionsManager.sol#L215
- compound/PositionsManager.sol#L258
- compound/PositionsManager.sol#L354

**Description:**  
When supplying/borrowing, the algorithm attempts to reduce the deltas `p2pBorrowDelta` and `p2pSupplyDelta` by moving borrowers and suppliers back to P2P. However, it does not check if P2P is enabled. This oversight has significant implications, especially when governance disables P2P and aims to redirect users and liquidity back to the pool through `increaseDelta` calls. Users could inadvertently re-enter P2P by supplying and borrowing.

**Recommendation:**  
Disable matching the initial delta-matching step in supply and borrow if P2P is disabled. This precaution is necessary only for supply and borrow operations and not for repay and withdraw. For repay and withdraw, while we are also reducing the delta, we are not creating new P2P credit lines (as `p2pAmount` also decreases, resulting in a differential of zero). This process can be viewed as unmatching our P2P balance, reducing the delta, shifting our P2P balance to the pool, and then withdrawing from the pool.

**Morpho:** Fixed in PR 1453.

**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | EBaizel, JayJonah8, Christoph Michel, Datapunk, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf

### Keywords for Search

`Bypass limit`

