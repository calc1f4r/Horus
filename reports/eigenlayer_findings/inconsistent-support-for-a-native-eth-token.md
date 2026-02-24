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
solodit_id: 30479
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#6-inconsistent-support-for-a-native-eth-token
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

Inconsistent support for a native `ETH` token

### Overview


This bug report highlights an issue with the current strategy for integrating `ETH` support in a contract. The use of native `ETH` instead of the ERC20 interface for balance checks and transactions has led to the need for duplicate operations and the inclusion of a mocked `ETH` address in the list of supported assets. This has caused problems with verifying balances, checking for supported assets, and swapping assets within the contract. The recommendation is to use the `WETH` contract instead of native `ETH` to simplify the architecture and eliminate the need for duplicate functions and a mocked asset. This would involve converting `ETH` into `WETH` in the `depositETH` function and using `WETH` as a general `ERC20` token. Additionally, for accurate processing of `stakeETH` in a specific function, `WETH` can be unwrapped to `ETH` before transfer and wrapped again upon withdrawal.

### Original Finding Content

##### Description
The current strategy for integrating the `ETH` support within the contract relies on usage of the native `ETH`, as opposed to the use of the ERC20 interface for balance checks and transactions. Consequently, native `ETH` is treated as an exceptional case, necessitating duplicate operations and the inclusion of a mocked `ETH` address within the list of supported assets. This approach introduces several issues:
- The balance of the mocked token is verified in the [`removeNodeDelegatorContractFromQueue`](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/contracts/LRTDepositPool.sol#L263) function.
- The `isSupportedAsset` check modifier is overlooked in several functions, including [`LRTDepositPool.depositETH`](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/contracts/LRTDepositPool.sol#L146), [`LRTDepositPool.transferETHToNodeDelegator`](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/contracts/LRTDepositPool.sol#L336), [`NodeDelegator.stakeETH`](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/contracts/NodeDelegator.sol#L175).
- The [`swapAssetWithinDepositPool`](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/contracts/LRTDepositPool.sol#L348) function lacks native ETH support.

##### Recommendation
We recommend utilizing the `WETH` contract instead of native `ETH` to facilitate more polimorphic architecture. This causes converting native `ETH` into `WETH` in the `LRTDepositPool.depositETH` function and utilizing the `WETH` as a general `ERC20` token, thereby eliminating the need for duplicate functions and the inclusion of a mocked asset among the supported assets. Furthermore, for accurate `NodeDelegate.stakeETH` processing, a `WETH` token can be unwrapped to the native `ETH` prior to its transfer to the `EigenPod` and wrapped again upon withdrawal.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | KelpDAO |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#6-inconsistent-support-for-a-native-eth-token
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

