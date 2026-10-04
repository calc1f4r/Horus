---
# Core Classification
protocol: Pino
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27253
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Pino.md
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

[M-03] The contracts owner can maliciously front-run users

### Overview


This bug report outlines a vulnerability in the `Swap` and `Aave` contracts that can allow a malicious or compromised owner to front-run user calls and gain access to user funds. This vulnerability has a high impact, as it can result in a loss of funds for users, but the likelihood of it being exploited is low, as it requires malicious or compromised owners. To address this vulnerability, it is recommended to remove the `setNewAddresses` functionality from both contracts, as it is unnecessary and a new contract can be deployed to update the addresses in the front-end.

### Original Finding Content

**Severity**

**Impact:**
High, as it can result in a loss of funds for users

**Likelihood:**
Low, as it requires a malicious or compromised owners

**Description**

The `Swap` and `Aave` contracts have the `setNewAddresses` functionality, which can be only called by the contracts `owner`. If users send `Multicall` calls to the protocol and are using either the `Swap` or `Aave` contracts, the `owner` can front-run their call by updating the addresses to his own controlled malicious contracts, which can receive the user assets and give nothing back in return.

**Recommendations**

Remove the method from both contracts as it is not needed as the contracts shouldn't be holding any value or allowances anyway between transactions - if you wish to update the addresses in them you can just deploy new `Swap` or `Aave` contracts and make the front-end forward calls to them.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Pino |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Pino.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

