---
# Core Classification
protocol: Napier Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34395
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Napier%20Finance/Napier%20v1/README.md#5-centralization-risks
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Centralization risks

### Overview


The report discusses a bug in the LST Adapter contracts that could potentially cause issues for users. The contracts have two privileged roles - owner and rebalancer - that have a lot of control over the functions of the contracts. However, this centralized governance model poses a risk to user trust and can lead to a single point of failure. The report recommends implementing a mechanism to prevent the modification of certain functions and suggests a more distributed approach for withdrawing funds to mitigate this risk. 

### Original Finding Content

##### Description
The LST Adapter contracts implement a centralized governance model with two privileged roles: owner and rebalancer. The owner has extensive control, including:

* Modifying the `tranche` value of an adapter, potentially halting all `previewDeposit` and `previewRedeem` functions marked with the `onlyTranche` modifier.
* Pausing/unpausing staking, altering staking limits, and assigning a new rebalancer to the pool.

The rebalancer role, while less powerful, can also significantly impact user experience by:

* Initiating withdrawal requests to integrated LST projects.
* Adjusting the adapter's buffer percentage.

If the rebalancer fails to initiate withdrawal requests, users will be unable to redeem their funds until the owner intervenes. This centralization of control introduces a single point of failure and poses a risk to user trust.

##### Recommendation
We recommend implementing a mechanism to prevent the modification of the `tranche` value while the tranche holds a non-zero balance of adapter shares. This ensures the intended functionality of the `onlyTranche`-marked functions. Additionally, we suggest considering a more distributed mechanism for withdrawing funds from integrated projects to mitigate the reliance on a single rebalancer for user redemptions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Napier Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Napier%20Finance/Napier%20v1/README.md#5-centralization-risks
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

