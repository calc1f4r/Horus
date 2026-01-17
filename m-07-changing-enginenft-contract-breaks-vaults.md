---
# Core Classification
protocol: Mochi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 941
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-mochi-contest
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/130

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
  - dexes
  - cdp
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-07] Changing engine.nft contract breaks vaults

### Overview


This bug report details a vulnerability in the Governance of a system that allows it to change the `engine.nft` address used by vaults to represent collateralized debt positions (CDP). If this address is changed, it could allow existing CDPs to be overwritten when a vault is minted using `MochiVault.mint`. This could have a significant negative impact on the system.

The recommended mitigation steps for this vulnerability are to either disallow setting a new NFT address, or to ensure that the new NFT's IDs start at the old NFT's IDs. This will help to ensure that existing CDPs are not inadvertently overwritten.

### Original Finding Content

_Submitted by cmichel_

Governance can change the `engine.nft` address which is used by vaults to represent collateralized debt positions (CDP).
When minting a vault using `MochiVault.mint` the address returned ID will be used and overwrite the state of an existing debt position and set its status to `Idle`.

#### Impact
Changing the NFT address will allow overwriting existing CDPs.

#### Recommended Mitigation Steps
Disallow setting a new NFT address. or ensure that the new NFT's IDs start at the old NFT's IDs.

**[ryuheimat (Mochi) confirmed](https://github.com/code-423n4/2021-10-mochi-findings/issues/130)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/130
- **Contest**: https://code4rena.com/contests/2021-10-mochi-contest

### Keywords for Search

`vulnerability`

