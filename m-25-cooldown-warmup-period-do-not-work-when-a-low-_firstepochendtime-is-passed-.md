---
# Core Classification
protocol: Yieldy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2900
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-yieldy-contest
source_link: https://code4rena.com/reports/2022-06-yieldy
github_link: https://github.com/code-423n4/2022-06-yieldy-findings/issues/88

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
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Lambda
---

## Vulnerability Title

[M-25] coolDown & warmUp period do not work when a low _firstEpochEndTime is passed to initialize

### Overview


This bug report is about the constructor of the Staking.sol contract. The issue is that the `_firstEpochEndTime` is not enforced to be larger than the current `block.timestamp`. This can lead to the `rebase` function being called multiple times in succession which causes the `epoch.number` to increase. As a result, the coolDown & warmUp period can be bypassed as `epoch.number >= info.expiry` will return true. 

To mitigate this vulnerability, the developers should either require that `_firstEpochEndTime` is larger than `block.timestamp` or set the expiry of the first epoch to `block.timestamp + _epochDuration`.

### Original Finding Content

_Submitted by Lambda_

In the constructor of `Staking.sol`, it is not enforced that the `_firstEpochEndTime` is larger than the current `block.timestamp`. If a low value is accidentally passed (or even 0), `rebase` can be called multiple times in sucession, causing the `epoch.number` to increase. Therefore, the coolDown & warmUp period can be circumvented in such a scenario, as `epoch.number >= info.expiry` (in `_isClaimAvailable` and `_isClaimWithdrawAvailable`) will return true after `rebase` caused several increases of `epoch.number`.

### Recommended Mitigation Steps

Either require that `_firstEpochEndTime` is larger than `block.timestamp` or set the expiry of the first epoch to `block.timestamp + _epochDuration`.

**[toshiSat (Yieldy) acknowledged and commented](https://github.com/code-423n4/2022-06-yieldy-findings/issues/88#issuecomment-1168044235):**
 > This is something we thought about and will most likely set the period temporarily 1 higher when launching with low initial epoch durations.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yieldy |
| Report Date | N/A |
| Finders | Lambda |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-yieldy
- **GitHub**: https://github.com/code-423n4/2022-06-yieldy-findings/issues/88
- **Contest**: https://code4rena.com/contests/2022-06-yieldy-contest

### Keywords for Search

`vulnerability`

