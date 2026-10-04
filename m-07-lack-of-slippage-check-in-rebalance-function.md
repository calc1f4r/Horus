---
# Core Classification
protocol: Radiant June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36378
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-June.md
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

[M-07] Lack of slippage check in `rebalance` Function

### Overview


The `rebalance` function in the Uniswap V3 LP contract does not have a slippage check, making it vulnerable to sandwich attacks. This means that an attacker can manipulate the price of the swap, causing a loss of funds for the contract. To fix this, a slippage check should be implemented to ensure that the swap stays within acceptable price limits.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

The `rebalance` function updates the Uniswap V3 LP position and performs the indicated swap based on the specified lower and upper ticks. However, this function lacks a slippage check, making it vulnerable to sandwich attacks. An attacker can front-run the rebalance transaction, causing unfavorable price movements, and then back-run the transaction to revert the price, resulting in a loss of funds for the contract when swapping.

```solidity
function rebalance(int24 _baseLower, int24 _baseUpper, int256 swapQuantity) public nonReentrant isRebalancer {
    ...
    if (swapQuantity != 0) {
        IUniswapV3Pool(pool).swap(
            address(this),
            swapQuantity > 0, // zeroToOne == true if swapQuantity is positive
            swapQuantity > 0 ? swapQuantity : -swapQuantity,
            // No limit on the price, swap through the ticks, until the `swapQuantity` is exhausted
            swapQuantity > 0 ? UniV3PoolMath.MIN_SQRT_RATIO + 1 : UniV3PoolMath.MAX_SQRT_RATIO - 1,
            abi.encode(address(this))
        );
    }
    ...
}
```

The absence of a slippage check means that the function does not verify the price impact of the swap, leaving it susceptible to manipulation by external actors.

**Recommendations**

To address this issue, implement slippage protection by adding a slippage check to the `rebalance` function. This can be achieved by specifying acceptable price limits for the swap and reverting the transaction if these limits are breached.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Radiant June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

