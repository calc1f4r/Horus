---
# Core Classification
protocol: Linea Plonk Verifier
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26830
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/06/linea-plonk-verifier/
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.40
financial_impact: medium

# Scoring
quality_score: 2
rarity_score: 4

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  -  Tejaswa Rastogi and David Pearce

  - Rai Yang
---

## Vulnerability Title

Allowing Program Execution Even After a Failed Step May Lead to Unnecessary Wastage of Gas

### Overview


A bug report has been filed regarding the Verifier algorithm in the zkEVM Operator. The Verifier stores the result of computations obtained in different steps, and if the final result is **1** or **true**, it verifies the proof. However, it is wasteful for the zkEVM Operator to continue with the rest of the operations if any step results into a failure, as the proof verification will be failing anyways. The functions which update the `state_success` state are: point_mul, point_add, point_acc_mul, verify_quotient_poly_eval_at_zeta, and batch_verify_multi_points. The recommendation is to revert the moment any step fails.

### Original Finding Content

#### Description


The Verifier stores the result of computations obtained in different steps of Verifier algorithm. The result is stored at a designated memory location `state_success` by doing bitwise **&** with the previous result, and if the final result at the end of all the steps comes out to be **1** or **true**, it verifies the proof.


However, it makes no sense to continue with the rest of the operations, if any step results into a failure, as the proof verification will be failing anyways. But, it will result into wastage of more gas for the zkEVM Operator.


The functions which update the `state_success` state are:


* **point\_mul**
* **point\_add**
* **point\_acc\_mul**
* **verify\_quotient\_poly\_eval\_at\_zeta**
* **batch\_verify\_multi\_points**


#### Recommendation


It would be best to revert, the moment any step fails.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2/5 |
| Rarity Score | 4/5 |
| Audit Firm | ConsenSys |
| Protocol | Linea Plonk Verifier |
| Report Date | N/A |
| Finders |  Tejaswa Rastogi and David Pearce
, Rai Yang |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/06/linea-plonk-verifier/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

