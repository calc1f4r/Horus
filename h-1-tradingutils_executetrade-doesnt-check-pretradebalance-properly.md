---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: pre/post_balance

# Attack Vector Details
attack_type: pre/post_balance
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3321
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/2
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-notional-judging/issues/110

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - pre/post_balance

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - lemonmon
  - 0x52
  - hansfriese
---

## Vulnerability Title

H-1: `TradingUtils._executeTrade()` doesn't check `preTradeBalance` properly.

### Overview


This bug report is about the `TradingUtils._executeTrade()` function not checking the `preTradeBalance` properly. This is a manual review issue found by 0x52, lemonmon, and hansfriese. The code snippet for the issue can be found at https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/TradingUtils.sol#L118-L160.

The issue is that the `preTradeBalance` is not saved correctly for some cases. For example, if `trade.sellToken` is some ERC20 token (not WETH/ETH) and `trade.buyToken` is WETH, the `preTradeBalance` will be 0 as both `if` conditions are false. Then all ETH inside the contract will be converted to WETH and considered as a `amountBought` [here](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/TradingUtils.sol#L143-L149) and [here](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/TradingUtils.sol#L61). This means that all ETH of the contract will be lost. Similarly, all WETH of the contract will be lost also when `trade.sellToken = some ERC20 token(not WETH/ETH), trade.buyToken = ETH` [here](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/TradingUtils.sol#L151-L158). This means that all of ETH/WETH balance of the contract might be lost in some cases.

The recommendation is to check `preTradeBalance` properly and remove the current code for `preTradeBalance` and insert the below code before executing the trade.

```solidity
if (trade.buyToken == address(Deployments.WETH)) {
    preTradeBalance

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-notional-judging/issues/110 

## Found by 
0x52, lemonmon, hansfriese

## Summary
`TradingUtils._executeTrade()` doesn't check `preTradeBalance` properly.

## Vulnerability Detail
`TradingUtils._executeTrade()` doesn't check `preTradeBalance` properly.

```solidity
function _executeTrade(
    address target,
    uint256 msgValue,
    bytes memory params,
    address spender,
    Trade memory trade
) private {
    uint256 preTradeBalance;

    if (trade.sellToken == address(Deployments.WETH) && spender == Deployments.ETH_ADDRESS) {
        preTradeBalance = address(this).balance;
        // Curve doesn't support Deployments.WETH (spender == address(0))
        uint256 withdrawAmount = _isExactIn(trade) ? trade.amount : trade.limit;
        Deployments.WETH.withdraw(withdrawAmount);
    } else if (trade.sellToken == Deployments.ETH_ADDRESS && spender != Deployments.ETH_ADDRESS) {
        preTradeBalance = IERC20(address(Deployments.WETH)).balanceOf(address(this));
        // UniswapV3 doesn't support ETH (spender != address(0))
        uint256 depositAmount = _isExactIn(trade) ? trade.amount : trade.limit;
        Deployments.WETH.deposit{value: depositAmount }();
    }

    (bool success, bytes memory returnData) = target.call{value: msgValue}(params);
    if (!success) revert TradeExecution(returnData);

    if (trade.buyToken == address(Deployments.WETH)) {
        if (address(this).balance > preTradeBalance) {
            // If the caller specifies that they want to receive Deployments.WETH but we have received ETH,
            // wrap the ETH to Deployments.WETH.
            uint256 depositAmount;
            unchecked { depositAmount = address(this).balance - preTradeBalance; }
            Deployments.WETH.deposit{value: depositAmount}();
        }
    } else if (trade.buyToken == Deployments.ETH_ADDRESS) {
        uint256 postTradeBalance = IERC20(address(Deployments.WETH)).balanceOf(address(this));
        if (postTradeBalance > preTradeBalance) {
            // If the caller specifies that they want to receive ETH but we have received Deployments.WETH,
            // unwrap the Deployments.WETH to ETH.
            uint256 withdrawAmount;
            unchecked { withdrawAmount = postTradeBalance - preTradeBalance; }
            Deployments.WETH.withdraw(withdrawAmount);
        }
    }
}
```

It uses `preTradeBalance` to manage the WETH/ETH deposits and withdrawals.

But it doesn't save the correct `preTradeBalance` for some cases.

- Let's assume `trade.sellToken = some ERC20 token(not WETH/ETH), trade.buyToken = WETH`
- Before executing the trade, `preTradeBalance` will be 0 as both `if` conditions are false.
- Then all ETH inside the contract will be converted to WETH and considered as a `amountBought` [here](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/TradingUtils.sol#L143-L149) and [here](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/TradingUtils.sol#L61).
- After all, all ETH of the contract will be lost.
- All WETH of the contract will be lost also when `trade.sellToken = some ERC20 token(not WETH/ETH), trade.buyToken = ETH` [here](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/TradingUtils.sol#L151-L158).

## Impact
All of ETH/WETH balance of the contract might be lost in some cases.

## Code Snippet
https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/TradingUtils.sol#L118-L160

## Tool used
Manual Review

## Recommendation
We should check `preTradeBalance` properly. We can remove the current code for `preTradeBalance` and insert the below code before executing the trade.

```solidity
if (trade.buyToken == address(Deployments.WETH)) {
    preTradeBalance = address(this).balance;
} else if (trade.buyToken == Deployments.ETH_ADDRESS) {
    preTradeBalance = IERC20(address(Deployments.WETH)).balanceOf(address(this));
}
```

## Discussion

**jeffywu**

@weitianjie2000

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Notional |
| Report Date | N/A |
| Finders | lemonmon, 0x52, hansfriese |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-notional-judging/issues/110
- **Contest**: https://app.sherlock.xyz/audits/contests/2

### Keywords for Search

`Pre/Post Balance`

