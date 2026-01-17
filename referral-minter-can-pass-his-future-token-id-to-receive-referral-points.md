---
# Core Classification
protocol: Metropolis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57427
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-29-Metropolis.md
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

Referral minter can pass his future token id to receive referral points.

### Overview


The bug report is about a function called referralMint() in a contract called AccessTokenContract.sol. This function allows a user to pre-compute a new item ID and use it as a referrerTokenld, which will give them referral points. However, there is a potential issue where the user can use their own newitemid as a referrerTokenld, which could result in them receiving referral points for themselves. The recommendation is to check that the referrerTokenld exists and is not the same as the newitemid. This issue has been resolved.

### Original Finding Content

**Description**

AccessTokenContract.sol: function referralMint(). Message sender can pre compute a newItemid, which will be minted to him and pass it as referrer Tokenld, thus receive referral points for himself. Also, having the opportunity to have several passports - the user can specify his referrerTokenld from his other passport.

**Recommendation**

Verify that referrerTokenld exists and is not equal to newitemid.

**Re-audit comment**

Resolved

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Metropolis |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-29-Metropolis.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

