---
# Core Classification
protocol: InsureDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1299
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-insuredao-contest
source_link: https://code4rena.com/reports/2022-01-insure
github_link: https://github.com/code-423n4/2022-01-insure-findings/issues/263

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

protocol_categories:
  - services
  - cross_chain
  - indexes
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - danb
---

## Vulnerability Title

[H-06] the first depositor to a pool can drain all users

### Overview


A bug report has been filed regarding a vulnerability in the PoolTemplate.sol contract. If there is no liquidity in the pool, the first deposit determines the total liquidity, and if the amount is too small, the minted liquidity for the next liquidity providers will round down to zero. This vulnerability allows an attacker to steal all money from liquidity providers. 

A proof of concept was provided to illustrate the vulnerability. In the scenario, a pool is created and the attacker is the first one to deposit an amount of 1, the smallest amount possible. The attacker then joins another pool to get attributions in the vault, transferring 1M dollar worth of attributions to the pool. When the next person deposits 500,000 dollars, the amount they will get is 0, meaning they will pay 500,000 dollars but the money will go to the index, allowing the attacker to withdraw it and get 1,500,000, stealing 500,000 dollars from the second investor.

The vulnerability was discovered through manual review.

### Original Finding Content

_Submitted by danb_

<https://github.com/code-423n4/2022-01-insure/blob/main/contracts/PoolTemplate.sol#L807>
if there is no liquidity in the pool, the first deposit determines the total liquidity, if the amount is too small the minted liquidity for the next liquidity providers will round down to zero.

#### Impact

An attacker can steal all money from liquidity providers.

#### Proof of Concept

consider the following scenario:
a pool is created.
the attacker is the first one to deposit, they deposit with \_amount == 1, the smallest amount possible. meaning the total liquidity is 1.
then they join another pool in order to get attributions in the vault.
they transfer the attributions to the pool using `transferAttribution`.
for example, they transferred 1M dollar worth of attributions.
the next person deposits in the index, for example, 500,000 dollars.
<https://github.com/code-423n4/2022-01-insure/blob/main/contracts/PoolTemplate.sol#L803>
the amount they will get is:

    _amount = (_value * _supply) / _originalLiquidity;

as we know:
\_amount = 500,000 dollar
\_supply = 1
\_totalLiquidity = 1,000,000 dollar (the attacker transferred directly)
the investor will get (500,000 dollar \* 1) / (1,000,000 dollar) = 0
and they will pay 500,000
this money will go to the index, and the attacker holds all of the shares, so they can withdraw it and get 1,500,000 stealing 500,000 dollars from the second investor.


**[oishun1112 (Insure) acknowledged and disagreed with severity](https://github.com/code-423n4/2022-01-insure-findings/issues/263):**
 > yes. Every address that has attributions can call transferAttribution(), however, the address has to call addValue() to earn attributions. addValue() has onlyMarket modifier.
> To pass onlyMarket modifier, ownership has to be stolen, in short.
> Since we assume ownership control is driven safely, we don't take this as an issue.

**[0xean (judge) commented](https://github.com/code-423n4/2022-01-insure-findings/issues/263#issuecomment-1023330012):**
 > Agree with warden that the privilege addresses should not be able to use approvals in a way that rugs users funds.
> 
> Based on the fact that we have seen many rug pulls in the space based on compromised "owner" keys, this is a valid attack path.
> 
> `
> 3 — High: Assets can be stolen/lost/compromised directly (or indirectly if there is a valid attack path that does not have hand-wavy hypotheticals).
> `




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | InsureDAO |
| Report Date | N/A |
| Finders | danb |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-insure
- **GitHub**: https://github.com/code-423n4/2022-01-insure-findings/issues/263
- **Contest**: https://code4rena.com/contests/2022-01-insuredao-contest

### Keywords for Search

`vulnerability`

