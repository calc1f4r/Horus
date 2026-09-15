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
solodit_id: 30470
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#1-excessive-rights-for-the-manager-role
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.90
financial_impact: high

# Scoring
quality_score: 4.5
rarity_score: 4.5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Excessive rights for the `MANAGER` role

### Overview


The current system allows the `MANAGER` role to have too much power, which can potentially lead to the withdrawal of all tokens from the contract. This role has the ability to swap supported tokens, add new tokens, set oracles, and transfer assets. This can be exploited by a manager to add their own token and oracle, transfer all tokens, and withdraw them. It is suggested to restrict the `MANAGER` role from accessing certain functions and only allow the admin to have these capabilities.

### Original Finding Content

##### Description
The current system configuration grants the `MANAGER` role extensive rights giving its owner the possibility to withdraw all the tokens from the contract. Specifically, the `MANAGER` is authorized to:
- Swap the supported tokens within the [`LRTDepositPool`](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/contracts/LRTDepositPool.sol#L355).
- Introduce new supported tokens to the [`LRTConfig`](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/contracts/LRTConfig.sol#L60) contract.
- Set the `IPriceFetcher` oracles to the [`LRTOracle`](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/contracts/LRTOracle.sol#L93) for the supported tokens.
- Transfer assets from the `NodeDelegator` contracts to the [`DepositorPool`](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/contracts/NodeDelegator.sol#L103).

Advantaging these permissions, a manager is able to add their own ERC-20 token and PriceFetcher for it to the system, transfer all the available tokens from the `NodeDelegator` contracts to `DepositorPool`, and then withdraw them using `swapAssetWithinDepositPool`.

While the MANAGER role acts as a sort of restricted administrative account, the fact that the MANAGER and DEFAULT_ADMIN roles are separated is the evidence that, by design, this role is not considered to be absolutely trustworthy.
##### Recommendation
We recommend revoking the access to call `LRTConfig.addNewSupportedAsset`, `LRTOracle.updatePriceOracleFor` and `LRTDepositPool.swapAssetWithinDepositPool` from the `MANAGER` role, confining such capabilities exclusively to the admin.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4.5/5 |
| Rarity Score | 4.5/5 |
| Audit Firm | MixBytes |
| Protocol | KelpDAO |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#1-excessive-rights-for-the-manager-role
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

