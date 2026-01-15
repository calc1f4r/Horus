---
# Core Classification
protocol: Umami
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44590
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-04-19-Umami.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

ChainLink successfull response not implemented correctly

### Overview


A bug has been reported in the ChainLinkWrapper contract, which is used to connect to external data sources. The bug affects the function _getCurrentChainlinkResponse, which is not properly assigning a value to the success field in the OracleResponse structure. This can cause successful calls to fail in the function _isBadOracleResponse. The recommendation is to assign a true value to the success field in the response structure. It should also be noted that the Chainlink wrapper has been removed and is no longer in use.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

The ChainLinkWrapper contract is not properly implementing the case where the oracle is responding successfully, this is originating from function _getCurrentChainlinkResponse L#168, the function is not assigning any value to the field success field from structure OracleResponse, this will make the successful call to fail in the check from function _isBadOracleResponse


**Recommendation**: 

Assign the true value for the sucess field from the response struct

More explanations → Untitled document

**Note**: Chainlink wrapper was removed, unused
https://github.com/UmamiDAO/V2-Vaults/commit/4419ae6e85f59ef5c3d711ec0c8f7b942620fe90

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Umami |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-04-19-Umami.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

