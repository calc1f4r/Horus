---
# Core Classification
protocol: Elektrik
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37561
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-09-Elektrik.md
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

TWAP CAN BE MANIPULATED IF THE PERIOD IS SHORT ENOUGH

### Overview


The report describes a bug in a function called `getUsdPrice` in a contract called `UsdOracle.sol`, which is used to convert a token amount to USD. The bug allows the price to be manipulated if the input value for `_period` is set to a short value. The recommendation is to add a check to ensure that `_period` is at least 30 minutes to prevent this manipulation. The client comments that they want the contract to be flexible and that the backend will send a period of 30 for spot prices to avoid manipulation. 

### Original Finding Content

**Severity**: Medium	

**Status**: Acknowledged

**Description**

The function `getUsdPrice` in `UsdOracle.sol` is used for converting an amount of token to usd. This function gets `_period` as input. `_period` is the number of seconds from which to calculate the TWAP. If `_period` is set to a short value then the price can be manipulated.


**Recommendation**:

Add a check that ensures that `_period` is at least 30 minutes to avoid price manipulation.

**Client comment**: 

Oracle contract is a helper contract, and we want it to be as flexible as possible. Also we are using the same contract at frontend for spot prices. Where twap manipulation is concerned the back-end will send the period as 30

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Elektrik |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-09-Elektrik.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

