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
solodit_id: 28447
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Oracle/README.md#1-require-without-message
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

Require without message

### Overview

See description below for full details.

### Original Finding Content

##### Description
In the following functions if revert occurs then user won't receive any information:
https://github.com/lidofinance/curve-merkle-oracle/blob/ae093b308999a564ed3f23d52c6c5dce946dbfa7/contracts/StateProofVerifier.sol#L100
https://github.com/lidofinance/curve-merkle-oracle/blob/ae093b308999a564ed3f23d52c6c5dce946dbfa7/contracts/StableSwapStateOracle.sol#L466
https://github.com/lidofinance/curve-merkle-oracle/blob/ae093b308999a564ed3f23d52c6c5dce946dbfa7/contracts/StableSwapStateOracle.sol#L474

##### Recommendation
We recommend to add message to require.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Oracle/README.md#1-require-without-message
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

