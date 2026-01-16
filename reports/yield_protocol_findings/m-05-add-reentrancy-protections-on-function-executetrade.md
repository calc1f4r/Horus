---
# Core Classification
protocol: Tracer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25493
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-06-tracer
source_link: https://code4rena.com/reports/2021-06-tracer
github_link: https://github.com/code-423n4/2021-06-tracer-findings/issues/143

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
  - derivatives

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-05] Add reentrancy protections on function `executeTrade`

### Overview


This bug report is about the `executeTrade` function of the `Trader` contract which has a potential reentrancy issue. Reentrancy is a type of attack which could happen when a user-controlled external contract calls the `makeOrder.market` function. It is recommended to add a reentrancy guard, like the one from OpenZeppelin, to prevent users from reentering the critical functions. The bug report was disputed as the issue was already known by the team, but marked as medium risk by the judge. It was also found to be a duplicate of another bug report (#72).

### Original Finding Content

_Submitted by shw, also found by 0xRajeev_

As written in the to-do comments, reentrancy could happen in the `executeTrade` function of `Trader` since the `makeOrder.market` can be a user-controlled external contract. See [L121-L126](https://github.com/code-423n4/2021-06-tracer/blob/main/src/contracts/Trader.sol#L121-L126) in `Trader.sol`.

Recommend adding a reentrancy guard (e.g., the [implementation from OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/security/ReentrancyGuard.sol)) to prevent the users from reentering critical functions.

**[raymogg (Tracer) disputed](https://github.com/code-423n4/2021-06-tracer-findings/issues/143#issuecomment-874405296):**
 > Disputing just as while this is important, its quite explicitly stated in the todo comment and as such is already known by the team as a potential issue.
>
> Realistically shouldn't be too much of a problem with whitelisting of the trader.

**[cemozerr (Judge) commented](https://github.com/code-423n4/2021-06-tracer-findings/issues/143#issuecomment-882105114):**
 > Marking this as medium risk as, regardless of being noted by the team, still poses a security threat.

**[OsmanBran (Tracer) commented](https://github.com/code-423n4/2021-06-tracer-findings/issues/143#issuecomment-874405296):**
 > Duplicate of [#72](https://github.com/code-423n4/2021-06-tracer-findings/issues/72)



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-tracer
- **GitHub**: https://github.com/code-423n4/2021-06-tracer-findings/issues/143
- **Contest**: https://code4rena.com/reports/2021-06-tracer

### Keywords for Search

`vulnerability`

