---
# Core Classification
protocol: Pendle Strategies V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51508
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/jigsaw-finance/pendle-strategies-v1
source_link: https://www.halborn.com/audits/jigsaw-finance/pendle-strategies-v1
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

Missing input validation at initialization

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `initialize()` function lacks proper input validation for contract parameters. The address parameter `jigsawRewardToken` is not validated against the zero address. Additionally, the `jigsawRewardDuration` parameter lacks bounds checking, which could allow initialization with zero value or setting values beyond reasonable thresholds.

##### BVSS

[AO:S/AC:L/AX:L/R:N/S:U/C:N/A:N/I:C/D:N/Y:N (2.0)](/bvss?q=AO:S/AC:L/AX:L/R:N/S:U/C:N/A:N/I:C/D:N/Y:N)

##### Recommendation

Add zero-address validation checks for all address parameters in the `initialize()` function and proper threshold validation for the `jigsawRewardDuration` parameter.

##### Remediation

**SOLVED:** The **Jigsaw Protocol team** solved this finding in commit `6173cc1` by adding validation checks for all addresses except for the `jigsawRewardDuration` parameter and stated the following rationale:

*This is intentional as we might want to be able to set* `jigsawRewardDuration` *equal to zero in some cases. Requiring that* `jigsawRewardDuration` *will always not be 0 would break product’s requirements. And in other hand we couldn’t come up with acceptable «upper limit» for input validation in case of* `jigsawRewardDuration`.

##### Remediation Hash

<https://github.com/jigsaw-finance/jigsaw-strategies-v1/pull/39/commits/6173cc193336b2b21ab90d42e33f9891e216eff8>

##### References

[jigsaw-finance/jigsaw-strategies-v1/src/pendle/PendleStrategy.sol#L169-L207](https://github.com/jigsaw-finance/jigsaw-strategies-v1/blob/9ecef78ef8cb421640c0b3bb449b3fa43ce35f5a/src/pendle/PendleStrategy.sol#L169-L207)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Pendle Strategies V1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/jigsaw-finance/pendle-strategies-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/jigsaw-finance/pendle-strategies-v1

### Keywords for Search

`vulnerability`

