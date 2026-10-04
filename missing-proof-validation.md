---
# Core Classification
protocol: Linea Plonk Prover (Backend) and Plonk Verifier Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35066
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/linea-prover-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Missing Proof Validation

### Overview


The `Verify` function in the gnark library does not currently validate certain elements, such as polynomial openings, public witness values, and proof commitments. This could potentially leave the system vulnerable to attacks. While this is not a problem for bn curves, it should still be addressed for other curves in the library. A recent update has partially resolved this issue by validating that proof commitments are from the correct subgroup, but it does not check for valid field elements in polynomial openings and public witness values. This could still be exploited by passing a 256-bit value that is not a valid field element. It is recommended to introduce these checks to reduce the risk of attacks and comply with the Plonk specification.

### Original Finding Content

The [`Verify` function](https://github.com/Consensys/gnark/blob/e2040836eb41a40df04a4a3648764b07a0fa12a2/backend/plonk/bn254/verify.go#L46) does not validate the following:


* Whether the polynomial openings are valid field elements
* Whether the public witness values are valid field elements
* Whether the proof commitments are valid elliptic curve points
* Whether the proof commitments are on the correct subgroup


Fortunately, bn curves [do not have small subgroups](https://hackmd.io/@jpw/bn254#Subgroup-check-for-mathbb-G_1) (and therefore are not subject to small subgroup attacks), but this should be validated for the other curves in the library.


In the interest of reducing the attack surface and increasing compliance with the [Plonk specification](https://eprint.iacr.org/2019/953.pdf), consider introducing these checks.


***Update:** Partially resolved in [pull request \#11](https://github.com/ThomasPiellard/gnark-oz/pull/11).*


*The fix validates that the commitments from the proof are elements of the correct subgroup. It does not check that the openings and the public values are valid field elements. The rationale is that these checks are done implicitly in Gnark during instantiation.*


*However, the implicit checks can still be bypassed (e.g., if one passes a 256\-bit value with all the bits set as in `a := fr.Element{ 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff}`, that is still a valid 256\-bit constant, but is not a BN254 field element).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Linea Plonk Prover (Backend) and Plonk Verifier Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/linea-prover-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

