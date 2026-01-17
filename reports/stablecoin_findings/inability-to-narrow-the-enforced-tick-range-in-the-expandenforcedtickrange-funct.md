---
# Core Classification
protocol: Panoptic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46532
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0eb3624c-90d4-40d8-93b7-558cb130f753
source_link: https://cdn.cantina.xyz/reports/cantina_panoptic_october_2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - r0bert
  - phaze
---

## Vulnerability Title

Inability to narrow the enforced tick range in the expandEnforcedTickRange function 

### Overview

See description below for full details.

### Original Finding Content

## Expand Enforced Tick Range

## Context
- `contracts/SemiFungiblePositionManager.sol#L426`
- `contracts/SemiFungiblePositionManager.sol#L422`

## Description
The `expandEnforcedTickRange()` function in the `SemiFungiblePositionManager` contract is designed to adjust the enforced tick range for a given Uniswap V4 pool based on the tokens' total supply. However, the function only allows for expanding the tick range and cannot narrow it. This limitation could be a problem when:

- **Dealing with inflationary tokens/tokens with an increasing total supply:** The enforced tick range should ideally be narrowed to reflect the new token supply dynamics.
  
- **Burnable/bridgeable tokens:** Tokens like USDC can be burned or bridged to another chain, temporarily reducing their total supply on the original chain. A malicious actor could exploit this by bridging a large amount of the token, reducing the total supply, and then calling `expandEnforcedTickRange` to expand the enforced tick range. Once the enforced tick range has been expanded, the actor can bridge the tokens back, restoring the initial total supply. However, because the function only allows expanding the tick range and not narrowing it, the excessively wide enforced tick range remains.

The inability to narrow the tick range could lead to an excessively wide enforced tick range that would not reflect the true liquidity or price dynamics of the pool, making the liquidity addition DoS attack economically viable.

## Recommendation
Instead of calculating the `minEnforcedTick` and `maxEnforcedTick` once during the pool initialization and only when the `expandEnforcedTickRange` function is called, consider executing the calculation directly in the `_createPositionInAMM()` internal function. Moreover, it is also recommended in this case to allow for the narrowing of the tick range. As the calculation would be implemented directly in the `_createPositionInAMM()` function, there is no room for flash loan/front-running to deny the creation of a position.

## Panoptic
Acknowledged. We are staying with the current approach to reduce gas costs. The lower bound of `MIN_ENFORCED_TICKFILL_COST` covers the vast majority of bridgeable/wrapped tokens economically (given the example of USDC, `MIN_ENFORCED_TICKFILL_COST` is over 50,000 times greater than the current total supply of that token, which itself already represents 30 billion dollars in value). The supply-based tick calculations are more relevant for very-high-supply tokens, which tend to have either a fixed or monotonically decreasing supply. In rare circumstances where a tick range for a pool is set too wide to prevent liquidity addition DoS, that pool will be automatically blacklisted from our interface.

## Canitna Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Panoptic |
| Report Date | N/A |
| Finders | r0bert, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_panoptic_october_2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0eb3624c-90d4-40d8-93b7-558cb130f753

### Keywords for Search

`vulnerability`

