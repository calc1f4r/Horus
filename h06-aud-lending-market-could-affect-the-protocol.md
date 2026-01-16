---
# Core Classification
protocol: Audius Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11317
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/audius-contracts-audit/
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
  - dexes
  - cdp
  - services
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H06] AUD lending market could affect the protocol

### Overview


This bug report is about the potential of an attacker to influence the result of a governance proposal if an AUD token lending market appears. Such an attack would require the attacker to stake tokens for a brief moment without waiting for the voting period to request an unstake. The only prerequisite for such an attack is having sufficient collateral, which could be easy if the AUD price is low. To counter this attack, Audius has enforced a relationship between the decreaseStakeLockupDuration variable and the votingPeriod + executionDelay, meaning that an attacker cannot unstake without waiting at least one votingPeriod + executionDelay time difference. This effectively makes the attack impossible.

### Original Finding Content

In case an AUD token lending market appears, an attacker could use this market to influence the result of a governance’s proposal, which could lead to a take over of the protocol.


An attacker would only need to stake tokens for a brief moment without waiting for the [`votingPeriod`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L23) to request an unstake. This aggravates the attack, as the attacker would only need to take a loan for the number of blocks established by the [`decreaseStakeLockupDuration` variable](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/ServiceProviderFactory.sol#L17).


The only prerequisite that an attacker needs for this attack is to have sufficient collateral, which could be trivial if a lending market of AUD tokens exists while AUD price is still low enough.


Consider countermeasures for these type of attacks, and have plan for how to react when a lending market for AUD is created.


***Update**: Fixed. As described in the updates of “[H08] Endpoint registration can be frontrun” and “[H09] Slash process can be bypassed”, `decreaseStakeLockupDuration` is already significantly larger than `votingPeriod` + `executionDelay`. Audius’s statement about this issue:*



> The above is no longer possible with our enforced relationship between decreaseStakeLockup and votingPeriod + delay. An attacker may still stake tokens immediately prior to a proposal, but the relationship between the two variables means they are still subject to a slash operation. This is because an attacker cannot unstake without waiting at at least one votingPeriod + executionDelay time difference.
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Audius Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/audius-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

