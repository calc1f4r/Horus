---
# Core Classification
protocol: Solana Core ELF Parser
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48747
audit_firm: OtterSec
contest_link: https://solana.com/
source_link: https://solana.com/
github_link: https://github.com/solana-labs/rbpf/pull/348

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
  - Harrison Green
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Off-by-one error in section size check

### Overview


The ELF Parser is incorrectly reporting sections as OutOfBounds if the section ends at the end of the ELF file. This means that a valid Solana ELF file may be rejected by the Solana runtime. To fix this issue, the range check needs to be modified to use > instead of >=. This bug has been addressed in Issue 365 and has been fixed in the patch 30e2c96.

### Original Finding Content

## ELF Parser Bug Report

The ELF Parser incorrectly reports sections as OutOfBounds if the section ends at the end of the ELF file.

```rust
rbpf@7f801c2:src/elf_parser/mod.rs RUST
170 if section_range.end >= elf_bytes.len() {
171     return Err(ElfParserError::OutOfBounds);
172 }
```

The impact of this bug is that a valid Solana ELF may be rejected by the Solana runtime.

## Remediation

Modify the range check to use `>` instead of `>=`.

## Patch

- Issue 365; fixed in commit `30e2c96`.

© 2022 OtterSec LLC. All Rights Reserved.  
8 / 16

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Solana Core ELF Parser |
| Report Date | N/A |
| Finders | Harrison Green, Robert Chen, OtterSec |

### Source Links

- **Source**: https://solana.com/
- **GitHub**: https://github.com/solana-labs/rbpf/pull/348
- **Contest**: https://solana.com/

### Keywords for Search

`vulnerability`

