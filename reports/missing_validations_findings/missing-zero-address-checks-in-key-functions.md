---
# Core Classification
protocol: NUTS Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62699
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Pike/README.md#2-missing-zero-address-checks-in-key-functions
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
  - MixBytes
---

## Vulnerability Title

Missing Zero-Address Checks in Key Functions

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified within the `setRiskEngine()`, `setOracle()`, `transfer()`, `transferFrom()`, `redeem()`, and `withdraw()` functions. 

- **`setRiskEngine()` and `setOracle()`** 
  These functions do not validate that the new addresses provided are non-zero. Using `address(0)` for critical protocol components could cause undefined behavior or reverts during execution (e.g., calls to a nonexistent RiskEngine or Oracle).
  
- **`transfer()` and `transferFrom()`** 
  These functions do not validate that the destination address `dst` is non-zero, violating the ERC20 standard and potentially resulting in irreversible token burns.

- **`redeem()` and `withdraw()`** 
  These functions do not validate that the `receiver` address is non-zero. Assigning `address(0)` here may cause an unintended token burn or a loss of funds.
##### Recommendation
We recommend adding zero-address checks in the relevant functions to prevent accidental or malicious misconfiguration.


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | NUTS Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Pike/README.md#2-missing-zero-address-checks-in-key-functions
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

