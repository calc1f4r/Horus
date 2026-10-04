---
# Core Classification
protocol: Optimism
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36604
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-optimism
source_link: https://code4rena.com/reports/2024-07-optimism
github_link: https://github.com/code-423n4/2024-07-optimism-findings/issues/82

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - RadiantLabs
  - zraxx
---

## Vulnerability Title

[M-02] Missing address check for instructions LH and LHU

### Overview


The bug report is about a problem in the code for the MIPS VM in the Optimism project. The issue is that the code does not check for half-word alignment, which is a requirement according to the MIPS specification. This could potentially lead to an Address Error exception. The recommended mitigation step is to check the address and revert if the least-significant bit is non-zero. The issue has been confirmed by the project team and is considered a valid Medium priority.

### Original Finding Content


<https://github.com/code-423n4/2024-07-optimism/blob/main/packages/contracts-bedrock/src/cannon/MIPS.sol#L990-L993><br><https://github.com/code-423n4/2024-07-optimism/blob/main/packages/contracts-bedrock/src/cannon/MIPS.sol#L1008-L1011>

### Impact

Instruction processing cannot detect problems in time.

### Details

According to [this](<https://www.cs.cmu.edu/afs/cs/academic/class/15740-f97/public/doc/mips-isa.pdf>), page 99, Section Restrictions, the address must be naturally aligned. If the least-significant bit of the address is non-zero, an Address Error exception occurs. However, in the contract, the address is not checked.

### Tools Used

Vscode

### Recommended Mitigation Steps

Check the address and when the least-significant bit of the address is non-zero, revert.

**[clabby (Optimism) confirmed and commented](https://github.com/code-423n4/2024-07-optimism-findings/issues/82#issuecomment-2260777993):**
 > This report is valid. The `MIPS` VM currently does not check for half-word alignment within the `LH` and `LHU` instruction implementations. Every piece of memory is guaranteed to be 4-byte aligned via the `0xFFFFFFFC` mask prior to the `readMem` call, but the ISA specification explicitly states a requirement for 2-byte alignment for these instructions.

**[obront (judge) commented](https://github.com/code-423n4/2024-07-optimism-findings/issues/82#issuecomment-2260798790):**
 > @clabby - If I'm understanding correctly, you're saying that there is no possible risk to this in Optimism's context, but that it is confirmed that it's not following the MIPS spec? If that's the case, I will plan to downgrade to low/QA.

**[clabby (Optimism) commented](https://github.com/code-423n4/2024-07-optimism-findings/issues/82#issuecomment-2260803528):**
 > @obront, I can confirm that we've seen no adverse effects from the out-of-spec implementation of these instructions to date. Though the surface is too large to make a blanket statement on there being no possible risk. We do intend to fix this and align with the MIPS specification.

**[obront (judge) commented](https://github.com/code-423n4/2024-07-optimism-findings/issues/82#issuecomment-2264466605):**
 > Because this is a confirmed divergence from the spec and we don't have a firm guarantee that it won't be reached in the program, I will be considering it a valid Medium.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Optimism |
| Report Date | N/A |
| Finders | RadiantLabs, zraxx |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-optimism
- **GitHub**: https://github.com/code-423n4/2024-07-optimism-findings/issues/82
- **Contest**: https://code4rena.com/reports/2024-07-optimism

### Keywords for Search

`vulnerability`

