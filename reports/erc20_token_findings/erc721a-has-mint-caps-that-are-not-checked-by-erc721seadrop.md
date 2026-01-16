---
# Core Classification
protocol: SeaDrop
chain: everychain
category: logic
vulnerability_type: min/max_cap_validation

# Attack Vector Details
attack_type: min/max_cap_validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6842
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Seadrop-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Seadrop-Spearbit-Security-Review.pdf
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
  - min/max_cap_validation
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Sawmon and Natalie
  - Dravee
  - Harikrishnan Mulackal
---

## Vulnerability Title

ERC721A has mint caps that are not checked by ERC721SeaDrop

### Overview


This bug report is regarding ERC721SeaDrop.sol, which is a smart contract that inherits from ERC721A. The issue is that this smart contract can potentially reach a maximum capacity of 264-1 for all fields, such as balance, numberMinted, and numberBurned. If the maximum capacity is reached for a balance and someone else transfers a token, the balance can overflow, reducing the balance and numberMinted to a much lower number, and increasing the numberBurned to a much higher number. 

To remedy this issue, it is recommended to add an additional check in the mintSeaDrop function that would check if the quantity would exceed the mint cap. OpenSea has taken action and added a restraint that maxSupply cannot be set to greater than 264-1, so balance nor number minted can exceed this. This was done via the commit 5a98d29.

### Original Finding Content

## Medium Risk Severity Report

## Context
`ERC721SeaDrop.sol#L137-L145`

## Description
`ERC721SeaDrop` inherits from `ERC721A`, which packs `balance`, `numberMinted`, `numberBurned`, and an extra data chunk into one storage slot (64 bits per sub-storage) for every address. This creates an inherent cap of \( 2^{64} - 1 \) on all these different fields. Currently, there is no check in `ERC721A`'s `_mint` for quantity nor in `ERC721SeaDrop`'s `mintSeaDrop` function.

Additionally, if an owner is close to reaching the maximum cap for their balance and someone else transfers a token to this owner, an overflow may occur for the balance and possibly the number of mints in `_packedAddressData`. This overflow could potentially reduce the balance and the `numberMinted` to a much lower number, while `numberBurned` could be increased to a much higher number.

## Recommendation
We should implement an additional check to verify if the quantity would exceed the mint cap in `mintSeaDrop`.

## OpenSea
We will add checks regarding the `ERC721A` limits. A restraint has been implemented where `maxSupply` cannot be set greater than \( 2^{64} - 1 \) so that neither balance nor number minted can exceed this limit. See the commit `5a98d29`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | SeaDrop |
| Report Date | N/A |
| Finders | Sawmon and Natalie, Dravee, Harikrishnan Mulackal |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Seadrop-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Seadrop-Spearbit-Security-Review.pdf

### Keywords for Search

`Min/Max Cap Validation, Business Logic`

