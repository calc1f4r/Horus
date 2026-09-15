---
# Core Classification
protocol: Plume Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52651
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/plume/plume-contracts
source_link: https://www.halborn.com/audits/plume/plume-contracts
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

Missing Validation for Zero Addresses in Constructor

### Overview

See description below for full details.

### Original Finding Content

##### Description

The constructors of both the `Distributor.sol` and `Staking.sol` contracts do not check if critical addresses (e.g., `_signer`, `_token`, `_staking`, `_stakingToken`) are zero.

  

Deploying contracts with zero addresses could lead to unexpected behavior or vulnerabilities, such as misdirected operations or inability to use the contract as intended.

##### BVSS

[AO:A/AC:L/AX:H/R:N/S:U/C:N/A:M/I:N/D:N/Y:N (1.7)](/bvss?q=AO:A/AC:L/AX:H/R:N/S:U/C:N/A:M/I:N/D:N/Y:N)

##### Recommendation

It is recommended to add explicit checks in the constructor to revert if any of the provided addresses are zero.

##### Remediation

**ACKNOWLEDGED:** The **Plume team** has acknowledged this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Plume Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/plume/plume-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/plume/plume-contracts

### Keywords for Search

`vulnerability`

