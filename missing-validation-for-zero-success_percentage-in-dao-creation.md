---
# Core Classification
protocol: XDAO
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61887
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
source_link: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.73
financial_impact: low

# Scoring
quality_score: 3.666666666666667
rarity_score: 4

# Context Tags
tags:
  - access_control
  - account_abstraction
  - auditing_and_logging

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - István Böhm
  - Andy Lin
  - Cameron Biniamow
---

## Vulnerability Title

Missing Validation for Zero `success_percentage` in DAO Creation

### Overview

See description below for full details.

### Original Finding Content

**Update**
The team addressed in: `a429b0c9ce78be9294a27934e1a184261b88917a`, `2255f30c7f9559ce225b407c26f6d816325d78f3`with the following explanation:

> Second commit (2255f30c7f9559ce225b407c26f6d816325d78f3) contains constants.fc update.

**File(s) affected:**`contracts/factory.fc`, `contracts/master.fc`

**Description:** In both the `factory`’s `op::create_master` and the `master`’s `op::change_success_percentage`, the code checks that `success_percentage` does not exceed 100%, but it does not enforce a minimum above zero.

Generally, we should not expect a proposal to pass with zero votes.

**Recommendation:** Add a validation such as `throw_if(error::value_too_low, success_percentage == 0)` in both `op::create_master` and `op::change_success_percentage` to ensure `success_percentage >= 1`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 3.666666666666667/5 |
| Rarity Score | 4/5 |
| Audit Firm | Quantstamp |
| Protocol | XDAO |
| Report Date | N/A |
| Finders | István Böhm, Andy Lin, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html

### Keywords for Search

`Access Control, Account Abstraction, Auditing and Logging`

