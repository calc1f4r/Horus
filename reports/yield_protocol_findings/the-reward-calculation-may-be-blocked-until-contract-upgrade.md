---
# Core Classification
protocol: KelpDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30473
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#4-the-reward-calculation-may-be-blocked-until-contract-upgrade
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

The reward calculation may be blocked until contract upgrade

### Overview


The `NodeDelegator.initiateWithdrawRewards()` function currently has a bug where it will stop working if the EigenPod balance is over 16 ETH. This is not intended and should be fixed so that rewards can still be calculated and withdrawn. It is important to find a permanent solution for this issue to prevent rewards from being blocked in the future.

### Original Finding Content

##### Description
Currently, the `NodeDelegator.initiateWithdrawRewards()` will [revert](https://github.com/Kelp-DAO/LRT-rsETH/blob/e75e9ef168a7b192abf76869977cd2ac8134849c/contracts/NodeDelegator.sol#L232) if the balance of the EigenPod exceeds 16 ETH. This is intended to distinguish between the staking rewards and the stake withdrawal.

It is expected that rewards will be less than 16 ETH; otherwise, something unexpected has occurred (i.e., the validator initiated the withdrawal) and should be resolved manually. It is an ad-hoc temporary solution that will require a contract upgrade by design.

This finding is rated HIGH as the reward calculation may be blocked until a manual contract upgrade.
##### Recommendation
We recommend developing and upgrading to a long-term solution that does not lead to the freezing of the rewards.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | KelpDAO |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#4-the-reward-calculation-may-be-blocked-until-contract-upgrade
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

