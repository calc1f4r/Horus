---
# Core Classification
protocol: OpenVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53428
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/a88a1481-b269-4e1f-8ee3-f73afc20095c
source_link: https://cdn.cantina.xyz/reports/cantina_competition_openvm_january2025.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cergyk
---

## Vulnerability Title

Jalr imm_signis unconstrained 

### Overview


This bug report discusses an issue with the Jalr opcode circuit in a programming language called Rust. The circuit has a flag that is supposed to extend a 12-bit number, but the variable controlling this extension is not properly constrained. This means that the program flow can be changed by manipulating this variable. The report recommends adding a constraint to ensure that the variable is only set to 1 when the higher bit of the number is also 1. This issue has been fixed in a recent commit and the corresponding documentation has been updated. The fix has also been verified by Cantina Managed, a tool used to manage and verify code.

### Original Finding Content

## Context: core.rs#L143-L145

## Description
In the Jalr opcode circuit, there is a flag to sign extend the 12-bit immediate passed to the instruction:

```rust
// jalr/core.rs#L144
//@audit additional term because of sign extending the immediate
let imm_extend_limb = imm_sign * AB::F::from_canonical_u32((1 << 16) - 1);
let carry = (rs1_limbs_23 + imm_extend_limb + carry - to_pc_limbs[1]) * inv;
builder.when(is_valid).assert_bool(carry);
```

Unfortunately, `imm_sign` is not constrained, thus the prover can decide to make `imm_extend_limb` zero or `((1 << 16) - 1)` and change program flow.

## Recommendation
Consider adding a constraint asserting that `imm_sign` is 1 iff the higher bit of `imm` is 1:

```rust
+ self.range_bus
+ .range_check(imm - imm_sign * AB::F::from_canonical_u16(1 << 15), 15)
+ .eval(builder, is_valid);
```

## OpenVM
Fixed in commit `c5261bfa`, the fix updates the Jalr chip and the corresponding transpiler part to constrain the sign bit of the immediate through the field `g`. A new `ProcessedInstruction` struct was added so the core is able to send the `imm_sign` to the adapter. We assume that the transpiler correctly assigns the field `g` and we can constrain the `imm_sign` against the instruction field. The corresponding documentation was also updated.

## Cantina Managed
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | OpenVM |
| Report Date | N/A |
| Finders | cergyk |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_openvm_january2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/a88a1481-b269-4e1f-8ee3-f73afc20095c

### Keywords for Search

`vulnerability`

