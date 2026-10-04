---
# Core Classification
protocol: BnbX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50270
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/stader-labs/bnbx-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/stader-labs/bnbx-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

MISSING ADDRESS CHECK

### Overview

See description below for full details.

### Original Finding Content

##### Description

The lack of zero address validation has been found in many instances when assigning user-supplied address values to state variables directly.

Code Location
-------------

[BnbX.sol, #37-49](https://github.com/stader-labs/bnbX/blob/2ddf3e2c30321587742630de90a1414434ff256f/contracts/BnbX.sol#L45)
The `setStakeManager` function allows you to set a `stakeManager` address to 0x0.

[StakeManager.sol, #70-73](https://github.com/stader-labs/bnbX/blob/2ddf3e2c30321587742630de90a1414434ff256f/contracts/StakeManager.sol#L70)
The `StakeManager`'s contract `initialization` function does not check that the passed addresses are non-0.

[StakeManager.sol, #326-338](https://github.com/stader-labs/bnbX/blob/2ddf3e2c30321587742630de90a1414434ff256f/contracts/StakeManager.sol#L334)
The `setBotAddress` function allows a bot's address to be set to 0x0.

##### Score

Impact: 1  
Likelihood: 1

##### Recommendation

**SOLVED:** Added zero address checks in commit [4e04e46729153b6cb50d2ce4da2f807611fcc4d8](https://github.com/stader-labs/bnbX/commit/4e04e46729153b6cb50d2ce4da2f807611fcc4d8)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | BnbX |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/stader-labs/bnbx-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/stader-labs/bnbx-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

