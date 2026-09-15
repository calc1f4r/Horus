---
# Core Classification
protocol: Euler Labs - Euler Price Oracle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35788
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf
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
finders_count: 5
finders:
  - Christos Pap
  - M4rio.eth
  - Christoph Michel
  - David Chaparro
  - Emanuele Ricci
---

## Vulnerability Title

Single-step governance transfer can be risky

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
`Governable.sol#L39-L41`

## Description
`Governable.sol` implements the role of governor, which performs relevant actions like setting oracles for different assets and a possible fallback oracle. It uses a single-step role transfer design, which adds the risk of setting an unwanted role owner by accident. If the ownership transfer is not done with excessive care, it can be lost forever.

## Recommendation
Consider using a two-step ownership transfer mechanism for this critical governor change. This would avoid typos, "fat finger" mistakes, and transfers to the default address (0) value. Additionally, consider using an explicit `renounceOwnership` method to enable the expected renounce method. Some good implementations of the two-step ownership transfer pattern can be found at Open Zeppelin's **Ownable2Step** or Synthetic's **Owned**.

## Euler
Acknowledged. Won't fix.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Euler Labs - Euler Price Oracle |
| Report Date | N/A |
| Finders | Christos Pap, M4rio.eth, Christoph Michel, David Chaparro, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf

### Keywords for Search

`vulnerability`

