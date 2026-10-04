---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7316
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - business_logic

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

Expired liens taken from public vaults need to be liquidated otherwise processing an epoch halts/reverts

### Overview


This bug report is about an issue with the PublicVault.sol code, which is part of the Astaria and Spearbit services. The issue is that if a lien expires and no one calls the liquidate function, then the s.epochData[s.currentEpoch].liensOpenForEpoch will remain true and the processEpoch() function will revert until someone calls liquidate. This is because a lien's end falling in the s.currentEpoch andtimeToEpochEnd() == 0 imply that the lien is expired. The severity of this bug is medium risk.

The recommendation for this bug is for Astaria to have a monitoring solution setup to make sure the liquidate endpoint gets called for expired liens without delay. Both Astaria and Spearbit have acknowledged this bug.

### Original Finding Content

## Medium Risk Report

**Severity:** Medium Risk  
**Context:** PublicVault.sol#L275-L277  

## Description
`s.epochData[s.currentEpoch].liensOpenForEpoch` is decremented or is supposed to be decremented when for a lien with an end that falls on this epoch:

- The full payment has been made,
- Or the lien is bought out by a lien that is from a different vault or ends at a higher epoch,
- Or the lien is liquidated.

If for some reason a lien expires and no one calls `liquidate`, then `s.epochData[s.currentEpoch].liensOpenForEpoch > 0` will be true, and `processEpoch()` would revert until someone calls `liquidate`.

Note that a lien's end falling in the `s.currentEpoch` and `timeToEpochEnd() == 0` imply that the lien is expired.

## Recommendation
Astaria would need to have a monitoring solution set up to make sure the `liquidate` endpoint gets called for expired liens without delay.

**Astaria:** Acknowledged.  
**Spearbit:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

