---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33855
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#5-the-rate-can-differ-inside-one-block
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

The rate can differ inside one block

### Overview

See description below for full details.

### Original Finding Content

##### Description
A malicious user can front-run a rate update with another rate update, resulting in two token rate updates with different token rates for the same block https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/optimism/TokenRateOracle.sol#L120-L123. This will lead to a postponed rate update on L2.

##### Recommendation
We recommend making a rate update more centralized and using only `TokenRateNotifier` for it. Additionally, we recommend adding a mapping to the `TokenRateNotifier` which will account for the number of tx in the block. This number can be used in the oracle to order tx and correctly update rates.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#5-the-rate-can-differ-inside-one-block
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

