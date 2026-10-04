---
# Core Classification
protocol: Holograph
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5605
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-holograph-contest
source_link: https://code4rena.com/reports/2022-10-holograph
github_link: https://github.com/code-423n4/2022-10-holograph-findings/issues/322

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - services
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - csanuragjain
  - cccz
  - arcoun
  - Jeiwan
  - Chom
---

## Vulnerability Title

[M-12] Bond tokens (HLG) can get permanently stuck in operator

### Overview


This bug report is about the HolographOperator code in the GitHub repository code-423n4/2022-10-holograph. The bug occurs when the function `HolographOperator.executeJob` is executed by someone who is not an operator, and the time difference is less than 6. In this case, the slashed amount will be assigned to the `msg.sender` regardless if that sender is currently an operator or not. The issue is that if `msg.sender` is not already an operator at the time of executing the job, they cannot become one after to retrieve the reward they got for slashing the primary operator.

To mitigate this issue, it is recommended to either remove the requirement that `_bondedAmounts` need to be 0 prior to bonding and becoming an operator, so that non-operators can get access to the slashing reward by unbonding after, or to add a method to withdraw any `_bondedAmounts` of non-operators. The bug was discovered through manual review.

### Original Finding Content


[HolographOperator.sol#L374-L382](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L374-L382)<br>
[HolographOperator.sol#L849-L857](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L849-L857)<br>

Bond tokens (HLG) equal to the slash amount will get permanently stuck in the HolographOperator each time a job gets executed by someone who is not an (fallback-)operator.

### Proof of Concept

The `HolographOperator.executeJob` function can be executed by anyone after a certain passage of time:

```js
...
if (job.operator != address(0)) {
    ...
    if (job.operator != msg.sender) {
        //perform time and gas price check
        if (timeDifference < 6) {
            // check msg.sender == correct fallback operator
        }
        // slash primary operator
        uint256 amount = _getBaseBondAmount(pod);
        _bondedAmounts[job.operator] -= amount;
        _bondedAmounts[msg.sender] += amount;

        //determine if primary operator retains his job
        if (_bondedAmounts[job.operator] >= amount) {
            ...
        } else {
            ...
        }
    }
}
// execute the job
```

In case `if (timeDifference < 6) {` gets skipped, the slashed amount will be assigned to the `msg.sender` regardless if that sender is currently an operator or not. The problem lies within the fact that if `msg.sender` is not already an operator at the time of executing the job, he cannot become one after, to retrieve the reward he got for slashing the primary operator. This is because the function `HolographOperator.bondUtilityToken` requires `_bondedAmounts` to be 0 prior to bonding and hence becoming an operator:

```js
require(_bondedOperators[operator] == 0 && _bondedAmounts[operator] == 0, "HOLOGRAPH: operator is bonded");
```

### Recommended Mitigation Steps

Assuming that it is intentional that non-operators can execute jobs (which could make sense, so that a user could finish a bridging process on his own, if none of the operators are doing it): remove the requirement that `_bondedAmounts` need to be 0 prior to bonding and becoming an operator so that non-operators can get access to the slashing reward by unbonding after.

Alternatively (possibly preferrable), just add a method to withdraw any `_bondedAmounts` of non-operators.

**[alexanderattar (Holograph) commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/322#issuecomment-1306682172):**
 > Known issue that already has been fixed for the next update.
>
> [Feature/HOLO-605: C4 medium risk fixes](https://github.com/holographxyz/holograph-protocol/pull/88)



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Holograph |
| Report Date | N/A |
| Finders | csanuragjain, cccz, arcoun, Jeiwan, Chom, ctf_sec, Lambda, minhtrng |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-holograph
- **GitHub**: https://github.com/code-423n4/2022-10-holograph-findings/issues/322
- **Contest**: https://code4rena.com/contests/2022-10-holograph-contest

### Keywords for Search

`Business Logic`

