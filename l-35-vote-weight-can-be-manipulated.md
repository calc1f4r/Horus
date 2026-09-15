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
solodit_id: 4146
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/176

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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
finders_count: 0
finders:
---

## Vulnerability Title

[L-35] Vote weight can be manipulated

### Overview

See description below for full details.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The vote weight is determined by the `DAOVault` and `BondVault` weight (`voteWeight = _DAOVAULT.getMemberWeight(msg.sender) + _BONDVAULT.getMemberWeight(msg.sender)`).
The weight in these vaults is the deposited LP token.
The `BondVault` however pays for the `BASE` part itself (see `DAO.handleTransferIn`), therefore one only needs to deposit `tokens` and the `DAO` matches the **swap value**.

Therefore, it's possible to manipulate the pool, deposit only a small amount of `tokens` (receiving a large amount of matching `BASE` by the DAO) and receive a large amount of LP tokens this way.
 attack can be profitable:

1. Manipulate the pool spot price by dripping a lot of `BASE` into it repeatedly (sending lots of smaller trades is less costly due to the [path-independence of the continuous liquidity model](https://docs.thorchain.org/thorchain-finance/continuous-liquidity-pools)). This increases the `BASE` per `token` price.
2. Repeatedly call `DAO.bond(amount)` to drip `tokens` into the `DAO` and get matched with `BASE` tokens to provide liquidity. (Again, sending lots of smaller trades is less costly.) As the LP minting is relative to the manipulated low `token` reserve, a lot of LP units are minted for a low amount of `tokens`, leading to receiving large weight.
3. Create a proposal to send the entire reserve balance to yourself by using `grantFunds`
4. Unmanipulate the pool by sending back the `tokens` from 1. This might incur a loss.

The cost of the attack is the swap fees from the manipulation of 1. and 4. plus the (small due to manipulation) amount of tokens required to send in 2.
The profit can be the entire reserve amount which is unrelated to the pools (plus reclaiming lots of LP units over the span of the `BondVault` era).
The attack can be profitable under certain circumstances of:
- high reserves
- low liquidity in the pool

## Recommended Mitigation Steps
I don't think the attack would be feasible if we couldn't get the `DAO` to commit the lion's share of the `BASE` required to acquire LP units through the `BondVault` incentives.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/176
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`vulnerability`

