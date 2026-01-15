---
# Core Classification
protocol: Liquid Collective
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7010
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation
  - business_logic

protocol_categories:
  - staking_pool
  - liquid_staking
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Optimum
  - Matt Eccentricexit
  - Danyal Ellahi
  - Saw-mon and Natalie
  - Emanuele Ricci
---

## Vulnerability Title

OperatorsRegistry._getNextValidatorsFromActiveOperators can DOS Alluvial staking if there's anoperator with funded==stopped and funded == min(limit, keys)

### Overview


This bug report is about an issue related to the OperatorsRegistry._getNextValidatorsFromActiveOperators function not considering stopped operators when picking a validator. The issue can be reproduced in a scenario where there are two operators, op1 and op2, with different funded and stopped values. The function will always return an empty result, breaking the pickNextValidators mechanism and not being able to stake user's deposited ETH.

To solve this issue, the Alluvial team has recommended the reimplementation of the logic of Operators. _hasFundableKeys and the logic inside the OperatorsRegistry. _getNextValidatorsFromActiveOperators loop to correctly pick the active operator with the higher number of fundable keys without using the stopped attribute. The recommendation has been implemented in SPEARBIT/3 and acknowledged by Spearbit.

### Original Finding Content

## Severity: Critical Risk

## Context
OperatorsRegistry.1.sol#L403-L454

## Description
This issue is also related to `OperatorsRegistry._getNextValidatorsFromActiveOperators` which should not consider stopped when picking a validator.

Consider a scenario where we have:

### Operators
- **Op at index 0**
  - Name: `op1`
  - Active: `true`
  - Limit: `10`
  - Funded: `10`
  - Stopped: `10`
  - Keys: `10`

- **Op at index 1**
  - Name: `op2`
  - Active: `true`
  - Limit: `10`
  - Funded: `0`
  - Stopped: `0`
  - Keys: `10`

In this case:
- Op1 got all 10 keys funded and exited. Because it has `keys=10` and `limit=10`, it means that it has no more keys to get funded again.
- Op2 instead has still 10 approved keys to be funded.

Because of how the selection of the picked validator works:

```solidity
uint256 selectedOperatorIndex = 0;
for (uint256 idx = 1; idx < operators.length;) {
    if (
        operators[idx].funded - operators[idx].stopped <
        operators[selectedOperatorIndex].funded - operators[selectedOperatorIndex].stopped
    ) {
        selectedOperatorIndex = idx;
    }
    unchecked {
        ++idx;
    }
}
```

When the function finds an operator with `funded == stopped`, it will pick that operator because `0 < operators[selectedOperatorIndex].funded - operators[selectedOperatorIndex].stopped`.

After the loop ends, `selectedOperatorIndex` will be the index of an operator that has no more validators to be funded (for this scenario). Because of this, the following code:

```solidity
uint256 selectedOperatorAvailableKeys = Uint256Lib.min(
    operators[selectedOperatorIndex].keys,
    operators[selectedOperatorIndex].limit
) - operators[selectedOperatorIndex].funded;
```

When executed on Op1, it will set `selectedOperatorAvailableKeys = 0` and as a result, the function will return `return (new bytes[](0), new bytes[](0));`.

In this scenario when `stopped == funded` and there are no keys available to be funded (`funded == min(limit, keys)`), the function will always return an empty result, breaking the `pickNextValidators` mechanism that won't be able to stake user's deposited ETH anymore, even if there are operators with fundable validators.

Check the Appendix for a test case to reproduce this issue.

## Recommendation
Alluvial should:
- Reimplement the logic of `Operators._hasFundableKeys` that should select only active operators with fundable keys without using the `stopped` attribute.
- Reimplement the logic inside the `OperatorsRegistry._getNextValidatorsFromActiveOperators` loop to correctly pick the active operator with the higher number of fundable keys without using the `stopped` attribute.

**Alluvial:** Recommendation implemented in SPEARBIT/3.  
**Spearbit:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Liquid Collective |
| Report Date | N/A |
| Finders | Optimum, Matt Eccentricexit, Danyal Ellahi, Saw-mon and Natalie, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Business Logic`

