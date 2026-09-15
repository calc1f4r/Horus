---
# Core Classification
protocol: Streamr
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27155
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
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
  - Hans
---

## Vulnerability Title

Operators can bypass a `leavePenalty` using `reduceStakeTo()`

### Overview


This bug report describes an issue with the `reduceStakeTo()` function in the Streamr Network Contracts. It states that operators should pay a leave penalty when they unstake earlier than expected, but there are no relevant requirements in `reduceStakeTo()` so they can reduce their staking amount to the minimum value, resulting in a lower penalty.

The impact of this bug is that operators will only pay the leave penalty for the minimum amount. The recommended mitigation is to ensure that the penalty is the same, regardless of whether an operator only calls `forceUnstake` or first calls `reduceStakeTo`.

The bug has been fixed in commit [72323d0](https://github.com/streamr-dev/network-contracts/commit/72323d0099a85c8c7a5d59335492eebcc9cc66bb) and verified by Cyfrin.

### Original Finding Content

**Severity:** Medium

**Description:** Operators should pay a leave penalty when they unstake earlier than expected.
But there are no relevant requirements in `reduceStakeTo()` so they can reduce their staking amount to the minimum value.

- An operator staked 100 and he wants to unstake earlier.
- When he calls `forceUnstake()`, he should pay `100 * 10% = 10` as a penalty.
- But if he reduces the staking amount to the minimum(like 10) using `reduceStakeTo()` first and calls `forceUnstake()`, the penalty will be `10 * 10% = 1.`

**Impact:** Operators will pay a `leavePenalty` for the minimum amount only.

**Recommended Mitigation:** The penalty should be the same, whether an Operator only calls `forceUnstake`, or first calls `reduceStakeTo`.

**Client:** Fixed in commit [72323d0](https://github.com/streamr-dev/network-contracts/commit/72323d0099a85c8c7a5d59335492eebcc9cc66bb).

**Cyfrin:** Verified

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Streamr |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

