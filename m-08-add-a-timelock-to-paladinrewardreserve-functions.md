---
# Core Classification
protocol: Paladin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24722
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-paladin
source_link: https://code4rena.com/reports/2022-03-paladin
github_link: https://github.com/code-423n4/2022-03-paladin-findings/issues/31

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-08] Add a timelock to `PaladinRewardReserve` functions

### Overview


A bug has been found in the PaladinRewardReserve smart contract that allows the owner to approve and transfer any amount of tokens with no limits on any account. This could be a problem for investors, as it does not provide enough trust. To address this issue, a timelock should be added to the transfer and spender approved functions.

The bug was identified by Jujic and danb, and the proof of concept was provided in two sections of the PaladinRewardReserve.sol file. The tools used to identify the bug were VS Code. Kogaroshi (Paladin) acknowledged the bug and commented that in future evolutions of the DAO, a timelock and an on-chain Governance should be implemented to control the smart contract.

### Original Finding Content

_Submitted by Jujic, also found by danb_

The owner of PaladinRewardReserve can approve and transfer any amount of tokens with no limits on any account. This is not good for investors. To give more trust to users: these functions should be put behind a timelock.

### Proof of Concept

[PaladinRewardReserve.sol#L28](https://github.com/code-423n4/2022-03-paladin/blob/9c26ec8556298fb1dc3cf71f471aadad3a5c74a0/contracts/PaladinRewardReserve.sol#L28)<br>

[PaladinRewardReserve.sol#L52](https://github.com/code-423n4/2022-03-paladin/blob/9c26ec8556298fb1dc3cf71f471aadad3a5c74a0/contracts/PaladinRewardReserve.sol#L52)<br>

### Tools Used

VS Code

### Recommended Mitigation Steps

Add a timelock to transfer and spender approved functions.

**[Kogaroshi (Paladin) acknowledged and commented](https://github.com/code-423n4/2022-03-paladin-findings/issues/31#issuecomment-1086661744):**
 > Those 2 smart contracts will be owned by a Multisig, executing decisions based on Governance Votes in the Paladin DAO. In future evolutions of the DAO, it should have a Timelock and an on-chain Governance controlling the smart contract.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Paladin |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-paladin
- **GitHub**: https://github.com/code-423n4/2022-03-paladin-findings/issues/31
- **Contest**: https://code4rena.com/reports/2022-03-paladin

### Keywords for Search

`vulnerability`

