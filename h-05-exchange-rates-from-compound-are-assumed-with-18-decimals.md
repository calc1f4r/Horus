---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 634
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-08-yield-micro-contest-1
source_link: https://code4rena.com/reports/2021-08-yield
github_link: https://github.com/code-423n4/2021-08-yield-findings/issues/38

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - shw
---

## Vulnerability Title

[H-05] Exchange rates from Compound are assumed with 18 decimals

### Overview


This bug report is about the `CTokenMultiOracle` contract which is used to set the borrowing rate of Compound. The contract assumes the exchange rates (borrowing rate) of Compound always have 18 decimals, while this is not true. According to the Compound documentation, the exchange rate returned from the `exchangeRateCurrent` function is scaled by `1 * 10^(18 - 8 + Underlying Token Decimals)` (and so does `exchangeRateStored`). The bug is that using a wrong decimal number on the exchange rate could cause incorrect pricing on tokens. To mitigate this issue, it is recommended to follow the documentation and get the decimals of the underlying tokens to set the correct decimal of a `Source`.

### Original Finding Content

_Submitted by shw_

The `CTokenMultiOracle` contract assumes the exchange rates (borrowing rate) of Compound always have 18 decimals, while, however, which is not true. According to the [Compound documentation](https://compound.finance/docs/ctokens#exchange-rate), the exchange rate returned from the `exchangeRateCurrent` function is scaled by `1 * 10^(18 - 8 + Underlying Token Decimals)` (and so does `exchangeRateStored`). Using a wrong decimal number on the exchange rate could cause incorrect pricing on tokens. See [`CTokenMultiOracle.sol` #L110](https://github.com/code-423n4/2021-08-yield/blob/main/contracts/oracles/compound/CTokenMultiOracle.sol#L110).

Recommend following the documentation and getting the decimals of the underlying tokens to set the correct decimal of a `Source`.

**[alcueca (Yield) confirmed](https://github.com/code-423n4/2021-08-yield-findings/issues/38#issuecomment-899063337):**
 > Thanks a lot for coming up with this. I had looked into how Compound defined the decimals and couldn't find it.

**[alcueca (Yield) patched](https://github.com/code-423n4/2021-08-yield-findings/issues/38#issuecomment-901201555):**
 > [Fix](https://github.com/yieldprotocol/vault-v2/commit/e9c1ee5532c946e9ab2fc8912039829e190fbb64)



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | shw |

### Source Links

- **Source**: https://code4rena.com/reports/2021-08-yield
- **GitHub**: https://github.com/code-423n4/2021-08-yield-findings/issues/38
- **Contest**: https://code4rena.com/contests/2021-08-yield-micro-contest-1

### Keywords for Search

`vulnerability`

