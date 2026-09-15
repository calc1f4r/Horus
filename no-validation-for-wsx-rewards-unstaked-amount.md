---
# Core Classification
protocol: Liquistake
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58501
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-08-LiquiStake.md
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
  - zokyo
---

## Vulnerability Title

No validation for WSX rewards / unstaked amount.

### Overview


The bug report discusses an issue with the StWSX.sol contract, specifically with the oracle Report Unstaked Withdraw() and ReportRewards() functions. The report states that there are no checks in place to confirm that the necessary amount of WSX has been transferred to the contract before reporting, which could potentially lead to incorrect reporting. The recommendation is to add validation for the balance before and after reporting, or to add a transferFrom() function for WSX into the reporting functions. The auditors also suggest adding a similar check to the withdraw/claim functions. The report concludes that the issue has been resolved with updates made to the process of rewards collection and unstaking. 

### Original Finding Content

**Description**

StWSX.sol, oracle Report Unstaked Withdraw(), oracle ReportRewards()
It is assumed that the necessary amount of WSX will already be present on the contract at the moment of reporting. However, there are no checks to show that the rewards / unstaked amount was actually transferred to the contract - either by Oracle or by another entity.

**Recommendation**

Add validation for the balance before and after reporting and/or add transferFrom() (or another hook) for WSX into the reporting functions. Auditors assume that such a check may also be added to the withdraw/claim functions, depending on the process of forwarding tokens from the Staking Proxy.

**Re-audit comment**

Resolved.

Post-audit. The process of processing the rewards collection and unstaking was updated as the auditors have suggested (See Info-12).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Liquistake |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-08-LiquiStake.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

