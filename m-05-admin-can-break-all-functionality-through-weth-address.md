---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25328
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto-v2
source_link: https://code4rena.com/reports/2022-06-canto-v2
github_link: https://github.com/code-423n4/2022-06-NewBlockchain-v2-findings/issues/173

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
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-05] Admin Can Break All Functionality Through Weth Address

### Overview


This bug report is about a flaw in the protocol of the lending-market-v2. If the admin is mistakenly set to a WETH address, users will not be able to claim their rewards and all lending operations will be blocked. This could potentially allow an admin to break the protocol. The recommended mitigation steps are to set the WETH address through initializer or change it through governance. It is suggested that the severity of this issue is medium since malicious governance may be needed to exploit this bug.

### Original Finding Content

_Submitted by defsec_

On the protocol, almost all functionality is constructed through WETH address. However, if the admin is set to WETH address mistakenly, user could not claim through [Comptroller.sol#L1381](https://github.com/Plex-Engineer/lending-market-v2/blob/main/contracts/Comptroller.sol#L1381). Admin can break the protocol.

### Proof of Concept

<https://github.com/Plex-Engineer/lending-market-v2/blob/main/contracts/Comptroller.sol#L1479>

### Recommended Mitigation Steps

Set WETH address through initializer or change it through governance.

**[nivasan1 (Canto) disputed and commented](https://github.com/code-423n4/2022-06-canto-v2-findings/issues/173#issuecomment-1189682546):**
 > The admin of the lending-market and LP will be cosmos-sdk governance, vis-a-vis, the community, as such it is expected that a malicious governance proposal will not be passed.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-v2-findings/issues/173#issuecomment-1216868137):**
 > Similarly to findings about `admin` re-initializing contracts, the warden has shown how, because the WETH address can be changed, accounting and functionality of the protocol and it's interactions (in this case emission of rewards and all lending operations triggering a transfer of "COMP"), can be bricked.
> 
> Because this is contingent on malicious governance, I believe Medium Severity to be appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto-v2
- **GitHub**: https://github.com/code-423n4/2022-06-NewBlockchain-v2-findings/issues/173
- **Contest**: https://code4rena.com/reports/2022-06-canto-v2

### Keywords for Search

`vulnerability`

