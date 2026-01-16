---
# Core Classification
protocol: Neptune Mutual Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10492
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/neptune-mutual-audit/
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
  - launchpad
  - rwa
  - insurance
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Conflated staking pool reward balances

### Overview


A bug was discovered in the Neptune Mutual protocol that affects the way staking pools handle rewards. Each staking pool specifies its own reward token and corresponding balance in the same aggregate contract. However, when retrieving this value, the token balance of the aggregate contract is returned, which could include balances from other pools or any reward token balances that were directly sent to the contract. This could lead to user rewards being overstated, preventing them from claiming the last rewards. In addition, if a malicious actor sent a non-zero amount of reward tokens to the staking pool contract, it would further prevent users from unstaking. In order to fix this issue, the pool balance was read from the saved record in commit 8b660b13cf9fbcde0bfedb3819dbb670ba74b09a in pull request #156.

### Original Finding Content

Each staking pool specifies its own reward token and [corresponding balance](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/libraries/StakingPoolCoreLibV1.sol#L210-L214) in the same aggregate contract. When retrieving this value, the [token balance of the aggregate contract](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/libraries/StakingPoolLibV1.sol#L158) is returned. Since there could be multiple staking pools with the same reward token, this could include balances from other pools. It could also include any reward token balances that were directly sent to the contract.


Moreover, current user rewards [could also be overstated](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/libraries/StakingPoolLibV1.sol#L178), which would [prevent users from claiming the last rewards](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/libraries/StakingPoolLibV1.sol#L212). Since [rewards are claimed](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/libraries/StakingPoolLibV1.sol#L298) when withdrawing stake, anyone could prevent users from unstaking by directly sending reward tokens to the staking pool contract. Any non-zero amount would be sufficient to trigger this scenario. If this occurs, a recovery agent could still [retrieve](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/core/Recoverable.sol#L49) the funds from the aggregate pool contract and distribute them as desired, although it is not clear how they should distribute the remaining rewards.


Consider reading the pool balance from the saved record.


**Update:** *Fixed as of commit `8b660b13cf9fbcde0bfedb3819dbb670ba74b09a` in [pull request #156](https://github.com/neptune-mutual-blue/protocol/pull/156).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Neptune Mutual Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/neptune-mutual-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

