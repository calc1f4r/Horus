---
# Core Classification
protocol: Saffron
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31511
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.40
financial_impact: high

# Scoring
quality_score: 2
rarity_score: 2

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-05] Funds in vault can be temporarily locked by spamming dust deposits and withdrawals

### Overview


This bug report talks about an issue in the `finalizeVaultEndedWithdrawals()` function which is used to finalize fixed withdrawals. The problem is that the function iterates through a list of users which can be manipulated by an attacker, causing it to become unbounded and leading to a denial of service (DoS) attack. This can result in the funds in the vault being temporarily locked. The severity of this bug is classified as medium because it can be fixed by using the "settle debt" function. Another issue mentioned is that an attacker can prevent the vault from starting by spamming small deposits and withdrawing them at the right time. To mitigate this, it is recommended to set a higher minimum deposit amount and ensure that the unfilled capacity is not less than this amount.

### Original Finding Content

**Severity**

**Impact:** Medium, funds in vault will be temporarily locked

**Likelihood:** High, can always occur

**Description**

`finalizeVaultEndedWithdrawals()` is required to be called to finalize all fixed withdrawals, including on-going fixed withdrawals.

The issue is that it iterates through `fixedOngoingWithdrawalUsers`, which can be manipulated and become unbounded. An attacker can make `fixedOngoingWithdrawalUsers` extremely large by spamming dust fixed deposits of 100 wei (with multiple EOA) and then withdraw them when vault is on-going. This will cause `finalizeVaultEndedWithdrawals()` to be DoS, which prevents withdrawals when vault ends, resulting in the vault funds locked.

I have classified this as Medium impact as admin can recover the issue with settle debt function.

Another issue that can occur with dust deposits and withdrawals is that an attacker can prevent vault from starting. The attack can conducted by spamming multiple 1 wei variable deposits and then withdraw one of them whenever vault is going to start by frontrunning the last depositor.

**Recommendations**

One possible mitigation is to increase the attack cost by setting a higher minimum deposit amount (e.g. 0.1 ETH) for fixed/variable participants.

Take note to ensure deposits do not cause unfilled capacity to be less than the minimum deposit amount, otherwise it will prevent vault from starting.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 2/5 |
| Rarity Score | 2/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Saffron |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

