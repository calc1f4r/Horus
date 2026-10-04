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
solodit_id: 7318
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

redeemFutureEpoch transfers the shares from the msg.sender to the vault instead of from the owner

### Overview


A bug was reported in PublicVault.sol on line 143. The bug was that the redeemFutureEpoch function was transferring the vault shares from the message sender to the vault instead of from the owner. This posed a medium risk. To fix the bug, the first parameter passed to the ERC20(address(this)).safeTransferFrom needs to be the owner instead of the message sender. This has been fixed in the code at 443b0e01263755a64c98e3554b43a8fbfa1de215 and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
`PublicVault.sol#L143`

## Description
`redeemFutureEpoch` transfers the vault shares from the `msg.sender` to the vault instead of from the owner.

## Recommendation
The 1st parameter passed to the `ERC20(address(this)).safeTransferFrom` needs to be the owner:

```solidity
- ERC20(address(this)).safeTransferFrom(msg.sender, address(this), shares);
+ ERC20(address(this)).safeTransferFrom(owner, address(this), shares);
```

## Astaria
Fixed in `443b0e01263755a64c98e3554b43a8fbfa1de215`.

## Spearbit
Verified.

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

