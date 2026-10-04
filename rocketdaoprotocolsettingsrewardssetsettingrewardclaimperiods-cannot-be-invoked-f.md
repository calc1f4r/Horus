---
# Core Classification
protocol: Rocket Pool (Houston)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32006
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/12/rocket-pool-houston/
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
finders_count: 2
finders:
  - Dominik Muhs
  -  Valentin Quelquejay

---

## Vulnerability Title

RocketDAOProtocolSettingsRewards.setSettingRewardClaimPeriods() Cannot Be Invoked ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



The client acknowledged this issue and let us know that this setting was meant to be adjustable via the `setSettingUint()` function. Consequently, the redundant setter has been removed in commit `01897ca410ed2ef18f21818f68bb1d73af4fbe69`.


#### Description


The `setSettingRewardClaimPeriods()` function in `RocketDAOProtocolSettingsRewards.sol` currently serves no practical purpose as it cannot be invoked. This limitation arises because the only contract permitted to call this function is `RocketDAOProtocolProposals`, which does not expose this specific functionality. While the setting can still be altered using the `proposalSettingUint` setter in `RocketDAOProtocolProposal`, it is assumed that the `setSettingRewardClaimPeriods` function was intended for added clarity and ease of use.


**contracts/contract/dao/protocol/settings/RocketDAOProtocolSettingsRewards.sol:L46**



```
setUint(keccak256(abi.encodePacked(settingNameSpace, "rewards.claims", "periods")), _periods);

```
#### Recommendation


To make this function useful and align it with its intended purpose, we recommend integrating its functionality into `RocketDAOProtocolProposals`. In addition, we recommend that this function emit an event upon successful change of settings, enhancing the transparency of the operation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Rocket Pool (Houston) |
| Report Date | N/A |
| Finders | Dominik Muhs,  Valentin Quelquejay
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/12/rocket-pool-houston/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

