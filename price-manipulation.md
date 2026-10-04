---
# Core Classification
protocol: Aftermath Orderbook
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47458
audit_firm: OtterSec
contest_link: https://aftermath.finance/
source_link: https://aftermath.finance/
github_link: https://github.com/AftermathFinance

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
  - Robert Chen
  - Sangsoo Kang
  - MichałBochnak
---

## Vulnerability Title

Price Manipulation

### Overview


The report discusses a bug in a system that allows users to manipulate the book_price to their desired value. This can be done by influencing the mark_price within a certain percentage range of the index_price. The report suggests implementing additional safeguards or using decentralized oracles to prevent this type of manipulation. However, the team responsible for the system has chosen not to patch the bug as it is dependent on specific administrative actions.

### Original Finding Content

## Price Manipulation in Book Pricing

With significant resources, it is possible to manipulate the `book_price` to a desired value through front running. Currently, during the calculation of `premium_twap` and `spread_twap`, `clip_max_book_index_spread` confines the `book_price` within a range of plus five to minus five percent of the `index_price`. 

Nevertheless, it remains possible to influence the time-weighted average price by manipulating the `mark_price` within the same percentage range of the `index_price`. 

## Remediation

Implement additional safeguards, such as more sophisticated price manipulation detection algorithms or incorporated decentralized oracles.

## Patch

The Aftermath team has acknowledged this finding but chosen not to patch as the exploit is dependent on specific administrative actions.

© 2024 Otter Audits LLC. All Rights Reserved. 10/21

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Aftermath Orderbook |
| Report Date | N/A |
| Finders | Robert Chen, Sangsoo Kang, MichałBochnak |

### Source Links

- **Source**: https://aftermath.finance/
- **GitHub**: https://github.com/AftermathFinance
- **Contest**: https://aftermath.finance/

### Keywords for Search

`vulnerability`

