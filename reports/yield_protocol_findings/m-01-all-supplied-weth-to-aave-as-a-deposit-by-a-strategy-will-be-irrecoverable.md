---
# Core Classification
protocol: BakerFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33664
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-bakerfi
source_link: https://code4rena.com/reports/2024-05-bakerfi
github_link: https://github.com/code-423n4/2024-05-bakerfi-findings/issues/41

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
  - 0xStalin
  - zhaojie
---

## Vulnerability Title

[M-01] All supplied WETH to Aave as a deposit by a Strategy will be irrecoverable

### Overview


This bug report identifies a problem in the BakerFi code that could result in the loss of WETH supplied to Aave. The report includes a proof of concept that shows how the strategy does not have the ability to withdraw WETH from Aave, only collateral. This means that any leftover WETH after a swap will be deposited back into Aave and cannot be retrieved. The report recommends a mitigation step to use the excess WETH to repay more debt on Aave instead of supplying it, which will also improve the loan to value ratio. The BakerFi team has confirmed and fixed the issue. 

### Original Finding Content


### Impact

WETH supplied to Aave will be lost.

### Proof of Concept

When a strategy pays debt on Aave it does a swap of the withdrawn collateral from Aave in exchange for WETH. After the swap is completed, it checks [if there are any weth leftovers after the swap, if so, it deposits them back](https://github.com/code-423n4/2024-05-bakerfi/blob/main/contracts/core/strategies/StrategyLeverage.sol#L562-L566). The problem with this approach is that the strategy doesn't have any means to pull WETH out of Aave, the strategy is only capable of withdrawing the collateral from Aave, but not WETH.

```
    function _payDebt(uint256 debtAmount, uint256 fee) internal {
      ...

      //@audit-info => output represents the received amount of WETH for the swap
      uint256 output = _swap(
          ISwapHandler.SwapParams(
              ierc20A(),
              wETHA(),
              ISwapHandler.SwapType.EXACT_OUTPUT,
              amountIn,
              debtAmount + fee,
              _swapFeeTier,
              bytes("")
          )
      );

      //@audit-info => Checks if there are any WETH leftovers
      // When there are leftovers from the swap, deposit then back
      uint256 wethLefts = output > (debtAmount + fee) ? output - (debtAmount + fee) : 0;

      //@audit-issue => If any leftover WETH, it deposits them onto Aave!
      //@audit-issue => Once the WETH is deposited in Aave, the Strategy won't be able to pull it out.
      if (wethLefts > 0) {
          _supply(wETHA(), wethLefts);
      }
      emit StrategyUndeploy(msg.sender, debtAmount);
    }
```

The strategy uses the [`StrategyAAVEv3._withdraw() function`](https://github.com/code-423n4/2024-05-bakerfi/blob/main/contracts/core/strategies/StrategyAAVEv3.sol#L126-L129) to withdraw an asset from Aave, but, in the places where this function is called, the only assets requested to be withdrawn is the Collateral.

*   in the [`StrategyLeverage._payDebt()`](https://github.com/code-423n4/2024-05-bakerfi/blob/main/contracts/core/strategies/StrategyLeverage.sol#L549)
*   in the [`StrategyLeverage._repayAndWithdraw()`](https://github.com/code-423n4/2024-05-bakerfi/blob/main/contracts/core/strategies/StrategyLeverage.sol#L701)

### Recommended Mitigation Steps

Instead of supplying the `wethLefts`, use the excess WETH to repay more WETH debt on Aave, in this way, those extra WETHs won't be lost on Aave because the strategy doesn't have any means to withdraw them.

*   By using the extra WETH to repay more debt, the loan to value is brought down even to a healthier level.

```
    function _payDebt(uint256 debtAmount, uint256 fee) internal {
      ...
      ...
      ...

      //@audit => Instead of supplying WETH to Aave, use it to repay more debt
      if (wethLefts > 0) {
    -     _supply(wETHA(), wethLefts);
    +     _repay(wETHA(), wethLefts);
      }
      emit StrategyUndeploy(msg.sender, debtAmount);
    }
```

**[hvasconcelos (BakerFi) confirmed](https://github.com/code-423n4/2024-05-bakerfi-findings/issues/41#event-13082103117)**

**[ickas (BakerFi) commented](https://github.com/code-423n4/2024-05-bakerfi-findings/issues/41#issuecomment-2176097220):**
 > Fixed → https://github.com/baker-fi/bakerfi-contracts/pull/42



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BakerFi |
| Report Date | N/A |
| Finders | 0xStalin, zhaojie |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-bakerfi
- **GitHub**: https://github.com/code-423n4/2024-05-bakerfi-findings/issues/41
- **Contest**: https://code4rena.com/reports/2024-05-bakerfi

### Keywords for Search

`vulnerability`

