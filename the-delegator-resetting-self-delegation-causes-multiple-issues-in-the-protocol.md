---
# Core Classification
protocol: Templedao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33575
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Hans
---

## Vulnerability Title

The delegator resetting self-delegation causes multiple issues in the protocol

### Overview


This bug report describes an issue in the protocol where the vote power of delegators is not properly checked when it is changed. This can lead to problems in multiple parts of the protocol. For example, functions like `unsetUserVoteDelegate`, `_withdrawFor`, and `_stakeFor` do not properly handle changes in vote power and can result in reverts and allow attackers to gain infinite voting power. A proof of concept scenario is provided to demonstrate how this bug can be exploited. The recommended mitigation is to validate if the delegator has self-delegation enabled before executing these functions. The bug has been fixed in the TempleDAO project and verified by Cyfrin.

### Original Finding Content

**Description:** Whenever the vote power of delegators are changed, the validity of self-delegation of the delegator is not checked, which results in issues in multiple parts of the protocol.

- `unsetUserVoteDelegate`: It does not allow stakers to unset delegation through the function because it tries to subtract delegated balance from zero.
- `_withdrawFor`: It does not allow stakers to withdraw their assets because it tries to subtract delegated balance from zero.
- `_stakeFor`: It allows malicious stakers to get infinite voting power by repeating staking & modifying delegator & withdrawal process.

**Impact:** It allows attackers to repeat issues in `_stakeFor` to accumulate voting power, also it causes reverts in withdrawals.

**Proof of Concept:** Here's a scenario where a malicious attacker can get infinite voting power by repeating the following process:

1. Staker delegates to Bob.
2. Bob resets self-delegation.
3. The staker stakes the token.
4. The staker changes the delegation to another party.

**Recommended Mitigation:** In 3 functions above, it should validate if the delegator has self-delegation enabled at the time of function call.

**TempleDAO:** Fixed in [PR 1034](https://github.com/TempleDAO/temple/pull/1034)

**Cyfrin:** Verified

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Templedao |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

