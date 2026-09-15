---
# Core Classification
protocol: Kelp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53607
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
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

High Churn Rate Due To Arbitrage

### Overview

See description below for full details.

### Original Finding Content

## Description

The redemption rates are used to price assets. This has shown to not always equal the market price as LSTs can trade both above and below their redemption rate for extended periods of time. This means that the rsETH protocol can be used for arbitrages: a below peg asset can be deposited at peg rate and can be withdrawn for any other asset in order to turn a profit. Such market conditions would cause a lot of churn; assets would constantly be deposited and withdrawn. In turn, this may lower capital efficiency since assets would have to be deposited and withdrawn from EigenLayer instead of earning rewards.

## Recommendations

One way to mitigate this partially is by charging a fee to deposit and withdraw. This would discourage small arbitrages by making them unprofitable. As depositing and withdrawing is currently free, even small and temporary depegs may trigger arbitrages. 

Another mitigation would be to use the currently implemented deposit limits. If an asset were to have a larger depeg event, its deposit limits could be lowered to limit the arbitrage possibilities. This would also defend the value of rsETH and ensure it does not drop too much with the depegged asset.

## Resolution

The development team has opted for the above issue with the following statement: 

"We have a minimum withdrawal delay of 7 days, which should discourage this. On top of that we are going to charge a fee soon."

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Kelp |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf

### Keywords for Search

`vulnerability`

