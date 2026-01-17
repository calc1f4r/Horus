---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7149
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
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
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Xiaoming90
  - Blockdev
  - Gerard Persoon
  - Sawmon and Natalie
  - Csanuragjain
---

## Vulnerability Title

The set of tokens in an internal swap pool cannot be updated

### Overview


This bug report is about the SwapAdminFacet.sol function which initializes a swap between the owner and an admin. The problem is that once the swap is initialized, the set of tokens used in the stable swap pool, called _pooledTokens, cannot be updated. This could be dangerous if malicious or bad tokens are included in the set, as users' funds could be put at risk. 

The recommendation is to document the procedure of how _pooledTokens is selected and submitted to initializeSwap to reduce the risk of introducing malicious tokens into the system. The problem has been solved in PR 2354 and verified by Spearbit.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
*SwapAdminFacet.sol#L109-L119*

## Description
Once a swap is initialized by the owner or an admin (indexed by the `key` parameter), the `_pooledTokens` or the set of tokens used in this stable swap pool cannot be updated. 

Currently, the `s.swapStorages[_key]` pools are used in other facets for assets that have the hash of their canonical token ID and canonical domain equal to `_key`. This is particularly relevant when we need to swap between a local and adopted asset or when a user provides liquidity or interacts with other external endpoints of `StableSwapFacet`. 

If the submitted set of tokens to this pool `_pooledTokens`, besides the local and adopted token corresponding to `_key`, includes some other bad/malicious tokens, users' funds can be at risk in the pool in question. If this happens, we need to pause the protocol, push an update, and initialize the swap again.

## Recommendation
Document the procedure on how `_pooledTokens` is selected and submitted to `initializeSwap` to lower the risk of introducing potentially bad/malicious tokens into the system.

## Connext
Solved in PR 2354.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | Xiaoming90, Blockdev, Gerard Persoon, Sawmon and Natalie, Csanuragjain |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

