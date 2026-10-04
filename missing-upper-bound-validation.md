---
# Core Classification
protocol: WeightedLiquidityPool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52422
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dexodus/weightedliquiditypool
source_link: https://www.halborn.com/audits/dexodus/weightedliquiditypool
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

Missing Upper Bound Validation

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `setswapSlippage` function does not validate that the provided `slippage` value is less than or equal to `BASIS_POINTS`. If `slippage` is set to a value greater than `BASIS_POINTS`, it will result in underflows during calculations in the `swapEthToUsdc` and `swapUsdcToEth` functions. Specifically, the subtraction for `minUsdcOut` and `minWethOut` could yield negative results, causing the contract to revert.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:M/D:N/Y:N/R:P/S:C (3.9)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:M/D:N/Y:N/R:P/S:C)

##### Recommendation

Add a validation check in the `setswapSlippage` function to ensure that `slippage` does not exceed `BASIS_POINTS`. For example:

```
function setswapSlippage(uint256 slippage) external onlyOwner {
    require(slippage <= BASIS_POINTS, "Slippage exceeds allowable range");
    swapSlippage = slippage;
}

```

This ensures the `swapEthToUsdc` and `swapUsdcToEth` functions operate correctly and avoids unintended underflows. By restricting `slippage` to a valid range, the contract's behavior remains predictable and secure.

##### Remediation

**SOLVED**: The code is now checking for the upper bounds.

##### Remediation Hash

1f89558c1394d2c6a59238172e3e17ed50e32265

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | WeightedLiquidityPool |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/dexodus/weightedliquiditypool
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/dexodus/weightedliquiditypool

### Keywords for Search

`vulnerability`

