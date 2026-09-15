---
# Core Classification
protocol: Tokensfarm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57471
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-13-TokensFarm.md
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

No money back.

### Overview


The report states that there is a bug in the TokensFarm.sol and Perpetual TokensFarm contracts, specifically in the function deposit or makeDepositRequest. If the contracts allow commission to be paid in eth and the user sends more than the required amount, the excess amount is not returned to the user. The recommendation is to fix this issue and also consider the potential vulnerability of reentrancy. The re-audit comment says that the issue has been resolved by replacing the >= symbol with ==. 

### Original Finding Content

**Description**

TokensFarm.sol / Perpetual TokensFarm, function deposit / makeDepositRequest

If the farm contracts allow commission via eth (isFlatFeeAllowed), and the user sends eth more than the required limit, the rest will not be returned to him.

**Recommendation**

Add the processing of this case, returning the balance of the necessary funds to the user. Be careful and consider the reentrancy vulnerability.

**Re-audit comment**

Resolved.

From client:

>= was replaced with ==

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tokensfarm |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-13-TokensFarm.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

