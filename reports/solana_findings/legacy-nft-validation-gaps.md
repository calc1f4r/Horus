---
# Core Classification
protocol: Tensor Foundation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46759
audit_firm: OtterSec
contest_link: https://tensor.foundation/
source_link: https://tensor.foundation/
github_link: https://github.com/tensor-foundation

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
finders_count: 3
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Legacy NFT Validation Gaps

### Overview


The bug report discusses a vulnerability in TakeBidLegacy, specifically related to the handling of legacy standards for non-programmable NFTs. The issue involves missing validation for the master_edition account, which is responsible for ensuring the non-fungibility of an NFT. This validation is also missing for non-pNFTs. Additionally, there are missing checks for the metadata account in the TakeBidLegacy context. The suggested remediation is to add validation for the master_edition account and checks for the metadata account in TakeBidLegacy. This issue has been resolved in version #62.

### Original Finding Content

## Vulnerability Report

The vulnerability relates to verification gaps in **TakeBidLegacy** and the handling of legacy standards for NFTs (non-programmable NFTs). The **master_edition** account ensures the non-fungibility of an NFT. However, the **PDA** validation (Program-Derived Address) for **master_edition** is missing for non-pNFTs. Additionally, the metadata account’s seed checks are missing in the **TakeBidLegacy** context.

## Remediation

- Add **PDA**, initialized checks on **master_edition** in all legacy standard instructions.
- Include metadata account checks in **TakeBidLegacy**.

## Patch

Resolved in #62.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tensor Foundation |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://tensor.foundation/
- **GitHub**: https://github.com/tensor-foundation
- **Contest**: https://tensor.foundation/

### Keywords for Search

`vulnerability`

