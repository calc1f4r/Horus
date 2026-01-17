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
solodit_id: 28146
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#6-unnecessary-actions
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

Unnecessary actions

### Overview


This bug report is about a software code issue in the Lido-Dao project. The code is located at the lines 141-157, 166, 178 and 189. The issue is that when a variable does not change its value, it is not necessary to make a call to a certain function and record an event. 

To resolve the issue, the code needs to be changed. Specifically, at lines 141-145, a check needs to be added to make sure the value of the variable does not remain the same. Additionally, the use of the “if” operator must be removed from line 146. Similarly, checks need to be added at lines 166, 178 and 189 to make sure the values of the variables do not remain the same. 

In summary, the bug report is about a software code issue in the Lido-Dao project. To resolve the issue, the code needs to be changed by adding checks to make sure the values of the variables do not remain the same, and by removing the use of the “if” operator from line 146.

### Original Finding Content

##### Description
At the lines 
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.4.24/nos/NodeOperatorsRegistry.sol#L141-L157 there's a call to the `setNodeOperatorActive()` function to set the value of the `operators[_id].active` variable to `_active`.
However, if the value of the variable does not change, you do not need to make a call to the `_increaseKeysOpIndex()` function and record the `NodeOperatorActiveSet` event.
Before line 145, add the following check:
```
    require(operators[_id].active != _active, "SAME_VALUE");
```
And it will be necessary to remove the use of the `if` operator on line 146.   

At the line  
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.4.24/nos/NodeOperatorsRegistry.sol#L166 you need to add a check like this:
```
    require(operators[_id].name != _name, "SAME_VALUE");
```

At the line 
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.4.24/nos/NodeOperatorsRegistry.sol#L178 you need to add a check like this:
```
    require(operators[_id].rewardAddress != _rewardAddress, "SAME_VALUE");
```

At the line 
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.4.24/nos/NodeOperatorsRegistry.sol#L189 you need to add a check like this:
```
    require(operators[_id].stakingLimit != _stakingLimit, "SAME_VALUE");
```

##### Recommendation
The source code needs to be changed.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#6-unnecessary-actions
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

