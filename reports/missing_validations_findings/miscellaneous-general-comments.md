---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36027
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-2/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-2/review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Miscellaneous General Comments

### Overview

See description below for full details.

### Original Finding Content

## Description

This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Use of Magic Numbers**  
   Constants should be defined rather than using magic numbers. The number `50400` is used for `MAX_WITHDRAWAL_DELAY_BLOCKS`.
   - StrategyManagerStorage line [46]
   - DelayedWithdrawRouter line [24]  
   `7 days / 12 seconds` should be used instead.

2. **Lack of Zero-Address Check**  
   The recipient address in `DelayedWithdrawRouter.createDelayedWithdrawal()` is missing a zero-address check.

3. **Redundant Code**  
   The `if` statement, in `EigenPod.sol` on line [218], is redundant:  
   `if (!hasRestaked)`

4. **Project Files with Outdated Naming Conventions**  
   The `package.json` file in the project root directory still references `eigenlayr-contracts` instead of the new branding of `eigenlayer-contracts`.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

The development team has acknowledged these findings, addressing them where appropriate as follows:

1. **Use of Magic Numbers**: The development team has acknowledged this feedback and decided to maintain the current format of the `MAX_WITHDRAWAL_DELAY_BLOCKS` constant.

2. **Lack of Zero-Address Check**: A zero-address check has been added to the `DelayedWithdrawRouter.createDelayedWithdrawal` function in the following commit `762f732d`.

3. **Redundant Code**: The development team has acknowledged this feedback; however, they stated, "the intention of the code is clearer the way it is, even if a bit extraneous".

4. **Project Files with Outdated Naming Conventions**: This issue was resolved in the following commit `da0262af`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-2/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-2/review.pdf

### Keywords for Search

`vulnerability`

