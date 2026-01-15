---
# Core Classification
protocol: Aarna
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37186
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-04-aarna.md
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

Unnecessary decimal normalization for Chainlink price feeds

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Informational

**Status**:  Resolved

**Description**


The checkIfUSDC function from AFiStorage contract is designed to determine the price of a given token (tok) in terms of USDC. The function utilizes Chainlink oracles to retrieve the latest price data. However, it uses logic to adjust for potential variations in decimal precision of the price data returned from Chainlink. In reality, all Chainlink price feeds that offer a rate for non-ETH pairs consistently return values with 8 decimal precision. Therefore, this normalization logic is redundant and adds unnecessary complexity.

**Recommendation**: 

The function should be simplified by removing any logic related to adjusting based on different decimal precision.
Fix: The issue has been fixed as recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Aarna |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-04-aarna.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

