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
solodit_id: 3663
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/167

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

H-25: Triggering liquidations ahead of expected time leads to loss and lock of funds

### Overview


This bug report is about an issue found by 0xRajeev where triggering liquidations for a collateral after one of its liens has expired but before the auction window (default 2 days) at epoch end leads to loss and lock of funds. The liquidation logic does not execute the decrease of lien count and setting up of liquidation accountant if the time to epoch end is greater than the auction window (default 2 days). This will, at a minimum, lead to auction proceeds going to lien owners directly instead of via the liquidation accountants (loss of funds) and the epoch unable to proceed to the next on (lock of funds and protocol halt). The bug was found by manual review and the code snippet provided is from AstariaRouter.sol. The recommendation is to revisit the liquidation logic and its triggering related to the auction window and epoch end.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/167 

## Found by 
0xRajeev

## Summary

Triggering liquidations for a collateral after one of its liens has expired but before the auction window (default 2 days) at epoch end leads to loss and lock of funds.

## Vulnerability Detail

Liquidations are allowed to be triggered for a collateral if any of its liens have exceeded their loan duration with outstanding payments. However, the liquidation logic does not execute the decrease of lien count and setting up of liquidation accountant if the time to epoch end is greater than the auction window (default 2 days). The auction proceeds nevertheless.

## Impact

If liquidations are triggered before the auction window at epoch end, they will proceed to auctions without decreasing epoch lien count, without setting up the liquidation accountant for the lien and other related logic. This will, at a minimum, lead to auction proceeds going to lien owners directly instead of via the liquidation accountants (loss of funds) and the epoch unable to proceed to the next on (lock of funds and protocol halt).

## Code Snippet

1.https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L388-L415

## Tool used

Manual Review

## Recommendation

Revisit the liquidation logic and its triggering related to the auction window and epoch end.

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
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/167
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

