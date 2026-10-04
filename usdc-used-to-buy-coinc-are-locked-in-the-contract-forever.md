---
# Core Classification
protocol: Coinlend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20926
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-29-Coinlend.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.20
financial_impact: high

# Scoring
quality_score: 1
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - AuditOne
---

## Vulnerability Title

USDC used to buy COINC are locked in the contract forever

### Overview


The CoinlendCredits contract is a smart contract that allows users to use USDC to mint COINC tokens. However, the contract does not provide any way for users to redeem or withdraw the USDC they deposited into the contract, thus locking the amount of USDC deposited to the contract forever. To fix this issue, it is recommended to add a function to allow users to redeem COINC for USDC in the contract.

### Original Finding Content

**Description:**

In the CoinlendCredits contract, users can use USDC to mint COINC tokens. However, there is no way to redeem or withdraw the USDC in the contract. As a result, the amount of USDC deposited to the contract is locked forever.

**Recommendations:**

Consider adding a function to allow users to redeem COINC for USDC in the CoinlendCredits contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 1/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Coinlend |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-29-Coinlend.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

