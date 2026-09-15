---
# Core Classification
protocol: Hord
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35601
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-24-Hord.md
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

Precision value has double meaning

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Informational

**Status**: Acknowledged 

**Description**

HordETHStakingManager.sol, getLSDTokenBalanceInETH()
HordETHStakingManager.sol, depositWithLSDToken()

Looks like stakingConfiguration.percentPrecision() has double meaning in terms of application. It is used as an intermediate accuracy multiplier for the price calculation and as an price lining up to token decimals (as for the accuracy correction after the chainlink price extraction). Though, in a general case, the intermediate accuracy for HETH/ETH price calculation does not equal the accuracy for the oracle price lining up for stETH.

**Recommendation**. 

Verify that indeed the same value is required for both cases (1e18) and consider using a separate value for chainlink price lining up.
**Post-audit:** The Hord team verified the value to be the same for both cases.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Hord |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-24-Hord.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

