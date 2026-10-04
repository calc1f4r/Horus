---
# Core Classification
protocol: The Standard Auto Redemption
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45061
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
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
  - Giovanni Di Siena
---

## Vulnerability Title

`USDs` redemption calculation can be manipulated due to unsafe signed-unsigned cast

### Overview


Summary:

The bug report describes an issue in the code for calculating the redemption amount of a cryptocurrency called USDs. The code does not properly handle negative values, which can result in incorrect redemption amounts and potentially cause the system to fail. The recommended solution is to check the sign of the variable before incrementing it and to use a specific library for this type of calculation. The bug has been fixed by a commit from the Standard DAO and verified by Cyfrin.

### Original Finding Content

**Description:** The following logic is executed when calculating the `USDs` redemption amount, after the tick range has been advanced beyond that of the current tick:

```solidity
} else {
    (, int128 _liquidityNet,,,,,,) = pool.ticks(_lowerTick);
    _liquidity += uint128(_liquidityNet);
    (_amount0,) = LiquidityAmounts.getAmountsForLiquidity(
        _sqrtPriceX96,
        TickMath.getSqrtRatioAtTick(_lowerTick),
        TickMath.getSqrtRatioAtTick(_upperTick),
        _liquidity
    );
}
```

The `_liquidityNet` variable represents the net active liquidity delta when crossing between tick ranges, so this is considered along with the active liquidity of the original range; however, this value is cast from a signed integer to unsigned without actually checking the sign. Given that negative signed integers are represented using two's complement, net negative liquidities (i.e. less active liquidity in the subsequent range) will silently result in the incremented `_liquidity` being a very large number. This scenario could occur accidentally, or be forced by an attacker by the addition of just-in-time (JIT) liquidity, causing the target vault to be fully redeemed for the maximum `USDs`:

```solidity
if (_USDsTargetAmount > _vaultData.status.minted) _USDsTargetAmount = _vaultData.status.minted;
```

**Impact:** In the best case, more debt could be repaid than intended. In the worst case, fulfilment could be made to revert which will permanently disable auto redemption functionality (as described in a separate issue).

**Recommended Mitigation:** The sign of `_liquidityNet` should be checked before incrementing `_liquidity`, subtracting the absolute value if it is negative. Consider using the `LiquidityMath` [library](https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/LiquidityMath.sol).

**The Standard DAO:** Fixed by commit [49af007](https://github.com/the-standard/smart-vault/commit/49af007bcce5079ebfdc3de8f0c231ec4d0f121c).

**Cyfrin:** Verified. The `LiquidityMath` library is now used.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | The Standard Auto Redemption |
| Report Date | N/A |
| Finders | Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

