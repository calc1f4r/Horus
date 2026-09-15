---
# Core Classification
protocol: Mellow
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40586
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/72dfcce6-8b1b-4f5d-b5a7-657a40507b10
source_link: https://cdn.cantina.xyz/reports/cantina_mellow_apr2024.pdf
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
  - Kaden
  - Saw-mon and Natalie
  - deadrosesxyz
  - Akshay Srivastav
---

## Vulnerability Title

Lack of consideration of time in ensureNoMEV leads to unexpected reverts 

### Overview


The VeloOracle.sol code has a function called ensureNoMEV that checks the price of a pool by looking at recent observations. However, if there haven't been any recent changes to the pool, the function may revert even though the price hasn't actually changed. This can cause issues with rebalancing and lead to lost liquidity fees. The recommendation is to modify the function to consider the time between observations instead of just the number of observations. This bug has been fixed in a recent commit.

### Original Finding Content

## VeloOracle Analysis

## Context
`VeloOracle.sol#L11-L53`

## Description
`VeloOracle.ensureNoMEV` works by looking back at a given amount of observations and reverting if the tick delta between observations exceeds a `maxAllowedDelta`. The observations are retrieved from the given `CLPool` where they are written any time an in-range liquidity position is modified, or a swap occurs, updating the most recent observation if it was within 15 seconds. This logic is used to ensure that the price of the pool has not recently changed beyond a certain amount.

The problem with `ensureNoMEV`'s logic here is that it implicitly assumes that the observations that are being considered are recent. However, if there have not been any swaps or in-range liquidity modifications recently, then there will not be recent observations. Instead, we may be looking further back in time than intended.

Consider, for example, a circumstance where there's a large swap that exceeds the `maxAllowedDelta`, followed by no activity for a while. Even though the price has not recently changed, the function will revert since it's looking at the most recent observations, regardless of when they actually occurred.

The result of this is that rebalances can be DoS'd until sufficient observations are written such that `ensureNoMEV` no longer reverts. This can lead to extended periods of time in which the position is out of range and thus not earning liquidity fees.

## Recommendation
Consider modifying the `ensureNoMEV` logic to take into account the time between observations instead of just a lookback amount of observations. For example, if there are no observations exceeding the `maxAllowedDelta` in `x` seconds, return.

## Mellow
Fixed in commit `f839c6c8`.

## Cantina Managed
The issue has been fixed by incorporating a `maxAge` to determine whether observations should be evaluated. The fix persists and is present in `736eef90ecfa896b12b5f193e68bf95030eb475e`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Mellow |
| Report Date | N/A |
| Finders | Kaden, Saw-mon and Natalie, deadrosesxyz, Akshay Srivastav |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_mellow_apr2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/72dfcce6-8b1b-4f5d-b5a7-657a40507b10

### Keywords for Search

`vulnerability`

