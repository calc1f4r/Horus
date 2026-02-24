---
# Core Classification
protocol: Zerolend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45867
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-26-Zerolend.md
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

Missing call to _disableInitializers

### Overview


The report states that there is a bug in the TokenEmissionsStrategy contracts where they are using the Initializable module but do not have a constructor that calls _disableInitializers(). This can allow an attacker to take over an uninitialized contract, which can impact both the proxy and its implementation contract. To prevent this, it is recommended to call _disableInitializers() in the constructor to lock the implementation contract upon deployment. This will help prevent any potential attacks. 

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

The TokenEmissionsStrategy contracts are using the Initializable module and doesn’t have a constructor that calls _disableInitializers().  

An uninitialized contract can be taken over by an attacker. This applies to both a proxy and its implementation contract, which may impact the proxy. To prevent the implementation contract from being used, you should invoke the _disableInitializers() function in the constructor to automatically lock it when it is deployed, more information can be found here.

 **Recommendation**: 
 
 Consider calling _disableInitializers()in the constructor.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zerolend |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-26-Zerolend.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

