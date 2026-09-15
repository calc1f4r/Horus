---
# Core Classification
protocol: Akita
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48769
audit_firm: OtterSec
contest_link: https://akt.finance/
source_link: https://akt.finance/
github_link: https://github.com/otter-sec/akita/tree/master/ programs/akita.

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
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Closing Edit Proposals

### Overview

See description below for full details.

### Original Finding Content

## Edit Proposal PDA Accounts

The `edit_proposal` PDA accounts are created by taking the rent amount from the proposer. Those accounts should be properly closed and the rent amount should be sent back to the proposer.

## Remediation

The `edit_proposal` accounts should be closed as part of the `AcceptEditProposal` instruction and the rent amount sent back to the proposer. Alternatively, add a `CancelEditProposal` instruction to close the edit proposals that are not accepted. The rent expended there should be sent back to the proposer as well.

## Patch

Added a new instruction to close `EditProposal` in `0e9d501`.

© 2022 OtterSec LLC. All Rights Reserved. 13 / 25

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Akita |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec |

### Source Links

- **Source**: https://akt.finance/
- **GitHub**: https://github.com/otter-sec/akita/tree/master/ programs/akita.
- **Contest**: https://akt.finance/

### Keywords for Search

`vulnerability`

