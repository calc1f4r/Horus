---
# Core Classification
protocol: Malt Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16093
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-02-malt-protocol-versus-contest
source_link: https://code4rena.com/reports/2023-02-malt
github_link: https://github.com/code-423n4/2023-02-malt-findings/issues/6

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
  - algo-stables
  - reserve_currency
  - liquid_staking
  - cdp
  - services

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cccz
---

## Vulnerability Title

[M-15] LinearDistributor.declareReward: previouslyVested may update incorrectly, which will cause some rewards to be lost

### Overview


This bug report discusses a vulnerability in the LinearDistributor.declareReward function of the RewardSystem contract. The vulnerability occurs when the reward to distribute, represented by the variable distributed, is calculated using netVest (currentlyVested - previouslyVested). In this case, distributed cannot exceed balance, meaning that if balance is less than linearBondedValue * netVest / vestingBondedValue, part of the rewards in netVest will be lost. 

At the end of the function, previouslyVested is directly assigned to currentlyVested instead of using the Vested adjusted according to distributed, which means that the previously lost rewards will also be skipped in the next distribution. This can lead to a decrease in bufferRequirement, which can increase the number of forfeits. 

A proof of concept is provided in the report, as well as a recommended mitigation step. The recommended step is to adapt previouslyVested based on distributed, as shown in the code snippet provided. 

Overall, this bug report discusses a vulnerability in the LinearDistributor.declareReward function of the RewardSystem contract, and provides a proof of concept and a recommended mitigation step.

### Original Finding Content


In LinearDistributor.declareReward, distributed represents the reward to distribute and is calculated using netVest(currentlyVested - previouslyVested).

At the same time, distributed cannot exceed balance, which means that `if balance < linearBondedValue /ast netVest / vestingBondedValue`, part of the rewards in netVest will be lost.

```solidity
    uint256 netVest = currentlyVested - previouslyVested;
    uint256 netTime = block.timestamp - previouslyVestedTimestamp;

    if (netVest == 0 || vestingBondedValue == 0) {
      return;
    }

    uint256 linearBondedValue = rewardMine.valueOfBonded();

    uint256 distributed = (linearBondedValue * netVest) / vestingBondedValue;
    uint256 balance = collateralToken.balanceOf(address(this));

    if (distributed > balance) {
      distributed = balance;
    }

```

At the end of the function, previouslyVested is directly assigned to currentlyVested instead of using the Vested adjusted according to distributed, which means that the previously lost rewards will also be skipped in the next distribution.

```solidity
    previouslyVested = currentlyVested;
    previouslyVestedTimestamp = block.timestamp;
```

Also, in the next distribution, bufferRequirement will be small because distributed is small, so it may increase the number of forfeits.

        if (netTime < buf) {
          bufferRequirement = (distributed * buf * 10000) / netTime / 10000;
        } else {
          bufferRequirement = distributed;
        }

        if (balance > bufferRequirement) {
          // We have more than the buffer required. Forfeit the rest
          uint256 net = balance - bufferRequirement;
          _forfeit(net);
        }

### Proof of Concept

<https://github.com/code-423n4/2023-02-malt/blob/700f9b468f9cf8c9c5cffaa1eba1b8dea40503f9/contracts/RewardSystem/LinearDistributor.sol#L111-L153>

### Recommended Mitigation Steps

Consider adapting previouslyVested based on distributed:

```diff
    uint256 linearBondedValue = rewardMine.valueOfBonded();

    uint256 distributed = (linearBondedValue * netVest) / vestingBondedValue;
    uint256 balance = collateralToken.balanceOf(address(this));

    if (distributed > balance) {
      distributed = balance;
+    currentlyVested = distributed * vestingBondedValue / linearBondedValue + previouslyVested;
    }
```

**[0xScotch (Malt) confirmed and commented](https://github.com/code-423n4/2023-02-malt-findings/issues/6#issuecomment-1447053148):**
 > Finding is correct as stated. I'm not sure how we would ever get into the state required to manifest the bug. Obviously the implementation is incorrect though, so will be fixed.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Malt Protocol |
| Report Date | N/A |
| Finders | cccz |

### Source Links

- **Source**: https://code4rena.com/reports/2023-02-malt
- **GitHub**: https://github.com/code-423n4/2023-02-malt-findings/issues/6
- **Contest**: https://code4rena.com/contests/2023-02-malt-protocol-versus-contest

### Keywords for Search

`vulnerability`

