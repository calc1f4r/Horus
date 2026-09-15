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
solodit_id: 11320
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

[H09] Slash process can be bypassed

### Overview


The bug report is about the Audius Protocol, which is a decentralized music streaming platform. The report states that there are two ways for any address to be slashed: by a governance proposal or by a transaction performed by the guardian. The `votingPeriod` establishes how long a governance proposal is open for voting, while the `decreaseStakeLockupDuration` establishes the minimum length of time a service provider must wait before removing their stake. 

The bug report states that if `decreaseStakeLockupDuration` is less than or equal to the `votingPeriod`, it will be possible for a malicious service provider to remove their stake before it can be slashed by the Governance protocol. It recommends setting the `decreaseStakeLockupDuration` so it is much greater than the `votingPeriod` to ensure that a malicious service provider can always be slashed via governance.

The bug has been fixed in pull request #657. The `_updateDecreaseStakeLockupDuration` function enforces that the `decreaseStakeLockupDuration` value is greater than the voting period plus an execution delay.

### Original Finding Content

There are two ways for any address to be slashed. The first one is by a governance’s proposal, and the second one is by a transaction performed by the guardian.


For governance to decide to slash a service provider, a proposal must be submitted to the contract, stakers must vote on it and achieve a majority, and then it has to be executed. This process takes several blocks to complete.


[The `votingPeriod`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L23) establishes how long a governance proposal is open for voting.


Similarly, the [`decreaseStakeLockupDuration` variable](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/ServiceProviderFactory.sol#L17) establishes the minimum length of time a service provider must wait before removing their stake.


If `decreaseStakeLockupDuration` is less than or equal to the `votingPeriod`, it will be possible for a malicious service provider to remove their stake before it can be slashed by the Governance protocol.


Since the guardian is expected to be removed once the system is fully operational — meaning that slashing a malicious service provider using the guardian account will not be possible — consider setting the `decreaseStakeLockupDuration` so it is much greater than the `votingPeriod`. This would ensure that a malicious service provider can always be slashed via governance.


***Update**: Fixed in [pull request #657](https://github.com/AudiusProject/audius-protocol/pull/657). The `_updateDecreaseStakeLockupDuration` function enforces that the `decreaseStakeLockupDuration` value is greater than the voting period plus an execution delay.*

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

