---
# Core Classification
protocol: dForce
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36552
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/sUSX/README.md#6-inability-to-perform-a-cross-chain-transfer-due-to-mintcap
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

Inability to perform a cross-chain transfer due to mintCap

### Overview


The sUSX contract has a bug that can cause cross-chain transfers to fail if the destination chain's mint cap is reached. This means that users' funds can get locked and the only way to fix it is for the administrator to increase the mint cap. There is no way for users to withdraw their funds back to the source chain if this happens. To fix this, checks and fallback mechanisms should be implemented. This bug is marked as medium severity because it can temporarily lock users' funds.

### Original Finding Content

##### Description
Cross-chain transfers in the sUSX contract may be reverted on the destination chain in [`finalizeInboundTransferShares`](https://github.com/dforce-network/sUSX/blob/2ff5d7a8f9a509006557bf5de72fabf40d1138a5/src/sUSX.sol#L290) if the mint cap (`mintCap`) is reached. This issue arises because different chains may have different mintCap settings. When the mint cap on the destination chain is reached, the transaction reverts, leading to the following problems:

* Funds Locked: User's funds get locked, preventing the completion of  the withdrawal.
* Admin Intervention Required: The only way to resolve this issue is for the administrator to increase the mintCap on the destination chain.
* No Option to Withdraw Funds Back: Users have no ability to withdraw their funds back to the source chain if the transfer fails due to the mint cap limit.

This issue is marked as **medium** because it results in the temporary locking of users' funds in case of incorrect configuration.

##### Recommendation
We recommend implementing checks and fallback mechanisms to handle such scenarios.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/sUSX/README.md#6-inability-to-perform-a-cross-chain-transfer-due-to-mintcap
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

