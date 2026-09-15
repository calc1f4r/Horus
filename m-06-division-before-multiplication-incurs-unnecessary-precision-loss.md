---
# Core Classification
protocol: Numoen
chain: everychain
category: arithmetic
vulnerability_type: precision_loss

# Attack Vector Details
attack_type: precision_loss
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6516
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-numoen-contest
source_link: https://code4rena.com/reports/2023-01-numoen
github_link: https://github.com/code-423n4/2023-01-numoen-findings/issues/45

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - precision_loss

protocol_categories:
  - liquid_staking
  - dexes
  - lending
  - bridge
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - ladboy233
  - Breeje
---

## Vulnerability Title

[M-06] Division before multiplication incurs unnecessary precision loss

### Overview


This bug report is about a vulnerability in the codebase of a software system. The vulnerability is that the code is performing division before multiplication, which is causing unnecessary precision loss. This is happening when accruing interest and when computing an invariant.

Proof of concept is provided with the report, which shows that the code is performing division before multiplication, which is causing the precision loss. The code first divides the value borrowRate * totalLiquidityBorrowed / 1e18, and when computing the invariant, it divides amount0 * 1e18 / liqudiity.

The impact of this vulnerability is that it causes unnecessary precision loss.

The bug was identified using manual review.

The recommended mitigation step is to avoid division before multiplication and always perform division operation at last.

### Original Finding Content


[src/core/Pair.sol#L56](https://github.com/code-423n4/2023-01-numoen/blob/2ad9a73d793ea23a25a381faadc86ae0c8cb5913/src/core/Pair.sol#L56)<br>
[src/core/Pair.sol#L57](https://github.com/code-423n4/2023-01-numoen/blob/2ad9a73d793ea23a25a381faadc86ae0c8cb5913/src/core/Pair.sol#L57)<br>
[core/Lendgine.sol#L252](https://github.com/code-423n4/2023-01-numoen/blob/2ad9a73d793ea23a25a381faadc86ae0c8cb5913/src/core/Lendgine.sol#L252)

### Proof of Concept

In the current codebase, FullMath.mulDiv is used, the function takes three parameters.

Basically `FullMath.mulDIv(a, b, c)` means `a * b / c`.

Then there are some operations which incur unnecessary precision loss because of division before multiplcation.

When accruing interest, the code below:

```solidity
  /// @notice Helper function for accruing lendgine interest
  function _accrueInterest() private {
    if (totalSupply == 0 || totalLiquidityBorrowed == 0) {
      lastUpdate = block.timestamp;
      return;
    }

    uint256 timeElapsed = block.timestamp - lastUpdate;
    if (timeElapsed == 0) return;

    uint256 _totalLiquidityBorrowed = totalLiquidityBorrowed; // SLOAD
    uint256 totalLiquiditySupplied = totalLiquidity + _totalLiquidityBorrowed; // SLOAD

    uint256 borrowRate = getBorrowRate(_totalLiquidityBorrowed, totalLiquiditySupplied);

    uint256 dilutionLPRequested = (FullMath.mulDiv(borrowRate, _totalLiquidityBorrowed, 1e18) * timeElapsed) / 365 days;
    uint256 dilutionLP = dilutionLPRequested > _totalLiquidityBorrowed ? _totalLiquidityBorrowed : dilutionLPRequested;
    uint256 dilutionSpeculative = convertLiquidityToCollateral(dilutionLP);

    totalLiquidityBorrowed = _totalLiquidityBorrowed - dilutionLP;
    rewardPerPositionStored += FullMath.mulDiv(dilutionSpeculative, 1e18, totalPositionSize);
    lastUpdate = block.timestamp;

    emit AccrueInterest(timeElapsed, dilutionSpeculative, dilutionLP);
  }
```

Note the line:

```solidity
 uint256 dilutionLPRequested = (FullMath.mulDiv(borrowRate, _totalLiquidityBorrowed, 1e18) * timeElapsed) / 365 days;
```

This basically equals to `dilutionLPRequested = (borrowRate * totalLiquidityBorrowed / 1e18 * timeElapsed) / 365 days`

The first part of division can greatly truncate the value `borrowRate * totalLiquidityBorrowed / 1e18`, the totalLiquidityBorrowed should be normalized and scaled by token precision when adding liqudity instead of division by 1e18 here.

Same preicision loss happens when computng the invariant

```solidity
  /// @inheritdoc IPair
  function invariant(uint256 amount0, uint256 amount1, uint256 liquidity) public view override returns (bool) {
    if (liquidity == 0) return (amount0 == 0 && amount1 == 0);

    uint256 scale0 = FullMath.mulDiv(amount0, 1e18, liquidity) * token0Scale;
    uint256 scale1 = FullMath.mulDiv(amount1, 1e18, liquidity) * token1Scale;
```

`scale0 = (amount0 * 1e18 / liqudiity) * token0Scale`<br>
`scale1 = (amount1 * 1e18 / liqudiity) * token1Scale`

Whereas the amount0 and amount1 should be first be normalized by token0Scale and token1Scale and then divided by liquidity at last. If the liquidity is a larger number  `amount0 * 1e18 / liqudity` is already truncated to 0.

### Recommended Mitigation Steps

We recommend the protocol avoid divison before multiplication and always perform division operation at last.

**[kyscott18 (Numoen) confirmed](https://github.com/code-423n4/2023-01-numoen-findings/issues/45#issuecomment-1423236922)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Numoen |
| Report Date | N/A |
| Finders | ladboy233, Breeje |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-numoen
- **GitHub**: https://github.com/code-423n4/2023-01-numoen-findings/issues/45
- **Contest**: https://code4rena.com/contests/2023-01-numoen-contest

### Keywords for Search

`Precision Loss`

