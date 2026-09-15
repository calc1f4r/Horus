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
solodit_id: 35034
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Fee%20Distributor%20Diff%20Audit%20(v1)/README.md#2-clients-collateral-can-be-distributed-as-rewards
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

Client's collateral can be distributed as rewards

### Overview


The bug report describes a problem with the `_sendValue` function in the ContractWcFeeDistributor.sol file. If this function fails, it can cause the `s_validatorData.collateralReturnedCount` to be updated incorrectly, resulting in the client losing some of their collateral. Additionally, the `balance` function may also distribute the client's collateral as rewards. The recommendation is to add a check for this specific function and give the client another chance to receive their collateral if the first attempt fails. It is also suggested to add a cooldown period after the first attempt to prevent any potential malicious attacks.

### Original Finding Content

##### Description
If `_sendValue` reverts here https://github.com/p2p-org/eth-staking-fee-distributor-contracts/blob/30a7ff78e8285f2eae4ae552efb390aa4453a083/contracts/feeDistributor/ContractWcFeeDistributor.sol#L128-L131, then `s_validatorData.collateralReturnedCount` will be updated incorrectly, and the client will lose some collateral. Moreover, `balance` here https://github.com/p2p-org/eth-staking-fee-distributor-contracts/blob/30a7ff78e8285f2eae4ae552efb390aa4453a083/contracts/feeDistributor/ContractWcFeeDistributor.sol#L134 will account for the client's collateral and distribute it as rewards.

##### Recommendation
We recommend adding a check for this specific `_sendValue` and giving the client one more chance to receive collateral if the first attempt is reverted. Also, it is necessary to add some cooldown after the first attempt so no one can ddos it.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Fee%20Distributor%20Diff%20Audit%20(v1)/README.md#2-clients-collateral-can-be-distributed-as-rewards
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

