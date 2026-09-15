---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18301
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

A malicious collection admin can reclaim a pair at any time to deny enhanced setting royalties

### Overview


This bug report identified a vulnerability in the StandardSettings.sol contract, which allows a malicious collection admin to prematurely end a settings contract before the agreed upon lockup period. This would lead to the pair owner losing their upfront fee and any expected enhanced royalty payments. To address this issue, unlockTime should be enforced on collection admins authorized by authAllowedForToken. Sudorandom Labs has addressed this vulnerability in PR#85, which has been verified by Spearbit.

### Original Finding Content

## Security Report

## Severity
**Medium Risk**

## Context
`StandardSettings.sol#L164-L178`

## Description
A collection admin can forcibly/selectively call `reclaimPair()` prematurely (before the advertised and agreed upon lockup period) to unilaterally break the settings contract at any time. This will effectively lead to a Denial of Service (DoS) to the pair owner for the enhanced royalty terms of the setting despite paying the upfront fee and agreeing to a fee split in return. 

This issue arises because the `unlockTime` is enforced only on the previous pair owner and not on collection admins. A malicious collection admin can advertise very attractive setting royalty terms to entice pair owners to pay a high upfront fee to sign up for their settings contract but then force-end the contract prematurely. This situation will lead to the pair owner losing the paid upfront fee and the promised attractive royalty terms. 

A lax pair owner who may not be actively monitoring `SettingsRemovedForPair` events before the lockup period will be surprised at the prematurely forced settings contract termination by the collection admin, resulting in the loss of their earlier paid upfront fee and any payments of default royalty instead of their expected enhanced amounts.

## Recommendation
Enforce `unlockTime` on collection admins authorized by `authAllowedForToken`.

## Reports
- **Sudorandom Labs:** Addressed in PR#85.
- **Spearbit:** Verified that this is fixed by PR#85.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

