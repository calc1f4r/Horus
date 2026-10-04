---
# Core Classification
protocol: GammaSwap_2024-12-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45533
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GammaSwap-security-review_2024-12-30.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] `rebalancePosition()` transaction is susceptible to frontrunning

### Overview


The report discusses a bug in the `rebalancePosition()` function of the `GammaVault` manager. This bug can potentially cause the transaction to fail, preventing the position from being closed. The bug occurs when the `s.totalLiquidity` value is used to close the position, which can be manipulated by a malicious user causing the transaction to revert. To fix this bug, it is recommended to fetch the position liquidity directly from the Uniswap V3 position manager instead of using the cached value. This will prevent frontrunning and ensure the position can be closed successfully. 

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Position collaterals are rebalanced to align with a desired ratio specified by the `GammaVault` manager when the manager calls `rebalancePosition`. The steps performed during the rebalancing process include:

1. Collecting fees from the Uniswap V3 position.
2. Decreasing liquidity to zero.
3. Closing the position.
4. Opening a new position with a revised hedge.

```javascript
 function rebalancePosition(
        IGammaVault.RebalancePositionData memory params
    ) external virtual override {
        _validatePaths(params.path0, params.path1);

        _collectFees(s.tokenId, address(this));
        _decreaseLiquidity(
            s.tokenId,
            s.totalLiquidity,
            params.amount0Min,
            params.amount1Min
        );
        _closeLP(s.tokenId);

        //...
    }
```

```javascript
    function _closeLP(uint256 _tokenId) internal {
        if (_tokenId > 0) {
            IUniswapV3PositionManager(nftPosMgr).burn(_tokenId);
            s.tokenId = 0;
        }
    }
```

The `IUniswapV3PositionManager(nftPosMgr).burn()` call requires the position to have zero liquidity; otherwise, the transaction will revert:

```javascript
   function burn(uint256 tokenId) external payable override isAuthorizedForToken(tokenId) {
        Position storage position = _positions[tokenId];
        require(position.liquidity == 0 && position.tokensOwed0 == 0 && position.tokensOwed1 == 0, 'Not cleared');
        delete _positions[tokenId];
        _burn(tokenId);
    }
```

The `s.totalLiquidity` value is expected to be the total liquidity of the position, required for closing the position after withdrawal, however, using this cached value exposes the` rebalancePosition()` transaction to frontrunning, where a malicious user can frontrun the transaction by calling `NonfungiblePositionManager.increaseLiquidity()` and adding 1 wei of liquidity to the position.

This would cause the `burn()` call to revert, preventing the position from being closed since liquidity would no longer be zero.

## Recommendations

Fetch the position liquidity directly from the Uniswap V3 position manager inside the `rebalancePosition()` :

```diff
 function rebalancePosition(
        IGammaVault.RebalancePositionData memory params
    ) external virtual override {
        _validatePaths(params.path0, params.path1);
+   uint256 _totalLiquidity = _getTotalLiquidity(_tokenId);
        _collectFees(s.tokenId, address(this));
        _decreaseLiquidity(
            s.tokenId,
-           s.totalLiquidity,
+         _totalLiquidity,
           params.amount0Min,
            params.amount1Min
        );
        _closeLP(s.tokenId);

        //...
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | GammaSwap_2024-12-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GammaSwap-security-review_2024-12-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

