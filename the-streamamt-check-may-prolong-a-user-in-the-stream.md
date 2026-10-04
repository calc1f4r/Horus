---
# Core Classification
protocol: Locke
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6996
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Locke-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Locke-Spearbit-Security-Review.pdf
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - launchpad

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Mukesh Jaiswal
  - Eric Wang
  - Harikrishnan Mulackal
---

## Vulnerability Title

The streamAmt check may prolong a user in the stream

### Overview


This bug report is about the risk of a user being stuck in a pool with a bad rate or no rewards at all. The risk is present when a user stakes a small amount of tokens and another person deposits a large stake afterwards. This could cause the user to be stuck in the pool until the streamAmt for the user becomes non-zero. The recommendation is that if streamAmt ends up being zero for a certain accTimeDelta, the user should be able to exit the pool with their tokens, as long as they don't receive rewards for the same duration. This could potentially create issues related to unaccured seconds, so further investigation is needed.

### Original Finding Content

## Severity: Medium Risk

**Context:** Locke.sol#L165

**Description:**  
Assume that the amount of tokens staked by a user (`ts.tokens`) is low. This check allows another person to deposit a large stake in order to prolong the user in a stream (until `streamAmt` for the user becomes non-zero). For this duration, the user would be receiving a bad rate or 0 altogether for the reward token while being unable to exit from the pool.

```solidity
if (streamAmt == 0) revert ZeroAmount();
```

Therefore, if Alice stakes a small amount of deposit token and Bob comes along and deposits a very large amount of deposit token, it’s in Alice’s interest to exit the pool as early as possible, especially when this is an indefinite stream. Otherwise, the user would be receiving a bad rate for their deposit token.

**Recommendation:**  
The ideal scenario is if `streamAmt` ends up being zero for a certain `accTimeDelta`, the user should be able to exit the pool with `ts.tokens` as long as they don’t receive rewards for the same duration. However, in practice, implementing this may create issues related to unaccrued seconds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Locke |
| Report Date | N/A |
| Finders | Mukesh Jaiswal, Eric Wang, Harikrishnan Mulackal |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Locke-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Locke-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

