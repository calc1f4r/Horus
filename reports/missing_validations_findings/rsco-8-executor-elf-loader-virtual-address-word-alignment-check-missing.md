---
# Core Classification
protocol: Risc Zero
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53503
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-31-Risc Zero.md
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
  - Hexens
---

## Vulnerability Title

[RSCO-8] Executor ELF loader virtual address word alignment check missing

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** binfmt/src/elf.rs

**Description:**

The function load_elf() parses the ELF binary, loads the memory segments, and does sanity checks on the ELF structure, such as checking that the binary is 32-bit, RISC-V machine type, max memory checks, etc. Nonetheless, it fails to check that the section's virtual address (vaddr) is aligned to word size (4 bytes by default). 

This leads to situations where the page size can become bigger than 1024 bytes (1025-1027 bytes). Although the executor will fail to execute such a program and panic out the process, we are unaware of the circuit behaviour. 

```
            let vaddr: u32 = segment.p_vaddr.try_into()?;   
            let offset: u32 = segment.p_offset.try_into()?;
            for i in (0..mem_size).step_by(4) {
                let addr = vaddr.checked_add(i).context("Invalid segment vaddr")?;
                if i >= file_size {
                    // Past the file size, all zeros.
                    image.insert(addr, 0);
                } else {
                    let mut word = 0;
                    // Don't read past the end of the file.
                    let len = std::cmp::min(file_size - i, 4);
                    for j in 0..len {
                        let offset = (offset + i + j) as usize;
                        let byte = input.get(offset).context("Invalid segment offset")?;
                        word |= (*byte as u32) << (j * 8);
                    }
                    image.insert(addr, word);
                }
            }
```

**Remediation:**  Add a check to ensure that the ELF sections' virtual addresses are all aligned by word size.

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Risc Zero |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-31-Risc Zero.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

