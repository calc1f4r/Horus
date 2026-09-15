---
# Core Classification
protocol: Lyra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50547
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/lyra-finance/lyra-finance-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/lyra-finance/lyra-finance-smart-contract-security-assessment
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

LIQUIDITY POOL COULD RUN OUT OF SUSD TOKENS

### Overview


The bug report describes a problem that occurs when closing a long call position. This causes the `_maybeExchangeBase` function to be called with the argument `revertBuyOnInsufficientFunds` set to false, which allows the liquidity pool to swap sUSD for sETH without limits. This can lead to the liquidity pool running out of sUSD tokens, affecting operations such as withdrawal, premium payment, and settlement. The report includes a proof of concept showing how an attacker can take advantage of this vulnerability. The bug has been fixed in a recent commit to the **LiquidityPool** contract.

### Original Finding Content

##### Description

When closing a position **long call**, the `_maybeExchangeBase` function is called with the argument `revertBuyOnInsufficientFunds` set to **false**. As a consequence, the liquidity pool will be able to swap sUSD for sETH without limits and could eventually run out of sUSD tokens.

This situation could affect some relevant operations such as withdrawal, premium payment, settlement, etc.

`Proof of Concept:`

Initial liquidity info for the test:

![](images/HAL-03/initial_situation.png)

The attacker opens a long call position of 120 sETH. There is a big difference between `lockedCollateral.base` and `sETH balance` because of \vulnref{DIFFERENCES BETWEEN LOCKED COLLATERAL AND SETH BALANCE ARE NOT ADEQUATELY CAPPED}:

![](images/HAL-03/open_position_1.png)
![](images/HAL-03/open_position_2.png)

Because of the difference, the owner decides to set `maxFeePaid` = **MAX\_UINT** to enable sETH repurchase.

On the other hand, a user withdraws sUSD from liquidity pool. The image shows liquidity info after withdrawal:

![](images/HAL-03/after_withdraw.png)

Finally, the attacker closes the 82.6 sETH long call position:

![](images/HAL-03/close_position_1.png)

Since the swap is not limited by any parameter, the protocol uses all available sUSD. In the end, the new sUSD balance is almost 0 (`0.29037...` in the example):

![](images/HAL-03/close_position_2.png)

Code Location
-------------

#### LiquidityPool.sol

```
(uint quoteSpent, uint baseReceived) = synthetixAdapter.exchangeToExactBaseWithLimit(
  exchangeParams,
  address(optionMarket),
  amountBase,
  revertBuyOnInsufficientFunds ? freeLiquidity : type(uint).max
);
emit BasePurchased(quoteSpent, baseReceived);

```

##### Score

Impact: 4  
Likelihood: 4

##### Recommendation

**SOLVED:** The issue was fixed in commit [d8d2e902c6d368313d9e04bec40c21fbf70b870b](https://github.com/lyra-finance/lyra-protocol/commit/d8d2e902c6d368313d9e04bec40c21fbf70b870b). With the update to the `_getLiquidity` function in the **LiquidityPool** contract, this attack vector is not feasible.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Lyra Finance |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/lyra-finance/lyra-finance-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/lyra-finance/lyra-finance-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

