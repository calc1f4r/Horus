---
# Core Classification
protocol: Peapods_2024-11-16
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46005
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
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

[M-11] Observe might fail for newly created pools

### Overview


This bug report discusses an issue with the price of a quote token. The price is fetched from a specific contract, but the report suggests that this method may not always work as intended. Specifically, it mentions that if the contract does not have enough data, the price may not be accurate. The report recommends implementing a different approach to handle this issue.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

The price of the quote token is fetched from the UniswapV3SinglePriceOracle.sol as follows -->

```solidity
function _getSqrtPriceX96FromPool(IUniswapV3Pool _pool, uint32 _interval)
       public
       view
       returns (uint160 _sqrtPriceX96)
   {
       if (_interval == 0) {
           (_sqrtPriceX96,,,,,,) = _pool.slot0();
       } else {
           uint32[] memory secondsAgo = new uint32[](2);
           secondsAgo[0] = _interval;
           secondsAgo[1] = 0; // to (now)
           (int56[] memory tickCumulatives,) = _pool.observe(secondsAgo);
           int56 tickCumulativesDelta = tickCumulatives[1] - tickCumulatives[0];
           int24 arithmeticMeanTick = int24(tickCumulativesDelta / int32(_interval));
           // Always round to negative infinity
           if (tickCumulativesDelta < 0 && (tickCumulativesDelta % int32(_interval) != 0)) arithmeticMeanTick--;
           _sqrtPriceX96 = TickMath.getSqrtRatioAtTick(arithmeticMeanTick);
       }
   }
```

... where the pool is the v3 pool where we get the TWAP to price the underlying TKN of the pod represented through SP_TKN and then convert it to the spTKN price, and we call the `observe` function on the pool to get the tick cumulative. But it is possible that the v3 pool does not have sufficient observations yet and in that case, the observation call would fail. A proper approach to handle this can be seen implemented [here](https://github.com/NFTX-project/nftx-protocol-v3/blob/master/src/NFTXVaultFactoryUpgradeableV3.sol#L454)

## Recommendation

Pools having insufficient observations should be handled as explained above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Peapods_2024-11-16 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

