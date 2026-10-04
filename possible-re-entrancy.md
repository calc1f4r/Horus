---
# Core Classification
protocol: Railgun
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44483
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-12-21-Railgun.md
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

Possible re-entrancy

### Overview


A medium severity bug has been found and resolved in the RailgunSmartWallet.sol file. The issue occurs when an ERC20 token with a callback function is used in the transfer method or an ERC721 token is used in the transferFrom method, making the smart wallet vulnerable to a re-entrancy attack. To prevent this, it is recommended to ensure that the same transaction cannot be sent twice within one blockchain transaction by marking the hash as processed before sending any tokens. 

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**File**: RailgunSmartWallet.sol

**Function**: transact

**Details**:

In the case there'll be an ERC20 token with the callback functionality within the transfer method or an ERC721 within the transferFrom method, it's possible to have a re-entrancy attack.

**Recommendation**: 

make sure that the same Transaction could not be sent twice withing one blockchain tx. This could be done, for example, by marking the hash as processed before sending any tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Railgun |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-12-21-Railgun.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

