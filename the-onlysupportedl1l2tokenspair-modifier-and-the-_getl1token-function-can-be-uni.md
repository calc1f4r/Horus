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
solodit_id: 33864
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#14-the-onlysupportedl1l2tokenspair-modifier-and-the-_getl1token-function-can-be-unified
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

The `onlySupportedL1L2TokensPair` modifier and the `_getL1Token` function can be unified

### Overview

See description below for full details.

### Original Finding Content

##### Description
There is the `onlySupportedL1L2TokensPair` modifier defined at the line https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/optimism/RebasableAndNonRebasableTokens.sol#L51. It is used to check whether the user provided a correct pair of token addresses in the `L1ERC20ExtendedTokensBridge` contract. In the `L2ERC20ExtendedTokensBridge` contract, a different approach is employed where `_getL1Token` is used to get the corresponding token address on the L1 side. The same method can be adopted in the `L1ERC20ExtendedTokensBridge` so that users won't need to provide two token addresses.

##### Recommendation
We recommend implementing the `_getL2Token` function in the `L1ERC20ExtendedTokensBridge` contract which will return the corresponding token address on L2.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#14-the-onlysupportedl1l2tokenspair-modifier-and-the-_getl1token-function-can-be-unified
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

