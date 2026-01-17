---
# Core Classification
protocol: EIP-4337 – Ethereum Account Abstraction Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10634
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/eth-foundation-account-abstraction-audit/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - services

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L08] Paymasters cannot reduce unstaking delay after withdrawal window [core]

### Overview

See description below for full details.

### Original Finding Content

The `StakeManager` contract allows paymasters to lock funds for a period of time and they are [intentionally prevented](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/StakeManager.sol#L87) from reducing the delay. However, after unstaking their funds and waiting for the withdrawal period, they should be able to stake again with any delay. This is possible if they withdraw their funds first (which [clears the saved delay](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/StakeManager.sol#L127)), but this is should not be a necessary requirement.


Consider [updating the staking guard condition](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/StakeManager.sol#L87) to allow the delay time to be reduced if the `withdrawTime` has been reached.


***Update**: Fixed in pull request [#76](https://github.com/eth-infinitism/account-abstraction/pull/76/files). Staking state is no longer affected by the `withdrawTo` function. Users can now unlock an existing stake using `unlockStake` without needing to withdraw the funds, and they can then immediately restake by calling the `addStakeTo` function.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | EIP-4337 – Ethereum Account Abstraction Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/eth-foundation-account-abstraction-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

