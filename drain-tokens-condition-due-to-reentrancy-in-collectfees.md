---
# Core Classification
protocol: CLOBER
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7259
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - bridge
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Desmond Ho
  - Grmpyninja
  - Christoph Michel
  - Throttle
  - Taek Lee
---

## Vulnerability Title

Drain tokens condition due to reentrancy in collectFees

### Overview


This bug report is about the OrderBook.sol#L800-L810 function, collectFees. This function was not protected by a re-entrancy guard, which made it vulnerable to malicious hosts draining trading pools. If a transfer of at least one of the tokens in a trading pair allowed for arbitrary code to be invoked (e.g. token implementing callbacks/hooks), then the malicious host could take advantage of the lack of a re-entrancy guard and transfer collected fees multiple times to both the DAO and the host.

To mitigate this issue, it was recommended to either add a re-entrancy guard to the collectFees function or implement a check-effect-interaction pattern to update the balance before the transfer is executed. The issue was fixed in commit 93b287d2, and verified by Spearbit with the addition of a nonReentrant.

### Original Finding Content

## Security Issue Report

## Severity
**High Risk**

## Context
`OrderBook.sol#L800-L810`

## Description
The `collectFees` function is not guarded by a re-entrancy guard. In the event that a transfer of at least one of the tokens in a trading pair invokes arbitrary code (e.g., token implementing callbacks/hooks), it is possible for a malicious host to drain trading pools. The re-entrancy condition allows for the transfer of collected fees multiple times to both the DAO and the host, surpassing the actual fee counter.

## Recommendation
Add a re-entrancy guard to mitigate the issue in the `collectFees` function, or implement a check-effect-interaction pattern to update the balance before executing the transfer.

## Clober
Fixed in commit `93b287d2`.

## Spearbit
Verified. `nonReentrant` added.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | CLOBER |
| Report Date | N/A |
| Finders | Desmond Ho, Grmpyninja, Christoph Michel, Throttle, Taek Lee |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

