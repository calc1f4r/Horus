---
# Core Classification
protocol: Particle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40723
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/83468b34-954f-4650-b16d-7d72c5477780
source_link: https://cdn.cantina.xyz/reports/cantina_competition_particle_feb2024.pdf
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
finders_count: 3
finders:
  - m4rio
  - gmhacker
  - 100proof
---

## Vulnerability Title

Liquidity can still be supplied when the protocol is paused, even though mint is disabled 

### Overview


The report discusses a bug in the ParticlePositionManager contract, specifically in the onERC721Received function. This function allows for the direct transfer of a UniswapV3 position NFT to the ParticlePositionManager contract. However, when the protocol is paused, the mint function cannot be used, as it uses the whenNotPaused modifier. This means that users can still provide liquidity to the Particle position manager in an emergency situation, even when the protocol is paused. However, they will not be able to remove their liquidity, causing confusion and inconvenience. The recommendation is to add the whenNotPaused modifier to the onERC721Received function to avoid this confusion for users. The bug has been fixed and the pausable pattern is no longer used in the contract.

### Original Finding Content

## ParticlePositionManager Overview

## Context 
Location: `ParticlePositionManager.sol#L107-L120`

## Description
The `onERC721Received` function is used to allow a direct transfer of a UniswapV3 position NFT to `ParticlePositionManager`, using `ERC721.safeTransferFrom`. Alternatively, a user can call `ParticlePositionManager.mint`, where tokens will be transferred to the contract and the Particle manager will mint the NFT in Uniswap's position manager.

When the protocol gets paused, the `mint` function cannot be used any longer. That's because the `mint` function uses the `whenNotPaused` modifier. However, it's still possible to supply liquidity by using a direct NFT transfer, given that `onERC721Received` is not checking whether or not the protocol is paused. This means that users can actually still provide liquidity to the Particle position manager in an emergency situation where the protocol is paused.

Importantly, the user will not be able to remove their liquidity because those functions are paused. Therefore, a user can supply liquidity to `ParticlePositionManager` without realizing that the protocol is paused, and end up not being able to remove the liquidity, at least while the protocol is paused.

## Recommendation
Consider adding the `whenNotPaused` modifier to `onERC721Received` as well, avoiding confusing situations for the users.

## Particle
Fixed. We don't use the pausable pattern anymore.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Particle |
| Report Date | N/A |
| Finders | m4rio, gmhacker, 100proof |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_particle_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/83468b34-954f-4650-b16d-7d72c5477780

### Keywords for Search

`vulnerability`

