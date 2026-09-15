---
# Core Classification
protocol: UMA DVM 2.0 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10449
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-dvm-2-0-audit/
github_link: none

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
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Stake can be withheld indefinitely

### Overview


The Staker contract in UMAprotocol has a function called setUnstakeCoolDown that allows the contract owner to set the unstakeCoolDown variable to an arbitrarily large uint64 value. This variable controls the time that needs to pass between successful calls to requestUnstake and executeUnstake and retroactively applies changes to all users currently within the cooldown phase. This could be abused by the contract owner to make it practically impossible for users to retrieve their stake, which violates the trust assumptions typically present in a staking system. 

The intended use of this contract is to be owned by the GovernorV2 contract, which would allow affected stakers to control the unstakeCoolDown through governance proposals. However, voters who disagree with a majority vote to extend unstakeCoolDown will not be able to leave the staking system before the changes take effect.

To address this issue, UMA suggested validating the input of the setUnstakeCoolDown function against an acceptable maximum cooldown time and allowing the retroactive application of a new unstakeCoolDown value only in cases when it acts to decrease the cooldown time of users who are actively unstaking. However, UMA concluded that the increased complexity and gas cost of the suggested recommendation does not appear justified due to the economic incentives between stakeholders.

### Original Finding Content

In the [`Staker`](https://github.com/UMAprotocol/protocol/blob/7938617bf79854811959eb605237edf6bdccbc90/packages/core/contracts/oracle/implementation/Staker.sol) contract the function [`setUnstakeCoolDown`](https://github.com/UMAprotocol/protocol/blob/7938617bf79854811959eb605237edf6bdccbc90/packages/core/contracts/oracle/implementation/Staker.sol#L243) allows the contract owner to set the `unstakeCoolDown` variable to an arbitrarily large `uint64` value. This variable controls the time that needs to pass between successful calls to `requestUnstake` and `executeUnstake`. It retroactively applies changes to all users currently within the cooldown phase.


Giving the contract owner full control over setting `unstakeCoolDown` violates the trust assumptions typically present in a staking system. Namely, stakers expect to be able to retrieve their stake regardless of operator error or operator malice. Setting `unstakeCoolDown` to a very large value would render each user’s stake practically unretrievable.


The intended use of this contract is to be owned by the `GovernorV2` contract thereby allowing the affected stakers to control the `unstakeCoolDown` through governance proposals, which reduce the likelihood of malice. However, voters who disagree with a legitimate majority vote to extend `unstakeCoolDown` will most likely not be able to leave the staking system before the changes take effect.


Consider validating the input of the `setUnstakeCoolDown` function against an acceptable maximum cooldown time. Also consider allowing the retroactive application of a new `unstakeCoolDown` value only in cases when it acts to decrease the cooldown time of users who are actively unstaking.


**Update:** *Acknowledged. UMA indicated that the economic incentives between stakeholders make this scenario unlikely. The increased complexity and gas cost of the suggested recommendation does not appear justified.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UMA DVM 2.0 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uma-dvm-2-0-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

