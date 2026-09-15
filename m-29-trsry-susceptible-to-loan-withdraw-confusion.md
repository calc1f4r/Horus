---
# Core Classification
protocol: Olympus DAO
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3233
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-olympus-dao-contest
source_link: https://code4rena.com/reports/2022-08-olympus
github_link: https://github.com/code-423n4/2022-08-olympus-findings/issues/75

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - business_logic
  - approve

protocol_categories:
  - liquid_staking
  - yield
  - cross_chain
  - leveraged_farming
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - tonisives
  - Trust
  - 0xSky
  - datapunk
---

## Vulnerability Title

[M-29] TRSRY susceptible to loan / withdraw confusion

### Overview


This bug report is about a vulnerability in the code of a software system. The code in question is located at the GitHub link provided, and the vulnerability allows users with the permission to take out a loan to directly withdraw funds without registering it as a loan. This could have serious financial implications for the system. 

The proof of concept provided in the report outlines how the vulnerability could be exploited. The recommended mitigation steps suggest implementing a separate mapping called loanApproval and creating two new functions, setLoanApprovalFor() and getLoan(), to set and reduce the loanApproval balance, respectively. This would ensure that any loans taken out are properly registered and tracked. 

In conclusion, this bug report outlines a vulnerability in the code of a software system that could have serious financial implications if exploited. The recommended mitigation steps provided in the report should be implemented to ensure that any loans taken out are properly registered and tracked.

### Original Finding Content

_Submitted by Trust, also found by 0xSky, datapunk, and tonisives_

<https://github.com/code-423n4/2022-08-olympus/blob/main/src/modules/TRSRY.sol#L64-L102><br>

Treasury allocates approvals in the withdrawApproval mapping which is set via setApprovalFor(). In both withdrawReserves() and in getLoan(), \_checkApproval() is used to verify user has enough approval and subtracts the withdraw / loan amount. Therefore, there is no differentiation in validation between loan approval and withdraw approval. Policies which will use getLoan() (currently none) can simply withdraw the tokens without bookkeeping it as a loan.

### Proof of Concept

1.  Policy P has getLoan permission
2.  setApprovalFor(policy, token, amount) was called to grant P permission to loan amount
3.  P calls withdrawReserves(address, token, amount) and directly withdraws the funds without registering as loan

### Recommended Mitigation Steps

A separate mapping called loanApproval should be implemented, and setLoanApprovalFor() will set it, getLoan() will reduce loanApproval balance.

**[ind-igo (Olympus) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2022-08-olympus-findings/issues/75#issuecomment-1239657706):**
 > Confirmed. Good suggestion. Would put as low risk though.

**[0xean (judge) commented](https://github.com/code-423n4/2022-08-olympus-findings/issues/75#issuecomment-1250396074):**
 > Currently thinking Medium is appropriate for this issue, but will circle back on it. 

**[0xean (judge) commented](https://github.com/code-423n4/2022-08-olympus-findings/issues/75#issuecomment-1251404052):**
 > See [#293](https://github.com/code-423n4/2022-08-olympus-findings/issues/293) for a possible vector in which this could lead to loss of funds.  Going to leave as Medium.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Olympus DAO |
| Report Date | N/A |
| Finders | tonisives, Trust, 0xSky, datapunk |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-olympus
- **GitHub**: https://github.com/code-423n4/2022-08-olympus-findings/issues/75
- **Contest**: https://code4rena.com/contests/2022-08-olympus-dao-contest

### Keywords for Search

`Business Logic, Approve`

