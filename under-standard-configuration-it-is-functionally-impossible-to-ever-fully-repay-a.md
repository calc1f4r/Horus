---
# Core Classification
protocol: Aave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19215
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
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

Under standard configuration, it is functionally impossible to ever fully repay all GHO debts

### Overview

See description below for full details.

### Original Finding Content

## Description

Because interest is charged on GHO debt without any new GHO entering the system, there is a constantly expanding gap between the total supply of GHO and the sum of all GHO debts as denoted by `GhoVariableDebtToken`. In essence, after any amount of time from the `firstGHO debt`:

```
GHO.totalSupply < GhoVariableDebtToken.totalSupply
```

However, the difference between these two totals is equal to the amount of GHO that would be in the treasury if all the debts were repaid as much as possible with the existing GHO supply. In terms of the mathematics, if the treasury instantly recirculated these GHO tokens, the debts could be repaid.

In terms of practice on the blockchain, this does not seem to be possible, however. Attempts in tests to repay fully were all forced to wait at least one block by the AAVE pool error:

```
SAME_BLOCK_BORROW_REPAY ='48'; // 'Borrow and repay in same block is not allowed'
```

This means that interest is always accrued before debts can be repaid in full, even with a maximally cooperative treasury. This issue is further accentuated by GHO-07.

The practical impact of this issue is uncertain, and likely minimal. It is presumably unlikely that users will wish to all repay all GHO debts simultaneously, although it might harm the protocol if it is known that this is not possible. It may be that GHO may struggle with liquidity at times when many users wish to liberate their collateral. The behaviour of the treasury might also have an effect on these issues: if it trades away its GHO regularly, that will help to keep GHO supply up.

Also, if the system remains finely balanced in this way, any lost tokens would render debts theoretically unpayable simply because of limited GHO liquidity.

It might be theoretically possible to repay all GHO debts using accounts that pay no interest because of 100% discounts if those accounts paid off their debts last and the treasury cooperates by recirculating interest payments. However, 100% discounts may not be offered.

## Recommendations

Be aware of this issue and, if the development team feels it is necessary, consider potential strategies to ensure that no user would ever be technically locked from repaying their GHO debt due to lack of supply.

## Resolution

The development team have acknowledged the issue and decided to make no code changes at this time.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Aave |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf

### Keywords for Search

`vulnerability`

