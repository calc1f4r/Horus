---
# Core Classification
protocol: Mantle Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43400
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Mantle%20Network/cMETH/README.md#1-cross-chain-transfers-exceeding-the-cap-are-temporarily-locked
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

Cross-Chain Transfers Exceeding the Cap Are Temporarily Locked

### Overview


This bug report is about an issue in the `_credit` function of the `L2cmETH` contract. The function reverts when the credited amount is too high, causing tokens to be locked on the destination chain. This can happen when multiple transactions are processed at the same time or if the token cap is lowered during the transfer. This bug can disrupt cross-network operations and make transfers fail. To fix this, the report recommends implementing a rollback mechanism for failed transactions or giving admins other ways to resolve the issue.

### Original Finding Content

##### Description
This issue has been identified within the [\_credit](https://github.com/Se7en-Seas/cMETH-boring-vault/blob/d6e2d18f45a3e05d749d34966139fc85fc47f7e6/src/L2cmETH.sol#122) function of the `L2cmETH` contract.

The function reverts when the credited amount, combined with the `totalSupply`, exceeds the cap. In cases where multiple cross-chain transactions are processed simultaneously, or if the token cap is lowered during the transfer, tokens may be locked on the destination chain without prior warning that the cap would be exceeded. These tokens remain locked until the admin manually intervenes to increase the cap.

The issue is classified as **medium severity** because it can disrupt cross-network operations, resulting in failed transfers and negatively impacting the usability of the contract.

##### Recommendation
We recommend implementing a rollback mechanism for transactions that exceed the cap, allowing failed transactions to return to the sender chain without requiring admin intervention, or enabling admins to resolve the issue through actions other than increasing the cap.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Mantle Network |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Mantle%20Network/cMETH/README.md#1-cross-chain-transfers-exceeding-the-cap-are-temporarily-locked
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

