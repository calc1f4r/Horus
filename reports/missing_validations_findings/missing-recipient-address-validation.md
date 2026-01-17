---
# Core Classification
protocol: Camp - Re-Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62792
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/camp-re-audit/2a90a14d-4635-462c-905c-0b444e0d8cf8/index.html
source_link: https://certificate.quantstamp.com/full/camp-re-audit/2a90a14d-4635-462c-905c-0b444e0d8cf8/index.html
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
finders_count: 2
finders:
  - Paul Clemson
  - Darren Jensen
---

## Vulnerability Title

Missing Recipient Address Validation

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `74ef2d50b843fd5b4df2d80d37db62472c3dcf08`.

**File(s) affected:**`contracts/CampTimelockEscrow.sol`

**Description:** In `bridgeOut()`, the `_to` parameter specifies the recipient address. However, there is no check to ensure `_to` is not the zero address.

**Recommendation:** Add a validation to revert if `_to` is the zero address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Camp - Re-Audit |
| Report Date | N/A |
| Finders | Paul Clemson, Darren Jensen |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/camp-re-audit/2a90a14d-4635-462c-905c-0b444e0d8cf8/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/camp-re-audit/2a90a14d-4635-462c-905c-0b444e0d8cf8/index.html

### Keywords for Search

`vulnerability`

