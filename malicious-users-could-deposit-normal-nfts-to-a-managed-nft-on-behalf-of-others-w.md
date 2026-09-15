---
# Core Classification
protocol: Velodrome Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21381
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
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

protocol_categories:
  - dexes
  - services
  - yield_aggregator
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - Xiaoming90
  - 0xNazgul
  - Jonatas Martins
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Malicious users could deposit normal NFTs to a managed NFT on behalf of others without their permission

### Overview


The bug report is about a vulnerability in the VotingEscrow.sol#L130 code. The vulnerability is that the function depositManaged did not verify that the caller (msg.sender) is the owner of the_tokenId. As a result, a malicious user can deposit normal NFTs to a managed NFT on behalf of others without their permission. This could lead to a malicious owner of a managed NFT aggregating the voting power of the victim's normal NFTs and using it to pass malicious proposals or stealing rewards from the victims.

To fix the vulnerability, the code was modified to include additional validation to ensure that the caller is the owner of the deposited NFT. This was fixed in commit 712e14 and verified by Spearbit.

### Original Finding Content

## Vulnerability Report

## Severity
**High Risk**

## Context
**File:** `VotingEscrow.sol`  
**Line:** 130

## Description
The `VotingEscrow.depositManaged` function did not verify that the caller (`msg.sender`) is the owner of the `_tokenId`. As a result, a malicious user can deposit normal NFTs to a managed NFT on behalf of others without their permission.

```solidity
function depositManaged(uint256 _tokenId, uint256 _mTokenId) external nonReentrant {
    require(escrowType[_mTokenId] == EscrowType.MANAGED, "VotingEscrow: can only deposit into managed nft");
    require(!deactivated[_mTokenId], "VotingEscrow: inactive managed nft");
    require(escrowType[_tokenId] == EscrowType.NORMAL, "VotingEscrow: can only deposit normal nft");
    require(!voted[_tokenId], "VotingEscrow: nft voted");
    require(ownershipChange[_tokenId] != block.number, "VotingEscrow: flash nft protection");
    require(_balanceOfNFT(_tokenId, block.timestamp) > 0, "VotingEscrow: no balance to deposit");
    ..SNIP..
}
```

The owner of a normal NFT will have their voting balance transferred to a malicious managed NFT, resulting in loss of rewards and voting power for the victim. Additionally, a malicious owner of a managed NFT could aggregate the voting power of the victim's normal NFTs and perform malicious actions such as stealing the rewards from the victims or using its inflated voting power to pass malicious proposals.

## Recommendation
Implement additional validation to ensure that the caller is the owner of the deposited NFT.

```solidity
function depositManaged(uint256 _tokenId, uint256 _mTokenId) external nonReentrant {
    address sender = _msgSender();
    require(_isApprovedOrOwner(sender, _tokenId), "VotingEscrow: not owner or approved");
    require(escrowType[_mTokenId] == EscrowType.MANAGED, "VotingEscrow: can only deposit into managed nft");
    require(!deactivated[_mTokenId], "VotingEscrow: inactive managed nft");
    ..SNIP..
}
```

## Responses
**Velodrome:** Acknowledged and will fix. Fixed in commit `712e14`.  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Velodrome Finance |
| Report Date | N/A |
| Finders | Xiaoming90, 0xNazgul, Jonatas Martins, 0xLeastwood, Jonah1005, Alex the Entreprenerd |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

