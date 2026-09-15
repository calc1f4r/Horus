---
# Core Classification
protocol: iExec PoCo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13756
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/03/iexec-poco/
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

protocol_categories:
  - liquid_staking
  - dexes
  - services
  - rwa
  - payments

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Gonçalo Sá
  - Shayan Eskandari
---

## Vulnerability Title

System deployer is fully trusted in this version of the PoCo system  Acknowledged

### Overview


The iExec team has identified an issue with the ERC1538-compliant proxies used to construct the PoCo system. While it allows for easy upgradeability, it also strips the system of its trustless nature, leaving it vulnerable to malicious actors. It is recommended that ownership of the proxy be immediately revoked after deployment, or that a timespan period be enforced before any changes to the proxy methods can be made effective. This would allow actors in the system to monitor changes and “leave” the system before they are implemented, with a “human-friendly” time lock of 72 hours being advised.

### Original Finding Content

#### Resolution



Update from the iExec team:


After deployment, ownership is planned to be transferred to a multisig.
This is just the first step towards a more decentralised governance on the protocol. We will consider adding an intermediary contract that enforces the lock period. This would however, prevent us from any kind of “emergency” update.
The long term goal is it involve the community in the process, using a DAO or a similar solution.




#### Description


The introduction of ERC1538-compliant proxies to construct the PoCo system has many benefits. It heightens modularity, reduces the number of external calls between the system’s components and allows for easy expansion of the system’s capabilities without disruption of the service or need for off-chain infrastructure upgrade.
However, the last enumerated benefit is in fact a double-edged sword.


Even though ERC1538 enables easy upgradeability it also completely strips the PoCo system of all of its prior trustless nature. In this version the iExec development team should be entirely trusted by **every** actor in the system not to change the deployed on-chain delegates for new ones.


Also the deployer, `owner`, has permission to change some of the system variables, such as `m_callbackgas` for Oracle callback gas limit. This indirectly can lock the system, for example it could result in `IexecPocoDelegate.executeCallback()` reverting which prevents the finalization of corresponding task.


#### Recommendation


The best, easiest solution for the trust issue would be to immediately revoke ownership of the proxy right after deployment. This way the modular deployment would still be possible but no power to change the deployed on-chain code would exist.


A second best solution would be to force a timespan period before any change to the proxy methods (and its delegates) is made effective. This way any actor in the system can still monitor for possible changes and “leave” the system before they are implemented.


In this last option the “lock” period should, obviously, be greater than the amount of time it takes to verify a `Task` of the bigger category but it is advisable to decide on it by anthropomorphic rules and use a longer, “human-friendly” time lock of, for example, 72 hours.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | iExec PoCo |
| Report Date | N/A |
| Finders | Gonçalo Sá, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/03/iexec-poco/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

