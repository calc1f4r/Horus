---
# Core Classification
protocol: Clique
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53089
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/a80a46df-cbde-45ab-9c9a-a2b64f106ebf
source_link: https://cdn.cantina.xyz/reports/cantina_berachain_clique_january2025.pdf
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
finders_count: 2
finders:
  - Eric Wang
  - RustyRabbit
---

## Vulnerability Title

Potential issues of determining if a transaction is sent by the paymaster 

### Overview


The createStream() and createBatchStream() functions in StreamingNFT, and the claim() function in Distributor1 use an approach that is not recommended. This can cause issues such as poor user experience and double payment of gas fees. The contract owner should set a paymaster state variable to improve the design and prevent these issues. This bug has been fixed in the latest version of the contract. Access control has also been implemented to prevent regular users from creating streams for others. The airdrop system only supports individual users, not smart contract owners.

### Original Finding Content

## Context
- **File Locations**: 
  - `StreamingNFT.sol#L82-L87`
  - `StreamingNFT.sol#L105`

## Description
The `createStream()` and `createBatchStream()` functions in `StreamingNFT`, as well as the `claim()` function in `Distributor1`, use `tx.origin != onbehalfOf` to determine if the transaction is sent by the paymaster. This approach is not recommended due to several downsides:

1. **User Experience Issue**: 
   - Consider a scenario where the owner of the NFT is a smart contract wallet, and the owner of the wallet calls `createStream()`. The wallet owner won’t lose funds because the gas fees are sent to him. However, this may cause poor user experience if the owner wants to retain all funds in the smart contract wallet, as they need to transfer them back.

2. **Integration Challenges**: 
   - The design discourages integration with ERC-4337 accounts. The owner of ERC-4337 accounts creates user operations off-chain and sends them to bundlers. Bundlers then execute the operations on-chain and receive compensation for the spent gas fees. In this situation, `tx.origin` (the bundler) will receive compensation for gas fees again, leading to users effectively paying double gas fees.

3. **Paymaster Exploitation**: 
   - The design allows anyone to act as a paymaster, create streams for others, and be compensated for the gas fee. The gas fees are manually set by the contract owner, and since the price of the native token of Berachain may fluctuate, the contract owner must ensure gas fees are updated accordingly. If the gas fee is not updated in a timely manner, arbitragers may extract value from NFT holders by creating streams for them, causing users to pay more in gas fees than necessary.

## Recommendation
Since users creating streams for others is not an expected use case, consider adopting the following approach: The contract owner can set a `paymaster` state variable in the contract. The functions should check if `tx.origin == paymaster` is true. If so, transfer tokens to the paymaster; otherwise, transfer the entire amount to `onbehalfOf`.

## Clique
- Fixed in commit `04c52bd`.

## Cantina Managed
- **Verification**: The contract implemented a mapping `isPayMaster` to determine if `tx.origin` is a paymaster. Additionally, access control on the `createStream()` function ensures that either `tx.origin` should be a paymaster or the same as `onbehalfOf`. This latter condition prevents a regular user from creating streams for others.

A similar access control is also implemented in the `_claimVestedRewards()` function, ensuring that only the EOA owner of the NFT can claim the rewards. The client has clarified that the airdrop system only supports EOA owners of NFTs and not smart contract owners.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Clique |
| Report Date | N/A |
| Finders | Eric Wang, RustyRabbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_berachain_clique_january2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/a80a46df-cbde-45ab-9c9a-a2b64f106ebf

### Keywords for Search

`vulnerability`

