---
# Core Classification
protocol: OpenZeppelin Uniswap Hooks v1.1.0 RC 1 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61384
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/openzeppelin-uniswap-hooks-v1.1.0-rc-1-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Missing Liquidity Total Update in withdraw

### Overview


The `LimitOrderHook` contract has a problem in its `withdraw` function. When users withdraw their liquidity from filled orders, the total liquidity counter is not updated correctly. This means that the `liquidityTotal` variable continues to have an inflated value, causing users who withdraw later to receive less tokens than they should. The impact of this issue grows with each withdrawal and could result in some users receiving substantially less tokens than they should. To fix this, the `withdraw` function should be modified to update the total liquidity counter whenever a user withdraws. This would ensure that the total liquidity accurately reflects the remaining liquidity in the order, allowing for proportional withdrawals for all participants.

### Original Finding Content

The `LimitOrderHook` contract contains an issue in its `withdraw` [function](https://github.com/OpenZeppelin/uniswap-hooks/blob/087974776fb7285ec844ca090eab860bd8430a11/src/general/LimitOrderHook.sol#L342) where the [total liquidity counter](https://github.com/OpenZeppelin/uniswap-hooks/blob/087974776fb7285ec844ca090eab860bd8430a11/src/general/LimitOrderHook.sol#L359) is not properly updated when users withdraw their liquidity from filled orders. When a user withdraws their funds, the contract correctly [deletes](https://github.com/OpenZeppelin/uniswap-hooks/blob/087974776fb7285ec844ca090eab860bd8430a11/src/general/LimitOrderHook.sol#L356) the individual user's liquidity entry with `delete orderInfo.liquidity[msg.sender]`, but fails to decrease `orderInfo.liquidityTotal` accordingly.

This oversight means that the `liquidityTotal` variable continues to reflect an inflated value that includes withdrawn liquidity. Since this value is [used](https://github.com/OpenZeppelin/uniswap-hooks/blob/087974776fb7285ec844ca090eab860bd8430a11/src/general/LimitOrderHook.sol#L362) as the denominator when calculating proportional token distribution for subsequent withdrawals (`amount0 = FullMath.mulDiv(orderInfo.currency0Total, liquidity, liquidityTotal)`), users withdrawing later will receive systematically smaller amounts than they should. This is mainly because `currencyXTotal` is also [decreased](https://github.com/OpenZeppelin/uniswap-hooks/blob/087974776fb7285ec844ca090eab860bd8430a11/src/general/LimitOrderHook.sol#L366) at each withdrawal, losing the percentage ratio of owned shares within the order.

The impact of this issue increases with each withdrawal. As more users withdraw their liquidity, the discrepancy between the stored total liquidity and the actual remaining liquidity grows larger. In the worst-case scenario, if a significant portion of users have withdrawn, but the total has not been updated, the final users might receive substantially less than their fair share of tokens. In addition, if all users eventually withdraw, some tokens will remain locked in the contract due to division calculations using an artificially high denominator.

An example is as follows:

* Two users have both deposited 500 of liquidity, so `totalLiquidity` is 1000.
* The order is filled and there's now 1000 of `currency0`.

The expected outcome is that both users will receive 500 of `currency0` but let us see what happens: when the first user withdraws, `amount0` is `1000 * 500 / 1000` which is 500. After this withdrawal, `currency0Total` is 500 and `totalLiquidity` is 1000. If the second user withdraws at this point, `amount0` will be calculated as `500 * 500 / 1000` which ends up being 250 and not 500.

To address this issue, the `withdraw` function should be modified to update the total liquidity counter whenever a user withdraws. A simple subtraction could be added after the individual liquidity entry is deleted: `orderInfo.liquidityTotal -= liquidity;`.

This small change would ensure that the total liquidity accurately reflects the remaining liquidity in the order at all times, maintaining proportional withdrawals for all participants.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | OpenZeppelin Uniswap Hooks v1.1.0 RC 1 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/openzeppelin-uniswap-hooks-v1.1.0-rc-1-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

