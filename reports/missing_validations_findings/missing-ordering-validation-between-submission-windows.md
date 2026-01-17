---
# Core Classification
protocol: Powerloom L2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58822
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/powerloom-l-2/695c4ca5-2bab-42f2-b41d-bff9eec03f32/index.html
source_link: https://certificate.quantstamp.com/full/powerloom-l-2/695c4ca5-2bab-42f2-b41d-bff9eec03f32/index.html
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
finders_count: 4
finders:
  - Paul Clemson
  - Mustafa Hasan
  - Mostafa Yassin
  - Tim Sigl
---

## Vulnerability Title

Missing Ordering Validation Between Submission Windows

### Overview

See description below for full details.

### Original Finding Content

**File(s) affected:**`PowerloomDataMarket.sol`

**Description:**`PowerloomDataMarket`'s window update functions lack validation to maintain the required sequencing:

```
updateBatchSubmissionWindow()
updateSnapshotSubmissionWindow()
updateAttestationSubmissionWindow()
```

The submission windows must follow a specific order:

*   Snapshot window should be shorter than batch window
*   Batch window should be shorter than attestation window 
*   Attestation window must be longest to allow validators time to submit

Current implementation allows windows to be set in any order, which could:

*   Prevent validators from submitting attestations if attestation window is too short
*   Create timing conflicts between different submission phases
*   Break the intended sequence of the submission process

**Recommendation:** Add validation checks to ensure proper ordering between submission windows whenever any window duration is updated (snapshot < batch < attestation).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Powerloom L2 |
| Report Date | N/A |
| Finders | Paul Clemson, Mustafa Hasan, Mostafa Yassin, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/powerloom-l-2/695c4ca5-2bab-42f2-b41d-bff9eec03f32/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/powerloom-l-2/695c4ca5-2bab-42f2-b41d-bff9eec03f32/index.html

### Keywords for Search

`vulnerability`

