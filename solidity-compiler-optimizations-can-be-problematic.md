---
# Core Classification
protocol: Rocket Pool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16555
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
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
  - Dominik Teiml
  - Devashish Tomar
  - Maximilian Krüger
---

## Vulnerability Title

Solidity compiler optimizations can be problematic

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: High

## Type: Access Controls

### Description
Rocket Pool has enabled optional compiler optimizations in Solidity. There have been several optimization bugs with security implications. Moreover, optimizations are actively being developed. Solidity compiler optimizations are disabled by default, and it is unclear how many contracts in the wild actually use them. Therefore, it is unclear how well they are being tested and exercised.

High-severity security issues due to optimization bugs have occurred in the past. A high-severity bug in the emscripten-generated solc-js compiler used by Truffle and Remix persisted until late 2018. The fix for this bug was not reported in the Solidity CHANGELOG. Another high-severity optimization bug resulting in incorrect bit shift results was patched in Solidity 0.5.6. More recently, another bug due to the incorrect caching of keccak256 was reported.

A compiler audit of Solidity from November 2018 concluded that the optional optimizations may not be safe. It is likely that there are latent bugs related to optimization and that new bugs will be introduced due to future optimizations.

### Exploit Scenario
A latent or future bug in Solidity compiler optimizations—or in the Emscripten transpilation to solc-js—causes a security vulnerability in the Rocket Pool contracts.

### Recommendations
- **Short term**: Measure the gas savings from optimizations and carefully weigh them against the possibility of an optimization-related bug.
- **Long term**: Monitor the development and adoption of Solidity compiler optimizations to assess their maturity.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Rocket Pool |
| Report Date | N/A |
| Finders | Dominik Teiml, Devashish Tomar, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf

### Keywords for Search

`vulnerability`

