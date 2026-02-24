---
# Core Classification
protocol: Clave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54287
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b12ff6a1-673f-45d0-8066-4a8e21a361eb
source_link: https://cdn.cantina.xyz/reports/cantina_clave_feb2024.pdf
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
finders_count: 2
finders:
  - Riley Holterhus
  - Blockdev
---

## Vulnerability Title

Consider restricting users ' gas sponsorship usage 

### Overview


The GaslessPaymaster contract has a bug where registered accounts can potentially use up all of the contract's funds by making expensive transactions. This could negatively impact honest users. The report recommends either allocating a specific amount of gas to each user instead of a set number of transactions, or setting limits on the amount of gas and fees that can be used per transaction. The bug has been fixed in a recent update by adding a maximum sponsored ETH amount that can be used per transaction.

### Original Finding Content

## GaslessPaymaster Contract Analysis

## Context
GaslessPaymaster.sol#L71-L73

## Description
In the GaslessPaymaster contract, accounts that are registered in the claveRegistry will receive free gas sponsorships on a userLimit number of transactions. Each of these sponsored transactions can have arbitrary `gasLimit` and `maxFeePerGas` values, so users can potentially spend a large amount of the paymaster's ETH in each of their sponsored transactions. With enough unreasonably expensive transactions, the paymaster's balance could be depleted quickly, which would ruin the experience for honest users.

## Recommendation
Consider altering the paymaster to allocate users a certain amount of gas instead of a certain amount of transactions. Alternatively, consider adding upper bounds on the `gasLimit` and `maxFeePerGas` values, so that users can only use their sponsored transactions reasonably.

## Clave
Fixed in commit `c84a3e5f`.

## Cantina Managed
Verified. A `MAX_SPONSORED_ETH` constant was added to address the issue, and each sponsored transaction must now use less than this amount.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Clave |
| Report Date | N/A |
| Finders | Riley Holterhus, Blockdev |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_clave_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b12ff6a1-673f-45d0-8066-4a8e21a361eb

### Keywords for Search

`vulnerability`

