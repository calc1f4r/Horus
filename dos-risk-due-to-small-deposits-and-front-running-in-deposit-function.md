---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43838
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Genesis%20Staking/README.md#2-dos-risk-due-to-small-deposits-and-front-running-in-deposit-function
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
  - MixBytes
---

## Vulnerability Title

DoS Risk Due to Small Deposits and Front-Running in `deposit` Function

### Overview


This bug report is about a problem with the `deposit` function in the `Prestaking` contract. There are two ways that someone could exploit this function to disrupt the staking system. One way is by making very small deposits (1 wei) which would make it difficult for others to use the system. The other way is by front-running other users' transactions, causing them to fail due to a limit being exceeded. This could prevent valid users from depositing tokens. To fix this issue, the report suggests implementing a minimum deposit amount and adjusting the logic to prevent deposits from exceeding the limit. The severity of this issue is classified as medium.

### Original Finding Content

##### Description
This issue has been identified in the `deposit` function of the `Prestaking` contract.
There are two potential attack vectors that could be used to DoS the system:

1. **Small Deposits (1 wei deposits)**: Malicious users can fill the `stakingWallets` with extremely small deposits (e.g., 1 wei), which would make it harder to use the system effectively. Adding a minimum deposit amount would prevent such attacks by ensuring that deposits are meaningful, thus limiting the attacker's ability to spam the system with tiny amounts.
  
2. **Front-Running the Max Token Limit**: A malicious user could front-run other transactions by depositing a small amount (e.g., 1 wei) just before another user's deposit, which would cause the second transaction to revert due to the `maxTokens` limit being breached. This is a denial-of-service risk that can be mitigated by adjusting the logic to ensure that deposits do not push the total amount beyond the `maxTokens` limit.

The issue is classified as **Medium** severity because it can be exploited to disrupt the normal operation of the staking system, potentially preventing valid users from depositing tokens.
##### Recommendation
- **Minimum Deposit Requirement**: Implement a minimum deposit amount to ensure that users cannot spam the system with tiny deposits.
- **Max Token Check**: Ensure that deposits do not exceed the `maxTokens` limit by using `maxTokens` instead of `amount` if `amount > maxTokens` is true.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Genesis%20Staking/README.md#2-dos-risk-due-to-small-deposits-and-front-running-in-deposit-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

