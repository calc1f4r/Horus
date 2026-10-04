---
# Core Classification
protocol: Infrared Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54047
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/89e5aa01-14ad-48f8-af3d-d1182d4ffefb
source_link: https://cdn.cantina.xyz/reports/cantina_infrared_july2024.pdf
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
finders_count: 4
finders:
  - 0xRajeev
  - Mario Poneder
  - Cryptara
  - phaze
---

## Vulnerability Title

Acknowledged Medium-Low severity issues from Velodrome security review should be re- considered 

### Overview


This is a bug report for the Velodrome Spearbit Security Review. Infrared, a platform that uses a modified version of Velodrome's contracts, has identified four issues with medium and low severity that were reported in Velodrome's security review but not fixed as recommended. These issues include potential manipulation of bribes and fees, inconsistency in certain functions, and the ability for managed NFTs to vote multiple times. The recommendation is for Velodrome to revisit these issues and consider a different resolution to address the risks. It is also suggested to reevaluate other voting related issues in the report in the context of Infrared.

### Original Finding Content

## Velodrome Spearbit Security Review

## Description

Infrared derives its Voting logic from a slightly modified version of Velodrome's corresponding contracts. We identified a total of four applicable Medium and Low severity issues that were reported in Velodrome's Spearbit security review and acknowledged by the Velodrome team without fixing it as recommended. We are highlighting those issues here for awareness and potential reconsideration of a different resolution:

1. **Issue 5.3.3 (Medium severity)**:
   - Bribe and fee token emissions can be gamed by users. Voters can continue to earn bribes and fees for their votes that are disproportionately higher compared to their decaying veNFT voting weight if no one pokes their positions.

2. **Issue 5.3.9 (Medium severity)**:
   - Inconsistency between `balanceOfNFT`, `balanceOfNFTAt`, and `_balanceOfNFT` functions. The flash-loan protection implemented in `balanceOfNFT()` using `ownershipChange[_tokenId] == block.number` is not consistently applied to `balanceOfNFTAt()` and `_balanceOfNFT` functions, which could allow integrators using those functions to bypass it.

3. **Issue 6.4.3 (Low severity)**:
   - Managed NFT can vote more than once per epoch under certain circumstances. Users can bypass the one-vote-per-epoch with Managed NFTs by voting once, withdrawing and redepositing NFTs into Managed NFTs, and voting again.

4. **Issue 6.4.8 (Low severity)**:
   - Slightly Reduced Voting Power due to Rounding Error. A fully locked NFT will incur a slight loss of vote weight because of rounding errors.

## Recommendation

Consider revisiting the original issues to either acknowledge the risk as-is or potentially evaluate a different resolution as per the original recommendation. It is also worth reevaluating other Voting related issues from the report to understand their implications in the context of Infrared.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Infrared Finance |
| Report Date | N/A |
| Finders | 0xRajeev, Mario Poneder, Cryptara, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_infrared_july2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/89e5aa01-14ad-48f8-af3d-d1182d4ffefb

### Keywords for Search

`vulnerability`

