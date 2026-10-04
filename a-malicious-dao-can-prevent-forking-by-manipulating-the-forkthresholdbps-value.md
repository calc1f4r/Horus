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
solodit_id: 21335
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

A malicious DAO can prevent forking by manipulating the forkThresholdBPS value

### Overview


This bug report outlines the potential risk of a malicious majority manipulating the forkThresholdBPS value, which is a DAO governance controlled value. The forkThresholdBPS value is used to determine when a fork is executed. If the forkThresholdBPS is set to an unreasonably high value, the fork will not be executed. This poses a risk to minority token holders who may be unable to join a fork before the malicious proposal is executed. The severity of this issue is rated as Medium, as the likelihood of it occurring is low, but the impact is high. 

Recommendations to mitigate this risk include considering a MAX_FORK_THRESHOLD value, such as 50%, and preventing the increase of forkThresholdBPS if a fork is in the escrow period. It is also important for token holders to actively monitor all proposals for malicious updates.

### Original Finding Content

## Severity Report

## Severity
**Medium Risk**

## Context
NounsDAOV3Admin.sol#L530-L537

## Description
While some of the documentation, see [1](#) and [2](#), note that the fork threshold is expected to be 20%, the `forkThresholdBPS` is a DAO governance controlled value that may be modified via `_setForkThresholdBPS()`. 

A malicious majority can prevent forking at any time by setting the `forkThresholdBPS` to an unreasonably high value that is >= majority voting power. For a fork that is slowly gathering support via escrowing (thus giving time for a DAO proposal to be executed), a malicious majority can reactively manipulate `forkThresholdBPS` to prevent that fork from being executed.

While the governance process gives an opportunity to detect and block such malicious proposals, the assumption is that a malicious majority can force through any proposal, even a visibly malicious one. Also, it is not certain that all governance proposals undergo thorough scrutiny of security properties and their impacts. Token holders need to actively monitor all proposals for malicious updates to create, execute, and join a fork before such a proposal takes effect.

A malicious majority can prevent a minority from forking by manipulating the `forkThresholdBPS` value.  
**Low likelihood + High impact = Medium severity.**

## Recommendation
Mitigation options:
1. Consider a `MAX_FORK_THRESHOLD` value e.g. 50% for `forkThresholdBPS`.
2. Consider preventing the increase of `forkThresholdBPS` if a fork is in the escrow period.

## Nouns
We don't think a maximum value is needed here. If a malicious majority can set this value to be unreasonably high without the minority noticing, it's likely they would also be able to upgrade the DAO contracts without them noticing.

## Spearbit
Acknowledged.

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

