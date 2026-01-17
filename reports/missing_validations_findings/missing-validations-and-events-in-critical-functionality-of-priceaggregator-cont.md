---
# Core Classification
protocol: Narwhal Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44713
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal Finance.md
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

Missing Validations and events in Critical functionality of PriceAggregator Contract

### Overview

See description below for full details.

### Original Finding Content

**Severity**  : Low

**Status**: Resolved

**Description**:


setUSDTFeed function: The function lacks input validation, which means that any value can be passed to it, potentially causing unexpected behavior or errors in the system. It would be best to validate the input to ensure that it is a valid feed address before setting it.
setOracle function: Similar to setUSDTFeed, this function also lacks input validation, allowing any address to be set as the oracle address, which could result in unexpected behavior or errors. Additionally, the function does not emit an event, making it difficult to track changes made to the oracle address.
setAge function: The function has input validation to prevent the age value from exceeding a certain limit. However, it does not emit an event, making it difficult to track changes made to the age value.
setNarwhalTrading function: The function lacks input validation, allowing any address to be set as the NarwhalTrading address, which could result in unexpected behaviour or errors. Additionally, the function does not emit an event, making it difficult to track changes made to the NarwhalTrading address.

**Recommendations** : 

For the setUSDTFeed function:
Add a check to ensure that the _feed parameter is not equal to zero.
Emit an event after setting the new feed.
For the setOracle function:
Add a check to ensure that the _oracle parameter is not equal to zero.
Emit an event after setting the new oracle.
For the setAge function:
Add a check to ensure that the _age parameter is not greater than 60.
Emit an event after setting the new age.
For the setNarwhalTrading function:
Add a check to ensure that the _NarwhalTrading parameter is not equal to zero.
Emit an event after setting the new NarwhalTrading address.

**Fixed**: Issue fixed in commit a72e06b

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Narwhal Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

