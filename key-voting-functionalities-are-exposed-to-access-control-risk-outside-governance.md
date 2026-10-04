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
solodit_id: 54049
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

Key voting functionalities are exposed to access control risk outside governance control 

### Overview


The report discusses a vulnerability in Infrared's voting contracts. These contracts allow for the splitting of veNFTs and the management of voter and distributor addresses. However, the deployer of these contracts, who is meant to be the Velodrome Team multisig, has access to these functions instead of the Infrared Governor. This poses a risk as the deployer may not have the same level of security as the Governor. The severity of this vulnerability is low, but the likelihood of it occurring is high. The recommendation is to replace the team's access control with the Infrared Governor.

### Original Finding Content

## Vulnerability Report on Infrared's Voting Contracts

## Context
- **IVotingEscrow.sol**: Lines 178-179
- **VotingEscrow.sol**: Lines 81, 256-266, 1129-1132, 1235-1241

## Description
Infrared's voting contracts are derived from Velodrome, retaining the team address configuration set to the deployer (originally meant to be the address of the Velodrome Team multisig) of the VotingEscrow contract. This address is authorized to call the following functions:
- `setArtProxy()`
- `toggleSplit()`
- `setVoterAndDistributor()`

The `toggleSplit()` function controls the splitting feature of veNFTs while `setVoterAndDistributor()` manages the updates of voter and distributor contract addresses (the entities that have deposit authorization for managed NFTs). In Infrared's context, these functionalities are ideally meant to be controlled by the Governor. 

Allowing the deployer to manage these functionalities outside of governance control is risky because deployer keys may not necessarily maintain the same security posture as the Governor, particularly after migration to a token-based governance system.

## Impact
**Severity**: Low  
The key voting functionalities are exposed to access control risks outside of governance control.

## Likelihood
**Likelihood**: High  
Key voting functionalities `toggleSplit()` and `setVoterAndDistributor()` are always managed by the team address in the current implementation.

## Recommendation
Consider replacing team access control for these functionalities with Infrared Governor.

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

