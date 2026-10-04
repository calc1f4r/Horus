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
solodit_id: 19486
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Insecure BytesLib Dependency

### Overview

See description below for full details.

### Original Finding Content

## Description

The `solidity-bytes-utils` v0.0.6 dependency has a critical vulnerability in the `BytesLib.slice()` method.  
See [here](https://github.com/GNSPS/solidity-bytes-utils#important-fixes-changelog) for more info.  
The current codebase does not expose this vulnerability, as user-supplied inputs are never passed to `BytesLib.slice()`.

## Recommendations

- Ensure any future updates to Lido avoid introducing user-supplied input to the arguments for `BytesLib.slice()`.
- Consider introducing documentation, automation, or procedures to check that future updates are consistent with this recommendation.
- When possible (i.e. when AragonOS can migrate to a newer version of Solidity), update to a newer version of the `solidity-bytes-utils` dependency.

## Resolution

The Lido team has acknowledged this in Issue #247 and will be careful to continue to avoid passing user-supplied input.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf

### Keywords for Search

`vulnerability`

