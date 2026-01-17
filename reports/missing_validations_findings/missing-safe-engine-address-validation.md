---
# Core Classification
protocol: Ocean Protocol H2O System and Action
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50376
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
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

MISSING SAFE ENGINE ADDRESS VALIDATION

### Overview

See description below for full details.

### Original Finding Content

##### Description

It was noted that `safeEngine_` address is not validated in `SurplusAuctionHouse.sol` contract. Lack of address validation has been found when assigning supplied address values to state variables directly. `safeEngine_` address should be `!=0` or add logic to check if the provided address is a valid Safe Engine Address.

Code Location
-------------

#### SurplusAuctionHouse.sol

```
    constructor(address safeEngine_, address protocolToken_) public {
        authorizedAccounts[msg.sender] = 1;
        safeEngine = SAFEEngineLike(safeEngine_);
        protocolToken = TokenLike(protocolToken_);
        contractEnabled = 1;
        emit AddAuthorization(msg.sender);
    }

```

#### SAFEEngine.sol

```
    constructor() public {
        authorizedAccounts[msg.sender] = 1;
        safeDebtCeiling = uint256(-1);
        contractEnabled = 1;
        emit AddAuthorization(msg.sender);
        emit ModifyParameters("safeDebtCeiling", uint256(-1));
    }

```

##### Score

Impact: 3  
Likelihood: 2

##### Recommendation

**SOLVED**: The `H2O team` solved the above issue in the commit [9c3225a836a570df867a8116eeac6f678b322a13](https://github.com/stablecoin-research/h20/commit/9c3225a836a570df867a8116eeac6f678b322a13). As a result, the team added the zero address check to `safeEngine_` throughout the in-scope H2O system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Ocean Protocol H2O System and Action |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

