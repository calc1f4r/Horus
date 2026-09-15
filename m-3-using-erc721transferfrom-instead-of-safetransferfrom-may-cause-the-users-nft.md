---
# Core Classification
protocol: FrankenDAO
chain: everychain
category: uncategorized
vulnerability_type: transferfrom_vs_safetransferfrom

# Attack Vector Details
attack_type: transferfrom_vs_safetransferfrom
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3595
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/18
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/55

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 5

# Context Tags
tags:
  - transferfrom_vs_safetransferfrom
  - nft
  - erc721

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - launchpad
  - payments

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - Nyx
  - WATCHPUG
  - Bnke0x0
  - saian
  - rvierdiiev
---

## Vulnerability Title

M-3: Using `ERC721.transferFrom()` instead of `safeTransferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721

### Overview


This bug report is about a vulnerability found in the smart contract code of the "FrankenDAO" project. The vulnerability is related to the use of `ERC721.transferFrom()` instead of `safeTransferFrom()` when sending a Non-Fungible Token (NFT). The issue was discovered by a group of people including saian, rvierdiiev, WATCHPUG, Tomo, Bnke0x0, Nyx. 

Using `transferFrom()` may result in the NFT being sent to a contract that does not support ERC721, thus freezing the NFT in the contract. This is because, according to the EIP-721 documentation, a wallet, broker or auction application must implement the wallet interface if it will accept safe transfers.

The impact of this vulnerability is that the NFT may get stuck in the contract that does not support ERC721. The code snippet related to this issue can be found at the given link. The vulnerability was discovered through manual review and the recommended solution is to consider using `safeTransferFrom()` instead of `transferFrom()`. The issue was fixed by zobront and the fix can be found at the given link.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/55 

## Found by 
saian, rvierdiiev, WATCHPUG, Tomo, Bnke0x0, Nyx

## Summary

There are certain smart contracts that do not support ERC721, using `transferFrom()` may result in the NFT being sent to such contracts.

## Vulnerability Detail

In `unstake()`, `_to` is param from user's input.

However, if `_to` is a contract address that does not support ERC721, the NFT can be frozen in that contract.

As per the documentation of EIP-721:

> A wallet/broker/auction application MUST implement the wallet interface if it will accept safe transfers.

Ref: https://eips.ethereum.org/EIPS/eip-721

## Impact

The NFT may get stuck in the contract that does support ERC721.

## Code Snippet

https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Staking.sol#L463-L489

## Tool used

Manual Review

## Recommendation

Consider using `safeTransferFrom()` instead of `transferFrom()`.

## Discussion

**zobront**

Fixed: https://github.com/Solidity-Guild/FrankenDAO/pull/10

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | FrankenDAO |
| Report Date | N/A |
| Finders | Nyx, WATCHPUG, Bnke0x0, saian, rvierdiiev, Tomo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/55
- **Contest**: https://app.sherlock.xyz/audits/contests/18

### Keywords for Search

`transferFrom vs safeTransferFrom, NFT, ERC721`

