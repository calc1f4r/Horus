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
solodit_id: 6702
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
rarity_score: 4

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

H-2: Precision differences when calculating userCollateralRatioMantissa causes major issues for some token pairs

### Overview


This bug report is about the precision differences when calculating userCollateralRatioMantissa which causes major issues for some token pairs. This was found by GimelSec, joestakey, peanuts, usmannk, bin2chen, ast3ros, 0x52, Bauer, TrungOre, gogo, ctf_sec, and __141345__.

When calculating userCollateralRatioMantissa, both debt value and collateral values are left in the native precision. This causes issues with specific token pairs, including being unable to liquidate a subset of positions no matter what. This is because of the precision differences between the loan token and the collateral token. For example, if a user has a collateral balance of 100,001 SHIB (100,001e18) and a loan borrow of 1 USDC (1e6), then their userCollateralRatioMantissa will actually calculate as zero.

The impact of this bug is that some token pairs will always be/will become broken. The code snippet which can be found at https://github.com/sherlock-audit/2023-02-surge/blob/main/surge-protocol-v1/src/Pool.sol#L455-L498 was used for this bug. The recommendation for this bug is that userCollateralRatioMantissa should be calculated using debt and collateral values normalized to 18 decimal points.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-surge-judging/issues/122 

## Found by 
GimelSec, joestakey, peanuts, usmannk, bin2chen, ast3ros, 0x52, Bauer, TrungOre, gogo, ctf\_sec, \_\_141345\_\_

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

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
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

