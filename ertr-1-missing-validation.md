---
# Core Classification
protocol: GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27196
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
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

ERTR-1 | Missing Validation

### Overview


This bug report is related to the deposit and order creation process in the GMX platform. Currently, when creating a deposit, there is no validation that the longToken or shortToken are valid for the supplied market. This can lead to users losing their tokens in the depositStore. Additionally, there is no validation that either the long token amount or short token amount is non-zero. This check should be added to prevent the keeper from executing trivial deposits. Furthermore, when creating an order, there is no validation that the initial collateral token is valid for the provided market, which can lead to invalid orders stored in the orderStore.

The GMX team has acknowledged the report and recommended that validations for the deposit and order creation process be implemented. This will ensure that users do not lose their tokens in the depositStore, and that invalid orders are not stored in the orderStore.

### Original Finding Content

**Description**

When creating a deposit, there is no validation that the `longToken` or the `shortToken` are valid for the supplied market. If WBTC is accidentally used as the long token in an ETH/USDC market, the user would lose their WBTC in the `depositStore`.

Furthermore, there is no validation that either the long token amount or short token amount is non-zero. This check should be added to prevent the keeper from executing trivial deposits.

Additionally, when creating an order, there is no validation that the initial collateral token is valid for the provided market, which can lead to invalid orders stored in the `orderStore`.

**Recommendation**

Implement the above mentioned validations.

**Resolution**

GMX Team: Acknowledged

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | GMX |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

