---
# Core Classification
protocol: Gro Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 413
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-gro-protocol-contest
source_link: https://code4rena.com/reports/2021-06-gro
github_link: https://github.com/code-423n4/2021-06-gro-findings/issues/52

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xRajeev
---

## Vulnerability Title

[M-04] Flash loan risk mitigation is optional and not robust enough

### Overview


This bug report is about a vulnerability in which the switchEoaOnly() allows the owner to disable preventSmartContracts, and this will allow any smart contract to interact with the protocol and potentially exploit any underlying flash loan vulnerabilities. The current mitigation is to optionally prevent contracts, except whitelisted partner ones, from interacting with the protocol to prevent any flash loan manipulations. The bug report also includes the Proof of Concept, Tools Used, and Recommended Mitigation Steps.

The Proof of Concept includes five links to the code in the Github repository. The Tools Used are Manual Analysis. The Recommended Mitigation Steps include adding logic to prevent multiple txs to protocol from the same address within the same block.

In conclusion, this bug report is about a vulnerability in which the switchEoaOnly() allows the owner to disable preventSmartContracts, and this could potentially exploit any underlying flash loan vulnerabilities. The bug report includes the Proof of Concept, Tools Used, and Recommended Mitigation Steps.

### Original Finding Content

_Submitted by 0xRajeev_

The `switchEoaOnly()` allows the owner to disable `preventSmartContracts` (the project’s plan apparently is to do so after the beta-period) which will allow any smart contract to interact with the protocol and potentially exploit any underlying flash loan vulnerabilities which are specified as an area of critical concern.

The current mitigation is to optionally prevent contracts, except whitelisted partner ones, from interacting with the protocol to prevent any flash loan manipulations. A more robust approach would be to add logic preventing multiple txs to the protocol from the same address/`tx.origin` within the same block when smart contracts are allowed. This will avoid any reliance on trust with integrating partners/protocols.

Recommend adding logic that prevents multiple txs to the protocol from the same address and within the same block.

**[kristian-gro (Gro) acknowledged but disagreed with severity](https://github.com/code-423n4/2021-06-gro-findings/issues/52#issuecomment-880041099):**
> Low-severity: This is a temporary blocker to not let SCs interact with gro-protocol, planned to be removed after beta as it might potentially stop other integrations (as per issue 51)
> 
> Acknowledged, this is just a temporary block, and is planned to be removed in future releases - other protection exists to protect the system from flash loan manipulations.

**[ghoul-sol (Judge) commented](https://github.com/code-423n4/2021-06-gro-findings/issues/52#issuecomment-886701698):**
 > It looks like a low risk issue since it's a future problem and not something that is an immediate issue, however, it's not clear how the protocol will protect itself against flash loans after this temporary blocker is off. One of the critical protocol's concerns are flash loans manipulations therefore I think medium risk is justified here.




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gro Protocol |
| Report Date | N/A |
| Finders | 0xRajeev |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-gro
- **GitHub**: https://github.com/code-423n4/2021-06-gro-findings/issues/52
- **Contest**: https://code4rena.com/contests/2021-07-gro-protocol-contest

### Keywords for Search

`vulnerability`

