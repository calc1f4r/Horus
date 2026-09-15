---
# Core Classification
protocol: Hubble
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1533
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-hubble-contest
source_link: https://code4rena.com/reports/2022-02-hubble
github_link: https://github.com/code-423n4/2022-02-hubble-findings/issues/76

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
  - services
  - derivatives
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - throttle
---

## Vulnerability Title

[M-16] USDC blacklisted accounts can DoS the withdrawal system

### Overview


This bug report describes a vulnerability in the USDC withdrawal system of the 2022-02-hubble project. This vulnerability can cause a Denial of Service (DoS) attack of the USDC withdrawal system. It occurs when a user tries to make a withdrawal to a blacklisted user. This causes the withdrawal system to be bricked since the blacklisted user is never cleared. The vulnerability was identified through manual review. Possible solutions to mitigate the vulnerability are to implement 2-step withdrawals or to skip blacklisted users in the processWithdrawals loop.

### Original Finding Content

_Submitted by throttle_

DoS of USDC withdrawal system

### Proof of Concept

Currently, withdrawals are queued in an array and processed sequentially in a for loop.<br>
However, a `safeTransfer()` to USDC blacklisted user will fail. It will also brick the withdrawal system because the blacklisted user is never cleared.

<https://github.com/code-423n4/2022-02-hubble/blob/main/contracts/VUSD.sol#L53-L67>

### Recommended Mitigation Steps

Possible solutions:<br>
1st solution:<br>
Implement 2-step withdrawals:<br>
\- In a for loop, increase the user's amount that can be safely withdrawn.<br>
\- A user himself withdraws his balance<br>

2nd solution:<br>
Skip blacklisted users in a processWithdrawals loop

**[atvanguard (Hubble) confirmed](https://github.com/code-423n4/2022-02-hubble-findings/issues/76)**

**[moose-code (judge) commented](https://github.com/code-423n4/2022-02-hubble-findings/issues/76#issuecomment-1059987539):**
 > Interesting! Yes, this would be bad.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Hubble |
| Report Date | N/A |
| Finders | throttle |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-hubble
- **GitHub**: https://github.com/code-423n4/2022-02-hubble-findings/issues/76
- **Contest**: https://code4rena.com/contests/2022-02-hubble-contest

### Keywords for Search

`vulnerability`

