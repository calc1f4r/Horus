---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53559
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Lack of Whitelist Validation in addStrategiesToOperatorSet()

### Overview

See description below for full details.

### Original Finding Content

## Description

The `addStrategiesToOperatorSet()` function does not validate whether the strategies being added to an operator set are whitelisted on **StrategyManager**. This allows AVSs to add arbitrary strategies to an operator set.

## AllocationManager.sol::addStrategiesToOperatorSet()

```solidity
function addStrategiesToOperatorSet(
    address avs,
    uint32 operatorSetId,
    IStrategy[] calldata strategies
) external checkCanCall(avs) {
    OperatorSet memory operatorSet = OperatorSet(avs, operatorSetId);
    bytes32 operatorSetKey = operatorSet.key();
    require(_operatorSets[avs].contains(operatorSet.id), InvalidOperatorSet());
    for (uint256 i = 0; i < strategies.length; i++) {
        // @audit no validation of whether the strategy is whitelisted
        require(_operatorSetStrategies[operatorSetKey].add(address(strategies[i])), StrategyAlreadyInOperatorSet());
        emit StrategyAddedToOperatorSet(operatorSet, strategies[i]);
    }
}
```

## Recommendations

Consider validating that each strategy has been approved by **StrategyManager** to prevent arbitrary strategies from being added to an operator set.

## Resolution

The Eigenlayer team has acknowledged the issue with the following comment:
> "Whitelisting is primarily concerned with deposits on the StrategyManager side. While this finding is valid, we feel it’s more trouble than it’s worth to add this check to the AllocationManager."

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf

### Keywords for Search

`vulnerability`

