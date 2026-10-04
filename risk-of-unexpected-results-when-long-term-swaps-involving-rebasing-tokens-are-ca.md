---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17908
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ22022.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ22022.pdf
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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Gustavo Grieco
  - Michael Colburn
---

## Vulnerability Title

Risk of unexpected results when long-term swaps involving rebasing tokens are canceled

### Overview


This bug report outlines a problem with FraxSwap's use of rebasing tokens, which are tokens whose supply can be adjusted to control their prices. When users cancel or withdraw from long-term swaps, the transactions can revert due to changes in the balance of the UniV2TWAMMPair contract. This is because the internal bookkeeping for the swap is not updated to reflect the rebase, meaning that the token transfer from the contract to the user is not successful. This can cause the contract's balance of the token to be exhausted before all users are able to withdraw, causing the transactions to revert. 

To prevent this issue, it is recommended to document the issues involving rebasing tokens and long-term swaps to ensure that users are aware of them. Additionally, it is recommended to evaluate the security risks surrounding ERC20 tokens and how they could affect every system component.

### Original Finding Content

## Diﬃculty: High

## Type: Data Validation

### Description
FraxSwap’s use of rebasing tokens—tokens whose supply can be adjusted to control their prices—could cause transactions to revert after users cancel or withdraw from long-term swaps.

FraxSwap offers a new type of swap called a “long-term swap,” which executes certain swaps over an extended period of time. Users can cancel or withdraw from long-term swaps and recover all of their purchased and unsold tokens.

```solidity
//@notice stop the execution of a long term order
function cancelLongTermSwap(uint256 orderId) external lock execVirtualOrders {
    (address sellToken, uint256 unsoldAmount, address buyToken, uint256 purchasedAmount) = longTermOrders.cancelLongTermSwap(orderId);
    bool buyToken0 = buyToken == token0;
    twammReserve0 -= uint112(buyToken0 ? purchasedAmount : unsoldAmount);
    twammReserve1 -= uint112(buyToken0 ? unsoldAmount : purchasedAmount);
    // transfer to owner of order
    _safeTransfer(buyToken, msg.sender, purchasedAmount);
    _safeTransfer(sellToken, msg.sender, unsoldAmount);
    // update order. Used for tracking / informational
    longTermOrders.orderMap[orderId].isComplete = true;
    emit CancelLongTermOrder(msg.sender, orderId, sellToken, unsoldAmount, buyToken, purchasedAmount);
}
```
*Figure 1.1: The cancelLongTermSwap function in the UniV2TWAMMPair contract*

However, if a rebasing token is used in a long-term swap, the balance of the UniV2TWAMMPair contract could increase or decrease over time. Such changes in the contract’s balance could result in unintended effects when users try to cancel or withdraw from long-term swaps. 

For example, because all long-term swaps for a pair are processed as part of any function with the execVirtualOrders modifier, if the actual balance of the UniV2TWAMMPair is reduced as part of one or more rebases in the underlying token, this balance will not be reflected correctly in the contract’s internal accounting, and cancel and withdraw operations will transfer too many tokens to users. Eventually, this will exhaust the contract’s balance of the token before all users are able to withdraw, causing these transactions to revert.

### Exploit Scenario
Alice creates a long-term swap; one of the tokens to be swapped is a rebasing token. After some time, the token’s supply is adjusted, causing the balance of UniV2TWAMMPair to decrease. Alice tries to cancel the long-term swap, but the internal bookkeeping for her swap was not updated to reflect the rebase, causing the token transfer from the contract to Alice to revert and blocking her other token transfers from completing. To allow Alice to access funds and to allow subsequent transactions to succeed, some tokens need to be explicitly sent to the UniV2TWAMMPair contract to increase its balance.

### Recommendations
- Short term, explicitly document issues involving rebasing tokens and long-term swaps to ensure that users are aware of them.
- Long term, evaluate the security risks surrounding ERC20 tokens and how they could affect every system component.

### References
- Common errors with rebasing tokens on Uniswap V2

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Gustavo Grieco, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ22022.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ22022.pdf

### Keywords for Search

`vulnerability`

