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
solodit_id: 35041
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Fee%20Distributor%20Diff%20Audit%20(v1)/README.md#3-an-incorrect-distribution-of-rewards-in-case-of-_sendvalue-revert
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

An incorrect distribution of rewards in case of `_sendValue` revert

### Overview


The bug report states that there is a problem with the `_sendValue` call in the `OracleFeeDistributor.sol` contract. This can cause the `s_clientOnlyClRewards` value to be incorrect if the call is reverted. The recommendation is to not update the `s_clientOnlyClRewards` if the `_sendValue` calls are being reverted.

### Original Finding Content

##### Description
Because of a possible revert of the `_sendValue` call updated value of the `s_clientOnlyClRewards,` https://github.com/p2p-org/eth-staking-fee-distributor-contracts/blob/30a7ff78e8285f2eae4ae552efb390aa4453a083/contracts/feeDistributor/OracleFeeDistributor.sol#L151 will lead to an incorrect distribution of the rewards.

##### Recommendation
It's recommended not to update `s_clientOnlyClRewards` if all `_sendValue` calls were reverted.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Fee%20Distributor%20Diff%20Audit%20(v1)/README.md#3-an-incorrect-distribution-of-rewards-in-case-of-_sendvalue-revert
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

