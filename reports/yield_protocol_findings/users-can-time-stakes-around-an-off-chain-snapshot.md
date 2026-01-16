---
# Core Classification
protocol: NetMind
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59215
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html
source_link: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html
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
finders_count: 3
finders:
  - Jennifer Wu
  - Cameron Biniamow
  - Jonathan Mevs
---

## Vulnerability Title

Users Can Time Stakes around an Off-Chain Snapshot

### Overview


The report discusses an issue with the reward calculation system in the Pledge.sol file. The client has acknowledged the issue and explained that the system will be upgraded to count a pledge as a day if it exceeds 24 hours. However, there is a concern that users can exploit this by timing their calls to stake and cancel stake in order to receive rewards without staking for a significant amount of time. The team has acknowledged that this may not have a big impact, but it could be profitable for users if the rewards exceed the gas cost of the transaction. The recommendation is to introduce variability to when the snapshot is taken and to calculate rewards based on the time spent staking.

### Original Finding Content

**Update**
The client acknowledged the issue and provided the following explanation:

> The reward calculation system will be upgraded to count as a day if the pledge time exceeds 24 hours.

**File(s) affected:**`Pledge.sol`

**Description:** In conversations with the NMT team, they described that the Rewards received by a user would be done off-chain. However, there will be snapshots done for rewards at a recurring timestamp, once daily. This creates the opportunity for users to time their calls to `Pledge.stake()` immediately before the off-chain snapshot is taken and call `Pledge.cancleStake()` immediately after to capture staking rewards while only having to stake for very minimal time. The team has acknowledged that this will be of minimal impact because rewards would be so small, however, if the rewards exceed the gas cost of the transaction, it is indeed profitable for a user to do this.

**Recommendation:** Consider introducing some sort of variability to when the snapshot is taken, and consider calculating rewards based on time spent staking.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | NetMind |
| Report Date | N/A |
| Finders | Jennifer Wu, Cameron Biniamow, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html

### Keywords for Search

`vulnerability`

