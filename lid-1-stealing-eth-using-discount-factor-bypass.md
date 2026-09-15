---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53465
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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
  - Hexens
---

## Vulnerability Title

[LID-1] Stealing ETH using discount factor bypass

### Overview


This bug report discusses a critical issue in a smart contract that handles withdrawal requests. The problem lies in the calculation of a discount factor, which is used to determine the actual amount of ETH that a user can withdraw. Due to an incorrect comparison in the code, a user can bypass a necessary check and claim a larger amount of ETH than they should be able to. This can lead to theft of ETH from other users in the withdrawal queue. The recommended fix is to replace a variable in the code, and the issue has been resolved.

### Original Finding Content

**Severity:** Critical

**Path:** WithdrawalQueueBase.sol:_claimWithdrawalTo#L428-L462

**Description:**

Whenever a batch of withdrawal requests is finalised, a discount factor is calculated and a checkpoint is created if the new factor differs. The discount factor is calculated as the actual amount of ETH divided by the total requested amount and only the actual amount of ETH is locked.

When the user claims their withdrawal request, they would only receive their portion of the actual amount of ETH by multiplying their request amount with the discount factor.

We found that there is an incorrect comparison in `_claimWithdrawalTo` on line 449: The next checkpoint’s `fromId` is compared with `_hint` instead of `_requestId`. As a result, this check can be entirely bypassed and allows a user to choose any checkpoint from the past with a better (or no) discount factor.

As a result, any user would be able to always claim the full amount, even though that ETH is not actually there in the contract. Too much ETH would be subtracted from the locked ETH counter and other withdrawal requests will not be claimable anymore.

The vulnerability can therefore be used to steal ETH from other users in the withdrawal queue.

```
if (_hint + 1 <= lastCheckpointIndex) {
    if (_getCheckpoints()[_hint + 1].fromId <= _hint) {
        revert InvalidHint(_hint);
    }
}
```


**Remediation:**  Replace `_hint` with `_requestId` on line 449 in `WithdrawalQueueBase.sol`.

**Status:** Fixed



- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

