---
# Core Classification
protocol: Possumadapters
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44153
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PossumAdapters-Security-Review.md
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
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[L-04] Missing Recipient Address Validation in `sellPortalEnergy()` Function of `AdaptersV1` Contract

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Reported By

[DevPelz](https://twitter.com/Pelz_Dev)

## Description

The `sellPortalEnergy()` function in the `AdaptersV1` contract lacks validation for the recipient address, which can lead to serious vulnerabilities. Depending on the selected mode, this function transfers PSM tokens or adds liquidity to a pair, potentially allowing unauthorized transfers to `address(0)` or other unintended recipients.

## Impact

This vulnerability can result in unauthorized transfers of PSM tokens to `address(0)` or other unintended recipients. Additionally, if the mode selected is 1, the function adds liquidity to a pair, which could result in the minting of Ramses pair tokens to an unauthorized recipient, potentially causing significant damage or financial loss.

## Location of Affected Code

File: [src/AdapterV1.sol#L548](https://github.com/shieldify-security/SPP-Adapters/blob/335351b51a87ce3d20ea471d0f686776ce7d2393/src/AdapterV1.sol#L548)

File: [src/AdapterV1.sol#L555](https://github.com/shieldify-security/SPP-Adapters/blob/335351b51a87ce3d20ea471d0f686776ce7d2393/src/AdapterV1.sol#L555)

File: [src/AdapterV1.sol#L590](https://github.com/shieldify-security/SPP-Adapters/blob/335351b51a87ce3d20ea471d0f686776ce7d2393/src/AdapterV1.sol#L590)

File: [src/AdapterV1.sol#L652](https://github.com/shieldify-security/SPP-Adapters/blob/335351b51a87ce3d20ea471d0f686776ce7d2393/src/AdapterV1.sol#L652)

## Recommendation

To mitigate this vulnerability, implement validation checks for the recipient address in the `sellPortalEnergy()` function. Ensure that the recipient address is not set to `address(0)` or any other unauthorized recipient before proceeding with token transfers or liquidity additions.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Possumadapters |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PossumAdapters-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

