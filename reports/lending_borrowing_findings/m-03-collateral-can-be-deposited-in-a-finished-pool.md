---
# Core Classification
protocol: Sublime
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1197
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-sublime-contest
source_link: https://code4rena.com/reports/2021-12-sublime
github_link: https://github.com/code-423n4/2021-12-sublime-findings/issues/169

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
  - cdp
  - services
  - leveraged_farming
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - pedroais
---

## Vulnerability Title

[M-03] Collateral can be deposited in a finished pool

### Overview


This bug report describes an issue with the depositCollateral function in the Pool contract. The function does not check the status of the loan before allowing collateral to be deposited, meaning that collateral can be deposited in a finished loan and all funds will be lost. The recommended mitigation step is to require loan status to be collection or active in the depositCollateral function. This will ensure that collateral can only be deposited in active loans, preventing users from losing funds.

### Original Finding Content

_Submitted by pedroais_

#### Proof of Concept

The depositCollateral function doesn't check the status of the pool so collateral can be deposited in a finished loan. This can happen by mistake and all funds will be lost.

<https://github.com/code-423n4/2021-12-sublime/blob/9df1b7c4247f8631647c7627a8da9bdc16db8b11/contracts/Pool/Pool.sol#L207>

#### Recommended Mitigation Steps

Require loan status to be collection or active in the depositCollateral function.

**[ritik99 (Sublime) disagreed with severity](https://github.com/code-423n4/2021-12-sublime-findings/issues/169#issuecomment-1001019540):**
 > We will add a check for this. The issue however stems from user error. Sending assets to an address without proper checks does not constitute an attack path imo. We would suggest a rating of (1) Low or (0) non-critical given the low likelihood and the impact of the attack (only the user making the incorrect transaction is affected)

**[0xean (judge) commented](https://github.com/code-423n4/2021-12-sublime-findings/issues/169#issuecomment-1018679575):**
 > `
> 2 — Med: Assets not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements.
> `
> 
> This definitely qualifies as "external requirements" and a simple check would assist in avoid it.




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sublime |
| Report Date | N/A |
| Finders | pedroais |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-sublime
- **GitHub**: https://github.com/code-423n4/2021-12-sublime-findings/issues/169
- **Contest**: https://code4rena.com/contests/2021-12-sublime-contest

### Keywords for Search

`vulnerability`

