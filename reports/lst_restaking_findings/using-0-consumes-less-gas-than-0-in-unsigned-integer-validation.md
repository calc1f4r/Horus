---
# Core Classification
protocol: Aura Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50557
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/aura-finance/aura-finance-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/aura-finance/aura-finance-smart-contract-security-assessment
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

USING != 0 CONSUMES LESS GAS THAN > 0 IN UNSIGNED INTEGER VALIDATION

### Overview

See description below for full details.

### Original Finding Content

##### Description

In the `require` statements below, `> 0` was used to validate if the unsigned integer parameters are bigger than 0. It is known that, using `!= 0` costs less gas than `> 0`.

Code Location
-------------

`aura-contracts/AuraBalRewardPool.sol`

* Line 121 `require(_amount > 0, "RewardPool : Cannot stake 0");`
* Line 139 `require(_amount > 0, "RewardPool : Cannot stake 0");`
* Line 157 `require(amount > 0, "RewardPool : Cannot withdraw 0");`
* Line 232 `require(rewardsAvailable > 0, "!balance");`

`aura-contracts/AuraLocker.sol`

* Line 236 `require(rewardData[_rewardsToken].lastUpdateTime > 0, ...`
* Line 285 `require(_amount > 0, "Cannot stake 0");`
* Line 399 `require(amt > 0, "Nothing locked");`
* Line 425 `require(length > 0, "no locks");`
* Line 471 `require(locked > 0, "no exp locks");`
* Line 511 `require(len > 0, "Nothing to delegate");`
* Line 862 `require(_rewards > 0, "No reward");`

`aura-contracts/AuraMerkleDrop.sol`

* Line 139 `require(_amount > 0, "!amount");`

`aura-contracts/AuraPenaltyForwarder.sol`

* Line 55 `require(bal > 0, "!empty");`

`aura-contracts/AuraVestedEscrow.sol`

* Line 55 `require(totalLocked[_recipient] > 0, "!funding");`

`aura-contracts/BalLiquidityProvider.sol`

* Line 74 `require(balAfter > 0, "!mint");`

`aura-contracts/ExtraRewardsDistributor.sol`

* Line 104 `require(_amount > 0, "!amount");`
* Line 180 `require(_index > 0 && ...);`

`aura-contracts/RewardPoolDepositWrapper.sol`

* Line 51 `require(minted > 0, "!mint");``

`convex-platform/BaseRewardPool.sol`

* Line 215 `require(_amount > 0, 'RewardPool : Cannot stake 0');`
* Line 231 `require(amount > 0, 'RewardPool : Cannot withdraw 0');`

`convex-platform/ConvexMasterChef.sol`

* Line 138 `require(totalAllocPoint > 0, "!alloc");`

`convex-platform/CrvDepositor.sol`

* Line 169 `require(_amount > 0,"!>0");`

`convex-platform/PoolManagerSecondaryProxy.sol`

* Line 104 `require(weight > 0, "must have weight");`

`convex-platform/interfaces/BoringMath.sol`

* Line 20 `require(b > 0, "BoringMath: division by zero");`
* Line 102 `require(b > 0, "BoringMath: division by zero");`
* Line 123 `require(b > 0, "BoringMath: division by zero");`
* Line 143 `require(b > 0, "BoringMath: division by zero");`

For example, based on the following test contract:

#### GasTestRequire.sol

```
//SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

contract GasTestRequire {
    function originalrequire(uint256 len) public {
        require(len > 0, "Error!");
    }
    function optimalizedrequire(uint256 len) public {
        require(len != 0, "Error!");
    }
}

```

We can see the difference in gas costs:

![require.png](https://halbornmainframe.com/proxy/audits/images/659e8b9aa1aa3698c0e9d9ed)

##### Score

Impact: 1  
Likelihood: 1

##### Recommendation

**ACKNOWLEDGED**: The `Aura Finance team` acknowledged this finding and does not plan to correct it in the future to keep the difference between Aura and Convex as minimal as possible to aid in manual reviews and minimize the chance of introducing bugs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Aura Finance |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/aura-finance/aura-finance-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/aura-finance/aura-finance-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

