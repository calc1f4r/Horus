---
# Core Classification
protocol: Hubble
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4211
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-hubble-contest
source_link: https://code4rena.com/reports/2022-02-hubble
github_link: #l-05-missing-zero-address-check-in-constructors-and-the-setter-functions

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

protocol_categories:
  - dexes
  - services
  - derivatives
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-05] Missing zero-address check in constructors and the setter functions

### Overview

See description below for full details.

### Original Finding Content


Missing checks for zero-addresses may lead to infunctional protocol, if the variable addresses are updated incorrectly.

### Proof of Concept

Navigate to the following contract functions:

* <https://github.com/code-423n4/2022-02-hubble/blob/8c157f519bc32e552f8cc832ecc75dc381faa91e/contracts/MarginAccountHelper.sol#L19><br>

* <https://github.com/code-423n4/2022-02-hubble/blob/8c157f519bc32e552f8cc832ecc75dc381faa91e/contracts/VUSD.sol#L39><br>

* <https://github.com/code-423n4/2022-02-hubble/blob/8c157f519bc32e552f8cc832ecc75dc381faa91e/contracts/legos/Governable.sol#L16><br>

* <https://github.com/code-423n4/2022-02-hubble/blob/8c157f519bc32e552f8cc832ecc75dc381faa91e/contracts/InsuranceFund.sol#L35><br>

* <https://github.com/code-423n4/2022-02-hubble/blob/8c157f519bc32e552f8cc832ecc75dc381faa91e/contracts/MarginAccount.sol#L121><br>

### Recommended Mitigation Steps

Consider adding zero-address checks in the discussed constructors:<br>
require(newAddr != address(0));.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Hubble |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-hubble
- **GitHub**: #l-05-missing-zero-address-check-in-constructors-and-the-setter-functions
- **Contest**: https://code4rena.com/contests/2022-02-hubble-contest

### Keywords for Search

`vulnerability`

