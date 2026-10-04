---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7289
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation
  - auction

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

settleAuction() doesn't check if the auction was successful

### Overview


This bug report is about the function settleAuction() in CollateralToken.sol#L600. This function is a privileged functionality called by LienToken.payDebtViaClearingHouse(), and is intended to be called on a successful auction. However, it does not verify whether the auction was successful or not, which can be exploited by creating a fake Seaport order with one of its considerations set as the CollateralToken. Another potential issue is if the Seaport orders can be "Restricted" in future, then an authorized entity can force settleAuction on CollateralToken, and when SeaPort tries to call back on the zone to validate it would fail. 

To fix this issue, the following validations can be performed: CollateralToken doesn't own the underlying NFT, and collateralIdToAuction[collateralId] is active. This way, settleAuction() can only be called on the success of the Seaport auction created by Astaria protocol.

### Original Finding Content

## Security Risk Report

## Severity
**High Risk**

## Context
`CollateralToken.sol#L600`

## Description
The `settleAuction()` function is a privileged functionality called by `LienToken.payDebtViaClearingHouse()`. It is intended to be called on a successful auction, but it lacks verification to ensure this is the case. 

Anyone can create a fake Seaport order with one of its considerations set as the `CollateralToken`, as described in Issue 93. Another potential issue arises if the Seaport orders can be "Restricted" in the future. In that scenario, an authorized entity could force the execution of `settleAuction()` on `CollateralToken`, and when Seaport tries to call back on the zone to validate, it would likely fail.

## Recommendation
The following validations can be performed:

- `CollateralToken` doesn't own the underlying NFT.
- `collateralIdToAuction[collateralId]` is active.

By implementing these checks, `settleAuction()` can only be called upon the successful completion of the Seaport auction created by the Astaria protocol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

`Validation, Auction`

