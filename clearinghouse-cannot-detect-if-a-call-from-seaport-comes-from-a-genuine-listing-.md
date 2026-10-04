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
solodit_id: 7299
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

ClearingHouse cannot detect if a call from Seaport comes from a genuine listing or auction

### Overview


This bug report is about a vulnerability in the ClearingHouse.sol code. It allows anyone to create a SeaPort order with one of the considerations' recipients set to a ClearingHouse with a collateralId that is already set for auction. When the spoofed order settles, SeaPort calls into the fallback function and causes the genuine Astaria auction to settle. This creates a number of issues, such as the Astaria auction payee and the liquidator not receiving what they should, lien data and lien token being deleted or burnt, collateral token and data being burnt or deleted, and when the genuine auction settles, it will revert due to a s.collateralIdToAuction[collateralId] check.

Astaria has proposed a solution that involves adding a mechanism so that Seaport can send more data to ClearingHouse to check the genuineness of the fallback calls. Spearbit has acknowledged this solution.

### Original Finding Content

## Vulnerability Report

## Severity
**High Risk**

## Context
*ClearingHouse.sol#L21*

## Description
Anyone can create a SeaPort order with one of the considerations' recipients set to a ClearingHouse with a `collateralId` that is genuinely already set for auction. Once the spoofed order settles, SeaPort calls into this fallback function and causes the genuine Astaria auction to settle.

This allows an attacker to set random items on sale on SeaPort with funds directed here (small buying prices) to settle genuine Astaria auctions on the protocol.

### This causes:
- The Astaria auction payees and the liquidator would not receive what they would expect that should come from the auction. If the payee is a public vault, it would introduce incorrect parameters into its system.
- Lien data (`s.lienMeta[lid]`) and the lien token get deleted/burnt.
- Collateral token and data get burnt/deleted.
- When the actual genuine auction settles and calls back to here, it will revert due to `s.collateralIdToAuction[collateralId]` check.

## Recommendation
Astaria needs to introduce a mechanism so that SeaPort would send more data to ClearingHouse to check the genuineness of the fallback calls.

## Astaria
In a change yet to be merged, we have the ClearingHouse set up with checks to enforce that it has received enough of a payment in the right asset to complete the transaction. We ultimately do not care where the transaction came from as long as we are indeed offering the payment and are getting everything that the auction should cost. We will mark it as acknowledged and tag this ticket with the updates when merged.

## Spearbit
Acknowledged.

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

`Validation`

