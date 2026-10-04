---
# Core Classification
protocol: Sudoswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6778
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_lending
  - payments

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Max Goodman
  - Mudit Gupta
  - Gerard Persoon
---

## Vulnerability Title

Malicious Router can steal NFTs via Re-Entrancy attack

### Overview


This bug report is about a vulnerability in the LSSVMPair.sol and LSSVMPairERC20.sol smart contracts. If a malicious router is approved by the factory owner, they can call functions like swapTokenForAnyNFTs() and set is-Router to true. This could allow the malicious router to execute a token transfer so that the require of _validateTokenInput is satisﬁed when the context returns to the pair, allowing them to receive 2 NFTs by sending tokens only once. 

Sudoswap, the developers of the contracts, have addressed the immediate issue by validating NFT balances after the router.pairTransferERC20From call to mitigate re-entrant balance changes by a malicious router, and they are also addressing the broader issue of the cache function being exploitable in the GitHub Issue about simplifying the connection between the pair and the router. In order to protect against this vulnerability, Spearbit recommends Sudoswap to implement reentrancy modiﬁers, check if the NFT balance before and after router.pairTransferERC20From() is the same, and make sure the following contracts and addresses are trusted: the NFT contract, the ERC-20 tokens, the assetRecipient , the bonding curve, the factory, the factory owner, and the protocolFeeRecipient . 

Sudoswap has acknowledged the recommendation.

### Original Finding Content

## Severity: Medium Risk

### Context
- **Contracts:** `LSSVMPair.sol`, `LSSVMPairERC20.sol`

### Description
If the factory owner approves a malicious `_router`, it is possible for the malicious router to call functions like `swapTokenForAnyNFTs()` and set `is-Router` to true. Once that function reaches `router.pairTransferERC20From()` in `validateTokenInput()`, they can re-enter the pair from the router and call `swapTokenForAnyNFTs()` again.

This second time, the function reaches `router.pairTransferERC20From()`, allowing the malicious router to execute a token transfer so that the `require` of `validateTokenInput` is satisfied when the context returns to the pair. When the context returns from the reentrant call back to the original call, the `require` of `validateTokenInput` would still pass because the balance was cached before the reentrant call. Therefore, an attacker will receive 2 NFTs by sending tokens only once.

### Recommendation
Spearbit recommends Sudoswap to implement reentrancy modifiers (see finding "Add Reentrancy Guards" in the "Low Risk" section of this report). Sudoswap should also consider checking if the NFT balance before and after `router.pairTransferERC20From()` is the same. Finally, we recommend making sure the following contracts and addresses are trusted:
- The NFT contract
- The ERC-20 tokens
- The `assetRecipient`
- The bonding curve
- The factory
- The factory owner
- The `protocolFeeRecipient`

### Sudoswap
The immediate issue is addressed in this branch. We now validate NFT balances after the `router.pairTransferERC20From` call to mitigate re-entrant balance changes by a malicious router. The broader issue of the cache function being exploitable is addressed in the GitHub Issue about simplifying the connection between the pair and the router.

### Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap |
| Report Date | N/A |
| Finders | Max Goodman, Mudit Gupta, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

