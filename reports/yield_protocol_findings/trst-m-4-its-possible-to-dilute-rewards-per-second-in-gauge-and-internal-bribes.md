---
# Core Classification
protocol: Satin.Exchange
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18956
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-02-24-Satin.Exchange.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-4 It’s possible to dilute rewards per second in Gauge and Internal bribes

### Overview


A bug was found in the function `notifyRewardAmount()` which is used to distribute rewards to a gauge or an internal bribe. The bug allowed an attacker to dilute the rewards per second received by users by calling `notifyRewardAmount()` with a new reward of 1, extending the duration of the rewards that are currently being distributed. To mitigate this issue, access to the `notifyRewardAmount()` functions in Gauge.sol and InternalBribe.sol were restricted, and only callable by SatinVoter.sol and the trusted addresses responsible for sending $CASH rebases, if any.

Unfortunately, a new issue was introduced when the mitigation was implemented, the function `claimFees()` in Gauge.sol failed when calling `notifyRewardAmount()` on InternalBribe.sol because SatinVoter.sol did not set the **gauge** parameter in the internal bribe when a new gauge was created via `createGauge()`. To fix this issue, `notifyRewardAmount()` in Gauge.sol was made only callable by SatinVoter.sol and the $CASH rebase handler, while `notifyRewardAmount()` in InternalBribe.sol was only callable by Ve.sol and the associated gauge. The bug has now been resolved.

### Original Finding Content

**Description:**
The function `notifyRewardAmount()` is called to distribute new rewards to a gauge or an 
internal bribe. In particular, it increases the duration over which the rewards have to be 
distributed by **DURATION** every time it’s called:
```solidity 
    periodFinish[token] = block.timestamp + DURATION;
```
Because of this an attacker could dilute the rewards per second received by bribes and 
gauges users by calling `notifyRewardAmount()` with a new reward of 1, extending the 
duration of the rewards that are currently being distributed thus lowering the rewards per 
second received by users.

**Recommended mitigation:**
A mitigation that also have positive side-effects in lowering the attack surface is to restrict 
access to the Gauge.sol and InternalBribe.sol `notifyRewardAmount()` functions:
● Adjust `notifyRewardAmount()` in Gauge.sol to be only callable by SatinVoter.sol and
the trusted addresses responsible for sending $CASH rebases, if any.
● Adjust `notifyRewardAmount()` in InternalBribe.sol to be only callable by the 
associated gauge and Ve.sol.

**Team response:**
Fixed

**Mitigation review:**
The issue has been resolved as suggested but a new issue has been introduced, the function 
`claimFees()` in Gauge.sol will fail when calling `notifyRewardAmount()` on InternalBribe.sol 
because SatinVoter.sol does not set the **gauge** parameter in the internal bribe when a new 
gauge is created via `createGauge()`.

**Mitigation review 2:**
The introduced issue has been fixed, now `notifyRewardAmount()` in Gauge.sol is only callable 
by SatinVoter.sol and the $CASH rebase handler while `notifyRewardAmount()` in 
InternalBribe.sol is only callable by Ve.sol and the associated gauge.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Satin.Exchange |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-02-24-Satin.Exchange.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

