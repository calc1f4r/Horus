---
# Core Classification
protocol: Tradable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44923
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-01-Tradable.md
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

Excessive fee is not refunded to the user

### Overview


The swapLiquidity function in the TradableSideVault contract allows users to swap tokens using the Stargate router. However, if the user provides too much of a fee, the extra amount is refunded to the contract address instead of the user's address. To fix this, the msg.sender address should be set as the refund address. This issue has been resolved.

### Original Finding Content

**Severity**: Medium

**Status**:  Resolved

The swapLiquidity function in TradableSideVault contract is able to execute swap using the Stargate router. Users can call this function externally, supplying a fee in native tokens. However, in case of excessive fees being provided, the surplus is refunded to the contract address itself, rather than the msg.sender address.

Recommendation: Set msg.sender address as a refund address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tradable |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-01-Tradable.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

