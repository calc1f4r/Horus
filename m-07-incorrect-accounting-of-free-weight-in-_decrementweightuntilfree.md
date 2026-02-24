---
# Core Classification
protocol: Tribe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2073
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-xtribe-contest
source_link: https://code4rena.com/reports/2022-04-xtribe
github_link: https://github.com/code-423n4/2022-04-xtribe-findings/issues/61

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
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - gzeon
---

## Vulnerability Title

[M-07] Incorrect accounting of free weight in `_decrementWeightUntilFree`

### Overview


This bug report is about an issue with the '_decrementWeightUntilFree' function in the 'ERC20Gauges.sol' file on the 'flywheel-v2' GitHub repository. The issue is that when calculating the free weight, the code unnecessarily takes into account non-deprecated gauges, leading to incorrect accounting of free weight. 

To explain this in more detail, consider an example of Alice allocating 3 weight to gauge D, gauge A, and gauge B equally, where gauge D is deprecated. If Alice calls the '_decrementWeightUntilFree' function with a weight of 2, all 3 gauges will be freed, as the non-deprecated criteria is unnecessary. However, if Alice calls the function with a weight of 1, only 2 gauges will be freed. 

The recommended mitigation step is to not treat deprecated gauges separately.

### Original Finding Content

_Submitted by gzeon_

In `_decrementWeightUntilFree`, the free weight is calculated by `balanceOf[user] - getUserWeight[user]` plus weight freed from non-deprecated gauges. The non-deprecated criteria is unnecessary and lead to incorrect accounting of free weight.

### Proof of Concept

[ERC20Gauges.sol#L547-L583](https://github.com/fei-protocol/flywheel-v2/blob/77bfadf388db25cf5917d39cd9c0ad920f404aad/src/token/ERC20Gauges.sol#L547-L583)<br>

        function _decrementWeightUntilFree(address user, uint256 weight) internal {
            uint256 userFreeWeight = balanceOf[user] - getUserWeight[user];

            // early return if already free
            if (userFreeWeight >= weight) return;

            uint32 currentCycle = _getGaugeCycleEnd();

            // cache totals for batch updates
            uint112 userFreed;
            uint112 totalFreed;

            // Loop through all user gauges, live and deprecated
            address[] memory gaugeList = _userGauges[user].values();

            // Free gauges until through entire list or under weight
            uint256 size = gaugeList.length;
            for (uint256 i = 0; i < size && (userFreeWeight + totalFreed) < weight; ) {
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
                        i++;
                    }
                }
            }

            getUserWeight[user] -= userFreed;
            _writeGaugeWeight(_totalWeight, _subtract, totalFreed, currentCycle);
        }

Consider Alice allocated 3 weight to gauge D, gauge A and gauge B equally where gauge D is depricated

1.  Alice call \_decrementWeightUntilFree(alice, 2)
2.  userFreeWeight = 0
3.  gauge D is freed, totalFreed = 0, userFreed = 1
4.  (userFreeWeight + totalFreed) < weight, continue to free next gauge
5.  gauge A is freed, totalFreed = 1, userFreed = 2
6.  (userFreeWeight + totalFreed) < weight, continue to free next gauge
7.  gauge B is freed, totalFreed = 2, userFreed = 3
8.  All gauge is freed

Alternatively, Alice can

1.  Alice call \_decrementWeightUntilFree(alice, 1)
2.  userFreeWeight = balanceOf\[alice] - getUserWeight\[alice] = 3 - 3 = 0
3.  gauge D is freed, totalFreed = 0, userFreed = 1
4.  (userFreeWeight + totalFreed) < weight, continue to free next gauge
5.  gauge A is freed, totalFreed = 1, userFreed = 2
6.  (userFreeWeight + totalFreed) >= weight, break
7.  getUserWeight\[alice] -= totalFreed
8.  Alice call \_decrementWeightUntilFree(alice, 2)
9.  userFreeWeight = balanceOf\[alice] - getUserWeight\[alice] = 3 - 1 = 2
10. (userFreeWeight + totalFreed) >= weight, break
11. Only 2 gauge is freed

### Recommended Mitigation Steps

No need to treat deprecated gauge separately.

**[Joeysantoro (xTRIBE) confirmed and commented](https://github.com/code-423n4/2022-04-xtribe-findings/issues/61#issuecomment-1125550837):**
 > This appears correct. Would be for a Tribe dev to validate with a test that certain paths could brick create this incorrect accounting.



***





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tribe |
| Report Date | N/A |
| Finders | gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-xtribe
- **GitHub**: https://github.com/code-423n4/2022-04-xtribe-findings/issues/61
- **Contest**: https://code4rena.com/contests/2022-04-xtribe-contest

### Keywords for Search

`vulnerability`

