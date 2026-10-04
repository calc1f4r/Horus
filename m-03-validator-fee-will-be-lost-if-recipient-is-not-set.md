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
solodit_id: 34036
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

[M-03] Validator fee will be lost if recipient is not set

### Overview


This bug report discusses an issue with the `GaugeProxy::distributeToken` function that distributes rewards to gauges based on validator activity. The problem is that the code does not check if a `validatorFeeRecipient` has been set, which can result in the `fee` being burned (sent to the zero address) instead of being sent to the intended recipient. This bug has a high impact as it can lead to a loss of yield for validators, but its likelihood is low as it only occurs in a specific scenario. The recommendation is to add a check before transferring the `fee` to ensure that the `validatorFeeRecipient` is not set to the zero address.

### Original Finding Content

**Severity**

**Impact:**
High, as it will result in a loss of yield for a validator

**Likelihood:**
Low, as it requires a specific scenario

**Description**

In `GaugeProxy::distributeToken` rewards are distributed to gauges based on validator activity. Also some fee is taken, called a `validatorFee`, and sent to a different recipient for each validator. The problem is that the code doesn't check if a `validatorFeeRecipient` has been set - if it hasn't been then the `fee` would be burned (sent to the zero address).

**Recommendations**

Before doing `IERC20Metadata(tenet).transfer(validatorFeeRecipient[validators[i]], fee);` make sure to check if `validatorFeeRecipient[validators[i]] != address(0)` to not burn the `fee` sent.

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

