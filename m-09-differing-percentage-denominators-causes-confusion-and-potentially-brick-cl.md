---
# Core Classification
protocol: Joyn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1769
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-joyn-contest
source_link: https://code4rena.com/reports/2022-03-joyn
github_link: https://github.com/code-423n4/2022-03-joyn-findings/issues/53

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
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0x
  - hickuphh3
---

## Vulnerability Title

[M-09] Differing percentage denominators causes confusion and potentially brick claims

### Overview


This bug report is about a vulnerability in the Splitter.sol contract in the code-423n4/2022-03-joyn GitHub repository. The vulnerability is caused by the use of an incorrect denominator which could lead to the calculated claimable amount exceeding the actual available funds in the contract. This can lead to claims failing and funds being permanently locked. The recommended mitigation steps are to either remove the unused PERCENTAGE_SCALE or replace its value with 10_000 and use that instead. Additionally, there is an issue with the example scaled percentage given for platform fees which should be 500 instead of 200.

### Original Finding Content

_Submitted by hickuphh3, also found by 0x_

<https://github.com/code-423n4/2022-03-joyn/blob/main/splits/contracts/Splitter.sol#L14>

<https://github.com/code-423n4/2022-03-joyn/blob/main/splits/contracts/Splitter.sol#L103>

### Details & Impact

There is a `PERCENTAGE_SCALE = 10e5` defined, but the actual denominator used is `10000`. This is aggravated by the following factors:

1.  Split contracts are created by collection owners, not the factory owner. Hence, there is a likelihood for someone to mistakenly use `PERCENTAGE_SCALE` instead of `10000`.
2.  The merkle root for split distribution can only be set once, and a collection’s split and royalty vault can’t be changed once created.

Thus, if an incorrect denominator is used, the calculated claimable amount could exceed the actual available funds in the contract, causing claims to fail and funds to be permanently locked.

### Recommended Mitigation Steps

Remove `PERCENTAGE_SCALE` because it is unused, or replace its value with `10_000` and use that instead.

P.S: there is an issue with the example scaled percentage given for platform fees `(5% = 200)`. Should be `500` instead of `200`.

**[sofianeOuafir (Joyn) confirmed and commented](https://github.com/code-423n4/2022-03-joyn-findings/issues/53#issuecomment-1100123940):**
 > This is an issue and we intend to fix it



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Joyn |
| Report Date | N/A |
| Finders | 0x, hickuphh3 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-joyn
- **GitHub**: https://github.com/code-423n4/2022-03-joyn-findings/issues/53
- **Contest**: https://code4rena.com/contests/2022-03-joyn-contest

### Keywords for Search

`vulnerability`

