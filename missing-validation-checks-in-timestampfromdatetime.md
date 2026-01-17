---
# Core Classification
protocol: Coinbase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53151
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/28ee39b6-39e6-40fc-905e-31d7830e6ded
source_link: https://cdn.cantina.xyz/reports/cantina_berachain_nitro_december2024.pdf
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
  - Om Parikh
  - 0xWeiss
---

## Vulnerability Title

Missing validation checks in timestampFromDateTime 

### Overview

See description below for full details.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
In function `timestampFromDateTime`, it checks if `year >= 1970` but other input fields are not checked. Any values can be passed for month, day, hour, minute, second and will be accepted, leading to undefined behavior.

This may be protected currently implicitly by assuring that signed data was not tampered with at the call site where this library is currently used, but if the `Asn1Decode` library is used in isolation, it will lead to issues described above.

## Recommendation
```solidity
function timestampFromDateTime(
    uint256 year,
    uint256 month,
    uint256 day,
    uint256 hour,
    uint256 minute,
    uint256 second
) internal pure returns (uint256) {
    require(year >= 1970);
    // @audit add validator for month, day, hour, minute, second
    int256 _year = int256(year);
    int256 _month = int256(month);
    int256 _day = int256(day);
    int256 _days = _day - 32075 + 1461 * (_year + 4800 + (_month - 14) / 12) / 4
        + 367 * (_month - 2 - (_month - 14) / 12 * 12) / 12 - 3 * ((_year + 4900 + (_month - 14) / 12) / 100)
        / 4 - 2440588;
    return ((uint256(_days) * 24 + hour) * 60 + minute) * 60 + second;
}
```

## Coinbase
Fixed in PR 7.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Coinbase |
| Report Date | N/A |
| Finders | Om Parikh, 0xWeiss |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_berachain_nitro_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/28ee39b6-39e6-40fc-905e-31d7830e6ded

### Keywords for Search

`vulnerability`

