---
# Core Classification
protocol: Surge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18611
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/51
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-surge-judging/issues/122

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 12
finders:
  - TrungOre
  - Bauer
  - 0x52
  - gogo
  - bin2chen
---

## Vulnerability Title

H-1: Precision differences when calculating userCollateralRatioMantissa causes major issues for some token pairs

### Overview


This bug report is about the precision differences when calculating userCollateralRatioMantissa, which can cause major issues for some token pairs. When calculating userCollateralRatioMantissa, both debt value and collateral values are left in the native precision. This can cause certain token pairs to be completely broken, and other pairs to be partially broken, making it impossible to liquidate positions. This issue is particularly present with tokens that have very high or very low precision. A fix was proposed to normalize debt and collateral values to 18 decimal points. This fix was then double checked and implemented, resolving the issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-surge-judging/issues/122 

## Found by 
0x52, Bauer, GimelSec, TrungOre, \_\_141345\_\_, ast3ros, bin2chen, ctf\_sec, gogo, joestakey, peanuts, usmannk
## Summary

When calculating userCollateralRatioMantissa in borrow and liquidate. It divides the raw debt value (in loan token precision) by the raw collateral balance (in collateral precision). This skew is fine for a majority of tokens but will cause issues with specific token pairs, including being unable to liquidate a subset of positions no matter what.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-02-surge/blob/main/surge-protocol-v1/src/Pool.sol#L474

When calculating userCollateralRatioMantissa, both debt value and collateral values are left in the native precision. As a result of this certain token pairs will be completely broken because of this. Other pairs will only be partially broken and can enter state in which it's impossible to liquidate positions.

Imagine a token pair like USDC and SHIB. USDC has a token precision of 6 and SHIB has 18. If the user has a collateral balance of 100,001 SHIB (100,001e18) and a loan borrow of 1 USDC (1e6) then their userCollateralRatioMantissa will actually calculate as zero:

    1e6 * 1e18 / 100,001e18 = 0

There are two issues with this. First is that a majority of these tokens simply won't work. The other issue is that because userCollateralRatioMantissa returns 0 there are states in which some debt is impossible to liquidate breaking a key invariant of the protocol.

Any token with very high or very low precision will suffer from this.

## Impact

Some token pairs will always be/will become broken

## Code Snippet

https://github.com/sherlock-audit/2023-02-surge/blob/main/surge-protocol-v1/src/Pool.sol#L455-L498

## Tool used

[Solidity YouTube Tutorial](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

## Recommendation

userCollateralRatioMantissa should be calculated using debt and collateral values normalized to 18 decimal points



## Discussion

**xeious**

Fixed https://github.com/Surge-fi/surge-protocol-v1/commit/294aa4756fa32c66669e40902ec5c15aa05726e9

We need double checking on this.

**IAm0x52**

Fix looks good. All occurrences of this precision issue have been addressed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Surge |
| Report Date | N/A |
| Finders | TrungOre, Bauer, 0x52, gogo, bin2chen, joestakey, usmannk, \_\_141345\_\_, peanuts, GimelSec, ast3ros, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-surge-judging/issues/122
- **Contest**: https://app.sherlock.xyz/audits/contests/51

### Keywords for Search

`vulnerability`

