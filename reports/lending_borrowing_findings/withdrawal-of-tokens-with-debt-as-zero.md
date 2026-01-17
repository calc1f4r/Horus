---
# Core Classification
protocol: Curve Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27854
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Stablecoin%20(crvUSD)/README.md#1-withdrawal-of-tokens-with-debt-as-zero
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
  - MixBytes
---

## Vulnerability Title

Withdrawal of tokens with debt as zero

### Overview


This bug report is about a code that allows users to not spend debt in liquidation. The code in question is ```debt = unsafe_div(debt * frac, 10**18)```. If `debt * frac` is less than 10**18, then users don't have to pay for the liquidation part. An example was provided to demonstrate how this could be exploited to eliminate the entire collateral by passing frac as 1. However, the attack is disadvantageous due to the gas.

The recommendation is to add an additional check that `debt != 0`. This would prevent users from exploiting the code to avoid debt in liquidation.

### Original Finding Content

##### Description

This code allows you not to spend debt in liquidation (
https://github.com/curvefi/curve-stablecoin/blob/0d9265cc2dbd221b0f27f880fac1c590e1f12d28/contracts/Controller.vy#L990):
```
debt = unsafe_div(debt * frac, 10**18)
```

If `debt * frac` is less than 10**18, then you don't have to pay for the liquidation part. We especially have the ability to eliminate the entire collateral by passing frac as 1. Example:

```
l_amount = 1

collateral_token._mint_for_testing(user, c_amount)
market_controller.create_loan(c_amount, l_amount, n)
market_controller.liquidate_extended(user, 0, 10 ** 18 - 1, 
    True, ZERO_ADDRESS, [])
## d_debt = 0
## xy[0] = 0
## xy[1] 1000
## PROFIT stablecoin.balanceOf(user) +0
## PROFIT collateral_token.balanceOf(user) +1000
```

In this case, the attack is disadvantageous due to the gas.

##### Recommendation

It is recommended to add an additional check that `debt != 0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Curve Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Stablecoin%20(crvUSD)/README.md#1-withdrawal-of-tokens-with-debt-as-zero
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

