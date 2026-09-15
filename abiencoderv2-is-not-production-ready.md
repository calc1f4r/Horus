---
# Core Classification
protocol: MCD Core Smart Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17051
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf
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
finders_count: 4
finders:
  - JP Smith
  - Sam Moelius
  - David Pokora
  - Rajeev Gopalakrishna
---

## Vulnerability Title

ABIEncoderV2 is not production-ready

### Overview

See description below for full details.

### Original Finding Content

## Type: Patching
**Target:** dss-deploy-scripts

**Difficulty:** Low

## Description
The contracts use the new Solidity ABI encoder, `ABIEncoderV2`. This encoder is still experimental and is not ready for production use. More than three percent of all GitHub issues for the Solidity compiler are related to experimental features, with `ABIEncoderV2` constituting the vast majority of them. Several issues and bug reports are still open and unresolved. More than 20 high-severity bugs over the past year have been associated with `ABIEncoderV2`, and some are so recent they have not yet been included in a Solidity release. For example, earlier this year a severe bug was found in the encoder and was introduced in Solidity 0.5.5.

## Exploit Scenario
The MakerDAO contracts are deployed. After the deployment, a bug is found in the encoder. As a result, the contracts are broken and can be exploited, perhaps to incorrectly value a CDP.

## Recommendation
Short term, do not use either `ABIEncoderV2` or any other experimental Solidity features. Refactor the code to avoid passing or returning arrays of strings to and from functions. Long term, integrate static analysis tools like Slither into your CI pipeline to detect unsafe pragmas.

© 2019 Trail of Bits

Multi-Collateral Dai Security Review | 16

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | MCD Core Smart Contracts |
| Report Date | N/A |
| Finders | JP Smith, Sam Moelius, David Pokora, Rajeev Gopalakrishna |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf

### Keywords for Search

`vulnerability`

