---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25508
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-07-connext
source_link: https://code4rena.com/reports/2021-07-connext
github_link: https://github.com/code-423n4/2021-07-connext-findings/issues/12

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
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] Malicious router can block cross-chain-transfers

### Overview


This bug report is about an agreement between a user and a router in a cross-chain transfer. The user locks up funds on the sending chain and then the router responds with a prepare transaction of amount 0, without having to lock up anything. This allows the router to take on all cross-chain transfers without any penalty. 

A potential solution to this bug is to introduce a penalty mechanism for non-responsive routers that agreed off-chain, slashing part of their added liquidity. LayneHaber (Connext) acknowledged the bug and suggested that they are building penalty mechanisms outside of these contracts and are considering adding in a permissioned launch.

### Original Finding Content

_Submitted by 0xRajeev, also found by cmichel and shw_

The agreement between the `user` and the `router` seems to already happen off-chain because all the fields are required for the initial `In variantTransactionData` call already. A router could pretend to take on a user's cross-chain transfer, the user sends their `prepare` transaction, locking up funds on the sending chain.
But then the `router` simply doesn't respond or responds with a `prepare` transaction of `amount=0`.

The user's funds are then locked for the entire expiry time, whereas the router does not have to lock up anything as the amount is 0, even no gas if they simply don't respond. In this way, a router can bid on everything off-chain without a penalty, and take down everyone that accepts the bid.

Recommend that maybe there could be a penalty mechanism for non-responsive routers that agreed off-chain, slashing part of their added liquidity. Could also be that the bid signature already helps with this, but I'm not sure how it works as the off-chain part is not part of the repo.

**[LayneHaber (Connext) acknowledged](https://github.com/code-423n4/2021-07-connext-findings/issues/12#issuecomment-878590098):**
 > This is true, and we are building penalty mechanisms outside of these contracts. For now we are considering adding in a permissioned launch, see #49



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Connext |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-connext
- **GitHub**: https://github.com/code-423n4/2021-07-connext-findings/issues/12
- **Contest**: https://code4rena.com/reports/2021-07-connext

### Keywords for Search

`vulnerability`

