---
# Core Classification
protocol: INIT Capital
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29600
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-initcapital
source_link: https://code4rena.com/reports/2023-12-initcapital
github_link: https://github.com/code-423n4/2023-12-initcapital-findings/issues/13

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

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - 0x73696d616f
  - rvierdiiev
  - ladboy233
---

## Vulnerability Title

[M-09] If wLP is blacklisted, then user will not be able to withdraw it

### Overview


The bug report discusses an issue with the InitCapital platform where users are unable to withdraw wLP tokens that they have previously deposited as collateral. This is because the wLP tokens may be blacklisted by the governor, which prevents users from withdrawing them. This also affects the ability of liquidators to liquidate positions that are collateralized with blacklisted wLP tokens. The sponsor has proposed a solution to decrease the collateral factor for blacklisted wLP tokens until it reaches 0, and then blacklist the token. However, this could still prevent users from withdrawing their tokens if they have not decollateralized them yet. The impact of this bug is that users are unable to withdraw their wLP tokens after they have been blacklisted. The recommended mitigation steps suggest allowing users to withdraw their tokens even if they have been blacklisted, as the health check function ensures that the position has enough collateral. The bug was reported using VsCode. The sponsor has acknowledged the issue and stated that they will use unwhitelisting with caution.

### Original Finding Content


When users deposit wLP tokens as collateral, then they are checked [to be whitelisted](https://github.com/code-423n4/2023-12-initcapital/blob/main/contracts/core/InitCore.sol#L255).

Later, it's possible that for some reason wLP token [will be blacklisted](https://github.com/code-423n4/2023-12-initcapital/blob/main/contracts/core/Config.sol#L145) by governor. And once it's done, then users who already used that wLP token as collateral [will not be able to withdraw them](https://github.com/code-423n4/2023-12-initcapital/blob/main/contracts/core/InitCore.sol#L275).

Also same thing exists for the `liquidateWLp` function, which means that in case if position, that is collateralized with wLP that is blacklisted, will become unhealthy, then liquidators [will not be able to liquidate it](https://github.com/code-423n4/2023-12-initcapital/blob/main/contracts/core/InitCore.sol#L327).

Sponsor said that blacklisting flow will be as following.

*   Decrease collateral factor for blacklisted wLp until it becomes 0
*   then blacklist wLp

Considering this fact I realize that for liquidation this will not be an issue as wLp will have 0 collateralization power when it will be blacklisted. However it's still possible that some users will not decollateralize their wLp tokens yet for some reasom and thus they will not be able to withdraw them later.

### Impact

User can't withdraw previously deposited wLP tokens after they were blacklisted.

### Tools Used

VsCode

### Recommended Mitigation Steps

Even if wLP token is blacklisted now, you still should allow user to withdraw them. After all you have health check function that will guarantee that position has enough collateral.

**[fez-init (INIT) acknowledged and commented](https://github.com/code-423n4/2023-12-initcapital-findings/issues/13#issuecomment-1870294773):**
 > We will use unwhitelisting with care.


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | INIT Capital |
| Report Date | N/A |
| Finders | 0x73696d616f, rvierdiiev, ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-initcapital
- **GitHub**: https://github.com/code-423n4/2023-12-initcapital-findings/issues/13
- **Contest**: https://code4rena.com/reports/2023-12-initcapital

### Keywords for Search

`vulnerability`

