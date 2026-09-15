---
# Core Classification
protocol: Atlendis Labs Loan Products
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17579
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Gustavo Grieco
  - Nat Chin
  - Justin Jacob
  - Elvis Skozdopolj
---

## Vulnerability Title

Lack of zero-address checks

### Overview


This bug report is about data validation in the "src/" codebase. It mentions that a number of functions in the codebase do not check if the zero address is passed in as a parameter, which should not be set to zero. This can lead to exploitable scenarios such as Alice, the deployer of the RCLFactory, accidentally setting the factoryRegistry parameter to zero in the constructor, resulting in the deploy function always reverting and the contract unusable. Another scenario is if the governance in control of the RewardsManager contract accidentally adds an invalid module via the addModule function, which can lead to users' staked positions becoming permanently locked.

To fix the issue short term, it is suggested to add zero-address checks for the parameters listed and for all other parameters for which the zero address is not an acceptable value. Additionally, a supportsInterface check should be added to the RewardsManager contract to ensure an invalid module cannot be added. Long term, input validation should be reviewed across components to ensure bugs in other components do not prevent them from performing validation.

### Original Finding Content

## Diﬃculty: High

## Type: Data Validation

## Target: src/

## Description
A number of functions in the codebase do not revert if the zero address is passed in for a parameter that should not be set to zero. The following parameters, among others, do not have zero-address checks:

- The `token` and `rolesManager` variables in the PoolCustodian’s constructor
- The `_rolesManager`, `_pool`, and `_rewardsOperator` in `updateRolesManager`, `initializePool`, and `updateRewardsOperator`, respectively
- The `factoryRegistry` in `LoanFactoryBase` and in the `RCLFactory`
- The `rolesManager` in `Managed.sol`’s constructor
- The `module` address in `RewardsManager.sol`’s `addModule` function

## Exploit Scenario
Alice, the deployer of the `RCLFactory`, accidentally sets the `factoryRegistry` parameter to zero in the constructor. As a result, the `deploy` function will always revert and the contract will be unusable.

The governance in control of the `RewardsManager` contract accidentally adds an invalid module via the `addModule` function. Since all user actions loop through all of the added modules, all user-staked positions become permanently locked, and users are prevented from unstaking or claiming rewards.

## Recommendations
Short term, add zero-address checks for the parameters listed above and for all other parameters for which the zero address is not an acceptable value. Add a `supportsInterface` check for any modules added to the `RewardsManager` contract to ensure an invalid module cannot be added.

Long term, review input validation across components. Avoid relying solely on the validation performed by front-end code, scripts, or other contracts, as a bug in any of those components could prevent them from performing that validation.

---

Trail of Bits  
26  
Atlendis Labs Security Assessment  
PUBLIC

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Atlendis Labs Loan Products |
| Report Date | N/A |
| Finders | Gustavo Grieco, Nat Chin, Justin Jacob, Elvis Skozdopolj |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf

### Keywords for Search

`vulnerability`

