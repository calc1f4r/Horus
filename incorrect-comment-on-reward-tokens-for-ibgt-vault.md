---
# Core Classification
protocol: Infrared Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54099
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/89e5aa01-14ad-48f8-af3d-d1182d4ffefb
source_link: https://cdn.cantina.xyz/reports/cantina_infrared_july2024.pdf
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
finders_count: 4
finders:
  - 0xRajeev
  - Mario Poneder
  - Cryptara
  - phaze
---

## Vulnerability Title

Incorrect comment on reward tokens for IBGT vault 

### Overview

See description below for full details.

### Original Finding Content

## Context: Infrared.sol#L197-L201

## Description
The comment on line 197 in the initialize function of the Infrared contract incorrectly states that the IBGT vault can have IBGT and IRED rewards. In reality, the IBGT vault can also have Honey (Bera native stablecoin) as a reward token. This incorrect comment can lead to misunderstandings about the functionality and supported reward tokens of the IBGT vault.

## Recommendation
Update the comment to accurately reflect that the IBGT vault can have IBGT, IRED, and Honey as reward tokens. Ensure that all comments within the contract correctly describe the associated code behavior to maintain clarity and prevent misunderstandings.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Infrared Finance |
| Report Date | N/A |
| Finders | 0xRajeev, Mario Poneder, Cryptara, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_infrared_july2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/89e5aa01-14ad-48f8-af3d-d1182d4ffefb

### Keywords for Search

`vulnerability`

