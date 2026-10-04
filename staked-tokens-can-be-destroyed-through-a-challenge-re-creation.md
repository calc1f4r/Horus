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
solodit_id: 16577
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

Staked tokens can be destroyed through a challenge re-creation

### Overview


This bug report is about a data validation issue in a listing. The bug is of medium difficulty and occurs when a user stakes tokens to vote or create a challenge. If the tokens are not unstaked, they will be destroyed if the token owner challenges the listing multiple times. This is because the new value is assigned to the stake and is not added to the previously staked tokens. An example exploit scenario is when Bob votes against Alice's listing and stakes 10,000$, and Alice's listing is accepted. A few days later, Bob challenges Alice's listing and as a result, Bob's 10,000$ stake is destroyed. The recommendation is to add the previously staked tokens in addCandidate and to use Echidna and Manticore to ensure that the stake is always preserved if a challenge is re-created.

### Original Finding Content

## Data Validation

## Target: Listing

### Description

**Difficulty:** Medium  
Users stake tokens to vote or create a challenge. Tokens that are not unstaked can be destroyed if the tokens’ owner challenges a listing multiple times. 

To challenge a listing, a stake must be sent:
```python
if kind == CHALLENGE:  # a challenger must successfully stake a challenge
    self.market_token.transferFrom(owner, self, stake)
    self.stakes[owner][hash] = stake
```
*Figure 1: addCandidate (Voting.vy#L134-L136)*

The new value is assigned to the stake and is not added to the previously staked tokens. As a result, if previously staked tokens are not withdrawn, they will be destroyed.

### Exploit Scenario

Bob votes against Alice's listing. During the vote, Bob stakes $10,000. Alice’s listing is accepted. A few days later, Bob convinces other users that Alice's listing should be removed. Bob challenges Alice's listing. As a result, Bob’s $10,000 stake is destroyed.

### Recommendation

Add the previously staked tokens in `addCandidate`. Long term, use Echidna and Manticore to ensure that the stake is always preserved if a challenge is re-created.

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

