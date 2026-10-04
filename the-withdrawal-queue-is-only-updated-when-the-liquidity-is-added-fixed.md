---
# Core Classification
protocol: Bridge Mutual
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13499
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/03/bridge-mutual/
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

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Daniel Luca
  - Sergii Kravchenko
---

## Vulnerability Title

The withdrawal queue is only updated when the liquidity is added ✓ Fixed

### Overview


The bug report describes an issue with the withdrawal queue in a liquidity system. When the amount of liquidity is not much higher than the number of tokens locked for the collateral, it is impossible for users to withdraw liquidity. To resolve this issue, a withdrawal request is created and added to the withdrawal queue, and the user needs to wait until there is enough collateral for withdrawal. Currently, the queue can only be cleared when the internal `_updateWithdrawalQueue` function is called, which is only called in one place while adding liquidity. The recommendation is to create an external function that allows users to process the queue without adding new liquidity, such as when some policies expire.

### Original Finding Content

#### Resolution



The queue is now updated via the `external` function `updateWithdrawalQueue` but can only be called separately.


#### Description


Sometimes when the amount of liquidity is not much higher than the number of tokens locked for the collateral, it’s impossible to withdraw liquidity. For a user that wants to withdraw liquidity, a withdrawal request is created. If the request can’t be executed, it’s added to the withdrawal queue, and the user needs to wait until there’s enough collateral for withdrawal. There are potentially 2 ways to achieve that: either someone adds more liquidity or some existing policies expire.


Currently, the queue can only be cleared when the internal `_updateWithdrawalQueue`  function is called. And it is only called in one place while adding liquidity:


**code/contracts/PolicyBook.sol:L276-L290**



```
function \_addLiquidityFor(address \_liquidityHolderAddr, uint256 \_liquidityAmount, bool \_isLM) internal {
  daiToken.transferFrom(\_liquidityHolderAddr, address(this), \_liquidityAmount);   
  
  uint256 \_amountToMint = \_liquidityAmount.mul(PERCENTAGE\_100).div(getDAIToDAIxRatio());
  totalLiquidity = totalLiquidity.add(\_liquidityAmount);
  \_mintERC20(\_liquidityHolderAddr, \_amountToMint);

  if (\_isLM) {
    liquidityFromLM[\_liquidityHolderAddr] = liquidityFromLM[\_liquidityHolderAddr].add(\_liquidityAmount);
  }

  \_updateWithdrawalQueue();

  emit AddLiquidity(\_liquidityHolderAddr, \_liquidityAmount, totalLiquidity);
}

```
#### Recommendation


It would be better if the queue could be processed when some policies expire without adding new liquidity. For example, there may be an external function that allows users to process the queue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Bridge Mutual |
| Report Date | N/A |
| Finders | Daniel Luca, Sergii Kravchenko |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/03/bridge-mutual/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

