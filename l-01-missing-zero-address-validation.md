---
# Core Classification
protocol: Gluex V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61342
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/GlueX-V2-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-01] Missing Zero Address Validation

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

The contracts were found to be setting immutable addresses without proper validations for zero addresses.

## Location of Affected Code

File: [router_v1/GluexRouter.sol#L106](https://github.com/gluexprotocol/gluex_router_contract/blob/9c754a3985fa32b72d847c88c83575f29a86bc01/router_v1/GluexRouter.sol#L106)

```solidity
constructor(address gluexTreasury, address nativeToken) {
    // Ensure the addresses are not zero
    checkZeroAddress(gluexTreasury);

    _gluexTreasury = gluexTreasury;
@>> _nativeToken = nativeToken;
}
```

## Impact

If address type parameters do not include a zero-address check, contract functionality may become unavailable.

## Recommendation

Add a zero address validation to all the functions where addresses are being set.

## Team Response

Acknowledged.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Gluex V2 |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/GlueX-V2-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

