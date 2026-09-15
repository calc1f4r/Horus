---
# Core Classification
protocol: stETH by EaseDeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64089
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1203
source_link: none
github_link: https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi-judging/issues/708

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
finders_count: 42
finders:
  - Sa1ntRobi
  - ni8mare
  - destiny\_rs
  - HeckerTrieuTien
  - X0sauce
---

## Vulnerability Title

M-6: Wrong price validation in oracle causes early DoS and allows late-stage price manipulation

### Overview


This bug report discusses an issue found in the Morpho market implementation of the stNXM protocol. The issue was discovered by multiple individuals and was caused by the reliance on the `elapsedTime` variable in the `sanePrice` function, which validates the price of stNXM in wNXM terms. This validation formula magnifies small normal shifts in the price in the early stages of the protocol, causing reverts and disrupting the market. The impact of this bug is that it can easily disturb the Morpho market usage in the initial stages and allow abnormal prices to pass in later stages. The protocol team has fixed this issue in a recent commit. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi-judging/issues/708 

## Found by 
0x73696d616f, 0xAsen, 0xMosh, 0xSecurious, 0xc0ffEE, 0xeix, 0xgh0stcybers3c, ChargingFoxSec, HeckerTrieuTien, JuggerNaut, ReidnerM, Sa1ntRobi, Sir\_Shades, Solea, SuperDevFavour, TianZun, Vesko210, Wojack, X0sauce, ZeronautX, aster, befree3x, boredpukar, destiny\_rs, djshaneden, ethaga, h2134, iamephraim, joicygiore, khaye26, kimnoic, maxim371, merlin, ni8mare, pecata17107, securewei, shieldrey, slavina, th3hybrid, touristS, typicalHuman, werulez99

### Summary

Sanity check's reliance on `elapsedTime` will reject normal price shift in early stages of the protocol and allow price manipulation later on



### Root Cause

In oracle contract implementation dedicated for Morpho market, `sanePrice` [function](https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi/blob/main/stNXM-Contracts/contracts/core/stNxmOracle.sol#L45-L53) validates price of `stNXM` in `wNXM` terms in the following way:
```solidity
function sanePrice(uint256 _price) public view returns (bool) {
        // Amount of 1 year it's been
@>      uint256 elapsedTime = block.timestamp - startTime;
        // If price is lower than equal it's not too high.
        if (_price < 1e18) return true;

@>      uint256 apy = (_price - 1e18) * 31_536_000 / elapsedTime;
        return apy <= saneApy;
    }
```
Such APY formula will magnify small normal shifts in TWAP price in early stages of the protocol, when `elapsedTime` is small. Consider the following situation:

1. `elapsedTime` is equal to 7 days
2. For this period of time, price was higher at around 1% deviation mark - `1.01e18`, which is normal price shifts and is definitely not price manipulation
3.  The resulting APY at 7 day mark (highest denominator) - around `5.2e17`, which will cause a revert on [this line](https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi/blob/main/stNXM-Contracts/contracts/core/stNxmOracle.sol#L36). Quoting an oracle with such price deviation on DEX would revert as well, since denominator is smaller

For big `elapsedTime` values, big price deviations will be rendered as valid:

1. `elapsedTime` is equal to 3 years
2.  Price at the moment of quoting is `2.5e18` - `1.5e18` more than target `1e18` price
3. Resulting APY is at borderline - `5e17`, which allows such price to pass

First scenario will break the Morpho market usage, since any operation that would trigger `_isHealthy` check would revert due to price being rejected in oracle

### Internal Pre-conditions

None

### External Pre-conditions

None

### Attack Path

There is no real attack path, since normal operations will cause Morpho disturbance

### Impact

For intial stages, when `elapsedTime` is small - Morpho usage is easily disturbed by normal price movements
For later stages, when `elapsedTime ` is big - abnormal prices that may happen during low liquidity periods can pass

### PoC

_No response_

### Mitigation

_No response_

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/EaseDeFi/stNXM-Contracts/commit/7a9abd4e78bfb29416e9677040aa3650999ee353






### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | stETH by EaseDeFi |
| Report Date | N/A |
| Finders | Sa1ntRobi, ni8mare, destiny\_rs, HeckerTrieuTien, X0sauce, th3hybrid, ReidnerM, securewei, 0xeix, 0xAsen, djshaneden, pecata17107, TianZun, shieldrey, Vesko210, Solea, ChargingFoxSec, SuperDevFavour, ethaga, befree3x, ZeronautX, iamephraim, typicalHuman, JuggerNaut, 0xMosh, slavina, boredpukar, 0x73696d616f, Wojack, h2134, 0xSecurious, touristS, kimnoic, khaye26, joicygiore, Sir\_Shades, werulez99, 0xc0ffEE, aster, 0xgh0stcybers3c, merlin, maxim371 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi-judging/issues/708
- **Contest**: https://app.sherlock.xyz/audits/contests/1203

### Keywords for Search

`vulnerability`

