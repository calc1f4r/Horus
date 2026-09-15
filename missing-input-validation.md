---
# Core Classification
protocol: Hooks Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52474
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/tren-finance/hooks-contracts
source_link: https://www.halborn.com/audits/tren-finance/hooks-contracts
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Missing Input Validation

### Overview

See description below for full details.

### Original Finding Content

##### Description

Several functions in both `SwapManager` and `CurveSwapper` lack proper input validation, relying on assumptions about parameters that may not always hold true. This oversight introduces potential vulnerabilities and operational risks.

  

Examples:

* **SwapManager's** `_swapExactInput` **Function:** The function assumes the `pathFee` array always contains exactly two elements but performs no validation:

```
function _swapExactInput(..., uint256[] memory pathFee) private returns (uint256) {
    // ...
    IRouter.ExactInputParams memory params = IRouter.ExactInputParams({
        path: abi.encodePacked(
            address(tokenOut),
            uint24(pathFee[1]),
            stablecoin,
            uint24(pathFee[0]),
            tokenIn
        ),
        // ...
    });
}
```

  

* **CurveSwapper's** `swap` **Function:** The function assumes that any input token not equal to `underlyingAsset` must be the collateral token (`coll`):

```
function swap(address tokenIn, uint256 amount, address recipient) external onlySwapManager returns (uint256) {
    if (tokenIn == underlyingAsset) {
        // ... add liquidity logic ...
    } else {
        // @audit No validation that tokenIn == coll
        coll.approve(address(curvePool), amount);
        tokenAmountOut = curvePool.remove_liquidity_one_coin(...);
    }
}
```

If `tokenIn` is neither the `underlyingAsset` nor the `coll`, the function will incorrectly approve and interact with `curvePool`, leading to potentially undefined behavior.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:L/A:L/D:L/Y:L/R:P/S:U (2.2)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:L/A:L/D:L/Y:L/R:P/S:U)

##### Recommendation

Implement robust input validation for all critical functions to enforce expected parameter requirements. This will prevent unexpected behavior, reduce debugging complexity, and enhance overall security.

For the `SwapManager` example, make sure the `pathFee` argument only has two elements:

```
function _swapExactInput(..., uint256[] memory pathFee) private returns (uint256) {
    if (pathFee.length != 2) {
        revert SwapManager__InvalidPathLength();
    }
    // ... rest of the function
}
```

  

For the `CurveSwapper` example, validate that the `tokenIn` address is the expected by not assuming it is `coll`:

```
function swap(address tokenIn, uint256 amount, address recipient) external onlySwapManager returns (uint256) {
    if (tokenIn == underlyingAsset) {
        // ... add liquidity logic ...
    } else if (tokenIn == address(coll)) {
        // ... remove liquidity logic ...
    } else {
        revert CurveSwapper__InvalidTokenIn();
    }
}
```

  

Consider adding comprehensive input validation across all functions that make assumptions about their parameters.

##### Remediation

**SOLVED:** The **Tren finance team** fixed this finding in commit `a956282` by implementing the recommendation.

##### Remediation Hash

<https://github.com/Tren-Finance/Tren-Contracts/commit/a956282936a76e8e2cb2e602aa07e806f02f3c43>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Hooks Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/tren-finance/hooks-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/tren-finance/hooks-contracts

### Keywords for Search

`vulnerability`

