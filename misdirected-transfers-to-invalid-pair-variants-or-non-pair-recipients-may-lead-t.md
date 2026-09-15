---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18306
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

Misdirected transfers to invalid pair variants or non-pair recipients may lead to loss/lock of NFTs/tokens

### Overview


This bug report is about the functions depositNFTs() and depositERC20() in the LSSVMPairFactory.sol file. These functions allow deposits of ERC 721 Non-Fungible Tokens (NFTs) and ERC20 tokens after pair creation. However, the deposit transfers happen before the check to ensure it is a valid pair/variant for emitting an event. This could lead to misdirected deposits to invalid pair variants or non-pair recipients, resulting in loss/lock of NFTs/tokens. 

The recommendation is to apply the specific pair variant check for both events and transfers, and to check that the right tokens/NFTs are deposited. Sudorandom Labs have acknowledged the finding, but do not plan to make any additional changes. They believe that only event emission is important to be tracked with the pool type, as pool owners can always withdraw any ERC20/721/1155 sent to their pool. Spearbit have acknowledged this report.

### Original Finding Content

## Severity: Medium Risk

## Context
- LSSVMPairFactory.sol#L650-L663
- LSSVMPairFactory.sol#L668-L676

## Description
Functions `depositNFTs()` and `depositERC20()` allow deposits of ERC 721 NFTs and ERC20 tokens after pair creation. While they check that the deposit recipient is a valid pair/variant for emitting an event, the deposit transfers happen prior to the check and without the same validation. With dual home tokens (see weird-erc20), the emit could be skipped when the "other" token is transferred. 

Additionally, the `isPair()` check in `depositNFTs()` does not specifically check if the pair variant is `ERC721_ERC20` or `ERC721_ETH`. This allows accidentally misdirected deposits to invalid pair variants or non-pair recipients leading to loss/lock of NFTs/tokens.

## Recommendation
For functions `depositNFTs()` and `depositERC20()`, apply the specific pair variant check for both events and transfers, and ensure the right tokens/NFTs are deposited.

## Sudorandom Labs
We'll acknowledge the finding, but no additional changes at this time. Only event emission is important to be tracked with the pool type, as pool owners can always withdraw any ERC20/721/1155 sent to their pool (in the event they e.g. deposit to a pool they own for a different asset type).

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

