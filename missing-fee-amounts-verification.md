---
# Core Classification
protocol: Inception LRT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51627
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/tagus/inception-lrt
source_link: https://www.halborn.com/audits/tagus/inception-lrt
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
  - Halborn
---

## Vulnerability Title

Missing fee amounts verification

### Overview

See description below for full details.

### Original Finding Content

##### Description

In the `flashWithdraw()` function from the `InceptionVault` contract, the `fee` and `protocolWithdrawalFee` variables are not verified to be greater than zero. Although with the current implementation, it is highly unlikely to have a fee value of zero (for example, in cases where the `targetCapacity` value is set to a very low value), this oversight could allow a user the execution of flash withdrawals without paying the expected fee.

##### BVSS

[AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:L/Y:N (2.5)](/bvss?q=AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:L/Y:N)

##### Recommendation

It is recommended to add a check to ensure that the `fee` and `protocolWithdrawalFee` variables are greater than zero before proceeding with the flash withdrawal.

Remediation Plan
----------------

**SOLVED:** The **Tagus Labs team** has addressed the finding in commit `0229f48e38eacf23baa53c33190c968c8d2e324f` by following the mentioned recommendation.

##### Remediation Hash

<https://github.com/inceptionlrt/smart-contracts/commit/0229f48e38eacf23baa53c33190c968c8d2e324f>

##### References

InceptionVault.sol#L287-L314

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Inception LRT |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/tagus/inception-lrt
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/tagus/inception-lrt

### Keywords for Search

`vulnerability`

