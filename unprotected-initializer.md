---
# Core Classification
protocol: Stablr
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57456
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-08-StablR.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Unprotected initializer.

### Overview


The report discusses a bug found in the v2/FiatTokenV2.sol and v2/FiatTokenV2_1.sol functions, specifically in the initializeV2() function. This function is used as an additional initializer after a token upgrade. However, the second version is not initialized in an atomic way and requires a separate call, which could potentially lead to unauthorized access. The report recommends adding protection against unauthorized calls or providing a deployment/upgrade script to ensure proper initialization. The team responsible for the code has acknowledged the issue and plans to mitigate it by running a deployment and initialization before making an announcement. 

### Original Finding Content

**Description**

v2/FiatTokenV2.sol, initializeV2()

v2/Fiat TokenV2_1.sol, initializeV2_1()

Function serves as additional initializer after the token upgrade. Though, since the second version is not initialized in an atomic way (like it was for the first version initialized during the Proxy contract creation) and requires a separate call it should be protected against unauthorized calls (e.g. restricted to the owner only). Or, there should be a proof that function will be called through the AdminProxy upgradeAndCall() (e.g. with the appropriate deployment script). The issue is marked as high, since the initialization will change the storage to contain a new name and update initialization version. Though it is not critical, since it does not change critical for the protocol storage.

**Recommendation**

Add appropriate protection against unauthorized call, or provide a deployment/upgrade script with transparent upgradeAndCall() call.

**Re-audit comment**

Acknowledged.

Post-audit:

StablR team is acknowledged of the issue and stated that is the acceptable risk. StablR team will mitigate it by running deployment and initialization before announcement, after that it is immutable. Additionally StablR team will carefully check what happens after deployment, as they can spot what activity takes place subsequently.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Stablr |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-08-StablR.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

