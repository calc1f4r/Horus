---
# Core Classification
protocol: Lambo.win
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49618
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-12-lambowin
source_link: https://code4rena.com/reports/2024-12-lambowin
github_link: https://code4rena.com/audits/2024-12-lambowin/submissions/F-152

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
finders_count: 1
finders:
  - Evo
---

## Vulnerability Title

[M-07] Rebalance profit requirement prevents maintaining VETH/WETH peg

### Overview


The report discusses a bug in the code for the LamboRebalanceOnUniwap contract. The code currently has a requirement that the profit must be greater than zero in order for the contract to rebalance the VETH/WETH pool. However, this goes against the protocol's stated design goal of maintaining a 1:1 ratio for the pool, even if there is no profit to be made. The report recommends changing the code to allow for rebalancing even when there is no profit. The team behind Lambo.win has acknowledged the issue and it is recommended to update the code to address this bug.

### Original Finding Content



<https://github.com/code-423n4/2024-12-lambowin/blob/b8b8b0b1d7c9733a7bd9536e027886adb78ff83a/src/rebalance/LamboRebalanceOnUniwap.sol# L62>

The `profit > 0` requirement in the rebalance function actively prevents the protocol from maintaining the VETH/WETH 1:1 peg during unprofitable market conditions, when profit is ZERO.

### Proof of Concept

The protocol documentation and team’s design goals that the RebalanceOnUniswap contract is specifically designed to maintain the VETH/WETH pool ratio at 1:1, intentionally accepting gas losses as a trade-off for improved price stability.

It is mentioned in the previous audit, In the sponsor’s acknowledgement (from SlowMist audit, N12):

> According to the project team, the RebalanceOnUniswap contract is designed to maintain the VETH/WETH pool ratio at 1:1 rather than for profit. Gas costs are intentionally omitted to increase rebalancing frequency, accepting gas losses as a trade-off for improved price stability.

However, in [LamboRebalanceOnUniwap.sol# L68](https://github.com/code-423n4/2024-12-lambowin/blob/b8b8b0b1d7c9733a7bd9536e027886adb78ff83a/src/rebalance/LamboRebalanceOnUniwap.sol# L68):
```

    function rebalance(uint256 directionMask, uint256 amountIn, uint256 amountOut) external nonReentrant {
	    uint256 balanceBefore = IERC20(weth).balanceOf(address(this));
	    bytes memory data = abi.encode(directionMask, amountIn, amountOut);
	    IMorpho(morphoVault).flashLoan(weth, amountIn, data);
	    uint256 balanceAfter = IERC20(weth).balanceOf(address(this));
	    uint256 profit = balanceAfter - balanceBefore;
	    require(profit > 0, "No profit made");
}
```

The `require(profit > 0)` check means:

* Rebalancing can only occur when profitable, in situations where rebalancing is needed but arbitrage profits are zero, this directly contradicts the protocol’s stated design goal of accepting no profit to maintain the ratio 1:1.

An example scenario would be:

* VETH/WETH ratio deviates from 1:1
* Rebalancing opportunity exists to restore the peg
* Market conditions mean rebalancing would offer no profit but can still done
* The profit check prevents rebalancing

### Recommended Mitigation Steps

Update the `require(profit > 0)` to `require(profit >= 0)`.

**Shaneson (Lambo.win) acknowledged**

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lambo.win |
| Report Date | N/A |
| Finders | Evo |

### Source Links

- **Source**: https://code4rena.com/reports/2024-12-lambowin
- **GitHub**: https://code4rena.com/audits/2024-12-lambowin/submissions/F-152
- **Contest**: https://code4rena.com/reports/2024-12-lambowin

### Keywords for Search

`vulnerability`

