---
# Core Classification
protocol: Behodler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1360
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-behodler-contest
source_link: https://code4rena.com/reports/2022-01-behodler
github_link: https://github.com/code-423n4/2022-01-behodler-findings/issues/297

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.20
financial_impact: high

# Scoring
quality_score: 1
rarity_score: 2

# Context Tags
tags:

protocol_categories:
  - cross_chain
  - services
  - cdp
  - dexes
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - danb
---

## Vulnerability Title

[H-02] wrong minting amount

### Overview


This bug report is about a vulnerability found in the RebaseProxy.sol file in the 2022-01-behodler repository on GitHub. The user handle for the report is danb. 

The vulnerability is in the code on line 36 of the RebaseProxy.sol file, which currently reads: 
```
uint256 proxy = (baseBalance * ONE) / _redeemRate;
```
This should be changed to: 
```
uint256 proxy = (amount * ONE) / _redeemRate;
```
The change is necessary in order to ensure that the code works as expected. Without this change, the code may not function as intended and could lead to unexpected results. 

In summary, this bug report concerns a vulnerability in the RebaseProxy.sol file in the 2022-01-behodler repository on GitHub. The user handle for the report is danb and the problem is with the code on line 36, which should be changed from `uint256 proxy = (baseBalance * ONE) / _redeemRate;` to `uint256 proxy = (amount * ONE) / _redeemRate;` in order to ensure that the code works as expected.

### Original Finding Content

_Submitted by danb_

<https://github.com/code-423n4/2022-01-behodler/blob/main/contracts/TokenProxies/RebaseProxy.sol#L36>

```solidity
uint256 proxy = (baseBalance * ONE) / _redeemRate;
```

should be:
```solidity
uint256 proxy = (amount * ONE) / _redeemRate;
```

**[gititGoro (Behodler) confirmed, but disagreed with High severity and commented](https://github.com/code-423n4/2022-01-behodler-findings/issues/297#issuecomment-1030508474):**
 > Should be a balanceBefore and balanceAfter calculation with the diff being wrapped.

**[Jack the Pug (judge) commented](https://github.com/code-423n4/2022-01-behodler-findings/issues/297#issuecomment-1041248898):**
 > Valid `high`. The issue description can be more comprehensive though.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 1/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | Behodler |
| Report Date | N/A |
| Finders | danb |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-behodler
- **GitHub**: https://github.com/code-423n4/2022-01-behodler-findings/issues/297
- **Contest**: https://code4rena.com/contests/2022-01-behodler-contest

### Keywords for Search

`vulnerability`

