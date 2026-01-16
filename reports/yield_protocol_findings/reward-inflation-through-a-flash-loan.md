---
# Core Classification
protocol: Sperax - Farms
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59251
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/sperax-farms/e6f8e3b1-d55d-4c05-91da-30d4a4bb7633/index.html
source_link: https://certificate.quantstamp.com/full/sperax-farms/e6f8e3b1-d55d-4c05-91da-30d4a4bb7633/index.html
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
  - Gereon Mendler
  - Roman Rohleder
  - Jonathan Mevs
---

## Vulnerability Title

Reward Inflation Through a Flash Loan

### Overview


A bug has been reported in the `Rewarder.sol` and `Farm.sol` files where users are able to deposit and withdraw funds in the same block, leading to potential exploitation through a Flash Loan. This allows users to inflate their rewards by depositing a large amount of farm tokens and immediately withdrawing them, resulting in a higher reward payout. To fix this issue, a deposit timestamp has been added to the `Deposit` struct and a time delay has been implemented to prevent deposits and withdrawals from occurring in the same block. This will help prevent potential exploitation and ensure fair distribution of rewards. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `e1359d81959883d4485f09e48e28afa970627d89`. The client provided the following explanation:

> Added a depositTs in struct Deposit, it is updated in deposit() and increaseDeposit() and validated in withdraw() and decreaseDeposit()

This has been fixed as users can no longer deposit or withdraw in the same block.

**File(s) affected:**`Rewarder.sol`, `Farm.sol`

**Description:** As deposits and withdrawals are allowed to occur within the same block, it is possible for a user to significantly inflate the rewards through a Flash Loan. The exploit scenario below describes specifics. This attack is more feasible for smaller farms.

**Exploit Scenario:**

1.   The attacker makes an initial deposit, which will later be needed to claim rewards.
2.   The attacker receives a flash loan, from which they receive a large amount of farm tokens. 
3.   The attacker deposits these farm tokens, calibrates the rewards, and immediately withdraws their deposit, and repays the flash loan.
4.   Time passes.
5.   The attacker claims rewards at a highly inflated rate due to the rewards being calibrated at a time when there were substantial funds in the farm.

**Recommendation:** To mitigate this risk, consider disallowing deposits and withdrawals to occur in the same block. This can be done by including a deposit timestamp in the `Deposit` struct, and ensuring that some time has passed when a withdrawal is processed, or a deposit is decreased.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Sperax - Farms |
| Report Date | N/A |
| Finders | Gereon Mendler, Roman Rohleder, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/sperax-farms/e6f8e3b1-d55d-4c05-91da-30d4a4bb7633/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/sperax-farms/e6f8e3b1-d55d-4c05-91da-30d4a4bb7633/index.html

### Keywords for Search

`vulnerability`

