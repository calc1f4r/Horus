---
# Core Classification
protocol: Metalabel
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20408
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-01-01-Metalabel.md
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
  - Pashov
---

## Vulnerability Title

[M-01] Insufficient input data validation for `configureSequence`

### Overview


This bug report is about an issue with the `Collection::configureSequence` and `DropEngine::configureSequence` functions. If not properly validated, user input can result in a Denial of Service (DoS) or too big of a royalty payment. The likelihood of this happening is low, as it requires a configuration error or a malicious actor. 

The `_sequence` parameter of the `Collection::configureSequence` method is of type `SequenceData` and its fields are not validated. Five checks are missing: 1) `sealedBeforeTimestamp` is bigger than `block.timestamp`; 2) `sealedAfterTimestamp` is always bigger than `sealedBeforeTimestamp`; 3) the difference between `sealedBeforeTimestamp` and `sealedAfterTimestamp` is at least `2 days`; 4) the difference between `sealedBeforeTimestamp` and `sealedAfterTimestamp` is not more than `500 days`; and 5) the difference between `sealedBeforeTimestamp` and `block.timestamp` is not more than `10 days`. Additionally, in `DropEngine::configureSequence` the `royaltyBps` is not validated that it is not more than 100%. 

The recommendation is to add sensible constraints and validations for all user input mentioned above.

### Original Finding Content

**Impact:**
High, as some of those can result in a DoS or too big of a royalty payment

**Likelihood:**
Low, as it requires a configuration error or a malicious actor

**Description**

An authorized address for a node can call `Collection::configureSequence` where most of the input is not validated properly. The `_sequence` parameter of the method is of type `SequenceData` which fields are not validated. Missing checks are the following:

1.  `sealedBeforeTimestamp` is bigger than `block.timestamp`
2.  `sealedAfterTimestamp` is always bigger than `sealedBeforeTimestamp`
3.  The difference between `sealedBeforeTimestamp` and `sealedAfterTimestamp` is at least `2 days ` for example
4.  The difference between `sealedBeforeTimestamp` and `sealedAfterTimestamp` is not more than `500 days` for example
5.  The difference between `sealedBeforeTimestamp` and `block.timestamp` is not more than `10 days` for example

Also in `DropEngine::configureSequence` the `royaltyBps` is not validated that it is not more than 100% (a value of 10000). I suggest you add a lower royaltyBps upper bound.

**Recommendations**

Add sensible constraints and validations for all user input mentioned above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Metalabel |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-01-01-Metalabel.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

