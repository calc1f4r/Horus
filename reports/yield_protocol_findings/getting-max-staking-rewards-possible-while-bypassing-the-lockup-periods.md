---
# Core Classification
protocol: Sapien
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62039
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/index.html
source_link: https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/index.html
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
finders_count: 4
finders:
  - Paul Clemson
  - Julio Aguilar
  - Mostafa Yassin
  - Tim Sigl
---

## Vulnerability Title

Getting Max Staking Rewards Possible While Bypassing the Lockup Periods

### Overview


The client has marked a bug as "Fixed" and provided an explanation for the fix. The bug was related to the staking contract, which determines the multiplier a user gets based on staking amount and lockup period. However, the contract did not check if the lockup period had actually elapsed before allowing unstaking, leading to two potential consequences. The recommendation is to check the lockup period before initiating unstaking and limit the use of `instantUnstake()` to before the lockup period has ended.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `b175349`.

![Image 42: Alert icon](https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `228ae219c5478f375bed56376ffba8538ea2f09e`. The client provided the following explanation:

> The vulnerability was fixed by adding lock period validation checks across unstaking functions.

![Image 43: Alert icon](https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `228ae219c5478f375bed56376ffba8538ea2f09e`. The client provided the following explanation:

> The vulnerability was fixed by adding lock period validation checks across unstaking functions.

**File(s) affected:**`SapienStaking.sol`

**Description:** The staking contract determines the multiplier a user gets depending on the staking amount and the lockup period. Where the lockup period is the most important factor since it determines the max multiplier. However, any of the unstake-related functions check if the lockup period has actually elapsed. There are two consequences:

1.   A user can stake the needed amount for the max multiplier for 12 months to get the maximum rewards but only lock up the funds for two days after calling `initiateUnstake()` immediately after staking.
2.   A user can mistakenly call `instantUnstake()` after the lockup period has ended which would cost an unnecessary penalty.

**Recommendation:** We recommend to check that the lockup period has ended before allowing the user to initiate the unstaking process. Additionally, make sure the `instantUnstake()` can only be called before the lockup period has ended to avoid unnecessary penalties.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Sapien |
| Report Date | N/A |
| Finders | Paul Clemson, Julio Aguilar, Mostafa Yassin, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/index.html

### Keywords for Search

`vulnerability`

