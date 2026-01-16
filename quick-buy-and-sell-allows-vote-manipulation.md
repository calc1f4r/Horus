---
# Core Classification
protocol: The Computable Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16586
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf
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
finders_count: 3
finders:
  - Gustavo Grieco
  - Rajeev Gopalakrishna
  - Josselin Feist
---

## Vulnerability Title

Quick buy and sell allows vote manipulation

### Overview


This bug report is about data validation on the Reserve platform. It explains how an attacker with a large fund can manipulate the vote by buying a large amount of market tokens just before the voting ends and selling them right after. This way, the attacker can decide the outcome of the vote without being a market participant. The report also suggests an incentivization system to encourage users to vote earlier with a weight decreasing over time. This will make the attack more expensive and therefore make it harder for attackers with large funds to manipulate the vote.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** Reserve  

**Difficulty:** Low  

## Description  
Computable relies on a voting system that allows anyone to vote with any weight at the last minute. As a result, anyone with a large fund can manipulate the vote. Computable’s voting mechanism relies on staking. There is no incentive for users to stake tokens well before the voting ends. Users can buy a large amount of Market tokens just before voting ends and sell them right after it. As a result, anyone with a large fund can decide the outcome of the vote, without being a market participant.  

As all the votes are public, users voting earlier will be penalized, because their votes will be known by the other participants. An attacker can know exactly how much currency will be necessary to change the outcome of the voting, just before it ends.  

## Exploit Scenario  
Alice and Bob vote for their candidates with $10,000 worth of Market tokens. Eve buys $20,001 worth of Market tokens one block before the end of the vote. Eve votes for her candidate. Her candidate is elected. Eve sells all her Market tokens one block after the vote. As a result, Eve decided the outcome of the vote without being an active user of the system.  

## Recommendation  
Blockchain-based online voting is a known challenge. No perfect solution has been found so far.  

Incentivize users to vote earlier by implementing a weighted stake, with a weight decreasing over time. While it will not prevent users with unlimited resources from manipulating the vote at the last minute, it will make the attack more expensive.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | The Computable Protocol |
| Report Date | N/A |
| Finders | Gustavo Grieco, Rajeev Gopalakrishna, Josselin Feist |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf

### Keywords for Search

`vulnerability`

