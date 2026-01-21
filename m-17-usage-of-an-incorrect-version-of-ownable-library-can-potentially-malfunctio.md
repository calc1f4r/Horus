---
# Core Classification
protocol: Hubble
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42482
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-02-hubble
source_link: https://code4rena.com/reports/2022-02-hubble
github_link: https://github.com/code-423n4/2022-02-hubble-findings/issues/140

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
  - services
  - derivatives
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-17] Usage of an incorrect version of Ownable library can potentially malfunction all `onlyOwner` functions

### Overview


The current implementation of the code is using a non-upgradeable version of the Ownable library, which means that the deployer becomes the default owner in the constructor. However, this is not compatible with the proxy-based upgradeability system, which does not allow constructors to be used in upgradeable contracts. This results in there being no owner when the contract is deployed as a proxy contract. To fix this issue, it is recommended to use the upgradeable version of the Ownable library and the Initializable library. Additionally, the __Ownable_init(); function should be added at the beginning of the initializer. This bug affects the Oracle and AMM contracts.

### Original Finding Content

_Submitted by robee_

The current implementaion is using a non-upgradeable version of the Ownable library. Instead of the upgradeable version: @openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol.

A regular, non-upgradeable Ownable library will make the deployer the default owner in the constructor. Due to a requirement of the proxy-based upgradeability system, no constructors can be used in upgradeable contracts. Therefore, there will be no owner when the contract is deployed as a proxy contract

### Recommended Mitigation Steps

Use @openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol and @openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol instead.

And add __Ownable_init(); at the beginning of the initializer.
    
Oracle.sol<br>
AMM.sol



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Hubble |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-hubble
- **GitHub**: https://github.com/code-423n4/2022-02-hubble-findings/issues/140
- **Contest**: https://code4rena.com/reports/2022-02-hubble

### Keywords for Search

`vulnerability`

