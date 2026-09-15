---
# Core Classification
protocol: StakeDAO_2025-07-21
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63617
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-10] Oracle price manipulation causes incorrect collateral and utilization

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

In the `MorphoMarketFactory.create()` function, the amount of `collateralToSupply` is calculated based on the current `lp_price()` from either the `CurveStableswapOracle` or `CurveCryptoswapOracle`. However, both oracle's documentation **acknowledge** that the LP token price can be **manipulated within a single block** due to flash deposits/withdrawals.

Since `collateralToSupply` is pulled from the deployer based on this price, two risks arise:

- If the price is artificially low, more collateral than necessary will be pulled from the deployer.
- If the price is artificially high, less collateral than required will be pulled, and the expected utilization ratio (e.g., 90%) will not be achieved accurately.

After the block settles, and if the LP price drops back to its real value, the position may appear under-collateralized, potentially triggering liquidation in the next block.

```solidity
 function create(IStrategyWrapper collateral, IERC20Metadata loan, IOracle oracle, address irm, uint256 lltv)
        external
        onlyDelegateCall
        returns (Id id)
    {
        //...
        uint256 collateralToSupply = Math.mulDiv(
            Math.mulDiv(borrowAmount, 10 ** oracle.ORACLE_BASE_EXPONENT(), oracle.price(), Math.Rounding.Ceil),
            1e18,
            lltv,
            Math.Rounding.Ceil
        );

        //...
        vault.safeTransferFrom(msg.sender, address(this), collateralToSupply);
        //...
    }
```

Recommendation:  
Consider adding slippage tolerance validation against recent pricing before finalizing market creation.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StakeDAO_2025-07-21 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

