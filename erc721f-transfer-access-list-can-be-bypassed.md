---
# Core Classification
protocol: Fireblocks Upgradeable Tokens Audit - ERC721F
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49781
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fireblocks-upgradeable-tokens-audit-erc721f
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
  - OpenZeppelin
---

## Vulnerability Title

ERC721F Transfer Access List Can Be Bypassed

### Overview


The ERC721F contract has a bug that allows users to transfer tokens without proper access checks. This is because the contract inherits from ERC721Upgradeable, which includes two functions named safeTransferFrom with different parameters. These functions do not use the overridden transferFrom function, allowing users without proper access to transfer tokens. The issue has been acknowledged and resolved in a recent commit.

### Original Finding Content

The [`ERC721F`](https://github.com/fireblocks/reference-protocols/blob/e7003dfb9d89aa4b314a7428cbc59d07f178fd76/protocols/contracts/ERC721F.sol) contract implements logic to verify whether the sender and recipient have access. This functionality is introduced by overriding the [`transferFrom`](https://github.com/fireblocks/reference-protocols/blob/e7003dfb9d89aa4b314a7428cbc59d07f178fd76/protocols/contracts/ERC721F.sol#L279-283) function and including the necessary access checks. However, an issue arises because the contract inherits from the [`ERC721Upgradeable`](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/release-v4.9/contracts/token/ERC721/ERC721Upgradeable.sol) contract, which includes two additional functions, both named [`safeTransferFrom`](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/5bc59992591b84bba18dc1ac46942f1886b30ccd/contracts/token/ERC721/ERC721Upgradeable.sol#L162-L175) but having different parameters. These functions do not internally utilize the overridden `transferFrom` function but instead rely on the [`_safeTransfer`](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/5bc59992591b84bba18dc1ac46942f1886b30ccd/contracts/token/ERC721/ERC721Upgradeable.sol#L195-L198) function. Consequently, a user without the appropriate access can use the `safeTransferFrom` functionality to circumvent the access list checks and successfully transfer the tokens.

Consider introducing additional checks to ensure that proper handling of transfers is conducted through the `safeTransferFrom` functionality.

***Update:** Acknowledged, resolved in commit [7710940](https://github.com/fireblocks/reference-protocols/commit/7710940451037471b1ae9bd03ddce4c946afbc38).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Fireblocks Upgradeable Tokens Audit - ERC721F |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fireblocks-upgradeable-tokens-audit-erc721f
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

