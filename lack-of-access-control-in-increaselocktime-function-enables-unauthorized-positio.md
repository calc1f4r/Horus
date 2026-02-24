---
# Core Classification
protocol: Magpie
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44774
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-22-Magpie.md
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
  - Zokyo
---

## Vulnerability Title

Lack of access control in increaseLockTime function enables unauthorized position lock

### Overview


The bug report is about a function called increaseLockTime() in a contract called PendleStaking. This function allows anyone to lock a position for up to 104 weeks, but there is a vulnerability because there are no restrictions on who can call this function. This means that anyone can increase the lock time without permission. The recommendation is to add access controls or permission checks to this function to prevent unauthorized use. The client team does not think this needs to be changed, but it is recommended to add these controls to ensure the security of the contract.

### Original Finding Content

**Severity**: High

**Status**: Acknowledged

**Description**

The increaseLockTime() function in the PendleStaking contract allows anyone to lock the position of a PendleStaking for up to 104 weeks. The function takes an _unlockTime parameter, which represents the duration in seconds, to increase the lock time. Then, it invokes the increaseLockPosition function from the IPVotingEscrowMainchain contract, passing 0 as a pendle amount to be pulled in from user to lock and the calculated unlockTime as the lock duration. The vulnerability arises from the lack of access control or permission checks in this function. As a result, any address can call this function and increase the lock time for the position without any restrictions. 

**Recommendation**: 

Consider implementing proper access controls or permission checks in the increaseLockTime() function.
Comment from the client team: I don't think, this needs to be changed because we want the lock period to increase eventually and, the Pendle side is already checking this for us, if the lock time is not greater than last time then it will set the old lock time and if we want to change it, then we have to add timestamp at the time of deployment and do the calculation of unlock time with that in convertpendle, so timestamp will not increase, I haven't touched this

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Magpie |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-22-Magpie.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

