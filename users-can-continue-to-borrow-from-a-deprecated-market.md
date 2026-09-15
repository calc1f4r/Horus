---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6907
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
  - business_logic

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

Users can continue to borrow from a deprecated market

### Overview


This bug report is about the MorphoGovernance.sol contract. When a market is marked as deprecated, there is no verification that the borrow for that market has been disabled. This means a user could borrow from this market and be eligible to be liquidated. To fix this, two options were proposed - add a require or modifier to ensure borrow has been disabled, or disable borrow as part of deprecating the market. The latter was implemented in PR 1551 and verified. Morpho should check that all markets created are both not deprecated and not borrow-paused before deploying the PR to prevent entering a system state where the new checks would not work or would prevent resetting the flags.

### Original Finding Content

## Medium Risk Report

**Severity:** Medium Risk  
**Context:** 
- aave-v2/MorphoGovernance.sol#L395 
- compound/MorphoGovernance.sol#L372  

**Description:**  
When a market is being marked as deprecated, there is no verification that the borrow for that market has already been disabled. This means a user could borrow from this market and immediately be eligible to be liquidated.

**Recommendation:**  
A couple of options:
- Add a require or modifier to ensure borrow has been disabled, and revert if not.
- Disable borrow as part of deprecating the market.

**Morpho:**  
Fixed in PR 1551.

**Spearbit:**  
Verified. After the PR change, to be able to deprecate a market, Morpho must pause the borrowing state; otherwise, the transaction will revert. When both the borrow state is paused and the market is deprecated, if Morpho wants to "reset" those values (borrow not paused, and the market is not deprecated), Morpho must "un-deprecate" it and only then "un-pause" it.

**Note:**  
Morpho should check that all the markets created are both not deprecated and not borrow-paused before deploying the PR to be sure to not enter a case where the new checks would not work or would prevent resetting the flags because the system is in an inconsistent state.

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

`Business Logic`

