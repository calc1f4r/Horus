---
# Core Classification
protocol: Omni Halo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41499
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf
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
finders_count: 3
finders:
  - Dtheo
  - Shotes
  - Justin Traglia
---

## Vulnerability Title

guageBuffered() contains unsafe read of b.buffer

### Overview


A medium risk bug was reported in the buffer.go file, specifically in lines 121-136. The issue is that the buffer is being accessed by the guageBuffered() function, but it should be protected by a mutex (a type of lock). This could lead to memory corruption in Omni's fee oracle. The recommendation is to create a thread safe version of the guageBuffered() method. The bug has been fixed in the 8cc196bb commit and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
`buffer.go#L121-L136`

## Description
`b.buffer` is passed to `guageBuffered()` which references the buffer as `prices`. Access of this buffer should be protected by a mutex, in this case a read lock. This is called periodically in the `(b *Buffer) stream ticker` cadence. This opens up Omni's fee oracle to memory corruption.

## Recommendation
Create a thread safe `guageBuffered()` method.

## Omni
Fixed in `8cc196bb` as recommended.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Omni Halo |
| Report Date | N/A |
| Finders | Dtheo, Shotes, Justin Traglia |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf

### Keywords for Search

`vulnerability`

