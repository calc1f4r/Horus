---
# Core Classification
protocol: Karak-June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38496
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Karak-security-review-June.md
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

[M-01] The User can deny paying slashed tokens

### Overview


The report is about a bug in the system where slash tokens are not being transferred when the snapshot is expired. This happens because the user who initially withdrew their validator's balance and caused the slash event, did not call `startSnapshot()` and the snapshot expired. This prevents others from calling `validateExpiredSnapshot()` and transferring the slashed tokens. The recommendation is to fix the check in `validateExpiredSnapshot()` and check the expiration time of the previous snapshot's timestamp.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

Slash tokens only get transferred when `startSnapshot()` is called by the user or by others when the snapshot is expired. The issue is that if the user has no active validator then it won't be possible to call `validateExpiredSnapshot()` and slash tokens would stuck in the native node. This is the POC:

1. User1 withdraws all his validator's balance into the native node and updates the snapshot.
2. There's a slash event and native vault's users get slashed.
3. Now if User1 won't call `startSnapshot()` and the snapshot expires then others can't call `validateExpiredSnapshot()` and slashed tokens won't get transferred.

The reason why others can't call `validateExpiredSnapshot()` is because of this check:

```solidity
        if (validatorDetails.status != NativeVaultLib.ValidatorStatus.ACTIVE) revert ValidatorNotActive();
```

## Recommendations

Fix the check in the `validateExpiredSnapshot()` and check the expiration time of the previous snapshot's timestamp.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Karak-June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Karak-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

