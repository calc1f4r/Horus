---
# Core Classification
protocol: Nouns DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21327
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
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

protocol_categories:
  - dexes
  - yield
  - cross_chain
  - rwa
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - tchkvsky
  - Christos Papakonstantinou
  - Rajeev
  - r0bert
  - hyh
---

## Vulnerability Title

A malicious DAO can mint arbitrary fork DAO tokens

### Overview


This bug report is about a vulnerability in the NounsDAOV3Proposals, NounsDAOV3Fork and NounsTokenFork smart contracts. It has been assigned a Medium Risk severity. 

The vulnerability is that the original DAO is assumed to be honest during the fork period, however, the notion of the fork period is different on the fork DAO compared to the original DAO. If the original DAO executes a malicious proposal in the block at forkEndTimestamp, it will succeed on the original DAO side, but also mint arbitrary fork DAO tokens on the fork DAO side. This means that the original DAO can potentially manipulate the fork DAO governance to steal its treasury funds.

The recommendation to fix the issue is to make the treatment of fork period consistent between the original and fork DAOs in the NounsTokenFork smart contract. The fix has been implemented in nounsDAO/nouns-monorepo#719 and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
- NounsDAOV3Proposals.sol#L495
- NounsDAOV3Fork.sol#L203-L205
- NounsTokenFork.sol#L166-L174

## Description
The original DAO is assumed to be honest during the fork period, which is reinforced in the protocol by preventing it from executing any malicious proposals during that time. Fork joiners are minted fork DAO tokens by the original DAO via `claimDuringForkPeriod()`, which enforces the fork period on the fork DAO side. 

However, the notion of fork period is different on the fork DAO compared to the original DAO (as described in Issue 16). While the original DAO excludes `forkEndTimestamp` from the fork period, the fork DAO includes `forkingPeriodEndTimestamp` in its notion of the fork period.

If the original DAO executes a malicious proposal exactly in the block at `forkEndTimestamp`, which makes a call to `claimDuringForkPeriod()` to mint arbitrary fork DAO tokens, then the proposal will succeed on the original DAO side because it is one block beyond its notion of the fork period. The `claimDuringForkPeriod()` will succeed on the fork DAO side because it is in the last block in its notion of the fork period. 

The original DAO, therefore, can successfully mint arbitrary fork DAO tokens which can be used to:
1. Brick the fork DAO when those tokens are attempted to be minted via auctions later, or 
2. Manipulate the fork DAO governance to steal its treasury funds.

In PoS, blocks are exactly 12 seconds apart. With `forkEndTimestamp = block.timestamp + ds.forkPeriod` and `ds.forkPeriod` now set to 7 days, `forkEndTimestamp` is exactly 50400 blocks (7*24*60*60/12) after the block in which `executeFork()` was executed. A malicious DAO can coordinate to execute such a proposal exactly in that block.

Low likelihood + High impact = Medium severity.

## Recommendation
Make the treatment of fork period consistent between the original and fork DAOs in:

```solidity
function claimDuringForkPeriod(address to, uint256[] calldata tokenIds) external {
    if (msg.sender != escrow.dao()) revert OnlyOriginalDAO();
    - if (block.timestamp > forkingPeriodEndTimestamp) revert OnlyDuringForkingPeriod();
    + if (block.timestamp >= forkingPeriodEndTimestamp) revert OnlyDuringForkingPeriod();
    for (uint256 i = 0; i < tokenIds.length; i++) {
        uint256 nounId = tokenIds[i];
        _mintWithOriginalSeed(to, nounId);
    }
}
```

## Nouns
- **Implemented fix:** nounsDAO/nouns-monorepo#719.
- **Spearbit:** Verified that PR 719 fixes the issue as recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Nouns DAO |
| Report Date | N/A |
| Finders | tchkvsky, Christos Papakonstantinou, Rajeev, r0bert, hyh |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

