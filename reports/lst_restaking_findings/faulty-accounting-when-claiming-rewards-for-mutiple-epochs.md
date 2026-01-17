---
# Core Classification
protocol: Arkis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59954
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html
source_link: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html
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
  - Julio Aguilar
  - Ibrahim Abouzied
  - Hytham Farah
---

## Vulnerability Title

Faulty Accounting when Claiming Rewards for Mutiple Epochs

### Overview


The client has marked a bug as "Fixed" in the file "RewardsMath.sol". The bug occurred when calculating rewards for Liquidity Providers in the protocol. The function `calculateUserRewardsForTheWholeNumberOfEpochs()` did not accurately distribute rewards if the user had not interacted with the pool for multiple epochs. This was because the calculation assumed all epochs were the same length, when in reality they could vary. This could result in incorrect rewards being given to users. The bug was caused by the average TPS of the epochs being used instead of considering the length of each epoch. The recommended solution is to account for the individual length of each epoch when calculating rewards.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `fc1aef13ebdb852f69425438ae183c8077b77a5c`.

**File(s) affected:**`RewardsMath.sol`

**Description:** Liquidity Providers accumulate rewards across epochs. Rewards are recalculated and distributed when they interact with the Pool. If it has been several epochs since the user last interacted with the pool, the function `calculateUserRewardsForTheWholeNumberOfEpochs()` calculates the rewards for elapsed epochs by applying the average TPS of the epochs across the elapsed time.

However, the calculation assumes that each epoch is identical in length. Rewards should be distributed in proportion with the length of the epoch.

**Exploit Scenario:**

1.   LP stakes into the protocol.
2.   Epoch 1 elapses with a TPS of 10, and lasts for 10 seconds.
3.   Epoch 2 elapses with a TPS of 100, and lasts for 1 year.
4.   LP claims rewards. Given that the average TPS of the epochs is 55, the user is rewarded according to 55 TPS * (1 year + 10 seconds). This yields a different result than (10 TPS * 10 seconds) + (100 TPS * 1 year).

**Recommendation:** Consider the individual length of an epoch when calculating the rewards.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Arkis |
| Report Date | N/A |
| Finders | Julio Aguilar, Ibrahim Abouzied, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html

### Keywords for Search

`vulnerability`

