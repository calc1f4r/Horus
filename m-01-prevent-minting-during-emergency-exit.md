---
# Core Classification
protocol: yAxis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1061
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-yaxis-contest
source_link: https://code4rena.com/reports/2021-11-yaxis
github_link: https://github.com/code-423n4/2021-11-yaxis-findings/issues/12

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
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - TimmyToes
  - defsec
---

## Vulnerability Title

[M-01] Prevent Minting During Emergency Exit

### Overview


This bug report is about a potential increased financial loss during a security incident. It is related to the Alchemix Vault, where a user has the ability to trigger an emergency exit. During this emergency exit, users want to withdraw their funds and repay/liquidate to enable the withdrawal of funds. However, minting against debt does not seem like a desirable behaviour at this time. It could potentially enable unaware users to get themselves into trouble by locking up their funds, or allow an attacker to do more damage.

The recommended mitigation steps are to convert the emergency exit check to a modifier, award wardens who made that suggestion, and then apply that modifier. Alternatively, the team might want to allow minting against credit, as it might be seen as desirable during emergency exit. If this is desired, then the emergency exit check could be placed at line 624 with a modified message, instructing users to only use credit.

### Original Finding Content

_Submitted by TimmyToes, also found by defsec_

#### Impact

Potential increased financial loss during security incident.

#### Proof of Concept

<https://github.com/code-423n4/2021-11-yaxis/blob/0311dd421fb78f4f174aca034e8239d1e80075fe/contracts/v3/alchemix/Alchemist.sol#L611>

Consider a critical incident where a vault is being drained or in danger of being drained due to a vulnerability within the vault or its strategies.

At this stage, you want to trigger emergency exit and users want to withdraw their funds and repay/liquidate to enable the withdrawal of funds. However, minting against debt does not seem like a desirable behaviour at this time. It only seems to enable unaware users to get themselves into trouble by locking up their funds, or allow an attacker to do more damage.

#### Recommended Mitigation Steps

Convert emergency exit check to a modifier, award wardens who made that suggestion, and then apply that modifier here.

Alternatively, it is possible that the team might want to allow minting against credit: users minting against credit would effectively be cashing out their rewards. This might be seen as desirable during emergency exit, or it might be seen as a potential extra source of risk. If this is desired, then the emergency exit check could be placed at line 624 with a modified message, instructing users to only use credit.

**[Xuefeng-Zhu (yAxis) confirmed](https://github.com/code-423n4/2021-11-yaxis-findings/issues/12)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | TimmyToes, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-yaxis
- **GitHub**: https://github.com/code-423n4/2021-11-yaxis-findings/issues/12
- **Contest**: https://code4rena.com/contests/2021-11-yaxis-contest

### Keywords for Search

`vulnerability`

