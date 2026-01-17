---
# Core Classification
protocol: Chronicle Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54349
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5c55f883-124f-42f9-8315-f8bb0d5c2da9
source_link: https://cdn.cantina.xyz/reports/cantina_chronicle_oct2023.pdf
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
finders_count: 3
finders:
  - m4rio
  - shung
  - Christoph Michel
---

## Vulnerability Title

The age of the pokeData is updated once accepted 

### Overview

See description below for full details.

### Original Finding Content

## Context

**File:** Scribe.sol#L117  

## Description

When data is created offchain, an age is defined which represents the timestamp of the data creation. Once that data reaches the chain via the poke function, the age is updated to `block.timestamp`, invalidating the initial value.  

This can cause issues in scenarios of high volatility markets and high onchain usage. It can happen that data is waiting in the mempool long enough for a second piece of data to arrive. If the initial data reaches the block first, then the second value, which should be the most updated value, will be discarded. This occurs due to the fact that on Scribe.sol#L117, the update on age is done as follows:

```solidity
_pokeData.age = uint32(block.timestamp);
```

For the second call, the check on Scribe.sol#L95 will cause the transaction to revert:

```solidity
if (pokeData.age <= _pokeData.age) {
    revert StaleMessage(pokeData.age, _pokeData.age);
}
```

The same scenario happens on the ScribeOptimisc contract, with the optimistic pokes.

## Recommendation

Consider keeping the integrity of the data that is submitted onchain by not updating the age with the current timestamp.

## Chronicle

**Acknowledged.** While we think there are valid arguments for both types of definitions for a value's age, the simple reason we go with this one is due to backwards compatibility reasons with regards to MakerDAO's Median contract. However, we will review our documentation to ensure this behavior is sufficiently pointed out to users/integrators.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Chronicle Labs |
| Report Date | N/A |
| Finders | m4rio, shung, Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_chronicle_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5c55f883-124f-42f9-8315-f8bb0d5c2da9

### Keywords for Search

`vulnerability`

