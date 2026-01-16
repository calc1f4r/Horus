---
# Core Classification
protocol: Skip Slinky Oracle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47296
audit_firm: OtterSec
contest_link: https://skip.build/
source_link: https://skip.build/
github_link: https://github.com/skip-mev/slinky

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
  - Naoya Okanami
  - Robert Chen
---

## Vulnerability Title

Mismatch Between CometBFT and Application Views

### Overview


The Comet BFT's view of validators is different from the application's view, which can cause issues if not handled properly. The issue in the voteweighted::median arises from a mismatch in the data used to determine voting power. The code uses Vote Extensions to potentially contain additional information about validator votes, but this information is based on data from the previous height, creating a mismatch as voteWeight and totalBondedTokens are based on the current height. This can result in inaccurate voting power calculations. To fix this, it is important to properly utilize both Comet BFT's and the application's views to prevent liveliness issues. This issue has been fixed in P.R. #512. © 2024 Otter Audits LLC. All Rights Reserved. 7/19.

### Original Finding Content

## Comet BFT’s View of Validators

Comet BFT’s view of validators differs from the application’s view, making it imperative to handle and utilize these views appropriately. Failure to appropriately manage these disparate views can lead to unintended liveness issues.

## The Issue in `voteweighted::median`

The issue in `voteweighted::median` arises from a mismatch in the data used to determine voting power. The code utilizes Vote Extensions to potentially contain additional information about validator votes. However, these extensions are based on data from the previous height. This creates a mismatch as `voteWeight` and `totalBondedTokens` are based on the current height. Information from Vote Extensions may influence voting power calculations. However, since it is based on outdated data, it will result in inaccurate voting power calculations.

## Remediation

Ensure the proper utilization of Comet BFT’s and the application’s views to prevent liveness issues.

## Patch

Fixed in PR #512.

© 2024 Otter Audits LLC. All Rights Reserved. 7/19

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Skip Slinky Oracle |
| Report Date | N/A |
| Finders | Naoya Okanami, Robert Chen |

### Source Links

- **Source**: https://skip.build/
- **GitHub**: https://github.com/skip-mev/slinky
- **Contest**: https://skip.build/

### Keywords for Search

`vulnerability`

