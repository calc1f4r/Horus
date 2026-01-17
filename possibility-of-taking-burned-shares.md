---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28161
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/In-protocol%20Coverage/README.md#1-possibility-of-taking-burned-shares
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Possibility of taking burned shares

### Overview


A bug has been found in the Lido DAO’s SelfOwnedStETHBurner.sol contract which allows attackers to take burned shares profit without taking shares before the processLidoOracleReport() execution. This exploit is outlined in a gist by georgiypetrov. It is possible that this is a front-run attack, which would be the most convenient for the attacker. 

In order to fix this bug, it is recommended to add a limit on the amount of burned tokens. This would prevent the attacker from taking advantage of the bug and protect the users of the Lido DAO.

### Original Finding Content

##### Description
With attack it is possible to take burned shares profit even without taking shares before `processLidoOracleReport()` execution.
https://github.com/lidofinance/lido-dao/blob/ee1991b3bbea2a24b042b0a4433be04301992656/contracts/0.8.9/SelfOwnedStETHBurner.sol#L252
This exploit shows how the attack is done:
https://gist.github.com/georgiypetrov/22c0649058a97102e2fd97a1c619a3b3
If this is a front-run attack, then it will be the most convenient for the attacker.
##### Recommendation
It is necessary to add a limit on the amount of burned tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/In-protocol%20Coverage/README.md#1-possibility-of-taking-burned-shares
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

