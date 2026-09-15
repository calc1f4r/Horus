---
# Core Classification
protocol: Frax Solidity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17915
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
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
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

No clear mapping from contracts to tests

### Overview

See description below for full details.

### Original Finding Content

## Frax Solidity Security Assessment

**Difficulty:** High  
**Type:** Access Controls  
**Target:** Various  

## Description

There are 405 Solidity files within the `contracts` folder, but there are only 80 files within the `test` folder. Thus, it is not clear which tests correspond to which contracts. The number of contracts makes it impractical for a developer to run all tests when working on any one contract. Thus, to test a contract effectively, a developer will need to know which tests are specific to that contract. 

Furthermore, as per **TOB-FRSOL-001**, we recommend that the tests specific to contract X be run when a push or pull request affects contract X. To apply this recommendation, a mapping from the contracts to their relevant tests is needed.

## Exploit Scenario

Alice, a Frax Finance developer, makes a change to a Frax Solidity contract. Alice is unable to determine the file that should be used to test the contract and deploys the contract untested. The contract is exploited using a bug that would have been revealed by a test.

## Recommendations

**Short term:** For each contract, produce a list of tests that exercise that contract. If any such list is empty, produce tests for that contract. Having such lists will help facilitate contract testing following a change to it.

**Long term:** As per **TOB-FRSOL-001**, incorporate unit testing into the CI process by running the tests specific to contract X when a push or pull request affects contract X. Automating the testing process will help ensure the tests are run regularly and consistently.

1. `find contracts -name '*.sol' | wc -l`
2. `find test -type f | wc -l`

---

**Trail of Bits**  
**Frax Solidity Security Assessment**  
**PUBLIC**

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Solidity |
| Report Date | N/A |
| Finders | Samuel Moelius Maximilian Krüger Troy Sargent |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf

### Keywords for Search

`vulnerability`

