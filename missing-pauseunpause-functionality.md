---
# Core Classification
protocol: LMCV part 1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50706
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment
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

MISSING PAUSE/UNPAUSE FUNCTIONALITY

### Overview

See description below for full details.

### Original Finding Content

##### Description

In case a hack occurs, or an exploit is discovered, the team should be able to pause functionality until the necessary changes are made to the system.
To use a THORchain example again, the team behind THOR chain noticed an attack was going to occur well before the
system transferred funds to the hacker. However, they were unable to shut the system down fast enough (According to the [incident report](https://github.com/HalbornSecurity/PublicReports/blob/master/Incident%20Reports/Thorchain_Incident_Analysis_July_23_2021.pdf)).

In case of the contracts in scope, only `LMCV` and `LMCVProxy` can be stopped/resumed. Other contracts can only be disabled by the `cage` function (`CollateralJoin` and `CollateralJoinDecimals`) or do not have such possibility at all (`PSM`, `dPrimeJoin`).

##### Score

Impact: 3  
Likelihood: 2

##### Recommendation

**SOLVED**: The `cage` function was modified, and the `setLive` function was added to the contracts. Now all contracts except `dPrime` and `dPrimeJoin` can be stopped/resumed in case of an attack.

* [CollateralJoin.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/CollateralJoin.sol#L103)
* [CollateralJoinDecimals.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/CollateralJoinDecimals.sol#L80)
* [PSM.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/PSM.sol#L165)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | LMCV part 1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

