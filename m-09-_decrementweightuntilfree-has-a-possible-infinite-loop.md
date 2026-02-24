---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26078
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/735

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
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - tsvetanovv
  - bin2chen
  - Audinarey
  - SpicyMeatball
---

## Vulnerability Title

[M-09] `_decrementWeightUntilFree()` has a possible infinite loop

### Overview


A bug report has been submitted for a code snippet in the `_decrementWeightUntilFree()` method. The position of `i++` is wrong, which may lead to an infinite loop. This is because when `userGaugeWeight == 0`, `i` is not incremented. The current protocol does not restrict `getUserGaugeWeight[user][gauge] == 0`. The recommended mitigation step is to move the `i++` outside the if statement, to ensure that `i` is incremented regardless of the value of `userGaugeWeight`. This bug was confirmed by 0xLightt (Maia) and was addressed in the code.

### Original Finding Content


### Proof of Concept

In the loop of the `_decrementWeightUntilFree()` method, the position of `i++` is wrong, which may lead to an infinite loop.

```solidity
    function _decrementWeightUntilFree(address user, uint256 weight) internal nonReentrant {
...
        for (uint256 i = 0; i < size && (userFreeWeight + totalFreed) < weight;) {
            address gauge = gaugeList[i];
            uint112 userGaugeWeight = getUserGaugeWeight[user][gauge];
            if (userGaugeWeight != 0) {
                // If the gauge is live (not deprecated), include its weight in the total to remove
                if (!_deprecatedGauges.contains(gauge)) {
                    totalFreed += userGaugeWeight;
                }
                userFreed += userGaugeWeight;
                _decrementGaugeWeight(user, gauge, userGaugeWeight, currentCycle);
                unchecked {
@>                  i++;
                }
            }
        }
```

In the above code, when `userGaugeWeight == 0`, `i` is not incremented, resulting in a infinite loop. The current protocol does not restrict `getUserGaugeWeight[user][gauge] == 0`.

### Recommended Mitigation Steps

```solidity
    function _decrementWeightUntilFree(address user, uint256 weight) internal nonReentrant {
...
        for (uint256 i = 0; i < size && (userFreeWeight + totalFreed) < weight;) {
            address gauge = gaugeList[i];
            uint112 userGaugeWeight = getUserGaugeWeight[user][gauge];
            if (userGaugeWeight != 0) {
                // If the gauge is live (not deprecated), include its weight in the total to remove
                if (!_deprecatedGauges.contains(gauge)) {
                    totalFreed += userGaugeWeight;
                }
                userFreed += userGaugeWeight;
                _decrementGaugeWeight(user, gauge, userGaugeWeight, currentCycle);
-               unchecked {
-                  i++;
-               }
            }
+           unchecked {
+             i++;
+           }            
        }
```

### Assessed type

Context

**[0xLightt (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/735#issuecomment-1655670401)**

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/735#issuecomment-1708804582):**
 > Addressed [here](https://github.com/Maia-DAO/eco-c4-contest/tree/735).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | tsvetanovv, bin2chen, Audinarey, SpicyMeatball |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/735
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

