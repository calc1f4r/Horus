---
# Core Classification
protocol: Boba 1 (Bridges and LP floating fee)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60705
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
source_link: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
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
finders_count: 5
finders:
  - Pavel Shabarkin
  - Ibrahim Abouzied
  - Andy Lin
  - Adrian Koegl
  - Valerian Callens
---

## Vulnerability Title

Attacker Can Steal Tokens by Deploying Malicious Contracts

### Overview


This bug report discusses an issue with the current design of the NFTBridge system. The client has acknowledged the issue and provided an explanation. The problem is related to the registration process for new pairs of native ERC721 and ERC1155 tokens on the NFTBridge. The system requires a complementary contract on the other chain, which can be deployed by the user. However, this leaves room for malicious users to deploy harmful contracts and obtain the bridged token on the native chain. This is a serious problem because once a contract is registered, it cannot be modified. This could result in the affected token contract being permanently unbridgeable, users losing their tokens, and no way to pause a specific pair. The recommendation is to have a thorough process and checklist for registering new contracts and to consider implementing bytecode verification to prevent malicious contracts from being registered. 

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation: Before registering new pairs, the native NFT contracts are to be manually evaluated as per their compatibility and security (along with some automated test cases that are yet to be developed). Most NFTs to be registered as a pair on the NFTBridge should be projects with recognition. For the representation tokens on the non-native layer (L _StandardERC721,L_ StandardERC1155), the Boba team could deploy these contracts that work with their own centralized bridge. The NFTs however could have completely different other representation tokens deployed that could work with other bridges.

**File(s) affected:**`ERC1155Bridges/*.sol`, `ERC721Bridges/*.sol`, `standards/L1StandardERC721.sol`, `standards/L2StandardERC721.sol`, `standards/L1StandardERC1155.sol`, `standards/L2StandardERC1155.sol`

**Description:** A native ERC721 and ERC1155 token requires a complementing contract on the other chain in order to be bridgeable. In its current design, a user is responsible for deploying a `L1StandardERC721`, `L2StandardERC721`, `L1StandardERC1155`, or `L2StandardERC1155` contract. Subsequently, a user has to request registration of this contract on both chains.

A malicious user, however, could deploy a malicious contract in order to obtain the bridged token on the native chain. There are many possible ways for an attacker to hide malicious logic in such a deployed contract.

The severity of this issue arises through the fact that a configured token contract pair cannot be modified. If Boba admins fail to recognize malicious logic in a contract and register it on one or both chains, it cannot be reverted. This has three main consequences:

*   The affected native token contract will never be bridgeable through these contracts anymore (without loosing those tokens).
*   Users might accidentally use the bridge to a registered malicious contract and loose their tokens.
*   There is no implemented functionality to pause a specific pair.

**Recommendation:** Elaborate on the process and checklist used to register new contracts. Consider bytecode verification to avoid unnoticed malicious logic of such deployed contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Boba 1 (Bridges and LP floating fee) |
| Report Date | N/A |
| Finders | Pavel Shabarkin, Ibrahim Abouzied, Andy Lin, Adrian Koegl, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html

### Keywords for Search

`vulnerability`

