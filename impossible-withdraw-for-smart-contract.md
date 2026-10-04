---
# Core Classification
protocol: Keep3r.Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28294
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Keep3r.Network/README.md#1-impossible-withdraw-for-smart-contract
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

Impossible withdraw for smart contract

### Overview


This bug report is about a problem with the StakingRewardsV3 smart contract. If a smart contract deposits a Non-Fungible Token (NFT) to StakingRewardsV3, then it must have an `onERC721Received()` function or the `withdraw()` function will always revert. The recommended solution is to use `transferFrom()` instead of `safeTransferFrom()`. 

Non-Fungible Tokens (NFTs) are unique digital assets that are not interchangeable. They are used in a variety of ways, such as in gaming, digital art, and virtual real estate. StakingRewardsV3 is a smart contract that allows users to deposit NFTs and earn rewards.

When a smart contract deposits an NFT to StakingRewardsV3, the smart contract must have an `onERC721Received()` function. If this function is not included, the `withdraw()` function will always revert. This means that the withdrawal of the NFT will not be completed and the user will not receive their rewards.

To solve this issue, the bug report recommends using `transferFrom()` instead of `safeTransferFrom()`. `TransferFrom()` is a function that allows users to transfer tokens from one account to another. By using `transferFrom()`, users can ensure that their NFTs are transferred successfully and that they receive their rewards.

### Original Finding Content

##### Description
If any smart contract deposits NFT to StakingRewardsV3 it must have `onERC721Received()` function or `withdraw()` will always revert:
https://github.com/keep3r-network/StakingRewardsV3/tree/13ecc6966ae1a413f62224382bfd4d64b1a22351/contracts/StakingRewardsV3-1.sol#L256
##### Recommendation
We recommend to use `transferFrom()` instead of `safeTransferFrom()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Keep3r.Network |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Keep3r.Network/README.md#1-impossible-withdraw-for-smart-contract
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

