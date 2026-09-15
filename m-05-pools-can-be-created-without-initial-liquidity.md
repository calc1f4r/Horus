---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 503
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/151

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
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-05] Pools can be created without initial liquidity

### Overview


This bug report is about a vulnerability in a protocol that differentiates between public and private pool creations. The vulnerability is that anyone can flash loan the required initial pool liquidity, call `PoolFactory.createPoolADD`, receive the LP tokens in `addForMember` and withdraw liquidity again. The recommended mitigation steps are to consider burning some initial LP tokens or taking a pool creation fee instead.

### Original Finding Content

_Submitted by cmichel_

The protocol differentiates between public pool creations and private ones (starting without liquidity). However, this is not effective as anyone can just flashloan the required initial pool liquidity, call `PoolFactory.createPoolADD`, receive the LP tokens in `addForMember` and withdraw liquidity again.

Recommend considering burning some initial LP tokens or taking a pool creation fee instead.

**[SamusElderg (Spartan) confirmed](https://github.com/code-423n4/2021-07-spartan-findings/issues/151#issuecomment-886326598):**
 > Whilst we were aware of this (more of a deterrent than prevention) contributors have discussed some methods of locking this liquidity in and making it at least flash loan resistant. For instance, a withdraw-lock (global by pool) for 7 days after the pool's genesis so that no user can withdraw liquidity until 7 days have passed. There are other ideas floating around too; but regardless this issue will be addressed in some way prior to launch



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/151
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`vulnerability`

