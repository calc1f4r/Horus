---
# Core Classification
protocol: veToken Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6129
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-vetoken-finance-contest
source_link: https://code4rena.com/reports/2022-05-vetoken
github_link: https://github.com/code-423n4/2022-05-vetoken-findings/issues/120

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
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - shenwilly
  - sseefried
---

## Vulnerability Title

[M-08] Not updating `totalWeight` when operator is removed in `VeTokenMinter`

### Overview


This bug report is about a vulnerability in the VeTokenMinter and Booster contracts. The vulnerability is that when the removeOperator function is called on VeTokenMinter, the totalWeight state variable is not reduced, resulting in remaining operators not receiving a fair share of the total rewards and a portion of the rewards not being given out at all. To demonstrate the bug, an example is provided where Operator 1 is added with weight 9, and Operator 2 is added with weight 1, resulting in a totalWeight of 10. When Operator 1 is removed, 90% of the reward is no longer minted and distributed, which is unfair to the remaining operators. The bug was found using manual inspection. The recommended mitigation steps are to reduce the totalWeight so that the remaining operators receive a fair share of the total rewards, or rewrite the removeOperator function and modify addOperator so that a weight can be provided as an extra argument.

### Original Finding Content

_Submitted by sseefried, also found by shenwilly_

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/contracts/VeTokenMinter.sol#L36-L38>

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/contracts/VeTokenMinter.sol#L41-L4>

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/contracts/Booster.sol#L598-L614>

### Impact

The `totalWeight` state variable of the `VeTokenMinter` contract is used to work out the amount of `veAsset` earned when the `Booster.rewardClaimed` function is called.

However, while `totalWeight` is modified inside the `VeTokenMinter` contract when function `updateveAssetWeight` is called, the `totalWeight` is not similarly reduced when function `removeOperator` is called.

The impact is that remaining operators do not receive a fair share of the total rewards and a portion of the rewards are not given out at all.

### Proof of Concept

*   Operator 1 is added with weight 9
*   Operator 2 is added with weight 1

The `totalWeight` is now 10.

This means that Operator 1 receives 90% of the amount while Operator 2 receives 10%.

If we then call `removeOperator` on Operator 1 then 90% of the reward is no longer minted and distributed. This is unfair to the remaining operators.

The can be seen on lines [607 - 608](https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/contracts/Booster.sol#L607-L608) of the `Booster` contract. Function `rewardClaimed` will never be called for (removed) Operator 1. But for Operator 2 they will still receive 10% of the rewards even though Operator 1 is no longer registered in the system.

### Recommended Mitigation Steps

The `totalWeight` should be reduced so that the remaining operators receive a fair share of the total rewards.

Using just method calls from `VeTokenMinter` one could rectify this situation by

*   adding the removed operator with `addOperator`
*   setting the weight to `0` using `updateveAssetWeight`. This will have the effect of reducing the `totalWeight` by the right amount.
*   removing the operator again using `removeOperator`

However, the `removeOperator` function should just be rewritten to be as follows:

```
function removeOperator(address _operator) public onlyOwner {
    totalWeight -= veAssetWeights[_operator];
    veAssetWeights[_operator] = 0;
    operators.remove(_operator);
}
```

You might also want to modify `addOperator` so that a weight can be provided as an extra argument. This saves having to call `addOperator` and then `updateveAssetWeight` which could save on gas.

**[solvetony (veToken Finance) disagreed with severity and commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/120#issuecomment-1156643912):**
 > Confirmed. But this should be a middle risk. 

**[Alex the Entreprenerd (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/120#issuecomment-1193397795):**
 > The warden has shown how, due to a privileged call, removing an operator, the weight used to distribute rewards will not be updated fairly. 
> This will cause an improper distribution of rewards.
> 
> Because the finding is limited to Loss of Yield, due to Admin Configuration, I believe Medium Severity to be more appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | veToken Finance |
| Report Date | N/A |
| Finders | shenwilly, sseefried |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-vetoken
- **GitHub**: https://github.com/code-423n4/2022-05-vetoken-findings/issues/120
- **Contest**: https://code4rena.com/contests/2022-05-vetoken-finance-contest

### Keywords for Search

`vulnerability`

