---
# Core Classification
protocol: Resolv
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33572
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Resolv/README.md#4-stusr-yield-stealing
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

StUSR Yield Stealing

### Overview


The bug report discusses a vulnerability in the StUSR rewards system that allows hackers to steal yields. This can be done by front-running and back-running the `RewardDistributor.distribute()` transactions from the public mempool. This results in the hacker becoming the primary stakeholder and capturing all distributed rewards, causing regular users to lose their incentive to stake. The recommendation is to use private mempools for reward distribution transactions to prevent this exploit.

### Original Finding Content

##### Description

- https://github.com/resolv-im/resolv-contracts/blob/a36e73c4be0b5f233de6bfc8d2c276136bf67573/contracts/RewardDistributor.sol#L50

Rewards in StUSR are vulnerable to yield stealing. 

A hacker can sandwich the `RewardDistributor.distribute()` transactions from the public mempool:
1. In the first transaction, a hacker front-runs by staking a significant amount of USR in StUSR to become the primary stakeholder.
2. The transaction then occurs, distributing rewards in StUSR.
3. In the next transaction, the hacker back-runs by withdrawing their funds with a guaranteed profit.

This results in regular users losing the incentive to stake funds, as the hacker can capture all distributed rewards.

##### Recommendation

We recommend using private mempools for reward distribution transactions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Resolv |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Resolv/README.md#4-stusr-yield-stealing
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

