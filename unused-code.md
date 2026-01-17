---
# Core Classification
protocol: Archimedes Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50606
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/archimedes/archimedes-finance-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/archimedes/archimedes-finance-smart-contract-security-assessment
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

UNUSED CODE

### Overview

See description below for full details.

### Original Finding Content

##### Description

Unused pieces of code such as modifiers or variables have been found through the code. These unused variables increase gas costs for contract deploying and interactions, impact code readability and might cause the contract to behave in unexpected ways or introduce new vulnerabilities if these variables are mistakenly used.

Code Location
-------------

#### LeverageEngine.sol

```
    uint256 internal _positionId;

```

This variable is not used anywhere in the code.

#### CDPosition.sol

```
    struct CDP {
        uint256 oUSDPrinciple; // Amount of OUSD originally deposited by user
        uint256 oUSDInterestEarned; // Total interest earned (and rebased) so far
        uint256 oUSDTotal; // Principle + OUSD acquired from selling borrowed lvUSD + Interest earned
        uint256 lvUSDBorrowed; // Total lvUSD borrowed under this position
        uint256 shares; // Total vault shares allocated to this position
    }

```

`oUSDInterestEarned` is declared within CDP struct, but it is not used anywhere in the code.

```
    modifier notImplementedYet() {
        revert("Method not implemented yet");
        _;
    }

```

This modifier is not used anywhere.

##### Score

Impact: 1  
Likelihood: 1

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Archimedes Finance |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/archimedes/archimedes-finance-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/archimedes/archimedes-finance-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

