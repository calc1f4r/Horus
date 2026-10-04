---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3660
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/173

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xRajeev
---

## Vulnerability Title

H-22: Public vault depositors will receive fewer vault shares until the first payment

### Overview


This bug report is about the incorrect calculation of the total asset of a public vault, leading to depositors receiving fewer vault shares than expected. This issue was found by 0xRajeev and the impact of this vulnerability is that public vault depositors will receive fewer vault shares until the first payment. This vulnerability was identified through manual review, and the code snippet responsible for this issue can be found at https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/PublicVault.sol#L407. The recommendation to fix this issue is to revisit the logic behind updating the "last" value when "yIntercept" and/or "slope" are updated.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/173 

## Found by 
0xRajeev

## Summary

Public vault total asset calculation is incorrect until the first payment, leading to depositors receiving fewer vault shares than expected.

## Vulnerability Detail

As long as `PublicVault.last` is set to 0, the `PublicVault.totalAssets` function returns the actual ERC-20 token balance (WETH) of the public vault. Due to borrowing, this balance is reduced by the borrowed amount. Therefore, as there is no payment, this leads to depositors receiving fewer vault shares than expected.

## Impact

PoC: https://gist.github.com/berndartmueller/8a71ff76c7eb8207e1f01a154a873b2c

Public vault depositors will receive fewer vault shares until the first payment.
 
## Code Snippet

1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/PublicVault.sol#L407

## Tool used

Manual Review

## Recommendation

Revisit the logic behind updating `last` when `yIntercept` and/or `slope` are updated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | 0xRajeev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/173
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

