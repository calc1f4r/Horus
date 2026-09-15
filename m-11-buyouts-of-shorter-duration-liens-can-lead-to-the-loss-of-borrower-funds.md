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
solodit_id: 3686
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/171

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

M-11: Buyouts of shorter duration liens can lead to the loss of borrower funds

### Overview


This bug report is about an issue found in the AstariaRouter contract of the Sherlock-Audit project. The issue is that liens whose duration is equal to (or less than) the `minDurationIncrease` cannot be bought out to be replaced by newer liens with lower interest rates but the same duration. This results in an underflow in `_getRemainingInterest()` and locks the borrower out of better-termed liens, effectively resulting in the loss of their funds because of extra interest paid on older liens. This was found manually by 0xRajeev and the code snippets that are affected are located at https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L573 and https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L489-L490. The recommendation is to revisit the checking logic and minimum duration as it applies to shorter-duration loans. SantiagoGregory suggested to update the buyoutLien() function to check for a lower interest rate or higher duration.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/171 

## Found by 
0xRajeev

## Summary

Liens whose duration is equal to (or maybe less than) `minDurationIncrease` cannot be bought out to be replaced by newer liens with lower interest rates but the same duration. This locks the borrower out of better-termed liens, effectively resulting in the loss of their funds 
 
## Vulnerability Detail

Liens whose duration is equal to (or maybe less than) `minDurationIncrease` cannot be bought out to be replaced by newer liens with lower interest rates but the exact duration because it results in an underflow in `_getRemainingInterest()`.

Example scenario: if the strategy`liendetails.duration` is <= 14 days, then it's impossible to do a buyout of a new lien because the implemented check requires to wait `minDurationIncrease`, which is set to 14 days. However, if the buyer waits 14 days, the lien is expired, which triggers the earlier mentioned underflow.

## Impact

The borrower gets locked out of better-termed liens, effectively resulting in the loss of their funds because of extra interest paid on older liens.
 
## Code Snippet

1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L573
2. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L489-L490

## Tool used

Manual Review

## Recommendation

Revisit the checking logic and minimum duration as it applies to shorter-duration loans.

## Discussion

**SantiagoGregory**

We updated buyoutLien() to check for a lower interest rate *or* higher duration.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | 0xRajeev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/171
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

