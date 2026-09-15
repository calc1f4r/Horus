---
# Core Classification
protocol: Polynomial Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20225
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-03-polynomial
source_link: https://code4rena.com/reports/2023-03-polynomial
github_link: https://github.com/code-423n4/2023-03-polynomial-findings/issues/214

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
  - KIntern\_NA
---

## Vulnerability Title

[H-02] Hedging during liquidation is incorrect

### Overview


This bug report describes an issue with the liquidation process of a contract exchange, where the LiquidityPool will lose funds without expectation. When a short position is liquidated in the contract Exchange, the function `_liquidate` will be triggered. This function will burn the power Perp tokens and reduce the short position amount accordingly. Despite this, the `pool.liquidate` function will be called, and the LiquidityPool will be hedged with the same amount of debtRepaying. This leads to LiquidityPool being hedged more than it needs, and the position of the LiquidityPool in the Perp Market being incorrect.

The recommended mitigation step is to not hedge the LiquidityPool during liquidation. This bug report has been confirmed by mubaris (Polynomial).

### Original Finding Content


Hedging will not work as expected, and LiquidityPool will lose funds without expectation.

### Proof of concept

1.  When a short position is liquidated in contract Exchange, function `_liquidate` will be triggered. It will burn the power perp tokens and reduce the short position amount accordingly.

```solidity
function _liquidate(uint256 positionId, uint256 debtRepaying) internal {
    ...
    uint256 finalPosition = position.shortAmount - debtRepaying;
    uint256 finalCollateralAmount = position.collateralAmount - totalCollateralReturned;
    
    shortToken.adjustPosition(positionId, user, position.collateral, finalPosition, finalCollateralAmount);

    pool.liquidate(debtRepaying);
    powerPerp.burn(msg.sender, debtRepaying); 
    ...
```

2.  As you can see, it will decrease the size of short position by  `debtRepaying`, and burn `debtRepaying` power perp tokens. Because of the same amount, the skew of `LiquidityPool` will not change.
3.  Howerver, `pool.liquidate` will be called, and `LiquidityPool` will be hedged with `debtRepaying` amount.

```solidity
function liquidate(uint256 amount) external override onlyExchange nonReentrant {
    (uint256 markPrice, bool isInvalid) = getMarkPrice();
    require(!isInvalid);

    uint256 hedgingFees = _hedge(int256(amount), true);
    usedFunds += int256(hedgingFees);

    emit Liquidate(markPrice, amount);
}
```

4.  Therefore, LiquidityPool will be hedged more than it needs, and the position of `LiquidityPool` in the Perp Market will be incorrect (compared with what it should be for hedging).

### Recommended Mitigation Steps

Should not hedge the LiquidityPool during liquidation.

**[mubaris (Polynomial) confirmed](https://github.com/code-423n4/2023-03-polynomial-findings/issues/214#issuecomment-1494185661)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Polynomial Protocol |
| Report Date | N/A |
| Finders | KIntern\_NA |

### Source Links

- **Source**: https://code4rena.com/reports/2023-03-polynomial
- **GitHub**: https://github.com/code-423n4/2023-03-polynomial-findings/issues/214
- **Contest**: https://code4rena.com/reports/2023-03-polynomial

### Keywords for Search

`vulnerability`

