---
# Core Classification
protocol: BMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53440
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5b3d8ec8-95d8-4979-a082-f9681b32172c
source_link: https://cdn.cantina.xyz/reports/cantina_bmx_march2025.pdf
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
  - Chinmay Farkya
  - high byte
---

## Vulnerability Title

Conform to chainlink latestRoundData pattern 

### Overview

See description below for full details.

### Original Finding Content

## Context: wBltOracle.sol#L64-L70

## Description
Almost all values are ignored here but the chainlink signature is:

```solidity
function latestRoundData() external view
returns (
    uint80 roundId,
    int256 answer,
    uint256 startedAt,
    uint256 updatedAt,
    uint80 answeredInRound
)
```

This could break protocols trying to integrate this oracle as they most likely check price is not stale. The underlying oracle is out of scope; it is assumed to revert if the price is stale and update the price on demand. As such, unless there’s a specific reason to keep one of these values 0, it might make sense to return something like this instead:

```solidity
return (
    uint80(block.number),
    int256(_getNormalizedPrice()),
    block.timestamp,
    block.timestamp,
    uint80(block.number)
);
```

## BMX
This has been implemented in commit `2dcfad81`.

## Cantina Managed
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | BMX |
| Report Date | N/A |
| Finders | Chinmay Farkya, high byte |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_bmx_march2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5b3d8ec8-95d8-4979-a082-f9681b32172c

### Keywords for Search

`vulnerability`

