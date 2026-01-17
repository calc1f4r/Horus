---
# Core Classification
protocol: Ethereum Reserve Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51113
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/erd/ethereum-reserve-dollar-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/erd/ethereum-reserve-dollar-smart-contract-security-assessment
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

LONG LITERAL UINT256 USED IN COLLATERALMANAGER

### Overview

See description below for full details.

### Original Finding Content

##### Description

Critical protocol parameters are set within the `initialize()` function of `CollateralManager.sol` contract. Specifically, `MCR` (minimum collateral ratio) and `CCR` (critical collateral ratio) are set using a long literal. This can lead to confusion on the percentages configured for the correct functionality of the whole protocol.

Code Location
-------------

#### CollateralManager.sol

```
function initialize() public initializer {
    __Ownable_init();
    BOOTSTRAP_PERIOD = 14 days;
    MCR = 1100000000000000000; // 110%
    CCR = 1300000000000000000; // 130%
    EUSD_GAS_COMPENSATION = 200e18;
    MIN_NET_DEBT = 1800e18;
    BORROWING_FEE_FLOOR = (DECIMAL_PRECISION / 10000) * 75; // 0.75%

    REDEMPTION_FEE_FLOOR = (DECIMAL_PRECISION / 10000) * 75; // 0.75%
    RECOVERY_FEE = (DECIMAL_PRECISION / 10000) * 25; // 0.25%
    MAX_BORROWING_FEE = (DECIMAL_PRECISION / 100) * 5; // 5%
}

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:P/S:U (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:P/S:U)

##### Recommendation

**SOLVED**: The `ERD team` solved the issue with the following commit ID.

`Commit ID :` [0aaf1539e5897aca96034f20f82a0ec1a8d45182](https://github.com/Ethereum-ERD/dev-upgradeable/commit/0aaf1539e5897aca96034f20f82a0ec1a8d45182)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Ethereum Reserve Dollar |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/erd/ethereum-reserve-dollar-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/erd/ethereum-reserve-dollar-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

