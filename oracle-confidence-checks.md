---
# Core Classification
protocol: Argo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48530
audit_firm: OtterSec
contest_link: https://argo.fi/
source_link: https://argo.fi/
github_link: github.com/argodao/argo-move.

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
finders_count: 3
finders:
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Oracle Confidence Checks

### Overview


The report highlights an issue with high oracle confidence values, which indicate a disagreement among providers on the actual price. This is particularly evident in Pyth, where confidence is measured as the difference between the 25th and 75th quartile and the median price. The report suggests that it is safer to ignore these values rather than using potentially inaccurate ones. The suggested remediation is to check the confidence of oracles, and the issue has been resolved in a patch with the code "2c31c5c" in the file "argo_engine/sources/engine_v1.move" written in the programming language RUST. The code checks for confidence values and returns if they exceed the maximum confidence value set by the oracle.

### Original Finding Content

## Oracle Confidence Value Analysis

High oracle confidence values indicate that providers disagree on the actual price. Pyth, for example, represents confidence as the difference between the 25/75th quartile and the median price. In this case, it’s safer to ignore the value than to use a potentially inaccurate value.

## Remediation
- Check the confidence of oracles.

## Patch
- Resolved in commit `2c31c5c`.

### Code Snippet
```rust
let confidence_bps = scale_ceil(conf, BPS_PRECISION, magnitude);
if (confidence_bps > oracle.max_conf_bps) {
    return;
};
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Argo |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec |

### Source Links

- **Source**: https://argo.fi/
- **GitHub**: github.com/argodao/argo-move.
- **Contest**: https://argo.fi/

### Keywords for Search

`vulnerability`

