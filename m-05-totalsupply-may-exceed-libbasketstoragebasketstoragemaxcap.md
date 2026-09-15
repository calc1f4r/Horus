---
# Core Classification
protocol: Amun
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6527
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-amun-contest
source_link: https://code4rena.com/reports/2021-12-amun
github_link: https://github.com/code-423n4/2021-12-amun-findings/issues/283

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Czar102
  - gpersoon
  - gzeon
  - WatchPug
  - kenzo
---

## Vulnerability Title

[M-05] totalSupply may exceed LibBasketStorage.basketStorage().maxCap

### Overview


This bug report is about a vulnerability in the token supply of a certain system. If a user wants to join the pool, the check in the BasketFacet::joinPool does not include the fee. This means that if the fee is on and someone creates as many tokens as possible, the total supply can exceed the maxCap. Manual analysis was used to identify the vulnerability. To mitigate the issue, it is recommended to calculate the fee amount and fee beneficiary share before the require statement and check that the total supply plus the amount and fee beneficiary share is less than or equal to the maxCap.

### Original Finding Content

## Handle

Czar102


## Vulnerability details

## Impact

Total supply of the token may exceed the `maxCap` introduced. This can happen when a user wants to join the pool. The [check in `BasketFacet::joinPool(...)`](https://github.com/code-423n4/2021-12-amun/blob/main/contracts/basket/contracts/facets/Basket/BasketFacet.sol#L153-L156) includes only the base amount, without fee. Thus, if fee is on and someone will want to create as many tokens as possible, the `totalSupply + _amount` will be set to `maxCap`. The call will succeed, but new tokens were also minted as the fee for `bs.feeBeneficiary` if `bs.entryFee` and `bs.entryFeeBeneficiaryShare` are nonzero. Thus, the number of tokens may exceed `maxCap`.

## Tools Used

Manual analysis

## Recommended Mitigation Steps

Consider calculating `feeAmount` and `feeBeneficiaryShare` before the `require(...)` statement and check `totalSupply.add(_amount).add(feeBanficiaryShare) <= this.getCap()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Amun |
| Report Date | N/A |
| Finders | Czar102, gpersoon, gzeon, WatchPug, kenzo |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-amun
- **GitHub**: https://github.com/code-423n4/2021-12-amun-findings/issues/283
- **Contest**: https://code4rena.com/contests/2021-12-amun-contest

### Keywords for Search

`vulnerability`

