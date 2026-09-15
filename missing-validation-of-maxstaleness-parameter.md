---
# Core Classification
protocol: Superform v2 Periphery
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63107
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf
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
finders_count: 5
finders:
  - MiloTruck
  - Christoph Michel
  - Ethan
  - Noah Marconi
  - Ladboy233
---

## Vulnerability Title

Missing validation of maxStaleness parameter

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
- `SuperGovernor.sol#L288`
- `SuperGovernor.sol#L296`
- `SuperGovernor.sol#L305-L310`
- `SuperVaultAggregator.sol#L113`

## Description
The following functions set the `maxStaleness` property from a caller-supplied value without validating it first:
- `createVault` (`SuperVaultAggregator.sol#L113`)
- `setOracleMaxStaleness` (`SuperGovernor.sol#L288`)
- `setOracleFeedMaxStaleness` (`SuperGovernor.sol#L296`)
- `setOracleFeedMaxStalenessBatch` (`SuperGovernor.sol#L305`)

If the `maxStaleness` value is too low, every PPS update will be treated as stale. This will exempt the strategist from paying upkeep fees until `maxStaleness` is reset to an appropriate value.

## Recommendation
The protocol should define a `MIN_STALENESS` value, and each of the above functions should require that `maxStaleness >= MIN_STALENESS`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Superform v2 Periphery |
| Report Date | N/A |
| Finders | MiloTruck, Christoph Michel, Ethan, Noah Marconi, Ladboy233 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf

### Keywords for Search

`vulnerability`

