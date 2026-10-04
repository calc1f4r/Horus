---
# Core Classification
protocol: P2P.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35031
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Fee%20Distributor%20Diff%20Audit%20(v1)/README.md#1-rewards-can-be-accounted-as-collateral
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

Rewards can be accounted as collateral

### Overview


The bug report mentions an issue with the rewards system for a service. If the total rewards reach a certain amount, the rewards will be counted as collateral and the service will not collect fees. However, there is a problem with the code that does not check for a specific condition, which allows a malicious user to manipulate the system and receive more rewards. The recommendation is to add a check to prevent this from happening.

### Original Finding Content

##### Description
If the sum of the execution layer and consensus layer rewards reaches 32 ether, the rewards will be accounted as collateral, and the service will not collect some fees https://github.com/p2p-org/eth-staking-fee-distributor-contracts/blob/30a7ff78e8285f2eae4ae552efb390aa4453a083/contracts/feeDistributor/ContractWcFeeDistributor.sol#L114-L135. The main problem here is that there is no check that `collateralsCountToReturn <= (s_validatorData.exitedCount - s_validatorData.collateralReturnedCount)`. A malicious client can always front-run the `withdraw()` call and transfer additional eth to the contract, so EL + CL rewards always will be divisible by 32 eth.

##### Recommendation
We recommend adding the following check:
`collateralsCountToReturn <= (s_validatorData.exitedCount - s_validatorData.collateralReturnedCount)`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Fee%20Distributor%20Diff%20Audit%20(v1)/README.md#1-rewards-can-be-accounted-as-collateral
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

