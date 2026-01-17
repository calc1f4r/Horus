---
# Core Classification
protocol: FairSide
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42206
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-05-fairside
source_link: https://code4rena.com/reports/2021-05-fairside
github_link: https://github.com/code-423n4/2021-05-fairside-findings/issues/21

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
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] Call to `swapExactTokensForETH` in `liquidateDai()` will always fail

### Overview


The bug report discusses an issue with a function called `liquidateDai()` in the FairSide contract. This function is supposed to swap a cryptocurrency called Dai for Ethereum using a tool called Uniswap. However, the function fails because the contract has not given Uniswap permission to swap the tokens. This causes another function called `updateCostShareRequest()` to also fail. The report recommends adding permission for Uniswap to swap the tokens in order to fix the issue. The FairSide team has confirmed that they have fixed the issue in a recent update.

### Original Finding Content


`liquidateDai()` calls Uniswap’s `swapExactTokensForETH` to swap Dai to ETH. This will work if `msg.sender` (i.e., the FSD contract) has already given the router an allowance amount that is at least as much as the input token Dai.

Given that there is no prior approval, the call to UniswapV2 router for swapping will fail. This is because `msg.sender` has not approved UniswapV2 with an allowance for the tokens that are attempting to be swapped.

The impact is that, while working with the Dai stablecoin, `updateCostShareRequest()` will fail and revert.

Recommend adding FSD approval to UniswapV2 with an allowance for the tokens that are attempting to be swapped.

**[fairside-core (FairSide) confirmed](https://github.com/code-423n4/2021-05-fairside-findings/issues/21#issuecomment-852193172):**
> Fixed in [PR#19](https://github.com/fairside-core/2021-05-fairside/pull/19).



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | FairSide |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-fairside
- **GitHub**: https://github.com/code-423n4/2021-05-fairside-findings/issues/21
- **Contest**: https://code4rena.com/reports/2021-05-fairside

### Keywords for Search

`vulnerability`

