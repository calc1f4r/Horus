---
# Core Classification
protocol: Airpuff
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35398
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-10-airpuff.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Quoter uniswap integration.

### Overview


A high severity bug was found in the AirPuffHandlerM._uniswapExecution() function. The function uses a quoter to get the expected amount for a swap, but this method is not recommended due to instability and inefficiency. The recommendation is to remove the quoter integration and add a more stable and gas-efficient way to check the amountOutMinimum value. After the bug was resolved, the quoter was removed and the price is now calculated based on the price returned from an oracle.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**description**

AirPuffHandlerM._uniswapExecution().

The function uses a quoter for getting the expected amount out without executing the swap
and uses this value as `amountOutMinimum` as a parameter for the swap. However, this
method of getting the expected amount is not recommended for use for several reasons.

The first and main reason is that using a quoter on a chain is not stable enough, which often
causes reverts. Quoter is recommended for use in the backend regarding uniswap
documentation. Also, quoter is not gas efficient method.

**Recommendation:**

Remove quoter integration in the `_uniswapExecution` function and add a more stable and
gas-efficient variant for checking the `amountOutMinimum` value by adding the
`amountOutMinimum` argument to the swap function and swap structure.

**Post audit**

Quoter was removed. Price is calculated based on the price retuned from oracle.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Airpuff |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-10-airpuff.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

