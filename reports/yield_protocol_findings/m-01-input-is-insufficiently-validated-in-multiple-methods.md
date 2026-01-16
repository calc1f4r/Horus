---
# Core Classification
protocol: Vetenet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34034
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2023-12-01-veTenet.md
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
  - Pashov
---

## Vulnerability Title

[M-01] Input is insufficiently validated in multiple methods

### Overview


This bug report discusses an issue with insufficient input validation in multiple methods of the codebase. This can result in a high impact, such as loss of accrued yield for validators or denial of service for the protocol. However, the likelihood of this occurring is low as it requires a configuration error or malicious intent. The report recommends implementing stricter validation for certain input values to prevent these potential issues.

### Original Finding Content

**Severity**

**Impact:**
High, as it can result of loss of accrued yield for validators or DoS of the protocol

**Likelihood:**
Low, as it requires configuration error by `Governance` or `TLSDFactory` or them being malicious or compromised

**Description**

The input validation of multiple methods throughout the codebase is insufficient:

- In `RewardDistributor::setScanPeriod` if the `_newScanPeriod` argument is too big of a number it can result in a DoS in the `_distribute` method, and if it is too small it can result in lost unclaimed yield for validators
- In `GaugeProxy::setValidatorFee` if the `_fee` argument is more than `FEE_BASE` it will result in a DoS in `distributeToken` and also if it is equal to `FEE_BASE` it will result in the whole `rewardAmount` getting sent to the `validatorFeeRecipient` address
- In `TenetVesting::initialize` the `cliff`, `vestingPeriod` and `startTime` inputs are not properly validated and can contain too big values which can result in stuck funds in the contract if `revocable == false`

**Recommendations**

For the `scanPeriod`, make sure to not allow too big of a value and also to be certain that validators won't be using unclaimed yield. For the `validatorFee` cap it to some sensible value, possibly 10%. For the vesting parameters make sure that the `cliff` isn't too big, same for the `vestingPeriod` and also make sure that `startTime` isn't too further away in the future or already passed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Vetenet |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2023-12-01-veTenet.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

