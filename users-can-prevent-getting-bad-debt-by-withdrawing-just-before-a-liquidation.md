---
# Core Classification
protocol: Bima
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53159
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a
source_link: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
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
finders_count: 1
finders:
  - santipu
---

## Vulnerability Title

Users can prevent getting bad debt by withdrawing just before a liquidation 

### Overview


The report describes a bug where a user can exploit the system by closing and reopening their Trove to avoid bad debt and increase it for other Troves. This can be done by waiting for a liquidation event to occur and then quickly reopening the Trove. To prevent this, it is recommended to implement a timelock for Trove closures.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
When a Trove is liquidated with bad debt, it is redistributed between the open Troves within that TroveManager.

A user can prevent getting bad debt and increase the bad debt for other Troves by executing the following exploit:

1. Bob sees a liquidation with bad debt is going to happen and closes his Trove.
2. Bob waits for the liquidation to happen (or does the liquidation himself).
3. Bob opens his Trove again.

As long as the borrowing fee is lower than the bad debt that Bob would have received, this attack is profitable and will increase the bad debt going to the rest of the Troves. Also, Bob could not open the Trove again and avoid paying the borrowing fee, just avoiding the bad debt for free.

In short, Bob can avoid getting the bad debt and make other Troves get more bad debt than they should.

## Recommendation
To mitigate this issue, it is recommended to implement a timelock that ensures Troves are not closed instantly but need to go through a withdrawal period (e.g. 1 day).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Bima |
| Report Date | N/A |
| Finders | santipu |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a

### Keywords for Search

`vulnerability`

