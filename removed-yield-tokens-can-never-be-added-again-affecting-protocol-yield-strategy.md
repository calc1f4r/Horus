---
# Core Classification
protocol: Neutrl Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61813
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Neutrl-Spearbit-Security-Review-July-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Neutrl-Spearbit-Security-Review-July-2025.pdf
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
finders_count: 3
finders:
  - 0xRajeev
  - Chinmay Farkya
  - Kurt Barry
---

## Vulnerability Title

Removed yield tokens can never be added again affecting protocol yield strategy

### Overview

See description below for full details.

### Original Finding Content

## Low Risk Vulnerability Report

## Severity
Low Risk

## Context
`YieldDistributor.sol#L71-L89`

## Summary
Removed yield tokens from YieldDistributor can never be added again, which negatively affects protocol yield strategy and distribution thereafter.

## Finding Description
YieldDistributor manages and distributes yield from accepted stablecoins (USDC, USDT, and USDe) to sNUSD holders. While the yield generation happens offchain, the generated yield in USDC, USDT, and USDe is converted to NUSD via `convertYieldToNUSD()` and then distributed to sNUSD holders via `distributeYield()`.

The protocol manages the accepted yield tokens via `addYieldToken()` and `removeYieldToken()`. `addYieldToken()` prevents the addition of duplicated yield tokens by checking if the one being added already exists in the `yieldTokens` array. `removeYieldToken()` removes a yield token not by removing it from the array but only marking it as inactive via `yieldTokens[i].isActive = false`.

Given this differing logic during addition and removal, once a yield token is removed by marking it as inactive, it can never be added back again because `addYieldToken()` only checks for its presence and not for `isActive == true`.

## Impact Explanation
Low, because not being able to add a yield token back will negatively impact protocol yield strategy and distribution thereafter.

## Likelihood Explanation
Low, assuming it is unlikely for the admin to remove a yield token and then want to add it back later for some reason.

## Recommendation
Consider checking for `yieldTokens[i].isActive == true` along with `yieldTokens[i].token == _yieldToken` in `addYieldToken()` logic, so that:
1. If a token is present but `isActive == false`, then it can be set to true.
2. If a token is present and `isActive == true`, then it can revert.
3. If a token is absent, then it can be added.

## Neutrl
Fixed in PR 22.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Neutrl Contracts |
| Report Date | N/A |
| Finders | 0xRajeev, Chinmay Farkya, Kurt Barry |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Neutrl-Spearbit-Security-Review-July-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Neutrl-Spearbit-Security-Review-July-2025.pdf

### Keywords for Search

`vulnerability`

