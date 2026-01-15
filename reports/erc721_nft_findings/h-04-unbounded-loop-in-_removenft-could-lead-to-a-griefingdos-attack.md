---
# Core Classification
protocol: Visor
chain: everychain
category: dos
vulnerability_type: dos

# Attack Vector Details
attack_type: dos
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 192
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-visor-contest
source_link: https://code4rena.com/reports/2021-05-visorfinance
github_link: https://github.com/code-423n4/2021-05-visorfinance-findings/issues/80

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - dos
  - broken_loop

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - gpersoon
  - Sherlock
  - toastedsteakswhich
  - pauliax
  - cmichel
---

## Vulnerability Title

[H-04] Unbounded loop in _removeNft could lead to a griefing/DOS attack

### Overview


This bug report is about a vulnerability in the Visor.sol contract which allows for a Griefing/DOS attack. A malicious NFT contract could send many NFTs to the vault, which could cause excessive gas consumption and even transactions reverted when other users are trying to unlock or transfer NFTs. This is due to an unbounded loop in the `_removeNft` function and the fact that the `onERC721Received` function is permissionless. As a result, benign users would suffer from large and unnecessary gas consumption, which could even exceed the block gas limit and cause the transaction to fail. To mitigate this vulnerability, it is recommended to use a mapping to store the received NFTs into separate arrays according to `nftContract`. Alternatively, a method specifically for the owner to remove NFTs from the `nfts` array directly could be added.

### Original Finding Content

## Handle

shw


## Vulnerability details

## Impact

Griefing/DOS attack is possible when a malicious NFT contract sends many NFTs to the vault, which could cause excessive gas consumed and even transactions reverted when other users are trying to unlock or transfer NFTs.

## Proof of Concept

1. The function `_removeNft` uses an unbounded loop, which iterates the array `nfts` until a specific one is found. If the NFT to be removed is at the very end of the `nfts` array, this function could consume a large amount of gas.
2. The function `onERC721Received` is permissionless. The vault accepts any NFTs from any NFT contract and pushes the received NFT into the array `nfts`.
3. A malicious user could write an NFT contract, which calls `onERC721Received` of the vault many times to make to array `nfts` grow to a large size. Besides, the malicious NFT contract reverts when anyone tries to transfer (e.g., `safeTransferFrom`) its NFT.
4. The vault then has no way to remove the transferred NFT from the malicious NFT contract. The two only functions to remove NFTs, `transferERC721` and `timeUnlockERC721`, fail since the malicious NFT contract reverts all `safeTransferFrom` calls.
5. As a result, benign users who unlock or transfer NFTs would suffer from large and unnecessary gas consumption. The consumed gas could even exceed the block gas limit and cause the transaction to fail every time.

Referenced code:
[Visor.sol#L127-L140](https://github.com/code-423n4/2021-05-visorfinance/blob/main/contracts/contracts/visor/Visor.sol#L127-L140)
[Visor.sol#L514-L515](https://github.com/code-423n4/2021-05-visorfinance/blob/main/contracts/contracts/visor/Visor.sol#L514-L515)
[Visor.sol#L519-L522](https://github.com/code-423n4/2021-05-visorfinance/blob/main/contracts/contracts/visor/Visor.sol#L519-L522)
[Visor.sol#L571-L574](https://github.com/code-423n4/2021-05-visorfinance/blob/main/contracts/contracts/visor/Visor.sol#L571-L574)

## Tools Used

None

## Recommended Mitigation Steps

Use a mapping (e.g., `mapping(address=>Nft[]) nfts`) to store the received NFTs into separate arrays according to `nftContract` instead of putting them into the same one. Or, add a method specifically for the owner to remove NFTs from the `nfts` array directly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Visor |
| Report Date | N/A |
| Finders | gpersoon, Sherlock, toastedsteakswhich, pauliax, cmichel, shw |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-visorfinance
- **GitHub**: https://github.com/code-423n4/2021-05-visorfinance-findings/issues/80
- **Contest**: https://code4rena.com/contests/2021-05-visor-contest

### Keywords for Search

`DOS, Broken Loop`

