---
# Core Classification
protocol: AragonOne — Aragon Network Presale
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13903
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/11/aragonone-aragon-network-presale/
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
  - dexes
  - cdp
  - services
  - indexes
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Sergii Kravchenko
  - Martin Ortner
---

## Vulnerability Title

BalanceRedirectPresale - Tokens vest during the Presale phase  Won't Fix

### Overview


This bug report concerns the presale version of a token that is intended to be used with the Externally Owned Presale and Bonding Curve Template. The issue is that tokens are directly minted and assigned to contributors during the presale, which could be a problem if the minted token gives voting power in a Decentralized Autonomous Organization (DAO). The resolution is that tokens should be vested for contributors after the presale finishes. It is recommended that a note be added to the documentation to make potential users aware of this behavior, as it could have security implications if contributors get stake in return for their investments.

### Original Finding Content

#### Resolution



The issue was addressed with the following statement:



> 
> This presale version is intended to be used along with the Externally Owned Presale and Bonding Curve Template, which doesn’t have a Voting app, therefore contributors doesn’t have any voting power.
> The use case is the deployment of Aragon Network Jurors Token (ANJ) for the Aragon Court, which is not going to be active before the presale starts, so we don’t see any potential issue here.
> 
> 
> 




#### Description


Tokens are directly minted and assigned to contributors during the Presale. While this might not be an issue if the minted token does not give any voting power of some sort in a DAO it can be a problem for scenarios where contributors get stake in return for contributions.


#### Recommendation


Vest tokens for contributors after the presale finishes. In case this is the expected we suggest to add a note to the documentation to make potential users aware of this behaviour that might have security implications if contributors get stake in return for their investments.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | AragonOne — Aragon Network Presale |
| Report Date | N/A |
| Finders | Sergii Kravchenko, Martin Ortner |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/11/aragonone-aragon-network-presale/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

