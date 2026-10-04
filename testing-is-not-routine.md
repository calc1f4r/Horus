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
solodit_id: 17914
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

Testing is not routine

### Overview

See description below for full details.

### Original Finding Content

## Frax Solidity Security Assessment

## Difficulty: Undetermined

## Type: Testing

### Target: Various

### Description

The Frax Solidity repository does not have reproducible tests that can be run locally. Having reproducible tests is one of the best ways to ensure a codebase’s functional correctness. This finding is based on the following events:

- We tried to carry out the instructions in the Frax Solidity README at commit `31dd816`. We were unsuccessful.
- We reached out to Frax Finance for assistance. Frax Finance in turn pushed eight additional commits to the Frax Solidity repository (not counting merge commits).
- With these changes, we were able to run some of the tests, but not all of them.

These events suggest that tests require substantial effort to run (as evidenced by the eight additional commits), and that they were not functional at the start of the assessment.

### Exploit Scenario

Eve exploits a flaw in a Frax Solidity contract. The flaw would likely have been revealed through unit tests.

### Recommendations

**Short term:** Develop reproducible tests that can be run locally for all contracts. A comprehensive set of unit tests will help expose errors, protect against regressions, and provide a sort of documentation to users.

**Long term:** Incorporate unit testing into the CI process:

- Run the tests specific to contract X when a push or pull request affects contract X.
- Run all tests before deploying any new code, including updates to existing contracts.

Automating the testing process will help ensure the tests are run regularly and consistently. 

---

**Trail of Bits**

Frax Solidity Security Assessment

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

