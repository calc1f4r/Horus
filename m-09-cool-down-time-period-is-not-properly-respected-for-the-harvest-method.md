---
# Core Classification
protocol: Popcorn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22006
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-popcorn
source_link: https://code4rena.com/reports/2023-01-popcorn
github_link: https://github.com/code-423n4/2023-01-popcorn-findings/issues/558

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
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 16
finders:
  - Ch\_301
  - rbserver
  - Hawkeye
  - bin2chen
  - peakbolt
---

## Vulnerability Title

[M-09] cool down time period is not properly respected for the `harvest` method

### Overview


This bug report is about a vulnerability in the `Vault` of the RedVeil (Popcorn) project. The vulnerability is caused by the cool down period for the strategy harvest callback method not being properly respected. This means that on every deposit/withdraw into the `Vault`, the strategy is called every time, which can lead to unintended consequences. 

The main problem is that the `lastHarvest` state variable is only set in the constructor and not updated on strategy harvest method execution. To fix this issue, the `lastHarvest` state variable should be updated when the strategy harvest method is executed. 

The bug has been confirmed by the RedVeil (Popcorn) team and the recommended mitigation steps are provided in the report.

### Original Finding Content


<https://github.com/code-423n4/2023-01-popcorn/blob/d95fc31449c260901811196d617366d6352258cd/src/vault/adapter/abstracts/AdapterBase.sol#L86> 

<https://github.com/code-423n4/2023-01-popcorn/blob/d95fc31449c260901811196d617366d6352258cd/src/vault/adapter/abstracts/AdapterBase.sol#L438-L450>

### Vulnerability details

Harvest method is called on every deposit or withdraw into the `Vault` which further calls into the provided strategy.

This calling into strategy is limited by the cool down period. But in the current implementation is not properly respected.

### Impact

Setting the cool down period for a strategy harvest callback method is not working properly so that on every deposit/withdraw into `Vault` also the strategy is called every time.

### Proof of Concept

The main problem is that `lastHarvest` state variable is only set in the constructor:

<https://github.com/code-423n4/2023-01-popcorn/blob/d95fc31449c260901811196d617366d6352258cd/src/vault/adapter/abstracts/AdapterBase.sol#L86>

and is not updated on strategy harvest method execution in the following lines:

<https://github.com/code-423n4/2023-01-popcorn/blob/d95fc31449c260901811196d617366d6352258cd/src/vault/adapter/abstracts/AdapterBase.sol#L438-L450>

### Recommended Mitigation Steps

For the cool down period to work correctly, update tha `lastHarvest` state variable like this:

```diff
    function harvest() public takeFees {
        if (
            address(strategy) != address(0) &&
            ((lastHarvest + harvestCooldown) < block.timestamp)
        ) {
+
+           lastHarvest = block.timestamp;
+
            // solhint-disable
            address(strategy).delegatecall(
                abi.encodeWithSignature("harvest()")
            );
        }

        emit Harvested();
    }
```

**[RedVeil (Popcorn) confirmed](https://github.com/code-423n4/2023-01-popcorn-findings/issues/558)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Popcorn |
| Report Date | N/A |
| Finders | Ch\_301, rbserver, Hawkeye, bin2chen, peakbolt, ladboy233, Ruhum, 7siech, Walter, Malatrax, KIntern\_NA, thecatking, hansfriese, imare, rvierdiiev, eccentricexit |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-popcorn
- **GitHub**: https://github.com/code-423n4/2023-01-popcorn-findings/issues/558
- **Contest**: https://code4rena.com/reports/2023-01-popcorn

### Keywords for Search

`vulnerability`

