---
# Core Classification
protocol: Liquid Collective
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16364
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective3-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective3-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
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
  - Xiaoming90
  - Saw-Mon and Natalie
  - Optimum
  - Matt Eccentricexit
  - Danyal Ellahi
---

## Vulnerability Title

_pickNextValidatorsToExitFromActiveOperators uses the wrong index to query stopped validator count for operators

### Overview


This bug report is about an issue in the OperatorsRegistry.1.sol#L628 file. The issue occurs when querying the stopped validator counts in the In_pickNextValidatorsToExitFromActiveOperators function. The problem is that the operators array in memory does not necessarily have the same order as the actual OperatorsV2's operators. This is because the ones that don't have _hasExitableKeys will be skipped. Therefore, when querying the stopped validator counts, the index of the cached operator's array should be used, rather than the idx. The recommendation is to correct the calculation for currentStoppedCount to use operators[idx].index. Additionally, test cases should be added for the _pickNextValidatorsToExitFromActiveOperators function. The issue was fixed in the commit a109a1 and verified by Spearbit.

### Original Finding Content

## Severity: Critical Risk

**Context:** OperatorsRegistry.1.sol#L628

**Description:**  
In `pickNextValidatorsToExitFromActiveOperators`, `OperatorsV2.CachedOperator[] memory operators` does not necessarily have the same order as the actual `OperatorsV2`'s operators, since the ones that don't have `_hasExitableKeys` will be skipped (the operator might not be active or all of its funded keys might have been requested to exit). 

When querying the stopped validator counts:

```solidity
for (uint256 idx = 0; idx < exitableOperatorCount;) {
    uint32 currentRequestedExits = operators[idx].requestedExits;
    uint32 currentStoppedCount = _getStoppedValidatorsCountFromRawArray(stoppedValidators, idx);
}
```

One should not use the `idx` in the cached operator's array, but the cached index of this array element, as the indexes of `stoppedValidators` correspond to the actual stored operator's array in storage. Note that when emitting the `UpdatedRequestedValidatorExitsUponStopped` event, the correct index has been used.

**Recommendation:**  
The calculation for `currentStoppedCount` needs to be corrected to use `operators[idx].index`:

```solidity
uint32 currentStoppedCount = _getStoppedValidatorsCountFromRawArray(stoppedValidators, operators[idx].index);
```

Also, since this was not caught by test cases, it would be best to add some passing and failing test cases for `pickNextValidatorsToExitFromActiveOperators`.

**Liquid Collective:** Fixed in commit a109a1.  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Liquid Collective |
| Report Date | N/A |
| Finders | Xiaoming90, Saw-Mon and Natalie, Optimum, Matt Eccentricexit, Danyal Ellahi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective3-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective3-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

