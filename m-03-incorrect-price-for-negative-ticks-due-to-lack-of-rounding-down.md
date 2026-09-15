---
# Core Classification
protocol: Predy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34889
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-predy
source_link: https://code4rena.com/reports/2024-05-predy
github_link: https://github.com/code-423n4/2024-05-predy-findings/issues/115

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

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 19
finders:
  - josephdara
  - SBSecurity
  - grearlake
  - Kaysoft
  - ZanyBonzy
---

## Vulnerability Title

[M-03] Incorrect price for negative ticks due to lack of rounding down

### Overview


The bug report discusses an issue with the function `callUniswapObserve` used to get twap price tick. The problem occurs when the difference between two tickCumulatives values is negative, causing the tick to be rounded up instead of down. This results in incorrect prices being used. The report provides a proof of concept and recommends rounding down the int24 tick to mitigate the issue. The bug has been confirmed by the Warden and its peers and has been given a medium risk rating.

### Original Finding Content


The function `callUniswapObserve` is used to get twap price tick using `IUniswapV3PoolOracle.observe.selector` which is then used to calculate the `int24 tick`.

The problem is that in case if `(tickCumulatives[1] - tickCumulatives[0])` is negative, the tick should be rounded down as it's done in the `OracleLibrary` from uniswap.

As result, in case if `(tickCumulatives[1] - tickCumulatives[0])`is negative and `(tickCumulatives[1] - tickCumulatives[0]) % secondsAgo != 0`, then returned tick will be bigger then it should be, hence incorrect prices would be used.

### Proof of Concept

`Unihelper:::callUniswapObserve()`:

```solidity
        int56[] memory tickCumulatives = abi.decode(data, (int56[]));

        int24 tick = int24((tickCumulatives[1] - tickCumulatives[0]) / int56(int256(ago)));

        uint160 sqrtPriceX96 = TickMath.getSqrtRatioAtTick(tick);
```

In Uniswap's `OracleLibrary:::consult()`:

```solidity
        int56 tickCumulativesDelta = tickCumulatives[1] - tickCumulatives[0];
        uint160 secondsPerLiquidityCumulativesDelta =
            secondsPerLiquidityCumulativeX128s[1] - secondsPerLiquidityCumulativeX128s[0];

        arithmeticMeanTick = int24(tickCumulativesDelta / secondsAgo);
        // Always round to negative infinity
        if (tickCumulativesDelta < 0 && (tickCumulativesDelta % secondsAgo != 0)) arithmeticMeanTick--;
```

### Tools Used

Solodit

### Recommended Mitigation Steps

Round down the `int24 tick`:

```solidity
if (tickCumulativesDelta < 0 && (tickCumulativesDelta % secondsAgo != 0)) tick--;
```

### Assessed type

Math

**[syuhei176 (Predy) confirmed via duplicate Issue #65](https://github.com/code-423n4/2024-05-predy-findings/issues/65#event-13208488411)**

**[0xsomeone (judge) commented](https://github.com/code-423n4/2024-05-predy-findings/issues/115#issuecomment-2197280490):**
 > The Warden and its peers have demonstrated that the DEX price feed calculation does not round properly, resulting in a deviation of as much as one tick which, depending on the spacing of the pool, can be significant.
> 
> As such, I believe a medium risk rating is appropriate for this submission.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Predy |
| Report Date | N/A |
| Finders | josephdara, SBSecurity, grearlake, Kaysoft, ZanyBonzy, ayden, 0xabhay, kodyvim, 0xhere2learn, jolah1, Naresh, Sparrow, WinSec, Bauchibred, 0xhashiman, 1, 2, Giorgio, Tigerfrake |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-predy
- **GitHub**: https://github.com/code-423n4/2024-05-predy-findings/issues/115
- **Contest**: https://code4rena.com/reports/2024-05-predy

### Keywords for Search

`vulnerability`

