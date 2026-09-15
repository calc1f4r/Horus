---
# Core Classification
protocol: Brahma Fi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13255
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/05/brahma-fi/
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
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  -  George Kobakhidze

  - David Oz Kashi
  -  Sergii Kravchenko
---

## Vulnerability Title

ConvexPositionHandler._claimRewards incorrectly calculates amount of LP tokens to unstake

### Overview


This bug report is about a function in the ConvexPositionHandler contract called `_claimRewards` which is used to harvest Convex reward tokens and take the generated yield in ETH out of the Curve pool. The bug is that the calculation for the variable `lpTokenEarned` is incorrect, as it uses the `yieldEarned` variable which is denominated in ETH, when it should be denominated in LP tokens. This could lead to significant accounting issues, such as losses in the “no-loss” parts of the vault’s strategy, as 1 LP token is almost always guaranteed to be worth more than 1 ETH. 

The recommended fix is to calculate `lpTokenEarned` using the `currentSharePrice` already received from the Curve pool, so that the amount of LP tokens sent to be unwrapped and unstaked from the Convex and Curve pools is correct. This will also take care of the normalization factor. The new calculation should be `uint256 lpTokenEarned = yieldEarned / currentSharePrice;`.

### Original Finding Content

#### Description


`ConvexPositionHandler._claimRewards` is an internal function that harvests Convex reward tokens and takes the generated yield in ETH out of the Curve pool by calculating the difference in LP token price. To do so, it receives the current share price of the curve LP tokens and compares it to the last one stored in the contract during the last rewards claim. The difference in share price is then multiplied by the LP token balance to get the ETH yield via the `yieldEarned` variable:


**code/contracts/ConvexExecutor/ConvexPositionHandler.sol:L293-L300**



```
uint256 currentSharePrice = ethStEthPool.get\_virtual\_price();
if (currentSharePrice > prevSharePrice) {
    // claim any gain on lp token yields
    uint256 contractLpTokenBalance = lpToken.balanceOf(address(this));
    uint256 totalLpBalance = contractLpTokenBalance +
        baseRewardPool.balanceOf(address(this));
    uint256 yieldEarned = (currentSharePrice - prevSharePrice) \*
        totalLpBalance;

```
However, to receive this ETH yield, LP tokens need to be unstaked from the Convex pool and then converted via the Curve pool. To do this, the contract introduces `lpTokenEarned`:


**code/contracts/ConvexExecutor/ConvexPositionHandler.sol:L302**



```
uint256 lpTokenEarned = yieldEarned / NORMALIZATION\_FACTOR; // 18 decimal from virtual price

```
This calculation is incorrect. It uses yieldEarned which is denominated in ETH and simply divides it by the normalization factor to get the correct number of decimals, which still returns back an amount denominated in ETH, whereas an amount denominated in LP tokens should be returned instead.


This could lead to significant accounting issues including losses in the “no-loss” parts of the vault’s strategy as 1 LP token is almost always guaranteed to be worth more than 1 ETH. So, when the intention is to withdraw `X` ETH worth of an LP token, withdrawing `X` LP tokens will actually withdraw `Y` ETH worth of an LP token, where `Y>X`. As a result, less than expected ETH will remain in the Convex handler part of the vault, and the ETH yield will go to the Lyra options, which are much riskier. In the event Lyra options don’t work out and there is more ETH withdrawn than expected, there is a possibility that this would result in a loss for the vault.


#### Recommendation


The fix is straightforward and that is to calculate `lpTokenEarned` using the `currentSharePrice` already received from the Curve pool. That way, it is the amount of LP tokens that will be sent to be unwrapped and unstaked from the Convex and Curve pools. This will also take care of the normalization factor.
 `uint256 lpTokenEarned = yieldEarned / currentSharePrice;`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Brahma Fi |
| Report Date | N/A |
| Finders |  George Kobakhidze
, David Oz Kashi,  Sergii Kravchenko |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/05/brahma-fi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

