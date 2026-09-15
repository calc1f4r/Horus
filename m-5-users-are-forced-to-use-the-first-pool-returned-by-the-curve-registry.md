---
# Core Classification
protocol: Notional Update #2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6700
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/52
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-notional-judging/issues/11

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.87
financial_impact: medium

# Scoring
quality_score: 4.333333333333333
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - xiaoming90
---

## Vulnerability Title

M-5: Users are forced to use the first pool returned by the Curve Registry

### Overview


This bug report is about the issue M-5 which was found by xiaoming90. It was observed that when multiple pools are available, users are forced to use the first pool returned by the Curve Registry, which might not be the most optimal pool to trade with. This is because the `CurveAdapter._exactInSingle` function calls the `CURVE_REGISTRY.find_pool_for_coins` function to find the available pools for exchanging two coins without allowing users to define the `i` parameter of the `find_pool_for_coins` function. As a result, the first pool might have lesser liquidity, larger slippage, and higher fee than the other pools, resulting in the trade returning lesser assets than expected. The code snippet and tool used for finding the issue were provided. The recommendation was to allow users to choose which pool they want to trade against if multiple pools support the exchange. The issue was discussed and considered as a valid medium.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-notional-judging/issues/11 

## Found by 
xiaoming90

## Summary

If multiple pools support the exchange, users are forced to use the first pool returned by the Curve Registry. The first pool returned by Curve Registry might not be the most optimal pool to trade with. The first pool might have lesser liquidity, larger slippage, and higher fee than the other pools, resulting in the trade returning lesser assets than expected.

## Vulnerability Detail

When performing a trade via the `CurveAdapter._exactInSingle` function, it will call the [`CURVE_REGISTRY.find_pool_for_coins`](https://github.com/curvefi/curve-pool-registry/blob/0bdb116024ccacda39295bb3949c3e6dd0a8e2d9/contracts/Registry.vy#L329)  function to find the available pools for exchanging two coins.

https://github.com/sherlock-audit/2023-02-notional/blob/main/leveraged-vaults/contracts/trading/adapters/CurveAdapter.sol#L34

```solidity
File: CurveAdapter.sol
34:     function _exactInSingle(Trade memory trade)
35:         internal view returns (address target, bytes memory executionCallData)
36:     {
37:         address sellToken = _getTokenAddress(trade.sellToken);
38:         address buyToken = _getTokenAddress(trade.buyToken);
39:         ICurvePool pool = ICurvePool(Deployments.CURVE_REGISTRY.find_pool_for_coins(sellToken, buyToken));
40: 
41:         if (address(pool) == address(0)) revert InvalidTrade();
42: 
43:         int128 i = -1;
44:         int128 j = -1;
45:         for (int128 c = 0; c < MAX_TOKENS; c++) {
46:             address coin = pool.coins(uint256(int256(c)));
47:             if (coin == sellToken) i = c;
48:             if (coin == buyToken) j = c;
49:             if (i > -1 && j > -1) break;
50:         }
51: 
52:         if (i == -1 || j == -1) revert InvalidTrade();
53: 
54:         return (
55:             address(pool),
56:             abi.encodeWithSelector(
57:                 ICurvePool.exchange.selector,
58:                 i,
59:                 j,
60:                 trade.amount,
61:                 trade.limit
62:             )
63:         );
64:     }
```

However, it was observed that when multiple pools are available, users can choose the pool to return by defining the `i` parameter of the `find_pool_for_coins` function as shown below.

https://etherscan.io/address/0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5#code

```python
@view
@external
def find_pool_for_coins(_from: address, _to: address, i: uint256 = 0) -> address:
    """
    @notice Find an available pool for exchanging two coins
    @param _from Address of coin to be sent
    @param _to Address of coin to be received
    @param i Index value. When multiple pools are available
            this value is used to return the n'th address.
    @return Pool address
    """
    key: uint256 = bitwise_xor(convert(_from, uint256), convert(_to, uint256))
    return self.markets[key][i]
```

However, the `CurveAdapter._exactInSingle` did not allow users to define the `i` parameter of the `find_pool_for_coins` function. As a result, users are forced to trade against the first pool returned by the Curve Registry.

## Impact

The first pool returned by Curve Registry might not be the most optimal pool to trade with. The first pool might have lesser liquidity, larger slippage, and higher fee than the other pools, resulting in the trade returning lesser assets than expected.

## Code Snippet

https://github.com/sherlock-audit/2023-02-notional/blob/main/leveraged-vaults/contracts/trading/adapters/CurveAdapter.sol#L34

## Tool used

Manual Review

## Recommendation

If multiple pools support the exchange, consider allowing the users to choose which pool they want to trade against.

```diff
function _exactInSingle(Trade memory trade)
	internal view returns (address target, bytes memory executionCallData)
{
	address sellToken = _getTokenAddress(trade.sellToken);
	address buyToken = _getTokenAddress(trade.buyToken);
-	ICurvePool pool = ICurvePool(Deployments.CURVE_REGISTRY.find_pool_for_coins(sellToken, buyToken));
+	ICurvePool pool = ICurvePool(Deployments.CURVE_REGISTRY.find_pool_for_coins(sellToken, buyToken, trade.pool_index));	
```

## Discussion

**jeffywu**

Valid

**hrishibhat**

Given that this is only a possibility and all the conditions for loss of funds are not guaranteed, 
Considering this issue as a valid medium

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4.333333333333333/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Notional Update #2 |
| Report Date | N/A |
| Finders | xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-notional-judging/issues/11
- **Contest**: https://app.sherlock.xyz/audits/contests/52

### Keywords for Search

`vulnerability`

