---
# Core Classification
protocol: Gauntlet
chain: everychain
category: logic
vulnerability_type: fund_lock

# Attack Vector Details
attack_type: fund_lock
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7094
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
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
  - fund_lock
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - yield
  - insurance
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Emanuele Ricci
  - Eric Wang
  - Gerard Persoon
---

## Vulnerability Title

Implement a function to claim liquidity mining rewards

### Overview


This bug report is about the AeraVaultV1.sol, which is a liquidity provider of a Balancer pool. The AeraVault is entitled to claim rewards from the MerkleOrchard contract but is missing an implementation to interact with the contract. As a result, all rewards (BAL + other tokens) remain in the MerkleOrchard forever. 

The recommendation is to add a function to allow the vault owner (the Treasury) to claim those rewards. Information on how to interact with the contract can be found on the Balancer Documentation website. Rewards claimed by the AeraVault can then be distributed to the Treasury via the sweep function. Gauntlet has implemented the recommendation in PR #146 and Spearbit has acknowledged it.

### Original Finding Content

## Severity: High Risk

## Context
AeraVaultV1.sol

## Description
Balancer offers a liquidity mining rewards distribution for liquidity providers. 

Liquidity Mining distributions are available to claim weekly through the `MerkleOrchard` contract. Liquidity Providers can claim tokens from this contract by submitting claims to the tokens. These claims are checked against a Merkle root of the accrued token balances which are stored in a Merkle tree. Claiming through the `MerkleOrchard` is much more gas-efficient than the previous generation of claiming contracts, especially when claiming multiple weeks of rewards, and when claiming multiple tokens.

The AeraVault is itself the only liquidity provider of the Balancer pool deployed, so each week it’s entitled to claim those rewards. Currently, those rewards cannot be claimed because the AeraVault is missing an implementation to interact with the `MerkleOrchard` contract, causing all rewards (BAL + other tokens) to remain in the `MerkleOrchard` forever.

## Recommendation
Add a function to allow the vault owner (the Treasury) to claim those rewards. More information on how to claim rewards and interact with the contract can be found directly in the Balancer Documentation website.

Rewards claimed by the AeraVault can be later distributed to the Treasury via the sweep function.

## Gauntlet
Recommendation implemented in PR #146.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Gauntlet |
| Report Date | N/A |
| Finders | Emanuele Ricci, Eric Wang, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf

### Keywords for Search

`Fund Lock, Business Logic`

