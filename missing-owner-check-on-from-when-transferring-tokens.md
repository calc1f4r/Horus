---
# Core Classification
protocol: CLOBER
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7256
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation
  - ownership
  - nft

protocol_categories:
  - dexes
  - bridge
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Desmond Ho
  - Grmpyninja
  - Christoph Michel
  - Throttle
  - Taek Lee
---

## Vulnerability Title

Missing owner check on from when transferring tokens

### Overview


This bug report outlines a high risk vulnerability with the OrderNFT.sol#L207 contract. The vulnerability exists in the OrderNFT.transferFrom/safeTransferFrom functions, which use the internal _transfer function. This function checks approvals on msg.sender through _isApprovedOrOwner(msg.sender, tokenId), however it does not check that the specified "from" parameter is actually the owner of the Non-Fungible Token (NFT). This means an attacker can decrease other users' NFT balances, making them unable to cancel or claim their NFTs and locking users' funds. The attacker can do this by transferring their own NFT, passing the victim as the "from" parameter, by calling transferFrom(from=victim, to=attackerAccount, tokenId=attackerTokenId).

The recommendation to fix this issue is to add a check to the _transfer function, requiring that the owner of the tokenId is the same as the "from" parameter, through the command require(ownerOf(tokenId) == from, Errors.ACCESS). This has been fixed in PR 310, and verified by Spearbit.

### Original Finding Content

## Security Report

## Severity: High Risk

### Context
`OrderNFT.sol#L207`

### Description
The `OrderNFT.transferFrom`/`safeTransferFrom` methods use the internal `_transfer` function. While they check approvals on `msg.sender` through `_isApprovedOrOwner(msg.sender, tokenId)`, it is never checked that the specified `from` parameter is actually the owner of the NFT. 

An attacker can decrease other users' NFT balances, making them unable to cancel or claim their NFTs and locking users' funds. The attacker transfers their own NFT passing the victim as `from` by calling `transferFrom(from=victim, to=attackerAccount, tokenId=attackerTokenId)`. This passes the `_isApprovedOrOwner` check but reduces `from`'s balance.

### Recommendation
Add the following check to `_transfer`:

```solidity
require(ownerOf(tokenId) == from, Errors.ACCESS);
```

### Clober
Fixed PR 310.

### Spearbit
Verified. Ownership check added.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | CLOBER |
| Report Date | N/A |
| Finders | Desmond Ho, Grmpyninja, Christoph Michel, Throttle, Taek Lee |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Ownership, NFT`

