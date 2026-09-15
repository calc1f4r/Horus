---
# Core Classification
protocol: Beyond
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45763
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-24-Beyond.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Datafeed addresses are not replaceable

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low	

**Status**: Resolved

**Description**

The `TokenBridgeBase.sol` smart contract receives 2 addresses by constructor to be used as Chainlink datafeeds: `btcDataFeed` and `nativeDataFeed`. However these addresses can not be replaced by different ones if a new datafeed is deployed by Chainlink or needs to be changed by other any reason, for example security concerns. 

**Recommendation**:

Create 2 ‘set functions’ to modify these DataFeed addresses. Do not forget to make the functions only callable by the owner.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Beyond |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-24-Beyond.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

