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
solodit_id: 6997
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

User can stake before the stream creator produced a funding stream

### Overview


This bug report is about a medium risk issue found in a smart contract called Locke.sol#410. The problem is that if Alice stakes in a stream before it starts, and nobody funds the stream, Alice will lose some of her deposit depending on when she exits the stream. This should not happen since Alice's deposit tokens should be locked until the endDepositLock. 

To fix this issue, two mitigations are suggested. The first one is to add a frontend check that will warn the user if a stream does not have any reward tokens. The second one is to add a check in the stake function that will revert if rewardTokenAmount is equal to 0. With these two mitigations, Alice will not be able to stake in a stream without reward tokens and she will not lose her deposit if the stream is not funded.

### Original Finding Content

## Severity: Medium Risk

## Context
Locke.sol#410

## Description
Consider the following scenario:
1. Alice stakes in a stream before the stream starts.
2. Nobody funds the stream.
3. In case of an indefinite stream, Alice loses some of her deposit depending on when she exits the stream.

For a usual stream, Alice will have her deposit tokens locked until `endDepositLock`.

## Recommendation
Two mitigations are possible:
1. A frontend check warning the user if a stream does not have any reward tokens.
2. A check in the stake function which would revert when `rewardTokenAmount == 0`.

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

