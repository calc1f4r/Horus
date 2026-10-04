---
# Core Classification
protocol: NFTX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4021
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-nftx-contest
source_link: https://code4rena.com/reports/2021-05-nftx
github_link: https://github.com/code-423n4/2021-05-nftx-findings/issues/44

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

protocol_categories:
  - dexes
  - cross_chain
  - rwa
  - leveraged_farming
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-03] Missing parameter validation

### Overview

See description below for full details.

### Original Finding Content

## Handle

@cmichelio


## Vulnerability details


## Vulnerability Details

Missing parameter validation for functions:
- `NFTXEligiblityManager.addModule, updateModule`
- `NFTXFeeDistributor` all `setter` functions (`setTreasuryAddress`, ...)
- `NFTXVaultUpgradeable.setManager`

## Impact

Some wallets still default to zero addresses for a missing input which can lead to breaking critical functionality like setting the manager to the zero address and being locked out.

## Recommended Mitigation Steps

Validate the parameters.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | NFTX |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-nftx
- **GitHub**: https://github.com/code-423n4/2021-05-nftx-findings/issues/44
- **Contest**: https://code4rena.com/contests/2021-05-nftx-contest

### Keywords for Search

`vulnerability`

