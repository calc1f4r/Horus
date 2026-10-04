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
solodit_id: 28144
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#4-possible-blocking-of-work-with-buffered-eth
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

Possible blocking of work with buffered ETH

### Overview


A bug has been discovered in the code of the Lido DAO project. The function `addSigningKeysOperatorBH()` can be called from any address of operators, which increases the value of `KEYS_OP_INDEX_POSITION`. This can be used to block the operation of `depositBufferedEther()` which is not safe. It is recommended to add a restriction on the call to the `addSigningKeysOperatorBH()` function or remove it from the source code altogether.

### Original Finding Content

##### Description
At the lines 
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.4.24/nos/NodeOperatorsRegistry.sol#L252-L262 there's a function `addSigningKeysOperatorBH()`.
This function can be called from any address of operators `[_operator_id].rewardAddress`.
Calling this function increments the value of `KEYS_OP_INDEX_POSITION`. And the current value of `KEYS_OP_INDEX_POSITION` is used here:
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.8.9/DepositSecurityModule.sol#L413-L414.
Thus, any operator (and inactive too) can block the operation of `depositBufferedEther()`.
However, it is safe to do the same with the `addSigningKeys()` function, which can only be called by special users.
##### Recommendation
It is necessary to add a restriction on the call to the `addSigningKeysOperatorBH()` function or remove it from the source code altogether.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#4-possible-blocking-of-work-with-buffered-eth
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

