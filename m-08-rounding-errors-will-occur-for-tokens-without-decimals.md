---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24649
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-sushitrident
source_link: https://code4rena.com/reports/2021-09-sushitrident
github_link: https://github.com/code-423n4/2021-09-sushitrident-findings/issues/152

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
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-08] Rounding errors will occur for tokens without decimals

### Overview


Bug report: This report is about a bug related to tokens with zero decimals. When tokens with zero decimals are used in a constant product pool, small losses of precision are amplified due to the lack of decimals. For example, if 1000 of token0 and token1 (both with no decimals) are used in a swap, and 1,2,3,4 of token0 are swapped to token1, the output amount of token1 will be 0,1,2,3, resulting in the user losing 100%, 50%, 33%, 25% of their trade to rounding. A proposed solution to this bug is to round the final division upwards. However, it was determined that this is an acceptable risk and nothing can be done if the token itself does not have decimals.

### Original Finding Content


Some rare tokens have 0 decimals: https://etherscan.io/token/0xcc8fa225d80b9c7d42f96e9570156c65d6caaa25

For these tokens, small losses of precision will be amplified by the lack of decimals.

Consider a constant product pool with 1000 of token0 (with no decimals), and 1000 of token1 (also with no decimals). Suppose I swap n= 1,2,3,4 of token0 to token1. Then my output amount of token1 will be 0,1,2,3.

If token0/1 are valuable than I will be losing 100%, 50%, 33%, 25% of my trade to rounding.
Currently there is no valuable token with 0 decimals, but there may be in the future.

Rounding the final `getAmountOut` division upwards would fix this.

**[maxsam4 (Sushi) commented](https://github.com/code-423n4/2021-09-sushitrident-findings/issues/152#issuecomment-946648813):**
 > Acceptable risk. We can't do anything if the token itself doesn't have decimals. We don't create synthetic assets and fractionalize such tokens ourselves.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-sushitrident
- **GitHub**: https://github.com/code-423n4/2021-09-sushitrident-findings/issues/152
- **Contest**: https://code4rena.com/reports/2021-09-sushitrident

### Keywords for Search

`vulnerability`

