---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28162
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/In-protocol%20Coverage/README.md#1-there-is-no-processing-of-the-value-returned-by-the-function
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
  - MixBytes
---

## Vulnerability Title

There is no processing of the value returned by the function

### Overview


This bug report is about a problem with the code in the Lido-Dao repository on Github. Specifically, two lines of code in the SelfOwnedStETHBurner.sol file are not processing the boolean values they are returning. This means that the code is not functioning properly, and needs to be fixed.

To fix the bug, it is necessary to add processing of the values returned by the function. This could involve using the boolean values to control the flow of the code, or using them in an if/else statement to change the behavior of the code depending on the value returned. 

The bug report provides the exact lines of code that need to be fixed. It is important to make sure that the code is correctly processing the boolean values it is returning, so that the code can function as expected.

### Original Finding Content

##### Description
At the line
https://github.com/lidofinance/lido-dao/blob/ee1991b3bbea2a24b042b0a4433be04301992656/contracts/0.8.9/SelfOwnedStETHBurner.sol#L228
the `transfer()` function returns a boolean variable. But this variable is not processed in any way.
Similarly for the line:
https://github.com/lidofinance/lido-dao/blob/ee1991b3bbea2a24b042b0a4433be04301992656/contracts/0.8.9/SelfOwnedStETHBurner.sol#L203.
##### Recommendation
It is necessary to add processing of the values returned by the function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/In-protocol%20Coverage/README.md#1-there-is-no-processing-of-the-value-returned-by-the-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

