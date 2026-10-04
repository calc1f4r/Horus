---
# Core Classification
protocol: MakerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40412
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/9cff4d7b-b94c-4708-860e-f63f38e21148
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_snst_may2024.pdf
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
finders_count: 3
finders:
  - m4rio
  - shung
  - Christoph Michel
---

## Vulnerability Title

sNst accumulates DAI dust

### Overview

See description below for full details.

### Original Finding Content

## SNst.sol#L401

## Description
The sNst uses a fixed share price **chi** for minting and redeeming shares (compared to a dynamic one taking into account the total DAI assets / total shares). It also rounds in favor of the contract, against the user, when depositing and withdrawing assets. Therefore, a small DAI balance will accumulate in the contract as users interact with the contract. These assets are locked in the contract and cannot be withdrawn.

## Recommendation
As the dust value is tiny (in order of number of contract withdrawals) compared to DAI's 18-decimal precision, the excess locked value is negligible. No further action needs to be taken.

## Maker
Acknowledged.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, shung, Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_snst_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/9cff4d7b-b94c-4708-860e-f63f38e21148

### Keywords for Search

`vulnerability`

