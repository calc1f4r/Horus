---
# Core Classification
protocol: Hyperdrive June 2023
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35849
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
github_link: none

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
finders_count: 4
finders:
  - Saw-Mon and Natalie
  - Christoph Michel
  - Deivitto
  - M4rio.eth
---

## Vulnerability Title

addLiquidity(...) can be griefed

### Overview


This report discusses a high-risk bug in the HyperdriveLP and HyperdriveMath contracts. The bug allows an attacker to block other users from providing liquidity to the Hyperdrive by causing a division by zero error. This can be done by opening a short position with the maximum possible amount, which causes the APR calculation to result in a very large number. This issue is similar to previous attacks where the attacker tries to open a short with the maximum amount. The report recommends further analysis to prevent similar issues and suggests adding additional checks to prevent the division by zero attack. The issue has been partially addressed by mitigating the possibility of share reserves being too small, but the likelihood of this attack being successful is low due to the high fees required. 

### Original Finding Content

## Severity: High Risk

## Context
- HyperdriveLP .sol#L103-L110
- HyperdriveMath.sol#L47-L73
- HyperdriveLP .sol#L172

## Description
An attacker can DoS/block another user from providing liquidity to the Hyperdrive. The attack works as follows:

1. The attacker frontruns a transaction that would call `addLiquidity(...)` by opening the maximum possible short. In case of no or small outstanding longs (L0 < c < 0), the attacker can reduce `z` to a number close to 0 such that:
   ```
   APR = 1 - z * y / (t_norm_pos * z * y)
   ```
   blows up to a really big number since the denominator `z * y` would be a really small number, such that `apr = HyperdriveMath.calculateAPRFromReserves(...)` would not be less than or equal to `_maxApr` provided by the user in the next transaction. The attacker might also be able to trigger division by `z * y = 0` revert.
  
2. The user's transaction of calling `addLiquidity(...)` would be processed and reverted due to the above. Even if the user sets `_maxApr = type(uint256).max`, the attacker can take advantage of the division by 0 case or, if that is not possible, the following calculation of `lpShares` would underflow and revert due to the fact that `endingPresentValue < startingPresentValue`:
   ```
   lpShares = (endingPresentValue - startingPresentValue).mulDivDown(
       lpTotalSupply,
       startingPresentValue
   );
   ```

This line of attack is similar to the ones used in the below issues where the attacker tries to open a short with the maximum possible amount:
- Sandwich a call to `addLiquidity(...)` for profit
- Drain pool by sandwiching matured shorts

## Recommendation
More analysis needs to be performed to avoid issues like above, as having `z` really small is not desirable in many cases. A few things can be added to prevent the division by 0 attack. If the liquidity provider sets `_minApr = 0` and `_maxApr = type(uint256).max`, the calculation of `apr` and the bound checks below can be avoided:
```
uint256 apr = HyperdriveMath.calculateAPRFromReserves(
    _marketState.shareReserves,
    _marketState.bondReserves,
    _initialSharePrice,
    _positionDuration,
    _timeStretch
);
if (apr < _minApr || apr > _maxApr) revert Errors.InvalidApr();
```

## DELV
We've addressed the issue of the share reserves being able to be really small (or even zero), which mitigates the part of the issue that can't be fixed by having a wider slippage guard. Aside from that, the likelihood of add liquidity being griefed seems low considering that the attack would need to pay a large amount of fees every time a user attempts to add liquidity.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Hyperdrive June 2023 |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Christoph Michel, Deivitto, M4rio.eth |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf

### Keywords for Search

`vulnerability`

