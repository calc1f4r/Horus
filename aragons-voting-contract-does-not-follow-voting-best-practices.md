---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17892
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Aragon’s voting contract does not follow voting best practices

### Overview


This bug report is about the FraxPool.sol configuration. It is classified as a high difficulty issue. The voting contract lacks a way to mitigate the use of a “quick vote and withdraw” strategy, does not provide incentives for early voting, has no mitigations for spam attacks, uses a significantly outdated Solidity version, and has not had any updates released since July 2020.

An exploit scenario is provided where a miner, Eve, creates new votes to set a new minter on ERC20CRV on every block. Other users cannot participate in all of the votes, so one vote is accepted and Eve takes control of ERC20CRV’s minting.

Recommendations for short-term solutions include improving Aragon’s voting contract to mitigate the issues or implementing a different voting contract and performing a security assessment of the contract before deployment. For long-term solutions, staying up to date on the latest research on blockchain-based online voting and bidding is recommended. This research will continue to evolve, as there is not yet a perfect solution for the challenges of blockchain-based online voting.

### Original Finding Content

## Configuration Report

**Type:** Configuration  
**Target:** FraxPool.sol  

**Difficulty:** High  

## Description
`veFXS` uses the Aragon contract for voting. While its voting logic is simple, it fails to prevent several potential abuses of on-chain voting processes. The voting contract has the following issues:

- It lacks a way to mitigate the use of a “quick vote and withdraw” strategy.
- It does not provide incentives for early voting.
- It has no mitigations for spam attacks. An attacker with vote-creation rights could create hundreds of thousands of votes and would need only one to pass to succeed.
- It uses a significantly outdated Solidity version.
- It has not had any updates released since July 2020.

## Exploit Scenario
Eve, a miner, creates new votes to set a new minter on `ERC20CRV` on every block. Other users cannot participate in all of the votes. As a result, one vote is accepted, and Eve takes control of `ERC20CRV`’s minting.

## Recommendations
Short term, consider improving Aragon’s voting contract to mitigate the above issues. Alternatively, implement a different voting contract and perform a security assessment of the contract before deployment.

Long term, stay up to date on the latest research on blockchain-based online voting and bidding. This research will continue to evolve, as there is not yet a perfect solution for the challenges of blockchain-based online voting.

## References
- Vocdoni
- Security Disclosure: Aragon 0.6 Voting ("Voting v1")
- Aragon vote shows the perils of on-chain governance

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

