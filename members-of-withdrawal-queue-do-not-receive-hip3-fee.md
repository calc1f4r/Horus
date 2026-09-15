---
# Core Classification
protocol: Kinetiq LST Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63993
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
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
finders_count: 4
finders:
  - 0xRajeev
  - Kamensec
  - Optimum
  - Rvierdiiev
---

## Vulnerability Title

Members of withdrawal queue do not receive HIP3 fee

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
(No context files were provided by the reviewer)

## Description
When fees are distributed using the `stakeFees()` function, the `_exGhostLST` supply is increased based on the stake amount, while new `exLST` tokens are not minted. As a result, the `exLST : _exGhostLST` rate decreases, and the Hype share of active stakers increases in value.

When a withdrawal enters the blocking queue, some amount of `exLST` is burned and the corresponding `_exGhostLST` shares are transferred to the queue. Once this happens, subsequent `stakeFees()` calls do not increase the Hype value for users in the withdrawal queue, because their `_exGhostLST` balance is fixed and does not grow. Therefore, queued members do not receive fees earned by the deployed market during the time they are waiting.

## Recommendation
As this is a known limitation, it is recommended to document the behavior clearly so users understand that fees accumulated while in the withdrawal queue will not be attributed to them.

## Kinetiq
Fixed in PR 52.

## Spearbit
Fix verified. The team has added a comment that documents the problem.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Kinetiq LST Protocol |
| Report Date | N/A |
| Finders | 0xRajeev, Kamensec, Optimum, Rvierdiiev |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf

### Keywords for Search

`vulnerability`

