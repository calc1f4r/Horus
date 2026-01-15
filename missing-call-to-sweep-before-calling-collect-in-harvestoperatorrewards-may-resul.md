---
# Core Classification
protocol: Infrared Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49851
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
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
finders_count: 4
finders:
  - 0xRajeev
  - Chinmay Farkya
  - Cryptara
  - Noah Marconi
---

## Vulnerability Title

Missing call to sweep() before calling collect() in harvestOperatorRewards() may result in inaccu-

### Overview


This bug report discusses a potential issue with the rewards system in a specific part of the code. The problem occurs when the function "harvestOperatorRewards()" is called, as it may use outdated data to calculate fees, leading to incorrect rewards allocation. This can have a medium impact on the system, as it can cause mismanagement of fees and affect the trust in the reward system. The likelihood of this issue occurring is also medium, as the function is regularly used. The recommended solution is to add a call to "sweep()" before "collect()" in the code, which has already been fixed in a recent update. 

### Original Finding Content

## Rate Rewards

**Severity:** Medium Risk  
**Context:** RewardsLib.sol#L307-L313  
**Summary:** Missing sweep before calling collect in `harvestOperatorRewards()` may result in inaccurate rewards due to stale data being used.  

## Finding Description
In `harvestOperatorRewards()`, there is a potential issue with stale data being used when calculating fees via `collect()`. Specifically, `InfraredBERA.collect()` relies on the `shareholderFees` value, which may not be up-to-date unless a `sweep()` is performed beforehand. While `mint()` triggers a sweep, `collect()` does not. This discrepancy means that when `harvestOperatorRewards()` is called, it may process rewards using an outdated `shareholderFees` value, potentially leading to incorrect fee calculations and distribution.  

## Impact Explanation
**Medium**, because this can result in inaccurate rewards allocation due to outdated fee data, causing mismanagement of protocol fees and discrepancies in the operator rewards distribution, which could negatively affect the trust and reliability of the reward system.  

## Likelihood Explanation
**Medium**, because `harvestOperatorRewards()` is expected to be invoked regularly in the protocol to manage operator rewards. If a `sweep()` is not explicitly called prior to `collect()`, there is a consistent risk of stale data usage.  

## Recommendation
To ensure accurate fee calculations, `harvestOperatorRewards()` should explicitly trigger a `sweep()` operation in `InfraredBERA` before calling `collect()`. This will ensure that `shareholderFees` is always updated to the latest value before rewards are processed. This adjustment will align the behavior of `harvestOperatorRewards` with the safeguards provided by `mint`, reducing the risk of incorrect fee allocation.  

**Infrared:** Fixed in PR 326.  
**Spearbit:** Reviewed that PR 326 fixes the issue as recommended by adding a call to `compound()` (which calls `sweep()`) in `harvestOperatorRewards()` before calling `collect()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Infrared Contracts |
| Report Date | N/A |
| Finders | 0xRajeev, Chinmay Farkya, Cryptara, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf

### Keywords for Search

`vulnerability`

