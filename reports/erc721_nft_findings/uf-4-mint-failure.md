---
# Core Classification
protocol: Ultimate Fantoms
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20293
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-05-23-Ultimate Fantoms.md
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
  - Guardian Audits
---

## Vulnerability Title

UF-4 | Mint Failure

### Overview


This bug report is about an issue in the publicMint function of a program. When performing _earnTo = random() % (_tokenIdCounter.current() +1), it is possible that _earnTo is equal to _tokenIdCounter.current(), which yields a tokenID for a token that does not exist yet. This causes the subsequent call to ownerOf to fail and the mint to revert. The recommendation to fix this issue is to perform random() % _tokenIdCounter.current(). The resolution to this bug report is that the suggestion was applied and the issue was resolved.

### Original Finding Content

**Description**

In `publicMint`, when performing `_earnTo = random() % (_tokenIdCounter.current() +1)`, there is a
possibility `_earnTo` is equivalent to `_tokenIdCounter.current()` which yields a `tokenID` for a token that
does not exist yet. Therefore, the subsequent call to `ownerOf` will fail and the mint will revert.

**Recommendation**

Perform `random() % _tokenIdCounter.current()`.

**Resolution**

Ultimate Fantoms: Resolved, applied suggestion.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | Ultimate Fantoms |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-05-23-Ultimate Fantoms.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

