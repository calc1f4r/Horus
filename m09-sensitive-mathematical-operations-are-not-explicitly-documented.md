---
# Core Classification
protocol: Aave Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11614
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/aave-protocol-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M09] Sensitive mathematical operations are not explicitly documented

### Overview


The Aave team was attempting to make their platform as transparent as possible by implementing calculations in their smart contracts. These calculations involve complex arithmetic operations over different units, making it essential that they work flawlessly to avoid financial losses. However, the calculations were sparsely documented and lacked explicit units for the terms involved. This made auditing the code difficult and unreliable, and prevented validation of the formulas in the whitepaper. 

To improve the readability of the code and the users’ experience, it is necessary to document the calculations and explicitly state all units of terms involved. Additionally, thorough unit testing of all critical calculations should be done to programmatically ensure that the code’s behavior is expected.

The issue has been partially fixed with the most recent whitepaper being clearer. However, the units of the variables in the `CoreLibrary.sol` structs are still undocumented.

### Original Finding Content

Intending to make the platform as transparent as possible, the Aave team has implemented most of the calculations the Aave protocol relies on in their smart contracts. Such calculations usually entail complex arithmetic operations over balances, timestamps, rates, percentages, prices, decimals, among others, that are measured in several different units. It is of utmost importance for such operations to work flawlessly, considering that the Aave protocol is set out to handle large amounts of valuable assets, and any error may cause outstanding financial losses. However, such sensitive operations were found to be sparsely documented, the most important shortcoming being the lack of explicit units for each term involved.


This lack of explicit units for state variables, parameters and return values greatly hindered the auditing process. While attempts to validate all calculations spread throughout the code base were made, still the manual process was unreliable and error-prone. Mapping formulas to the provided whitepaper was not straightforward either, because there are many mismatches – as reported in [**“[L18] Whitepaper issues”**](#l18). Assessing for correctness becomes difficult when there is no way to straightforwardly understand the units used in each calculation, regardless of their simplicity. These are the reasons why we are listing this issue with Medium severity.


Great efforts must be made in term of documenting calculations and explicitly stating all units of the terms involved. This should greatly improve the readability of the code, which should add to the platform’s transparency and the users’ overall experience. As the process of manually auditing all sensitive arithmetic operations has been proven hard-to-follow, unreliable and potentially error-prone, thorough unit testing of all critical calculations is in order to programmatically ensure that the code’s current behavior is expected.


**Update**: *Partially fixed. The most recent whitepaper shared with us is significantly clearer. However, the units of the variables in the `CoreLibrary.sol` structs are still undocumented.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Aave Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/aave-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

