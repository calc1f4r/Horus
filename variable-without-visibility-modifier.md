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
solodit_id: 28148
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#8-variable-without-visibility-modifier
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

Variable without visibility modifier

### Overview


This bug report concerns the variable `guardianIndicesOneBased` in the DepositSecurityModule.sol file. The issue is that the variable does not have a visibility modifier, meaning it is not clear which visibility modifier is default. It is recommended to set the visibility modifier to `internal` to make it clear. This can be done by adding the code `mapping(address => uint256) internal guardianIndicesOneBased; // 1-based` to the DepositSecurityModule.sol file.

### Original Finding Content

##### Description
Variable [`guardianIndicesOneBased` hasn't visibiltity modifier](https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.8.9/DepositSecurityModule.sol#L61). It is not clear which visibility modifier is default.
##### Recommendation
It is recommended to set visibility to `internal`
```solidity
    mapping(address => uint256) internal guardianIndicesOneBased; // 1-based
```

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#8-variable-without-visibility-modifier
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

