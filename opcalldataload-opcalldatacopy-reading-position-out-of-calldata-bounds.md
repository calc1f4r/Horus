---
# Core Classification
protocol: Polygon zkEVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21372
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-2-Spearbit-27-March.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-2-Spearbit-27-March.pdf
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
finders_count: 8
finders:
  - Thibaut Schaeffer
  - Alex Beregszaszi
  - Blockdev
  - Lucas Vella
  - Paweł Bylica
---

## Vulnerability Title

opCALLDATALOAD /opCALLDATACOPY reading position out of calldata bounds

### Overview


This bug report is about an issue with the check for input calldata offset being within calldata bounds. The check was done as txCalldataLen < offset, but in case offset == txCalldataLen, it proceeded to load the memory word at address corresponding to position calldata[txCalldataLen] (memory word at address 1024 + txCalldataLen / 32). The recommendation was to check offset < txCalldataLen instead. Polygon-Hermez implemented the optimization in the PR #242 and added a comment regarding out-of-bounds in calldata-returndata-code.zkasm#L38. Spearbit acknowledged this.

### Original Finding Content

## Severity: Critical Risk

## Context
- zkevm-rom:calldata-returndata-code.zkasm#L24
- zkevm-rom:calldata-returndata-code.zkasm#L128

## Description
The check for input calldata offset being within calldata bounds is done as `txCalldataLen < offset`. In case `offset == txCalldataLen`, it proceeds to load the memory word at the address corresponding to position `calldata[txCalldataLen]` (memory word at address `1024 + txCalldataLen / 32`).

## Recommendation
Check `offset < txCalldataLen`.

## Polygon-Hermez
Implemented optimization in the PR [#242](link-to-PR) and added a comment regarding out-of-bounds in `calldata-returndata-code.zkasm#L38`.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Polygon zkEVM |
| Report Date | N/A |
| Finders | Thibaut Schaeffer, Alex Beregszaszi, Blockdev, Lucas Vella, Paweł Bylica, Christian Reitwiessner, Andrei Maiboroda, Leo Alt |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-2-Spearbit-27-March.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-2-Spearbit-27-March.pdf

### Keywords for Search

`vulnerability`

