---
# Core Classification
protocol: INIT Capital
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29599
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-initcapital
source_link: https://code4rena.com/reports/2023-12-initcapital
github_link: https://github.com/code-423n4/2023-12-initcapital-findings/issues/17

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

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - said
  - rvierdiiev
  - ladboy233
---

## Vulnerability Title

[M-08] `TRST-M-8` from previous audit still present

### Overview


This report discusses a bug in the Interest Accruing feature of the TRST-M-8 protocol. The bug causes interest to continue accruing even when repaying is paused, which can lead to users accumulating more debt than intended. The protocol team has stated that they have fixed the issue, but the bug still exists. The recommended mitigation step is to implement a logic that pauses all interest accruing, but it is uncertain if this is necessary. The issue has been acknowledged by the sponsor and should be considered a valid medium bug. 

### Original Finding Content


Interest accruing is not paused, when repaying is not allowed.

### Proof of Concept

TRST-M-8 from previous audit describes the fact, that when repaying is paused, then pool still continue accruing interests. Usually this is not considered as a medium bug anymore.
However, protocol team has stated that they have fixed everything.

I should say that TRST-M-8 still exists and in case repayment will be paused and user will not be able to reduce their debt, their debt shares will continue to accrue interest.

### Tools Used

VsCode

### Recommended Mitigation Steps

You can implement the logic that will pause all interest accruing as well, but I am not sure this is indeed needed.

**[fez-init (INIT) acknowledged and commented](https://github.com/code-423n4/2023-12-initcapital-findings/issues/17#issuecomment-1870188388):**
 > There might have been miscommunications with this issue being resolved. This issue from Trust should be communicated as acknowledged.

**[hansfriese (Judge) commented](https://github.com/code-423n4/2023-12-initcapital-findings/issues/17#issuecomment-1871329916):**
 > According to the sponsor's comment, it's worth keeping it as a valid medium.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | INIT Capital |
| Report Date | N/A |
| Finders | said, rvierdiiev, ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-initcapital
- **GitHub**: https://github.com/code-423n4/2023-12-initcapital-findings/issues/17
- **Contest**: https://code4rena.com/reports/2023-12-initcapital

### Keywords for Search

`vulnerability`

