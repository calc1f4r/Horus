---
# Core Classification
protocol: Skale Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13599
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/10/skale-network/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Sergii Kravchenko
  - Shayan Eskandari
---

## Vulnerability Title

Every node gets a full validator’s bounty ✓ Fixed

### Overview


The bug report is about a calculation issue related to the bounty of each validator in the Skale Network. The main change is related to how bounties are calculated for each validator. The problem is that the amount a validator should get is being divided among all nodes, rather than the validator receiving the full amount. The issue is addressed in two pull requests, Bug/skale 3273 formula fix 435 and SKALE-3273 Fix BountyV2 populating error 438. The main changes include deleting the `nodesByValidator` mapping, no longer using the mapping to calculate `_effectiveDelegatedSum` and bounties, and if a validator does not claim their bounty during a month, it being sent to the bounty pool for the next month. The recommendation is that each node should get only their parts of the bounty.

### Original Finding Content

#### Resolution



This issue is addressed in [Bug/skale 3273 formula fix 435](https://github.com/skalenetwork/skale-manager/pull/435) and [SKALE-3273 Fix BountyV2 populating error 438](https://github.com/skalenetwork/skale-manager/pull/438).


The main change is related to how [bounties](https://skale.network/blog/network-bounties-and-delegation-workflow/) are calculated for each validator. Below are a few notes on these pull requests:


* `nodesByValidator` mapping is no longer used in the codebase and the non-zero values are deleted when `calculateBounty()` is called for a specific validator. The mapping is kept in the code for compatible storage layout in upgradable proxies.
* Some functions such as `populate()` was developed for the transition to the upgraded contracts (rewrite `_effectiveDelegatedSum` values based on the new calculation formula). This function is not part of this review and will be removed in the future updates.
* Unlike the old architecture, `nodesByValidator[validatorId]` is no longer used within the system to calculate `_effectiveDelegatedSum` and bounties. This is replaced by using overall staked amount and duration.
* If a validator does not claim their bounty during a month, it is considered as a misbehave and her bounty goes to the bounty pool for the next month.




#### Description


To get the bounty, every node calls the `getBounty` function of the `SkaleManager` contract. This function can be called once per month. The size of the bounty is defined in the `BountyV2` contract in the `_calculateMaximumBountyAmount` function:


**code/contracts/BountyV2.sol:L213-L221**



```
return epochPoolSize
    .add(\_bountyWasPaidInCurrentEpoch)
    .mul(
        delegationController.getAndUpdateEffectiveDelegatedToValidator(
            nodes.getValidatorId(nodeIndex),
            currentMonth
        )
    )
    .div(effectiveDelegatedSum);

```
The problem is that this amount actually represents the amount that should be paid to the validator of that node. But each node will get this amount. Additionally, the amount of validator’s bounty should also correspond to the number of active nodes, while this formula only uses the amount of delegated funds.


#### Recommendation


Every node should get only their parts of the bounty.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Skale Network |
| Report Date | N/A |
| Finders | Sergii Kravchenko, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/10/skale-network/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

