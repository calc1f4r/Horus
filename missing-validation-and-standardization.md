---
# Core Classification
protocol: Internal Exchange Re-Assessment
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52031
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dappos/internal-exchange-re-assessment
source_link: https://www.halborn.com/audits/dappos/internal-exchange-re-assessment
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
  - Halborn
---

## Vulnerability Title

Missing Validation and Standardization

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `addPairInfo` function fails to validate and enforce critical constraints:

* **Token Equality**: No check ensures that `token0` and `token1` are distinct.
* **Token Standardization**: Tokens are not ordered consistently (e.g., lexicographically or by asset type).
* **Duplicate Pairs**: Multiple identical trading pairs (e.g., `ETH/USD`) can be added due to lack of uniqueness checks.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:L/A:N/D:N/Y:N/R:N/S:C (3.1)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:L/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

* **Validate Token Equality**: Add a requirement that `token0` and `token1` are distinct.

```
    require(token0 != token1, "Token0 and Token1 must be different");

```

* **Enforce Standardized Token Order**: Ensure `token0` is always the smaller address or the "base" token by predefined logic.

```
    if (token0 > token1) {
        (token0, token1) = (token1, token0);
    }

```

* **Prevent Duplicate Pairs**: Use a mapping to ensure each pair (`token0`, `token1`) is unique.

```
    mapping(address => mapping(address => bool)) public pairExists;

    require(!pairExists[token0][token1], "Trading pair already exists");
    pairExists[token0][token1] = true;

```

These changes ensure the integrity and consistency of trading pair configurations.

##### Remediation

**RISK ACCEPTED**: This problem does exist. However, the administrator will pay attention to the parameters.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Internal Exchange Re-Assessment |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/dappos/internal-exchange-re-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/dappos/internal-exchange-re-assessment

### Keywords for Search

`vulnerability`

