---
# Core Classification
protocol: Ozean Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49227
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Ozean%20Finance/README.md#12-missing-parameters-checks-in-lgestaking-constructor
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
  - MixBytes
---

## Vulnerability Title

Missing Parameters Checks in `LGEStaking` Constructor

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified within the constructor of the `LGEStaking` contract.

The constructor [lacks some validation checks](https://github.com/LayerLabs-app/Ozean-Contracts/blob/dacd9ed9c895c9b6be422531eea15fecc3c2b1d8/src/L1/LGEStaking.sol#L72-L93) for the input parameters. Specifically:
1. There is no check to ensure that `_owner` and `_wstETH` are non-zero addresses.
2. The `_tokens` array is not checked for duplicate addresses.

The issue is classified as **Low** severity because these omissions can be mitigated during deployment with careful input validation.

##### Recommendation
We recommend adding the following checks to the constructor:
1. Ensure `_owner` and `_wstETH` are non-zero addresses.
2. Verify that the `_tokens` array does not contain duplicate entries by adding here the following line:
`require(!allowlisted[_tokens[i]], "USDXBridge: Duplicate tokens.");`

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Ozean Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Ozean%20Finance/README.md#12-missing-parameters-checks-in-lgestaking-constructor
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

