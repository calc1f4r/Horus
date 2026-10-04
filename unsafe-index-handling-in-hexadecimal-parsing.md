---
# Core Classification
protocol: Name Service (BNS) Contracts v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52504
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
source_link: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
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

Unsafe index handling in hexadecimal parsing

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `hexStringToBytes32` function in the **HexUtils** library does not properly validate the `idx` and `lastIdx` input indices. While it ensures that `lastIdx` does not exceed the string's length, it neglects to verify that `idx` is within bounds and that `lastIdx` is greater than `idx`. This insufficient validation can result in out-of-bounds memory access, leading to reverts or undefined behavior.

##### BVSS

[AO:A/AC:L/AX:M/R:N/S:U/C:N/A:L/I:L/D:N/Y:N (2.1)](/bvss?q=AO:A/AC:L/AX:M/R:N/S:U/C:N/A:L/I:L/D:N/Y:N)

##### Recommendation

The `hexStringToBytes32` function should implement comprehensive checks to validate input indices. It must ensure that `idx` is less than the string's length, `lastIdx` does not exceed the string's length, and `idx` is strictly less than `lastIdx`. These validations should be enforced before processing the input to prevent any potential memory errors and guarantee reliable execution.

##### Remediation

**SOLVED:** The **Beranames team** solved the issue in the specified commit id.

##### Remediation Hash

<https://github.com/Beranames/beranames-contracts-v2/pull/107/commits/b6a61b43d5874d0ffa35e1ddbd7eb723df913bd6>

##### References

src/resolver/libraries/HexUtils.sol#L19

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Name Service (BNS) Contracts v2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2

### Keywords for Search

`vulnerability`

