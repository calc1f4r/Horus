---
# Core Classification
protocol: Trzn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37241
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN Finance.md
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

Missing checks for failures in `getChainlinkPrice` Function in `ERC20PriceOracle_V2`

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Acknowledged

**Description**

The `getChainlinkPrice` function does not include a check for potential failure scenarios when interacting with Chainlink oracles. 

**Recommendations**:

Implement error handling mechanisms to handle potential failures in fetching oracle data.

**Client comment**: If the Chainlink price fetching is down temporarily, it will be reverted and is as intended. However, in the case there is another reason the Chainlink service cannot be used, such as a chance in API service, the service can be continuously operation after updating the Oracle contract. 
In the future, if an error occurs in the implemented method (such as change in price fetching method from Chainlink, or service interruption from Chainlink), it will be updated so that another method can be used.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Trzn Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

