---
# Core Classification
protocol: Avacloud
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56690
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-04-09-AvaCloud.md
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
  - Hexens
---

## Vulnerability Title

[ETRP-16] Missing Curve Validation in BabyJubjub Circom Implementation

### Overview


This bug report discusses an issue with the Circom implementation of BabyJubjub curve operations. The report states that the implementation does not check if points are valid before performing operations, which could lead to errors. It also mentions that there is a template called `BabyCheck()` that can verify curve membership, but it is not being used in operations like `BabyAdd()`, `BabyDbl()`, or `BabyPbk()`. The report suggests fixing this issue by adding `BabyCheck()` calls at the beginning of templates that handle curve points. The status of the bug is marked as fixed.

### Original Finding Content

**Severity:** Medium

**Path:** circom/components.circom, circom/circomlib/babyjub.circom

**Description:** The Circom implementation of BabyJubjub curve operations does not validate that points lie on the curve before performing operations. In Circom (`babyjub.circom`), while a `BabyCheck()` template exists that can verify curve membership, it's not used in operations like `BabyAdd()`, `BabyDbl()`, or `BabyPbk()`, potentially allowing operations with invalid points.
```
template CheckValue() {
    signal input value;
    signal input privKey;
    signal input valueC1[2];
    signal input valueC2[2];

    // Verify the value is less than the base order
    assert(value < 2736030358979909402780800718157159386076813972158567259200215660948447373041);

    component checkValue = ElGamalDecrypt();
    checkValue.c1[0] <== valueC1[0];
    checkValue.c1[1] <== valueC1[1];
    checkValue.c2[0] <== valueC2[0];
    checkValue.c2[1] <== valueC2[1];
    checkValue.privKey <== privKey;
    
    component valueToPoint = BabyPbk();
    valueToPoint.in <== value;

    valueToPoint.Ax === checkValue.outx;
    valueToPoint.Ay === checkValue.outy;
}
```
```
template BabyCheck() {
    signal input x;
    signal input y;

    signal x2;
    signal y2;

    var a = 168700;
    var d = 168696;

    x2 <== x*x;
    y2 <== y*y;

    a*x2 + y2 === 1 + d*x2*y2;
}
```

**Remediation:**  Integrate curve validation in all BabyJubjub operations by adding `BabyCheck()` calls at the beginning of templates that handle curve points.

**Status:**  Fixed


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Avacloud |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-04-09-AvaCloud.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

