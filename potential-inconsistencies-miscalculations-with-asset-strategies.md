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
solodit_id: 35991
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf
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

Potential Inconsistencies & Miscalculations With Asset Strategies

### Overview

See description below for full details.

### Original Finding Content

## Description

The `updateAssetStrategy()` function in `LRTConfig` allows changing the strategy for an asset. In the current implementation, the EigenLayer team has indicated that there will only be one strategy for each supported asset. However, this could change in the future, either through implementing multiple strategies per asset, or having multi-asset strategies.

Any of these changes could be a breaking change for Kelp LRT.

## Multiple Strategies per Asset

In this scenario, if there are assets still in the old strategy when it is changed in Kelp LRT, assets in the old strategy will not be accounted for in calculations of `getAssetBalance()`. This will in turn lead to inaccurate rsETH price calculations.

## Multi Asset Strategies

In this scenario, there is potential for a single strategy to support multiple tokens used in Kelp LRT. If this is the case, care must be taken to ensure that this strategy is not used across multiple tokens in Kelp LRT. Otherwise, assets will be accounted for multiple times when looping through supported assets during rsETH price updates.

## Recommendations

- Monitor any breaking changes from EigenLayer both in terms of multiple strategies per asset or multi-asset strategies.
- Ensure that strategies are not modified without a proper migration process and never use the same strategy across multiple tokens, respectively.

## Resolution

The issue was acknowledged by the project team.

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

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf

### Keywords for Search

`vulnerability`

