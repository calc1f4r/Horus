---
# Core Classification
protocol: Optimism Smart Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10733
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/optimism-smart-contracts-audit/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L03] Lack of input validations

### Overview

See description below for full details.

### Original Finding Content

In the interest of predictability, some functions could benefit from more stringent input validations.


* The [`init` function](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/bridge/tokens/Abs_L2DepositedToken.sol#L59) of the `Abs_L2DepositedToken` abstract contract does not ensure that [the passed token gateway address](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/bridge/tokens/Abs_L2DepositedToken.sol#L60) is non-zero. If it is called with a zero address (before the gateway address in state is set to a non-zero value), it will incorrectly [emit](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/bridge/tokens/Abs_L2DepositedToken.sol#L68) an `Initialized` event.
* The [`getMerkleRoot` function](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/libraries/utils/Lib_MerkleTree.sol#L23) of the `Lib_MerkleTree` library provides 16 [default values](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/libraries/utils/Lib_MerkleTree.sol#L41-L58), which implicitly limits the depth of unbalanced trees to 16. Balanced trees, on the other hand, have no restriction. Although this is unlikely to matter in practice, usage assumptions should be documented and validated wherever possible. Consider explicitly bounding the number of elements by 216.
* According to the RLP specification described in the [Appendix B of Ethereum’s Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf#appendix.B), *“Byte arrays containing 264 or more bytes cannot be encoded”*. This restriction is not being explicitly enforced by the [`writeBytes` function](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/libraries/rlp/Lib_RLPWriter.sol#L23) of the `Lib_RLPWriter` library.
* The [`_editBranchIndex` function](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/libraries/trie/Lib_MerkleTrie.sol#L864) of the `Lib_MerkleTrie` library should explicitly validate that [the passed index](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/libraries/trie/Lib_MerkleTrie.sol#L866) is lower than the [`TREE_RADIX` constant](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/libraries/trie/Lib_MerkleTrie.sol#L34-L35) to avoid misusage.
* The [`_getNodePath` function](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/libraries/trie/Lib_MerkleTrie.sol#L603) of the `Lib_MerkleTrie` library should explicitly validate that [the passed node](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/libraries/trie/Lib_MerkleTrie.sol#L604) is a leaf or extension node to avoid misuse.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Optimism Smart Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/optimism-smart-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

