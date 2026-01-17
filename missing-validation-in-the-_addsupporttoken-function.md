---
# Core Classification
protocol: Meson Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18101
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/MesonProtocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/MesonProtocol.pdf
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
  - Damilola Edwards
  - Alexander Remie
  - Tjaden Hess
---

## Vulnerability Title

Missing validation in the _addSupportToken function

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Report

## Diﬃculty: Low

## Type: Auditing and Logging

## Description
Insufficient input validation in the `_addSupportToken` function makes it possible to register the same token as supported multiple times. This does not cause a problem, because if there are duplicate entries for a token in the token list, the last one added will be the one that is used. However, it does mean that multiple indexes could point to the same token, while the token would point to only one of those indexes.

```solidity
function _addSupportToken(address token, uint8 index) internal {
    require(index != 0, "Cannot use 0 as token index");
    _indexOfToken[token] = index;
    _tokenList[index] = token;
}
```
*Source: contracts/utils/MesonTokens.sol*

## Recommendations
- **Short term**: Have `_addSupportToken` check that the token is not already registered in the mapping (i.e., that its index is greater than zero).
- **Long term**: Implement validation of function inputs whenever possible.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Meson Protocol |
| Report Date | N/A |
| Finders | Damilola Edwards, Alexander Remie, Tjaden Hess |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/MesonProtocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/MesonProtocol.pdf

### Keywords for Search

`vulnerability`

