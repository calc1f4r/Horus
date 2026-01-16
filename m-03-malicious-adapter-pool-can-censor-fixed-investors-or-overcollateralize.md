---
# Core Classification
protocol: Saffron_2025-07-31
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62946
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review_2025-07-31.md
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

[M-03] Malicious adapter pool can censor fixed investors or overcollateralize

### Overview


The report indicates a bug in the protocol that can be exploited by malicious actors. The bug is related to the lack of an upper bound check on the liquidity provided by Fixed Side investors during capital deployment. This can result in Fixed Side investors unintentionally providing more liquidity than intended, leading to unfair distribution of profits and potential denial of service for Fixed Side participants. The report recommends enforcing upper bound liquidity checks and ensuring adapter pool authenticity to prevent this bug from being exploited.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Low

## Description

The protocol currently lacks an upper bound check on the actual liquidity provided by Fixed Side investors during capital deployment. In the `deployCapital()` process, token amounts (amount0, amount1) are calculated using pool parameters obtained via `pool.slot0()`. However, the provided pool address is not verified against Uniswap V3 Factory to ensure authenticity.

### Adapter Deployment (Unverified Pool):

```solidity
function createAdapter(
    uint256 adapterTypeId,
    address poolAddress,
    bytes calldata data
) public virtual {
    ...
    IAdapter(adapterAddress).initialize(adapterId, poolAddress, defaultDepositTolerance, data);
}
```

### Adapter Initialization:

```solidity
function initialize(
    uint256 _id,
    address _pool,
    uint256 _depositTolerance,
    bytes memory uniV3InitData
) public virtual override onlyWithoutVaultAttached onlyFactory {
    ...
    IUniswapV3Pool uniswapV3Pool = IUniswapV3Pool(_pool);
    pool = uniswapV3Pool;
}
```

A malicious actor can deploy an adapter pointing to a fake pool contract that returns manipulated `sqrtPriceX96` values, causing incorrect computation of required token amounts. As a result, the Fixed Side investor (even unintentionally) may provide **significantly more liquidity** than intended when minting the position.

### Token Amount Calculation using slot0():

```solidity
(uint160 sqrtRatioX96, , , , , , ) = pool.slot0();
(uint256 amount0, uint256 amount1) = LiquidityAmounts.getAmountsForLiquidity(
    sqrtRatioX96,
    poolMinTick.getSqrtRatioAtTick(),
    poolMaxTick.getSqrtRatioAtTick(),
    fixedSideCapacity
);
```

While the protocol verifies that actual minted liquidity meets a minimum threshold (`l * invDepositTolerance`), there is no check ensuring that the liquidity does **not exceed** a maximum limit:

```solidity
require(uint256(l) * invDepositTolerance / 10000 < _liquidity, "L");
```

### Attack Scenarios:

1. **Overcollateralization Exploit:**

   * Overcollateralizing Fixed Side shifts the position's weight towards Variable Side investors.
   * Variable Side participants unfairly receive a larger share of the position's yield, while Fixed Side investors risk more capital than intended.

2. **Censorship of Fixed Side Participation (Denial of Service):**

   * By setting the malicious pool's slot0() to return extreme values, an attacker can cause the calculated `amount0` and `amount1` to be unrealistically small.
   * Honest Fixed Side investors' calls will be reverted due to current slippage protection, effectively **blocking their ability to deploy capital**.
   * This **censorship vector** can be used to paralyze Fixed Side participation in specific Vaults.

This scenario can occur even if Fixed Side investors are non-malicious. However, a deliberate attacker could exploit this by:

1. Deploying a malicious adapter with a manipulated pool.
2. Forcing Fixed Side investors to overcontribute liquidity.
3. Or, preventing Fixed Side investors from participating altogether (censorship).
4. Then, entering as a Variable Side investor to gain an outsized share of profits without proportional risk.

## Recommendations

1. **Enforce Upper Bound Liquidity Checks:**

   * After minting, verify that the actual liquidity does not exceed a defined tolerance:

     ```solidity
     require(_liquidity <= uint256(l) * depositTolerance / 10000, "Excessive liquidity");
     ```
   * Where `depositTolerance` could be set to a reasonable upper slippage (e.g., 10100 = +1%).

2. **Ensure Adapter Pool Authenticity:**

   * Validate the pool address against Uniswap V3 Factory in the adapter constructor to prevent malicious pool injection.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Saffron_2025-07-31 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review_2025-07-31.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

