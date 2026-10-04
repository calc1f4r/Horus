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
solodit_id: 31518
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] `adminSettleDebtLockPeriod` might not be long enough

### Overview


The report discusses a bug in the system that may prevent users from withdrawing their `stETH` in time before it is transferred to the `AdminLidoAdapter`. This could have a high impact on users, but the likelihood of it happening is low. The issue is that the `admin` has the ability to end the vault early, but there is a timelock in place to give users a chance to withdraw before the transfer happens. However, the timelock may not be long enough as it is currently set to 3 days and the withdrawal process can take anywhere between 1-5 days according to Lido. The recommendation is to increase the timelock to 5 or 6 days to give users more time to react.

### Original Finding Content

**Severity**

**Impact:** High as users might not be able to withdraw in time before their `stETH` is transferred to `AdminLidoAdapter`

**Likelihood:** Low, as it needs to be a delay in the queue for lido withdrawals and an event that causes admin to trigger settle debt

**Description**

`admin` has the ability to end the vault early in case of unforeseen circumstances. This is done by first calling `initiatingAdminSettleDebt` which triggers a timelock before `adminSettleDebt` can be called. This so that users can chose to withdraw before all `stETH` and pending withdraw requests are transferred to `AdminLidoAdapter`.

The timelock, `adminSettleDebtLockPeriod`, is set in `VaultFactory` to `3 days`.

This might however not be enough. Looking at what lido says the withdrawal requests can take anything between 1-5 days:
https://blog.lido.fi/ethereum-withdrawals-overview-faq/#:~:text=How%20does%20the,1%2D5%20days.

> How does the withdrawal process work?
> The withdrawal process is simple and has two steps:
>
> Request: Lock your stETH/wstETH by issuing a withdrawal request. ETH is sourced to fulfill the request, and then locked stETH is > burned, which marks the withdrawal request as claimable. **Under normal circumstances, this can take anywhere between 1-5 days.**

**Recommendations**

Consider increasing the timelock to 5 days, or 6 days to give stakers a day to react as well. As well as addressing [H-09].

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
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

