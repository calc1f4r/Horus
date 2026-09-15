---
# Core Classification
protocol: Marginswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3873
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-marginswap-contest
source_link: https://code4rena.com/reports/2021-04-marginswap
github_link: https://github.com/code-423n4/2021-04-marginswap-findings/issues/39

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
  - indexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-08] PriceAware uses prices from getAmountsOut

### Overview


This bug report is about a vulnerability in the getPriceFromAMM function of Uniswap v2. This vulnerability can be exploited by manipulating the values returned from the getAmountsOut function, either with large capital or through flash loans. The impact of this vulnerability can be reduced with the UPDATE_MIN_PEG_AMOUNT and UPDATE_MAX_PEG_AMOUNT functions, but it is not completely eliminated. The email address and handle of the reporter is pauliax6@gmail.com and paulius.eth respectively, and the Ethereum address is 0x523B5b2Cc58A818667C22c862930B141f85d49DD. Uniswap v2 recommends using their TWAP oracle to mitigate this vulnerability.

### Original Finding Content


`getPriceFromAMM` relies on values returned from getAmountsOut which can be manipulated (e.g. with the large capital or the help of flash loans). The impact is reduced with UPDATE_MIN_PEG_AMOUNT and UPDATE_MAX_PEG_AMOUNT, however, it is not entirely eliminated.

Uniswap v2 recommends using their TWAP oracle: https://uniswap.org/docs/v2/core-concepts/oracles/



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Marginswap |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-marginswap
- **GitHub**: https://github.com/code-423n4/2021-04-marginswap-findings/issues/39
- **Contest**: https://code4rena.com/contests/2021-04-marginswap-contest

### Keywords for Search

`vulnerability`

