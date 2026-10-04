---
# Core Classification
protocol: stHYPE_2025-10-13
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63214
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/stHYPE-security-review_2025-10-13.md
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

[M-02] Deposits might fail if staking module account is not activated

### Overview


The report discusses a bug that has been resolved in a staking module. The bug occurs when the staking module tries to deposit HYPE into HyperCore's spot balance, but fails if the staking module account has never received funds in the L1. This causes the deposited HYPE to disappear from the total balance, leading to a lower total supply and other issues. The recommended solution is to add a check in the staking module to ensure that the account has been activated in HyperCore before depositing funds.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Low

## Description

On `deposit()`, the staking module sends HYPE to HyperCore's spot balance and then moves it to the staking balance. However, if the staking module account has not been activated in HyperCore (i.e., it has never received funds in the L1), then the deposit will fail silently.

As a result:

- The deposited HYPE will disappear from the total balance, as it is not credited to the spot balance until the account is activated. This will cause the total supply to be lower than expected, similar to the occurrence of a slashing event, leading to different issues, as the share price decreasing and the protocol receiving extra fees once the supply is recovered.

- Once the account is activated, the deposited HYPE will be available in the spot balance. This will require the manager to withdraw the funds to the EVM and then re-deposit them, as there is no function to move funds from spot to staking balance directly.

## Recommendations

Add a check in `addStakingModule()` to ensure that the staking module account has been activated in HyperCore, using the `PrecompileLib.coreUserExists()` function.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | stHYPE_2025-10-13 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/stHYPE-security-review_2025-10-13.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

