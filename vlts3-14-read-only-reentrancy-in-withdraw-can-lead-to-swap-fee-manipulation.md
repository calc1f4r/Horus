---
# Core Classification
protocol: Valantis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56686
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-03-17-Valantis.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.40
financial_impact: medium

# Scoring
quality_score: 2
rarity_score: 2

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[VLTS3-14] Read-only reentrancy in withdraw can lead to swap fee manipulation

### Overview


The bug report describes a medium severity issue in the `withdraw` function of the STEXAMM contract. This function allows LP shareholders to withdraw their tokens, but there is a problem with the way it handles the conversion of wHYPE to native HYPE. This can result in users receiving less swap fees than expected. The issue is caused by a lack of proper reentrancy protection, which can be fixed by using a modifier for `view` functions. The bug has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** src/STEXAMM.sol:withdraw#L523-L624

**Description:** In the `withdraw` function for LP shareholders in STEXAMM, the caller can choose to unwrap their wHYPE and receive native HYPE instead. This happens on lines 599-602 and an external call is made to the receiver, giving them execution.

Even though the function itself has the `nonReentrant` modifier, it is still an intermediate state: the `token0` (stHYPE) has already been burned previously using `burnToken0AfterWithdraw` on line 589, while remaining `token1` (wHYPE) is yet to be taken out of the pool using `withdrawLiquidity` on line 611.

Even though the pool itself does not use the `token0/token1` ratio for valuation, it does use this ratio to calculate the swap fee in STEXRatioSwapFeeModule:getSwapFeeInBips, which is used in SovereignPool:swap.

As such, a user can perform a swap inside of the receive callback, when the ratio of `token0/token1` is significantly lower than normal, and get less swap fees as a result.

The reentrancy guard of `STEXAMM` won’t be triggered, because `getLiquidityQuote` is `view` and not marked as `nonReentrant`.
```
    function withdraw(
        uint256 _shares,
        uint256 _amount0Min,
        uint256 _amount1Min,
        uint256 _deadline,
        address _recipient,
        bool _unwrapToNativeToken,
        bool _isInstantWithdrawal
    ) external override nonReentrant returns (uint256 amount0, uint256 amount1) {
        [..]
        
        if (cache.amount1LendingPool > 0) {
          _withdrawalModule.withdrawToken1FromLendingPool(
              cache.amount1LendingPool, _unwrapToNativeToken ? address(this) : _recipient
          );

          if (_unwrapToNativeToken) {
              IWETH9(token1).withdraw(cache.amount1LendingPool);
              Address.sendValue(payable(_recipient), cache.amount1LendingPool);
          }
        }
        
        [..]
    }
```

**Remediation:**  It is advisable to use a modifier for `view` function that are susceptible to read-only reentrancy. The modifier only checks whether the reentrancy guard is active and does not need to set it.

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2/5 |
| Rarity Score | 2/5 |
| Audit Firm | Hexens |
| Protocol | Valantis |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-03-17-Valantis.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

