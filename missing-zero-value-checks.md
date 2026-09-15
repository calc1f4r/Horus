---
# Core Classification
protocol: LMCV part 3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50683
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/damfinance/lmcv-part-3-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/damfinance/lmcv-part-3-smart-contract-security-assessment
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

MISSING ZERO VALUE CHECKS

### Overview

See description below for full details.

### Original Finding Content

##### Description

It was identified that within the code, several functions were lacking zero address or zero value validation on important parameters. Setting invalid parameters in the examples below might result in loss of funds, waste of gas, lose of administrative controls, or reverting during important operations:

Missing zero address checks:

`LayerZero/dPrimeConnectorLZ.sol`:

* Line 24 `constructor` is missing zero-address checks for `_lzEndpoint`, `_dPrimeContract`.

`hyperlane/dPrimeConnectorHyperlane.sol`:

* Line 71 `initialize` is missing zero-address checks for `_abacusConnectionManager`, `_interchainGasPaymaster`, `dPrimeContract`.
* Line 95 `transferRemote` is missing zero-address check for `_recipient`.

`dPrimeGuardian.sol`

* Line 16: `constructor` is missing zero-address check for `_dPrimeContract`.

It is also recommended to validate the following parameters and variables:

`hyperlane/dPrimeConnectorHyperlane.sol`:

* Line 95 `transferRemote` is missing zero value checks for `_destination`, `_amount`.
* Line 142 `retry` is missing zero-value check for `amount`.

##### Score

Impact: 3  
Likelihood: 1

##### Recommendation

**SOLVED**: The `DAMfinance team` solved the issue in commit [cfc13a8](https://github.com/DecentralizedAssetManagement/lmcv/commit/cfc13a806ba391c8875f9d363ee5b35b9a8f8acf) by adding checks where appropriate.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | LMCV part 3 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/damfinance/lmcv-part-3-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/damfinance/lmcv-part-3-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

