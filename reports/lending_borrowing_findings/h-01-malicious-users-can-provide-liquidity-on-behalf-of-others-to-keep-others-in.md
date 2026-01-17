---
# Core Classification
protocol: QuickSwap and StellaSwap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28848
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-quickswap
source_link: https://code4rena.com/reports/2022-09-quickswap
github_link: https://github.com/code-423n4/2022-09-quickswap-findings/issues/70

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

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-01] Malicious users can provide liquidity on behalf of others to keep others in the liquidity cooldown

### Overview


A bug has been identified in the AlgebraPool contract of QuickSwap and StellaSwap, which allows malicious users to keep other users on liquidity cooldown forever by providing a little bit of liquidity on behalf of other users. This would prevent other users from removing liquidity and lock their funds. This has been confirmed by vladyan18 and judged as a High severity issue by 0xean.

The bug is located in the mint and burn functions of the AlgebraPool contract. In the mint function, users can provide liquidity on behalf of other users, which also means that malicious users can keep other users on liquidity cooldown forever by providing a little bit of liquidity on behalf of other users. The burn function also includes a check to ensure that the current time is greater than lastLiquidityAddTimestamp + \_liquidityCooldown, however liquidityCooldown is max 1 day.

To mitigate this issue, consider allowing users to provide liquidity only for themselves, or setting liquidityCooldown to 0.

### Original Finding Content


In the AlgebraPool contract, when the user provides liquidity via the mint function, the lastLiquidityAddTimestamp is updated to the current time.

          (_position.liquidity, _position.lastLiquidityAddTimestamp) = (
            liquidityNext,
            liquidityNext > 0 ? (liquidityDelta > 0 ? _blockTimestamp() : lastLiquidityAddTimestamp) : 0
          );

Later when the user removes the liquidity via burn function, the transaction will revert if the current time is less than lastLiquidityAddTimestamp + \_liquidityCooldown.

          if (liquidityDelta < 0) {
            uint32 _liquidityCooldown = liquidityCooldown;
            if (_liquidityCooldown > 0) {
              require((_blockTimestamp() - lastLiquidityAddTimestamp) >= _liquidityCooldown);
            }
          }

liquidityCooldown is max 1 day.<br>
However, in the mint function, users can provide liquidity on behalf of other users, which also means that malicious users can keep other users on liquidity cooldown forever by providing a little bit of liquidity on behalf of other users, thus preventing other users from removing liquidity.

```
  function mint(vladyan18
    address sender,
    address recipient,  // @audit: users can provide liquidity on behalf of other users
    int24 bottomTick,
    int24 topTick,
    uint128 liquidityDesired,
    bytes calldata data
  )
...
      (, int256 amount0Int, int256 amount1Int) = _updatePositionTicksAndFees(recipient, bottomTick, topTick, int256(liquidityActual).toInt128());

```

### Proof of Concept

[AlgebraPool.sol#L226-L231](https://github.com/code-423n4/2022-09-quickswap/blob/15ea643c85ed936a92d2676a7aabf739b210af39/src/core/contracts/AlgebraPool.sol#L226-L231)<br>
[AlgebraPool.sol#L513-L523](https://github.com/code-423n4/2022-09-quickswap/blob/15ea643c85ed936a92d2676a7aabf739b210af39/src/core/contracts/AlgebraPool.sol#L513-L523)<br>

### Recommended Mitigation Steps

Consider allowing users to provide liquidity only for themselves, or setting liquidityCooldown to 0.

**[vladyan18 (QuickSwap & StellaSwap) confirmed](https://github.com/code-423n4/2022-09-quickswap-findings/issues/70)**

**[sameepsi (QuickSwap & StellaSwap) disagreed with severity and commented](https://github.com/code-423n4/2022-09-quickswap-findings/issues/70#issuecomment-1266436575):**
 > This is a valid issue but the severity should be medium. This can be easily mitigated by simply setting up cool down period to 0.

**[0xean (judge) commented](https://github.com/code-423n4/2022-09-quickswap-findings/issues/70#issuecomment-1267015318):**
 > See comment on [issue #83](https://github.com/code-423n4/2022-09-quickswap-findings/issues/83#issuecomment-1264731071).
> 
> Issue is valid and leads to locking of funds, High severity is warranted.  Turning cool down to 0 would work, but has other consequences for JIT liquidity. 



***
 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | QuickSwap and StellaSwap |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-quickswap
- **GitHub**: https://github.com/code-423n4/2022-09-quickswap-findings/issues/70
- **Contest**: https://code4rena.com/reports/2022-09-quickswap

### Keywords for Search

`vulnerability`

