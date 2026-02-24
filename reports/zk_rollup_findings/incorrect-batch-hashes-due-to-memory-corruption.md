---
# Core Classification
protocol: Scroll Phase 1 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32929
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/scroll-phase-1-audit
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

Incorrect Batch Hashes Due to Memory Corruption

### Overview


The ScrollChain contract has a bug that causes incorrect batch hashes when there are L1 transactions involved. The `_commitChunk` function, which computes the hash for each chunk in a batch, relies on the free memory pointer to be in the same location. However, when fetching L1 message hashes, an external call shifts the free memory pointer, causing incomplete chunk hashes. This results in incorrect batch hashes and prevents the network from finalizing. The suggested solutions are to limit the use of inline assembly or to keep track of the correct pointer for hashing. The bug has been fixed in a recent pull request.

### Original Finding Content

When committing a new batch, the `ScrollChain` contract calls the [`_commitChunk`](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/rollup/ScrollChain.sol#L394) function to compute a hash for each chunk in the batch. This hash includes the block contexts, as well as L1 and L2 transaction hashes that are part of this chunk. The `_commitChunk` function does this by getting the free memory pointer, storing everything it needs contiguously starting there, and then getting the free memory pointer again to [compute the keccak256 hash of this section of memory](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/rollup/ScrollChain.sol#L468).




```
 +----------------------+---------------------------+---------------------------+
|    block contexts    |       L1 msg hashes       |       L2 msg hashes       |
| (58 bytes per block) | (32 bytes per L1 message) | (32 bytes per L2 message) |
+----------------------+---------------------------+---------------------------+
^                                                                              ^ 
free memory pointer (read from 0x40)                                     dataPtr

```


Importantly, the function relies on the free memory pointer pointing to the same memory location to be able to [fetch the initial location](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/rollup/ScrollChain.sol#L467) from which to start computing the hash. However, when [fetching the L1 message hashes](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/rollup/ScrollChain.sol#L426), the code does an external call to [`getCrossDomainMessage`](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/rollup/ScrollChain.sol#LL507C63-L507C63) which stores its return value in memory. This causes the free memory pointer to be shifted by a word to the right for each L1 message being processed. This means that the chunk hashes are incomplete and the commitment would not include parts of the information needed as soon as a block contains L1 transactions.


The resulting batch would thus have an incorrect hash. The network would not be able to finalize when there are L1 transactions in a batch because the hash would not match with the proof based on the zkEVM circuits.


Consider limiting the inline assembly usage to be less error-prone for memory corruption issues. Otherwise, make sure to keep track of the right pointer to begin the hashing. Further, ensure that these endpoints and any changes to them are fully end-to-end tested.


***Update:** Resolved in [pull request #546](https://github.com/scroll-tech/scroll/pull/546) at commit [9606c61](https://github.com/scroll-tech/scroll/pull/546/commits/9606c61f5e70d46fae9e4024b574790bc14ff671).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Scroll Phase 1 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/scroll-phase-1-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

