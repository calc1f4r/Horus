---
# Core Classification
protocol: Moonscape
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52695
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/seascape/moonscape-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/seascape/moonscape-smart-contract-security-assessment
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

MISSING PARAMETERS VALIDATION

### Overview

See description below for full details.

### Original Finding Content

##### Description

None

Code Location
-------------

#### game/MoonscapeGame.sol

```
    constructor(
        address _mscpToken,
        address _cityNft,
        address _roverNft,
        address _scapeNft,
        address _verifier,
        address _feeTo
    ) public {
        MSCP = _mscpToken;
        cityNft = _cityNft;
        roverNft = _roverNft;
        scapeNft = _scapeNft;
        verifier = _verifier;
        feeTo = _feeTo;
    }

```

##### Score

Impact: 2  
Likelihood: 3

##### Recommendation

**SOLVED**: The code is now checking if the parameters are not zero.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Moonscape |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/seascape/moonscape-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/seascape/moonscape-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

