---
# Core Classification
protocol: Nftr
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26743
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2023-04-08-NFTR.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Guardian Audits
---

## Vulnerability Title

NMKT-1 | No Bids Can Be Entered

### Overview


This bug report is about a problem with a smart contract that is used to manage bids. The issue is that when no bids have been entered, the default values for the existing bid are an address of 0 and a tokenId of 0. The address of 0 does not have a function called ownerOf, so the call to getOwner will revert. This means that no bids can be entered.

The recommendation is to bypass the ownership check when there are no existing bids. This will ensure that the default values do not cause an issue and that bids can still be entered.

### Original Finding Content

**Description**

Initially, when no bids have been entered, the `existing` bid will have default values – `address(0)` as the collection and 0 for the `tokenId`. The zero address does not have function `ownerOf`, so the call to `getOwner` will revert. As a result, no bids can be entered.

**Recommendation**

Bypass the ownership check when there are no existing bids.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | Nftr |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2023-04-08-NFTR.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

