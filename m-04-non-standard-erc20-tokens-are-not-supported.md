---
# Core Classification
protocol: Mimo DeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2169
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-mimo-defi-contest
source_link: https://code4rena.com/reports/2022-04-mimo
github_link: https://github.com/code-423n4/2022-04-mimo-findings/issues/127

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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - robee
  - MaratCerby
  - ych18
  - defsec
---

## Vulnerability Title

[M-04] Non-standard ERC20 Tokens are Not Supported

### Overview


This bug report describes an issue with the SuperVault contract on the 2022-04-mimo GitHub repository. The problem occurs when trying to call the SuperVault.executeOperation function, which causes the transaction to revert. This is because the call to asset.approve() on line 97 does not match the expected function signature of approve() on the target contract, such as in the case of USDT. This issue can occur with any call to the approve function when the asset is an ERC20. The recommendation is to consider using the safeApprove of OZ to avoid this issue.

### Original Finding Content

_Submitted by ych18, also found by MaratCerby, robee, and defsec_

When trying to call `SuperVault.executeOperation`  the transaction reverts. This is because the call to `asset.approve()` in line{97} doesn't match the expected function signature of `approve()` on the target contract like in the case of USDT.

This issue exists in any call to approve function when the asset could be any ERC20.

Recommendation : consider using safeApprove of OZ

**[m19 (Mimo DeFi) acknowledged](https://github.com/code-423n4/2022-04-mimo-findings/issues/127)**

**[gzeoneth (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-04-mimo-findings/issues/127#issuecomment-1146832811):**
 > Judging as Med Risk as function availability could be impacted. Unlike the core protocol, `SuperVault` can take any token as input and USDT is listed on various lending protocol like AAVE.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mimo DeFi |
| Report Date | N/A |
| Finders | robee, MaratCerby, ych18, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-mimo
- **GitHub**: https://github.com/code-423n4/2022-04-mimo-findings/issues/127
- **Contest**: https://code4rena.com/contests/2022-04-mimo-defi-contest

### Keywords for Search

`vulnerability`

