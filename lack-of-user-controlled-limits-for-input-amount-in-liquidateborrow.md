---
# Core Classification
protocol: Umee
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16906
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
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
finders_count: 2
finders:
  - Paweł Płatek
  - Dominik Czarnota
---

## Vulnerability Title

Lack of user-controlled limits for input amount in LiquidateBorrow

### Overview


This bug report is about an issue with the umee/x/leverage module's LiquidateBorrow function. This function computes the amount of funds that will be transferred from the module to the caller in a liquidation, using asset prices retrieved from an oracle. However, there is no guarantee that the amount returned by the module will correspond to the current market price, as a transaction that updates the price feed could be mined before the call to LiquidateBorrow. 

The exploit scenario is that Alice calls the LiquidateBorrow function, and due to an oracle malfunction, the amount of collateral transferred from the module is much lower than the amount she would receive on another market. To prevent this, it is recommended to introduce a minRewardAmount parameter and add a check verifying that the reward value is greater than or equal to the minRewardAmount value. In the long term, it is recommended to always allow the caller to control the amount of a transfer, especially for amounts that depend on factors that can change between transactions. This would involve enabling the caller to add a lower limit for a transfer from a module and an upper limit for a transfer of the caller’s funds to a module. The difficulty level of this finding is high.

### Original Finding Content

## Diﬃculty: High

## Type: Testing

### Target: umee/x/leverage

## Description

The `x/leverage` module’s `LiquidateBorrow` function computes the amount of funds that will be transferred from the module to the function’s caller in a liquidation. The computation uses asset prices retrieved from an oracle.

There is no guarantee that the amount returned by the module will correspond to the current market price, as a transaction that updates the price feed could be mined before the call to `LiquidateBorrow`.

Adding a lower limit to the amount sent by the module would enable the caller to explicitly state his or her assumptions about the liquidation and to ensure that the collateral payout is as proﬁtable as expected. It would also provide additional protection against the misreporting of oracle prices. Since such a scenario is unlikely, we set the diﬃculty level of this finding to high.

Using caller-controlled limits for the amount of a transfer is a best practice commonly employed by large DeFi protocols such as Uniswap.

## Exploit Scenario

Alice calls the `LiquidateBorrow` function. Due to an oracle malfunction, the amount of collateral transferred from the module is much lower than the amount she would receive on another market.

## Recommendations

- **Short term**: Introduce a `minRewardAmount` parameter and add a check verifying that the reward value is greater than or equal to the `minRewardAmount` value.
  
- **Long term**: Always allow the caller to control the amount of a transfer. This is especially important for transfer amounts that depend on factors that can change between transactions. Enable the caller to add a lower limit for a transfer from a module and an upper limit for a transfer of the caller’s funds to a module.

---

Trail of Bits  
UMEE Security Assessment  
PUBLIC

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Umee |
| Report Date | N/A |
| Finders | Paweł Płatek, Dominik Czarnota |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf

### Keywords for Search

`vulnerability`

