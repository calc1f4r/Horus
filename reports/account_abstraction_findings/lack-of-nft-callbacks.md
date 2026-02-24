---
# Core Classification
protocol: Otim Smart Wallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57053
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-03-otim-smart-wallet-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-03-otim-smart-wallet-securityreview.pdf
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
  - Quan Nguyen
  - Omar Inuwa Trail of Bits PUBLIC
---

## Vulnerability Title

Lack of NFT callbacks

### Overview


This bug report is about a problem that occurs when an externally owned account (EOA) upgrades to a smart wallet. The issue is that the smart wallet is unable to receive non-fungible tokens (NFTs) because it does not have the necessary token callbacks. This means that the user will not be able to receive NFTs, which could cause problems when trying to purchase them from a marketplace. The recommended solution is to add support for ERC-721 and ERC-1155 in the delegate contract, or to create a receiver contract that the delegate contract can inherit from. In the long term, it is important to test how the Otim protocol works with other standards to ensure compatibility.

### Original Finding Content

## Diﬃculty: Low

## Type: Denial of Service

### Description
In the current implementation, when an EOA upgrades to a smart wallet, it will no longer be able to receive NFTs due to a lack of token callbacks in the current implementation. Per the ERC-721 and ERC-1155 standards, when an NFT is transferred using `safeTransfer`, the method checks if the receiving address is an EOA or a smart contract. For the transfer to succeed, the receiver must be an EOA or a smart contract that implements `IERC721Receiver.onERC721Received`. The EIP-7702 standard transforms an EOA into a smart contract, so `IERC721Receiver.onERC721Received` must be implemented in the smart wallet implementation; otherwise, the user will not be able to continue to receive NFTs.

### Exploit Scenario
A user attempts to purchase an NFT from a marketplace, but their transaction will always revert due to a lack of token callbacks in their smart wallet implementation.

### Recommendations
- **Short term**: Add support for ERC-721 and ERC-1155 in the delegate contract; add support directly, or make a receiver contract that the delegate contract will inherit from.
- **Long term**: Identify other standards the Otim protocol is planned to be compatible with and test how they behave with Otim smart wallets.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Otim Smart Wallet |
| Report Date | N/A |
| Finders | Quan Nguyen, Omar Inuwa Trail of Bits PUBLIC |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-03-otim-smart-wallet-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-03-otim-smart-wallet-securityreview.pdf

### Keywords for Search

`vulnerability`

