---
# Core Classification
protocol: BendDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49599
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-12-benddao-invitational
source_link: https://code4rena.com/reports/2024-12-benddao-invitational
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
  - lending

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-02] Missing price staleness check `inAdapter::latestAnswer`

### Overview

See description below for full details.

### Original Finding Content


* Instances(2)

There are no staleness checks in multiple `latestAnswer` methods from the adapter. Due to latestAnswer is not used in flows in scope. No material impact.

1. [src/oracles/EETHPriceAdapter.sol# L77]((<https://github.com/code-423n4/2024-12-benddao/blob/489f8dd0f8e86e5a7550cc6b81f9edfe79efbf4e/src/oracles/EETHPriceAdapter.sol# L77>):

   
```

   function latestAnswer() public view virtual returns (int256) {
       int256 basePrice = BASE_AGGREGATOR.latestAnswer();
       int256 weETHPrice = WEETH_AGGREGATOR.latestAnswer();

       return _convertWEETHPrice(basePrice, weETHPrice);
   }
   
```

2. [src/oracles/SUSDSPriceAdapter.sol# L62](https://github.com/code-423n4/2024-12-benddao/blob/489f8dd0f8e86e5a7550cc6b81f9edfe79efbf4e/src/oracles/SUSDSPriceAdapter.sol# L62):

   
```

   function latestAnswer() public view virtual returns (int256) {
       int256 usdsPrice = USDS_AGGREGATOR.latestAnswer();
       return _convertUSDSPrice(usdsPrice);
   }
   
```


```

### Recommendation
Consider using latestRoundData and check timestamp is not stale.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BendDAO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-12-benddao-invitational
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-12-benddao-invitational

### Keywords for Search

`vulnerability`

