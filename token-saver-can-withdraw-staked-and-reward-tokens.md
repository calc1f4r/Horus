---
# Core Classification
protocol: Rainmaker
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56298
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-12-29-Rainmaker.md
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
  - Zokyo
---

## Vulnerability Title

Token saver can withdraw staked and reward tokens.

### Overview


The bug report is about an issue with transferring tokens. Specifically, in the function "saveToken," there are no limitations on the types of tokens that can be transferred. The recommendation is to add a restriction on transferring tokens that have been staked or received as rewards. The client has verified that this ability will be delegated to a multisig wallet.

### Original Finding Content

**Description**

Line 24-27, function saveToken. There are no restrictions on which tokens can be transferred.

**Recommendation**:

Add a restriction on transferring staked and reward tokens.
PostAudit. Client verified that ability to transfer tokens will be delegated to multisig wallet.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Rainmaker |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-12-29-Rainmaker.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

