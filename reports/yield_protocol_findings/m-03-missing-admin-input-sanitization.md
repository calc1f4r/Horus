---
# Core Classification
protocol: Azuro
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20345
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-12-01-Azuro.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.20
financial_impact: medium

# Scoring
quality_score: 1
rarity_score: 1

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[M-03] Missing admin input sanitization

### Overview


This bug report outlines potential security issues in the `LP.sol` contract. It is likely that a malicious or compromised admin, or an error on the admin's part, could exploit these issues. The impact of exploiting this vulnerability could be high, as important protocol functionality could be bricked. 

The bug report describes that the `claimTimeout` property in `LP.sol` is not checked for having a very big value in both its setter function and in `initialize`. The same is true for the setter function of `withdrawTimeout`. Additionally, the `checkFee` method in `LP.sol` has a loose validation, allowing the max sum of all fees to be higher than 100%. Finally, the `startsAt` argument of `shiftGame` in `LP.sol` is not validated to ensure it is not after the current timestamp.

The bug report recommends adding an upper cap for `claimTimeout` & `withdrawTimeout`, making the max sum of all fees to be lower (for example 20%), and checking that `startsAt >= blockTimestamp` in `shiftGame`. 

In conclusion, this bug report outlines a potential vulnerability in the `LP.sol` contract. It is recommended that the suggested measures be taken to prevent exploitation of this vulnerability.

### Original Finding Content

**Likelihood:**
Low, because it requires a malicious/compromised admin or an error on admin side

**Impact:**
High, because important protocol functionality can be bricked

**Description**

It is not checked that the `claimTimeout` property in `LP.sol` both in its setter function and in `initialize` does not have a very big value. Same thing for the setter function of `withdrawTimeout`. Also, the `checkFee` method in `LP.sol` has a loose validation - the max sum of all fees should be much lower than 100%. Finally the `startsAt` argument of `shiftGame` in `LP.sol` is not validated that it is not after the current timestamp.

**Recommendations**

Add an upper cap for `claimTimeout` & `withdrawTimeout`. Make the max sum of all fees to be lower - for example 20%. In `shiftGame` check that `startsAt >= blockTimestamp`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 1/5 |
| Rarity Score | 1/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Azuro |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-12-01-Azuro.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

