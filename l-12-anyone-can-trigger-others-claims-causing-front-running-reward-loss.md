---
# Core Classification
protocol: BOB-Staking_2025-10-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63735
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/BOB-Staking-security-review_2025-10-18.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-12] Anyone can trigger others' claims causing front-running reward loss

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

`claimRewards(address receiver)` lets **any caller** pass any `receiver`:

```solidity
function claimRewards(address receiver) external nonReentrant {
    _claimRewards(receiver, true);
}
```

Inside `_claimRewards`, the contract settles the **receiver’s** rewards. When `rewardTokenBalance` is low, only a small portion is staked and the rest is pushed into `residualRewardBalance[receiver]` (paid later as a plain transfer, not compounded).

A malicious actor can **front-run** a user’s own claim and call `claimRewards` to diminish `rewardTokenBalance`   This forces the victim’s rewards into `residualRewardBalance` (and zeroes their `unclaimedRewards`) right before the victim tries to auto-compound, making the victim **miss compounding yield** on the residual portion. No theft occurs, but it’s a repeatable **grief** that reduces the victim’s APR.

**Recommendations**
Restrict self-claims only:** require `receiver == msg.sender`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | BOB-Staking_2025-10-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/BOB-Staking-security-review_2025-10-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

