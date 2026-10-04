---
# Core Classification
protocol: Dharma Labs Smart Wallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16795
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
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
  - eric.rafaloﬀ@trailofbits.com Dominik Czarnota
  - Eric Rafaloﬀ
---

## Vulnerability Title

Missing error check when calling ecrecover

### Overview

See description below for full details.

### Original Finding Content

## Auditing and Logging

**Type:** Auditing and Logging  
**Target:** Multiple Files  

**Difficulty:** Low  

## Description  
Several calls are made to the ECDSA library, which is a wrapper around the built-in `ecrecover` function, without explicitly checking if an error occurred (i.e., an address of 0 is returned).

- implementations/key-ring/DharmaKeyRingImplementationV0.sol#L141
- implementations/smart-wallet/DharmaSmartWalletImplementationV2.sol#L569
- implementations/smart-wallet/DharmaSmartWalletImplementationV2.sol#L1121
- implementations/smart-wallet/DharmaSmartWalletImplementationV2.sol#L1129
- implementations/smart-wallet/DharmaSmartWalletImplementationV2.sol#L1313
- registries/DharmaKeyRegistryV1.sol#L68

*Figure 6.1: List of affected functions.*

## Exploit Scenario  
All identified instances were found to be unexploitable, due to adequate data validation of user and Dharma signing keys elsewhere in the codebase. However, future changes to the codebase risk introducing an exploitable instance of this issue if return values of `ecrecover` are never checked.

## Recommendation  
**Short term:** Validate that the returned address of calling `ecrecover` is not zero.  
**Long term:** Add more unit testing to check that invalid signatures are properly handled throughout the codebase.

© 2019 Trail of Bits  
Dharma Labs Smart Wallet Review | 18

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Dharma Labs Smart Wallet |
| Report Date | N/A |
| Finders | eric.rafaloﬀ@trailofbits.com Dominik Czarnota, Eric Rafaloﬀ |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf

### Keywords for Search

`vulnerability`

