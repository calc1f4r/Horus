---
# Core Classification
protocol: Aarna
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37175
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-04-aarna.md
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

Centralization risk due to owner setting the protocol contracts

### Overview


This bug report discusses a medium severity issue that has already been resolved. The bug was found in the Contract AFiStorage.sol, where the owner can set the protocol contracts for aave, compound, and dydx using a method called afiSync(...). This could potentially be exploited by a malicious owner to set a malicious address for the protocol contracts, which could result in the loss of user funds. The recommendation is to use a 2/3 or 3/5 Multisig wallet or a secure governance mechanism to prevent this from happening. The issue has been fixed as recommended.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

In Contract AFiStorage.sol, the owner can set the protocol contracts for aave, compound and dydx using afiSync(...) method.

A malicious owner can utilize this to set malicious address for the protocol contracts where eventually users funds will be staked. This might be detrimental to the users such as the lenders
As they will lose their deposited fund.

**Recommendation**:  

It is advised to utilize at least a 2/3 or a 3/5 Multisig wallet used by different trusted participants or use a secure governance mechanism to decentralize its usage.
**Fix**: The issue has been fixed as recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Aarna |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-04-aarna.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

