---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37443
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Value `minMarketTokens`, `minLongTokenAmount`, `minShortTokenAmount` Hardcoded to 0

### Overview


This bug report discusses an issue with the GMX `ExchangeRouter.createDeposit()` external call in two contracts, GmRouter.sol and GlmRebalance.sol. The `minMarketTokens` value is hardcoded to 0, which can lead to unexpected changes in the price of market tokens. This can result in the vault receiving fewer market tokens than expected. In addition, the `minLongTokenAmount` and `minShortTokenAmount` values are also set to 0, leaving withdrawals vulnerable to slippage. This means that the amount of tokens received may be significantly smaller than expected, resulting in a loss of funds. The recommendation is to set the `minMarketTokens` value correctly and consider not leaving the `minLongTokenAmount` and `minShortTokenAmount` values as 0. One possible solution is to use the `Reader.getWithdrawalAmountOut()` function to determine the correct minimum amounts after factoring in slippage. 

### Original Finding Content

**Severity** - Medium

**Status** - Resolved

**Description**

There is GMX `ExchangeRouter.createDeposit()` external call made in GmRouter.sol and GlmRebalance.sol contracts.
The value for `minMarketTokens` in Router and Rebalance contract is hardcoded to 0, the index token for the market could change in price and alter the price of the market token, making the market token price change unexpectedly causing the vault to receive fewer market tokens than expected.

Also, any deposits/orders that might get executed by the keeper before the deposit may affect the balance of long/short backing tokens in the market and result in more negative impact than expected causing the vault to receive fewer market tokens than expected.
Similarly, in `ExchangeRouter.createWithdrawal(...)`, `minLongTokenAmount` and `minShortTokenAmount` are set to 0.
This leaves withdrawals vulnerable to slippage, especially since withdrawal requests are not executed instantly, but reliant on GMX’s keepers to execute the request.
The market’s state might change significantly between the time the withdrawal request was created and the time GMX’s keepers execute the withdrawal, potentially causing the amount of tokens received to be much smaller than expected and resulting in a loss of funds. 

**Recommendation**: 

Set the `minMarketTokens` to a correct/safe value throughout the codebase. Consider not leaving `minLongTokenAmount` and `minShortTokenAmount` as 0. A possible approach would be to fetch the output amount of long and short tokens with `Reader.getWithdrawalAmountOut()` and use those values as the minimum amounts after factoring in slippage.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

