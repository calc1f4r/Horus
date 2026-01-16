---
# Core Classification
protocol: Kakeru Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51817
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/kakeru/kakeru-contracts
source_link: https://www.halborn.com/audits/kakeru/kakeru-contracts
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
  - Halborn
---

## Vulnerability Title

Lack of variable initialization

### Overview


This bug report discusses an issue with the `unstake` function in the **fund** contract. When this function is called, it is supposed to allow users to withdraw previously staked tokens. However, the first time it is executed, the `withdraw` function does not work properly because the variable `time2fullredemption` is not initialized. This results in different behavior for the contract the first time it is executed compared to subsequent executions. It is recommended to initialize the variable `time2fullredemption` to ensure consistent behavior for all executions of the contract. The `Kakeru team` has confirmed that this is the expected behavior and provided an explanation for it. No remediation plan is needed for this issue.

### Original Finding Content

##### Description

The `unstake` function of the **fund** contract allows to unstake and withdraw previously staked tokens.

However, the call to `withdraw`which is inside the `unstake` functiondoes not work the first time it is executed since the variable `time2fullredemption`used in the function `get_claim_able_token`is not initialized, having the same value as the variable `last_withdraw_time_user`.

This means that the behavior of the contract is not the same the first time it is executed as it is the following times.

![Unstake function](https://halbornmainframe.com/proxy/audits/images/66034c0653b13d194e093f56)![Withdraw function](https://halbornmainframe.com/proxy/audits/images/6603457153b13d194e093d1a)![get_claim_able_token function](https://halbornmainframe.com/proxy/audits/images/66034bc653b13d194e093f50)

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:M/D:L/Y:N/R:N/S:U (5.6)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:M/D:L/Y:N/R:N/S:U)

##### Recommendation

It is recommended to initialize the variable `time2fullredemption` before executing the `withdraw` function to have the same behavior in all executions of the contract. Otherwise, this could have unexpected consequences in the off chain modules that communicate with the contract.

Remediation Plan
----------------

**NOT APPLICABLE:** The `Kakeru team` have explained that this is the expected behavior:

1. *When the user deposits tokens into the* `fund` *contract, they receive* `ve_tokens`*.*
2. *To redeem tokens, the user first calls* `unstake`*. This destroys their* `ve_tokens` *and records the start time for linear release. On the first unstake, the* `withdraw` *method only records this start time. On subsequent unstakes, the withdraw method settles any previously unwithdrawn tokens.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Kakeru Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/kakeru/kakeru-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/kakeru/kakeru-contracts

### Keywords for Search

`vulnerability`

