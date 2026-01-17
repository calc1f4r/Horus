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
solodit_id: 50377
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

MISSING FACTORY ADDRESS VALIDATION

### Overview

See description below for full details.

### Original Finding Content

##### Description

It was noted that `factory_` address is not validated in `GebProxyRegistry.sol` contract. Lack of address validation has been found when assigning supplied address values to state variables directly. `factory_` address should be `!=0` or add logic to check if the provided address is a valid Factory Address.

Code Location
-------------

#### GebProxyRegistry.sol

```
    constructor(address factory_) public {
        factory = DSProxyFactory(factory_);
    }

```

#### proxy.sol

```
contract DSProxyFactory {
    event Created(address indexed sender, address indexed owner, address proxy, address cache);
    mapping(address=>bool) public isProxy;
    DSProxyCache public cache;

    constructor() public {
        cache = new DSProxyCache();
    }


```

##### Score

Impact: 3  
Likelihood: 2

##### Recommendation

**SOLVED**: The `H2O team` solved the above issue in the commit [48863e0b91e152c6900fb6d61d31566fa9819bb1](https://github.com/stablecoin-research/h20-proxy-registry/commit/48863e0b91e152c6900fb6d61d31566fa9819bb1). As a result, the team added the zero address check to `factory_`.

#### Updated Code

```
    constructor(address factory_) public {
        require(factory_ != address(0), "GebProxyRegistry/proxy-factory-address-invalid");
        factory = DSProxyFactory(factory_);
    }

```

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

